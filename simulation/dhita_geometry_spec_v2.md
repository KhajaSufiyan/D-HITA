# D-HITA Geometry Spec v2 — separated curved boards (CST, uL = 94)

Status: UHF stack complete and solving. L-band ground/substrate footprint TBC.
Date: 2026-09-29. Supersedes the earlier flat combined-board spec.

## Construction method (sphere-shell, replaces the failed Bend tool)

Every antenna layer is a spherical shell segment built the same way:

1. Sphere, centre (0, 0, hZ), outer radius = R_outer
2. Sphere `t`, centre (0, 0, hZ), radius = R_inner -> Boolean **Subtract**
3. Brick `c`, X/Y range as tabled, Z from hZ to 20, Vacuum -> Boolean **Intersect**
4. Transform -> Rotate about global X, pivot (0, 0, hZ), "Shape center" UNCHECKED, OK once

Choose **None** on every Shape Intersection pop-up. `c` must show a solid-cube icon
before the Intersect; a sheet icon means a zero-thickness brick, which silently turns
the shell into a 2D sheet and breaks the mesher with "self-intersections".

## Parameters

| Name | Value | Meaning |
|---|---|---|
| hR | 125 | helmet outer radius (mm) |
| hZ | -126 | helmet centre Z; crown apex at Z = -1 |
| ht | 5.6 | helmet shell thickness |
| h | 3.5 | substrate thickness |
| tc | 1 | conductor thickness |
| uL | 94 | UHF patch length |
| uFx | 12 | UHF feed distance from the short |
| band2L | 55.1 | L-band patch X length |
| band2W | 74 | L-band patch Y width |
| band2Px | 16 | L-band probe offset from patch centre |

## Helmet

Sphere centre (0, 0, -126), outer radius 125, inner radius 119.4 (= hR - ht),
cut to a hemisphere keeping Z >= -126. Material Aramid, er 3.8, tan d 0.02 (assumed,
not vendor-confirmed).

## Board topology — TWO SEPARATE PIECES

The UHF and L-band boards are independent. `gU/sU/pU` and `gL/sL/pL` are separate
shells with vacuum between them: no shared substrate, no shared ground, nothing
bridging the gap. Their centres are 49 deg apart on the helmet (-24 deg and +25 deg).

They must be fabricated as two separate flex parts. A single sheet spanning 49 deg
plus both board widths would be a dome section ~190 mm across, and flattening that
much double curvature requires gores. It is also not what is simulated.

The two ground planes are electrically isolated. The only common point in a real
build is the radio chassis, where both coax shields land. Bridging them on the
helmet changes both bands.

Keep-out gap, measured from the crown at the ground radius 125.5 mm:
- UHF ground near edge: 2.98 deg from the crown = 6.5 mm of arc
- L-band ground near edge: TBC
- Total gap approx **13 mm**, assuming gL runs to +/-47 mm in Y. Consistent with the
  ~12.7 mm figure recorded earlier. Confirm from the gL brick.

## UHF board — shorted quarter-wave patch, rotate X = -24 deg (lands on +Y side)

| Shape | Material | R inner | R outer | X range | Y range |
|---|---|---|---|---|---|
| gU ground | PEC | 125 | 126 | -57 .. +62 | -45 .. +45 |
| sU substrate | Kapton | 126 | 129.5 | -58 .. +63 | -46 .. +46 |
| pU patch | PEC | 129.5 | 130.5 | -47 .. +47 | -30 .. +30 |
| wU short wall | PEC | 125 | 130.5 | -47 .. -45 | -30 .. +30 |

X max of gU = `-47+uL+15`; X max of sU = `-46+uL+15`; X max of pU = `-47+uL`.

The wall deliberately reaches down to R 125, overlapping gU, so the two bond in the
mesh. A wall that only touches gU at R 126 does NOT connect: the resonance stays at
the unshorted value (~955 MHz) and CST reports self-intersections. Build order after
rotating wU: `sU` Boolean **Insert** wU, then `pU` Boolean **Add** wU.

Port 1: discrete edge, 50 ohm, radius 0, global coordinates (not WCS), defined after
rotation: (-35, 49.02, -15.9) -> (-35, 50.92, -11.62).
Lower end sits at r = 125.5 (inside gU), upper end at r = 130.0 (inside pU).

