/*
Title: Description
*/

#include <iostream>
#include <cstring>
#include <cstdlib>
#include "pico/stdlib.h"
#include "hardware/adc.h"
#include "hardware/gpio.h"
#include "circular_buffer.h"

using namespace std;

void process_command(char* command);

uint32_t sampling_rate = 10000; // 10 kHz

// Command Buffer
char command[64];
uint32_t command_index = 0;

uint16_t output[BUFFER_SIZE];
    
// Sampling
uint32_t sample_period_us = 1000000 / sampling_rate;

uint32_t copied_samples = 0;

int command_processing = 0;

int main() {
    stdio_init_all();

    // Circular Buffer init
    CircularBuffer buffer;
    init_buffer(&buffer);

    // Onboard LED init
    const uint LED_PIN = PICO_DEFAULT_LED_PIN;

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    gpio_put(LED_PIN, 0);

    // ADC init
    adc_init();

    adc_gpio_init(26);
    adc_select_input(0);

    while (1) {

        // Checking for CONFIG changes (currently just testing serial communication between Python and cpp)

        int character = getchar_timeout_us(0);

        if (character != PICO_ERROR_TIMEOUT) {

            command_processing = 1;
            
            if (character == '\n') {
                command[command_index] = '\0';

                process_command(command);

                command_index = 0;
                command_processing = 0;
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

        if (buffer.full && copied_samples >= BUFFER_SIZE && !command_processing) {
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

// CONFIG Processing
void process_command(char* command) {
    if (strncmp(command, "RATE ", 5) == 0) {
        uint32_t new_rate = atoi(command + 5);

        if (new_rate > 0) {
            sampling_rate = new_rate;
            sample_period_us = 1000000 / sampling_rate;

            copied_samples = 0;
            
            // Debugging output to Python
            printf("RATE %lu\n", sampling_rate);
        }
    }
}   