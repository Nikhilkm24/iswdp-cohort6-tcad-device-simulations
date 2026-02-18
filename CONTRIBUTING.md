# Contributing to ISWDP TCAD Simulations

Thank you for your interest in contributing to the ISWDP Cohort 6 TCAD Device Simulations repository!

## How to Contribute

### Adding Simulation Files

1. **Choose the appropriate directory** based on simulation type:
   - `process_modeling/` for process simulations
   - `mosfet_characterization/` for device characterization
   - `rf_analysis/` for RF simulations
   - `thermal_analysis/` for thermal simulations
   - `parameter_extraction/` for extraction scripts
   - `model_calibration/` for calibration work

2. **Follow naming conventions**:
   - Use descriptive names: `nmos_idvg_100nm.cmd`
   - Include relevant parameters in filename
   - Add README.md if creating a new subdirectory

3. **Document your simulations**:
   - Add comments in command files
   - Describe the purpose and expected results
   - Include parameter values and units
   - Note any special requirements

### Code Style Guidelines

#### Command Files (.cmd)
- Use clear section headers with comments
- Group related commands together
- Include units in comments
- Document physics models enabled

#### Python Scripts (.py)
- Follow PEP 8 style guidelines
- Include docstrings for functions
- Add type hints where appropriate
- Use meaningful variable names

#### Documentation (.md)
- Use clear headings and structure
- Include examples where helpful
- Keep language clear and concise
- Add references where appropriate

### Git Workflow

1. **Create a descriptive branch name**:
   ```bash
   git checkout -b feature/add-finfet-simulations
   ```

2. **Make focused commits**:
   ```bash
   git add specific_files
   git commit -m "Add FinFET process simulation"
   ```

3. **Keep commits atomic**: One logical change per commit

4. **Write clear commit messages**:
   - First line: Brief summary (50 chars or less)
   - Blank line
   - Detailed description if needed

### Submitting Changes

1. Ensure your simulations run successfully
2. Update relevant documentation
3. Add examples if introducing new concepts
4. Test on a clean environment if possible
5. Submit a pull request with clear description

## What to Contribute

### High Priority
- Complete simulation workflows
- Validated parameter extraction scripts
- Calibrated models
- Tutorial examples
- Bug fixes

### Medium Priority
- Additional visualization scripts
- Optimization examples
- Statistical analysis tools
- Documentation improvements

### Future Enhancements
- Automation scripts
- GUI tools
- Advanced analysis techniques
- Integration with other tools

## Quality Standards

### For Simulation Files
- Should run without errors
- Include expected output description
- Have reasonable default parameters
- Be well-documented

### For Scripts
- Should handle errors gracefully
- Include usage examples
- Have clear dependencies listed
- Follow coding best practices

### For Documentation
- Be accurate and up-to-date
- Include relevant references
- Use correct technical terminology
- Be accessible to target audience

## Questions or Issues?

- Open an issue on GitHub for bugs or questions
- Check existing documentation first
- Provide detailed information when reporting issues
- Include error messages and log files

## Code of Conduct

- Be respectful and professional
- Provide constructive feedback
- Help others learn and grow
- Share knowledge generously
- Acknowledge others' contributions

## License

All contributions are subject to the MIT License as specified in the LICENSE file.

## Recognition

Contributors will be acknowledged in:
- Commit history
- README.md contributors section
- Project documentation

Thank you for helping make this resource better for the ISWDP community!
