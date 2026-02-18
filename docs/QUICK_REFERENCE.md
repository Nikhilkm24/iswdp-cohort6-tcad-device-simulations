# TCAD Quick Reference

Essential commands and tips for TCAD simulations.

## Common Commands

### Running Simulations

```bash
# Process simulation
sprocess input.cmd

# Device simulation
sdevice input.cmd

# With multiple cores
sdevice -n 4 input.cmd

# Interactive mode
sdevice -i input.cmd
```

### Visualization

```bash
# Sentaurus Visual
svisual structure.tdr

# Inspect (plotting)
inspect
inspect -l simulation.log
inspect -df output.plt
```

### File Management

```bash
# View TDR file info
tdx -info structure.tdr

# Convert TDR to VTK
tdx -vt structure.tdr

# Extract 1D profile
tdx -1d -x 0 -y 0 structure.tdr
```

## Typical Simulation Flow

1. **Define Structure**
   - Use SDE GUI or command file
   - Set geometry and doping

2. **Run Process Simulation** (optional)
   ```bash
   sprocess process.cmd
   ```

3. **Run Device Simulation**
   ```bash
   sdevice device.cmd
   ```

4. **Visualize Results**
   ```bash
   svisual output_des.tdr
   ```

5. **Extract Data**
   ```bash
   inspect -df output_des.plt
   ```

## Key Physics Models

### Always Include
```tcl
Physics {
    Mobility(DopingDependence HighFieldSaturation)
    Recombination(SRH Auger)
    EffectiveIntrinsicDensity(BandGapNarrowing)
}
```

### For Advanced Simulations
```tcl
Physics {
    Hydrodynamic              # High-field transport
    QuantumPotential          # Quantum effects
    Thermodynamic             # Self-heating
    eBarrierTunneling         # Gate tunneling
}
```

## Common Plot Variables

```tcl
Plot {
    eDensity hDensity          # Carrier densities
    ElectricField Potential     # Fields
    eCurrent hCurrent          # Currents
    Doping                     # Doping profile
    eMobility hMobility        # Mobility
    eVelocity hVelocity        # Velocity
    ConductionBand ValenceBand # Band structure
}
```

## Troubleshooting Quick Fixes

### Non-Convergence
1. Reduce voltage steps: `MaxStep=0.01`
2. Increase iterations: `Iterations=100`
3. Reduce damping: `NotDamped=100`

### Mesh Issues
1. Refine critical regions
2. Check aspect ratio < 100:1
3. Use adaptive meshing

### Runtime Issues
1. Use 2D instead of 3D
2. Enable parallelization
3. Optimize mesh

## File Extensions

- `.cmd` - Command/input files
- `.tdr` - Structure/result files (binary)
- `.plt` - Plot data files (ASCII)
- `.log` - Simulation log files
- `.par` - Parameter files
- `.dat` - Data files

## Useful Environment Variables

```bash
export STROOT=/path/to/sentaurus
export PATH=$STROOT/bin:$PATH
export LM_LICENSE_FILE=port@server

# Parallel processing
export SNPS_MAX_WORKERS=8
```

## Quick Parameter Ranges

### NMOS (typical)
- Vth: 0.3-0.7 V
- μ: 300-600 cm²/V·s
- Ion: 500-1000 μA/μm

### PMOS (typical)
- Vth: -0.3 to -0.7 V
- μ: 100-300 cm²/V·s
- Ion: 300-700 μA/μm

## Resources

- SolvNetPlus: Official Synopsys documentation
- This repo: Examples and detailed guides
- `docs/`: Comprehensive guides
- TCAD Central: Community forum

## Emergency Contacts

For software issues:
- Synopsys support
- Local CAE team
- ISWDP instructors

For repository issues:
- Open GitHub issue
- Check documentation first
