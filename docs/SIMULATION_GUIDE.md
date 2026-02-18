# TCAD Simulation Guide

Comprehensive guide for running TCAD simulations in this repository.

## Table of Contents

1. [Introduction](#introduction)
2. [Software Setup](#software-setup)
3. [Simulation Workflow](#simulation-workflow)
4. [Best Practices](#best-practices)
5. [Common Issues](#common-issues)

## Introduction

This guide provides essential information for working with Synopsys Sentaurus TCAD simulations in this repository.

## Software Setup

### Prerequisites

1. **Synopsys Sentaurus TCAD Installation**
   - Version: 2022.03 or later recommended
   - Required modules:
     - Sentaurus Process (sprocess)
     - Sentaurus Device (sdevice)
     - Sentaurus Structure Editor (SDE)
     - Sentaurus Visual (svisual)
     - Inspect

2. **Environment Setup**
   ```bash
   # Add to .bashrc or .bash_profile
   export STROOT=/path/to/sentaurus/installation
   export PATH=$STROOT/bin:$PATH
   export LM_LICENSE_FILE=port@license_server
   ```

3. **Python Environment** (for post-processing)
   ```bash
   pip install numpy matplotlib pandas scipy
   ```

## Simulation Workflow

### 1. Structure Definition

**Option A: Using SDE (GUI)**
```bash
sde &
# Use GUI to create device structure
# Save as structure.cmd
```

**Option B: Using Command File**
```tcl
# structure.cmd
(sdegeo:create-rectangle ...)
(sdedr:define-constant-profile ...)
```

### 2. Process Simulation

```bash
# Run process simulation
sprocess input_process.cmd

# Output: final_structure_fps.tdr
```

### 3. Device Simulation

```bash
# Run device simulation
sdevice input_device.cmd

# Outputs: 
#   - n@node@_des.tdr (structure with solution)
#   - n@node@_des.plt (plot files)
#   - n@node@.log (simulation log)
```

### 4. Visualization and Analysis

```bash
# Visualize structure and results
svisual output_des.tdr

# Extract data
inspect -l output.log

# Plot results
python plot_results.py
```

## Best Practices

### Meshing

1. **Adaptive Meshing**
   ```tcl
   Physics {
       Mesh { 
           Adaptive { MaxRefineLevel=3 }
       }
   }
   ```

2. **Critical Region Refinement**
   - Fine mesh in channel region
   - Fine mesh at junctions
   - Coarser mesh in bulk

3. **Mesh Quality Checks**
   - Aspect ratio < 100:1
   - Smooth transitions
   - Adequate resolution

### Physics Models

1. **Basic Models** (always include)
   ```tcl
   Physics {
       Mobility(DopingDependence)
       Recombination(SRH Auger)
   }
   ```

2. **Advanced Models** (when needed)
   ```tcl
   Physics {
       Hydrodynamic           # High-field transport
       QuantumPotential       # Quantum effects
       Thermodynamic          # Self-heating
   }
   ```

### Convergence

1. **Start Simple**
   - Begin with basic physics models
   - Add complexity incrementally
   - Verify convergence at each step

2. **Convergence Parameters**
   ```tcl
   Solve {
       Coupled { Iterations=100 }
       NotDamped=100
   }
   ```

3. **Troubleshooting**
   - Reduce voltage steps
   - Increase damping
   - Refine mesh
   - Check for negative concentrations

## Common Issues

### Issue 1: Non-Convergence

**Symptoms**: Simulation stops with convergence error

**Solutions**:
- Reduce voltage/bias steps
- Increase maximum iterations
- Improve mesh quality
- Check boundary conditions
- Start from previous solution

### Issue 2: Unphysical Results

**Symptoms**: Negative currents, incorrect polarity

**Solutions**:
- Verify doping types and concentrations
- Check contact definitions
- Verify bias polarities
- Review physics models

### Issue 3: Long Runtime

**Symptoms**: Simulation takes too long

**Solutions**:
- Optimize mesh (fewer elements)
- Use 2D instead of 3D when possible
- Disable unnecessary physics models
- Use parallel processing
- Save intermediate results

### Issue 4: Memory Issues

**Symptoms**: Out of memory errors

**Solutions**:
- Reduce mesh density
- Use 64-bit version
- Increase system memory
- Split simulation into steps
- Use cluster resources

## File Management

### Naming Conventions

- Process files: `process_<description>.cmd`
- Device files: `device_<test>_<conditions>.cmd`
- Structures: `structure_<device>_<variant>.tdr`
- Results: `<device>_<test>_results.plt`

### Version Control

- Track `.cmd` files (simulation input)
- Track `.par` files (parameters)
- Ignore `.tdr` files (large binary)
- Ignore `.log` files (generated)
- Include `.gitignore` for TCAD outputs

### Backup Strategy

- Regular backups of input files
- Archive important results
- Document simulation conditions
- Keep parameter change log

## Performance Optimization

### Parallel Processing

```bash
# Use multiple cores
sdevice -n 4 input.cmd

# Distributed computing
sdevice -m "host1 host2" input.cmd
```

### Mesh Optimization

1. Use appropriate element types
2. Leverage symmetry
3. Optimize refinement regions
4. Balance accuracy vs. speed

### Solver Options

```tcl
Math {
    Method=ILS          # Iterative linear solver (faster)
    DirectSolver        # Direct solver (more robust)
    Extrapolate         # Use previous solution
    Derivatives         # Numerical derivatives
}
```

## Resources

- Synopsys SolvNetPlus: Official documentation and examples
- TCAD Central: Community forum
- This repository: `examples/` directory
- Training materials: `docs/` directory

## Contact and Support

For issues specific to this repository, please open an issue on GitHub.

For TCAD software issues, contact Synopsys support or your local CAE team.
