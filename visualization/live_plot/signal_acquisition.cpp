/*
Signal Acquisition: Reading data from the GPIO pin and using a circular buffer to output chunks of data to serial output to be plotted by live_plot.py
*/

#include <iostream>
#include <cstring>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/gpio.h"
#include "circular_buffer.h"

using namespace std;

const uint32_t SAMPLING_RATE = 10000; // 10 kHz

// Command Buffer
char command[64];
uint32_t command_index = 0;



int main() {
    stdio_init_all();

    // Onboard LED init
    const uint LED_PIN = PICO_DEFAULT_LED_PIN;

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_put(LED_PIN, 0);

    // ADC init
    adc_init();

    adc_gpio_init(26);
    adc_select_input(0);

    // Circular Buffer init
    CircularBuffer buffer;
    init_buffer(&buffer);

    uint16_t output[BUFFER_SIZE];
    
    // Sampling
    uint32_t sample_period_us = 1000000 / SAMPLING_RATE;

    uint32_t copied_samples = 0;

    while (1) {

        // Checking for CONFIG changes (currently just testing serial communication between Python and cpp)

        int character = getchar_timeout_us(0);

        if (character != PICO_ERROR_TIMEOUT) {
            if (character == '\n') {
                command[command_index] = '\0';

                if (!strcmp(command, "CONFIG")) {
                    gpio_put(LED_PIN, 1);
                }

                command_index = 0;
            }

            else if (command_index < sizeof(command) - 1) {
                command[command_index++] = character;
            }
        }

        while (copied_samples < BUFFER_SIZE) {
            uint16_t sample = adc_read();
            write_buffer(&buffer, sample);
            copied_samples++;
            sleep_us(sample_period_us);
        }

        if (buffer.full && copied_samples >= BUFFER_SIZE && command_index == 0) {
            copy_buffer(&buffer, output);
            
            printf("START\n");
            for (uint32_t i = 0; i < BUFFER_SIZE; i++) {
                printf("%d\n", output[i]);
            }

            printf("END\n");

            copied_samples = 0;
        }

        
    }
}