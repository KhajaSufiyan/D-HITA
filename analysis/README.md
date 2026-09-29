# Analysis

## `flatten_dimensions.py`

Converts the chord (CAD) dimensions of the curved v2 shells to developed arc lengths for flex-PCB artwork, using `s = r·asin(x/r)` at the substrate mid-radius r = 127.75 mm (formula from `simulation/dhita_geometry_spec_v2.md`).

```
python3 analysis/flatten_dimensions.py
```

Check against the spec: the UHF substrate, ground and patch reproduce the spec's developed sizes exactly (126.1 × 94.1, 123.8 × 92.0, 96.3 × 60.6 mm). The **L-band patch does not quite match**: the script gives 55.5 × 75.1 mm, the spec lists 55.4 × 74.8 mm (0.1 / 0.3 mm apart). Both are within the few-percent distortion the spec already warns about for flattening a sphere, but one of the two calculations used a different radius or method — settle which before sending artwork to a fab house.

## `sparams.py`, `s11_report.py`, `compare_sim_meas.py`, `selftest.py`

Tools for when CST exports and VNA data exist (none in the repo yet). No dependencies beyond numpy and matplotlib.

| Script | Does |
|---|---|
| `sparams.py` | Loads Touchstone (`.s1p` / `.s2p`, RI/MA/DB, any unit) and text/CSV exports (dB, magnitude, Re/Im, mag/phase) |
| `s11_report.py` | Resonance, S11 minimum, −10 dB and −7 dB bandwidth, checked against the acceptance rule (S11 ≤ −10 dB pass, ≤ −7 dB accepted; L-band BW ≥ 40 MHz pass, ≥ 28 MHz accepted; UHF resonance inside 403–470 MHz), plus a PNG plot |
| `compare_sim_meas.py` | Resonance shift, match-depth change and bandwidth ratio between a simulated and a measured trace, plus an overlay plot |
| `selftest.py` | 20 checks against a synthetic resonator with a known analytic answer (resonance, S11 minimum and both bandwidths agree exactly; file formats round-trip; port ordering; plots are written) |

```
python3 analysis/selftest.py
python3 analysis/s11_report.py results/v2_uhf.s1p --band uhf --target 436 --plot uhf.png
python3 analysis/s11_report.py export.txt --band lband --funit GHz --fmt db      # CST 1D text export
python3 analysis/compare_sim_meas.py sim.s1p vna.s1p --plot compare.png
```

Limits: the CST text-export layout hasn't been checked against a real export from your version of CST, so if a file fails to load, send me a sample. The self-test uses synthetic data only. Nothing here reads gain or efficiency; S11 only.

## `make_helmet_shell.py`

Generates the idealised v2 helmet shell as an STL (`simulation/helmet/helmet_shell_R125_t5.6.stl`) from the CST spec, and self-checks that the mesh is watertight and its volume matches the analytic value. See `simulation/helmet/README.md`.
