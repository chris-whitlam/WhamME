import dbus
from bluetooth.service import Descriptor

class SongsDescriptor(Descriptor):
    SONGS_DESCRIPTOR_UUID = "2904"
    SONGS_DESCRIPTOR_VALUE = "Songs"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.SONGS_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.SONGS_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value