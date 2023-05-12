import dbus
from bluetooth.service import Characteristic

from bluetooth.descriptors.expression_descriptor import ExpressionDescriptor

from midi.midi_service import MidiService

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

EXPRESSION_CHARACTERISTIC_UUID = "00000003-710e-4a5b-8d75-3e5b444bc3cf"

class ExpressionCharacteristic(Characteristic):
    def __init__(self, service, midi_service: MidiService):
        self.current_expression = 100
        self.notifying = False
        self.midi_service = midi_service

        Characteristic.__init__(
                self, EXPRESSION_CHARACTERISTIC_UUID,
                ["read", "write"], service)
        self.add_descriptor(ExpressionDescriptor(self))

    def get_expression(self):
        value = []

        for c in str(self.current_expression):
            value.append(dbus.Byte(c.encode()))

        return value

    def set_expression_callback(self):
        if self.notifying:
            value = self.get_expression()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_expression()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_expression_callback)

    def WriteValue(self, value, options):
        str_value = '%s' % ''.join([str(v) for v in value])
        str_value = str_value.replace('"', "")
        print("Expression set to: %s" % str_value)
        int_value = int(str_value)
        self.midi_service.set_expression(int_value)
        self.current_expression = str_value
        

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_expression()

        return value