---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2021-igcrn/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - training-target
  - amplitude
  - phase
---

# Mask + Mapping + Phase Target

The **mask + mapping + phase** training target is a multi-output prediction scheme introduced by [[concepts/igcrn|IGCRN]] (Liu & Zhang, Interspeech 2021) for spectrogram-based speech enhancement. It uses two parallel decoders: one predicts an **amplitude mask** $A_{msk}$ together with an **amplitude mapping** $A_{map}$, and the other predicts the **real and imaginary parts of the phase** $P_{est}$. The estimated complex spectrum is reconstructed by combining the mask, the mapping, and the phase:

$$A_{est} = A_{msk} \otimes A_{nsy} + A_{map}\tag{4}$$

$$P_{est} = \frac{P_{est_r} + j P_{est_i}}{\sqrt{P_{est_r}^2 + P_{est_i}^2}}\tag{5}$$

$$X_{est} = A_{est} \otimes P_{est}\tag{6}$$

where $A_{nsy}$ is the noisy speech amplitude (used as a residual carrier for the mask output) and $\otimes$ is element-wise multiplication.

## Motivation: Complementary Strengths of Mask and Mapping

Two common ways to predict the amplitude spectrogram are:

- **Mask-based prediction** — predict a ratio mask $A_{msk}$ applied to the noisy amplitude: $\hat A = A_{msk} \otimes A_{nsy}$. Works well at high SNR because the mask can directly reuse the input features. The mask output is bounded and easy to learn when the speech is dominant.
- **Mapping-based prediction** — directly predict the clean amplitude: $\hat A = A_{map}$. Works better at low SNR where the noisy amplitude is a poor starting point and the network needs to "hallucinate" the clean speech from spectral context.

The two are complementary: masking is good where the input is informative, mapping is good where it is not. Combining them in a single decoder (Equation 4) lets the network choose the right balance per time-frequency bin. This generalizes prior schemes:

- **Phasen** (Yin et al. 2020) — predicts amplitude mask + clean phase; the IGCRN paper adds the mapping term to this baseline.
- **Multi-target ensemble** (Zhang et al. 2017) — uses two separate networks for mask and mapping, then a third network to combine them; IGCRN combines them in a single decoder.

## Phase Prediction

Phase is predicted separately by a second decoder that outputs real and imaginary parts, then **normalized to unit magnitude** (Equation 5). This decouples phase from amplitude: the phase decoder only needs to learn the direction of the complex spectrum, not its magnitude, which the authors found more effective than having the phase decoder implicitly encode amplitude. This approach follows Phasen's reasoning that estimating amplitude and phase separately outperforms [[concepts/complex-ratio-mask|complex ratio mask]] prediction, where amplitude and phase are coupled.

## Loss Function (Phasen Loss)

Training uses the Phasen loss (Yin et al. 2020), a compressed-amplitude RI loss that operates on the cube-root-compressed amplitude and the corresponding real/imaginary phase components:

$$\mathcal{L} = \frac{1}{F} \sum_{i=1}^{F} \big( (A_s[i])^{\frac{1}{3}} - (A_{est}[i])^{\frac{1}{3}} \big)^2 + \frac{1}{F} \sum_{i=1}^{F} \big( (A_s[i])^{\frac{1}{3}} \otimes P_{s_r}[i] - (A_{est}[i])^{\frac{1}{3}} \otimes P_{est_r}[i] \big)^2 + \frac{1}{F} \sum_{i=1}^{F} \big( (A_s[i])^{\frac{1}{3}} \otimes P_{s_i}[i] - (A_{est}[i])^{\frac{1}{3}} \otimes P_{est_i}[i] \big)^2$$

where $A_s, P_{s_r}, P_{s_i}$ are the clean amplitude and real/imaginary phase, and $F$ is the number of frequency bins. The cube-root compression emphasizes small-amplitude components and improves perceptual weighting.

## Empirical Evidence

The IGCRN paper provides an ablation (Table 3, -3 dB SNR) showing that each addition to the target improves performance:

| Target | STOI (white / destroyerops / babble) | PESQ | SDR |
|--------|--------------------------------------|------|-----|
| GCRN(CS) — complex spectral mapping | 0.85 / 0.84 / 0.85 | 2.35 / 2.54 / 2.59 | 3.4 / 3.5 / 3.3 |
| GCRN(Msk+Ps) — amplitude mask + clean phase | 0.90 / 0.87 / 0.85 | 2.74 / 2.75 / 2.62 | 11.6 / 10.0 / 8.5 |
| **GCRN(Msk+Map+Ps)** — proposed target | **0.90 / 0.88 / 0.87** | **2.89 / 2.87 / 2.77** | **11.8 / 11.3 / 10.4** |

`GCRN(Msk+Ps)` beats `GCRN(CS)` because amplitude and phase are coupled in the complex spectrum — predicting them separately is more effective than mapping the complex spectrum directly. Adding the amplitude mapping term (`GCRN(Msk+Map+Ps)`) further improves performance, especially at low SNR where the mapping branch pays more attention to the amplitude. The proposed target still falls well short of the full IGCRN model, confirming that the [[concepts/inplace-convolution|inplace architecture]] (not just the target) drives most of the gain.

## Distinction from Complex Spectrum Mapping

The mask + mapping + phase target is **related to but distinct from** [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping (CSM)]]:

- **CSM** directly maps the noisy complex spectrum to the clean complex spectrum by predicting real and imaginary parts (or amplitude and phase). The network learns an implicit amplitude + phase transformation.
- **Mask + mapping + phase** explicitly decomposes the prediction into three terms — a mask (reuses noisy amplitude), a mapping (predicts clean amplitude directly), and a phase (predicted separately and normalized). The mask term is grounded in the noisy input; the mapping term can deviate from it; the phase is decoupled from amplitude.

The IGCRN ablation shows that the explicit decomposition outperforms direct CSM at low SNR. ICCRN, IGCRN's successor, uses a pure CSM target (with a weighted L1 RI+amplitude loss and STFT-consistency enforcement) — a different design choice, suggesting that the optimal target depends on the architecture and training setup.

## Related Concepts

- [[concepts/igcrn|IGCRN]] — the model that introduces this target
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — related training paradigm
- [[concepts/complex-ratio-mask|Complex Ratio Mask]] — alternative mask-based target that couples amplitude and phase
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask]] — foundational mask-based prediction
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — typical architecture used with this target
- [[concepts/iccrn|ICCRN]] — successor that uses pure CSM instead, illustrating the trade-off

## Related Sources

- [[sources/liu-2021-igcrn|Liu & Zhang 2021: IGCRN — Inplace Gated Convolutional Recurrent Neural Network]]