## L-band board — half-wave patch, rotate X = +25 deg (lands on -Y side)

| Shape | Material | R inner | R outer | X range | Y range |
|---|---|---|---|---|---|
| gL ground | PEC | 125 | 126 | TBC | TBC |
| sL substrate | Kapton | 126 | 129.5 | TBC | TBC |
| pL patch | PEC | 129.5 | 130.5 | -27.55 .. +27.55 | -37 .. +37 |

Port 2: discrete edge, 50 ohm, (16, -52.61, -13.19) -> (16, -54.52, -9.08).
Same radii as port 1. This port has worked reliably from the start.

To fill the TBC rows: History List -> the "define brick: component1:c" rows
immediately before `boolean intersect shapes: component1:gL, component1:c` and the
same for `sL` -> select the row and click Edit.

## Developed (flattened) dimensions — for flex-PCB artwork

Arc length s = r * asin(x / r), taken at the substrate mid-radius r = 127.75 mm.
Form both parts to a 127.75 mm spherical radius. The chord values in the tables
above are for CAD only; do not use them for artwork.

### UHF part

| Feature | Developed size |
|---|---|
| Substrate sU | 126.1 x 94.1 mm |
| Ground gU | 123.8 x 92.0 mm |
| Patch pU | 96.3 x 60.6 mm |
| Shorting wall | 2.2 mm wide, full 60.6 mm patch edge |
| Feed from shorted edge | 12.7 mm |

Placement inside the UHF part (the patch is NOT centred along the long axis):
- Ground inset 1.1 mm from the substrate edge on all four sides
- Patch long axis: 12.1 mm from the substrate edge at the shorted end,
  17.8 mm at the open end
- Patch short axis: centred, 16.8 mm margin each side
- Bend axis along the 126.1 mm dimension

The asymmetry is deliberate: the ground extends further past the open end, which is
where the fringing fields radiate.

### L-band part

| Feature | Developed size |
|---|---|
| Patch pL | 55.4 x 74.8 mm |
| Feed from patch centre | 16 mm, along the 55.4 mm axis |
| Substrate sL | TBC |
| Ground gL | TBC |

Bend axis along the long dimension.

A spherical surface cannot be flattened without distortion. Over this angular span the
error is a few percent; a real flex part needs relief cuts or gores at the corners.

## Simulation results at uL = 94

| | UHF (port 1) | L-band (port 2) |
|---|---|---|
| S11 minimum | 422 MHz @ -7.6 dB | ~1364 MHz (marker TBC) |
| Target | 436 MHz | 1363 MHz |
| Directivity | 2.462 dBi | 6.634 dBi |
| Radiation efficiency | -3.418 dB | -0.279 dB |
| Total efficiency | -19.25 dB | -0.478 dB |
| Gain (IEEE) | -0.96 dBi | 6.36 dBi |
| Realized gain | -16.79 dBi | 6.16 dBi |

UHF realized gain is dominated by mismatch: the monitor is at 436 MHz while the
antenna resonates at 422 MHz. Tuned, it would reach roughly -1 dBi. The ceiling is
physical: at 436 MHz the 94 mm patch is 0.14 lambda, and the lossy Aramid absorbs
about half the input power. The earlier flat combined board hit 6.84 dBi at 460 MHz
with a 170.4 mm patch, so gain here is traded directly against footprint.

## Known open issues

- `uL = 91` and `uL = 92` were not verified; changing uL rebuilt three coincident
  curved shells at once and the mesher failed with self-intersections. Untested
  workaround: leave gU/sU at 94 and Subtract a trim brick from pU alone.
- UHF match is -7.6 dB against a -10 dB requirement. `uFx` has not been swept.
- UHF -10 dB bandwidth is only a few MHz. Not yet measured or checked against the
  NSG requirement.
- L-band S2,2 shifted between runs (1364 MHz standalone, nearer 1500 MHz in one
  combined run). Needs a clean re-read now that the UHF stack is stable.
- Solver settings: cells per max model box edge = 7, adaptive mesh passes min = max = 2,
  to stay under the Learning Edition's 20,000 tetrahedron cap.
