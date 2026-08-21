cmake_minimum_required(VERSION 3.12)

# SDK Location
set(PICO_SDK_PATH "/home/awong50/pico/pico-sdk/")

include(${PICO_SDK_PATH}/pico_sdk_init.cmake)

project(InputTest)

pico_sdk_init()

add_executable(InputTest
    main.cpp    
)

target_link_libraries(InputTest
    pico_stdlib
    hardware_adc
    hardware_gpio
)

pico_add_extra_outputs(InputTest)
pico_enable_stdio_usb(InputTest 1)
pico_enable_stdio_uart(InputTest 0)
