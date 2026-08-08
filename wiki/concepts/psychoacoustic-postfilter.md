---
type: concept
created: 2026-08-08
updated: 2026-08-08
sources:
  - raw/papers/wung-2011-residual-echo-suppression-system/full-text.md
tags:
  - psychoacoustic-postfilter
  - residual-echo-suppression
  - masking-threshold
  - speech-enhancement
---

# Psychoacoustic Postfilter

A psychoacoustic postfilter is a spectral gain that suppresses residual echo (or noise) only up to the point where it would become *audible* against the near-end signal, exploiting the frequency-masking property of human hearing. Beyond that point the gain is left at unity so the near-end speech is undistorted. It is the perceptually motivated counterpart of a pure Wiener/LSA suppressor.

## Key Formulations

Model the AEC error as $E_k = V_k + B_k$ (near-end plus residual echo), and the postfiltered estimate as $\hat{V}_k = H_k E_k$. Assuming $V_k \perp B_k$, the near-end distortion decomposes as

$$\mathcal{E}\{|V_k - \hat{V}_k|^2\} = (1-H_k)^2\,\lambda_V(k) + H_k^2\,\lambda_B(k).$$

To minimally impact the near-end speech, the gain is chosen so that the residual-echo distortion term equals the **masking threshold** $T_V(k)$ of the near-end signal:

$$H_k = \min\left\{1,\ \sqrt{\frac{T_V(k)}{\lambda_B(k)}}\right\}.$$

If the residual echo is already masked by the near-end signal ($T_V(k) > \lambda_B(k)$), then $H_k = 1$ and the near-end signal passes through unchanged. The masking threshold is computed from a rough near-end estimate $\tilde{V}_k$ (e.g., the output of an LSA estimator applied to $E_k$); in [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]] it is obtained from **MPEG-1 Psychoacoustic Model 2**.

### Operating Pipeline

1. Obtain a residual echo estimate $\hat{B}_k$.
2. Apply an LSA gain to $E_k$ using $\hat{B}_k$ to get a rough near-end estimate $\tilde{V}_k$.
3. Compute the masking threshold $T_V(k)$ from $\tilde{V}_k$.
4. Compute $H_k$ and apply it to $E_k$ to get the final near-end estimate $\hat{V}_k$.

Because the masking threshold rises during double talk (loud near-end speech masks the residual echo), overestimation of $\hat{B}$ during strong double talk is harmless — the postfilter simply passes the signal through.

## Related Concepts

- [[concepts/residual-echo-suppression|Residual Echo Suppression]] — the postfilter is the perceptually motivated gain stage of RES.
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]] — the upstream stage whose error signal the postfilter cleans.

## Related Sources

- [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]] — uses the psychoacoustic postfilter [4] (Gustafsson, Martin, Jax & Vary, 2002) with MPEG-1 Model 2 masking on top of the proposed residual echo estimate.
