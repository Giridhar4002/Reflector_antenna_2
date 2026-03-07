---
title: CICAD 2025 Reflector Antenna Problem-2 - Design and Analysis Tool
emoji: 📡
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.43.2
app_file: app.py
pinned: false
---

# 📡 CICAD 2025 — Reflector Antenna Problem-2: Design and Analysis Tool

## Overview

This Streamlit application provides a **complete analytical solution** to **Reflector Antenna Problem-2** from the CICAD 2025 Assignment (Jan 31, 2026, submission due Feb 28, 2026). The tool solves all six parts (a–f) of the problem using Gaussian beam analysis and the design equations from the reference literature.

### Problem Statement

> **Given:** A center-fed reflector with 2.5 m diameter and f/D ratio of 0.9. Operating frequency = 12 GHz. The reflector is fed using a 2×2 element patch antenna array with element spacing of 0.5λ. Assume patch antenna efficiency of 90%.

---

## Problem Parts Solved

### Part (a) — Reflector & Feed Configuration Sketch
- Generates a dimensioned sketch of the center-fed parabolic reflector
- Labels all key parameters: D, F, f/D, θ₀ (half-angle subtended at feed)
- Shows the 2×2 patch array feed positioned at the focal point

### Part (b) — Feed Array Directivity, 3dB Beamwidth & Illumination Taper
- Computes feed array directivity using: `D_array = 10·log₁₀[N · η_e · 4π(d/λ)²]`
- Calculates feed 3dB beamwidth: `θ₃dB = A · (λ / L)` where L = Nx × d
- Determines illumination taper at reflector edges: `T = 3·(θ₀/θ₃dB)²`
- Plots the feed radiation pattern using sinc function for rectangular aperture

### Part (c) — Reflector Peak Directivity & 3dB Beamwidth
- Computes the cos^n model parameter: `n = -0.05T / log₁₀[cos(θ₀/2)]`
- Calculates aperture efficiency: `η_f = 4·cot²(θ₀/2)·[1-cos^n(θ₀/2)]²·(n+1)/n²`
- Peak directivity: `D_peak = 10·log₁₀[(πD/λ)² · η_f]`
- Secondary beam 3dB beamwidth: `θ₃ = (0.762T + 58.44)·λ/D`
- Plots efficiency vs. taper curves and directivity vs. diameter parametric curves

### Part (d) — Aperture Efficiency
- Reports the computed aperture efficiency from Part (c)
- Analyzes whether the illumination taper is in the optimal 10–12 dB range
- Discusses efficiency optimization strategies

### Part (e) — Secondary Beam Pattern & Sidelobe Reduction
- Plots the reflector secondary radiation pattern using the piecewise Gaussian model:
  - Main beam region: `g(θ) = -3·(2θ/θ₃)² dB`
  - Sidelobe plateau: `g(θ) = SLL`
  - Sidelobe roll-off: `g(θ) = SLL - 25·log(θ / 1.5·θ_SLL)`
- Computes first sidelobe level: `SLL = -0.037T² - 0.376T - 17.6 dB`
- Provides two specific suggestions to reduce sidelobe levels:
  1. Increase illumination taper by adjusting feed parameters
  2. Apply amplitude taper across the array feed elements

### Part (f) — Comparison: 0.5λ vs 0.7λ Element Spacing
- Recomputes all parameters with d = 0.7λ
- Generates a side-by-side comparison table
- Plots the new secondary beam pattern
- Provides detailed analysis of how each performance marker changes:
  - Feed directivity, feed beamwidth, illumination taper
  - Reflector efficiency, peak directivity, secondary beamwidth, sidelobe levels

---

## Key Equations Used

All equations are sourced from:

1. **Element Spacing & Array Directivity** (Ref [1], Eq. 3):
   ```
   D_p = 10·log₁₀(N) + 10·log₁₀[η_e · 4πA_e / λ²]
   ```

2. **Illumination Taper** (Gaussian beam model, Ref [2], Eq. 4):
   ```
   T = 10·log₁₀·e^(-A·(θ₀/θ_b)²)  →  simplified as T = 3·(θ₀/θ₃dB)²
   ```

3. **Reflector Efficiency** (Ref [1], Eq. 15):
   ```
   η_f = 4·cot²(θ₀/2)·[1 - cos^n(θ₀/2)]²·(n+1)/n²
   ```

4. **Peak Directivity** (Ref [1], Eq. 14):
   ```
   D_peak = 10·log₁₀[(4πA/λ²)·η_f]
   ```

5. **3dB Beamwidth** (Ref [1], Eq. 17):
   ```
   θ₃ = (0.762T + 58.44)·λ/D
   ```

6. **Sidelobe Level** (Ref [2], Eq. 7):
   ```
   SLL = -0.037T² - 0.376T - 17.6 dB
   ```

7. **Center-fed geometry**:
   ```
   θ₀ = 2·arctan(D / 4F)
   ```

---

## How to Run

### Local Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd reflector-antenna-problem2

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Hugging Face Spaces

This app is configured for deployment on Hugging Face Spaces with Streamlit SDK v1.43.2. Simply push the repository to a Hugging Face Space and it will auto-deploy.

---

## File Structure

```
.
├── app.py                # Main Streamlit application with all computations and plots
├── requirements.txt      # Python dependencies
├── .gitattributes        # Git LFS configuration
└── README.md             # This file
```

---

## Default Parameter Values

| Parameter | Value | Description |
|-----------|-------|-------------|
| D | 2.5 m | Reflector diameter |
| f/D | 0.9 | Focal-length-to-diameter ratio |
| F | 2.25 m | Focal length (= f/D × D) |
| Frequency | 12 GHz | Operating frequency |
| λ | 25 mm | Wavelength at 12 GHz |
| D/λ | 100 | Reflector diameter in wavelengths |
| Array | 2×2 | Number of patch elements |
| d | 0.5λ | Element spacing (12.5 mm) |
| η_patch | 90% | Patch antenna efficiency |

---

## Interactive Features

- **Sidebar controls** allow overriding all input parameters
- **"Run Full Analysis" button** triggers computation of all parts
- **Multiple plots** generated: reflector sketch, feed pattern, secondary beam, efficiency curves, parametric design curves
- **Comparison mode** automatically computes and displays 0.5λ vs 0.7λ results

---

## References

1. S. K. Rao and C. Ostroot, "Design Principles and Guidelines for Phased Array and Reflector Antennas," *IEEE Antennas & Propagation Magazine*, vol. 62, no. 2, pp. 74–81, April 2020.

2. S. Kotta and G. Gupta, "Reflector Antennas Design and Analysis Software," *IEEE Wireless Antenna and Microwave Symposium (WAMS)*, 2024.

3. S. Kotta and G. Gupta, "Phased Array Antenna Design and Analysis Tool," *IEEE Wireless Antenna and Microwave Symposium (WAMS)*, 2023.

4. S. K. Rao, L. Shafai, S. K. Sharma, *Handbook of Reflector Antennas and Feed Systems*, Volume III, Artech House, 2013.

---

## Author

CICAD 2025 Internship Assignment — Reflector Antenna Problem-2  
Submission Deadline: February 28, 2026

---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
