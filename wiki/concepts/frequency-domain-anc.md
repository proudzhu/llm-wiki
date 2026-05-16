---
type: concept
created: 2026-04-11
updated: 2026-04-11
sources:
tags:
- active-noise-control
- adaptive-filtering
- efficiency
- frequency-domain
---

# Frequency-Domain ANC

**Frequency-Domain ANC** implements the adaptive filtering algorithm in the frequency domain using FFT-based block processing, rather than sample-by-sample time-domain processing. It is one of the "special algorithms" described in [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]].

## Motivation

The time-domain [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] requires $O(L)$ multiplications per sample for a filter of length $L$. When $L$ is large (long secondary paths, wideband noise), this becomes computationally prohibitive.

By transforming to the frequency domain using **overlap-save** or **overlap-add** block convolution, the complexity is reduced to approximately $O(\frac{L}{B} \log_2 L)$ per sample, where $B$ is the block size.

## Algorithm

### Block FxLMS (BFXLMS)

1. **Buffer** $B$ samples of the reference signal $x(n)$
2. **FFT** the buffered block: $X(k) = \text{FFT}[x(n)]$
3. **Filter** in frequency domain: $Y(k) = W(k) \cdot X(k)$ (element-wise multiplication)
4. **IFFT** to get the output block: $y(n) = \text{IFFT}[Y(k)]$
5. **Overlap-save** to produce the final output
6. **Update** weights in the frequency domain:

$$W_{m+1}(k) = W_m(k) + \mu \cdot E(k) \cdot X_f^*(k)$$

where $X_f(k)$ is the FFT of the filtered reference signal (passed through $\hat{S}(z)$).

### Partitioned Block FxLMS

For very long filters, a single FFT block may introduce excessive algorithmic delay. **Partitioned Block FxLMS** (PBFXLMS) divides the filter into $P$ shorter partitions, each processed independently:

$$W(k) = [W_0(k), W_1(k), \dots, W_{P-1}(k)]$$

Each partition has its own delay line, and the outputs are summed. This trades a small amount of computation for significantly reduced latency.

## Advantages

| Property | Time-Domain FxLMS | Block FxLMS | Partitioned BFXLMS |
|----------|-------------------|-------------|---------------------|
| **Complexity** | $O(L)$ per sample | $O(\frac{1}{B} L \log_2 L)$ | $O(\frac{1}{B} L \log_2 B)$ |
| **Convergence** | Standard | Similar (may improve with whitening) | Similar |
| **Algorithmic delay** | 1 sample | $B$ samples | $B/P$ per partition |
| **Best for** | Short filters ($L < 128$) | Long filters, non-real-time | Long filters, real-time |

## Disadvantages

- **Algorithmic delay**: Block processing introduces $B$-sample latency, problematic for real-time ANC
- **Circular convolution artifacts**: Requires overlap-save/overlap-add to avoid
- **Gradient constraint**: Frequency-domain weight updates require a gradient constraint (time-domain windowing) to ensure correct convergence
- **Implementation complexity**: More complex than time-domain FxLMS

## Related

- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — The time-domain baseline
- [[subband-anc|Subband ANC]] — Alternative efficiency approach: decompose into subbands instead of full-block FFT
- [[multi-channel-anc|Multi-Channel ANC]] — Frequency-domain processing is even more critical in multi-channel (complexity scales as $O(M \cdot L \cdot N)$)
- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section VII-C: Frequency-Domain ANC

## Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section VII-C
## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[multi-channel-anc|Multi-Channel ANC]]
- [[subband-anc|Subband ANC]]

## Related Sources

- [[sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
