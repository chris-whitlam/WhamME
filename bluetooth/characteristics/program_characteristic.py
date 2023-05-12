import dbus
from bluetooth.service import Characteristic

from bluetooth.descriptors.program_descriptor import ProgramDescriptor

from midi.midi_service import MidiService

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

PROGRAM_CHARACTERISTIC_UUID = "00000002-710e-4a5b-8d75-3e5b444bc3cf"

class ProgramCharacteristic(Characteristic):
    def __init__(self, service, midi_service: MidiService):
        self.current_program = 43
        self.notifying = False
        self.midi_service = midi_service

        Characteristic.__init__(
                self, PROGRAM_CHARACTERISTIC_UUID,
                ["read", "write"], service)
        self.add_descriptor(ProgramDescriptor(self))

    def get_program(self):
        value = []

        for c in str(self.current_program):
            value.append(dbus.Byte(c.encode()))

        return value

    def set_program_callback(self):
        if self.notifying:
            value = self.get_program()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_program()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_program_callback)

    def WriteValue(self, value, options):
        str_value = '%s' % ''.join([str(v) for v in value])
        str_value = str_value.replace('"', "")
        print("Program set to: %s" % str_value)
        int_value = int(str_value)
        self.midi_service.set_program(int_value)
        self.current_program = str_value
        

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_program()

        return value