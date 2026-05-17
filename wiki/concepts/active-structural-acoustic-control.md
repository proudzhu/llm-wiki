---
type: concept
created: 2026-05-17
updated: 2026-05-17
tags:
  - active-noise-control
  - structural-acoustics
  - vibration-control
---

# Active Structural Acoustic Control (ASAC)

## Overview

**Active Structural Acoustic Control (ASAC)** reduces radiated noise from a structure by controlling the vibration of its casing or panels, rather than canceling the sound in the acoustic field. It is a form of global noise control that addresses noise at its structural source.

## Motivation

Direct acoustic ANC (canceling sound in air) creates localized quiet zones. ASAC reduces the vibration of radiating surfaces (e.g., vehicle panels, aircraft fuselages, machinery casings), thereby reducing noise throughout the surrounding space.

## Key Techniques

- **Multi-channel FxLMS**: Used for controlling multiple structural modes simultaneously
- **Piezoelectric actuators**: Bonded to structures for precise vibration control
- **PVDF sensors**: Polyvinylidene fluoride film sensors for error measurement
- **Iterative learning control (ILC)**: For repetitive impact noises (e.g., mechanical presses)
- **Distributed switched-error FxLMS**: For active casings with multiple error sensors

## Applications

- **Aircraft**: Fuselage vibration control for cabin noise reduction
- **Vehicles**: Panel vibration control for interior quietness
- **Helicopters**: Gearbox noise and vibration control
- **Double panel systems**: Noise transmission through double walls

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/active-vibration-control|Active Vibration Control]]
- [[concepts/multi-channel-anc|Multi-channel ANC]]

## Related Sources

- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC — Part I: Linear Systems]]
