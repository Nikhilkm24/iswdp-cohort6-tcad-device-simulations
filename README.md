# ISWDP Cohort 6 - TCAD Device Simulations

Advanced semiconductor device simulations performed during ISWDP Cohort 6 using Synopsys Sentaurus TCAD, covering 2D/3D process modeling, MOSFET characterization, RF & thermal analysis, parameter extraction, and model calibration.

## Overview

This repository contains comprehensive TCAD (Technology Computer-Aided Design) simulations for semiconductor device analysis and characterization. The simulations are performed using Synopsys Sentaurus TCAD tools and cover various aspects of device physics and performance analysis.

## Repository Structure

```
├── process_modeling/          # 2D and 3D process simulations
│   ├── 2d_simulations/       # Two-dimensional process modeling
│   └── 3d_simulations/       # Three-dimensional process modeling
├── mosfet_characterization/  # MOSFET device characterization
│   ├── nmos/                 # N-type MOSFET simulations
│   └── pmos/                 # P-type MOSFET simulations
├── rf_analysis/              # RF performance analysis
├── thermal_analysis/         # Thermal characteristics and analysis
├── parameter_extraction/     # Device parameter extraction
├── model_calibration/        # Model calibration and validation
├── docs/                     # Documentation and guides
└── examples/                 # Example scripts and workflows
```

## Simulation Categories

### 1. Process Modeling (2D/3D)
- Ion implantation simulations
- Diffusion and annealing processes
- Oxidation and etching
- Thin film deposition
- Complete process flow integration

### 2. MOSFET Characterization
- I-V characteristics (Id-Vg, Id-Vd)
- Threshold voltage extraction
- Subthreshold slope analysis
- Drive current and on/off ratio
- Short channel effects
- DIBL (Drain-Induced Barrier Lowering)
- Gate leakage analysis

### 3. RF Analysis
- High-frequency performance metrics
- S-parameters extraction
- Cut-off frequency (fT) analysis
- Maximum oscillation frequency (fmax)
- Noise figure analysis

### 4. Thermal Analysis
- Self-heating effects
- Temperature distribution
- Thermal resistance extraction
- Power dissipation analysis
- Junction temperature analysis

### 5. Parameter Extraction
- Device model parameters
- BSIM model extraction
- Mobility parameters
- Capacitance parameters
- Series resistance extraction

### 6. Model Calibration
- Model validation against measurements
- Parameter optimization
- Statistical analysis
- Corner model development

## Prerequisites

- Synopsys Sentaurus TCAD suite
  - Sentaurus Structure Editor (SDE)
  - Sentaurus Process
  - Sentaurus Device
  - Sentaurus Visual
  - Inspect (for result analysis)
- Linux/Unix environment
- Python 3.x (for data processing and visualization)

## Getting Started

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Nikhilkm24/iswdp-cohort6-tcad-device-simulations.git
cd iswdp-cohort6-tcad-device-simulations
```

2. Ensure Synopsys Sentaurus TCAD tools are properly installed and configured

### Running Simulations

Each simulation directory contains:
- Input deck files (`.cmd` for device simulations)
- Structure files (`.tdr`)
- Parameter files
- README with specific instructions

Example workflow:
```bash
cd mosfet_characterization/nmos
sdevice nmos_idvg.cmd
inspect -l nmos_idvg.log
```

## Documentation

Detailed documentation for each simulation type is available in the `docs/` directory:
- Process simulation guide
- Device simulation best practices
- Parameter extraction methodology
- Analysis and visualization techniques

## Results and Data

Simulation results include:
- Device structures (`.tdr` files)
- Current-voltage characteristics
- Electric field distributions
- Carrier concentration profiles
- Parameter extraction results
- Performance metrics

## Contributing

This repository represents work performed during ISWDP Cohort 6. For questions or contributions, please open an issue or contact the repository maintainer.

## References

- Synopsys Sentaurus TCAD Documentation
- ISWDP (Intel Semiconductor Workforce Development Program) resources
- Relevant semiconductor device physics textbooks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Nikhil KM - ISWDP Cohort 6

## Acknowledgments

- Intel Semiconductor Workforce Development Program (ISWDP)
- Synopsys for TCAD tools
- ISWDP Cohort 6 instructors and peers