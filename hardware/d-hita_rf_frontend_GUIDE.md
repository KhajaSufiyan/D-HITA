# D-HITA RF Frontend — Build Guide (R2, Passive Dual-Feed, Kapton Flex)

**Revision R2 — 28 Sep 2026.** Supersedes the active-switch revision (SKY13350 + ESP32-C3 + Li-Po on Rogers 4350B in an enclosure). That design is **rejected** — do not build it. There is no MCU, no switch, no battery, no firmware, and no enclosure in this build.

**What this is:** two independent probe-fed patches on one Kapton flex sheet. UHF (460 MHz) and L-band (1364 MHz) each have their own feed, their own matching pad site, and their own U.FL output. Both bands are live simultaneously. The board is entirely passive.

---

## Tools
- Flex-capable PCB fabrication (outsourced — see Assumptions)
- Soldering iron with fine tip, or hot air station
- Solder paste (SAC305, or low-temp Bi58Sn42 — preferred for polyimide, lower thermal stress)
- Multimeter with fine probes
- Tweezers (anti-static)
- ESD workstation mat
- **Vector Network Analyzer (VNA)** — mandatory, not optional. The matching pad values are determined on the VNA, not in advance.
- 0402 trim kit: assorted Murata LQW15A inductors and GRM1555 / TDK C1005 C0G capacitors
- Isopropyl alcohol (99%) and lint-free swabs
- Laser cutter or precision knife for coverlay trimming

**No longer needed:** USB-C programming cable, ESP-IDF/Arduino toolchain, solder stencil for Rogers, Li-Po handling equipment.

## Assumptions
- Access to a **flex-PCB** fabrication service (polyimide, not rigid FR-4 or Rogers). This is the key sourcing dependency.
- The 3.5 mm substrate thickness is realised as a thin Kapton patch/feed layer over a flexible foam or silicone spacer — **solid 3.5 mm Kapton laminate is not a stock product.** This remains an open fabrication item and must be settled with the fab house before release.
- Basic SMD hand-soldering skill. Only 0402 passives and two U.FL connectors are hand-placed; there are no QFN or fine-pitch ICs in this build.
- VNA access for post-fabrication matching trim.

---

## 1. Fabrication

### 1.1 Release the flex stackup to the fab house
**Prepare and send the Kapton flex artwork.**

1. Confirm the stackup with the fab house: copper on polyimide top layer (patches + feed routing), 3.5 mm dielectric separation to a continuous copper ground plane. Discuss how they will achieve 3.5 mm — laminated foam spacer, silicone, or stacked polyimide.
2. Board outline: 250 × 445 mm (X −125 to +125, Y −125 to +320).
3. Top layer: UHF patch 170.4 × 148.8 mm centred at Y = 0; L-band patch 55.1 × 74 mm centred at Y = 250. Edge-to-edge separation ~65 mm.
4. Bottom layer: continuous copper ground plane across the full board outline. This is also the head-isolation shield — no cutouts, no voids under the patches.
5. Plated vias: one at (X = 30, Y = 0) for the UHF probe, one at (X = 16, Y = 250) for the L-band probe.
6. Feed routing: 50 Ω microstrip calculated for εr = 3.5 at h = 3.5 mm. Ask the fab house to confirm the trace width against their actual stackup rather than trusting a calculator value.

> **Tip:** The 65 mm patch separation and the 3.5 mm dielectric thickness are the two dimensions that must not be "optimised" by the fab house for panel efficiency. Separation controls inter-band isolation (currently −50 to −90 dB); thickness controls radiation efficiency, and thinning it was what dropped the UHF patch to 14% efficiency in earlier simulation runs.

### 1.2 Inspect the incoming boards
**Verify what arrived matches what was ordered.**

1. Measure both patch dimensions with calipers against the drawing. A few tenths of a millimetre is fine; several millimetres will shift resonance.
2. Measure the actual dielectric thickness at several points. Report any variation over ±0.3 mm — it will change both resonances.
3. Continuity-check the ground plane across the full board. Any break under a patch ruins that patch.
4. Check each probe via for continuity from top pad to ground plane, and confirm it is *not* shorted to the patch copper.
5. Clean both faces with 99% IPA and a lint-free wipe.

