# Open Items

Collected from the summary PDF, build guide, config JSON and geometry spec v2.

## Requirements and sources
- Exact NSG L-band video link frequency `[TO BE CLARIFIED]` (1350–1450 MHz is a working assumption; the L-band plan used 1.30–1.40 GHz)
- Source document for the UHF 403–470 MHz band (config records it as MHA/CRPF QRs, June 2025, co-signed by NSG; the 10 Sep summary PDF still lists UHF endpoints as unconfirmed)
- NSG radio model(s) and body-worn video RF link
- Numeric targets: gain, bandwidth criterion, S11/VSWR threshold, thickness, mass
- Ruggedness / environmental standard; ballistic / impact validation method

## Simulation
- v2 UHF match is −7.6 dB against a −10 dB target; feed position `uFx` not swept
- v2 UHF resonance 422 MHz vs 436 MHz target
- UHF −10 dB bandwidth never measured or simulated
- L-band ground (`gL`) and substrate (`sL`) X/Y ranges are TBC in the spec (read them from the CST History List)
- L-band S22 marker not recorded; earlier run showed a shift towards ~1500 MHz — needs a clean re-read
- `uL = 91` / `92` not verified (mesher self-intersections)
- Head model / helmet + head simulation not documented in this repo
- Aramid helmet material properties are assumed, not vendor-confirmed
- Learning Edition cell/tetrahedron cap (20,000 vs 100,000 quoted in different files) to be confirmed

## Hardware
- 3.5 mm flexible substrate realisation (thin Kapton over foam/silicone spacer; solid 3.5 mm Kapton is not a stock product)
- Bulkhead connector type, SMA vs TNC `[TO BE CLARIFIED]`
- RF shield material and geometry `[TO BE CLARIFIED]`
- Helmet model, shell material, approved mounting method `[TO BE CLARIFIED]`
- Build guide, parts CSV and config/connection JSON to be rewritten for v2 (two separate parts)

## Process
- Research comparison matrix and gap analysis (3–5 gaps)
- Final team roster
- Flex-PCB artwork (KiCad), fab-house quote, prototype, VNA and radiation measurements
