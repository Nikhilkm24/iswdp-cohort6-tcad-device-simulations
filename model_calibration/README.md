# Model Calibration

Model calibration and validation for compact device models.

## Overview

This directory contains methodologies for calibrating TCAD models and compact models (SPICE/BSIM) against measurement data or reference simulations.

## Calibration Objectives

1. **Accuracy**: Match target data within acceptable error
2. **Predictivity**: Extrapolate beyond calibration range
3. **Robustness**: Stable across process variations
4. **Scalability**: Valid for different geometries
5. **Physical Validity**: Parameters within physical limits

## Calibration Types

### 1. Process Calibration
- Implantation dose and energy
- Diffusion coefficients
- Oxidation rates
- Etch rates
- Deposition parameters

### 2. Device Model Calibration
- Transport models (mobility, velocity saturation)
- Recombination models (SRH, Auger)
- Tunneling models (gate leakage)
- Impact ionization
- Temperature dependencies

### 3. Compact Model Calibration
- BSIM4/BSIM6 parameters
- PSP model parameters
- HiSIM model parameters
- RF model parameters
- Noise model parameters

## Calibration Flow

### Step 1: Define Target Data
- Measurement data (silicon results)
- Reference TCAD simulations
- Published data (if no measurements)
- Identify critical characteristics

### Step 2: Select Calibration Parameters
- Physical parameters (doping, oxide thickness)
- Model parameters (mobility coefficients)
- Numerical parameters (if needed)
- Set parameter ranges

### Step 3: Define Error Metrics
- Mean squared error (MSE)
- Root mean squared error (RMSE)
- Mean absolute percentage error (MAPE)
- Maximum error
- Weighted combinations

### Step 4: Optimization
- Manual tuning (initial)
- Automated optimization
- Multi-objective optimization
- Parameter sensitivity analysis

### Step 5: Validation
- Compare calibrated vs. target
- Test on validation dataset
- Check extrapolation capability
- Verify physical consistency

## Calibration Targets

### DC Characteristics
- Id-Vg curves (linear and log scale)
- Id-Vd curves
- Threshold voltage
- Subthreshold slope
- Output conductance
- Body effect

### AC Characteristics
- Gate capacitance (C-V)
- Small-signal parameters
- S-parameters
- fT and fmax

### Temperature Dependence
- Parameter temperature coefficients
- Temperature-dependent mobility
- Leakage temperature dependence

### Geometry Scaling
- Short-channel effects
- Narrow-width effects
- Length and width dependence

## Tools and Methods

### Optimization Algorithms
- **Simplex Method**: Fast, local optimization
- **Levenberg-Marquardt**: Nonlinear least squares
- **Genetic Algorithm**: Global optimization
- **Particle Swarm**: Multi-modal optimization
- **Bayesian Optimization**: Efficient sampling

### Software Tools
- **Sentaurus Parameter Optimizer**: Automated calibration
- **Python scipy.optimize**: Custom scripts
- **MATLAB Optimization Toolbox**: Advanced algorithms
- **IC-CAP**: Industry-standard tool
- **UTMOST**: Parameter extraction/optimization

## Calibration Database

### Data Organization
```
calibration/
├── target_data/          # Measurement or reference data
├── initial_parameters/   # Starting parameter sets
├── calibrated_models/    # Calibrated parameter files
├── validation_results/   # Comparison plots
└── optimization_logs/    # Convergence history
```

### Parameter Tracking
- Version control for parameter sets
- Change logs and notes
- Calibration date and source
- Responsible engineer
- Validation status

## Error Metrics

### Relative Error
```
ε_rel = |I_sim - I_target| / |I_target|
```

### RMS Error
```
RMSE = sqrt(Σ(I_sim - I_target)² / N)
```

### Log-Scale Error (for currents)
```
ε_log = |log(I_sim) - log(I_target)|
```

### Weighted Error
```
ε_weighted = w_linear·ε_linear + w_log·ε_log
```

## Validation Procedures

### Cross-Validation
1. Split data into calibration and validation sets
2. Calibrate on calibration set
3. Validate on validation set
4. Check for overfitting

### Physical Validation
- Parameter values within physical limits
- Monotonic dependencies where expected
- Correct temperature coefficients
- Reasonable extrapolation

### Statistical Validation
- Error distribution analysis
- Outlier identification
- Confidence intervals
- Correlation analysis

## Corner Models

### Process Corners
- **TT**: Typical-Typical (nominal)
- **FF**: Fast-Fast (best case speed)
- **SS**: Slow-Slow (worst case speed)
- **SF**: Slow NMOS, Fast PMOS
- **FS**: Fast NMOS, Slow PMOS

### Corner Calibration
1. Identify key process parameters
2. Define ±3σ variations
3. Simulate corner cases
4. Extract corner model parameters
5. Validate circuit performance

## Statistical Calibration

### Monte Carlo Analysis
- Random parameter variations
- Statistical distributions (Gaussian, uniform)
- Correlation between parameters
- Yield analysis

### Response Surface Methodology
- Design of experiments (DOE)
- Parameter space sampling
- Response surface fitting
- Sensitivity analysis

## Documentation

### Calibration Report
1. **Objective**: What was calibrated and why
2. **Data Source**: Origin of target data
3. **Method**: Calibration procedure and tools
4. **Results**: Achieved accuracy and validation
5. **Parameters**: Final calibrated values
6. **Limitations**: Known issues and restrictions
7. **Recommendations**: Suggested improvements

## Best Practices

1. **Start Simple**: Begin with key parameters
2. **Validate Early**: Check results at each step
3. **Document Everything**: Track all changes
4. **Physical First**: Prioritize physical parameters
5. **Avoid Overfitting**: Don't tune too many parameters
6. **Test Extrapolation**: Verify beyond calibration range
7. **Version Control**: Maintain parameter history
8. **Peer Review**: Have others validate results

## Common Pitfalls

- Over-parameterization (too many free parameters)
- Local minima trapping
- Ignoring parameter correlations
- Insufficient validation data
- Unrealistic parameter values
- Poor initial guesses
- Inadequate error metrics

## Example Results

### Before Calibration
- RMSE: 15-30% typical
- Poor subthreshold match
- Incorrect temperature dependence

### After Calibration
- RMSE: <5% target
- Excellent subthreshold agreement
- Accurate temperature scaling
- Valid across geometries
