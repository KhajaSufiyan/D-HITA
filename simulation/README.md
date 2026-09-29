# Simulation (CST Studio Suite, Learning Edition)

| File | Purpose |
|---|---|
| `cst_software_settings.md` | Project units and the `FR4_substrate` material dialog dump. **Note:** this is FR4 with ε = 1 and no loss — it does not describe the `Kapton_flex` (εr 3.5, tan δ 0.002) or aramid (εr 3.8, tan δ 0.02) materials the designs actually use. Those definitions still need to be added. |
| `cst_lessons_and_lband_plan.md` | Ten lessons from the UHF runs and the L-band build plan (2026-09-27) |
| `dhita_geometry_spec_v2.md` | v2 curved, separated boards: construction method, parameters, tables, developed dimensions, results, open issues (2026-09-29) |
| `results/` | Exported S-parameters, patterns and screenshots (none added yet — see its README) |

## Design versions

- **v1 — flat combined board** (R2, 2026-09-28): single Kapton flex sheet, 250 × 445 mm, h = 3.5 mm. Parameters are in `hardware/d-hita_rf_frontend_CONFIG.json`.
- **v2 — curved separated boards on helmet** (2026-09-29): parameters and tables in `dhita_geometry_spec_v2.md`.

Suggested git tags once the CST files are committed: `v1-flat`, `v2-curved`.

## Solver notes

Learning Edition cap: 20,000 tetrahedra (the lessons file also mentions 100k — confirm). v2 settings: cells per max model box edge = 7, adaptive mesh passes min = max = 2. Check the mesh cell count before clicking Start; update farfield and power-loss monitors to the actual resonance after every run.
