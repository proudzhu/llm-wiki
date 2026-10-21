---
type: concept
created: 2026-10-21
updated: 2026-10-21
sources:
  - raw/papers/peled-2026-anc-ar-glasses-directional-robustness/full-text.md
tags:
  - active-noise-control
  - virtual-sensing
  - augmented-reality
---

# ANC for AR Glasses

**ANC for AR Glasses** is the application of active noise control to augmented reality glasses, an emerging research area with two defining constraints: (i) there is **no microphone at the wearer's ear**, so the quiet zone can only be served by [[concepts/virtual-sensing|Virtual Sensing]]; and (ii) microphones are fixed on the glasses frame, creating a **causality constraint** — for source directions where the wavefront reaches the ear before the frame reference microphone, the required controller is non-causal and attenuation collapses.

## Geometry and Causality

AR glasses (e.g., the Project Aria platform) provide microphones and loudspeakers around the frame. With the reference and monitor microphones lying in the xy-plane and the monitor placed on the frame above the ear, attenuation is approximately symmetric around the reference–monitor axis angle $\phi_0$, where the relative propagation delay between reference and monitor/virtual microphones is maximal — the most favorable causality condition. When the source azimuth deviates more than $\pm 90°$ from $\phi_0$, the noise reaches the monitor/virtual microphone *before* the reference, requiring a non-causal controller; all algorithms degrade significantly in this region.

## Why Virtual Sensing Is Necessary

[[sources/peled-2026-anc-ar-glasses-directional-robustness|Peled & Rafaely 2026]] compared monitor-based NFxLMS (adaptation from the frame microphone), virtual-based NFxLMS (ground truth, adaptation at the ear), and [[concepts/auxiliary-filter-virtual-sensing|AF-VS]] control in a free-field simulation with Project Aria geometry: the monitor-based controller falls far short of ear-position attenuation, while AF-VS nearly bridges the gap — establishing virtual sensing as a **requirement** rather than an enhancement for AR-glasses ANC.

## Directional Robustness

Because the primary path from a moving noise source changes with direction-of-arrival (see [[concepts/primary-path-variability|Primary Path Variability]]), a virtual sensing filter calibrated at one DOA degrades when the noise arrives from another. Peled & Rafaely's sensitivity analysis shows the auxiliary filter is most robust along the reference–monitor axis, and a finite bank of AFs selected by DOA (5 filters: within 3.7 dB of per-DOA calibration) offers a practical alternative to continuous recalibration.

## Related Work

- [[sources/xiao-2023-spatially-selective-anc|Xiao, Xu & Zhao 2023]] demonstrated directional noise reduction in an AR-glasses simulation but relied on binaural error microphones near the ears, which may not be available in practice.
- Head-mounted ANC studies (Miyake 2023; Miyazaki & Kajikawa 2015) use error microphones close to the ear or target non-AR scenarios, differing from feasible AR-glasses designs.

## Related Concepts

- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/auxiliary-filter-virtual-sensing|Auxiliary Filter Virtual Sensing (AF-VS)]]
- [[concepts/primary-path-variability|Primary Path Variability]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/auditory-augmented-reality|Auditory Augmented Reality]]

## Related Sources

- [[sources/peled-2026-anc-ar-glasses-directional-robustness|Peled & Rafaely 2026: ANC for AR Glasses with Directional Robustness]]
- [[sources/xiao-2023-spatially-selective-anc|Xiao, Xu & Zhao 2023: Spatially Selective ANC]]
