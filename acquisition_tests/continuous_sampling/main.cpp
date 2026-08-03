/*
Continuous Sampling Test: Creating a circular buffer struct, constantly filling and overriding its values while copying the array at intervals to read it to file and terminal output
*/

#include <iostream>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/gpio.h"

using namespace std;

const int BUFFER_SIZE = 1000;

struct CircularBuffer {
    uint16_t data[BUFFER_SIZE];
    uint32_t write_index;
    bool full;
};

void init_buffer(CircularBuffer* buffer) {
    buffer->write_index = 0;
    buffer->full = false;
}

void write_buffer(CircularBuffer* buffer, uint16_t sample) {
    buffer->data[buffer->write_index] = sample;
    buffer->write_index++;

    if (buffer->write_index == BUFFER_SIZE) {
        buffer->write_index = 0;
        buffer->full = true;
    }
}

void copy_buffer(CircularBuffer* buffer, uint16_t* output) {
    uint32_t index = buffer->full ?  buffer->write_index : 0;
    uint32_t length = buffer->full ? BUFFER_SIZE : buffer->write_index;

    for (uint32_t i = 0; i < length; i++) {
        output[i] = buffer->data[index];
        index++;

        if (index == BUFFER_SIZE) {
            index = 0;
        }
    }


}

uint16_t read_buffer(CircularBuffer* buffer, uint32_t position) {
    if (!buffer->full && position >= buffer->write_index) {
        return 0;
    }

    uint32_t index = buffer->full ? (buffer->write_index + position) % BUFFER_SIZE : position;

    return buffer->data[index];
}

int main() {
    stdio_init_all();

    adc_init();

    adc_gpio_init(26);
    adc_select_input(0);

    CircularBuffer buffer;
    init_buffer(&buffer);

    uint16_t output[BUFFER_SIZE];

    double sampling_rate = 10000; // 10 kHz
    uint32_t sample_period_us = 1000000 / sampling_rate;

    uint32_t copied_samples = 0;

    while (1) {
        uint16_t sample = adc_read();

        write_buffer(&buffer, sample);
        copied_samples++;

        if (buffer.full && copied_samples >= BUFFER_SIZE) {
            copy_buffer(&buffer, output);
            
            cout << "----- NEW BUFFER -----" << endl;
            for (uint32_t i = 0; i < BUFFER_SIZE; i++) {
                cout << output[i] << endl;
            }

            copied_samples = 0;
        }

        sleep_us(sample_period_us);
    }
}