cmake_minimum_required(VERSION 3.12)

# SDK Location
set(PICO_SDK_PATH "/home/aidan/pico/pico-sdk/")

include(${PICO_SDK_PATH}/pico_sdk_init.cmake)

project(PicoScope)

pico_sdk_init()

add_executable(PicoScope
    main.cpp
    ../lib/circular_buffer/circular_buffer.cpp
)

target_include_directories(PicoScope PRIVATE
    ../lib/circular_buffer
)

target_link_libraries(PicoScope
    pico_stdlib
    hardware_adc
    hardware_gpio
)

pico_add_extra_outputs(PicoScope)
pico_enable_stdio_usb(PicoScope 1)
pico_enable_stdio_uart(PicoScope 0)
