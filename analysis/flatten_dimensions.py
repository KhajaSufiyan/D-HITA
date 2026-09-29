#!/usr/bin/env python3
"""Flatten chord (CAD) dimensions of the curved D-HITA boards to developed arc lengths.

Formula from simulation/dhita_geometry_spec_v2.md:
    s = r * asin(x / r), taken at the substrate mid-radius r = 127.75 mm.

Inputs are the X / Y ranges of each shell brick in the CST tables (chord values, mm).
Output is the developed length along each axis, for flex-PCB artwork.

A sphere cannot be flattened without distortion; treat results as a few-percent
approximation and add relief cuts / gores at the corners on the real part.
"""
from math import asin

R_MID = 127.75  # mm, substrate mid-radius (126 .. 129.5)


def arc(x, r=R_MID):
    """Arc length from the crown-centre line to chord coordinate x."""
    return r * asin(x / r)


def developed(lo, hi, r=R_MID):
    """Developed length between two chord coordinates lo..hi."""
    return arc(hi, r) - arc(lo, r)


# (name, (x_lo, x_hi), (y_lo, y_hi)) -- from the UHF table at uL = 94
UHF_PARTS = [
    ("Substrate sU", (-58, 63), (-46, 46)),
    ("Ground gU", (-57, 62), (-45, 45)),
    ("Patch pU", (-47, 47), (-30, 30)),
]

# L-band patch (only row of the L-band table that is not TBC)
LBAND_PARTS = [
    ("Patch pL", (-27.55, 27.55), (-37, 37)),
]


def report(title, parts):
    print(title)
    for name, (x0, x1), (y0, y1) in parts:
        print(f"  {name:<13} {developed(x0, x1):6.1f} x {developed(y0, y1):5.1f} mm")


if __name__ == "__main__":
    report("UHF part (uL = 94)", UHF_PARTS)
    report("L-band part", LBAND_PARTS)
