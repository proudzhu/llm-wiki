---
type: concept
created: 2026-07-31
updated: 2026-07-31
sources:
  - raw/papers/choi-2021-trunet-real-time-speech-enhancement/full-text.md
tags:
  - speech-enhancement
  - mask
  - phase-aware
  - complex-valued
  - deep-learning
---

# Phase-aware β-sigmoid Mask (PHM)

The **Phase-aware β-sigmoid Mask (PHM)** is a complex-valued masking method proposed by Choi et al. (ICASSP 2021) for simultaneous denoising and dereverberation in the STFT domain. Unlike standard magnitude masks bounded in $[0, 1]$, PHM uses a learnable $\beta$ coefficient to extend the magnitude range and reconstructs phase geometrically via the law of cosines, while guaranteeing that the estimated target source and the remaining components sum exactly to the mixture.

## Motivation

Most masking-based speech enhancers estimate only a magnitude mask and reuse the noisy phase for reconstruction — a known sub-optimality. Prior phase-aware approaches (e.g., Wang et al. 2019, [6] in the paper) reconstruct phase from a trigonometric perspective but do not enforce a strict decomposition of the mixture. PHM is designed so that the sum of the estimated target source and the remaining part is **always equal to the mixture** in the complex STFT domain:

$$
X_{t,f} = Y_{t,f}^{(k)} + Y_{t,f}^{(\neg k)}, \quad k \in \{d, r, n\}
$$

where $k$ denotes one of {direct path, reverberation, noise}.

## Construction

### Step 1: Magnitude Mask with Flexible Range

The network outputs two magnitude masks via a sigmoid scaled by a learnable $\beta_{t,f}$:

$$
|M_{t,f}^{(k)}| = \beta_{t,f} \cdot \sigma^{(k)}(z_{t,f}) = \beta_{t,f} \cdot \left(1 + e^{-(z_{t,f}^{(k)} - z_{t,f}^{(\neg k)})}\right)^{-1}
$$

where $z_{t,f}^{(k)}$ is the network output at $(t, f)$ for source $k$, and $\beta_{t,f}$ is computed via an additional network layer with softplus activation:

$$
\beta_{t,f} = 1 + \text{softplus}((\psi_\beta(\phi))_{t,f})
$$

This design serves two purposes:
1. **Flexible magnitude range**: $|M_{t,f}^{(k)}| \in [0, \beta_{t,f}]$ rather than $[0, 1]$, allowing values close to optimal rather than being bounded by 1 like a standard sigmoid mask.
2. **Triangle inequality satisfaction**: Because the complex masks $M^{(k)}$ and $M^{(\neg k)}$ must form a triangle with the mixture, $\beta$ is designed to satisfy:
   - $|M^{(k)}| + |M^{(\neg k)}| \geq 1$ (satisfied by softplus offset of 1)
   - $\left| |M^{(k)}| - |M^{(\neg k)}| \right| \leq 1$ (satisfied by clipping $\beta_{t,f}$ upper bound)

### Step 2: Phase Mask via Law of Cosines

Given the three magnitudes (mixture = 1, $|M^{(k)}|$, $|M^{(\neg k)}|$) as triangle sides, the cosine of the absolute phase difference $\Delta\theta_{t,f}^{(k)}$ between the mixture and source $k$ is:

$$
\cos(\Delta\theta_{t,f}^{(k)}) = \frac{1 + |M_{t,f}^{(k)}|^2 - |M_{t,f}^{(\neg k)}|^2}{2 |M_{t,f}^{(k)}|}
$$

The rotational direction $\xi_{t,f} \in \{1, -1\}$ (clockwise or counterclockwise for phase correction) is estimated via a **two-class straight-through Gumbel-softmax**, yielding the phase mask:

$$
e^{j\theta_{t,f}^{(k)}} = \cos(\Delta\theta_{t,f}^{(k)}) + j \xi_{t,f} \sin(\Delta\theta_{t,f}^{(k)})
$$

The final complex mask is $M_{t,f}^{(k)} = |M_{t,f}^{(k)}| \cdot e^{j\theta_{t,f}^{(k)}}$, applied as $\hat{Y}_{t,f}^{(k)} = M_{t,f}^{(k)} \cdot X_{t,f}$.

## Quadrilateral Extension for Joint Denoising + Dereverberation

![[raw/papers/choi-2021-trunet-real-time-speech-enhancement/figures/4ec22ea430998abf9d5c7c809b19a420fb56ad94b751cefc89074b859c87b138.jpg|PHM quadrilateral illustration]]

*Figure 2: Quadrilateral masking — two PHM pairs form a quadrilateral whose fourth side (reverberation) is uniquely determined.*

To extract both the direct source and reverberation, **two pairs of PHMs** are produced simultaneously:

- **Pair 1**: $M_{t,f}^{(d)}$ and $M_{t,f}^{(\neg d)}$ — separates the mixture into direct source vs. the rest (reverberation + noise).
- **Pair 2**: $M_{t,f}^{(n)}$ and $M_{t,f}^{(\neg n)}$ — separates the mixture into noise vs. reverberant source (direct + reverberation).

Since each PHM pair forms a triangle in the complex STFT domain, the two triangles together form a **quadrilateral**. With three sides and two side angles determined by the two PHM pairs, the fourth side — the reverberation mask $M_{t,f}^{(r)}$ — is **uniquely determined**. This geometric construction enables single-stage joint denoising and dereverberation.

## Distinction from Prior Phase-Aware Masks

| Property | Standard cRM | Wang et al. 2019 [6] | **PHM** |
|----------|:------------:|:--------------------:|:-------:|
| Magnitude bounded to $[0,1]$ | ✗ | ✓ | ✗ (β-extended) |
| Phase estimated | ✓ (direct regression) | ✓ (trigonometric) | ✓ (law of cosines) |
| Mixture = target + rest (guaranteed) | ✗ | ✗ | ✓ |
| Single-stage joint denoising + dereverberation | ✗ | ✗ | ✓ (quadrilateral) |

The key distinction from Wang et al. 2019 is the **strict mixture-conservation property** — PHM is designed so the sum of the estimated target source and the remaining part is always equal to the mixture, whereas Wang et al. estimate phase rotation without enforcing this constraint.

## Related Concepts

- [[concepts/trunet|Tiny Recurrent U-Net (TRU-Net)]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask (cRM)]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/choi-2021-trunet-real-time-speech-enhancement|Choi et al. 2021: Real-Time Denoising and Dereverberation with Tiny Recurrent U-Net]]
