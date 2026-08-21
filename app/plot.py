import matplotlib.pyplot as plt


def adc_to_voltage(samples):
    return [
        sample * 3.3 / 4095
        for sample in samples
    ]


class WaveformPlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots(
            figsize=(10, 4)
        )

        self.value_display = self.fig.text(
            0.75,
            0.5,
            "",
            fontsize=12
        )

        # Open the Matplotlib window
        plt.show(block=False)

    def update(self, samples, sampling_rate):
        if not samples:
            return

        voltages = adc_to_voltage(samples)
        latest_voltage = voltages[-1]

        self.ax.clear()

        self.ax.plot(voltages)

        self.ax.set_xlabel("Sample")
        self.ax.set_ylabel("Voltage (V)")
        self.ax.set_title("ADC Waveform")
        self.ax.set_ylim(0, 3.31)
        self.ax.grid(True)

        self.value_display.set_text(
            f"Voltage: {latest_voltage:.2f} V\n"
            f"Sampling Rate: {sampling_rate} Hz"
        )

        self.fig.canvas.draw_idle()