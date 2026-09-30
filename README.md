# D-HITA — Dual-band Helmet-Integrated Tactical Antenna

**SIH26185 · Ministry of Home Affairs / National Security Guard (Police II Division) · Category: Hardware**  
**Team: Tech Elite-X (Team ID: 150092) · Theme: Robotics and Drones**

A lightweight, flexible, low-profile antenna that moves tactical-radio and body-worn-video antennas from the vest to the helmet, for NSG operators working in urban close-quarter-battle (CQB) environments. It is **passive** (no battery, MCU or switch), covers **UHF** (radio) and **L-band** (video) with two independent probe-fed microstrip patches on Kapton flex, and uses the underside ground plane as a head-isolation shield. Each band has its own U.FL output and 50 Ω coax pigtail.

## Status — read this first

| Stage | State |
|---|---|
| Problem analysis, requirements | Done (numeric targets partly `[TO BE CLARIFIED]`) |
| EM simulation (CST Studio Learning Edition) | **Done for flat board (v1); curved-on-helmet (v2) partly done** |
| Flex-PCB artwork / fabrication | **Not started** |
| VNA / radiation measurements | **None — everything below is simulated, not measured** |
| Helmet + head simulation | Helmet shell modelled in v2; head model not documented in this repo |

## Headline simulation results

Two design versions exist. They are **different antennas** — do not compare rows across versions without reading the notes.

| | v1 — flat combined board (R2, 2026-09-28) | v2 — curved separated boards on helmet (2026-09-29) |
|---|---|---|
| Layout | One 250 × 445 mm flex sheet carrying both patches | Two independent curved flex parts on a spherical helmet shell |
| UHF resonance | 460 MHz | 422 MHz (target 436) |
| UHF S11 | −9.6 dB | −7.6 dB |
| UHF radiation efficiency | 74 % (−1.319 dB) | −3.418 dB (~46 %) |
| UHF gain | 6.84 dBi | −0.96 dBi (IEEE) |
| UHF patch | 170.4 × 148.8 mm, probe-fed | 94 mm shorted quarter-wave patch |
| L-band resonance | 1364 MHz | ~1364 MHz (marker TBC) |
| L-band S11 | −10.15 dB | TBC |
| L-band radiation efficiency | 92 % (−0.35 dB) | −0.279 dB (~94 %) |
| L-band gain | 7.39 dBi | 6.36 dBi (IEEE) |
| L-band −10 dB bandwidth | ~35 MHz | not recorded |

Notes: v2 UHF gain is dominated by mismatch (monitor at 436 MHz, resonance at 422 MHz) and lossy aramid helmet material (assumed εr 3.8, tan δ 0.02, not vendor-confirmed). UHF −10 dB bandwidth has never been measured. Full detail: [`simulation/dhita_geometry_spec_v2.md`](simulation/dhita_geometry_spec_v2.md) and [`hardware/d-hita_rf_frontend_CONFIG.json`](hardware/d-hita_rf_frontend_CONFIG.json).

## Acceptance rule

Hit the target; if not, within a **30 % buffer** of target is accepted (e.g. S11 ≤ −7 dB against a −10 dB target).

## Repository map

| Folder | Contents |
|---|---|
| [`docs/`](docs/) | Project summary PDF, decision log, open items, requirement traceability |
| [`requirements/`](requirements/) | SIH26185 requirements, working numeric targets, and a source register (UHF band, NSG tenders) |
| [`research/`](research/) | Reference list (five papers) — comparison matrix not yet built |
| [`simulation/`](simulation/) | CST settings, materials, lessons learned, geometry spec v2, helmet model, results |
| [`hardware/`](hardware/) | Build guide, parts list (CSV), config + connection JSON, archived rejected design |
| [`measurement/`](measurement/) | VNA procedure pointer and log templates (no data yet) |
| [`analysis/`](analysis/) | Python tools: S11 report, sim-vs-measurement comparison, flat-artwork converter, helmet STL generator (self-tested) |
| [`presentation/`](presentation/) | Official SIH 2026 slide deck (PPTX, PDF, and slide previews) |
| [`images/`](images/) | Screenshots and renders (to be added) |

## Known inconsistencies (being resolved)

- The build guide, parts CSV and config/connection JSON describe **v1** (single flat 250 × 445 mm sheet). v2 requires **two separate flex parts**. These files have not yet been updated to v2 — see [`hardware/README.md`](hardware/README.md).
- `docs/SIH26185_Project_Summary_DHITA.pdf` is dated 10 Sep 2026 and states that no simulation results exist; that is no longer true.
- The UHF 403–470 MHz band now has a primary source (MHA/CRPF QRs, June 2025, NSG co-signed) — see [`requirements/sources.md`](requirements/sources.md).
- **The L-band video-link frequency is unsourced.** The NSG body-worn-video tender describes relay over a cellular network and the internet, with no RF band or L-band requirement; the earlier MHA camera QRs list 4G/3G + Wi-Fi. The PS still asks for L-band, but the 1350–1450 MHz figure has no source. Details and next step in [`requirements/sources.md`](requirements/sources.md) §3.

## Open items

See [`docs/OPEN_ITEMS.md`](docs/OPEN_ITEMS.md). Highlights: exact NSG L-band video frequency, bulkhead connector (SMA vs TNC), RF shield material, helmet model and mounting method, 3.5 mm flexible substrate realisation (Kapton over foam/silicone), UHF bandwidth and match on the curved board.

## Team

Roster `[TO BE CLARIFIED]` — see [`TEAM.md`](TEAM.md) (template, to be filled in).
