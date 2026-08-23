/*
PicoScope Firmware for Sampling and communication with Python GUI
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

// Signal Generation
const uint SIGNAL_PIN = 15;
const uint32_t SIGNAL_PERIOD_US = 100000;
absolute_time_t signal_toggle_time;
bool signal_state = false;

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

    gpio_init(SIGNAL_PIN);
    gpio_set_dir(SIGNAL_PIN, GPIO_OUT);
    gpio_put(SIGNAL_PIN, 0);
    
    signal_toggle_time = make_timeout_time_us(SIGNAL_PERIOD_US / 2);

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

        absolute_time_t start_time = get_absolute_time();

        while (copied_samples < BUFFER_SIZE) {
            uint16_t sample = adc_read();
            write_buffer(&buffer, sample);
            copied_samples++;
            sleep_us(sample_period_us);

            if (absolute_time_diff_us(get_absolute_time(), signal_toggle_time) <= 0) {
                signal_state = !signal_state;
                gpio_put(SIGNAL_PIN, signal_state);
                signal_toggle_time = make_timeout_time_us(SIGNAL_PERIOD_US / 2);
            }
        }

        absolute_time_t end_time = get_absolute_time();

        uint64_t elapsed_us = absolute_time_diff_us(start_time, end_time);

        uint32_t actual_rate = (uint32_t)((BUFFER_SIZE * 1000000ULL) / elapsed_us);

        if (buffer.full && copied_samples >= BUFFER_SIZE && !command_processing) {
            copy_buffer(&buffer, output);

            printf("ACTUAL_RATE %lu\n", actual_rate);
            
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