#!/usr/bin/env python3
"""Compare a simulated and a measured S11 trace: resonance shift, match-depth change and
bandwidth ratio. This is the simulation-vs-measurement evidence the project needs.

Example:
    python3 analysis/compare_sim_meas.py sim_v2_uhf.s1p vna_uhf_on_helmet.s1p --plot compare.png
"""
import argparse
import sys

import numpy as np

from s11_report import analyze
from sparams import load_s, s_db


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sim")
    ap.add_argument("meas")
    ap.add_argument("--funit", default="GHz", help="frequency unit of text/CSV files")
    ap.add_argument("--fmt", default="db", help="text/CSV column format: db, mag, ri, madeg, dbdeg")
    ap.add_argument("--plot", help="save an overlay PNG here")
    a = ap.parse_args(argv)

    fs, ss = load_s(a.sim, funit=a.funit, fmt=a.fmt)
    fm, sm = load_s(a.meas, funit=a.funit, fmt=a.fmt)
    ys, ym = s_db(ss), s_db(sm)
    rs, rm = analyze(fs, ys), analyze(fm, ym)

    def bw(r):
        b = r["bands"]["-10dB"]
        return None if b is None else b["bw_MHz"]

    d = rm["f_res_MHz"] - rs["f_res_MHz"]
    print(f"{'':10}{'sim':>12}{'measured':>12}")
    print(f"{'f_res MHz':<10}{rs['f_res_MHz']:>12.2f}{rm['f_res_MHz']:>12.2f}")
    print(f"{'S11 min dB':<10}{rs['s11_min_dB']:>12.2f}{rm['s11_min_dB']:>12.2f}")
    bs, bm = bw(rs), bw(rm)
    print(f"{'-10dB BW':<10}{('none' if bs is None else f'{bs:.1f}'):>12}{('none' if bm is None else f'{bm:.1f}'):>12}")
    print(f"resonance shift (meas - sim): {d:+.2f} MHz ({100*d/rs['f_res_MHz']:+.2f} %)")
    print(f"match depth change:           {rm['s11_min_dB'] - rs['s11_min_dB']:+.2f} dB (positive = measured is shallower)")
    if bs and bm:
        print(f"bandwidth ratio (meas / sim): {bm / bs:.2f}")

    if a.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(fs / 1e6, ys, label="simulation")
        ax.plot(fm / 1e6, ym, label="measured")
        ax.axhline(-10, color="tab:green", ls="--", lw=1)
        ax.axhline(-7, color="tab:orange", ls="--", lw=1)
        ax.set_xlabel("Frequency (MHz)")
        ax.set_ylabel("S11 (dB)")
        ax.grid(alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(a.plot, dpi=150)
        print("plot saved:", a.plot)
    return 0


if __name__ == "__main__":
    sys.exit(main())
