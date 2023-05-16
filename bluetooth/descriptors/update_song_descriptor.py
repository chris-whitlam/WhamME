import dbus
from bluetooth.service import Descriptor

class UpdateSongDescriptor(Descriptor):
    UPDATE_SONG_DESCRIPTOR_UUID = "2905"
    UPDATE_SONG_DESCRIPTOR_VALUE = "Update Song"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.UPDATE_SONG_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.UPDATE_SONG_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value