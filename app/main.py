"""
Main application for PicoScope GUI
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

from serial_interface import PicoSerial
from plot import WaveformPlot


DEFAULT_SAMPLING_RATE = 5000

pico = PicoSerial()

# GUI
root = tk.Tk()
root.title("PicoScope")
root.geometry("400x250")

plot = WaveformPlot()


# Sampling Rate
sampling_rate_label = ttk.Label(
    root,
    text="Sampling Rate (Hz):"
)
sampling_rate_label.pack(pady=(20, 5))

sampling_rate_entry = ttk.Entry(
    root,
    width=15
)

sampling_rate_entry.insert(
    0,
    str(DEFAULT_SAMPLING_RATE)
)

sampling_rate_entry.pack()


# Current Rate Display
current_rate_label = ttk.Label(
    root,
    text="Current Rate: -- Hz"
)

current_rate_label.pack(pady=10)


# Sampling Rate Apply Button
def apply_sampling_rate():
    try:
        rate = int(sampling_rate_entry.get())

        if rate <= 0:
            return

        pico.set_sampling_rate(rate)

    except ValueError:
        print("Invalid sampling rate. Please enter a positive integer")


apply_button = ttk.Button(
    root,
    text="Apply",
    command=apply_sampling_rate
)

apply_button.pack(pady=5)


# Update
update_id = None


def update():
    global update_id

    samples, sampling_rate = pico.read_buffer()

    if sampling_rate is not None:
        current_rate_label.config(
            text=f"Current Rate: {sampling_rate} Hz"
        )

    if samples:
        plot.update(samples, sampling_rate)

    update_id = root.after(10, update)


# Finish closing after Pico has received reset rate
def finish_close():
    if pico.ser.is_open:
        pico.ser.close()

    plt.close("all")
    root.destroy()


# Clean shutdown
def on_close():
    global update_id

    if update_id is not None:
        root.after_cancel(update_id)
        update_id = None

    # Reset Pico to default rate before closing
    if pico.ser.is_open:
        pico.set_sampling_rate(DEFAULT_SAMPLING_RATE)
        root.after(100, finish_close)

    else:
        finish_close()


root.protocol(
    "WM_DELETE_WINDOW",
    on_close
)


update_id = root.after(0, update)

root.mainloop()