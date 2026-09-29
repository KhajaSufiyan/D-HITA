# Analysis

## `flatten_dimensions.py`

Converts the chord (CAD) dimensions of the curved v2 shells to developed arc lengths for flex-PCB artwork, using `s = r·asin(x/r)` at the substrate mid-radius r = 127.75 mm (formula from `simulation/dhita_geometry_spec_v2.md`).

```
python3 analysis/flatten_dimensions.py
```

Check against the spec: the UHF substrate, ground and patch reproduce the spec's developed sizes exactly (126.1 × 94.1, 123.8 × 92.0, 96.3 × 60.6 mm). The **L-band patch does not quite match**: the script gives 55.5 × 75.1 mm, the spec lists 55.4 × 74.8 mm (0.1 / 0.3 mm apart). Both are within the few-percent distortion the spec already warns about for flattening a sphere, but one of the two calculations used a different radius or method — settle which before sending artwork to a fab house.

## To add

Scripts for plotting S11, extracting −10 dB bandwidth from exported curves, and comparing simulation with measurement once data exists.
