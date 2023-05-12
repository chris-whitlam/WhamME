import dbus
from bluetooth.service import Descriptor

class SongDescriptor(Descriptor):
    SONG_DESCRIPTOR_UUID = "2903"
    SONG_DESCRIPTOR_VALUE = "Song"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.SONG_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.SONG_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value