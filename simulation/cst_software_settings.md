# CST Studio Suite Settings Reference

This document contains the configuration and material settings extracted from CST Studio Suite. It can be used to guide AI or users in replicating or understanding the specific project setup.

## 1. Project Units
*   **Dimensions:** mm
*   **Frequency:** GHz
*   **Voltage:** V
*   **Conductance:** S
*   **Inductance:** nH
*   **Temperature:** °C
*   **Time:** ns
*   **Current:** A
*   **Resistance:** Ohm
*   **Capacitance:** pF

---

## 2. Material Settings: `FR4_substrate`

### General Tab
*   **Material name:** FR4_substrate
*   **Material folder:** [Empty]
*   **Problem type:** Default
*   **Type:** Normal
*   **Epsilon:** 1
*   **Mu:** 1
*   **Color:** Cyan (Light Blue)
*   **Transparency:** 0%
*   **Draw as wireframe:** Unchecked
*   **Draw reflective surface:** Unchecked
*   **Allow outline display:** Checked
*   **Draw outline for transparent shapes:** Unchecked
*   **Add to material library:** Unchecked

### Conductivity Tab
*   **Electric conductivity:** Checked (`El. conductivity`) -> `0 S/m`
*   **Magnetic conductivity:** Checked (`Mag. conductivity`) -> `0 1/Sm`
*   **Advanced parameters:** Unchecked
*   **Tangent delta el. / mag.:** Unchecked
*   **Frequency range [MHz]:** Fmin: `300`, Fmax: `550`

### Dispersion Tab
*   **Dielectric dispersion:** `Disp. model` -> `None`
*   **Magnetic dispersion:** `Disp. model` -> `None`
*   **Parameter conversion System:** Gauss
*   **Parameter conversion Frequency:** 0.0 MHz
*   **Biasing field:** Homogeneous field

### Thermal Tab
*   **General Type:** Normal
*   **Nonlinear:** Unchecked
*   **Thermal conductivity:** 0 W/K/m
*   **Specific heat:** 0 J/K/kg
*   **Material density (Rho):** 0 kg/m³
*   **Thermal diffusivity:** [Empty] m²/s
*   **Dynamic viscosity:** 0 Pa.s
*   **Emissivity:** Checked -> `0`
*   **Thermal expansion coefficient:** 0.0 1e-6 / K
*   **Bioheat - Bloodflow coefficient:** 0 W/K/m³
*   **Bioheat - Basal metabolic rate:** 0.0 W/m³
*   **Bioheat - Convection transfer coefficient (Voxel model):** 0.0 W/m²/K
*   **Solar radiation model - Type:** Opaque
*   **Solar radiation model - Absorptance:** 0.0

### Mechanics Tab
*   **Type:** Unused
*   **Young's modulus:** 0 GPa
*   **Poisson's ratio:** 0.0
*   **Thermal expansion coefficient:** 0.0 1e-6 / K
*   **Material density info:** 0 kg/m³

### Density Tab
*   **Material density Rho:** 0 kg/m³
*   **Buoyancy model Type:** Boussinesq
*   **Thermal expansion coefficient:** 0.0 1e-6 / K
