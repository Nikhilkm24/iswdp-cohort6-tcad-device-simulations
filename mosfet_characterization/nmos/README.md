# NMOS Characterization

N-type MOSFET characterization simulations and parameter extraction.

## Overview

This directory contains device simulations for NMOS transistors, including:
- DC I-V characteristics
- AC small-signal analysis
- Parameter extraction
- Performance optimization

## Simulation Types

### Transfer Characteristics (Id-Vg)
- Linear region (low Vd)
- Saturation region (high Vd)
- Log-scale for subthreshold
- Multiple temperatures

### Output Characteristics (Id-Vd)
- Multiple Vg bias points
- Linear to saturation transition
- Channel length modulation
- Output resistance

## Typical Device Parameters

- **Channel Length**: 0.1 - 10 μm
- **Channel Width**: 1 - 100 μm
- **Gate Oxide**: 1 - 10 nm
- **Vth**: 0.3 - 0.7 V (typical)
- **Supply Voltage**: 1.0 - 2.5 V

## File Organization

```
nmos/
├── idvg/              # Transfer characteristics
├── idvd/              # Output characteristics
├── extraction/        # Parameter extraction
└── README.md          # This file
```

## Running Simulations

```bash
# Transfer characteristics
cd idvg
sdevice nmos_idvg.cmd

# Output characteristics
cd idvd
sdevice nmos_idvd.cmd
```

## Analysis

- Extract Vth, SS, DIBL, Ion, Ioff
- Plot linear and log-scale curves
- Compare different geometries
- Temperature dependence
