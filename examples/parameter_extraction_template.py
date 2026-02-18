"""
Example Python Script: MOSFET Parameter Extraction
Author: ISWDP Cohort 6
Purpose: Extract key MOSFET parameters from TCAD simulation data

This script demonstrates how to:
1. Load simulation data from TCAD output files
2. Plot I-V characteristics
3. Extract device parameters (Vth, SS, Ion, Ioff, gm)
4. Generate publication-quality plots
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate, optimize

# =============================================================================
# CONFIGURATION
# =============================================================================

# Input file (TCAD output in ASCII format)
INPUT_FILE = "nmos_idvg_des.plt"

# Device parameters (update based on your device)
W = 10e-6  # Width in meters
L = 1e-6   # Length in meters

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_tcad_data(filename):
    """
    Load TCAD simulation data from .plt file
    
    Returns:
        vg: Gate voltage array (V)
        id: Drain current array (A)
        vd: Drain voltage (constant)
    """
    try:
        # Load data (adjust column indices based on your file format)
        data = np.loadtxt(filename, skiprows=1)  # Skip header
        
        vg = data[:, 0]  # Gate voltage (column 0)
        id = data[:, 1]  # Drain current (column 1)
        
        print(f"Loaded {len(vg)} data points from {filename}")
        return vg, id
        
    except Exception as e:
        print(f"Error loading file: {e}")
        print("This is a template - update INPUT_FILE with actual data")
        # Return dummy data for demonstration
        vg = np.linspace(-0.5, 2.0, 100)
        id = 1e-12 * np.exp(vg/0.1) + 1e-3 * (vg - 0.5)**2 * (vg > 0.5)
        return vg, id

# =============================================================================
# PARAMETER EXTRACTION FUNCTIONS
# =============================================================================

def extract_threshold_voltage(vg, id, method='linear_extrapolation'):
    """
    Extract threshold voltage using linear extrapolation method
    
    Args:
        vg: Gate voltage array
        id: Drain current array
        method: Extraction method ('linear_extrapolation', 'constant_current')
    
    Returns:
        vth: Threshold voltage (V)
    """
    # Calculate transconductance
    gm = np.gradient(id, vg)
    
    if method == 'linear_extrapolation':
        # Find point of maximum transconductance
        max_gm_idx = np.argmax(gm)
        
        # Fit line in region around max gm
        fit_range = 5
        idx_start = max(0, max_gm_idx - fit_range)
        idx_end = min(len(vg), max_gm_idx + fit_range)
        
        # Linear fit: Id = gm * (Vg - Vth)
        p = np.polyfit(vg[idx_start:idx_end], id[idx_start:idx_end], 1)
        vth = -p[1] / p[0]  # x-intercept
        
        return vth
    
    elif method == 'constant_current':
        # Vth at Id = (W/L) * 1e-7 A
        id_threshold = (W/L) * 1e-7
        idx = np.argmin(np.abs(id - id_threshold))
        return vg[idx]

def extract_subthreshold_slope(vg, id):
    """
    Extract subthreshold slope (SS) in mV/decade
    
    Returns:
        ss: Subthreshold slope (mV/decade)
    """
    # Find subthreshold region (Id < 1e-6 * Ion)
    ion = np.max(id)
    subthreshold_mask = id < 1e-6 * ion
    
    if np.sum(subthreshold_mask) < 2:
        return np.nan
    
    vg_sub = vg[subthreshold_mask]
    log_id_sub = np.log10(np.abs(id[subthreshold_mask]) + 1e-20)
    
    # Fit line in subthreshold region
    p = np.polyfit(vg_sub, log_id_sub, 1)
    
    # SS = 1 / slope, converted to mV/decade
    ss = 1000.0 / p[0]  # mV/decade
    
    return ss

def extract_on_off_currents(vg, id, vdd=1.0):
    """
    Extract Ion (on current) and Ioff (off current)
    
    Args:
        vg: Gate voltage array
        id: Drain current array
        vdd: Supply voltage (V)
    
    Returns:
        ion: On current at Vg = Vdd (A)
        ioff: Off current at Vg = 0V (A)
    """
    # Ion: current at Vg = Vdd
    ion_idx = np.argmin(np.abs(vg - vdd))
    ion = id[ion_idx]
    
    # Ioff: current at Vg = 0V
    ioff_idx = np.argmin(np.abs(vg - 0.0))
    ioff = id[ioff_idx]
    
    return ion, ioff

def extract_max_transconductance(vg, id):
    """
    Extract maximum transconductance
    
    Returns:
        gm_max: Maximum transconductance (S)
    """
    gm = np.gradient(id, vg)
    gm_max = np.max(gm)
    return gm_max

# =============================================================================
# PLOTTING FUNCTIONS
# =============================================================================

def plot_transfer_characteristics(vg, id, vth=None, save_path=None):
    """
    Plot Id-Vg characteristics (linear and log scale)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Linear scale
    ax1.plot(vg, id * 1e6, 'b-', linewidth=2)
    ax1.set_xlabel('Gate Voltage (V)', fontsize=12)
    ax1.set_ylabel('Drain Current (μA)', fontsize=12)
    ax1.set_title('Transfer Characteristics (Linear)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    if vth is not None:
        ax1.axvline(vth, color='r', linestyle='--', label=f'Vth = {vth:.3f} V')
        ax1.legend()
    
    # Log scale
    ax2.semilogy(vg, np.abs(id), 'b-', linewidth=2)
    ax2.set_xlabel('Gate Voltage (V)', fontsize=12)
    ax2.set_ylabel('Drain Current (A)', fontsize=12)
    ax2.set_title('Transfer Characteristics (Log)', fontsize=14)
    ax2.grid(True, alpha=0.3, which='both')
    
    if vth is not None:
        ax2.axvline(vth, color='r', linestyle='--', label=f'Vth = {vth:.3f} V')
        ax2.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()

def plot_transconductance(vg, id, save_path=None):
    """
    Plot transconductance (gm) vs gate voltage
    """
    gm = np.gradient(id, vg)
    
    plt.figure(figsize=(8, 6))
    plt.plot(vg, gm * 1e6, 'b-', linewidth=2)
    plt.xlabel('Gate Voltage (V)', fontsize=12)
    plt.ylabel('Transconductance (μS)', fontsize=12)
    plt.title('Transconductance vs Gate Voltage', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Mark maximum
    gm_max_idx = np.argmax(gm)
    plt.plot(vg[gm_max_idx], gm[gm_max_idx] * 1e6, 'ro', markersize=10,
             label=f'gm_max = {gm[gm_max_idx]*1e6:.2f} μS at Vg = {vg[gm_max_idx]:.2f} V')
    plt.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    plt.show()

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    """
    Main analysis function
    """
    print("=" * 70)
    print("MOSFET Parameter Extraction")
    print("=" * 70)
    
    # Load data
    print("\n1. Loading simulation data...")
    vg, id = load_tcad_data(INPUT_FILE)
    
    # Extract parameters
    print("\n2. Extracting device parameters...")
    
    vth = extract_threshold_voltage(vg, id)
    print(f"   Threshold Voltage (Vth):     {vth:.3f} V")
    
    ss = extract_subthreshold_slope(vg, id)
    print(f"   Subthreshold Slope (SS):     {ss:.1f} mV/decade")
    
    ion, ioff = extract_on_off_currents(vg, id, vdd=1.0)
    print(f"   On Current (Ion):            {ion*1e6:.2f} μA")
    print(f"   Off Current (Ioff):          {ioff*1e12:.2f} pA")
    print(f"   On/Off Ratio:                {ion/ioff:.2e}")
    
    gm_max = extract_max_transconductance(vg, id)
    print(f"   Max Transconductance (gm):   {gm_max*1e6:.2f} μS")
    
    # Generate plots
    print("\n3. Generating plots...")
    plot_transfer_characteristics(vg, id, vth, save_path='transfer_characteristics.png')
    plot_transconductance(vg, id, save_path='transconductance.png')
    
    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
