# Thermal Analysis

Thermal characteristics and self-heating analysis for semiconductor devices.

## Overview

This directory contains simulations for analyzing thermal behavior, heat dissipation, and temperature effects in semiconductor devices.

## Key Thermal Phenomena

### 1. Self-Heating Effects
- Joule heating in active regions
- Temperature rise during operation
- Impact on device performance
- Thermal time constants

### 2. Temperature Distribution
- 2D/3D temperature maps
- Hot spot identification
- Gradient analysis
- Spatial temperature profiles

### 3. Thermal Resistance (Rth)
- Junction-to-ambient thermal resistance
- Junction-to-case thermal resistance
- Channel-to-substrate thermal path
- Material-dependent thermal conductivity

### 4. Power Dissipation
- Static power (leakage)
- Dynamic power (switching)
- Total power distribution
- Peak power locations

## Simulation Types

### Steady-State Thermal Analysis
- Equilibrium temperature distribution
- Constant power dissipation
- Thermal resistance extraction
- Heat flux analysis

### Transient Thermal Analysis
- Time-dependent heating/cooling
- Thermal time constants
- Pulsed operation
- Thermal cycling

### Coupled Electro-Thermal Simulation
- Self-consistent electrical and thermal
- Temperature-dependent parameters
- Mobility degradation with temperature
- Leakage increase with temperature

## Physics Models

### Thermal Transport
- Heat diffusion equation
- Thermal conductivity (temperature-dependent)
- Boundary conditions:
  - Isothermal contacts
  - Adiabatic boundaries
  - Convective cooling

### Temperature Effects on Electrical Parameters
- Mobility temperature dependence
- Bandgap temperature coefficient
- Threshold voltage shift
- Saturation velocity change
- Leakage current increase

## Tools Used

- **Sentaurus Device (sdevice)**: Coupled electro-thermal simulation
- **Sentaurus Interconnect**: Package-level thermal analysis
- **Sentaurus Visual**: Temperature visualization
- **Inspect**: Thermal parameter extraction

## Simulation Setup

### Material Properties
- Silicon thermal conductivity: ~150 W/(m·K)
- Oxide thermal conductivity: ~1.4 W/(m·K)
- Metal thermal conductivity: ~200-400 W/(m·K)
- Temperature dependence included

### Boundary Conditions
- Heat sink temperature (ambient)
- Contact thermal resistance
- Substrate backside cooling
- Package thermal model

### Physics Activation
```tcl
Physics {
    Temperature
    Thermodynamic
    HeatFlowModel
}
```

## Key Output Parameters

1. **Maximum Junction Temperature (Tjmax)**
   - Critical for reliability
   - Derating considerations

2. **Thermal Resistance (Rth)**
   - Rth = ΔT / P
   - Units: K/W or °C/W

3. **Temperature Coefficient**
   - ∂Id/∂T at constant bias
   - Performance degradation rate

4. **Thermal Time Constant (τth)**
   - Time to reach thermal equilibrium
   - Important for pulsed operation

## Running Simulations

```bash
# Run steady-state thermal simulation
sdevice thermal_steady_state.cmd

# Run transient thermal simulation
sdevice thermal_transient.cmd

# Run coupled electro-thermal
sdevice coupled_thermal.cmd
```

## Analysis and Visualization

### Temperature Maps
- 2D cross-sectional temperature
- 3D volume temperature rendering
- Isothermal contours

### Thermal Plots
- Temperature vs. power
- Temperature vs. time
- Spatial temperature profiles

## Design Considerations

### Thermal Management
- Heat sink design
- Thermal interface materials
- Package selection
- Die attach quality

### Layout Optimization
- Device spacing
- Power device placement
- Thermal vias
- Multi-finger layouts

### Operating Conditions
- Maximum power limits
- Duty cycle optimization
- Pulsed vs. continuous operation
- Ambient temperature range

## Reliability Impact

### Temperature-Accelerated Degradation
- Electromigration (EM)
- Time-Dependent Dielectric Breakdown (TDDB)
- Hot Carrier Injection (HCI)
- Bias Temperature Instability (BTI)

### Arrhenius Acceleration
- Lifetime = L0 · exp(Ea/kT)
- Acceleration factor calculations

## Example Applications

- Power amplifier thermal design
- High-power LED analysis
- Power MOSFET/IGBT characterization
- Integrated circuit hot spot analysis
- Package thermal evaluation

## Typical Results

- Temperature rise: 10-100°C above ambient
- Thermal resistance: 1-100 K/W (device-dependent)
- Thermal time constant: 1 μs - 1 ms
- Performance degradation: 0.5-2% per °C
