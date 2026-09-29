# Helmet and head models

## Helmet shell — `helmet_shell_R125_t5.6.stl`

The idealised helmet used in the v2 CST model, as a mesh you can open in FreeCAD, SolidWorks, Blender or any STL viewer (units mm).

| Parameter | Value | From |
|---|---|---|
| Outer radius `hR` | 125 | `../dhita_geometry_spec_v2.md` |
| Thickness `ht` | 5.6 (inner radius 119.4) | same |
| Centre | (0, 0, −126); crown apex at Z = −1 | same |
| Extent | Hemisphere, Z ≥ −126 | same |
| Material in CST | Aramid, εr 3.8, tan δ 0.02 (assumed) | see `../materials.md` |

Regenerate or change parameters: `python3 analysis/make_helmet_shell.py --help` (run from the repo root). The script self-checks that the mesh is watertight and that its volume matches the analytic shell volume (within 1 %).

What it is **not**: a real ballistic-helmet shape, and it does not include the antenna boards. The real helmet model and shell material are still `[TO BE CLARIFIED]`.

## Head model — not yet defined

No head model is documented anywhere in the project files, so none is provided. The head + helmet simulation is still open. Decisions needed before building it:

| Item | Status |
|---|---|
| Head geometry (sphere, ellipsoid, or CST/voxel head) | TBD |
| Head size and air/liner gap to the helmet inner surface (radius 119.4 mm) | TBD |
| Tissue properties at 403–470 MHz and at the L-band frequency | TBD — take from a published tissue database (for example the IT'IS Foundation database) or CST's built-in tissue library, and cite it |
| Homogeneous vs layered (skin / bone / brain) | TBD |
| What to report | Change in resonance, S11 and efficiency versus helmet-only; head-directed radiation; SAR if feasible |

Things to keep in mind:
- The v2 helmet inner radius (119.4 mm, so a hemisphere about 239 mm across) is considerably larger than a typical adult head. Either place a smaller head inside it deliberately, with the gap defined, or revisit the helmet radius.
- A lossy head volume adds a lot of mesh. The v2 model was already tuned to stay under the Learning Edition tetrahedron cap (cells per box edge = 7, adaptive passes = 2), so expect to hit the cap. Check the mesh count before starting, and consider HFSS Student or a reduced model if needed.
- Transmit power (see `../../requirements/sources.md` §4) determines whether SAR is a real concern.