> **Tip:** Do this before soldering anything. A board with the wrong dielectric thickness is not worth populating.

### 1.3 Trim the polyimide coverlay
**Cut the coverlay to cover feed routing only.**

1. Cut the 0.025 mm coverlay to cover the two feed-routing corridors, the two matching pad sites, and the U.FL footprints — with cutouts at the connector openings.
2. **Do not cut a piece that covers either radiating patch.** Dielectric loading over a patch detunes it. The patch areas stay bare.
3. Use low power / high speed on a laser cutter to avoid charring, or cut by hand with a fresh blade against a straightedge.
4. Clean any carbonised debris from cut edges.

> **Tip:** If in doubt, make the coverlay smaller. There is no downside to leaving more copper exposed on the feed side; there is a real downside to covering a patch.

---

## 2. Assembly

### 2.1 Populate the matching pad sites — initial configuration
**Fit the 0 Ω jumpers and leave the shunt positions empty.**

1. On both the UHF and L-band matching pad sites, solder a **0 Ω 0402 jumper into the series position**.
2. Leave **both shunt-to-ground positions unpopulated (DNP)** on each site.
3. This gives a straight-through feed, which is the correct starting point — simulation already shows S11 of −9.6 dB (UHF) and −10.15 dB (L-band) without any matching components.
4. Clean flux residue with IPA. Flux left on RF traces on a low-loss substrate causes real dielectric loading.

> **Tip:** The shunt positions exist so the board can be trimmed after measurement. Populating them now with guessed values will make the match worse, not better.

### 2.2 Solder the two U.FL connectors
**Mount UHF Radio U.FL and L-Band Video U.FL.**

1. Place the UHF U.FL at the end of the UHF feed routing (~8 mm past the matching pad site), and the L-band U.FL at the end of the L-band routing (~6 mm past its matching pad).
2. Hand-solder or hot-air reflow. If using reflow on polyimide, prefer a low-temperature Bi58Sn42 profile over SAC305's 245–250 °C peak — polyimide tolerates it, but there is no reason to thermally stress a flex board unnecessarily.
3. Ensure the connector shell ground is properly bonded to the ground plane through the via stitching.
4. Inspect under magnification for bridging between signal pin and shell.
5. Clean all flux with IPA and a lint-free swab.

> **Tip:** U.FL is the most mechanically fragile point on this assembly. Plan strain relief for both pigtails within 20 mm of the connector before the board goes anywhere near a helmet.

### 2.3 Laminate the coverlay
**Apply the trimmed coverlay over the feed regions.**

1. Clean the feed-side surface with IPA.
2. Align the coverlay over the feed corridors and matching sites, with connector cutouts clear.
3. Laminate with even pressure; cure under low heat per the Pyralux datasheet.
4. Confirm again that no coverlay overhangs either radiating patch.

### 2.4 Attach the coax pigtails
**Mate the U.FL pigtails and secure them.**

1. Mate the UHF pigtail to the UHF Radio U.FL and the L-band pigtail to the L-Band Video U.FL. Press vertically — U.FL plugs do not tolerate angled insertion.
2. Route both pigtails along the intended helmet-shell path and secure with non-metallic cable clips.
3. Terminate both at their bulkhead connectors. **Bulkhead connector type (SMA vs TNC) is still [TO BE CLARIFIED]** — confirm against the NSG radio and body-worn video connector interfaces before committing.

---

## 3. Bring-up (VNA)

### 3.1 Measure UHF S11
**Baseline the UHF port against simulation.**

1. Calibrate the VNA over 300–700 MHz at the end of the UHF pigtail (calibrate at the pigtail end, not the connector — the cable is part of the system).
2. Sweep and record the S11 curve.
3. **Expected from simulation:** resonance at ~460 MHz, S11 ≈ −9.6 dB.
4. Record the actual resonant frequency and depth. Expect a shift — the physical substrate realisation differs from the simulated ideal.
5. Measure the −10 dB bandwidth. **This value has never been measured or simulated for UHF** and is the project's one outstanding performance unknown.

