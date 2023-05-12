import dbus
from bluetooth.service import Descriptor

class ExpressionDescriptor(Descriptor):
    EXPRESSION_DESCRIPTOR_UUID = "2902"
    EXPRESSION_DESCRIPTOR_VALUE = "Expression"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.EXPRESSION_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.EXPRESSION_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value