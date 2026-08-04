# Live Plot

This program uses C++ and Python to display a constantly updating waveform output of the current ADC voltage. It uses the Pico SDK to read the ADC value at GPIO 0 (Pin 26), outputs the raw ADC value to serial, and then Python to grab the serial output and plot it using matplotlib.

## Requirements

This program uses the Pico SDK and a few Python libraries. The Pico SDK is the default, and its installation will be omitted.

### Python Dependencies

1. Python Version 3.10.12
2. Python virtual environment (venv): `sudo apt install python3-venv`
3. Python tk (Ttkinter): `sudo apt install python3-tk` (GUI platform for WSL Ubuntu)
4. Python venv requirements: `pip install requirements.txt` (Run this command within the venv)
