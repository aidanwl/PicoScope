/*
Signal Acquisition: Reading data from the GPIO pin and using a circular buffer to output chunks of data to serial output to be plotted by live_plot.py
*/

#include <iostream>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/gpio.h"
#include "circular_buffer.h"

using namespace std;

const uint32_t SAMPLING_RATE = 10000; // 10 kHz

int main() {
    stdio_init_all();

    adc_init();

    adc_gpio_init(26);
    adc_select_input(0);

    CircularBuffer buffer;
    init_buffer(&buffer);

    uint16_t output[BUFFER_SIZE];

    
    uint32_t sample_period_us = 1000000 / SAMPLING_RATE;

    uint32_t copied_samples = 0;

    while (1) {
        uint16_t sample = adc_read();

        write_buffer(&buffer, sample);
        copied_samples++;

        if (buffer.full && copied_samples >= BUFFER_SIZE) {
            copy_buffer(&buffer, output);
            
            cout << "START" << endl;
            for (uint32_t i = 0; i < BUFFER_SIZE; i++) {
                cout << output[i] << endl;
            }

            cout << "END" << endl;

            copied_samples = 0;
        }

        sleep_us(sample_period_us);
    }
}