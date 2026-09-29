# Open Items

Collected from the summary PDF, build guide, config JSON and geometry spec v2.

## Requirements and sources
- **L-band video link frequency: unsourced.** The NSG body-worn-video tender and the earlier MHA camera QRs describe cellular / Wi-Fi / internet relay, not an L-band RF link (see `requirements/sources.md` §3). The 1350–1450 MHz assumption (and the 1.30–1.40 GHz in the early plan) has no source. Ask the SIH mentors / NSG nodal contact; find the MHA body-worn-camera QRs (V3)
- Which transmit power class (1.4 W QR hand-held; 4 W, 20 W, 40 W in NSG tenders) would feed the helmet antenna — matters for head exposure / SAR
- NSG radio model(s)
- Numeric targets: gain, bandwidth criterion, S11/VSWR threshold, thickness, mass
- Ruggedness / environmental standard; ballistic / impact validation method
- Section/page numbers for the UHF source and the tender PDFs (retrieved through automated summaries; open and cite properly)

_Resolved 2026-09-30:_ source for the UHF 403–470 MHz band (MHA/CRPF QRs, June 2025) — see `requirements/sources.md`.

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
