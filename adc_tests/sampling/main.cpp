/*
ADC Sampling Test: Tests the Pico ADC sampling system by acquiring analog samples at a target sampling rate and then measuring the actual acquisition rate
*/

#include <iostream>
#include "pico/stdlib.h"
#include "pico/time.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"

using namespace std;

float get_voltage() {
    return adc_read() * 3.3f / 4095.0f;
}

// Measures the maximum ADC acquisition rate using software polling
double max_acquisition_rate(uint64_t samples) {

    absolute_time_t start_time = get_absolute_time();

    for (uint64_t i = 0; i < samples; i++) {
        get_voltage();
    }

    absolute_time_t end_time = get_absolute_time();

    return samples / (absolute_time_diff_us(start_time, end_time) / 1000000.0);
}

int main() {
    stdio_init_all();

    cout << "Sampling Test" << endl;

    adc_init();

    adc_gpio_init(26);
    adc_select_input(0);

    while (1) {
        uint64_t samples = 10000000;
        float max_rate = max_acquisition_rate(samples);
        cout << "Maximum Acquisition Rate: " << max_rate << " kS/s" << endl;

        sleep_ms(1000);
    }    
    
}