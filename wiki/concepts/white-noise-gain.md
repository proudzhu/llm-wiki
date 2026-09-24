---
type: concept
created: 2026-05-07
updated: 2026-09-24
tags:
  - beamforming
  - robustness
  - microphone-arrays
sources:
  - raw/papers/pan-2020-microphone-array-beamforming/full-text.txt
  - raw/papers/deng-2026-joint-covariance-wng-mvdr/full-text.md
  - raw/papers/zhu-2025-kronecker-superdirective-beamforming/full-text.txt
  - raw/papers/cohen-2019-differential-kronecker-beamforming/full-text.txt
  - raw/papers/desena-2012-higher-order-differential/full-text.md
---

# White Noise Gain (WNG)

**Category**: Beamforming Robustness Metric

## Definition

The White Noise Gain (WNG) quantifies a beamformer's robustness to spatially uncorrelated (white) noise. It is defined as the ratio of output SNR to input SNR in a spatially white noise field:

$$W = \frac{|\mathbf{w}^H \mathbf{d}|^2}{\|\mathbf{w}\|^2} = \frac{1}{\|\mathbf{w}\|^2}$$

where the second equality holds under the distortionless constraint $\mathbf{w}^H \mathbf{d} = 1$.

## Interpretation

- **High WNG**: The beamformer is robust to uncorrelated sensor noise and array imperfections
- **Low WNG**: The weight vector norm $\|\mathbf{w}\|^2$ is large, indicating sensitivity to noise and potential target cancellation
- **Maximum WNG**: For an $M$-element array, the theoretical maximum is $10\log_{10}(M)$ dB (achieved by the delay-and-sum beamformer)

## WNG Collapse in Snapshot Deficiency

When the sample SCM is estimated from insufficient snapshots ($L < M$ or $L \approx M$):
1. The SCM becomes ill-conditioned
2. The weight vector norm $\|\mathbf{w}\|^2$ spikes
3. WNG plummets, causing severe target signal cancellation

## WNG-Constrained Beamforming (Mittal et al. 2026)

Mittal et al. (2026) propose enforcing a strict lower bound $W \geq W_{\min}$ via adaptive diagonal loading. Using the Kantorovich inequality, they derive:

$$\frac{W}{M} \geq \frac{4\kappa}{(\kappa+1)^2}$$

This maps the desired WNG bound to a maximum allowable condition number $\kappa_{\max}$, enabling principled loading parameter selection.

### Practical WNG Bound

A typical choice is $W_{\min} = 10\log_{10}(M) - 3$ dB, allowing 3 dB of WNG degradation from the delay-and-sum maximum in exchange for adaptive interference nulling.

## Practical Threshold Rule of Thumb

[[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020]] state a practical system-level rule: since most microphone sensors' self-noise lies in the 20–35 dBA range, a WNG above **−20 dB** generally prevents white-noise amplification problems in real systems (i.e., yields good robustness). The exact WNG level required depends on the sensors' self-noise and inter-sensor mismatch — lower self-noise tolerates lower WNG for the same robustness.

## WNG in Fixed Superdirective Design

For fixed [[concepts/superdirective-beamforming|superdirective beamformers]], WNG is the robustness metric traded against the directivity factor: maximizing DF drives WNG strongly negative at low frequencies (white-noise amplification). Two loading-based control mechanisms appear in the literature (Zhu et al. 2025): (i) a fixed diagonal loading factor $\epsilon$ in $[\boldsymbol{\Gamma} + \epsilon\mathbf{I}]^{-1}$, and (ii) a **per-frequency bisection** on $\epsilon$ that pins WNG to an explicit target (e.g., 0 dB or −10 dB) at every bin. In [[concepts/kronecker-product-beamforming|Kronecker product beamforming]], the decomposition rank $P$ provides an additional WNG knob: larger $P$ raises DF but lowers WNG.

