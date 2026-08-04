#include "circular_buffer.h"


void init_buffer(CircularBuffer* buffer)
{
    buffer->write_index = 0;
    buffer->full = false;
}


void write_buffer(CircularBuffer* buffer, uint16_t sample)
{
    buffer->data[buffer->write_index] = sample;

    buffer->write_index++;

    if (buffer->write_index == BUFFER_SIZE)
    {
        buffer->write_index = 0;
        buffer->full = true;
    }
}


void copy_buffer(CircularBuffer* buffer, uint16_t* output)
{
    uint32_t index = buffer->full ? buffer->write_index : 0;
    uint32_t length = buffer->full ? BUFFER_SIZE : buffer->write_index;

    for (uint32_t i = 0; i < length; i++)
    {
        output[i] = buffer->data[index];

        index++;

        if (index == BUFFER_SIZE)
        {
            index = 0;
        }
    }
}


uint16_t read_buffer(CircularBuffer* buffer, uint32_t position)
{
    if (!buffer->full && position >= buffer->write_index)
    {
        return 0;
    }

    uint32_t index;

    if (buffer->full)
    {
        index = (buffer->write_index + position) % BUFFER_SIZE;
    }
    else
    {
        index = position;
    }

    return buffer->data[index];
}