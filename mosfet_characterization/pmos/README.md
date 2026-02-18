# PMOS Characterization

P-type MOSFET characterization simulations and parameter extraction.

## Overview

This directory contains device simulations for PMOS transistors, including:
- DC I-V characteristics
- AC small-signal analysis
- Parameter extraction
- Performance optimization

## Simulation Types

### Transfer Characteristics (Id-Vg)
- Linear region (low |Vd|)
- Saturation region (high |Vd|)
- Log-scale for subthreshold
- Multiple temperatures

### Output Characteristics (Id-Vd)
- Multiple Vg bias points
- Linear to saturation transition
- Channel length modulation
- Output resistance

## Typical Device Parameters

- **Channel Length**: 0.1 - 10 μm
- **Channel Width**: 2 - 200 μm (often 2-3× NMOS)
- **Gate Oxide**: 1 - 10 nm
- **Vth**: -0.3 to -0.7 V (typical)
- **Supply Voltage**: -1.0 to -2.5 V

## PMOS Considerations

- Lower mobility than NMOS (holes vs. electrons)
- Typically requires larger W for same drive current
- Different optimal channel doping
- Temperature coefficient differences

## File Organization

```
pmos/
├── idvg/              # Transfer characteristics
├── idvd/              # Output characteristics
├── extraction/        # Parameter extraction
└── README.md          # This file
```

## Running Simulations

```bash
# Transfer characteristics
cd idvg
sdevice pmos_idvg.cmd

# Output characteristics
cd idvd
sdevice pmos_idvd.cmd
```

## Analysis

- Extract Vth, SS, DIBL, Ion, Ioff
- Plot linear and log-scale curves
- Compare with NMOS
- Optimize W/L ratio for CMOS
