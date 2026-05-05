---
type: concept
created: 2026-04-11
updated: 2026-04-11
sources:
tags:
- active-noise-control
- adaptive-filtering
- efficiency
- subband
---

# Subband ANC

**Subband ANC** decomposes the reference and error signals into multiple frequency subbands using a filter bank, processes each subband independently with its own adaptive filter, and then recombines the outputs. It is described in [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] as one of the "special algorithms" for ANC.

## Motivation

Standard time-domain [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] treats all frequencies equally, but:
- **Noise spectra are non-uniform**: Different frequency bands have different characteristics
- **Secondary paths vary by frequency**: $\hat{S}(z)$ has different phase/magnitude responses across frequency
- **Convergence rate varies by frequency**: High-energy bands converge fast, low-energy bands converge slowly — the step size is limited by the highest-energy band

Subband processing addresses these issues by **optimizing each band independently**.

## Architecture

```
x(n) → Analysis Filter Bank → [Subband 0, Subband 1, ..., Subband K-1]
                                    ↓          ↓                    ↓
                              FxLMS₀    FxLMS₁    ...   FxLMS_{K-1}
                                    ↓          ↓                    ↓
                         Synthesis Filter Bank → y(n) → Secondary Path
```

1. **Analysis filter bank**: Decompose $x(n)$ and $e(n)$ into $K$ subbands
2. **Per-subband FxLMS**: Each subband runs its own adaptive filter with independent step size $\mu_k$
3. **Synthesis filter bank**: Recombine subband outputs into the full-band control signal

## Advantages

| Property | Full-band FxLMS | Subband ANC |
|----------|-----------------|-------------|
| **Convergence** | Limited by worst-case band | Each band optimized independently |
| **Complexity** | $O(L)$ per sample | $O(L/K)$ per subband (decimated) |
| **Numerical stability** | Single step size | Per-band step sizes |
| **Targeted control** | All frequencies treated equally | Can emphasize/de-emphasize specific bands |

## Key Design Choices

### Filter Bank Type
- **Uniform DFT filter bank**: Equal bandwidth, simple implementation
- **Cosine-modulated filter bank**: Better frequency selectivity
- **Wavelet packet**: Non-uniform, matches human auditory perception

### Decimation Factor
Each subband can be **decimated** (downsampled) by factor $D$, reducing computation by $D \times$:
- Narrower subbands → slower signal dynamics → larger decimation possible
- Trade-off: aliasing from imperfect filter bank reconstruction

### Step Size Allocation
$$\mu_k = \frac{\alpha}{P_k + \beta}$$
where $P_k$ is the power in subband $k$, $\alpha$ is a global scaling factor, and $\beta$ prevents division by zero.

## Disadvantages

- **Aliasing**: Imperfect reconstruction filter banks introduce aliasing between subbands
- **Delay**: Analysis/synthesis filter banks add latency
- **Complexity overhead**: Filter bank implementation adds computation
- **Tuning**: More parameters to optimize (number of subbands, decimation factor, per-band step sizes)

## Related

- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]] — The time-domain baseline
- [[frequency-domain-anc|Frequency-Domain ANC]] — Alternative efficiency approach: FFT-based block processing
- [[multi-channel-anc|Multi-Channel ANC]] — Subband processing is even more valuable in multi-channel (complexity reduction compounds)
- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section VII-D: Subband ANC

## Sources

- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]] — Section VII-D
## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[frequency-domain-anc|Frequency-Domain ANC]]
- [[multi-channel-anc|Multi-Channel ANC]]

## Related Sources

- [[../sources/kuo-1999-active-noise-control-tutorial-review|Kuo 1999: Active Noise Control Tutorial Review]]
