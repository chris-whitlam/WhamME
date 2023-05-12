import dbus
from time import sleep
from threading import Event, Thread

from bluetooth.service import Characteristic

from bluetooth.descriptors.song_descriptor import SongDescriptor

from midi.midi_service import MidiService

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

SONG_CHARACTERISTIC_UUID = "00000004-710e-4a5b-8d75-3e5b444bc3cf"

# class SongThread(threading.Thread):
#     def __init__(self, threadID, name, midi_service: MidiService, file_path):
#         threading.Thread.__init__(self)
#         self.th
#         self.midi_service = midi_service
#         self.file_path = file_path
    
#     def run(self):
#         self.midi_service(self.file_path)

class SongCharacteristic(Characteristic):
    def __init__(self, service, midi_service: MidiService):
        self.current_song = ''
        self.notifying = False
        self.midi_service = midi_service
        self.current_song_thread = None
        self.stop_playback_event = Event()

        Characteristic.__init__(
                self, SONG_CHARACTERISTIC_UUID,
                ["read", "write"], service)
        self.add_descriptor(SongDescriptor(self))

    def get_song(self):
        value = []

        for c in str(self.current_song):
            value.append(dbus.Byte(c.encode()))

        return value

    def set_song_callback(self):
        if self.notifying:
            value = self.get_song()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_song()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_song_callback)

    def WriteValue(self, value, options):
        str_value = '%s' % ''.join([str(v) for v in value])
        str_value = str_value.replace('"', "")
        print("Song set to: %s" % str_value)
        self.stop_playback_event.clear()
        if (self.current_song_thread is not None and self.current_song_thread.is_alive()):
            self.stop_playback_event.set()
            self.current_song_thread.join()

        self.current_song_thread = Thread(
            target=self.midi_service.play_midi_file, 
            args=(self.stop_playback_event,)
        )

        self.current_song_thread.start()
        self.current_song = str_value

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_song()

        return value