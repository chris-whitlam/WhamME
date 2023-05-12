import dbus
from bluetooth.service import Descriptor

class ProgramDescriptor(Descriptor):
    PROGRAM_DESCRIPTOR_UUID = "2901"
    PROGRAM_DESCRIPTOR_VALUE = "Program"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.PROGRAM_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.PROGRAM_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value