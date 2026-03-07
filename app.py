"""
CICAD 2025 - Reflector Antenna Problem-2
Center-Fed Reflector with 2x2 Patch Array Feed

Given:
  - Center-fed reflector, D = 2.5 m, f/D = 0.9
  - Operating frequency = 12 GHz
  - Feed: 2x2 element patch antenna array, spacing = 0.5 lambda
  - Patch antenna efficiency = 90%

Parts (a)-(f) solved with full calculations and plots.

References:
  [1] S. K. Rao, C. Ostroot, "Design Principles and Guidelines for Phased Array
      and Reflector Antennas," IEEE AP Magazine, April 2020.
  [2] S. Kotta, G. Gupta, "Reflector Antennas Design and Analysis Software,"
      IEEE WAMS 2024.
  [3] S. Kotta, G. Gupta, "Phased Array Antenna Design and Analysis Tool,"
      IEEE WAMS 2023.
"""

import os
os.system("pip install matplotlib")
os.system("pip install scipy")

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc
import math

# ============================================================
# CONSTANTS & GIVEN PARAMETERS
# ============================================================

# Radiating element constants (C values for theta_b = C * lambda/d)
# For reflector feed analysis using Gaussian beam model
radiating_element_dict = {
    "Potter-type horn": 35,
    "Dominant TE11-mode Circular Horn": 31,
    "Dominant-mode Square Horn": 27.5,
    "High-efficiency Square Horn": 26,
    "High-efficiency Multimode Horn": 31.5,
    "Corrugated Horn": 37.5,
    "Cup-dipole Element": 29,
    "Patch": 58,
    "Dipole": 58
}

# ============================================================
# CORE COMPUTATION FUNCTIONS
# ============================================================

