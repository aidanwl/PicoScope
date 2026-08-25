"""
Waveform plotting
"""

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import csv
from datetime import datetime

ADC_MAX = 4095
ADC_VOLTAGE = 3.3
HISTORY_SIZE = 10000

def adc_to_voltage(samples):
    return [sample * ADC_VOLTAGE / ADC_MAX for sample in samples]

class WaveformPlot:
    def __init__(self):

        # Figure and axis
        self.fig, self.ax = plt.subplots(
            figsize=(10, 4)
        )

        self.fig.canvas.manager.set_window_title(
            "PicoScope Waveform"
        )

        # Waveform history
        self.history = []
        self.history_size = HISTORY_SIZE

        # Current sampling rate
        self.sampling_rate = None

        # Number of samples visible horizontally
        self.view_width = 1000

        self.auto_follow = True

        # Default vertical range
        self.default_y_min = 0
        self.default_y_max = 3.31

        # Amount to move vertically when panning
        self.vertical_pan_step = 0.25

        # Display for latest voltage and sampling rate
        self.value_display = self.fig.text(
            0.75,
            0.5,
            "",
            fontsize=12
        )

        # Initial graph setup
        self.ax.set_xlabel("Sample")
        self.ax.set_ylabel("Voltage (V)")
        self.ax.set_title("ADC Waveform")
        self.ax.set_xlim(
            0,
            self.view_width
        )
        self.ax.set_ylim(
            self.default_y_min,
            self.default_y_max
        )
        self.ax.grid(True)

        # Open Matplotlib window
        plt.show(block=False)

    def update(self, samples, sampling_rate):
        if not samples:
            return

        if sampling_rate:
            self.sampling_rate = sampling_rate

        # Convert new ADC samples to voltage
        new_voltages = adc_to_voltage(samples)

        # Add new samples to history
        self.history.extend(new_voltages)

        # Prevent history from growing forever
        if len(self.history) > self.history_size:
            excess = (len(self.history) - self.history_size)
            self.history = self.history[excess:]

        # Latest voltage
        latest_voltage = self.history[-1]

        # Update display
        if self.sampling_rate:
            self.value_display.set_text(
                f"Voltage: {latest_voltage:.2f} V\n"
                f"Sampling Rate: {self.sampling_rate} Hz"
            )
        else:
            self.value_display.set_text(
                f"Voltage: {latest_voltage:.2f} V"
            )

        # Save current viewport
        current_x_limits = self.ax.get_xlim()
        current_y_limits = self.ax.get_ylim()

        # Redraw waveform
        self.ax.clear()

        x = np.arange(len(self.history))

        self.ax.plot(
            x,
            self.history
        )

        self.ax.set_xlabel("Sample")
        self.ax.set_ylabel("Voltage (V)")
        self.ax.set_title("ADC Waveform")
        self.ax.grid(True)

        # Automatically follow newest samples
        if self.auto_follow:
            if len(self.history) <= self.view_width:
                left = 0
                right = self.view_width

            else:
                right = len(self.history)
                left = (right - self.view_width)

            self.ax.set_xlim(left, right)
            self.ax.set_ylim(self.default_y_min, self.default_y_max)

        else:
            # Preserve limits
            self.ax.set_xlim(current_x_limits)
            self.ax.set_ylim(current_y_limits)

        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def zoom_in(self):

        # Get current horizontal view
        left, right = self.ax.get_xlim()
        center = (left + right) / 2
        width = right - left

        new_width = width * 0.5

        if new_width < 10:
            new_width = 10

        self.view_width = int(new_width)

        # When manually viewing stop following
        self.auto_follow = False

        self.ax.set_xlim(center - new_width / 2, center + new_width / 2)

        self.fig.canvas.draw_idle()

    def zoom_out(self):

        # Get current horizontal view
        left, right = self.ax.get_xlim()
        center = (left + right) / 2
        width = right - left

        # Double visible width
        new_width = width * 2

        if new_width > self.history_size:
            new_width = self.history_size

        self.view_width = int(new_width)

        self.auto_follow = False

        self.ax.set_xlim(center - new_width / 2, center + new_width / 2)

        self.fig.canvas.draw_idle()

    def pan_left(self):

        # Move horizontal view toward older samples
        left, right = self.ax.get_xlim()
        width = right - left
        shift = width * 0.25

        new_left = left - shift
        new_right = right - shift

        if new_left < 0:
            new_left = 0
            new_right = width

        self.auto_follow = False

        self.ax.set_xlim(new_left, new_right)

        self.fig.canvas.draw_idle()

    def pan_right(self):

        # Move horizontal view toward newer samples
        left, right = self.ax.get_xlim()
        width = right - left
        shift = width * 0.25

        new_left = left + shift
        new_right = right + shift

        newest = len(self.history)

        if new_right >= newest:
            new_right = newest
            new_left = max(0, newest - width)

            self.auto_follow = True

        else:
            self.auto_follow = False

        self.ax.set_xlim(new_left, new_right)

        self.fig.canvas.draw_idle()

    def pan_up(self):

        # Move vertical view upward
        bottom, top = self.ax.get_ylim()
        height = top - bottom
        shift = max(self.vertical_pan_step, height * 0.25)

        new_bottom = bottom + shift
        new_top = top + shift

        self.ax.set_ylim(new_bottom, new_top)

        self.auto_follow = False

        self.fig.canvas.draw_idle()

    def pan_down(self):

        # Move vertical view downward
        bottom, top = self.ax.get_ylim()
        height = top - bottom
        shift = max(self.vertical_pan_step, height * 0.25)

        new_bottom = bottom - shift
        new_top = top - shift

        self.ax.set_ylim(
            new_bottom,
            new_top
        )

        self.auto_follow = False

        self.fig.canvas.draw_idle()

    def reset_view(self):

        # Return to newest waveform data
        self.auto_follow = True

        self.ax.set_ylim(self.default_y_min, self.default_y_max)

        # Reset horizontal range
        if len(self.history) <= self.view_width:
            left = 0
            right = self.view_width

        else:
            right = len(self.history)
            left = (right - self.view_width)

        self.ax.set_xlim(left, right)

        self.fig.canvas.draw_idle()

    def save_waveform(self):

        # Do not save if there is no waveform data
        if not self.history:
            print("No waveform data to save.")
            return

        # Generate default filename
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        default_filename = (
            f"waveform_{timestamp}"
        )

        # Ask user where to save the waveform
        filename = filedialog.asksaveasfilename(
            title="Save Waveform",
            initialfile=default_filename,
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("All Files", "*.*")
            ]
        )

        if not filename:
            return

        # Filename cleaning
        if filename.lower().endswith(".png"):
            base_filename = filename[:-4]
        else:
            base_filename = filename

        image_filename = (
            base_filename + ".png"
        )

        csv_filename = (
            base_filename + ".csv"
        )

        # Save the graph exactly as currently displayed
        self.fig.savefig(
            image_filename,
            dpi=300,
            bbox_inches="tight"
        )

        # Get the current viewport
        x_limits = self.ax.get_xlim()
        y_limits = self.ax.get_ylim()

        # Save waveform data
        with open(
            csv_filename,
            "w",
            newline=""
        ) as file:
            writer = csv.writer(file)

            # Metadata
            writer.writerow([
                "# PicoScope Waveform"
            ])

            writer.writerow([
                "# Sampling Rate (Hz)",
                self.sampling_rate
            ])

            writer.writerow([
                "# X Axis Min",
                x_limits[0]
            ])

            writer.writerow([
                "# X Axis Max",
                x_limits[1]
            ])

            writer.writerow([
                "# Y Axis Min",
                y_limits[0]
            ])

            writer.writerow([
                "# Y Axis Max",
                y_limits[1]
            ])

            writer.writerow([])

            # Waveform data
            writer.writerow([
                "Sample",
                "Voltage (V)"
            ])

            for index, voltage in enumerate(
                self.history
            ):

                writer.writerow([
                    index,
                    voltage
                ])

        print(
            f"Waveform saved:\n"
            f"  Image: {image_filename}\n"
            f"  Data:  {csv_filename}"
        )