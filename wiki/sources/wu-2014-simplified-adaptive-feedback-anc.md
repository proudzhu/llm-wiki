---
type: source
created: 2026-04-10
updated: 2026-04-10
sources:
tags:
- active-noise-control
- adaptive-feedback
- filtered-x-lms-algorithm
- signal-processing
aliases:
- 'Wu 2014: Simplified Adaptive Feedback ANC'
---

# A Simplified Adaptive Feedback Active Noise Control System

**Authors**: [[../entities/lifu-wu|Lifu Wu]], [[../entities/xiaojun-qiu|Xiaojun Qiu]], [[../entities/yecai-guo|Yecai Guo]]
**Published**: 2014, Applied Acoustics, Vol. 81, pp. 40–46
**DOI**: [10.1016/j.apacoust.2014.02.006](http://dx.doi.org/10.1016/j.apacoust.2014.02.006)
**📎 Zotero**: [zotero://select/items/0_IUCZFYQX](zotero://select/items/0_IUCZFYQX) |

## Summary

Proposes a **Simplified Adaptive Feedback (SimpAFB)** ANC system that uses the error signal directly as the reference signal, eliminating the need for the convolution operation required in the conventional IMC-based system. The key insight: in practical ANC systems, perfect noise cancellation is impossible, so the error signal always contains some portion of the primary noise — making it a viable reference signal. The system uses a **leaky FxLMS** algorithm to maintain stability.

## Key Takeaways

1. **The simplification**: Instead of regenerating the reference signal via IMC structure (error signal + secondary signal filtered through estimated secondary path), the SimpAFB system uses the error signal directly: `X_sa(z) = E(z)`. This eliminates the expensive convolution operation.

2. **Why it works** — three justifications:
   - Practical feedback ANC systems only achieve limited attenuation (~10 dB), so the error signal always contains primary noise components
   - During initial adaptation, noise reduction is small, so the difference between error signal and primary noise is negligible
   - Imperfect secondary path estimation means the IMC system's reference signal quality is similar to the SimpAFB system's

3. **Leaky FxLMS is essential**: The standard FxLMS algorithm can cause the SimpAFB system to become divergent. The leaky FxLMS limits the adaptive filter gain, improving feedback loop stability — at the cost of introducing bias into the convergent filter.

4. **Stability analysis**: The SimpAFB stability condition is `|∠S(e^jω) - ∠[(1-S(e^jω)W_sa(e^jω))] - ∠Ŝ(e^jω)| < π/2`. This is **worse** than the IMC system's condition because the `∠[1-S(e^jω)W_sa(e^jω)]` term always exists even with perfect secondary path estimation.

5. **Performance comparison**:
   - With perfect secondary path estimation: SimpAFB achieves ~10 dB vs IMC's ~15 dB (5 dB gap)
   - With imperfect estimation (realistic): gap narrows to ~2 dB
   - Both significantly outperform non-adaptive systems in adaptability

6. **Experimental validation**: Tested in a 200 cm duct with DSP (TMS320C6747, 16 kHz sample rate). Results:
   - 250–300 Hz narrow band noise: ~10 dB reduction
   - 250–350 Hz narrow band noise: ~7 dB reduction (wider bandwidth = less predictable = worse performance)

## System Comparison

| System | Performance | Advantages | Weaknesses |
|--------|------------|------------|------------|
| **SimpAFB** (proposed) | Good | Adaptive, low computation, easy implementation | Potential weak stability, potential low noise reduction |
| **IMC-based** | Best | Adaptive, good stability and noise reduction | High computation, can't directly use FxLMS ANC controllers |
| **Non-adaptive** | Moderate | Low cost, simple structure | Non-adaptive, weak stability, complex design |

## Key Equations

- **SimpAFB closed-loop transfer function**: `H_sa(z) = E(z)/D(z) = 1 / [1 - S(z)W_sa(z)]`
- **IMC reference signal synthesis**: `X(z) = E(z) - Ŝ(z)Y(z) = D(z) + [S(z) - Ŝ(z)]Y(z)`
- **SimpAFB reference signal**: `X_sa(z) = E(z) = D(z) + S(z)Y(z)`

## Related Concepts

- [[../concepts/active-noise-control|Active Noise Control]]
- [[../concepts/adaptive-feedback-control|Adaptive Feedback Control]]
- [[../concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[../concepts/internal-model-control|Internal Model Control]]
- [[../concepts/leaky-fxlms-algorithm|Leaky FxLMS Algorithm]]

## Related Entities

- [[../entities/lifu-wu|Lifu Wu]] — First author, Nanjing University of Information Science and Technology
- [[../entities/xiaojun-qiu|Xiaojun Qiu]] — Corresponding author, Nanjing University
- [[../entities/yecai-guo|Yecai Guo]] — Co-author, Nanjing University of Information Science and Technology

## Related Synthesis
