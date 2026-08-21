/*
Circular Buffer Test: Simple circular buffer with test code
*/

#include <iostream>

using namespace std;

const int BUFFER_SIZE = 1000;

struct CircularBuffer {
    uint16_t data[BUFFER_SIZE];
    uint32_t write_index;
    bool full;
};

void init_buffer(CircularBuffer* buffer) {
    buffer->write_index = 0;
    buffer->full = false;
}

void write_buffer(CircularBuffer* buffer, uint16_t sample) {
    buffer->data[buffer->write_index] = sample;
    buffer->write_index++;

    if (buffer->write_index == BUFFER_SIZE) {
        buffer->write_index = 0;
        buffer->full = true;
    }
}

void copy_buffer(CircularBuffer* buffer, uint16_t* output) {
    uint32_t index = buffer->full ?  buffer->write_index : 0;
    uint32_t length = buffer->full ? BUFFER_SIZE : buffer->write_index;

    for (uint32_t i = 0; i < length; i++) {
        output[i] = buffer->data[index];
        index++;

        if (index == BUFFER_SIZE) {
            index = 0;
        }
    }


}

uint16_t read_buffer(CircularBuffer* buffer, uint32_t position) {
    if (!buffer->full && position >= buffer->write_index) {
        return 0;
    }

    uint32_t index = buffer->full ? (buffer->write_index + position) % BUFFER_SIZE : position;

    return buffer->data[index];
}


int main() {
    CircularBuffer buffer;

    init_buffer(&buffer);

    for (uint16_t i = 0; i < 1500; i++) {
        write_buffer(&buffer, i);
    }

    uint16_t output[BUFFER_SIZE];

    copy_buffer(&buffer, output);

    for (int i = 0; i < BUFFER_SIZE; i++) {
        cout << "Position " << i << ": " << output[i] << endl;
    }
}