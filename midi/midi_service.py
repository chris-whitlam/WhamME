import mido
from threading import Event
from time import sleep, time


class MidiService:
    def __init__(self, portName):
        self.portName = portName
        self.connect(self.portName)

    def connect(self, portName):
        outputDevices = mido.get_output_names()
        print(outputDevices)

        for deviceName in outputDevices:
            if portName in deviceName:
                self.port = mido.open_output(deviceName)
                return

        raise Exception(portName + " not found in avaliable ports", outputDevices)

    def set_program(self, value):
        msg = mido.Message("program_change", program=value)
        self.__send_message(msg)

    def set_expression(self, value):
        if value < 0 or value > 127:
            raise ValueError("Expression value must be between 0 and 127")

        msg = mido.Message("control_change", control=11, value=value)
        self.__send_message(msg)

    def play_midi_file(self, event: Event, file_name, bpm: int):
        file_path = "./data/" + file_name
        mid = mido.MidiFile(file_path)

        self._countdown(bpm)

        for msg in self.play(mid, bpm):
            if event.is_set():
                break

            self.__send_message(msg)

    def _countdown(self, bpm: int):
        length_of_beat = 60.0 / bpm
        self.set_program(33)
        sleep(length_of_beat)
        self.set_program(32)
        sleep(length_of_beat)
        self.set_program(33)
        sleep(length_of_beat)
        self.set_program(32)
        sleep(length_of_beat)

    def play(self, mid, bpm=120, meta_messages=False):
        start_time = time()
        input_time = 0.0

        # default bpm/tempo
        track_tempo = 120
        time_multiplier = track_tempo / bpm

        # search midi file for tempo/bpm
        for msg in mid:
            if isinstance(msg, mido.MetaMessage) and not meta_messages:
                if msg.dict()["type"] == "set_tempo":
                    track_tempo = int(mido.tempo2bpm(msg.dict()["tempo"]))
                    time_multiplier = track_tempo / bpm
                    break

        for msg in mid:
            time_multiplier = track_tempo / bpm
            input_time += msg.time * time_multiplier

            playback_time = time() - start_time
            duration_to_next_event = input_time - playback_time

            if duration_to_next_event > 0.0:
                sleep(duration_to_next_event)

            # Update tempo/bpm incase changes throughout song
            if isinstance(msg, mido.MetaMessage) and not meta_messages:
                if msg.dict()["type"] == "set_tempo":
                    track_tempo = int(mido.tempo2bpm(msg.dict()["tempo"]))
                    time_multiplier = track_tempo / bpm
                continue
            else:
                yield msg

    def close_port(self):
        self.port.close()

    def __send_message(self, msg):
        self.port.send(msg)
