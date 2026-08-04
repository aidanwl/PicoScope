#ifndef CIRCULAR_BUFFER_H
#define CIRCULAR_BUFFER_H

#include <cstdint>

const uint32_t BUFFER_SIZE = 1000;

struct CircularBuffer {
    uint16_t data[BUFFER_SIZE];
    uint32_t write_index;
    bool full;
};

void init_buffer(CircularBuffer* buffer);

void write_buffer(CircularBuffer* buffer, uint16_t sample);

void copy_buffer(CircularBuffer* buffer, uint16_t* output);

uint16_t read_buffer(CircularBuffer* buffer, uint32_t position);


#endif

