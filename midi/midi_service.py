import mido
from threading import Event
from time import sleep

class MidiService:
  def __init__(self, portName):
    self.portName = portName
    self.connect(self.portName)

  def connect(self, portName):
    outputDevices = mido.get_output_names()
    print(outputDevices)

    for deviceName in outputDevices:
      if (portName in deviceName):
        self.port = mido.open_output(deviceName)
        return

    raise Exception(portName + ' not found in avaliable ports', outputDevices)

  def set_program(self, value):
    msg = mido.Message('program_change', program=value)
    self.__send_message(msg)

  def set_expression(self, value):
    if (value < 0 or value > 127):
      raise ValueError('Expression value must be between 0 and 127')

    msg = mido.Message('control_change', control=value)
    self.__send_message(msg)

  def play_midi_file(self, event: Event):
      mid = mido.MidiFile('./data/Map_Of_The_Problematique.mid')

      for msg in mid.play():
        if (event.is_set()):
          break
        self.__send_message(msg)

  def __send_message(self, msg):
    self.port.send(msg)
    
