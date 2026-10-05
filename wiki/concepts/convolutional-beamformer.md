---
type: concept
created: 2026-10-05
updated: 2026-10-05
sources:
  - raw/papers/ueda-2024-online-joint-optimization/full-text.md
  - raw/papers/nakatani-2022-switching-iva/full-text.md
tags:
  - dereverberation
  - blind-source-separation
  - beamforming
  - convolutional-beamforming
  - speech-enhancement
---

# Convolutional Beamformer (CBF)

A **convolutional beamformer (CBF)** performs dereverberation and source separation *jointly* as a single linear convolution over the current and past STFT frames of the microphone signals, instead of cascading a dereverberation filter and a separation matrix optimized separately. It is the filter structure underlying the WPE×IVA/IVE joint-optimization family (Nakatani, Ikeshita et al.) and their switching and online descendants.

## Formulation

Stacking the current observation $\boldsymbol{x}(f,t)$ with the delayed past observation sequence $\bar{\boldsymbol{x}}(f,t) = [\boldsymbol{x}^{\top}(f,t{-}D), \dots, \boldsymbol{x}^{\top}(f,t{-}D{-}L{+}1)]^{\top}$ ($D$: prediction delay, $L$: filter length), a CBF produces source and noise estimates via

$$
\begin{bmatrix} \hat{\boldsymbol{s}}(f,t) \\ \hat{\boldsymbol{z}}(f,t) \end{bmatrix} = \begin{bmatrix} \boldsymbol{W}(f) \\ \bar{\boldsymbol{W}}(f) \end{bmatrix}^{\mathsf{H}} \begin{bmatrix} \boldsymbol{x}(f,t) \\ \bar{\boldsymbol{x}}(f,t) \end{bmatrix},
$$

where $\boldsymbol{W}(f)$ is the separation matrix and $[\boldsymbol{W}^{\top}, \bar{\boldsymbol{W}}^{\top}]^{\top}$ is the full CBF. The structure **decomposes** into a [[concepts/weighted-prediction-error|WPE]] stage followed by a separation stage:

$$
\boldsymbol{y}(f,t) = \boldsymbol{x}(f,t) - \boldsymbol{G}^{\mathsf{H}}(f)\,\bar{\boldsymbol{x}}(f,t), \qquad
\begin{bmatrix} \hat{\boldsymbol{s}}(f,t) \\ \hat{\boldsymbol{z}}(f,t) \end{bmatrix} = \boldsymbol{W}^{\mathsf{H}}(f)\,\boldsymbol{y}(f,t),
$$

with dereverberation filter $\boldsymbol{G} = -\bar{\boldsymbol{W}}\boldsymbol{W}^{-1}$. The point of the CBF is that $\boldsymbol{W}$ and $\boldsymbol{G}$ are optimized by **one** maximum-likelihood criterion defined on the final outputs — "joint" (×) optimization — rather than each by its own cost function ("+" cascading), which is what makes separation accurate with STFT frames shorter than the reverberation time: the WPE stage removes the reverberation that a short frame cannot average out.

## Algorithm Family

The joint-optimization literature is organized by (offline/online) × (with/without spatial regularization) and by the separation model inside the CBF:

| | Without WPE | With WPE (CBF) |
|---|---|---|
| **Offline** | IVA, IVE, ILRMA | WPE×IVA, WPE×IVE, OverILRMA |
| **Online** | online-IVA, online-IVE | [[concepts/online-joint-optimization\|online-WPE×IVA/IVE]] |
| **Switching** | swIVA | [[concepts/switching-civa\|swCIVA]] |

- **WPE×IVE** (offline; Ikeshita & Nakatani 2021): the IVE instantiation — computationally cheap because only the $N$ source filters and the noise subspace, not all $M$ demixing rows, are estimated.
- **swCIVA** (Nakatani et al. 2022): a bank of $I$ MCLP filters and $J$ separation matrices with a per-TF-bin switch, for few-microphone mixtures.
- **online-WPE×IVE / online-WPE×SRIVE** (Ueda et al. 2024): the online instantiation via a forgetting-factor likelihood; source-wise factorization of the WPE stage keeps the per-frame cost at $O(F(N{+}1)M^2L^2)$, and adding DOA-based [[concepts/spatial-regularization|spatial regularization]] costs nothing extra.

## Related Concepts

- [[concepts/weighted-prediction-error|Weighted Prediction Error (WPE)]]
- [[concepts/independent-vector-extraction|Independent Vector Extraction]]
- [[concepts/online-joint-optimization|Online Joint Optimization (online-WPE×IVE)]]
- [[concepts/switching-civa|Switching CIVA (swCIVA)]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/ueda-2024-online-joint-optimization|Ueda et al. 2024: Blind and Spatially-Regularized Online Joint Optimization of Source Separation, Dereverberation, and Noise Reduction]] — Section III formulation of the CBF and its decomposition; online instantiation with efficient updates
- [[sources/nakatani-2022-switching-iva|Nakatani et al. 2022: Switching IVA and Its Extension to Blind and Spatially Guided Convolutional Beamforming]] — swCIVA: the switching instantiation of the CBF for few-microphone joint separation and dereverberation
