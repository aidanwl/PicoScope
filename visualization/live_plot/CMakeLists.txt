cmake_minimum_required(VERSION 3.12)

# SDK Location
set(PICO_SDK_PATH "/home/awong50/pico/pico-sdk/")

include(${PICO_SDK_PATH}/pico_sdk_init.cmake)

project(SignalAcquisition)

pico_sdk_init()

add_executable(SignalAcquisition
    signal_acquisition.cpp
    ../../lib/circular_buffer/circular_buffer.cpp
)

target_include_directories(SignalAcquisition PRIVATE
    ../../lib/circular_buffer
)

target_link_libraries(SignalAcquisition
    pico_stdlib
    hardware_adc
    hardware_gpio
)

pico_add_extra_outputs(SignalAcquisition)
pico_enable_stdio_usb(SignalAcquisition 1)
pico_enable_stdio_uart(SignalAcquisition 0)
