---
type: concept
created: 2026-08-27
updated: 2026-08-27
sources:
  - raw/papers/guldenschuh-2014-secondary-path-irregularities/full-text.md
tags:
  - active-noise-control
  - feedback-anc
  - robust-stability
  - adaptive-filtering
---

# DC-Gain Stability Constraint

The **DC-gain stability constraint** is a time-domain robust-stability check for adaptive feedback ANC, introduced by [[sources/guldenschuh-2014-secondary-path-irregularities|Guldenschuh & de Callafon (2014)]]. It reduces the frequency-domain robust constraint $|W(j\omega)| < 1/U_{\max}(\omega)$ to a single summation of the adaptive filter's coefficients:

$$
\sum_l w_l < \frac{1}{U_{\max}(0)}
$$

requiring only **6 MACs per filter update** — no real-time Fourier transform and no auxiliary noise injection.

## Derivation

1. **Robust IMC constraint**: for additive uncertainty $U(\omega) = |\hat{G} - G_i|$, feedback stability is guaranteed if $|W(j\omega) \cdot U_{\max}(\omega)| < 1$ (a [[robust-stability-constraint|robust stability constraint]]).
2. **Single-bin reduction**: instability is typically caused by a distinct pole at a distinct frequency, so it suffices to check only the frequency bins where $G$ has sharp dynamics. Evaluating one bin costs $O(N)$ (cosine/sine kernel) vs. $O(N \log_2 N)$ for a full transform.
3. **DC-bin reduction**: [[secondary-path-variability|secondary-path irregularities]] (leaks, lifting) act below 300 Hz. With a deliberately coarse frequency resolution — $L = 6$ taps at $f_s = 7350$ Hz gives 1200 Hz per bin — all low-frequency adaptation of $W$ lands in the DC bin, and the check collapses to the plain coefficient sum.

## Detection Principle: The Adaptive Filter as Plant Monitor

Because $W$ performs system identification of $G^{-1}$, any low-frequency drop of $G$ (headphones lifted/leaky) forces $W$ to boost its low-frequency gain — **independently of the excitation spectrum**. A growing DC gain of $W$ therefore signals a secondary-path irregularity before the loop rings. Experimentally, the DC gain always exceeded the $-17.3$ dB threshold ($1/U_{\max}(0)$) before instability occurred, across sinusoidal, narrowband, white, and pink excitations with abrupt path switching.

## Fallback Behavior

On violation, the LMS update is interrupted and $W$ **smoothly converges** (normalized difference update over $M$ samples) to a stable default filter — a scaled Kronecker impulse at $-20$ dB (2.7 dB headroom below the bound). Afterwards, adaptation resumes; if $G$ still deviates, the filter cycles between growth and scale-back rather than diverging.

## Comparison with Alternatives

| Approach | Cost per update | Narrowband NR | Broadband NR |
|----------|-----------------|---------------|--------------|
| DC-gain constraint (6 taps) | 6 MACs | 14 dB (12.5% below MMSE) | matches Rafaely |
| [[constrained-fdlms|Constrained FDLMS]] (Rafaely & Elliott 2000, 12 taps) | ≥ 661 MACs (2×24-pt FFT + IFFT) | 2–5 dB better | matches |
| Online SPM (Zhang et al. 2003) | 3 LMS updates | slightly better than DC-gain | 50–62% worse (auxiliary noise + hard norm constraint) |

## Limitations

- Only applicable at **low frequency resolution** (short filters): a 12-tap filter would require extending the analysis to the 612 Hz bin (~60 MACs), eroding the advantage
- Occasionally **conservative**: the filter switches to the default even when the loop would have remained stable
- Costs ~2 dB narrowband reduction vs. a longer filter

## Related Concepts

- [[concepts/robust-stability-constraint|Robust Stability Constraint]] — the parent frequency-domain condition
- [[concepts/secondary-path-variability|Secondary Path Variability]] — the phenomenon being detected
- [[concepts/constrained-fdlms|Constrained FDLMS]] — the frequency-domain penalty alternative
- [[concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]] — complementary adaptation-stability ingredient
- [[concepts/feedback-anc|Feedback ANC]]
- [[concepts/internal-model-control|Internal Model Control]]

## Related Sources

- [[sources/guldenschuh-2014-secondary-path-irregularities|Guldenschuh & de Callafon 2014: Detection of Secondary-Path Irregularities in ANC Headphones]]
- [[sources/rafaely-2000-constrained-fdlms|Rafaely & Elliott 2000: Constrained FDLMS]] — the full-band comparison baseline
