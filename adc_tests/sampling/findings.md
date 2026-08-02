# Sampling Test Findings

## Maximum ADC Acquisition Rate

### Test Setup
- Sample count: 100,000 samples
- Sampling method: Software polling

### Results
- Measured acquisition rate: ~400 kS/s
- ADC theoretical maximum rate: ~500 kS/s

### Notes
- Measured acqusition rate is likely lower due to acquisiton method: software overhead from ADC polling adds time
- Tested higher and lower sample counts - Results are the same