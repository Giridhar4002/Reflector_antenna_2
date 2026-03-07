---
title: Reflector Antenna Design CICAD 2025
emoji: 📡
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: 1.54.0
app_file: app.py
pinned: false
---

# 📡 Center-Fed Parabolic Reflector Antenna Design Tool
### CICAD 2025 Assignment — Full Analytical Solution

This Streamlit application provides a complete solution for the CICAD 2025 reflector antenna design assignment. It solves all parts **(a) through (f)** using Gaussian beam analysis and circular aperture theory.

## Default Assignment Configuration
- **Reflector Diameter:** 2.5 m
- **f/D Ratio:** 0.9  →  Focal Length f = 2.25 m
- **Frequency:** 12 GHz  →  λ = 25 mm
- **Feed:** 2×2 patch array, d = 0.5λ, efficiency = 90%

## Parts Solved

| Part | Description |
|------|-------------|
| **(a)** | Cross-section sketch of reflector + feed with all labelled dimensions (D, f, ψ₀, h, HPBW) |
| **(b)** | Feed array HPBW, directivity, and Gaussian illumination taper at reflector edge |
| **(c)** | Reflector secondary beam peak directivity and –3 dB beamwidth |
| **(d)** | Full aperture efficiency breakdown: η_spillover × η_illumination × η_element |
| **(e)** | Secondary beam pattern plot + two sidelobe reduction methods |
| **(f)** | Spacing 0.5λ → 0.7λ: conceptual and quantitative beam performance comparison |

## Key Formulas Used

**Half-subtended angle:**  
ψ₀ = 2·arctan(1 / (4·f/D))

**2-element array half-HPBW:**  
sin(θ_hp) = λ / (4·d)  →  θ_hp = arcsin(1 / (4·d/λ))

**Gaussian edge taper:**  
T_edge (dB) = −3·(ψ₀/θ_b)²

**Peak directivity:**  
D_peak = η_ap · (πD/λ)²

**Aperture efficiency:**  
η_ap = η_s (spillover) × η_i (illumination) × η_e (element)

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```