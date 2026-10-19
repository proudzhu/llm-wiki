---
type: concept
created: 2026-08-08
updated: 2026-10-19
sources:
  - raw/papers/gustafsson-2002-psychoacoustic-aec-nr/full-text.md
  - raw/papers/wung-2011-residual-echo-suppression-system/full-text.md
  - raw/papers/watanabe-2026-low-frequency-harmonic-control/full-text.md
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

### Original Derivation: Combined Residual Echo and Noise (Gustafsson et al. 2002)

The postfilter was originally derived not for residual echo alone but for the *joint* attenuation of residual echo $B(\Omega)$ and noise $N(\Omega)$ in the sending path of a hands-free telephone. Instead of a complete-removal objective, attenuation factors $\zeta_b, \zeta_n \in [0,1]$ select how much of each interference should *remain* (e.g. $\zeta_b = 0.0003 \widehat{=} -35$ dB, $\zeta_n = 0.01 \widehat{=} -40$ dB), so the residual noise keeps its natural character at a reduced level. The error against the desired output $S + \zeta_b B + \zeta_n N$ splits into three independent components:

$$R_{qq}(\Omega) = (1-H)^2 R_{ss} + (\zeta_b - H)^2 R_{bb} + (\zeta_n - H)^2 R_{nn}.$$

The design objective is that the *excess* residual echo and excess noise — the deviations from the desired attenuation — are just masked by the near-end speech, $(\zeta_b - H)^2 R_{bb} + (\zeta_n - H)^2 R_{nn} \stackrel{!}{=} R_{TT}(\Omega)$, which solves (with a practical simplification of the quadratic) to

$$\tilde H^{IND}(\Omega) = \min\left(1,\ \sqrt{\frac{R_{TT}(\Omega)}{R_{bb}(\Omega)+R_{nn}(\Omega)}} + \frac{\zeta_n R_{nn}(\Omega)+\zeta_b R_{bb}(\Omega)}{R_{nn}(\Omega)+R_{bb}(\Omega)}\right).$$

Two structural properties distinguish it from Wiener/LSA rules: (i) if excess echo and noise are already masked by near-end speech, the gain is exactly 1 — the near-end speech is *not* distorted; (ii) if neither near-end speech nor residual echo is present, the gain is the constant $\zeta_n$, so musical noise is impossible by construction. The masking threshold $R_{TT}(\Omega)$ is computed with **MPEG-1 Psychoacoustic Model 2** from a *preliminary* near-end estimate produced by a conventional (LSA) combined rule. In [[sources/gustafsson-2002-psychoacoustic-aec-nr|Gustafsson, Martin, Jax & Vary 2002]], after parameter-matching the LSA baseline so that all instrumental measures coincide, listening tests still preferred the psychoacoustic rule in 97% of double-talk judgments (75% under rapidly changing echo paths).

The echo-only gain $H_k = \min\{1, \sqrt{T_V(k)/\lambda_B(k)}\}$ used by Wung et al. 2011 is the noise-free special case of this original joint formulation.

## Related Concepts

- [[concepts/residual-echo-suppression|Residual Echo Suppression]] — the postfilter is the perceptually motivated gain stage of RES.
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]] — the upstream stage whose error signal the postfilter cleans.
- [[concepts/minimum-statistics|Minimum Statistics]] — supplies the VAD-free noise PSD estimate the joint postfilter needs.
- [[concepts/low-frequency-harmonic-control|Low-Frequency Harmonic Control]] — the masking-aware counterpart for playback intelligibility: instead of suppressing noise up to the masking threshold, it reallocates the desired signal's harmonic energy into less-masked bands (open-ear headphone scenario).

## Related Sources

- [[sources/gustafsson-2002-psychoacoustic-aec-nr|Gustafsson, Martin, Jax & Vary 2002]] — the original paper: derives the $\tilde H^{IND}$ rule for *combined* residual echo and noise attenuation with MPEG-1 Model 2 masking, and validates it against a parameter-matched MMSE-LSA baseline (97% listening-test preference in stationary double talk).
- [[sources/wung-2011-residual-echo-suppression-system|Wung et al. 2011]] — uses the psychoacoustic postfilter of [[sources/gustafsson-2002-psychoacoustic-aec-nr|Gustafsson et al. 2002]] with MPEG-1 Model 2 masking on top of the proposed residual-echo estimate.
- [[sources/watanabe-2026-low-frequency-harmonic-control|Watanabe et al. 2026]] — shares the masking-aware post-filtering principle, applied to playback intelligibility rather than residual-noise suppression.
