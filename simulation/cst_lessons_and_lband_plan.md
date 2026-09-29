# D-HITA — CST Lessons Learned (UHF) + L-band Build Plan

**Updated:** 27 Sep 2026
**Hard constraint:** 24 hours to finish UHF + L-band + conform to helmet + 3D sim with real helmet and head. Every step below is picked for speed, not elegance.
**Acceptance rule:** hit the target; if not, within a 30% buffer of target is accepted.

---

## 1. What the UHF run taught us (do not re-learn these)

| # | What happened | Root cause | Rule going forward |
|---|---|---|---|
| 1 | "Mesh cell limit exceeded" (Learning Edition) | Big ground plane + thick metal + default mesh | Zero-thickness metal (patch, ground). Check the mesh cell count in mesh view **before** clicking Start. Confirm the license limit first (seen as both 20k and 100k). |
| 2 | Port "inside metal" / staircasing error | Port Z2 didn't match substrate top after thickness change | Port Z1 = ground (0), Z2 = substrate top. Every time. |
| 3 | Boolean subtract deleted the Patch / cut the Substrate | CST selection order in Boolean dialogs | **Never use Boolean.** Build shapes from separate bricks, or avoid needing a notch at all. |
| 4 | Textbook W/L on Kapton overshot (landed 372 MHz instead of 436) | Closed-form formulas are approximate on thin substrates | Treat formula dims as a start; parametrise L and sweep it once. |
| 5 | Efficiency ~14% even on low-loss Kapton | Substrate electrically too thin (h/λ ≈ 0.0003). 88% of power lost in dielectric, 0 in metal | **h/λ ≥ 0.02.** Thickness is the efficiency lever, not tan δ. |
| 6 | 5 mm substrate → 84% rad. eff., +5.45 dBi gain | Fix for #5 confirmed | Use the same 5 mm stack for L-band so both bands share one build-up. |
| 7 | Stack "disconnected" (S11 ≈ 0 dB, −48 dB eff.) | Set substrate Zmin=3 instead of 0 | Ground Z=0, substrate Zmin=0 → Zmax=h, patch/feed/port-top at Z=h. |
| 8 | Inset feed on 5 mm substrate barely matched (S11 −3.6 → −4.2 dB) | Inset microstrip feed is the wrong tool on a thick substrate | **Use a probe (vertical) feed** — discrete port from ground to patch. No feedline, no notch, no Boolean. Match by moving one X coordinate. |
| 9 | Farfield reported at stale 436 MHz after resonance moved to 448 | Monitor frequency not updated | After every run: read S11 dip → set farfield + power-loss monitors to that frequency → rerun. |
| 10 | Mismatch vs loss confusion | Only looking at S11 | Always read Rad. Eff. vs Tot. Eff.: gap = mismatch; low Rad. Eff. = loss. |

---

## 2. L-band targets

Design centre **1.35 GHz** (band assumption 1.30–1.40 GHz, NSG spec still TO BE CLARIFIED).

| Metric | Target | Accepted (30% buffer) |
|---|---|---|
| Resonance | 1.35 GHz | 1.30–1.40 GHz |
| S11 at resonance | ≤ −10 dB | ≤ −7 dB |
| Rad. efficiency | ≥ 50% (−3 dB) | ≥ 35% (−4.6 dB) |
| Gain | ≥ 5 dBi | ≥ 3.5 dBi |
| −10 dB bandwidth | ≥ 40 MHz | ≥ 28 MHz |

Known limit: a single patch on this stack gives roughly 2–3% bandwidth (~30–40 MHz). It will **not** cover all of 1.30–1.40 GHz. Fine for one video channel; not fine if the full 100 MHz is mandatory.

---

## 3. L-band geometry (Kapton_flex εr=3.5, tan δ=0.002, h=5 mm)

Calculated: λ = 222 mm, h/λ = 0.0225 (passes lesson #5), εeff = 3.18.

| Item | Value (mm) | CST coordinates |
|---|---|---|
| Ground (zero thickness, PEC) | 130 × 130 | X −65..65, Y −65..65, Z 0..0 |
| Substrate (Kapton_flex) | 130 × 130 × 5 | X −65..65, Y −65..65, Z 0..5 |
| Patch (zero thickness, PEC) | L = 57.5 (X), W = 74 (Y) | X −28.75..28.75, Y −37..37, Z 5..5 |
| Probe feed (discrete port) | 10 mm off centre along X (resonant length) | X = 10, Y = 0, Z1 = 0, Z2 = 5 |

Parametrise in CST: `L = 57.5`, `W = 74`, `h = 5`, `px = 10`. Use the parameters in the brick fields so tuning is one number change, not rebuilding bricks.

---

## 4. Run order (L-band)

1. New project, same template (Planar, Frequency Domain). Units as in `cst_software_settings.md`.
2. Frequency range **1.0–1.7 GHz**. Monitors: farfield + power loss at 1.35 GHz.
3. Build ground → substrate → patch with the table above. No feedline.
4. Discrete edge port, 50 Ω, vertical at (px, 0), Z 0 → 5.
5. Mesh view → read the cell count → only then Start.
6. Read S11 dip:
   - Resonance off? Scale L: `L_new = L × (f_got / 1.35)`. One step, rerun.
   - Match off? Sweep `px` 6 → 16 mm in 2 mm steps and keep the best S11. (Toward the edge raises input impedance, toward the centre lowers it.)
7. Update monitors to the actual resonance (lesson #9), rerun, record S11, Rad. Eff., Tot. Eff., gain.
8. Stop when section 2 targets (or buffer) are met. Move on — no polishing.

---

## 5. Open debt (logged, not solved today)

- 5 mm solid Kapton does not exist as a flex laminate. Fabrication equivalent: thin Kapton patch layer on a flexible foam/silicone spacer. Re-check after the helmet sim.
- UHF on 5 mm still needs its match fixed — apply the same probe-feed change (lesson #8).
- L-band exact endpoints still TO BE CLARIFIED.
