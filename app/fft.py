"""
FFT Analysis and Display
"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt


ADC_MAX = 4095
ADC_VOLTAGE = 3.3


class FFTWindow:

    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 4))

        self.fig.canvas.manager.set_window_title("PicoScope FFT")

        self.peak_display = self.fig.text(
            0.75,
            0.85,
            "",
            fontsize=12
        )

        plt.show(block=False)

    def update(self, samples, sampling_rate):

        if not samples or not sampling_rate:
            return

        # Convert ADC samples to voltages
        voltages = (np.array(samples, dtype=float) * ADC_VOLTAGE / ADC_MAX)

        # Remove DC component (Center to 0 instead of offset)
        voltages = (voltages - np.mean(voltages))

        # Hann Window
        window = np.hanning(len(voltages))
        windowed = (voltages* window)

        # FFT (Implement custom FFT later)
        fft_result = np.fft.rfft(windowed)

        # Frequency Axis (frequency bins)
        frequencies = np.fft.rfftfreq(len(voltages), d=1 / sampling_rate)

        magnitude = np.abs(fft_result)

        # Ignore DC
        if len(magnitude) > 0:
            magnitude[0] = 0

        # Peak (Dominant Frequency)
        peak_index = np.argmax(magnitude)

        dominant_frequency = (frequencies[peak_index])

        # Plot
        self.ax.clear()

        self.ax.plot(
            frequencies,
            magnitude
        )

        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude")
        self.ax.set_title("FFT Spectrum")

        self.ax.grid(True)

        self.peak_display.set_text(f"Peak: {dominant_frequency:.2f} Hz")

        self.fig.canvas.draw_idle()