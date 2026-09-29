# Hardware

| File | What it is |
|---|---|
| `d-hita_rf_frontend_GUIDE.md` | Step-by-step build guide, revision R2 (fabrication, assembly, VNA bring-up, helmet validation) |
| `d-hita_rf_frontend_PARTS.csv` | Bill of materials (16 line items; estimated costs as recorded, currency not stated) |
| `d-hita_rf_frontend_CONFIG.json` | Full project config: substrate, board geometry, per-band results, parts, connections, removed parts, open items |
| `d-hita_rf_frontend_ELECTRICAL_CONNECTIONS.json` | Signal and ground connections |
| `d-hita_rf_frontend_MECHANICAL_CONNECTIONS.json` | Physical placement and offsets |
| `archive/` | Rejected designs, kept for the record — **do not build** |

## ⚠ These files describe v1 (single flat board), not v2

The guide, BOM and JSON files specify **one** 250 × 445 mm Kapton sheet carrying both patches (UHF 170.4 × 148.8 mm, L-band 55.1 × 74 mm). The v2 design (`../simulation/dhita_geometry_spec_v2.md`) uses **two separate curved flex parts** with a 94 mm shorted UHF patch and no shared ground. Until the hardware files are regenerated for v2, do not send the guide's §1.1 artwork spec to a fab house. Developed (flat) dimensions for the v2 UHF part are in the geometry spec; L-band substrate and ground sizes are still TBC there.

## Fabrication caveat

Solid 3.5 mm Kapton laminate is not a stock product. The plan is a thin Kapton patch/feed layer over a flexible foam or silicone spacer, to be confirmed with the flex fab house. Kapton-over-foam properties will differ from the simulated solid εr 3.5 stack.