> **Tip:** 460 MHz sits inside the confirmed NSG/MHA UHF band of 403–470 MHz, but close to its top edge. If the physical board shifts upward, it leaves the band. If it shifts downward, it moves toward the band centre, which is better. Note which way it went.

### 3.2 Measure L-band S11
**Baseline the L-band port.**

1. Recalibrate over 1200–1600 MHz at the end of the L-band pigtail.
2. Sweep and record.
3. **Expected from simulation:** resonance at ~1364 MHz, S11 ≈ −10.15 dB, −10 dB bandwidth ~35 MHz.
4. Record actual resonance, depth and bandwidth.

### 3.3 Measure port-to-port isolation (S21)
**Confirm the two patches are not coupling badly in hardware.**

1. Connect port 1 to the UHF pigtail and port 2 to the L-band pigtail.
2. Sweep 300–1700 MHz and record S21.
3. **Expected from simulation:** −50 to −90 dB across most of the range, with a worst case of −30 to −40 dB in the 900–1200 MHz dead zone between bands.
4. If measured isolation is worse than −25 dB anywhere in either operating band, stop and investigate before proceeding — it usually means a ground plane defect rather than a spacing problem.

### 3.4 Trim the matching networks
**Populate shunt components only where measurement says to.**

1. Work one band at a time. Do not trim both simultaneously — you will not know which change caused which effect.
2. If S11 at the target frequency is already ≤ −10 dB, **leave the 0 Ω jumper alone and populate nothing.** A good match needs no matching network.
3. If S11 is inadequate, use the Smith chart to determine whether a shunt capacitor or shunt inductor is needed, and fit a single 0402 component into one shunt position.
4. Re-measure after every single component change. Record the value fitted and the resulting S11.
5. If the series position needs to become reactive, replace the 0 Ω jumper with the required series component.
6. Keep a written log of every trial value — this log is the fabrication record for V2.

> **Tip:** Resist the temptation to chase the last decibel. The project acceptance rule is target or within a 30% buffer. S11 of −7 dB clears the buffer on both bands.

---

## 4. Integration and Validation

### 4.1 Mount to the helmet
**External side-mounted configuration (Design 3).**

1. Mount the flex assembly on the *outside* of the helmet shell — no cutting into the shell, no internal cavity access.
2. Ground plane / shield faces the helmet and head; patches face outward.
3. Use non-metallic adhesive. Metallic fasteners through the board will corrupt the ground plane and detune both bands.
4. Route both coax pigtails cleanly along the shell with strain relief at the board end.

### 4.2 Re-measure on the helmet
**The helmet and head change the antenna. Measure again.**

1. Repeat 3.1, 3.2 and 3.3 with the assembly mounted on the helmet, and again with the helmet worn or on a head phantom.
2. Expect resonance to shift and efficiency to drop — the flat, free-space numbers are not the on-helmet numbers.
3. Record both conditions. The simulation-vs-measurement comparison across flat / curved / on-head is the core evidence deliverable for SIH26185.

> **Tip:** Conformal (curved) simulation and the helmet + head model have **not yet been run**. The flat design is complete and passes on both bands; curvature and head loading are the next simulation phase and the measurements here are what validate them.

### 4.3 Radiation measurement (if lab access allows)
1. Measure gain and radiation pattern for both bands if an anechoic chamber or suitable range is available.
2. **Expected from simulation:** UHF gain 6.84 dBi, radiation efficiency ~74%; L-band gain 7.39 dBi, radiation efficiency ~92%.
3. Confirm the pattern favours upward/outward radiation with reduced head-directed energy — this is a direct SIH26185 problem-statement requirement.

---

## Known open items
- Exact NSG L-band video link frequency **[TO BE CLARIFIED]** — 1350–1450 MHz is a working assumption
- 3.5 mm flexible substrate realisation (Kapton over foam/silicone spacer) — open fabrication item
- Ruggedized bulkhead connector selection, SMA vs TNC **[TO BE CLARIFIED]**
- RF shield material and exact geometry **[TO BE CLARIFIED]**
- Helmet model, shell material, approved mounting method **[TO BE CLARIFIED]**
- UHF −10 dB bandwidth — never measured, carried as known debt
- Conformal and helmet + head simulation — not yet run
