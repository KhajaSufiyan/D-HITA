#!/usr/bin/env python3
"""Self-test for the analysis scripts, using a synthetic resonator with a known analytic answer.

    python3 analysis/selftest.py

The synthetic antenna is a coupled resonator: G(f) = (b - 1 - jx) / (b + 1 + jx), x = 2*Q*(f-f0)/f0.
    |S11| at f0        = |b-1| / (b+1)
    -10 dB bandwidth   = x10 * f0 / Q,  x10 = sqrt((0.1(b+1)^2 - (b-1)^2) / 0.9)
Nothing here is project data; it only proves the tools compute what they claim to.
"""
import contextlib
import io
import os
import subprocess
import sys
import tempfile

import numpy as np

import compare_sim_meas
import s11_report
from sparams import load_s, s_db

HERE = os.path.dirname(os.path.abspath(__file__))
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")


def resonator(f_mhz, f0, bw10, beta=1.5):
    x10 = np.sqrt((0.1 * (beta + 1) ** 2 - (beta - 1) ** 2) / 0.9)
    q = x10 * f0 / bw10
    x = 2 * q * (f_mhz - f0) / f0
    return (beta - 1 - 1j * x) / (beta + 1 + 1j * x), q


def analytic(f0, bw10, beta=1.5):
    x10 = np.sqrt((0.1 * (beta + 1) ** 2 - (beta - 1) ** 2) / 0.9)
    thr7 = 10 ** (-0.7)
    x7 = np.sqrt((thr7 * (beta + 1) ** 2 - (beta - 1) ** 2) / (1 - thr7))
    return {
        "smin": 20 * np.log10(abs(beta - 1) / (beta + 1)),
        "bw7": bw10 * x7 / x10,
    }


def write_s1p(path, f_hz, s, fmt="DB", unit="GHz"):
    div = {"HZ": 1, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}[unit.upper()]
    with open(path, "w") as fh:
        fh.write("! synthetic\n")
        fh.write(f"# {unit} S {fmt} R 50\n")
        for f, v in zip(f_hz, s):
            if fmt == "DB":
                a, b = 20 * np.log10(abs(v)), np.degrees(np.angle(v))
            elif fmt == "MA":
                a, b = abs(v), np.degrees(np.angle(v))
            else:
                a, b = v.real, v.imag
            fh.write(f"{f/div:.9g} {a:.9g} {b:.9g}\n")


