# Decision Log

Each entry is taken from the project files in this repo; the source is given so it can be checked.

| Date | Decision | Why | Source |
|---|---|---|---|
| 2026-09-10 | Passive antenna baseline; no helmet battery/MCU/PA | Problem is RF + mechanical integration; active parts add nothing to the baseline | `docs/SIH26185_Project_Summary_DHITA.pdf` §2.1 |
| 2026-09-27 | Substrate **thickness**, not loss tangent, is the efficiency lever; require h/λ ≥ 0.02 | At h = 0.2 mm the UHF patch radiated ~14 % (h/λ ≈ 0.0003, ~88 % of power lost in the dielectric); 5 mm gave 84 % radiation efficiency | `simulation/cst_lessons_and_lband_plan.md` #5, #6 |
| 2026-09-27 | Probe (vertical) feed instead of inset microstrip feed | Inset feed barely matched on a thick substrate (S11 −3.6 → −4.2 dB) | `simulation/cst_lessons_and_lband_plan.md` #8 |
| 2026-09-27 | Zero-thickness metal for patch and ground | Avoids Learning Edition mesh-cell limit | `simulation/cst_lessons_and_lband_plan.md` #1 |
| 2026-09-28 | **Reject** active-switch design (SKY13350 switch + ESP32-C3 + Li-Po on Rogers 4350B in an enclosure) | Replaced by passive dual-feed; no switching, battery, firmware or enclosure needed | `hardware/d-hita_rf_frontend_CONFIG.json` (`revision`, `removedFromPriorRevision`) |
| 2026-09-28 | **Reject** Rogers 4350B; use Kapton flex | Rogers is rigid and cannot conform to helmet curvature | `hardware/d-hita_rf_frontend_CONFIG.json` (`substrate.rationale`) |
| 2026-09-28 | Two independent feeds, no diplexer / crossover | Both bands run simultaneously; a diplexer became unnecessary | `hardware/d-hita_rf_frontend_CONFIG.json` |
| 2026-09-28 | Substrate 3.5 mm (earlier L-band plan used 5 mm) | 3.5 mm is the thickness both bands were tuned to in the combined project | `hardware/d-hita_rf_frontend_CONFIG.json` |
| 2026-09-28 | Accept UHF shift 436 → 460 MHz in the combined layout instead of re-tuning | Still inside the 403–470 MHz band, but close to the upper edge | `hardware/d-hita_rf_frontend_CONFIG.json` (`bands[0].shiftNote`) |
| 2026-09-28 | Coverlay over feed/matching regions only; patches left bare | Dielectric loading over a patch detunes it | `hardware/d-hita_rf_frontend_GUIDE.md` §1.3 |
| 2026-09-28 | Matching pads: 0 Ω series jumper, shunts DNP; values found on the VNA | Simulated match is already ≈ −10 dB; physical board will differ | `hardware/d-hita_rf_frontend_GUIDE.md` §2.1 |
| 2026-09-28 | Ground plane doubles as head-isolation shield | Meets the PS underside-shielding requirement without extra parts | `hardware/d-hita_rf_frontend_CONFIG.json` |
| 2026-09-29 | Move from one flat combined board (v1) to **two separate curved boards** (v2) | A single sheet spanning both boards is a ~190 mm dome section; flattening it needs gores | `simulation/dhita_geometry_spec_v2.md` |
| 2026-09-29 | Build curved geometry as spherical shells (Sphere − Sphere ∩ Brick, then rotate) | The CST Bend tool failed | `simulation/dhita_geometry_spec_v2.md` |
| 2026-09-29 | UHF patch becomes a 94 mm **shorted quarter-wave** patch on the curved board | Footprint reduction; trades gain directly against size (v1 170.4 mm patch: 6.84 dBi; v2: −0.96 dBi) | `simulation/dhita_geometry_spec_v2.md` |

## Practices that changed

- Lesson #3 (2026-09-27) says "never use Boolean". The v2 sphere-shell method (2026-09-29) relies on Boolean Subtract / Intersect / Insert / Add. The lessons file has not been updated to reflect this.