def compute_all(D_m, f_D, freq_GHz, num_elements_total, num_elements_x,
                spacing_lambda, patch_efficiency_pct, element_type="Patch"):
    """
    Master computation function for center-fed reflector with array feed.
    Returns a dictionary with all computed parameters.
    """
    results = {}

    # --- Basic parameters ---
    c = 0.299792458  # speed of light in m/GHz
    wavelength = c / freq_GHz  # meters
    F_m = f_D * D_m  # focal length in meters
    D_lambda = D_m / wavelength  # reflector diameter in wavelengths
    F_lambda = F_m / wavelength  # focal length in wavelengths

    results["wavelength_m"] = wavelength
    results["wavelength_mm"] = wavelength * 1000
    results["F_m"] = F_m
    results["D_lambda"] = D_lambda
    results["F_lambda"] = F_lambda
    results["D_m"] = D_m
    results["f_D"] = f_D
    results["freq_GHz"] = freq_GHz

    # --- Center-fed reflector geometry ---
    # For center-fed: h = 0, theta_0 = 2 * arctan(D / (4F))
    h = 0  # no offset for center-fed
    theta_0_rad = 2 * np.arctan(D_lambda / (4 * F_lambda))
    theta_0_deg = np.degrees(theta_0_rad)
    theta_star_deg = 0  # center-fed: feed points at vertex

    results["h_m"] = 0
    results["h_lambda"] = 0
    results["theta_0_deg"] = theta_0_deg
    results["theta_star_deg"] = theta_star_deg

    # Half-angle subtended at feed
    half_angle_deg = theta_0_deg / 2  # used for some formulas
    results["half_subtended_angle_deg"] = theta_0_deg

    # --- Part (b): Feed Array Directivity and 3dB Beamwidth ---
    N = num_elements_total
    eta_feed = patch_efficiency_pct / 100.0
    d_lambda = spacing_lambda  # element spacing in wavelengths

    # Array directivity: D_array = 10*log10[N * eta_e * 4*pi*(d/lambda)^2]
    D_array_linear = N * eta_feed * 4 * np.pi * d_lambda**2
    D_array_dBi = 10 * np.log10(D_array_linear)

    results["N_elements"] = N
    results["spacing_lambda"] = d_lambda
    results["spacing_mm"] = d_lambda * wavelength * 1000
    results["D_array_dBi"] = D_array_dBi

    # Array beamwidth: using sinc-based array
    # For a 2x2 array: Nx = 2 elements in x-direction
    Nx = num_elements_x
    L_sq = Nx * d_lambda  # total array size in wavelengths (each direction)

    # Radiating element constant for Patch
    A_const = radiating_element_dict.get(element_type, 58)

    # 3dB beamwidth of the feed array (approximate)
    # Using: theta_3dB ≈ A * (lambda / (Nx * d))
    # For a small array, the array factor beamwidth:
    theta_3dB_feed_deg = A_const * (1.0 / L_sq)

    results["L_sq_lambda"] = L_sq
    results["theta_3dB_feed_deg"] = theta_3dB_feed_deg

    # --- Illumination Taper at reflector edges ---
    # Using Gaussian beam model: T = 3 * (theta_0 / theta_3dB_feed)^2
    T_dB = 3 * (theta_0_deg / theta_3dB_feed_deg)**2

    results["T_dB"] = T_dB

    # --- Part (c): Reflector Peak Directivity and 3dB Beamwidth ---
    # Efficiency: eta_f = 4*cot^2(theta_0/2)*[1 - cos^n(theta_0/2)]^2 * (n+1)/n^2
    # n = -0.05*T / log10[cos(theta_0/2)]
    theta_0_half_rad = np.radians(theta_0_deg / 2)
    cos_half = np.cos(theta_0_half_rad)

    if cos_half > 0 and cos_half < 1:
        log_cos_half = np.log10(cos_half)
        if log_cos_half != 0:
            n = -0.05 * T_dB / log_cos_half
        else:
            n = 1.0
    else:
        n = 1.0

    results["n_value"] = n

    cot_half = 1.0 / np.tan(theta_0_half_rad)
    eta_f = 4 * cot_half**2 * (1 - cos_half**n)**2 * (n + 1) / n**2

    results["eta_f"] = eta_f
    results["eta_f_pct"] = eta_f * 100

    # Peak directivity: D_peak = 10*log10[(pi*D/lambda)^2 * eta_f]
    D_peak_dBi = 10 * np.log10((np.pi * D_lambda)**2 * eta_f)
    results["D_peak_dBi"] = D_peak_dBi

    # 3dB beamwidth of reflector secondary beam
    # theta_3 = (0.762*T + 58.44) * lambda/D
    theta_3_sec_deg = (0.762 * T_dB + 58.44) * (1.0 / D_lambda)
    results["theta_3_sec_deg"] = theta_3_sec_deg

    # --- Part (d): Aperture Efficiency ---
    results["aperture_efficiency_pct"] = eta_f * 100

    # --- Part (e): Side Lobe Level ---
    # SLL = -0.037*T^2 - 0.376*T - 17.6
    SLL_dB = -0.037 * T_dB**2 - 0.376 * T_dB - 17.6
    results["SLL_dB"] = SLL_dB

    # --- Scan factor (for reference) ---
    x_val = 0.3 if T_dB < 6 else 0.36
    sf_temp = (D_m / (4 * F_m))**2
    sf_temp1 = (1 + x_val * sf_temp) / (1 + sf_temp)
    # For center-fed, theta_star = 0, so cos(theta_star) = 1
    scan_factor = sf_temp1 * np.degrees(np.arctan((1 + 1) / (2 * F_m)))
    results["scan_factor"] = scan_factor

    # --- Part (f): Comparison with 0.7 lambda spacing ---
    d_lambda_new = 0.7
    L_sq_new = Nx * d_lambda_new
    D_array_new_linear = N * eta_feed * 4 * np.pi * d_lambda_new**2
    D_array_new_dBi = 10 * np.log10(D_array_new_linear)
    theta_3dB_feed_new = A_const * (1.0 / L_sq_new)
    T_new_dB = 3 * (theta_0_deg / theta_3dB_feed_new)**2

    if cos_half > 0 and cos_half < 1 and log_cos_half != 0:
        n_new = -0.05 * T_new_dB / log_cos_half
    else:
        n_new = 1.0

    eta_f_new = 4 * cot_half**2 * (1 - cos_half**n_new)**2 * (n_new + 1) / n_new**2
    D_peak_new_dBi = 10 * np.log10((np.pi * D_lambda)**2 * eta_f_new)
    theta_3_sec_new = (0.762 * T_new_dB + 58.44) * (1.0 / D_lambda)
    SLL_new_dB = -0.037 * T_new_dB**2 - 0.376 * T_new_dB - 17.6

    results["d_lambda_new"] = d_lambda_new
    results["D_array_new_dBi"] = D_array_new_dBi
    results["theta_3dB_feed_new"] = theta_3dB_feed_new
    results["T_new_dB"] = T_new_dB
    results["n_new"] = n_new
    results["eta_f_new"] = eta_f_new
    results["eta_f_new_pct"] = eta_f_new * 100
    results["D_peak_new_dBi"] = D_peak_new_dBi
    results["theta_3_sec_new"] = theta_3_sec_new
    results["SLL_new_dB"] = SLL_new_dB

    return results


