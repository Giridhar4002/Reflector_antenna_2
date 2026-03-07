import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Center-Fed Reflector & Phased Array Feed", layout="wide")

st.title("Center-Fed Reflector Antenna Design & Analysis")
st.markdown("Based on CICAD 2025: Phased Array and Reflector Antenna Design Challenges (Problem-2)")

# --- Sidebar Inputs ---
st.sidebar.header("Design Parameters")
D = st.sidebar.number_input("Reflector Diameter (m)", value=2.5)
f_D = st.sidebar.number_input("f/D Ratio", value=0.9)
freq_GHz = st.sidebar.number_input("Operating Frequency (GHz)", value=12.0)
n_elements = st.sidebar.number_input("Array Elements (N x N)", value=2)
spacing_lambda = st.sidebar.number_input("Element Spacing (λ)", value=0.5)
efficiency_pct = st.sidebar.number_input("Patch Antenna Efficiency (%)", value=90.0)

# --- Computations ---
c = 3e8
freq_Hz = freq_GHz * 1e9
lam_m = c / freq_Hz
lam_cm = lam_m * 100
F = f_D * D
eff_patch = efficiency_pct / 100.0

# Reflector Geometry (a)
theta_0_rad = 2 * math.atan(D / (4 * F))
theta_0_deg = math.degrees(theta_0_rad)

# Phased Array Feed Calculations (b)
# For an N x N array, physical aperture side length L = N * spacing * lambda
L_array_m = n_elements * spacing_lambda * lam_m
area_phys = L_array_m**2
area_eff = eff_patch * area_phys
D_array_lin = (4 * math.pi / lam_m**2) * area_eff
D_array_dBi = 10 * math.log10(D_array_lin)
# Approximate array 3dB beamwidth (deg) = 51 * (lambda / L)
theta_3dB_array = 51 * (lam_m / L_array_m)

# Illumination taper at edges: T(dB) = 12 * (theta_0 / theta_3dB_array)^2
taper_dB = 12 * (theta_0_deg / theta_3dB_array)**2

# Secondary Beam Calculations (c & d)
# Using standard reflector approximations based on illumination taper
# For T ~ 4.4 dB, spillover is high. Estimated aperture efficiency ~ 55%
eta_ap = 0.55 
HPBW_ref = 70 * (lam_m / D) # typically 70 for slight taper, 65 for uniform
D_ref_lin = eta_ap * (math.pi * D / lam_m)**2
D_ref_dBi = 10 * math.log10(D_ref_lin)
SLL_dB = -19.0 # Approximate first side lobe level for this taper

# --- UI Outputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("b. Phased Array Feed Performance")
    st.write(f"**Operating Wavelength (λ):** {lam_cm:.2f} cm")
    st.write(f"**Array Physical Aperture Area:** {(area_phys/lam_m**2):.2f} $\\lambda^2$")
    st.write(f"**Phased Array Directivity:** {D_array_dBi:.2f} dBi")
    st.write(f"**Phased Array 3 dB Beamwidth:** {theta_3dB_array:.2f}°")
    st.write(f"**Subtended Half-Angle ($\\theta_0$):** {theta_0_deg:.2f}°")
    st.write(f"**Illumination Taper at Edges:** {taper_dB:.2f} dB")

    st.subheader("c & d. Reflector Secondary Beam & Efficiency")
    st.write(f"**Secondary 3 dB Beamwidth:** {HPBW_ref:.2f}°")
    st.write(f"**Estimated Aperture Efficiency:** {eta_ap * 100:.1f}%")
    st.write(f"**Peak Secondary Directivity:** {D_ref_dBi:.2f} dBi")

    st.subheader("e. SLL Reduction Suggestions")
    st.info("""
    **To reduce the first side lobe level (SLL), we can:**
    1. **Increase the Edge Taper:** Increase the array aperture size to achieve an optimal ~10 dB edge taper, which significantly lowers edge diffraction.
    2. **Amplitude Weighting:** Apply amplitude tapering (e.g., binomial or Chebyshev distribution) across the 2x2 patch elements instead of uniform feeding.
    """)

    st.subheader("f. Analysis: Changing spacing to 0.7λ")
    L_new = n_elements * 0.7 * lam_m
    theta_3dB_new = 51 * (lam_m / L_new)
    taper_new = 12 * (theta_0_deg / theta_3dB_new)**2
    st.write(f"**New Feed 3dB BW:** {theta_3dB_new:.1f}° | **New Edge Taper:** {taper_new:.1f} dB")
    st.success("""
    **Conceptual Beam Performance Markers:**
    * **Spillover Efficiency:** INCREASES (less energy spilling past the reflector due to tighter feed beam).
    * **Overall Aperture Efficiency:** INCREASES (taper of 8.7 dB is much closer to the optimum ~10 dB).
    * **Secondary Peak Directivity:** INCREASES (due to better aperture efficiency).
    * **First Side Lobe Level (SLL):** DECREASES/IMPROVES (smoother field distribution at the aperture edges).
    * **Secondary Beamwidth:** SLIGHTLY INCREASES (due to higher amplitude taper broadening the secondary beam).
    """)

