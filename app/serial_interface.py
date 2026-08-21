"""
Title: Description
"""

import serial 

PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

class PicoSerial:
    def __init__(self, port=PORT, baud_rate=BAUD_RATE):
        self.ser = serial.Serial(port, baud_rate)
        self.current_sampling_rate = None
        print("Connected to Pico")

    def set_sampling_rate(self, rate):
        command = f"RATE {rate}\n"
        self.ser.write(command.encode())

    def process_line(self, line):
        if line.startswith("RATE"):
            rate = int(line[5:])
            return "RATE", rate

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

        while True:

            line = self.ser.readline().decode().strip()

            message_type, value = self.process_line(line)

            if message_type == "RATE":

                self.current_sampling_rate = value

                print(
                    "Pico sampling rate:",
                    self.current_sampling_rate,
                    "Hz"
                )

            elif message_type == "START":

                break


        while True:

            line = self.ser.readline().decode().strip()

            message_type, value = self.process_line(line)

            if message_type == "SAMPLE":

                samples.append(value)

            elif message_type == "END":

                break

            elif message_type == "RATE":

                self.current_sampling_rate = value

                print(
                    "Pico sampling rate:",
                    self.current_sampling_rate,
                    "Hz"
                )


        return samples, self.current_sampling_rate