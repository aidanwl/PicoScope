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

// Triggering
uint16_t trigger_level = 2048; // Trigger level for rising edge
const uint32_t PRE_TRIGGER_SAMPLES = 250; 
const uint32_t POST_TRIGGER_SAMPLES = BUFFER_SIZE - PRE_TRIGGER_SAMPLES - 1;

// Show waveform is trigger doesn't occur
const uint64_t AUTO_TRIGGER_TIMEOUT_US = 1000000; // 1 second

uint16_t previous_sample = 0;

absolute_time_t auto_trigger_start;

int main() {
    stdio_init_all();

    // Circular Buffer init
    CircularBuffer buffer;
    init_buffer(&buffer);

    // Onboard LED init (Debugging)
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

    auto_trigger_start = get_absolute_time();

    while (1) {

        // Checking for CONFIG changes
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

        // Generte Signal
        if (absolute_time_diff_us(get_absolute_time(), signal_toggle_time) <= 0) {
            signal_state = !signal_state;
            gpio_put(SIGNAL_PIN, signal_state);
            signal_toggle_time = make_timeout_time_us(SIGNAL_PERIOD_US / 2);
        }

        uint16_t sample = adc_read();
        write_buffer(&buffer, sample);

        bool trigger_detected = previous_sample < trigger_level && sample >= trigger_level;

        previous_sample = sample;

        // Waveform history before trigger
        if ((buffer.full || buffer.write_index >= PRE_TRIGGER_SAMPLES) && trigger_detected && !command_processing) {
            
            // Must check one previous sample since write_index points to next index to write to
            uint32_t trigger_position = buffer.full ? BUFFER_SIZE - 1 : buffer.write_index - 1;

            // Find oldest position needed to obtain PRE_TRIGGER_SAMPLES before trigger
            uint32_t start_position = trigger_position - PRE_TRIGGER_SAMPLES;

            for (uint32_t i = 0; i < PRE_TRIGGER_SAMPLES; i++) {
                uint32_t position = buffer.full ? (start_position + i) % BUFFER_SIZE : start_position + i;

                if (buffer.full) {
                    output[i] = buffer.data[(buffer.write_index + position) % BUFFER_SIZE];
                } else {
                    output[i] = buffer.data[position];
                }
            }
            
            output[PRE_TRIGGER_SAMPLES] = sample;

            absolute_time_t start_time = get_absolute_time();

            // Copy pre-trigger samples
            for (uint32_t i = 0; i < POST_TRIGGER_SAMPLES; i++) {

                // Continue Signal Generation
                if (absolute_time_diff_us(get_absolute_time(), signal_toggle_time) <= 0) {
                    signal_state = !signal_state;
                    gpio_put(SIGNAL_PIN, signal_state);
                    signal_toggle_time = make_timeout_time_us(SIGNAL_PERIOD_US / 2);
                }     
                
                uint16_t post_sample = adc_read();
                output[PRE_TRIGGER_SAMPLES + 1 + i] = post_sample;
                write_buffer(&buffer, post_sample);
                sleep_us(sample_period_us);
            }

            absolute_time_t end_time = get_absolute_time();

            uint64_t elapsed_us = absolute_time_diff_us(start_time, end_time);
            uint32_t actual_rate = (uint32_t)((POST_TRIGGER_SAMPLES * 1000000ULL) / elapsed_us);

            printf("ACTUAL_RATE %lu\n", actual_rate);
            
            printf("START\n");
            for (uint32_t i = 0; i < BUFFER_SIZE; i++) {
                printf("%d\n", output[i]);
            }

            printf("END\n");

            auto_trigger_start = get_absolute_time();
        }

        if (buffer.full && !command_processing && absolute_time_diff_us(auto_trigger_start, get_absolute_time()) >= AUTO_TRIGGER_TIMEOUT_US) {
            copy_buffer(&buffer, output);

            printf("AUTO TRiGGER\n");
            
            printf("START\n");
            
            for (uint32_t i = 0; i < BUFFER_SIZE; i++) {
                printf("%d\n", output[i]);
            }

            printf("END\n");

            auto_trigger_start = get_absolute_time();
        }

        sleep_us(sample_period_us);
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