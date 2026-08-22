"""
Serial Interface between Python and C++
"""

import serial


PORT = "/dev/ttyACM0"
BAUD_RATE = 115200


class PicoSerial:

    def __init__(self, port=PORT, baud_rate=BAUD_RATE):

        self.ser = serial.Serial(port, baud_rate)

        self.current_sampling_rate = None
        self.actual_sampling_rate = None

        print("Connected to Pico")


    def set_sampling_rate(self, rate):

        command = f"RATE {rate}\n"

        self.ser.write(command.encode())


    def process_line(self, line):

        if line.startswith("RATE "):

            rate = int(line[5:])

            return "RATE", rate


        if line.startswith("ACTUAL_RATE "):

            rate = int(line[12:])

            return "ACTUAL_RATE", rate


        if line == "START":

            return "START", None


        if line == "END":

            return "END", None


        try:

            sample = int(line)

            return "SAMPLE", sample

        except ValueError:

            return None, None


    def read_buffer(self):

        samples = []

        # Wait for the beginning of the Pico transmission
        while True:

            line = self.ser.readline().decode().strip()

            message_type, value = self.process_line(line)


            if message_type == "RATE":

                self.current_sampling_rate = value

                print(
                    "Pico requested sampling rate:",
                    self.current_sampling_rate,
                    "Hz"
                )


            elif message_type == "ACTUAL_RATE":

                self.actual_sampling_rate = value

                print(
                    "Pico actual sampling rate:",
                    self.actual_sampling_rate,
                    "Hz"
                )


            elif message_type == "START":

                break


        # Read waveform samples
        while True:

            line = self.ser.readline().decode().strip()

            message_type, value = self.process_line(line)


            if message_type == "SAMPLE":

                samples.append(value)


            elif message_type == "END":

                break


            elif message_type == "RATE":

                self.current_sampling_rate = value


            elif message_type == "ACTUAL_RATE":

                self.actual_sampling_rate = value


        return (
            samples,
            self.current_sampling_rate,
            self.actual_sampling_rate
        )