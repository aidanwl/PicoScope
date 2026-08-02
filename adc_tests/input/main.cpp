/*
Potentiometer ADC Test: Converts raw ADC values into voltage measured over USB serial
*/

#include <iostream>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"
using namespace std;

int main() {
    stdio_init_all();
    cout << "Potentiometer Test" << endl;

    adc_init();

    adc_gpio_init(26);
    adc_select_input(0);

    while (1) {
        const float conversion_factor = 3.3f / 4095.0f;
        uint16_t result = adc_read();
        cout << "Voltage:" << result * conversion_factor << endl;
        sleep_ms(500);
    }
}
