---
type: concept
created: 2026-04-17
sources:
- zotero://select/items/0_LJDPCZ9G
- zotero://select/items/0_WY4S7C6Z
- zotero://select/items/0_WX2XSXDA
tags:
- active-noise-control
- control-theory
- signal-processing
updated: 2026-04-18
---
# Virtual Sensing

**Virtual Sensing** (or Virtual Microphone technology) is a method in **[[active-noise-control|Active Noise Control]]** and structural monitoring where the acoustic or vibration signal is estimated at a physical location where it is impossible or impractical to place a physical sensor.

For a detailed analysis of the algorithmic development, see **[[synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]**.

## Motivation in ANC
In many applications (e.g., headphones, vehicle headrests), the "quiet zone" needs to be at the listener's ear, but the physical error microphone must be placed elsewhere for comfort or design reasons. Virtual sensing allows the system to project the silence zone to the actual ear canal.

## Common Algorithms
- **Remote Microphone Technique (RMT)**: Uses an auxiliary microphone during a training phase to learn the relationship between the physical error mic and the virtual location.
- **Virtual Microphone Arrangement (VMA)**: Uses a physical array to interpolate the pressure at a virtual point.
- **Observer-Based Estimation**: Uses a **[[state-space-model|State-Space Model]]** and **[[kalman-filter|Kalman Filter]]** to estimate the virtual state based on available physical measurements.
- **Neural Observation Filters**: Uses deep learning (e.g., Obs-TasNet) to estimate filters online for dynamic environments.

## Challenges
- **Spatial Aliasing**: The distance between physical and virtual sensors must be small relative to the wavelength of the noise being cancelled.
- **Plant Changes**: The transfer function between the physical and virtual locations may change if the listener moves their head.
- **Latency**: The estimation process adds computational delay to the control loop.

## Related Concepts
- [[active-noise-control|Active Noise Control]]
- [[kalman-filter|Kalman Filter]]
- [[state-space-model|State-Space Model]]
- [[secondary-path-modeling|Secondary Path Modeling]]
- [[ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]
- [[deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Synthesis
- [[synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]
- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]

## Related Sources
- [[sources/a-review-of-virtual-sensing-algorithms-for-active-|A Review of Virtual Sensing Algorithms for ANC]]: Systematic overview and comparison of VS algorithms.
- [[sources/holzmueller-2026-obs-tasnet-virtual-sensing|Holzmüller 2026: Obs-TasNet for Virtual Sensing]]: Deep learning approach to VS.
- [[sources/petersen-2008-kalman-filter-virtual-sensing-anc|Petersen 2008: Kalman Filter for Virtual Sensing]]: State-space observer approach.
- [[sources/wang-2024-computation-efficient-virtual-sensing|Wang 2024: Computation-Efficient Virtual Sensing with MCALMS]]: Multi-channel VS optimization using MCALMS algorithm.

