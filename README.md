# PicoScope

PicoScope is a custom oscilloscope built using the Raspberry Pi Pico 2. The Pico
samples an analog signal into a circular buffer with the onboard ADC and sends the raw readings over USB serial to a Python application, which converts them to voltage and plots the waveform in real time.

## Features

- ADC waveform acquisition on ADC0 / GPIO 26 (Pico pin 31)
- Fixed-size 1,000-sample circular capture buffer for continuous waveform acquisition
- USB serial interface between the Pico firmware and Python application
- Python GUI for live waveform visualization, voltage monitoring, and acquisition-rate feedback
- Automatic restoration of the default acquisition configuration when the Python application closes
- ADC validation and acquisition experiments under `tests/`

## Project Structure

| Directory | Purpose |
| --- | --- |
| `firmware/` | Pico firmware, CMake configuration, and UF2 build output |
| `app/` | Python GUI, serial protocol handling, and waveform plotting |
| `lib/circular_buffer/` | Reusable circular-buffer implementation used by the firmware |
| `tests/` | ADC, acquisition, buffering, and live-plot experiments |

## Current Progress

### Working

- The Pico initializes ADC0 and samples an analog input.
- Captures are sent as `START`, 1,000 raw ADC values, and `END` lines.
- The Python application reads the serial stream and plots the converted voltage.
- The sampling rate can be changed from the GUI and acknowledged by the Pico.

### In Progress / Known Limitations

- Sampling is controlled by software polling and `sleep_us()`, so the achieved
	rate is lower than the requested rate, especially at higher frequencies.
- There is no trigger system, selectable input channel, or configurable capture
	length yet.
- Serial settings are currently fixed to `/dev/ttyACM0` and 115200 baud in
	`app/serial_interface.py`.
- The firmware currently streams complete blocks rather than providing a
	continuous, independently timed display update.

## Requirements (For Windows WSL Ubuntu)

- Raspberry Pi Pico and an analog signal within the Pico ADC input range
- WSL Ubuntu with the Pico SDK installed at `/home/$USER/pico/pico-sdk/` (Can change SDK location as long as PATH is corrected in CMakeLists.txt)
- CMake and Ninja (or default generator)
- Python 3.10 or newer
- Python virtual-environment support
- Tk support for the GUI

Install the Ubuntu GUI and virtual-environment packages if needed:

```bash
sudo apt update
sudo apt install python3-venv python3-tk cmake ninja-build
```

## Build and Flash the Firmware

From the repository root in WSL Ubuntu:

```bash
cd firmware
cmake -G Ninja -DPICO_BOARD=pico2 ..
cmake --build build
```

The build creates `firmware/build/PicoScope.uf2`. Put the Pico into bootloader
mode, then copy that UF2 file to the mounted `RPI-RP2` drive. After flashing,
reconnect the Pico so it appears as `/dev/ttyACM0`.

## Run the Python Application

From the repository root in WSL Ubuntu:

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

The app opens the control window and a Matplotlib waveform window. Connect the
analog signal to GPIO 26 / ADC0 and a Pico ground pin. Keep the input between 0
and 3.3 V. Close the GUI to stop the application (resets the Pico to the
default 5 kHz application rate before disconnecting).

## Serial Protocol

The Python app sends sampling-rate changes as:

```text
RATE 10000
```

The Pico acknowledges a valid rate with `RATE <hz>` and sends captures in this
format:

```text
START
<raw ADC sample>
...
END
```

Raw 12-bit ADC values are converted by the application using a 3.3 V reference.

## Tests

The test directories contain standalone experiments rather than an automated
test suite. See `tests/adc_tests/README.md` and
`tests/live_plot_test/README.md` for their individual setup and results.