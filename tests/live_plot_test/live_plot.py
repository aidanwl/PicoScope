"""
Live Plot: Reads serial outputs, fills a sample array, and then plots the adc readings as voltages
"""

import serial
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
BUFFER_SIZE = 1000

ser = serial.Serial(PORT, BAUD_RATE)

print("Connected to Pico")

# Config
current_sampling_rate = None

def set_sampling_rate(rate):
    command = f"RATE {rate}\n"
    ser.write(command.encode())

# Standardize lines from Pico to (TYPE, VALUE) format
def process_serial_line(line):
    if line.startswith("RATE"):
        rate = int(line[5:])
        return "RATE", rate

    if line == "START":
        return "START", None

    if line == "END":
        return "END", None

    # If not command, assume it is ADC sample

    try:
        sample = int(line)
        return "SAMPLE", sample

    except ValueError:
        return None, None

def read_buffer():

    global current_sampling_rate

    samples = []

    while True:

        line = ser.readline().decode().strip()

        message_type, value = process_serial_line(line)

        if message_type == "RATE":

            current_sampling_rate = value

            print(
                "Pico sampling rate:",
                current_sampling_rate,
                "Hz"
            )

        elif message_type == "START":

            break


    while True:

        line = ser.readline().decode().strip()

        message_type, value = process_serial_line(line)

        if message_type == "SAMPLE":

            samples.append(value)

        elif message_type == "END":

            break

        elif message_type == "RATE":

            current_sampling_rate = value

            print(
                "Pico sampling rate:",
                current_sampling_rate,
                "Hz"
            )

    return samples

def adc_to_voltage(samples):
    return [sample * 3.3 / 4095 for sample in samples]

set_sampling_rate(5000)

"""
# Prints one graph (plt.show() disables the loop until it is closed)
while True:
    print("Waiting for buffer")

    samples = read_buffer()

    print("Received", len(samples), "samples")

    voltages = adc_to_voltage(samples)

    # Plot waveform

    plt.figure(figsize=(10, 4))
    plt.plot(voltages)

    plt.xlabel("Sample")
    plt.ylabel("Voltage (V)")
    plt.title("ADC Waveform")

    plt.grid(True)

    plt.show()
"""

# Continuous plotting

plt.ion() # Enables interactive mode

fig, ax = plt.subplots(figsize=(10, 4))

value_display = fig.text(
    0.85,
    0.5,
    "",
    fontsize=12
)

while True:
    samples = read_buffer()

    voltages = adc_to_voltage(samples)

    latest_voltage = voltages[-1]

    ax.clear()

    ax.plot(voltages)

    ax.set_xlabel("Sample")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("ADC Waveform")



    value_display.set_text(
        f"Voltage: {latest_voltage:.2f} V\n"
        f"Sampling Rate: {current_sampling_rate} Hz"
    )

    ax.set_ylim(0, 3.31)

    ax.grid(True)

    plt.pause(0.01)