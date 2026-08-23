"""
Main application for PicoScope GUI
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from serial_interface import PicoSerial
from plot import WaveformPlot


DEFAULT_SAMPLING_RATE = 10000

pico = PicoSerial()

# GUI
root = tk.Tk()
root.title("PicoScope")
root.geometry("400x350")

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


# Requested Rate Display
requested_rate_label = ttk.Label(
    root,
    text="Requested Rate: -- Hz"
)
requested_rate_label.pack(pady=(10, 2))


# Actual Rate Display
actual_rate_label = ttk.Label(
    root,
    text="Actual Rate: -- Hz"
)
actual_rate_label.pack(pady=2)


# Accuracy Display
accuracy_label = ttk.Label(
    root,
    text="Accuracy: --"
)
accuracy_label.pack(pady=(2, 10))


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

# Triggering
trigger_enabled = tk.BooleanVar(value=True)
trigger_position = tk.IntVar(value=50)

def toggle_trigger():
    pico.set_trigger_enabled(trigger_enabled.get())

trigger_button = ttk.Checkbutton(
    root,
    text="Trigger",
    variable=trigger_enabled,
    command=toggle_trigger
)

trigger_button.pack(pady=(10, 2))

trigger_position_label = ttk.Label(
    root,
    text="Trigger Position: 50%"
)


trigger_position_label.pack()

def update_trigger_position(value):
    position = int(float(value))
    trigger_position_label.config(text=f"Trigger Position: {position}%")

trigger_slider = ttk.Scale(
    root,
    from_=0,
    to=100,
    orient="horizontal",
    variable=trigger_position,
    command=update_trigger_position
)

trigger_slider.pack(
    fill="x",
    padx=30,
    pady=(2,10)
)

def apply_trigger_position():
    pico.set_trigger_position(trigger_position.get())

trigger_apply_button = ttk.Button(
    root,
    text="Apply Trigger Position",
    command=apply_trigger_position
)

trigger_apply_button.pack(pady=5)

# Update
update_id = None


def update():
    global update_id

    samples, requested_rate, actual_rate = pico.read_buffer()

    if requested_rate is not None:
        requested_rate_label.config(
            text=f"Requested Rate: {requested_rate} Hz"
        )

    if actual_rate is not None:
        actual_rate_label.config(
            text=f"Actual Rate: {actual_rate} Hz"
        )

    if requested_rate is not None and actual_rate is not None:
        accuracy = actual_rate / requested_rate * 100

        accuracy_label.config(
            text=f"Accuracy: {accuracy:.2f}%"
        )

    if samples:
        plot.update(samples, actual_rate)

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