with col2:
    st.subheader("a. Rough Sketch of Reflector & Feed")
    # Draw simple matplotlib sketch for center-fed geometry
    fig_geom, ax_geom = plt.subplots(figsize=(6, 6))
    
    # Parabola formulation y^2 = 4Fx -> x = y^2 / 4F
    y_vals = np.linspace(-D/2, D/2, 100)
    x_vals = y_vals**2 / (4 * F)
    
    ax_geom.plot(x_vals, y_vals, 'b-', linewidth=3, label=f'Reflector (D={D}m)')
    
    # Feed point at focal point (F, 0)
    ax_geom.plot(F, 0, 'ro', markersize=8, label='2x2 Patch Array Feed')
    
    # Draw subtended angles
    ax_geom.plot([F, x_vals[0]], [0, y_vals[0]], 'g--', alpha=0.6)
    ax_geom.plot([F, x_vals[-1]], [0, y_vals[-1]], 'g--', alpha=0.6, label=f'Subtended Angle 2$\\theta_0$ = {2*theta_0_deg:.1f}°')
    ax_geom.plot([0, F*1.2], [0, 0], 'k-.', alpha=0.3, label='Boresight Axis')
    
    ax_geom.set_title("Center-Fed Reflector Geometry")
    ax_geom.set_xlabel("x (m)")
    ax_geom.set_ylabel("y (m)")
    ax_geom.legend()
    ax_geom.grid(True)
    ax_geom.set_aspect('equal', adjustable='datalim')
    
    st.pyplot(fig_geom)

    st.subheader("e. Approximate Secondary Beam Pattern")
    # Draw Approximate Radiation Pattern
    fig_pat, ax_pat = plt.subplots(figsize=(6, 4))
    
    theta_pat = np.linspace(-3, 3, 500)
    # Sinc squared approximation for main lobe and side lobes
    u = math.pi * (D / lam_m) * np.sin(np.radians(theta_pat))
    # Avoid division by zero
    u[u==0] = 1e-9
    pattern_linear = (np.sin(u) / u)**2
    pattern_dB = 10 * np.log10(pattern_linear)
    
    # Normalize to peak directivity
    pattern_dB_shifted = pattern_dB + D_ref_dBi
    # Apply SLL floor for realistic visualization based on taper
    pattern_dB_shifted = np.maximum(pattern_dB_shifted, D_ref_dBi + SLL_dB - 10)
    
    ax_pat.plot(theta_pat, pattern_dB_shifted, 'indigo', linewidth=2)
    ax_pat.axhline(D_ref_dBi, color='r', linestyle='--', alpha=0.5, label=f'Peak: {D_ref_dBi:.1f} dBi')
    ax_pat.axhline(D_ref_dBi - 3, color='g', linestyle='--', alpha=0.5, label=f'3dB BW: {HPBW_ref:.2f}°')
    ax_pat.axhline(D_ref_dBi + SLL_dB, color='orange', linestyle='--', alpha=0.5, label=f'First SLL: ~{SLL_dB} dBc')
    
    ax_pat.set_ylim(D_ref_dBi - 40, D_ref_dBi + 5)
    ax_pat.set_title("Secondary Beam Pattern (Approximate)")
    ax_pat.set_xlabel("Angle (degrees)")
    ax_pat.set_ylabel("Directivity (dBi)")
    ax_pat.legend()
    ax_pat.grid(True)
    
    st.pyplot(fig_pat)