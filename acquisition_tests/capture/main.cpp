/*
ADC Capture/Buffer Test: Creating a sample buffer, filling it with ADC readings at a fixed sampling rate, and printing the collected waveform data
*/

#include <iostream>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"

using namespace std;

void capture_samples(uint16_t* buffer, uint64_t samples, double sampling_rate) {
    uint64_t sample_period_us = 1000000.0 / sampling_rate;

    for (uint64_t i = 0; i < samples; i++) {
        buffer[i] = adc_read();
        sleep_us(sample_period_us);
    }

}

int main() {
    stdio_init_all();

    cout << "ADC Capture Test" << endl;

    adc_init();

    adc_gpio_init(26);
    adc_select_input(0);

    uint64_t samples = 10000;
    double sampling_rate = 10000; // 10 kHz

    uint16_t buffer[samples];

    capture_samples(buffer, samples, sampling_rate);

    while (1) {
        for (uint64_t i = 0; i < samples; i++) {
            cout << "Sample " << i << ": " << buffer[i] * 3.3f / 4095.0f << "V" << endl;
        }
        sleep_ms(1000);
    }
}