# Sampling Test Findings

## Maximum ADC Acquisition Rate

### Test Setup
- Sample count: 100,000 
- Sampling method: Software polling

### Results
- Measured acquisition rate: ~400 kS/s
- ADC theoretical maximum rate: ~500 kS/s

### Notes
- Measured acqusition rate is likely lower due to acquisiton method: software overhead from ADC polling adds time
- Tested higher and lower sample counts - Results are the same

## Controlled Sampling 

### Test Setup
- Sampling method: Software-controlled sampling using `sleep_us()`
- Sample count: 10,000 

### Results

| Requested Sampling Rate | Measured Sampling Rate | Accuracy |
|-------------------------|------------------------|----------|
| 1 kHz                   |        998.002         |  99.8%   |
| 10 kHz                  |        9803.82         |   98%    |
| 50 kHz                  |        45454.1         |   91%    |
| 100 kHz                 |        83331.9         |   83.3%  |

### Notes
- The measured sampling rate is lower than the requested rate due to software overhead (instead of just the period of the sleep and ADC, there is also the code time)
- As the requested sample rate increases, the accuracy decreases because ADC conversion time and software execution overhead becomes a larger portion of the total sampling period