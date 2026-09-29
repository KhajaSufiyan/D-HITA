#!/usr/bin/env python3
"""Report resonance, match depth and bandwidth from an S11 trace, checked against the
project acceptance rule (target, or within a 30 % buffer).

Acceptance thresholds (docs: simulation/cst_lessons_and_lband_plan.md, requirements/README.md):
    S11 <= -10 dB  -> PASS,  <= -7 dB -> ACCEPTED (buffer),  otherwise FAIL
    L-band -10 dB bandwidth >= 40 MHz -> PASS, >= 28 MHz -> ACCEPTED   (no UHF bandwidth target defined yet)
    UHF resonance must lie inside 403-470 MHz (MHA/CRPF QRs, June 2025).

Examples:
    python3 analysis/s11_report.py results/v1_flat_uhf.s1p --band uhf --target 436
    python3 analysis/s11_report.py results/lband_s11.csv --band lband --funit GHz --fmt db --plot lband.png
    python3 analysis/s11_report.py run.s2p --port 2 2 --band lband     # S22 from a 2-port file
"""
import argparse
import os
import sys

import numpy as np

from sparams import load_s, s_db

BANDS = {"uhf": (403.0, 470.0), "lband": (None, None)}  # MHz; L-band endpoints are unconfirmed
S11_PASS, S11_BUFFER = -10.0, -7.0
LBAND_BW_PASS, LBAND_BW_BUFFER = 40.0, 28.0


def contiguous_band(f, y, thr, i0):
    """Frequency interval around index i0 where y <= thr, with linear interpolation at the
    crossings. Returns (f_lo, f_hi, truncated) or None if y[i0] > thr. truncated=True means
    the band ran off the end of the sweep, so the bandwidth is a lower bound."""
    if y[i0] > thr:
        return None
    lo = i0
    while lo > 0 and y[lo - 1] <= thr:
        lo -= 1
    hi = i0
    while hi < len(y) - 1 and y[hi + 1] <= thr:
        hi += 1
    trunc = lo == 0 or hi == len(y) - 1

    def cross(a, b):  # a inside, b outside
        return f[a] + (thr - y[a]) * (f[b] - f[a]) / (y[b] - y[a])

    f_lo = f[0] if lo == 0 else cross(lo, lo - 1)
    f_hi = f[-1] if hi == len(y) - 1 else cross(hi, hi + 1)
    return f_lo, f_hi, trunc


def analyze(freq_hz, y_db):
    f = freq_hz / 1e6
    i0 = int(np.argmin(y_db))
    out = {"f_res_MHz": float(f[i0]), "s11_min_dB": float(y_db[i0]), "bands": {}}
    for name, thr in (("-10dB", S11_PASS), ("-7dB", S11_BUFFER)):
        b = contiguous_band(f, y_db, thr, i0)
        out["bands"][name] = None if b is None else {
            "lo_MHz": float(b[0]), "hi_MHz": float(b[1]),
            "bw_MHz": float(b[1] - b[0]), "truncated": bool(b[2]),
        }
    return out


def verdict(value, pass_thr, buf_thr, lower_is_better):
    ok = (value <= pass_thr) if lower_is_better else (value >= pass_thr)
    if ok:
        return "PASS"
    okb = (value <= buf_thr) if lower_is_better else (value >= buf_thr)
    return "ACCEPTED (within 30% buffer)" if okb else "FAIL"


def make_plot(path, freq_hz, y_db, res, band_mhz, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    f = freq_hz / 1e6
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(f, y_db, lw=1.6, label="S11")
    ax.axhline(S11_PASS, color="tab:green", ls="--", lw=1, label="-10 dB target")
    ax.axhline(S11_BUFFER, color="tab:orange", ls="--", lw=1, label="-7 dB (buffer)")
    if band_mhz[0] is not None:
        ax.axvspan(band_mhz[0], band_mhz[1], color="grey", alpha=0.15, label="required band")
    ax.plot(res["f_res_MHz"], res["s11_min_dB"], "rv", label=f'min {res["s11_min_dB"]:.1f} dB @ {res["f_res_MHz"]:.1f} MHz')
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("S11 (dB)")
    ax.set_title(title)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--band", choices=BANDS, help="applies band-specific checks")
    ap.add_argument("--band-lo", type=float, help="required band start, MHz (overrides preset)")
    ap.add_argument("--band-hi", type=float, help="required band end, MHz (overrides preset)")
    ap.add_argument("--target", type=float, help="target resonance, MHz (e.g. 436 or 1363)")
    ap.add_argument("--port", type=int, nargs=2, default=[1, 1], metavar=("I", "J"), help="S(i,j) from a Touchstone file")
    ap.add_argument("--funit", default="GHz", help="frequency unit of text/CSV files (default GHz)")
    ap.add_argument("--fmt", default="db", help="text/CSV column format: db, mag, ri, madeg, dbdeg")
    ap.add_argument("--plot", help="save a PNG plot here")
    a = ap.parse_args(argv)

    f, s = load_s(a.file, a.port[0], a.port[1], a.funit, a.fmt)
    y = s_db(s)
    res = analyze(f, y)
    lo, hi = BANDS.get(a.band, (None, None))
    lo = a.band_lo if a.band_lo is not None else lo
    hi = a.band_hi if a.band_hi is not None else hi

    print(f"file:            {a.file}  (S{a.port[0]}{a.port[1]}, {len(f)} points, {f[0]/1e6:.1f}-{f[-1]/1e6:.1f} MHz)")
    print(f"resonance:       {res['f_res_MHz']:.2f} MHz")
    print(f"S11 at minimum:  {res['s11_min_dB']:.2f} dB   -> {verdict(res['s11_min_dB'], S11_PASS, S11_BUFFER, True)}")
    for k in ("-10dB", "-7dB"):
        b = res["bands"][k]
        if b is None:
            print(f"{k} bandwidth:  none (trace never reaches {k})")
        else:
            note = "  [sweep too narrow: value is a lower bound]" if b["truncated"] else ""
            print(f"{k} bandwidth:  {b['bw_MHz']:.1f} MHz  ({b['lo_MHz']:.1f} - {b['hi_MHz']:.1f}){note}")
    if a.target:
        d = res["f_res_MHz"] - a.target
        print(f"vs target:       {d:+.1f} MHz ({100*d/a.target:+.1f} %) from {a.target:g} MHz")
    if lo is not None:
        inside = lo <= res["f_res_MHz"] <= hi
        print(f"band {lo:g}-{hi:g} MHz: resonance {'inside' if inside else 'OUTSIDE'}")
    if a.band == "lband":
        bw = (res["bands"]["-10dB"] or {}).get("bw_MHz", 0.0)
        print(f"L-band BW check: {bw:.1f} MHz -> {verdict(bw, LBAND_BW_PASS, LBAND_BW_BUFFER, False)}")
    elif a.band == "uhf":
        print("UHF BW check:    no UHF bandwidth target defined yet (open item)")
    if a.plot:
        make_plot(a.plot, f, y, res, (lo, hi), os.path.basename(a.file))
        print("plot saved:     ", a.plot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
