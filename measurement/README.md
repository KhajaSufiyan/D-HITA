# Measurement

**Nothing has been measured yet.** All numbers in this repo are CST simulation results.

The VNA procedure is in `../hardware/d-hita_rf_frontend_GUIDE.md` §3 (S11 for each band, S21 isolation, matching trim) and §4 (on-helmet and on-head re-measurement, radiation).

Measure and record each band under three conditions so simulation and measurement can be compared: **flat / free space**, **on the helmet**, **helmet worn or on a head phantom**.

## Templates (`templates/`)

- `s11_log_template.csv` — one row per measurement
- `trim_log_template.csv` — one row per matching-component change (this log is the fabrication record for V2; re-measure after every single change)

Suggested layout for raw data: `measurement/data/<date>_<band>_<condition>.s1p` (or `.s2p` for S21).
