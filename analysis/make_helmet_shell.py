#!/usr/bin/env python3
"""Generate the simulated D-HITA helmet shell as a binary STL (units: mm).

Geometry from simulation/dhita_geometry_spec_v2.md:
    hemispherical shell, outer radius hR = 125, thickness ht = 5.6 (inner 119.4),
    centre at (0, 0, hZ) with hZ = -126 (crown apex at Z = -1), keeping Z >= hZ.

This is the *idealised CST helmet*, not a real ballistic-helmet shape.

Usage:
    python3 analysis/make_helmet_shell.py [--out simulation/helmet/helmet_shell_R125_t5.6.stl]
Run with --check to only build the mesh in memory and print the self-test.
"""
import argparse
import struct
import sys
from math import cos, sin, pi

import numpy as np


def build_shell(hR=125.0, ht=5.6, hz=-126.0, n_lat=32, n_lon=96):
    """Return (vertices Nx3, triangles Mx3 int) of a closed hemispherical shell."""
    r_out, r_in = hR, hR - ht
    centre = np.array([0.0, 0.0, hz])
    verts = []

    def add(p):
        verts.append(p)
        return len(verts) - 1

    def sphere_grid(r):
        pole = add(centre + [0, 0, r])
        rings = []
        for k in range(1, n_lat + 1):
            th = k * (pi / 2) / n_lat
            ring = [
                add(centre + [r * sin(th) * cos(2 * pi * j / n_lon),
                              r * sin(th) * sin(2 * pi * j / n_lon),
                              r * cos(th)])
                for j in range(n_lon)
            ]
            rings.append(ring)
        return pole, rings

    po, ro = sphere_grid(r_out)
    pi_, ri = sphere_grid(r_in)

    tris = []  # (tri, kind) kind: 'out' | 'in' | 'rim'
    for pole, rings, kind in ((po, ro, "out"), (pi_, ri, "in")):
        for j in range(n_lon):
            jn = (j + 1) % n_lon
            tris.append(((pole, rings[0][j], rings[0][jn]), kind))
        for k in range(n_lat - 1):
            for j in range(n_lon):
                jn = (j + 1) % n_lon
                a, b = rings[k][j], rings[k][jn]
                c, d = rings[k + 1][jn], rings[k + 1][j]
                tris.append(((a, d, c), kind))
                tris.append(((a, c, b), kind))
    for j in range(n_lon):  # rim annulus at Z = hz
        jn = (j + 1) % n_lon
        a, b = ro[-1][j], ro[-1][jn]
        c, d = ri[-1][jn], ri[-1][j]
        tris.append(((a, d, c), "rim"))
        tris.append(((a, c, b), "rim"))

    V = np.array(verts)
    T = []
    for (i, j, k), kind in tris:  # orient every face outward from the solid
        p0, p1, p2 = V[i], V[j], V[k]
        n = np.cross(p1 - p0, p2 - p0)
        cen = (p0 + p1 + p2) / 3 - centre
        want = {"out": cen, "in": -cen, "rim": np.array([0.0, 0.0, -1.0])}[kind]
        T.append((i, j, k) if np.dot(n, want) > 0 else (i, k, j))
    return V, np.array(T, dtype=int)


def signed_volume(V, T):
    a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    return float(np.sum(np.einsum("ij,ij->i", a, np.cross(b, c))) / 6.0)


def is_watertight(T):
    """Every directed edge appears once and its reverse appears once."""
    edges = {}
    for i, j, k in T:
        for e in ((i, j), (j, k), (k, i)):
            edges[e] = edges.get(e, 0) + 1
    return all(n == 1 and edges.get((e[1], e[0]), 0) == 1 for e, n in edges.items())


def write_binary_stl(path, V, T, name=b"D-HITA helmet shell"):
    tri = V[T]
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True)
    with open(path, "wb") as f:
        f.write(name.ljust(80, b" "))
        f.write(struct.pack("<I", len(T)))
        for k in range(len(T)):
            f.write(struct.pack("<12fH", *n[k], *tri[k].ravel(), 0))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--hR", type=float, default=125.0)
    ap.add_argument("--ht", type=float, default=5.6)
    ap.add_argument("--hz", type=float, default=-126.0)
    ap.add_argument("--nlat", type=int, default=32)
    ap.add_argument("--nlon", type=int, default=96)
    ap.add_argument("--out", default="simulation/helmet/helmet_shell_R125_t5.6.stl")
    ap.add_argument("--check", action="store_true", help="self-test only, write nothing")
    a = ap.parse_args(argv)

    V, T = build_shell(a.hR, a.ht, a.hz, a.nlat, a.nlon)
    vol = signed_volume(V, T)
    exact = 2 / 3 * pi * (a.hR ** 3 - (a.hR - a.ht) ** 3)
    ok_vol = vol > 0 and abs(vol - exact) / exact < 0.01
    ok_wt = is_watertight(T)
    print(f"triangles: {len(T)}  vertices: {len(V)}")
    print(f"volume: {vol:,.0f} mm^3 (analytic {exact:,.0f}, diff {100*(vol-exact)/exact:+.2f} %) -> {'OK' if ok_vol else 'FAIL'}")
    print(f"watertight / consistently oriented: {'OK' if ok_wt else 'FAIL'}")
    print(f"Z range: {V[:,2].min():.1f} .. {V[:,2].max():.1f} mm (crown should be {a.hz + a.hR:.1f})")
    if not (ok_vol and ok_wt):
        return 1
    if not a.check:
        write_binary_stl(a.out, V, T)
        print("wrote", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
