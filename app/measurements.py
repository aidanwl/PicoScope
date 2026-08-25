"""
Measurement Calculations and Display
"""

import tkinter as tk
from tkinter import ttk
import math

ADC_MAX = 4095
ADC_VOLTAGE = 3.3

def adc_to_voltage(samples):
    return [sample * ADC_VOLTAGE / ADC_MAX for sample in samples]

def calculate_rms(voltages):
    if not voltages:
        return None

    return math.sqrt(sum(voltage ** 2 for voltage in voltages) / len(voltages))

def calculate_vpp(voltages):
    if not voltages:
        return None

    return max(voltages) - min(voltages)

def calculate_vmax(voltages):
    if not voltages:
        return None

    return max(voltages)

def calculate_vmin(voltages):
    if not voltages:
        return None

    return min(voltages)

def calculate_mean(voltages):
    if not voltages:
        return None

    return sum(voltages) / len(voltages)

def calculate_amplitude(voltages):
    vpp = calculate_vpp(voltages)

    if vpp is None:
        return None

    return vpp / 2

def calculate_frequency(samples, sampling_rate):
    if not samples or not sampling_rate:
        return None

    voltages = adc_to_voltage(samples)

    mean = sum(voltages) / len(voltages)

    crossings = []

    for i in range(1, len(voltages)):
        if voltages[i - 1] < mean <= voltages[i]:
            crossings.append(i)

    if len(crossings) < 2:
        return None

    periods = [crossings[i] - crossings[i - 1] for i in range(1, len(crossings))]

    average_period = sum(periods) / len(periods)

    if average_period == 0:
        return None

    return sampling_rate / average_period

def calculate_period(samples, sampling_rate):
    frequency = calculate_frequency(samples, sampling_rate)

    if frequency is None or frequency == 0:
        return None

    return 1 / frequency

class MeasurementWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("PicoScope Measurements")
        self.window.geometry("350x400")

        title = ttk.Label(
            self.window,
            text="Measurements",
            font=("TkDefaultFont", 16, "bold")
        )

        title.pack(pady=(15, 15))

        self.frequency_label = ttk.Label(
            self.window,
            text="Frequency: -- Hz"
        )

        self.frequency_label.pack(pady=5)

        self.period_label = ttk.Label(
            self.window,
            text="Period: -- ms"
        )

        self.period_label.pack(pady=5)

        self.rms_label = ttk.Label(
            self.window,
            text="RMS: -- V"
        )

        self.rms_label.pack(pady=5)

        self.vpp_label = ttk.Label(
            self.window,
            text="Vpp: -- V"
        )

        self.vpp_label.pack(pady=5)

        self.vmax_label = ttk.Label(
            self.window,
            text="Vmax: -- V"
        )

        self.vmax_label.pack(pady=5)

        self.vmin_label = ttk.Label(
            self.window,
            text="Vmin: -- V"
        )

        self.vmin_label.pack(pady=5)

        self.mean_label = ttk.Label(
            self.window,
            text="Mean: -- V"
        )

        self.mean_label.pack(pady=5)

        self.amplitude_label = ttk.Label(
            self.window,
            text="Amplitude: -- V"
        )

        self.amplitude_label.pack(pady=5)

    def update(self, samples, sampling_rate):
        if not samples or not sampling_rate:
            return

        # Convert once
        voltages = adc_to_voltage(samples)

        # Calculate measurements
        frequency = calculate_frequency(
            samples,
            sampling_rate
        )

        period = None

        if frequency is not None and frequency != 0:
            period = 1 / frequency

        rms = calculate_rms(voltages)
        vpp = calculate_vpp(voltages)
        vmax = calculate_vmax(voltages)
        vmin = calculate_vmin(voltages)
        mean = calculate_mean(voltages)
        amplitude = calculate_amplitude(voltages)

        # Frequency
        if frequency is not None:
            self.frequency_label.config(
                text=f"Frequency: {frequency:.2f} Hz"
            )

        else:
            self.frequency_label.config(
                text="Frequency: -- Hz"
            )

        # Period
        if period is not None:
            self.period_label.config(
                text=f"Period: {period * 1000:.3f} ms"
            )

        else:
            self.period_label.config(
                text="Period: -- ms"
            )

        # RMS
        if rms is not None:
            self.rms_label.config(
                text=f"RMS: {rms:.3f} V"
            )

        # Vpp
        if vpp is not None:
            self.vpp_label.config(
                text=f"Vpp: {vpp:.3f} V"
            )

        # Vmax
        if vmax is not None:
            self.vmax_label.config(
                text=f"Vmax: {vmax:.3f} V"
            )

        # Vmin
        if vmin is not None:
            self.vmin_label.config(
                text=f"Vmin: {vmin:.3f} V"
            )

        # Mean
        if mean is not None:
            self.mean_label.config(
                text=f"Mean: {mean:.3f} V"
            )

        # Amplitude
        if amplitude is not None:
            self.amplitude_label.config(
                text=f"Amplitude: {amplitude:.3f} V"
            )