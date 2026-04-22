# 🌌 DITM-Framework (v2.1)
### Dense Interaction Theory Model: A Numerical Approach to Gravity and Galactic Dynamics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Overview
**DITM-Framework** is a numerical simulation engine that models gravitational interaction as a fluid-dynamic process within a **dense spatial grid (The Bulk)**. 

Unlike Modified Newtonian Dynamics (MOND), DITM does not alter Newton's law itself but redefines the **medium** through which gravity propagates. This framework provides a unified explanation for kinetic anomalies and galactic observations without the need for **Dark Matter**.

---

## 📐 Mathematical Foundation
The model is built on two fundamental constraints of the spatial grid:

### 1. Grid Interaction Ceiling ($VC_{LIMIT}$)
Derived from the geometric ratio of linear propagation vs. grid node topology:
$$VC_{LIMIT} = \frac{C}{1 + \pi} \approx 83,424.62 \text{ km/s}$$
*This represents the maximum "clock speed" of physical reality.*

### 2. Grid Saturation ($S$)
As gravitational potential ($\phi$) approaches the grid's capacity, permeability decreases to prevent singularities:
$$S = \frac{1}{1 + (\phi / \phi_{crit})}$$

---

## 📊 Core Simulation Results
Verified across 15 orders of magnitude using the integrated `test_bench.py`.

| Object | Saturation % | Gravity (m/s²) | Status |
| :--- | :--- | :--- | :--- |
| **Earth** | 100.0000% | **9.8200** | Match (Standard) |
| **Sun** | 99.9964% | **273.7663** | Match (Standard) |
| **Galaxy (50k ly)** | N/A | **+50.72% Boost** | **Dark Matter Alternative** |
| **Neutron Star** | 21.9925% | **~1.03e11** | Singularity Prevented |

---

## 🚀 Kinetic Anomalies Replication
DITM replicates historical NASA probe data using a single universal viscosity constant ($\zeta$).

| Probe Name | Altitude (km) | DITM Drift (mm/s²) |
| :--- | :--- | :--- |
| **Pioneer 10** | Deep Space | **-0.0000000105** |
| **NEAR Shoemaker** | 539 | **-0.0002377358** |
| **Galileo (Flyby I)** | 960 | **-0.0002305568** |
| **Rosetta** | 1954 | **-0.0001346541** |

### 🛰️ Interpretation
- **Flyby Anomalies:** Low-altitude probes (NEAR, Galileo) show higher drift due to intensified interaction with Earth's "Propeller Effect" (frame-dragging of the Bulk).
- **Pioneer Anomaly:** The deep space drift matches the expected sunward acceleration vector caused by baseline Bulk Drag.

---

## 🌀 Galactic Dynamics
In large-scale systems, the **Propeller Effect** (rotational stirring of the Bulk) becomes the dominant force. At galactic scales, DITM provides the necessary velocity boost to match observed rotation curves without requiring Dark Matter halos.

---

## 🛠 Installation & Usage
1. Clone the repository.
2. Ensure you have the engine files in the `/engine` folder.
3. Run the test bench:
   ```bash
   python test_bench.py