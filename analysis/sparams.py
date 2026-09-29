"""Loaders for S-parameter data: Touchstone (.s1p/.s2p) and simple text/CSV exports.

Used by s11_report.py and compare_sim_meas.py. No dependencies beyond numpy.
"""
import os
import re

import numpy as np

_UNIT = {"HZ": 1.0, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
_NUM = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")


def _complex(a, b, fmt):
    fmt = fmt.upper()
    if fmt == "RI":
        return a + 1j * b
    if fmt == "MA":
        return a * np.exp(1j * np.deg2rad(b))
    if fmt == "DB":
        return 10 ** (a / 20.0) * np.exp(1j * np.deg2rad(b))
    raise ValueError(f"unknown Touchstone format {fmt!r}")


def read_touchstone(path):
    """Return (freq_hz [N], S [N, n, n]) for a 1- or 2-port Touchstone file."""
    m = re.search(r"\.s(\d+)p$", path, re.I)
    if not m:
        raise ValueError(f"not a Touchstone file name: {path}")
    n = int(m.group(1))
    if n not in (1, 2):
        raise ValueError("only .s1p and .s2p are supported")
    unit, fmt = 1e9, "MA"  # Touchstone defaults
    nums = []
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            line = line.split("!", 1)[0].strip()
            if not line:
                continue
            if line.startswith("#"):
                for tok in line[1:].upper().split():
                    if tok in _UNIT:
                        unit = _UNIT[tok]
                    elif tok in ("RI", "MA", "DB"):
                        fmt = tok
                continue
            nums.extend(float(t) for t in line.split())
    per = 1 + 2 * n * n
    if len(nums) % per:
        raise ValueError(f"{path}: {len(nums)} numbers is not a multiple of {per}")
    d = np.array(nums).reshape(-1, per)
    freq = d[:, 0] * unit
    vals = _complex(d[:, 1::2], d[:, 2::2], fmt)
    if n == 1:
        S = vals.reshape(-1, 1, 1)
    else:  # file order is S11 S21 S12 S22
        S = np.empty((len(freq), 2, 2), dtype=complex)
        S[:, 0, 0], S[:, 1, 0], S[:, 0, 1], S[:, 1, 1] = vals.T
    return freq, S


def read_text(path, funit="GHz", fmt="db"):
    """Read a delimited text/CSV export. Header and comment lines are skipped.

    fmt: 'db'    freq, S_dB
         'mag'   freq, |S|
         'ri'    freq, Re, Im
         'madeg' freq, |S|, phase_deg
         'dbdeg' freq, S_dB, phase_deg
    Returns (freq_hz, s complex 1-D).
    """
    rows = []
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            toks = [t for t in re.split(r"[,;\s]+", line.strip()) if t]
            if toks and all(_NUM.match(t) for t in toks):
                rows.append([float(t) for t in toks])
    if not rows:
        raise ValueError(f"{path}: no numeric rows found")
    w = min(len(r) for r in rows)
    d = np.array([r[:w] for r in rows])
    freq = d[:, 0] * _UNIT[funit.upper()]
    fmt = fmt.lower()
    need = {"db": 2, "mag": 2, "ri": 3, "madeg": 3, "dbdeg": 3}[fmt]
    if w < need:
        raise ValueError(f"{path}: format {fmt!r} needs {need} columns, found {w}")
    if fmt == "db":
        s = 10 ** (d[:, 1] / 20.0) + 0j
    elif fmt == "mag":
        s = d[:, 1] + 0j
    elif fmt == "ri":
        s = d[:, 1] + 1j * d[:, 2]
    elif fmt == "madeg":
        s = d[:, 1] * np.exp(1j * np.deg2rad(d[:, 2]))
    else:
        s = 10 ** (d[:, 1] / 20.0) * np.exp(1j * np.deg2rad(d[:, 2]))
    return freq, s


def load_s(path, i=1, j=1, funit="GHz", fmt="db"):
    """Load S(i,j) from a Touchstone or text file. Returns (freq_hz, s complex 1-D), sorted by frequency."""
    if re.search(r"\.s\d+p$", path, re.I):
        f, S = read_touchstone(path)
        s = S[:, i - 1, j - 1]
    else:
        if (i, j) != (1, 1):
            raise ValueError("text/CSV files hold a single trace; use i=j=1")
        f, s = read_text(path, funit, fmt)
    order = np.argsort(f)
    return f[order], s[order]


def s_db(s):
    return 20.0 * np.log10(np.maximum(np.abs(s), 1e-12))
