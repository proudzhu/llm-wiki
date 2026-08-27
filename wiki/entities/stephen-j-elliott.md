---
type: entity
created: 2026-04-12
updated: 2026-08-27
tags:
- acoustics
- researcher
sources:
  - raw/papers/rafaely-2000-constrained-fdlms/full-text.md
---
# Stephen J. Elliott

**Stephen J. Elliott** is a Professor of Signal Processing and Control at the Institute of Sound and Vibration Research (ISVR), University of Southampton. He is one of the most prominent researchers in the field of **Active Noise Control (ANC)** and active structural control.

## Contributions to ANC

Professor Elliott has published hundreds of papers and several definitive textbooks on active control. His research has laid the foundational theory for many ANC architectures used today:

### 1. Adaptive Feedback ANC
He was a pioneer in developing the **Internal Model Control (IMC)** framework for adaptive feedback systems, enabling ANC in devices like headphones where a reference signal is not available (Rafaely & Elliott 1996).

### 2. Multi-channel ANC
He developed the theoretical framework for multi-channel feedforward systems, analyzing the complexity and convergence of MIMO controllers for large enclosures.

### 3. Optimal Control Theory
His work bridged the gap between signal processing (LMS/FxLMS) and modern control theory (MVC, $H_\infty$), proving the optimality and stability conditions for various active control structures.

- Co-authored "A computationally efficient frequency-domain LMS algorithm with constraints on the adaptive filter" (IEEE Trans. Signal Processing 2000) — with [[boaz-rafaely|Boaz Rafaely]], introduced [[concepts/constrained-fdlms|constrained FDLMS]], a penalty-function extension of frequency-domain LMS supporting magnitude, output-power, and robust-stability constraints in real time — [[sources/rafaely-2000-constrained-fdlms|Rafaely & Elliott 2000]]

## Academic Influence

Professor Elliott has supervised numerous PhD students who have gone on to become leaders in the field, including:
- **[[marek-pawelczyk|Marek Pawełczyk]]**
- **[[boaz-rafaely|Boaz Rafaely]]**
- **[[piero-iared-rivera-benois|Piero Iared Rivera Benois]]** (as a co-supervisor/collaborator)

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/internal-model-control|Internal Model Control]]
- [[concepts/minimum-variance-control|Minimum Variance Control]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]

## Related Sources

- [[sources/rafaely-2000-constrained-fdlms|Rafaely & Elliott 2000: Computationally Efficient Frequency-Domain LMS with Constraints]]
- [[sources/pawelczyk-1997-anc-feedback-fixed-adaptive|Pawelczyk 1997: ANC Feedback Fixed/Adaptive]]
- [[sources/benois-2020-hybrid-pseudo-cascaded-anc-headphones|Benois 2020: Hybrid and Pseudo-Cascaded ANC for Headphones]]
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] (References his work extensively)

## Related Entities

- [[boaz-rafaely|Boaz Rafaely]]
- [[marek-pawelczyk|Marek Pawełczyk]]
- [[piero-iared-rivera-benois|Piero Iared Rivera Benois]]
