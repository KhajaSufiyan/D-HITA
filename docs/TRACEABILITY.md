# Requirement Traceability

Requirement → design response → evidence in this repo → gap. "Sim" means CST simulation only; nothing has been measured.

| SIH26185 requirement | Design response | Evidence so far | Gap |
|---|---|---|---|
| Helmet integration | External side-mounted flex assembly (Design 3), no cutting into the shell | Helmet shell modelled in v2 | Helmet model / mounting method `[TO BE CLARIFIED]`; not physically built |
| Low / zero profile, flexible, conformal | Kapton flex, 3.5 mm stack, curved parts (v2) | Sim v2 | 3.5 mm realisation (foam/silicone) open; flattening needs relief cuts / gores |
| Lightweight, ultra-thin | Passive, no enclosure | — | Mass and thickness limits not stated; nothing weighed |
| UHF support | Probe-fed patch (v1); shorted quarter-wave patch (v2) | v1: 460 MHz, −9.6 dB, 6.84 dBi. v2: 422 MHz, −7.6 dB, −0.96 dBi | v2 fails match and gain; bandwidth never measured |
| L-band support | Half-wave patch, probe-fed | v1: 1364 MHz, −10.15 dB, 7.39 dBi, ~35 MHz. v2: 6.36 dBi | Exact band `[TO BE CLARIFIED]`; v2 S11 marker TBC |
| Underside RF shielding | Continuous ground plane at Z = 0 | Modelled as PEC in both versions | No head-directed-radiation result; head model not documented; shield material TBC |
| Upward / outward radiation | Patches face outward, ground faces head | Directivity values only | No pattern plots in repo |
| High gain | Thick substrate, probe feed | See UHF / L-band rows | Numeric target not stated |
| Ruggedized coax along helmet | U.FL + 50 Ω pigtail to bulkhead | Parts list | Bulkhead type TBC; strain relief untested |
| Connect to existing radios / body-worn video | Independent U.FL output per band | — | Equipment models and connectors `[TO BE CLARIFIED]` |
| No degradation of ballistic protection | No cutting or drilling of the shell | — | No validation method defined |
