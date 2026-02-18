# Example: Simple NMOS Transfer Characteristics (Id-Vg)
# This is a simplified NMOS device simulation for educational purposes
# Demonstrates basic Sentaurus Device simulation setup

# =============================================================================
# DEVICE STRUCTURE
# =============================================================================
# This section would normally load a device structure from process simulation
# For this example, we assume a structure file exists
# In practice, you would use: File { Grid = "@tdr@" }

File {
    Grid     = "nmos_structure.tdr"      # Input device structure
    Plot     = "nmos_idvg_des.tdr"       # Output with solution
    Current  = "nmos_idvg_des.plt"       # I-V data
    Output   = "nmos_idvg_des.log"       # Simulation log
}

# =============================================================================
# ELECTRODE DEFINITIONS
# =============================================================================
# Define electrical contacts for the device

Electrode {
    { Name="gate"     Voltage=0.0 }       # Gate contact
    { Name="source"   Voltage=0.0 }       # Source contact (ground)
    { Name="drain"    Voltage=0.0 }       # Drain contact
    { Name="substrate" Voltage=0.0 }      # Substrate/bulk contact
}

# =============================================================================
# PHYSICS MODELS
# =============================================================================
# Enable physics models for simulation

Physics {
    # Basic models (always needed)
    Mobility(
        DopingDependence              # Mobility depends on doping
        HighFieldSaturation           # Velocity saturation
        Enormal                       # Normal field dependence
    )
    
    Recombination(
        SRH(DopingDependence)         # Shockley-Read-Hall recombination
        Auger                         # Auger recombination
    )
    
    EffectiveIntrinsicDensity(        # Bandgap narrowing
        BandGapNarrowing(OldSlotboom) 
    )
}

# =============================================================================
# PLOT VARIABLES
# =============================================================================
# Specify what to save in output files

Plot {
    # Fields and potentials
    eDensity hDensity                 # Carrier densities
    eQuasiFermi hQuasiFermi           # Quasi-Fermi levels
    ElectricField                     # Electric field
    Potential                         # Electrostatic potential
    
    # Doping
    Doping DonorConcentration AcceptorConcentration
    
    # Current densities
    eCurrent hCurrent                 # Electron and hole currents
    CurrentDensity                    # Total current density
    
    # Band structure
    BandGap BandGapNarrowing
    Affinity
    ConductionBand ValenceBand
    
    # Mobility and velocity
    eMobility hMobility
    eVelocity hVelocity
}

# =============================================================================
# MATHEMATICAL METHODS
# =============================================================================
# Configure numerical solver

Math {
    Extrapolate                       # Extrapolate from previous solution
    Derivatives                       # Use analytical derivatives
    Avalderivatives                   # Avalanche derivatives
    RelErrControl                     # Relative error control
    Digits=5                          # Accuracy
    Iterations=20                     # Maximum iterations per step
    Notdamped=100                     # No damping for first iterations
}

# =============================================================================
# SIMULATION SEQUENCE
# =============================================================================

Solve {
    # 1. INITIAL SOLUTION: Equilibrium (all voltages = 0)
    Coupled(Iterations=100) { Poisson }
    Coupled { Poisson Electron Hole }
    
    # 2. RAMP DRAIN VOLTAGE: Set Vd = 0.05V (linear region)
    Quasistationary(
        InitialStep=0.01 MaxStep=0.05 MinStep=1e-4
        Goal { Name="drain" Voltage=0.05 }
    ) { Coupled { Poisson Electron Hole } }
    
    # 3. SWEEP GATE VOLTAGE: Transfer characteristics (Id-Vg)
    # Sweep from -0.5V to 2.0V to capture subthreshold and on-state
    NewCurrentFile="idvg_linear_"
    Quasistationary(
        InitialStep=0.05 MaxStep=0.1 MinStep=1e-4
        Goal { Name="gate" Voltage=2.0 }
    ) { Coupled { Poisson Electron Hole }
        CurrentPlot( Time=(Range=(0 1) Intervals=100) )
    }
    
    # Reset gate voltage
    Quasistationary(
        InitialStep=0.05 MaxStep=0.1 MinStep=1e-4
        Goal { Name="gate" Voltage=0.0 }
    ) { Coupled { Poisson Electron Hole } }
    
    # 4. RAMP DRAIN VOLTAGE: Set Vd = 1.0V (saturation region)
    Quasistationary(
        InitialStep=0.05 MaxStep=0.1 MinStep=1e-4
        Goal { Name="drain" Voltage=1.0 }
    ) { Coupled { Poisson Electron Hole } }
    
    # 5. SWEEP GATE VOLTAGE: Transfer characteristics at high Vd
    NewCurrentFile="idvg_saturation_"
    Quasistationary(
        InitialStep=0.05 MaxStep=0.1 MinStep=1e-4
        Goal { Name="gate" Voltage=2.0 }
    ) { Coupled { Poisson Electron Hole }
        CurrentPlot( Time=(Range=(0 1) Intervals=100) )
    }
}

# =============================================================================
# NOTES FOR USERS
# =============================================================================
# 1. This file requires a device structure file "nmos_structure.tdr"
#    You can create this using Sentaurus Structure Editor or Process
#
# 2. Typical NMOS parameters:
#    - Gate length: 0.1 - 10 μm
#    - Gate oxide: 1 - 10 nm
#    - Channel doping: 1e15 - 1e17 cm^-3
#    - S/D doping: 1e19 - 1e20 cm^-3
#
# 3. Expected outputs:
#    - nmos_idvg_des.tdr: Device structure with solution
#    - nmos_idvg_des.plt: I-V characteristics data
#    - idvg_linear_des.plt: Linear region data
#    - idvg_saturation_des.plt: Saturation region data
#
# 4. To extract parameters:
#    - Load .plt files in Inspect or Python
#    - Plot Id vs Vg (linear and log scale)
#    - Extract Vth, SS, Ion, Ioff, gm
#
# 5. Modifications to try:
#    - Change Vd values (e.g., 0.1V, 0.5V, 1.5V)
#    - Extend Vg range (e.g., -1V to 3V)
#    - Add temperature sweep
#    - Enable quantum corrections
#
# =============================================================================
