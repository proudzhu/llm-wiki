---
type: concept
created: 2026-04-29
updated: 2026-04-29
tags:
  - virtual-sensing
  - anc
  - remote-microphone
---

# Remote Microphone Technique

The **Remote Microphone Technique (RMT)** is a virtual sensing method that estimates the error signal at a target (virtual) location using a fixed compensation filter derived from the transfer functions between the physical error microphone and the virtual target point.

## Formulation

The compensation filter $C(z)$ is derived from:

$$C(z) = \frac{G_{ev}(z)}{G_{ee}(z)}$$

where $G_{ev}(z)$ is the transfer function from control source to virtual location, and $G_{ee}(z)$ is the transfer function from control source to physical error microphone.

## Limitations

- Fixed compensation filter assumes stationary acoustic paths
- Sensitive to changes in noise characteristics and acoustic environment
- Requires accurate estimation of transfer functions

## Related Concepts

- [[../concepts/virtual-sensing|Virtual Sensing]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/secondary-path-modeling|Secondary Path Modeling]]

## Related Sources

- [[../sources/a-review-of-virtual-sensing-algorithms-for-active-|Moreau 2008: Review of Virtual Sensing Algorithms for ANC]]
- [[../sources/toyooka-2026-hybrid-anc-remote-sensing|Toyooka 2026: Hybrid ANC with Dual Compensation]]