Under a Kronecker filter $\mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$, the WNG **factorizes** as $W(\mathbf{h}) = W_1(\mathbf{h}_1) \times W_2(\mathbf{h}_2)$ (Cohen, Benesty & Chen 2019) — unlike the directivity factor, which does not factorize. This makes the virtual-array WNGs directly controllable design knobs: the KP cardioid pairs a delay-and-sum $\mathbf{h}_1$ (maximum WNG) with the differential $\mathbf{h}_2$, and the robust KP variant adds an $\epsilon_2$ regularization whose increase monotonically raises WNG at the cost of DF.

## Data-Driven WNG Estimation

Conventionally, the WNG lower bound $W_{\min}$ is a fixed hyperparameter tuned manually (e.g., $10\log_{10}(M) - 3$ dB for all frequencies). Deng et al. (2026) introduce a **frequency-adaptive learnable WNG** scheme where a neural network predicts a per-frequency-bin WNG threshold $\mathcal{W}_0(k)$ jointly with T-F masks for [[concepts/spatial-covariance-matrix|SCM]] estimation. The WNG prediction is implicitly supervised via the beamforming reconstruction loss rather than requiring explicit WNG labels, enabling the network to discover optimal frequency-dependent robustness tradeoffs automatically. This approach outperforms fixed-threshold baselines by +1.4–1.8 dB SNR gain under both matched and mismatched array conditions.

## WNG of Differential Microphone Arrays

For second-order DMAs, [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012]] derive closed-form look-direction WNGs for both the conventional (real-root) cascade and their complex-root structure: both depend on the pattern coefficients $(a_1, a_2)$ only through a product with $kd$ ($k$ = wave number, $d$ = spacing), and take very similar values in their respective regions of the $(a_1,a_2)$ plane. WNG collapses as $kd$ shrinks — at $kd=0.25$, second-order patterns sit around −20 to −30 dB (hypercardioid −29.9 dB, cardioid-A −20 dB), and at $kd=0.1$ both structures are nearly unusable without very low-noise capsules. This yields an explicit operational band for a DMA:

$$f_{\min} = \frac{\gamma c}{2\pi d} \quad (\text{WNG bound, } \gamma = \text{smallest acceptable } kd), \qquad f_{\max} = \frac{c}{4d} \quad (\text{Taylor-approximation bound})$$

which is the quantitative form of the familiar "differential arrays amplify noise at low frequencies" limitation. Multi-spacing sub-arrays merged with crossover filters extend the band because WNG is a function of the product $kd$ alone.

## Related Concepts

- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/kantorovich-inequality|Kantorovich Inequality]]
- [[concepts/condition-number|Condition Number]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/robust-minimum-variance-beamforming|Robust Minimum Variance Beamforming]]
- [[concepts/neural-beamforming|Neural Beamforming]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]

## Related Sources

- [[sources/mittal-2026-adaptive-diagonal-loading-beamforming|Mittal et al. 2026: Adaptive Diagonal Loading for Norm Constrained Beamforming]]
- [[sources/deng-2026-joint-covariance-wng-mvdr|Deng et al. 2026: Joint Covariance and WNG Learning for Robust MVDR]]
- [[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025: Low-Rank Robust Superdirective Beamforming Using Multidimensional Kronecker Products]] — WNG as the robustness metric in superdirective design; per-frequency bisection on the loading factor to hit a WNG target; rank-P as a WNG knob
- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]] — WNG factorization $W = W_1 \times W_2$ under Kronecker filters; $\epsilon_2$ regularization knob
- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — practical rule of thumb: sensor self-noise 20–35 dBA implies WNG > −20 dB is generally safe
- [[sources/desena-2012-higher-order-differential|De Sena, Hacihabiboglu & Cvetkovic 2012: On the Design and Implementation of Higher Order Differential Microphones]] — closed-form WNG of second-order DMA structures; WNG as a function of $kd$ defining the operational band $[\gamma c/2\pi d,\ c/4d]$
