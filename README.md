# PicoScope

PicoScope is a custom oscilloscope built using the Raspberry Pi Pico 2. The Pico
samples an analog signal into a circular buffer with the onboard ADC and sends the raw readings over USB serial to a Python application. The Python application converts the raw ADC readings to voltage and provides waveform visualization, triggering, measurements, frequency-domain analysis, waveform freezing, and waveform saving.

---

## Features

### Signal Acquisition

- ADC waveform acquisition on ADC0 / GPIO 26 (Pico pin 31)
- 12-bit ADC resolution
- 0–3.3 V input range
- Fixed-size 1,000-sample circular capture buffer
- Configurable sampling rate from the Python GUI
- Continuous acquisition on the Pico
- USB serial communication between the Pico and Python application
- Raw ADC samples converted to voltage in Python
- Requested sampling-rate reporting
- Measured actual sampling-rate reporting
- Sampling-rate accuracy calculation

### Waveform Visualization

- Live waveform display using Matplotlib
- Voltage displayed on the vertical axis
- Sample number displayed on the horizontal axis
- Automatic following of the newest samples
- Persistent waveform history
- Zoom in
- Zoom out
- Pan left
- Pan right
- Pan up
- Pan down
- Reset view

### Triggering

- Rising-edge waveform triggering
- Trigger enable/disable control
- Configurable trigger position from 0–100%
- Pre-trigger samples
- Post-trigger samples
- Automatic capture fallback when a trigger is not detected
- Trigger configuration controlled from the Python GUI

---

## Measurements

| Measurement | Description |
| --- | --- |
| Frequency | Estimated signal frequency from rising mean-level crossings |
| Period | Inverse of the measured frequency |
| RMS | Root-mean-square voltage of the captured samples |
| Vpp | Difference between maximum and minimum voltage |
| Vmax | Maximum measured voltage |
| Vmin | Minimum measured voltage |
| Mean | Average voltage of the captured waveform |
| Amplitude | Half of the measured peak-to-peak voltage |

### Frequency-Domain Analysis

- FFT-based frequency-domain analysis
- Magnitude spectrum visualization
- DC removal before FFT analysis
- Frequency axis calculated from the acquisition rate
- Identification of dominant frequency components

### Waveform Controls

- Freeze the displayed waveform
- Resume live waveform updates
- Inspect a frozen waveform without it changing
- Zoom and pan while inspecting the waveform

### Saving

- Save the waveform at the time the save operation is performed
- Preserve the current zoom and pan state when saving the graph
- Save waveform data for later analysis
- Preserve the displayed waveform and underlying numerical data

### Application Behavior

- Separate waveform visualization window
- Separate measurement display
- Separate FFT analysis window
- Automatic restoration of the default acquisition configuration when the
  Python application closes
- Clean serial connection shutdown
- Matplotlib windows closed during application shutdown

---

### Serial Configuration

The current Python serial configuration is fixed to:

```text
/dev/ttyACM0
115200 baud
```

These values are currently defined in:

```text
app/serial_interface.py
```

A future version could allow the serial port and baud rate to be configured.

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

## Project Structure

| Directory | Purpose |
| --- | --- |
| `firmware/` | Pico firmware, CMake configuration, and UF2 build output |
| `app/` | Python GUI, serial protocol handling, waveform plotting, measurements, and FFT analysis |
| `lib/circular_buffer/` | Reusable circular-buffer implementation used by the firmware |
| `tests/` | ADC, acquisition, buffering, and live-plot experiments |

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

## Tests

The test directories contain standalone experiments rather than an automated
test suite. See `tests/adc_tests/README.md` and
`tests/live_plot_test/README.md` for their individual setup and results.

## Next Steps

- Improve acquisition timing by replacing software-based sampling delays with Pico hardware timers and/or ADC FIFO/DMA.
- Improve trigger responsiveness and reduce acquisition latency.
- Improve frequency estimation for noisy and non-sinusoidal signals.
- Implement a custom radix-2 FFT to better understand and demonstrate the underlying DSP algorithm.
- Move selected signal-processing operations onto the Pico where practical.
- Improve serial communication robustness and error handling.
- Add additional waveform and signal-analysis controls as the project develops.
- Expand automated testing for ADC acquisition, triggering, measurements, FFT analysis, and serial communication.