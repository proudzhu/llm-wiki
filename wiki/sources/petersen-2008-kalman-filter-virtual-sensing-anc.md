---
type: source
created: 2026-04-18
updated: 2026-04-18
sources:
- zotero://select/items/0_WX2XSXDA
tags:
- active-noise-control
- kalman-filter
- state-space
- virtual-sensing
---

# Petersen 2008: A Kalman filter approach to virtual sensing for ANC

**Title**: A Kalman filter approach to virtual sensing for active noise control
**Authors**: Dick Petersen, Rufus Fraanje, Ben Cazzolato, Anthony Zander, Colin Hansen
**Journal**: Mechanical Systems and Signal Processing
**Date**: 2008-02-01

## Summary

Local active noise control systems aim to produce zones of quiet at desired locations, such as the ears of an observer. However, the resulting zones of quiet are usually centered at the physical error sensors and are often too small to extend to the observer's ears.

This paper proposes a **[[concepts/kalman-filter|Kalman Filter]]** approach to overcome this limitation. By modeling the acoustic system in a **[[concepts/state-space-model|state-space]]** framework, the Kalman filter provides an optimal estimate of the error signals at "virtual" locations remote from the physical sensors.

## Key Technical Details

1.  **State-Space Modeling**: The acoustic path and primary noise sources are modeled using state-space equations.
2.  **Optimal Estimation**: The Kalman filter uses available physical microphone measurements and control signals to minimize the mean square estimation error at the virtual microphone location.
3.  **Robustness**: Unlike the deterministic [[concepts/virtual-sensing|Remote Microphone Technique (RMT)]], the Kalman filter approach explicitly accounts for measurement noise and stochastic primary fields.
4.  **Local ZoQ**: The method allows for the projection of the Zone of Quiet (ZoQ) exactly to the listener's ear without placing hardware there.

## Related Concepts
- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/kalman-filter|Kalman Filter]]
- [[concepts/state-space-model|State-Space Model]]

## Related Synthesis
- [[synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]
- [[synthesis/kalman-filter-theory-and-application|Kalman Filter Theory and Application]]
