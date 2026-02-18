# MOSFET Characterization

Comprehensive MOSFET device characterization simulations including both NMOS and PMOS devices.

## Overview

This directory contains device simulations for extracting key MOSFET electrical characteristics and performance parameters.

## Simulation Types

### Current-Voltage Characteristics

#### Id-Vg (Transfer Characteristics)
- Drain current vs. gate voltage at fixed Vd
- Linear and saturation regions
- Threshold voltage extraction
- Subthreshold slope
- On/off current ratio
- Transconductance (gm)

#### Id-Vd (Output Characteristics)
- Drain current vs. drain voltage at various Vg
- Linear to saturation transition
- Channel length modulation
- Output resistance
- Saturation current

### Key Parameters Extracted

1. **Threshold Voltage (Vth)**
   - Linear extrapolation method
   - Constant current method
   - Transconductance peak method

2. **Subthreshold Slope (SS)**
   - Minimum SS in subthreshold region
   - Interface trap density correlation

3. **DIBL (Drain-Induced Barrier Lowering)**
   - Vth shift with Vd change
   - Short channel effect indicator

4. **Drive Current (Ion)**
   - Maximum current at Vg=Vd=Vdd
   - Performance metric

5. **Off Current (Ioff)**
   - Leakage at Vg=0V
   - Power consumption indicator

6. **On/Off Ratio**
   - Ion/Ioff ratio
   - Digital switching performance

## Directory Structure

```
mosfet_characterization/
├── nmos/                 # N-type MOSFET simulations
│   ├── idvg/            # Transfer characteristics
│   ├── idvd/            # Output characteristics
│   └── extraction/      # Parameter extraction
└── pmos/                # P-type MOSFET simulations
    ├── idvg/            # Transfer characteristics
    ├── idvd/            # Output characteristics
    └── extraction/      # Parameter extraction
```

## Simulation Setup

### Device Structure
- Gate oxide thickness
- Channel doping
- Source/drain doping
- Gate length and width
- Spacer geometry
- Contact positions

### Physics Models
- Drift-diffusion transport
- Shockley-Read-Hall recombination
- Bandgap narrowing
- Mobility models (Philips, Canali)
- Velocity saturation
- Quantization effects (if needed)

## Tools Used

- **Sentaurus Device (sdevice)**: Device simulation
- **Sentaurus Visual**: Visualization and analysis
- **Inspect**: Data plotting and extraction

## Running Simulations

```bash
# Run NMOS Id-Vg simulation
cd nmos/idvg
sdevice nmos_idvg.cmd

# Run PMOS Id-Vd simulation
cd pmos/idvd
sdevice pmos_idvd.cmd

# View results
svisual nmos_idvg_des.tdr
```

## Analysis and Plotting

Use Inspect or Python scripts to:
- Plot I-V curves
- Extract parameters
- Generate log-scale plots
- Calculate derivatives (gm, gd)
- Compare different geometries/conditions

## Example Output Files

- `.plt` files: Electrical characteristic data
- `.tdr` files: Device structure and field distributions
- `.log` files: Simulation log and convergence
- `.par` files: Extracted parameters

## Performance Metrics

### Digital Performance
- Switching speed
- Gate delay
- Power-delay product

### Analog Performance
- Transconductance efficiency (gm/Id)
- Output resistance
- Intrinsic gain

### RF Performance
- Gate capacitance
- Transit time
- Cut-off frequency estimate
