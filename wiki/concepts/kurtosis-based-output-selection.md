---
type: concept
created: 2026-10-03
updated: 2026-10-03
sources:
  - raw/papers/low-2004-hybrid-bss-anc/full-text.txt
tags:
  - higher-order-statistics
  - blind-source-separation
  - speech-enhancement
  - signal-processing
---

# Kurtosis-Based Output Selection

**Kurtosis-based output selection** is the higher-order-statistical test proposed by [[sources/low-2004-hybrid-bss-anc|Low & Nordholm 2004]] to identify the speech-dominant output among the $L$ outputs of an $L$-microphone [[concepts/blind-source-separation|blind source separation]] stage. BSS recovers sources up to an unknown ordering, so which output contains the target is a priori unknown; the kurtosis (fourth-order statistic) resolves this without any training or source model beyond a distributional argument.

## Rationale

- The kurtosis of a Gaussian distribution is zero; a **supergaussian** distribution has positive kurtosis.
- By the Central Limit Theorem, the sum of several distributions tends toward Gaussian — spatially **diffuse interference** therefore tends toward a Gaussian-like distribution.
- **Speech** has a Laplacian distribution, which is supergaussian and thus has positive kurtosis.

Hence the BSS output with the **highest kurtosis** is labelled speech-dominant; the remaining $L-1$ outputs serve as interference references (e.g., for the ANC stage of [[concepts/hybrid-bss-anc-speech-enhancement|hybrid BSS-ANC speech enhancement]]).

## Formulation

For complex subband signals, the kurtosis of the $l$th BSS output is averaged over the $M$ subbands:

$$\xi_l = \frac{1}{M}\sum_{m=0}^{M-1} \frac{E[|y_l^{(m)}(k)|^4] - 2E^2[|y_l^{(m)}(k)|^2] - |E^2[(y_l^{(m)}(k))^2]|}{\sigma_{y_l}^{4(m)}(k)}$$

where $E[\cdot]$ is expectation and $\sigma_{y_l}^{2(m)}$ the variance of $y_l^{(m)}(k)$. The output with the highest $\xi_l$ becomes $y_{\mathrm{speech}}^{(m)}(k)$; the others become $y_{l,\mathrm{ref}}^{(m)}(k)$, $l = 1, \dots, L-1$.

## Relation to Other Approaches

- In contrast to post-hoc [[concepts/permutation-alignment|permutation alignment]] (which aligns frequency bins to a consistent source order), kurtosis-based selection side-steps per-bin alignment concerns by classifying whole outputs statistically — appropriate when only the target needs to be recovered (extraction), not all sources.
- It is a purely statistical (blind) discriminator: no voice activity detection, DOA estimate, or trained model is required, consistent with the geometry-free design of the hybrid BSS-ANC system.

## Related Concepts

- [[concepts/hybrid-bss-anc-speech-enhancement|Hybrid BSS-ANC Speech Enhancement]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/low-2004-hybrid-bss-anc|Low & Nordholm 2004: A Hybrid Speech Enhancement System Employing Blind Source Separation and Adaptive Noise Cancellation]]