# ============================================================
# PLOTTING FUNCTIONS
# ============================================================

def plot_reflector_sketch(D_m, F_m, feed_size_m):
    """Part (a): Draw a rough sketch of the center-fed reflector and feed."""
    fig, ax = plt.subplots(1, 1, figsize=(9, 7))
    ax.set_aspect('equal')

    # Parabola: y^2 = 4*F*x  =>  x = y^2/(4F)
    y_vals = np.linspace(-D_m/2, D_m/2, 500)
    x_vals = y_vals**2 / (4 * F_m)

    # Shift so vertex is at origin
    ax.plot(x_vals, y_vals, 'b-', linewidth=2.5, label='Reflector')

    # Focal point
    ax.plot(F_m, 0, 'r*', markersize=15, label=f'Focal Point (F={F_m:.2f}m)')

    # Feed array representation
    feed_half = feed_size_m / 2
    feed_rect = plt.Rectangle((F_m - 0.02, -feed_half), 0.04, feed_size_m,
                               fill=True, color='orange', alpha=0.8, label='2×2 Patch Array Feed')
    ax.add_patch(feed_rect)

    # Axis of symmetry
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)

    # Dimension lines
    # Diameter
    ax.annotate('', xy=(x_vals[-1], D_m/2), xytext=(x_vals[-1], -D_m/2),
                arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
    ax.text(x_vals[-1] + 0.08, 0, f'D = {D_m} m', fontsize=10, color='green',
            ha='left', va='center')

    # Focal length
    ax.annotate('', xy=(0, -D_m/2 - 0.15), xytext=(F_m, -D_m/2 - 0.15),
                arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
    ax.text(F_m/2, -D_m/2 - 0.3, f'F = {F_m:.2f} m (f/D = {F_m/D_m:.1f})',
            fontsize=10, color='red', ha='center')

    # Feed rays to reflector edges
    ax.plot([F_m, x_vals[0]], [0, y_vals[0]], 'k--', linewidth=0.8, alpha=0.5)
    ax.plot([F_m, x_vals[-1]], [0, y_vals[-1]], 'k--', linewidth=0.8, alpha=0.5)

    # Theta_0 angle annotation
    theta_0_deg = 2 * np.degrees(np.arctan(D_m / (4 * F_m)))
    angle_arc = Arc((F_m, 0), 0.6, 0.6, angle=180,
                    theta1=-theta_0_deg/2, theta2=theta_0_deg/2,
                    color='purple', linewidth=1.5)
    ax.add_patch(angle_arc)
    ax.text(F_m - 0.45, 0.15, f'θ₀={theta_0_deg:.1f}°', fontsize=9, color='purple')

    ax.set_xlabel('Axial Distance (m)', fontsize=11)
    ax.set_ylabel('Aperture Distance (m)', fontsize=11)
    ax.set_title('Center-Fed Reflector with 2×2 Patch Array Feed\n(Reflector Antenna Problem-2)',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.15, F_m + 0.4)
    ax.set_ylim(-D_m/2 - 0.5, D_m/2 + 0.3)

    plt.tight_layout()
    return fig


def plot_feed_radiation_pattern(results):
    """Plot the 2x2 array feed radiation pattern."""
    D_array = results["D_array_dBi"]
    L_sq = results["L_sq_lambda"]
    d_lambda = results["spacing_lambda"]
    Nx = 2

    theta_deg = np.linspace(-90, 90, 5001)
    theta_rad = np.radians(theta_deg)

    # Sinc-based pattern for rectangular aperture
    u = L_sq * np.pi * np.sin(theta_rad)
    with np.errstate(divide='ignore', invalid='ignore'):
        pattern = np.where(np.abs(u) < 1e-12, 1.0, (np.sin(u) / u)**2)

    pattern_dB = D_array + 10 * np.log10(np.maximum(pattern, 1e-15))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(theta_deg, pattern_dB, 'b-', linewidth=1.5)
    ax.set_xlabel('θ (degrees)', fontsize=11)
    ax.set_ylabel('Directivity (dBi)', fontsize=11)
    ax.set_title(f'2×2 Patch Array Feed Radiation Pattern\n'
                 f'(d = {d_lambda}λ, Peak = {D_array:.2f} dBi)', fontsize=12, fontweight='bold')
    ax.set_xlim(-90, 90)
    ax.set_ylim(D_array - 40, D_array + 3)
    ax.axhline(D_array - 3, color='red', linestyle='--', alpha=0.5, label='−3 dB level')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_secondary_beam(results, label_suffix=""):
    """Part (e): Plot the reflector secondary beam pattern."""
    T = results.get("T_dB" if not label_suffix else "T_new_dB", results["T_dB"])
    D_peak = results.get("D_peak_dBi" if not label_suffix else "D_peak_new_dBi", results["D_peak_dBi"])
    D_lambda = results["D_lambda"]
    theta_3 = results.get("theta_3_sec_deg" if not label_suffix else "theta_3_sec_new", results["theta_3_sec_deg"])
    SLL = results.get("SLL_dB" if not label_suffix else "SLL_new_dB", results["SLL_dB"])

    # Compute secondary pattern using piecewise Gaussian beam model
    half_power_bw = (0.058 * T**2 + 0.171 * T + 58.44) / D_lambda
    sidelobe_level = -0.037 * T**2 - 0.376 * T - 17.6

    # theta_SLL: angle where main beam meets sidelobe plateau
    if sidelobe_level < 0:
        theta_SLL = 0.5 * half_power_bw * np.sqrt(abs(sidelobe_level) / 3)
    else:
        theta_SLL = half_power_bw

    x_vals = np.linspace(0, max(5 * theta_SLL, 10), 5000)
    y_vals = np.full_like(x_vals, sidelobe_level)

    # Region 1: main beam (Gaussian)
    region1 = (x_vals >= 0) & (x_vals <= theta_SLL)
    with np.errstate(divide='ignore', invalid='ignore'):
        y_vals[region1] = -3 * (2 * x_vals[region1] / half_power_bw)**2

    # Region 3: sidelobe roll-off
    region3 = x_vals > 1.5 * theta_SLL
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = x_vals[region3] / (1.5 * theta_SLL)
        y_vals[region3] = sidelobe_level - 25 * np.log10(np.maximum(ratio, 1e-10))

    # Full pattern (mirror for negative angles)
    x_full = np.concatenate((-x_vals[::-1][:-1], x_vals))
    y_full = np.concatenate((y_vals[::-1][:-1], y_vals))

    # Scale to absolute directivity
    y_absolute = D_peak + y_full

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Normalized pattern
    ax1.plot(x_full, y_full, 'b-', linewidth=1.5)
    ax1.axhline(sidelobe_level, color='red', linestyle=':', alpha=0.5,
                label=f'SLL = {sidelobe_level:.1f} dB')
    ax1.axhline(-3, color='green', linestyle='--', alpha=0.5, label='−3 dB level')
    ax1.set_xlabel('θ (degrees)', fontsize=11)
    ax1.set_ylabel('Normalized Gain (dB)', fontsize=11)
    title_suffix = f" (d={results.get('d_lambda_new', 0.7)}λ)" if label_suffix else " (d=0.5λ)"
    ax1.set_title(f'Normalized Secondary Beam{title_suffix}', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-5 * theta_SLL, 5 * theta_SLL)
    ax1.set_ylim(min(-50, sidelobe_level - 15), 3)

    # Absolute directivity pattern
    ax2.plot(x_full, y_absolute, 'b-', linewidth=1.5)
    ax2.axhline(D_peak - 3, color='green', linestyle='--', alpha=0.5,
                label=f'−3 dB = {D_peak - 3:.1f} dBi')
    ax2.axhline(D_peak + sidelobe_level, color='red', linestyle=':', alpha=0.5,
                label=f'1st SLL = {D_peak + sidelobe_level:.1f} dBi')
    # Annotate peak
    ax2.annotate(f'Peak = {D_peak:.1f} dBi', xy=(0, D_peak),
                 xytext=(1.5, D_peak - 2), fontsize=9,
                 arrowprops=dict(arrowstyle='->', color='black'))
    # Annotate 3dB BW
    ax2.annotate(f'3dB BW = {theta_3:.2f}°', xy=(theta_3/2, D_peak - 3),
                 xytext=(2, D_peak - 6), fontsize=9,
                 arrowprops=dict(arrowstyle='->', color='green'))

    ax2.set_xlabel('θ (degrees)', fontsize=11)
    ax2.set_ylabel('Directivity (dBi)', fontsize=11)
    ax2.set_title(f'Reflector Secondary Beam{title_suffix}', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(-5 * theta_SLL, 5 * theta_SLL)

    plt.tight_layout()
    return fig


def plot_efficiency_vs_taper(theta_0_deg):
    """Plot antenna efficiency as a function of illumination taper."""
    T_range = np.linspace(1, 30, 200)
    theta_0_half_rad = np.radians(theta_0_deg / 2)
    cos_half = np.cos(theta_0_half_rad)
    log_cos_half = np.log10(cos_half) if cos_half > 0 and cos_half < 1 else -0.01

    thetas = [theta_0_deg - 10, theta_0_deg, theta_0_deg + 10]
    labels = [f'θ₀ = {t:.0f}°' for t in thetas]

    fig, ax = plt.subplots(figsize=(8, 5))

    for theta, label in zip(thetas, labels):
        th_half_rad = np.radians(theta / 2)
        cos_h = np.cos(th_half_rad)
        log_c = np.log10(cos_h) if 0 < cos_h < 1 else -0.01
        cot_h = 1.0 / np.tan(th_half_rad) if np.tan(th_half_rad) != 0 else 1.0

        n_arr = -0.05 * T_range / log_c
        eta_arr = 4 * cot_h**2 * (1 - cos_h**n_arr)**2 * (n_arr + 1) / n_arr**2
        ax.plot(T_range, eta_arr, linewidth=1.5, label=label)

    ax.set_xlabel('Illumination Taper (dB)', fontsize=11)
    ax.set_ylabel('Antenna Efficiency', fontsize=11)
    ax.set_title('Reflector Antenna Efficiency vs Illumination Taper', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_directivity_vs_diameter(D_lambda, F_lambda, T_dB):
    """Plot directivity and beamwidth as a function of reflector diameter."""
    D_range = np.linspace(0.3 * D_lambda, 1.5 * D_lambda, 200)
    F_range = D_range * (F_lambda / D_lambda)  # keep f/D constant

    theta_0_range = 2 * np.degrees(np.arctan(D_range / (4 * F_range)))
    theta_0_half_rad = np.radians(theta_0_range / 2)
    cos_half = np.cos(theta_0_half_rad)
    log_cos_half = np.log10(cos_half)

    n_arr = np.where(log_cos_half != 0, -0.05 * T_dB / log_cos_half, 1.0)
    cot_half = 1.0 / np.tan(theta_0_half_rad)
    eta_arr = 4 * cot_half**2 * (1 - cos_half**n_arr)**2 * (n_arr + 1) / n_arr**2

    dir_arr = 10 * np.log10((np.pi * D_range)**2 * eta_arr)
    bw_arr = (0.762 * T_dB + 58.44) / D_range

    fig, ax1 = plt.subplots(figsize=(8, 5))

    color1 = 'tab:blue'
    color2 = 'tab:orange'

    ax1.plot(D_range, dir_arr, color=color1, linewidth=1.5, label='Directivity')
    ax1.set_xlabel('Reflector Diameter (D/λ)', fontsize=11)
    ax1.set_ylabel('Directivity (dBi)', color=color1, fontsize=11)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    ax2.plot(D_range, bw_arr, color=color2, linewidth=1.5, label='3-dB Beamwidth')
    ax2.set_ylabel('3-dB Beamwidth (°)', color=color2, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=color2)

    ax1.set_title('Directivity and Beamwidth vs Reflector Diameter', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right', fontsize=9)

    plt.tight_layout()
    return fig


def plot_comparison_table(results):
    """Part (f): Comparison table between 0.5λ and 0.7λ spacing."""
    data = {
        "Parameter": [
            "Element Spacing (λ)",
            "Feed Array Directivity (dBi)",
            "Feed 3dB Beamwidth (°)",
            "Illumination Taper T (dB)",
            "Reflector Efficiency (%)",
            "Peak Directivity (dBi)",
            "Secondary 3dB Beamwidth (°)",
            "First Sidelobe Level (dB)"
        ],
        "d = 0.5λ": [
            f"{results['spacing_lambda']:.2f}",
            f"{results['D_array_dBi']:.2f}",
            f"{results['theta_3dB_feed_deg']:.2f}",
            f"{results['T_dB']:.2f}",
            f"{results['eta_f_pct']:.2f}",
            f"{results['D_peak_dBi']:.2f}",
            f"{results['theta_3_sec_deg']:.2f}",
            f"{results['SLL_dB']:.2f}"
        ],
        "d = 0.7λ": [
            f"{results['d_lambda_new']:.2f}",
            f"{results['D_array_new_dBi']:.2f}",
            f"{results['theta_3dB_feed_new']:.2f}",
            f"{results['T_new_dB']:.2f}",
            f"{results['eta_f_new_pct']:.2f}",
            f"{results['D_peak_new_dBi']:.2f}",
            f"{results['theta_3_sec_new']:.2f}",
            f"{results['SLL_new_dB']:.2f}"
        ],
        "Change": [
            "↑ Increased",
            "↑ Increased",
            "↓ Narrower",
            "↑ Increased",
            "See analysis",
            "See analysis",
            "↑ Broader",
            "↓ Lower (better)"
        ]
    }
    return pd.DataFrame(data)


# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(page_title="CICAD 2025 - Reflector Antenna Problem-2", layout="wide")

st.title("📡 CICAD 2025 — Reflector Antenna Problem-2")
st.markdown("""
**Center-Fed Reflector with 2×2 Patch Array Feed**

*Given:* D = 2.5 m, f/D = 0.9, f = 12 GHz, 2×2 patch array feed (d = 0.5λ), η_patch = 90%
""")

# Sidebar for optional parameter overrides
with st.sidebar:
    st.header("📐 Input Parameters")
    st.markdown("*(Pre-filled with problem values)*")
    D_m = st.number_input("Reflector Diameter D (m)", value=2.5, min_value=0.1)
    f_D = st.number_input("f/D ratio", value=0.9, min_value=0.1)
    freq = st.number_input("Frequency (GHz)", value=12.0, min_value=0.1)
    N_total = st.number_input("Total Array Elements", value=4, min_value=1)
    N_x = st.number_input("Elements per side (Nx)", value=2, min_value=1)
    d_lam = st.number_input("Element Spacing (λ)", value=0.5, min_value=0.1)
    eta_patch = st.number_input("Patch Efficiency (%)", value=90.0, min_value=1.0, max_value=100.0)
    element_type = st.selectbox("Feed Element Type", list(radiating_element_dict.keys()), index=7)

if st.button("🚀 Run Full Analysis", type="primary"):

    results = compute_all(D_m, f_D, freq, N_total, N_x, d_lam, eta_patch, element_type)

    # ========== PART (a) ==========
    st.header("Part (a): Reflector and Feed Configuration Sketch")

    feed_size = 2 * d_lam * results["wavelength_m"]
    fig_sketch = plot_reflector_sketch(D_m, results["F_m"], feed_size)
    st.pyplot(fig_sketch)

    st.markdown(f"""
    **Key Dimensions:**
    - Reflector Diameter: D = {D_m} m = {results['D_lambda']:.2f} λ
    - Focal Length: F = {results['F_m']:.2f} m = {results['F_lambda']:.2f} λ
    - f/D ratio: {f_D}
    - Half-angle subtended at feed: θ₀ = {results['theta_0_deg']:.2f}°
    - Configuration: Center-fed (no offset, h = 0)
    - Feed: 2×2 patch array at focal point, element spacing = {d_lam}λ = {results['spacing_mm']:.2f} mm
    """)

    # ========== PART (b) ==========
    st.header("Part (b): Feed Array Directivity, 3dB Beamwidth & Illumination Taper")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **Feed Array Parameters (2×2 Patch Array, d = {d_lam}λ):**
        - Number of elements: N = {results['N_elements']}
        - Element spacing: d = {d_lam}λ = {results['spacing_mm']:.2f} mm
        - Array size (per side): L = Nx × d = {N_x} × {d_lam}λ = {results['L_sq_lambda']:.2f}λ
        - **Feed Array Directivity: D_array = {results['D_array_dBi']:.2f} dBi**
        - **Feed 3dB Beamwidth: θ₃dB = {results['theta_3dB_feed_deg']:.2f}°**
        """)
    with col2:
        st.markdown(f"""
        **Illumination Taper Calculation:**
        - θ₀ (half-angle at feed) = {results['theta_0_deg']:.2f}°
        - Feed beamwidth θ₃dB = {results['theta_3dB_feed_deg']:.2f}°
        - T = 3 × (θ₀/θ₃dB)² = 3 × ({results['theta_0_deg']:.2f}/{results['theta_3dB_feed_deg']:.2f})²
        - **Illumination Taper T = {results['T_dB']:.2f} dB**
        """)

    fig_feed = plot_feed_radiation_pattern(results)
    st.pyplot(fig_feed)

    # ========== PART (c) ==========
    st.header("Part (c): Reflector Peak Directivity and 3dB Beamwidth")

    st.markdown(f"""
    **Reflector Secondary Beam Calculations:**

    1. **cos^n model parameter:** n = −0.05T / log₁₀[cos(θ₀/2)] = {results['n_value']:.4f}

    2. **Aperture Efficiency:**
       η_f = 4·cot²(θ₀/2)·[1 − cos^n(θ₀/2)]²·(n+1)/n² = **{results['eta_f_pct']:.2f}%**

    3. **Peak Directivity:**
       D_peak = 10·log₁₀[(πD/λ)² · η_f] = 10·log₁₀[(π × {results['D_lambda']:.2f})² × {results['eta_f']:.4f}]
       **D_peak = {results['D_peak_dBi']:.2f} dBi**

    4. **3dB Beamwidth:**
       θ₃ = (0.762T + 58.44) × λ/D = (0.762 × {results['T_dB']:.2f} + 58.44) / {results['D_lambda']:.2f}
       **θ₃ = {results['theta_3_sec_deg']:.2f}°**
    """)

    col1, col2 = st.columns(2)
    with col1:
        fig_eff = plot_efficiency_vs_taper(results["theta_0_deg"])
        st.pyplot(fig_eff)
    with col2:
        fig_dir = plot_directivity_vs_diameter(results["D_lambda"], results["F_lambda"], results["T_dB"])
        st.pyplot(fig_dir)

    # ========== PART (d) ==========
    st.header("Part (d): Aperture Efficiency")

    st.markdown(f"""
    **Aperture Efficiency of the Reflector Antenna:**

    The aperture efficiency accounts for spillover, illumination, phase, and polarization efficiencies.
    Using the Gaussian beam model with T = {results['T_dB']:.2f} dB:

    **η_f = {results['aperture_efficiency_pct']:.2f}%**

    *Note:* The optimal illumination taper for maximum efficiency is typically 10–12 dB.
    With T = {results['T_dB']:.2f} dB, {'the taper is close to optimal.' if 8 < results['T_dB'] < 14 else 'the taper is not optimal, so efficiency can be improved by adjusting the feed.'}
    """)

    # ========== PART (e) ==========
    st.header("Part (e): Secondary Beam Pattern and Sidelobe Reduction")

    fig_sec = plot_secondary_beam(results)
    st.pyplot(fig_sec)

    st.markdown(f"""
    **Secondary Beam Performance:**
    - Peak Directivity: **{results['D_peak_dBi']:.2f} dBi**
    - 3dB Beamwidth: **{results['theta_3_sec_deg']:.2f}°**
    - First Sidelobe Level: **{results['SLL_dB']:.2f} dB** below peak

    ---
    **Two Suggested Changes to Reduce First Sidelobe Level:**

    1. **Increase illumination taper (increase feed array beamwidth):** By using a smaller feed array
       or reducing element spacing, the feed beam becomes wider, providing a higher edge taper on the
       reflector. This reduces sidelobe levels at the cost of slightly lower aperture efficiency and broader beamwidth.

    2. **Apply amplitude taper across the array feed elements:** Instead of uniform excitation of
       the 2×2 array, apply a tapered amplitude distribution (e.g., parabolic on pedestal) to the array elements.
       This controls the sidelobe envelope of both the feed pattern and the resulting reflector secondary pattern.
    """)

    # ========== PART (f) ==========
    st.header("Part (f): Comparison — Element Spacing 0.5λ vs 0.7λ")

    comp_df = plot_comparison_table(results)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    # Also plot secondary beam for 0.7 lambda
    fig_sec_new = plot_secondary_beam(results, label_suffix="_new")
    st.pyplot(fig_sec_new)

    st.markdown(f"""
    **Analysis of Changing Element Spacing from 0.5λ to 0.7λ:**

    When element spacing increases from 0.5λ to 0.7λ in the 2×2 feed array:

    | Effect | Explanation |
    |--------|-------------|
    | **Feed directivity increases** | Larger element area → higher element gain → D_array: {results['D_array_dBi']:.2f} → {results['D_array_new_dBi']:.2f} dBi |
    | **Feed beamwidth decreases** | Narrower feed beam: {results['theta_3dB_feed_deg']:.2f}° → {results['theta_3dB_feed_new']:.2f}° |
    | **Illumination taper increases** | More taper at reflector edges: {results['T_dB']:.2f} → {results['T_new_dB']:.2f} dB |
    | **Sidelobe level decreases** | Higher taper → lower SLL: {results['SLL_dB']:.2f} → {results['SLL_new_dB']:.2f} dB |
    | **Secondary beamwidth increases** | Broader secondary beam: {results['theta_3_sec_deg']:.2f}° → {results['theta_3_sec_new']:.2f}° |
    | **Aperture efficiency changes** | η: {results['eta_f_pct']:.2f}% → {results['eta_f_new_pct']:.2f}% |
    | **Peak directivity changes** | D_peak: {results['D_peak_dBi']:.2f} → {results['D_peak_new_dBi']:.2f} dBi |

    **Key Insight:** Increasing element spacing creates a narrower feed beam, which increases the
    illumination taper. This trades off aperture efficiency (and peak gain) for improved sidelobe performance.
    If taper goes significantly beyond 10–12 dB, both efficiency and directivity will drop.
    """)

    st.divider()
    st.markdown("""
    ---
    **References:**
    1. S. K. Rao, C. Ostroot, "Design Principles and Guidelines for Phased Array and Reflector Antennas," *IEEE AP Magazine*, April 2020.
    2. S. Kotta, G. Gupta, "Reflector Antennas Design and Analysis Software," *IEEE WAMS 2024*.
    3. S. Kotta, G. Gupta, "Phased Array Antenna Design and Analysis Tool," *IEEE WAMS 2023*.
    """)
