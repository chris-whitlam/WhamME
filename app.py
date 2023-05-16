#!/usr/bin/python3

from bluetooth.advertisement import Advertisement
from bluetooth.service import Application, Service

from bluetooth.characteristics.program_characteristic import ProgramCharacteristic
from bluetooth.characteristics.expression_characteristic import ExpressionCharacteristic
from bluetooth.characteristics.song_characteristic import SongCharacteristic
from bluetooth.characteristics.songs_characteristic import SongsCharacteristic
from bluetooth.characteristics.update_song_characteristic import UpdateSongCharacteristic

from midi.midi_service import MidiService

LOCAL_NAME = "WhamME"
WHAMME_SERVICE_UUID = "00000001-710e-4a5b-8d75-3e5b444bc3cf"

class WhamMEAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("WhamME")
        self.include_tx_power = True

class WhamMEService(Service):
    def __init__(self, index, midi_service):
        self.midi_service = midi_service
        Service.__init__(self, index, WHAMME_SERVICE_UUID, True)
        self.add_characteristic(ProgramCharacteristic(self, self.midi_service))
        self.add_characteristic(ExpressionCharacteristic(self, self.midi_service))
        self.add_characteristic(SongCharacteristic(self, self.midi_service))
        self.add_characteristic(SongsCharacteristic(self))
        self.add_characteristic(UpdateSongCharacteristic(self))

MIDI_PORT='MIDI 1'
midi_service = MidiService(MIDI_PORT)

app = Application()
app.add_service(WhamMEService(0, midi_service))
app.register()

adv = WhamMEAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    midi_service.close_port()
    app.quit()
