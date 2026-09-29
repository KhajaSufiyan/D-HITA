# Requirements

## SIH26185 requirements (from the problem statement, as summarised in the project PDF §1.2)

| Requirement | Meaning |
|---|---|
| Helmet integration | Integrate seamlessly into/on tactical ballistic helmets |
| Low / zero profile | Minimal protrusion, ruggedized |
| Flexible / conformal | Elements conform to helmet geometry |
| Lightweight, ultra-thin | Microstrip patch elements |
| UHF + L-band | Both must be supported; the PS gives **no** numeric endpoints |
| RF shielding | Underside shield isolates the head |
| Radiation direction | Optimised upward and outward |
| High gain | No numeric target stated |
| Coax interface | Ruggedized coax routed cleanly along the helmet to existing radios and body-worn video |
| Protection | Must not degrade ballistic or impact ratings |

The PS does **not** state 300 MHz–3 GHz, or any gain, bandwidth, range, substrate, shield material, connector, dimension or weight figure. Those are engineering targets derived by the team.

## Working targets

**Acceptance rule:** target, or within a 30 % buffer.

| Metric | UHF | L-band |
|---|---|---|
| Band | 403–470 MHz (sourced, see `sources.md`) | 1350–1450 MHz working assumption (1.30–1.40 GHz in the early plan) — `[TO BE CLARIFIED]` |
| S11 at resonance | ≤ −10 dB (accepted ≤ −7 dB) | ≤ −10 dB (accepted ≤ −7 dB) |
| Radiation efficiency | — | ≥ 50 % (accepted ≥ 35 %) |
| Gain | — | ≥ 5 dBi (accepted ≥ 3.5 dBi) |
| −10 dB bandwidth | not yet defined | ≥ 40 MHz (accepted ≥ 28 MHz) |

L-band figures come from `simulation/cst_lessons_and_lband_plan.md` §2. No equivalent UHF gain/efficiency targets are recorded in the project files.

**UHF band source:** 403–470 MHz is stated in the MHA/CRPF QRs for digital UHF radio sets (June 2025, NSG among the co-signers). Link, verification notes and the NSG 2026 tender list are in [`sources.md`](sources.md).

**L-band caution:** no source gives 1350–1450 MHz (or any other L-band range) as the NSG video link. The NSG body-worn-video tender and the earlier MHA camera QRs describe cellular / Wi-Fi / internet relay, not an L-band RF link. Treat the L-band figures above as placeholders until the intended band is confirmed. See [`sources.md`](sources.md) §3.
