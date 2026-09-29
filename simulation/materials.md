# CST Material Definitions — `Kapton_flex`, `Aramid`, PEC

**Read this first:** these are *reconstructed* from the parameter values recorded in the project files. They are **not** an export of your actual CST dialogs (those two dialogs were never provided). Open your `.cst` project, compare each field below against what you actually used, and correct this file where they differ. `cst_software_settings.md` is the real dump for `FR4_substrate`, which the final designs do not use.

## Where each material is used

| Material | Used for | Source of values |
|---|---|---|
| `Kapton_flex` | Substrate (both bands, v1 and v2) | `hardware/d-hita_rf_frontend_CONFIG.json`, `cst_lessons_and_lband_plan.md` |
| `Aramid` | Helmet shell (v2) | `dhita_geometry_spec_v2.md` — **assumed**, not vendor-confirmed |
| PEC | Patch, ground plane, shorting wall, probe | both specs |
| Vacuum | Space between the two v2 boards; brick `c` in the shell construction | `dhita_geometry_spec_v2.md` |

## `Kapton_flex`

| Field | Value |
|---|---|
| Material name | Kapton_flex |
| Type | Normal |
| Epsilon (εr) | 3.5 |
| Mu (μr) | 1 |
| Electric conductivity | 0 S/m |
| Magnetic conductivity | 0 1/Sm |
| Tangent delta (el.) | 0.002 |
| Dispersion | None (dielectric and magnetic) |

Notes:
- εr 3.5 and tan δ 0.002 are the simulated values. The solid 3.5 mm layer does not exist as a laminate: the real part is a thin Kapton layer over a foam or silicone spacer (open fabrication item). Re-simulate with a two-layer stack once the spacer material is chosen.
- If you use "Tangent delta el." with a frequency range, make it span the band being simulated (the FR4 dump used 300–550 MHz for UHF; the L-band plan used 1.0–1.7 GHz), or one material per band.
- Thickness lives in the geometry, not the material: h = 3.5 mm in the final designs (5 mm in the early L-band plan).

## `Aramid` (helmet shell, v2)

| Field | Value |
|---|---|
| Material name | Aramid |
| Type | Normal |
| Epsilon (εr) | 3.8 |
| Mu (μr) | 1 |
| Electric conductivity | 0 S/m |
| Tangent delta (el.) | 0.02 |
| Dispersion | None |

Notes:
- **Assumed.** Replace with vendor or measured data for the real helmet shell when the helmet model is known (`[TO BE CLARIFIED]`).
- The v2 spec attributes about half the input power lost at UHF to this material, so this one number strongly drives the UHF gain result. Sweep tan δ (for example 0.005 to 0.03) before drawing conclusions about the UHF antenna.

## PEC

Patch, ground and shorting wall are PEC. Ground and patch are zero-thickness in v1; in v2 they are 1 mm shells (`tc = 1`). Note that PEC ignores copper loss, so all conductor loss is missing from the reported radiation efficiencies. Real etched copper on flex will be slightly worse.
