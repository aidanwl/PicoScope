cmake_minimum_required(VERSION 3.12)

# SDK Location
set(PICO_SDK_PATH "/home/awong50/pico/pico-sdk/")

include(${PICO_SDK_PATH}/pico_sdk_init.cmake)

project(CaptureTest)

pico_sdk_init()

add_executable(CaptureTest
    main.cpp    
)

target_link_libraries(CaptureTest
    pico_stdlib
    hardware_adc
    hardware_gpio
)

pico_add_extra_outputs(CaptureTest)
pico_enable_stdio_usb(CaptureTest 1)
pico_enable_stdio_uart(CaptureTest 0)