def main():
    f0, bw10 = 1364.0, 35.0
    f_mhz = np.linspace(1000, 1700, 2801)  # 0.25 MHz step
    f_hz = f_mhz * 1e6
    s, _ = resonator(f_mhz, f0, bw10)
    ref = analytic(f0, bw10)

    # 1. analysis vs analytic
    r = s11_report.analyze(f_hz, s_db(s))
    check("resonance", abs(r["f_res_MHz"] - f0) < 0.3, f'{r["f_res_MHz"]:.2f} vs {f0}')
    check("S11 minimum", abs(r["s11_min_dB"] - ref["smin"]) < 0.05, f'{r["s11_min_dB"]:.3f} vs {ref["smin"]:.3f} dB')
    check("-10 dB bandwidth", abs(r["bands"]["-10dB"]["bw_MHz"] - bw10) < 0.3, f'{r["bands"]["-10dB"]["bw_MHz"]:.2f} vs {bw10} MHz')
    check("-7 dB bandwidth", abs(r["bands"]["-7dB"]["bw_MHz"] - ref["bw7"]) < 0.3, f'{r["bands"]["-7dB"]["bw_MHz"]:.2f} vs {ref["bw7"]:.2f} MHz')

    with tempfile.TemporaryDirectory() as tmp:
        # 2. Touchstone round trips in all formats and units
        for fmt in ("DB", "MA", "RI"):
            for unit in ("GHz", "MHz"):
                p = os.path.join(tmp, f"t_{fmt}_{unit}.s1p")
                write_s1p(p, f_hz, s, fmt, unit)
                f2, s2 = load_s(p)
                ok = np.allclose(f2, f_hz, rtol=1e-8) and np.max(np.abs(s_db(s2) - s_db(s))) < 1e-3
                check(f"touchstone {fmt}/{unit} round trip", ok)

        # 3. s2p port ordering: file order is S11 S21 S12 S22
        p = os.path.join(tmp, "two.s2p")
        with open(p, "w") as fh:
            fh.write("# GHz S RI R 50\n")
            fh.write("1.0  0.1 0.0  0.2 0.0  0.3 0.0  0.4 0.0\n")
            fh.write("2.0  0.1 0.0  0.2 0.0  0.3 0.0  0.4 0.0\n")
        got = {(i, j): load_s(p, i, j)[1][0].real for i in (1, 2) for j in (1, 2)}
        check("s2p ordering", got == {(1, 1): 0.1, (2, 1): 0.2, (1, 2): 0.3, (2, 2): 0.4}, str(got))

        # 4. text/CSV with header, dB and Re/Im
        p = os.path.join(tmp, "cst.csv")
        with open(p, "w") as fh:
            fh.write("Frequency / GHz, S1,1 [dB]\n")
            fh.write("# comment\n")
            for f, y in zip(f_mhz / 1e3, s_db(s)):
                fh.write(f"{f:.9g},{y:.9g}\n")
        f3, s3 = load_s(p, funit="GHz", fmt="db")
        check("csv dB with header", np.max(np.abs(s_db(s3) - s_db(s))) < 1e-6)
        p = os.path.join(tmp, "ri.txt")
        with open(p, "w") as fh:
            for f, v in zip(f_mhz / 1e3, s):
                fh.write(f"{f:.9g} {v.real:.9g} {v.imag:.9g}\n")
        f4, s4 = load_s(p, funit="GHz", fmt="ri")
        check("text Re/Im", np.max(np.abs(s4 - s)) < 1e-6)

        # 5. no dip -> no bandwidth
        flat = -5.0 + 0 * f_mhz
        r5 = s11_report.analyze(f_hz, flat)
        check("shallow trace has no -10 dB band", r5["bands"]["-10dB"] is None and r5["bands"]["-7dB"] is None)

        # 6. band running off the sweep is flagged
        keep = (f_mhz > 1350) & (f_mhz < 1380)
        r6 = s11_report.analyze(f_hz[keep], s_db(s)[keep])
        check("truncated band flagged", r6["bands"]["-7dB"]["truncated"] or r6["bands"]["-10dB"]["truncated"])

        # 7. simulation vs measurement: shifted +10 MHz
        s_shift, _ = resonator(f_mhz, f0 + 10, bw10)
        ps, pm = os.path.join(tmp, "sim.s1p"), os.path.join(tmp, "meas.s1p")
        write_s1p(ps, f_hz, s)
        write_s1p(pm, f_hz, s_shift)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            compare_sim_meas.main([ps, pm, "--plot", os.path.join(tmp, "cmp.png")])
        out = buf.getvalue()
        check("compare reports +10 MHz shift", "+10.00 MHz" in out or "+9.9" in out or "+10.0" in out, out.splitlines()[-4] if out else "")
        check("compare plot written", os.path.getsize(os.path.join(tmp, "cmp.png")) > 2000)

        # 8. CLI end to end + plot
        png = os.path.join(tmp, "rep.png")
        cp = subprocess.run(
            [sys.executable, os.path.join(HERE, "s11_report.py"), ps, "--band", "lband", "--target", "1363", "--plot", png],
            capture_output=True, text=True,
        )
        check("s11_report CLI runs", cp.returncode == 0 and "L-band BW check" in cp.stdout, cp.stderr.strip()[:200])
        check("s11_report verdicts", "PASS" in cp.stdout and "S11 at minimum" in cp.stdout)
        check("s11_report plot written", os.path.exists(png) and os.path.getsize(png) > 2000)

    print()
    print(f"{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
