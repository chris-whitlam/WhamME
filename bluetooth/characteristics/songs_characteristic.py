import dbus
import json
from bluetooth.service import Characteristic

from bluetooth.descriptors.songs_descriptor import SongsDescriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

SONGS_CHARACTERISTIC_UUID = "00000005-710e-4a5b-8d75-3e5b444bc3cf"

class SongsCharacteristic(Characteristic):
    def __init__(self, service):
        self.notifying = False

        Characteristic.__init__(
                self, SONGS_CHARACTERISTIC_UUID,
                ["read"], service)
        self.add_descriptor(SongsDescriptor(self))

    def get_songs(self):
        f = open('./data/songs.json')
        songs = json.load(f)
        f.close()

        data = []
        for s_id, s_info in songs.items():
            data.append({ "id": s_id, "name": s_info['name'], "bpm": s_info['bpm'] })
        
        value = []
        string_data = json.dumps(data)
        for c in str(string_data):
            value.append(dbus.Byte(c.encode()))

        return value

    def set_songs_callback(self):
        if self.notifying:
            value = self.get_songs()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_songs()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_songs_callback)

    def WriteValue(self, value, options):
        return

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_songs()

        return value