---
type: concept
created: 2026-05-06
updated: 2026-05-06
sources:
  - raw/papers/holzmuller-2026-dtw-secondary-path-anc/full-text.md
tags:
  - signal-processing
  - time-alignment
  - sequence-matching
---

# Dynamic Time Warping

**Dynamic Time Warping (DTW)** is an algorithm for finding an optimal alignment between two temporal sequences that may vary in speed or timing. Originally developed for spoken word recognition (Sakoe & Chiba 1978), it has been applied to impulse response interpolation, acoustic event detection, and [[../concepts/secondary-path-interpolation|Secondary Path Interpolation]] in [[../concepts/active-noise-control|ANC]].

## Overview

Given two sequences $A := \{A_a\}_{a=1}^{N_a}$ and $B := \{B_b\}_{b=1}^{N_b}$, DTW finds a warping path $p := \{p_\ell\}_{\ell=1}^{N_\ell}$ with $p_\ell = (a_\ell, b_\ell)$ that minimizes the total alignment cost.

### Cost Matrix

The local cost between all element pairs forms a cost matrix:

$$C(a, b) = |A_a - B_b|$$

### Optimal Warping Path

The path minimizing total cost:

$$p^* := \arg\min_p \sum_{\ell=1}^{N_\ell} c(A_{a_\ell}, B_{b_\ell})$$

subject to three constraints:

1. **Boundary conditions**: $p_1 = (1,1)$ and $p_{N_\ell} = (N_a, N_b)$
2. **Monotonicity**: $a_\ell \leq a_{\ell+1}$ and $b_\ell \leq b_{\ell+1}$
3. **Continuity**: Allowed step patterns (e.g., classical: $p_{\ell+1} - p_\ell \in \{(1,0), (0,1), (1,1)\}$)

### Computational Complexity

Computed via dynamic programming in $\mathcal{O}(N_a N_b)$ time.

## Warping and De-warping

To warp sequence $B$ onto $A$, matching indices are found:

$$M_{B \to A}(a) = \{b_\ell^* \mid a_\ell^* = a\}$$

Updated indices are extracted via rounded mean:

$$b_a = \text{round}\left(\text{mean}\left(M_{B \to A}(a)\right)\right)$$

The warped sequence is then:

$$B_{B \to A} = \{B_{b_a}\}_{a=1}^{N_a}$$

## Step Patterns

Different continuity conditions and local weightings produce different alignment behaviors:

| Pattern | Characteristic | Best For |
|---------|---------------|----------|
| symmetric1 | Classic; emphasizes diagonal steps | Lateral translation (global time offset) |
| symmetricP1/P2 | Sakoe-Chiba slope constraint | Yaw rotation (complex variations) |
| Rabiner-Juang II(b) | Balanced slope weighting | Compromise for both translation and rotation |

## Applications in Acoustics

- **HRIR Interpolation**: DTW-based interpolation of head-related impulse responses exhibits lower phase error than ordinary time-domain interpolation with and without global alignment (Bernhard et al. 2015)
- **BRIR Processing**: Nonlinear alignment of binaural room impulse responses for temporal coherence (Kearney et al. 2009)
- **Reflection Detection**: Identifying individual sound events in room impulse responses (Kelly & Boland 2014)
- **ANC Secondary Path Interpolation**: Aligning secondary path impulse responses before interpolation to preserve phase accuracy across positions (Holzmüller & Sontacchi 2026)

## Comparison with Global Time Alignment

| Aspect | Global Time Alignment | DTW |
|--------|----------------------|-----|
| Alignment type | Single global offset | Sample-by-sample nonlinear |
| Handles reflections | No | Yes |
| Computational cost | Low (cross-correlation) | Higher (dynamic programming + spline) |
| Accuracy for lateral translation | Good | Better |
| Accuracy for contralateral sources | Poor | Limited (two-path problem near 90°) |

## Related Concepts

- [[../concepts/secondary-path-interpolation|Secondary Path Interpolation]]
- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[../concepts/offline-secondary-path-modeling|Offline Secondary-Path Modeling]]

## Related Sources

- [[../sources/holzmuller-2026-dtw-secondary-path-anc|Holzmüller & Sontacchi 2026: DTW for Secondary Path Interpolation in ANC]]
