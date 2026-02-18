# RF Analysis

High-frequency and RF performance analysis for semiconductor devices.

## Overview

This directory contains simulations and analysis for RF (Radio Frequency) performance characterization of devices, focusing on high-frequency behavior and key RF metrics.

## RF Performance Metrics

### 1. S-Parameters (Scattering Parameters)
- S11, S12, S21, S22 extraction
- Impedance matching analysis
- Frequency-dependent behavior
- Two-port network characterization

### 2. Cut-off Frequency (fT)
- Unity current gain frequency
- Small-signal current gain (h21)
- Frequency response analysis
- Bias dependence

### 3. Maximum Oscillation Frequency (fmax)
- Unity power gain frequency
- Mason's unilateral gain
- Device stability
- Power performance

### 4. Small-Signal Parameters
- Input capacitance (Cgs, Cgd)
- Output capacitance (Cds)
- Gate resistance (Rg)
- Source/drain resistance (Rs, Rd)
- Transconductance (gm)
- Output conductance (gd)

### 5. Noise Analysis
- Noise figure (NF)
- Minimum noise figure (NFmin)
- Noise parameters
- Frequency dependence

## Simulation Approach

### AC Analysis
- Small-signal AC simulation
- Frequency sweep (1 MHz - 100 GHz)
- Bias point optimization
- Impedance extraction

### Mixed-Mode Analysis
- AC and DC coupled simulation
- Operating point determination
- Small-signal linearization

## Key Applications

- **LNA Design**: Low-noise amplifier optimization
- **PA Design**: Power amplifier characterization
- **Mixer Design**: Frequency conversion analysis
- **Oscillator Design**: Negative resistance, gain
- **Switch Design**: Insertion loss, isolation

## Physics Models

- Drift-diffusion with AC analysis
- High-frequency mobility models
- Gate resistance effects
- Substrate coupling
- Parasitic capacitances
- NQS (Non-Quasi-Static) effects

## Simulation Setup

### Device Configuration
- Appropriate biasing (Vg, Vd)
- Contact definitions for ports
- Substrate connection
- Source degeneration (if applicable)

### AC Analysis Settings
- Frequency range and stepping
- Number of frequency points
- Convergence criteria
- Small-signal perturbation

## Tools Used

- **Sentaurus Device (sdevice)**: AC small-signal simulation
- **EMW (ElectroMagnetic Wave)**: Full-wave EM simulation
- **Sentaurus Visual**: Result visualization
- **Inspect**: Data extraction and plotting

## Running Simulations

```bash
# Run AC analysis
sdevice rf_ac_analysis.cmd

# Extract S-parameters
inspect -l rf_ac_analysis.log

# Plot frequency response
python plot_rf_metrics.py
```

## Output Files

- AC impedance data
- S-parameter files (.s2p format)
- Frequency-dependent gain
- Capacitance vs. frequency
- Noise parameters

## Analysis Scripts

Python/MATLAB scripts for:
- S-parameter plotting (Smith charts)
- fT and fmax extraction
- Noise figure calculation
- Stability factor analysis
- De-embedding procedures

## Parameter Extraction

### fT Extraction
1. Extract h21 (short-circuit current gain)
2. Plot |h21| vs. frequency (log-log)
3. Extrapolate to unity gain (0 dB)
4. Read fT at unity gain

### fmax Extraction
1. Calculate unilateral power gain (U)
2. Plot U vs. frequency (log-log)
3. Extrapolate to unity gain
4. Read fmax at unity gain

## Optimization Targets

- Maximize fT and fmax
- Minimize gate resistance
- Reduce parasitic capacitances
- Optimize device geometry
- Balance noise and gain

## Typical Results

- fT range: 10 GHz - 300 GHz (depending on technology)
- fmax range: 20 GHz - 500 GHz
- Noise figure: 1-3 dB (for optimized LNA)
- Input/output impedance at 50Ω matching
