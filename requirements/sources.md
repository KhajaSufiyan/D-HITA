# Source Register

Primary sources for the frequency and equipment requirements. Read on 2026-09-30 through automated page retrieval, which summarises rather than transcribes: open each PDF and note the section/page numbers before citing in the deck or report.

## 1. UHF band — 403–470 MHz (now sourced)

**Document:** QRs/TDs of Digital Hand-Held UHF Transceiver Set, Digital UHF Base/Mobile Transceivers Set and Digital UHF Repeater Set — Ministry of Home Affairs / CRPF Communication & IT Directorate, June 2025.
**URL:** https://www.mha.gov.in/sites/default/files/2025-06/AppQRsTDsDigiUHF_06062025.pdf

What it says:
- 403–470 MHz ("full band") for all three radio types
- Power classes: 1.4 W hand-held, 20 W mobile/base, 40 W or more repeater
- Approval pages include an NSG signatory alongside CRPF, CISF, ITBP, BSF, SSB, Assam Rifles and DCPW representatives

This replaces the "source not in repo" caveat on the UHF band.

## 2. NSG 2026 procurement (archive listing)

Archive index: https://nsg.gov.in/archive-tender/current-tenders

| Item | Bid ref | Date on archive | Document |
|---|---|---|---|
| Wireless Body Worn Video System | GEM/2026/B/7517372 | 03-06-2026 | https://nsg.gov.in/resources/uploads/TenderManagement/178048996348.pdf |
| Digital UHF Hand Held Radio Sets — 4 W | GEM/2026/B/7540163 | 23-06-2026 | https://nsg.gov.in/resources/uploads/TenderManagement/178220161366.pdf |
| Digital UHF Hand Held Radio Sets — 20 W | GEM/2026/B/7540671 | 23-06-2026 | https://nsg.gov.in/resources/uploads/TenderManagement/178220186760.pdf |
| Digital UHF Repeater Set — 40 W | GEM/2026/B/7540825 | 23-06-2026 | https://nsg.gov.in/resources/uploads/TenderManagement/178220202420.pdf |
| Digital UHF Hand Held Radio Sets — 4 W (re-listed) | GEM/2026/B/7816513 | 10-08-2026 | https://nsg.gov.in/resources/uploads/TenderManagement/178659795126.pdf |
| Digital UHF Hand Held Radio Sets — 20 W (re-listed) | GEM/2026/B/7817167 | 10-08-2026 | https://nsg.gov.in/resources/uploads/TenderManagement/178659814948.pdf |
| Digital UHF Repeater Set — 40 W (re-listed) | GEM/2026/B/7818796 | 10-08-2026 | https://nsg.gov.in/resources/uploads/TenderManagement/178659832414.pdf |

Dates and references are as listed on the archive page; two of the PDFs (video, 20 W) were opened and matched their listings (video: 148 pieces, "as per MHA QRs (V3)"; 20 W: 188 units, "as per MHA QR (V2)"). The other five PDFs were not opened.

## 3. Finding: the video link is not shown to be L-band

- The NSG body-worn-video tender says the camera must relay feeds in real time in online mode and, when there is no **cellular network**, record and store them and relay later or by physical connection to a computer. The accompanying software must feed a central server or incident command post **over the internet**. The document gives no RF band, antenna or L-band requirement, and points to the MHA QRs (V3) for the rest.
- The earlier MHA/CRPF body-worn-camera QRs (for RAF, 6 Jun 2021, https://www.mha.gov.in/sites/default/files/QRs_BodyWornCameraSystems_25062021.PDF) specify "4G/3G + Wi-Fi", IP streaming and a cloud platform, and no L-band or other RF frequency.
- The V3 QRs themselves were not found or read.

**What this means.** The SIH26185 problem statement still asks for L-band, so the requirement stands. But the 1350–1450 MHz "video link" figure now has no source, and the only NSG camera evidence points at cellular/Wi-Fi. Resolve this before spending more simulation time on L-band tuning: ask the SIH mentors / NSG nodal contact which L-band frequency they mean, and look for the MHA BWC QRs (V3).

## 4. Also worth checking

The NSG radio tenders are for 4 W, 20 W and 40 W sets (the QR lists 1.4 W for the hand-held class). A helmet-mounted antenna sits close to the head, so transmit power matters for head exposure and for the "SAR if feasible" item in the project plan. Confirm which power class would actually feed the helmet antenna.
