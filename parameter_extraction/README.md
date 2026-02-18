# Parameter Extraction

Device parameter extraction for compact model development and characterization.

## Overview

This directory contains methodologies and simulations for extracting device parameters from TCAD simulations or measurement data for use in compact models (SPICE, BSIM, etc.).

## Parameter Categories

### 1. Basic Device Parameters
- Oxide thickness (tox, EOT)
- Channel length (Leff, Lgate)
- Channel width (W)
- Junction depths (Xj)
- Doping concentrations (Na, Nd)

### 2. Threshold Voltage Parameters
- Zero-bias threshold voltage (Vth0)
- Body effect coefficient (γ)
- Channel length modulation (λ)
- DIBL coefficient
- Short-channel effects parameters

### 3. Mobility Parameters
- Low-field mobility (μ0)
- Vertical field mobility degradation (θ)
- Coulomb scattering coefficient
- Phonon scattering coefficient
- Surface roughness scattering

### 4. Capacitance Parameters
- Gate oxide capacitance (Cox)
- Overlap capacitances (Cgso, Cgdo, Cgbo)
- Junction capacitances (Cj, Cjsw)
- Gate-to-bulk capacitance
- Fringing capacitances

### 5. Series Resistance
- Source resistance (Rs)
- Drain resistance (Rd)
- Gate resistance (Rg)
- Contact resistance (Rc)

### 6. Leakage Parameters
- Gate leakage current
- Junction leakage
- GIDL (Gate-Induced Drain Leakage)
- Subthreshold parameters (n, SS)

## Extraction Methods

### Direct Extraction
- Geometrical parameters from structure
- Doping from profiles
- Capacitance from C-V curves

### Optimization-Based Extraction
- Parameter fitting to measured data
- Multi-objective optimization
- Sensitivity analysis
- Parameter correlation handling

### Physics-Based Extraction
- Split C-V method for mobility
- Y-function method for mobility/Vth
- Gated diode for series resistance
- Shift-and-ratio for Vth

## BSIM Model Parameters

### BSIM4 Key Parameters
- VTH0 (threshold voltage)
- U0 (low-field mobility)
- VSAT (saturation velocity)
- TOXE (electrical oxide thickness)
- K1, K2 (body effect)
- AGS (gate bias effect on output resistance)
- PCLM (channel length modulation)
- A0 (bulk charge effect)

### Parameter Extraction Flow
1. Extract geometrical and process parameters
2. Extract threshold voltage parameters
3. Extract mobility parameters
4. Extract series resistance
5. Extract capacitance parameters
6. Extract channel length modulation
7. Validate and optimize

## Tools Used

- **Sentaurus Device**: Generate I-V, C-V data
- **Inspect**: Data extraction and processing
- **Python/MATLAB**: Optimization algorithms
- **UTMOST**: Automated parameter extraction (if available)
- **IC-CAP**: Parameter extraction suite (if available)

## Simulation Setup

### DC Characterization
```tcl
# Id-Vg sweeps at multiple Vd
# Id-Vd sweeps at multiple Vg  
# Multiple geometries (W/L variations)
# Body bias sweeps for body effect
```

### AC Characterization
```tcl
# C-V measurements
# Small-signal parameters
# Y-parameters or S-parameters
```

## Data Requirements

### Measurement/Simulation Matrix
- Multiple gate lengths: L = 0.1, 0.2, 0.5, 1, 2, 5, 10 μm
- Multiple widths: W = 1, 2, 5, 10, 20 μm
- Multiple temperatures: T = -40, 27, 85, 125°C
- Multiple body biases: Vb = 0, -0.5, -1, -2 V
- Drain voltages: Vd = 0.05, 1.0, 1.2, 2.5 V

## Extraction Procedures

### 1. Threshold Voltage (Vth)
```python
# Linear extrapolation method
# Find max(gm) point
# Extrapolate linear region to Id=0
# Vth = Vg intercept
```

### 2. Mobility (μeff)
```python
# Split C-V method
# μeff = L/(W·Cox·(Vg-Vth)) · gd
# At low Vd (linear region)
```

### 3. Series Resistance (Rs, Rd)
```python
# Shift-and-ratio method
# Compare long and short channels
# Extract from linear region resistance
```

### 4. Channel Length Modulation (λ)
```python
# From Id-Vd saturation region slope
# λ = (1/Id)·(dId/dVd)
```

## Output Files

- Extracted parameter tables
- Parameter vs. geometry plots
- Parameter vs. temperature
- Model card files (.lib)
- Validation plots (measured vs. modeled)

## Validation and Optimization

### Model Validation
- Compare TCAD vs. compact model
- Check all operating regions:
  - Subthreshold
  - Linear
  - Saturation
- Multiple bias conditions
- Multiple geometries

### Optimization Techniques
- Least-squares fitting
- Genetic algorithms
- Gradient-based optimization
- Multi-start optimization
- Global vs. local optimization

## Parameter Correlation

### Interdependent Parameters
- Vth and mobility
- Series resistance and mobility
- Overlap capacitance and Leff
- Body effect and substrate doping

### Extraction Order
1. Geometrical parameters (fixed)
2. Threshold voltage
3. Mobility parameters
4. Series resistance
5. Output conductance
6. Capacitances

## Typical Parameter Ranges

### NMOS (example values)
- Vth0 = 0.3 - 0.7 V
- μ0 = 300 - 600 cm²/V·s
- Vsat = 1×10⁵ - 1×10⁷ cm/s
- Rs, Rd = 50 - 200 Ω·μm

### PMOS (example values)
- Vth0 = -0.3 to -0.7 V
- μ0 = 100 - 300 cm²/V·s
- Vsat = 8×10⁴ - 8×10⁶ cm/s
- Rs, Rd = 100 - 400 Ω·μm

## Best Practices

1. Extract parameters in logical order
2. Use appropriate measurement/simulation conditions
3. Validate at each step
4. Document parameter sources
5. Consider temperature and geometry scaling
6. Check parameter physical validity
7. Perform sensitivity analysis
8. Maintain parameter database
