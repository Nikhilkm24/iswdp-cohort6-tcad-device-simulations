# Example TCAD Simulations

This directory contains example simulation files to help you get started with TCAD simulations.

## Overview

The examples provided here are simplified but functional simulation templates that demonstrate:
- Basic simulation setup
- Common physics models
- Typical analysis flows
- Result extraction

## Available Examples

### 1. Simple NMOS I-V Simulation
- `nmos_simple_idvg.cmd` - Basic transfer characteristics
- Demonstrates: Device setup, voltage sweep, basic physics

### 2. Process Flow Example
- `simple_process_flow.cmd` - Basic CMOS process
- Demonstrates: Implantation, diffusion, oxidation

### 3. Parameter Extraction Template
- `parameter_extraction_template.py` - Python script
- Demonstrates: Data loading, plotting, parameter extraction

### 4. Thermal Analysis Example
- `thermal_analysis_simple.cmd` - Self-heating simulation
- Demonstrates: Coupled electro-thermal simulation

## Using the Examples

### Method 1: Copy and Modify

```bash
# Copy example to your working directory
cp examples/nmos_simple_idvg.cmd mosfet_characterization/nmos/

# Modify parameters as needed
# Run simulation
cd mosfet_characterization/nmos/
sdevice nmos_simple_idvg.cmd
```

### Method 2: Run in Place

```bash
# Run directly from examples directory
cd examples
sdevice nmos_simple_idvg.cmd
```

## Example Structure

Each example includes:
- Commented code explaining each section
- Typical parameter values
- Expected outputs
- Suggestions for modifications

## Learning Strategy

1. **Start with simple examples**
   - Understand basic structure
   - Learn command syntax
   - See results

2. **Modify parameters**
   - Change dimensions
   - Vary doping
   - Try different bias

3. **Combine concepts**
   - Add complexity gradually
   - Integrate multiple examples
   - Build custom simulations

## Important Notes

- Examples use simplified physics for fast execution
- Production simulations may need more advanced models
- Always validate results against known data
- Adapt examples to your specific needs

## Contributing

If you develop useful example simulations, consider contributing them back to this repository!

## Further Reading

- See `docs/SIMULATION_GUIDE.md` for detailed information
- Check individual simulation directories for specific examples
- Review Synopsys documentation for advanced features
