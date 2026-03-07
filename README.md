# 📡 CICAD 2025 — Phased Array Antenna Design & Analysis Tool

> **Assignment Problem 2:** Design a hexagonal-grid phased array antenna at 44.5 GHz ± 1 GHz with Potter horn elements, circular aperture, 10 dB amplitude taper, ±9° scan, and 40 dBi minimum gain.

---

## 🎯 Overview

This Streamlit application solves the CICAD 2025 Phased Array Problem 2 end-to-end. It implements the closed-form design equations from:

- **S. K. Rao & C. Ostroot**, *"Design Principles and Guidelines for Phased Array and Reflector Antennas,"* IEEE Antennas & Propagation Magazine, April 2020.
- **S. Kotta & G. Gupta**, *"Phased Array Antenna Design and Analysis Tool,"* IEEE WAMS 2023.

The tool calculates element spacing, element gain, number of elements, array layout, and radiation patterns — all interactively via a browser UI.

---

## 📋 Problem Statement

| Parameter | Value |
|---|---|
| Centre frequency | 44.5 GHz |
| Bandwidth | ±1.0 GHz (43.5–45.5 GHz) |
| Grid | Hexagonal |
| Aperture shape | Close to circular |
| Feed element | Potter horn |
| Scan region | ±9 degrees |
| Minimum gain over coverage | 40 dBi |
| Amplitude taper | 10 dB across the array |
| Horn aperture efficiency | 70% |

### Sub-problems

| Part | Task |
|---|---|
| **A** | Calculate the required array peak directivity |
| **B** | Calculate element spacing, element gain, and number of elements |
| **C** | Plot the array layout and radiation patterns |
| **D** | Analyse complexity reduction when scan angle is reduced to ±6° |

---

## 🔬 Key Equations Implemented

### Hexagonal Lattice Element Spacing — Eq. (2)

```
d_h / λ_h ≤ 1.1547 / (sin θ_sm + sin θ_G)
```

where `λ_h` is wavelength at the highest frequency (worst-case grating lobes), `θ_sm` is the maximum scan angle, and `θ_G` is the grating-lobe placement angle.

### Required Peak Directivity — Eq. (5)

```
D_p = G_min + L_s + SL + GL_pe + T_L + X + I_m
```

All terms in dB. `SL` is scan loss, `T_L` is taper loss, `I_m` is implementation margin.

### Number of Elements — Eq. (4)

```
N = 10^(0.1·D_p − 0.1·D_e)
```

### Array Peak Directivity — Eq. (3)

```
D_p = 10·log₁₀(N) + 10·log₁₀[η_e · 4π·A_e / λ_l²]
```

### Scan Loss (Directive Elements, d/λ > 1) — Eq. (6)

```
SL = 3·(θ_sm / (0.5·θ_3))²
```

### Taper Efficiency — Eq. (10)

```
η = 75·(1+T)² / (1+T+T²)   [%]
```

where `T = 10^(−taper_dB/20)`.

---

## 🖥️ Application Structure

```
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitattributes      # Git LFS configuration
└── README.md           # This file
```

### UI Layout

- **Sidebar**: All input parameters (frequency, scan angle, gain, taper, efficiency, losses)
- **Tab A**: Peak directivity calculation with full loss budget
- **Tab B**: Element spacing, element gain, number of elements, grating-lobe analysis
- **Tab C**: Interactive array layout plot + radiation patterns (φ = 0° cut)
- **Tab D**: Side-by-side comparison at reduced scan angle (default ±6°)
- **Tab Ref**: Equations reference card

---

## 🚀 Running Locally

### Prerequisites

- Python 3.9+
- pip

### Install & Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Deploy on Hugging Face Spaces

This repository is configured for direct deployment on [Hugging Face Spaces](https://huggingface.co/spaces) with Streamlit SDK:

1. Create a new Space (SDK: Streamlit)
2. Push this repo
3. The app will build and deploy automatically

---

## 📊 Sample Results (Default Parameters)

| Metric | ±9° Scan | ±6° Scan |
|---|---|---|
| Element spacing (d/λ) | ~3.13 | ~3.61 |
| Scan loss | varies | lower |
| Number of elements | ~469 | fewer |
| Element count reduction | — | significant |

*Exact values depend on all sidebar parameters. Run the app to see live results.*

---

## 🧮 Design Methodology

1. **Frequency Setup**: Use `f_max` for grating-lobe avoidance (shortest λ), `f_min` for directivity (longest λ), `f_center` for nominal calculations.

2. **Grating-Lobe Placement**: Automatically placed just outside the scan region per established rules (θ_G = θ_sm + 1° for ≤15°, +2° for ≤45°, +5° for >60°).

3. **Loss Budget**: Scan loss + taper loss + front-end loss + pointing error + implementation margin → required peak directivity.

4. **Element Count**: From required D_p and achievable D_e, compute N. Generate hexagonal grid inside circular aperture.

5. **Taper Weights**: Parabolic-on-pedestal amplitude distribution applied radially for sidelobe control.

6. **Array Factor**: Full 2D element-by-element summation with taper weights for accurate pattern computation.

---

## 📚 References

1. S. K. Rao and C. Ostroot, "Design Principles and Guidelines for Phased Array and Reflector Antennas," *IEEE Antennas & Propagation Magazine*, vol. 62, no. 2, pp. 74–81, Apr. 2020.

2. S. Kotta and G. Gupta, "Phased Array Antenna Design and Analysis Tool," *IEEE Wireless Antenna and Microwave Symposium (WAMS)*, 2023.

3. S. Kotta and G. Gupta, "Reflector Antennas Design and Analysis Software," *IEEE WAMS*, 2024.

4. R. J. Mailloux, *Phased Array Antenna Handbook*, Artech House, 1994.

---

## 📝 License

This tool is developed for educational purposes as part of the CICAD 2025 internship programme. The design equations are from published IEEE literature.

---

## 👥 Acknowledgments

- **Dr. Sudhakar K. Rao** — Design equations and methodology
- **Dr. Gaurangi Gupta** — Assignment guidance
- **Sriya Kotta** — Original MATLAB/Python software framework

---

*CICAD 2025 | Submission deadline: 28 Feb 2026*
