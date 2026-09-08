---
type: entity
created: 2026-05-23
updated: 2026-09-08
tags:
  - researcher
  - active-noise-control
  - hearables
  - spatially-selective-anc
  - signal-processing
---

# Tong Xiao

**Affiliation**: Department of Medical Physics and Acoustics and Cluster of Excellence "Hearing4all.connects", Carl von Ossietzky Universität Oldenburg, Germany
**Affiliation (2023)**: Centre for Audio, Acoustics and Vibration, University of Technology Sydney, Australia (work conducted during internship at Facebook Reality Labs Research, Redmond, WA, USA)
**Role**: Researcher
**Research Focus**: Spatially selective active noise control (SSANC) for hearables, soft-constrained ANC formulations, and robust controller design under secondary path variations.

## Key Contributions

- Proposed the spatially selective ANC system with a Frost-type ReIR spatial constraint on the hybrid ANC cost function, physically preserving the desired sound instead of reconstructing it — demonstrated on a six-microphone AR-glasses array (J. Acoust. Soc. Am. 2023) — [[sources/xiao-2023-spatially-selective-anc|Xiao 2023]]
- Soft-constrained spatially selective ANC formulation that balances noise reduction with speech preservation via relative impulse responses (ReIRs)
- Robust extension of soft-constrained SSANC that averages the cost over a measured set of secondary paths to handle plant variability without online identification
- Real-time validation of SSANC algorithms on a dSPACE SCALEXIO + FPGA platform with closed-fitting KEMAR hearables

## Related Sources

- [[sources/xiao-2023-spatially-selective-anc|Xiao 2023: Spatially Selective Active Noise Control Systems]]
- [[sources/xiao-2026-robust-spatially-selective-anc|Xiao 2026: Robust Soft-Constrained SSANC for Hearables]]

## Related Concepts

- [[concepts/spatially-selective-anc|Spatially Selective ANC]]
- [[concepts/soft-constrained-anc|Soft-Constrained ANC]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/robust-control|Robust Control]]

## Related Entities

- [[entities/simon-doclo|Simon Doclo]] — Supervisor/co-author
- [[entities/reinhild-roden|Reinhild Roden]] — Co-author
- [[entities/matthias-blau|Matthias Blau]] — Co-author
