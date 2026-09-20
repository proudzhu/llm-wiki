---
type: concept
created: 2026-05-13
updated: 2026-09-20
sources:
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
  - raw/papers/huang-2025-steerable-neural-directional-filtering/full-text.md
  - raw/papers/zhu-2025-kronecker-superdirective-beamforming/full-text.txt
  - raw/papers/cohen-2019-differential-kronecker-beamforming/full-text.txt
  - raw/papers/pan-2020-microphone-array-beamforming/full-text.txt
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
tags:
  - directivity-pattern
  - spatial-audio
  - beamforming
---

# Directivity Pattern

A directivity pattern describes the directional sensitivity of a beamformer or microphone, characterizing how spatial responses vary for sounds arriving from different directions $(\theta,\phi)$.

## Mathematical Definition

The directivity pattern $\Lambda(\theta,\phi)$ defines the gain applied to sound arriving from azimuth $\theta$ and polar angle $\phi$. The directivity index (DI) quantifies the overall directivity:

$$\mathrm{DI}=10\log_{10}\left(\frac{\Lambda_{\max}}{\frac{1}{4\pi}\int_0^{2\pi}\int_0^{\pi}\Lambda(\theta,\phi)\sin\phi\,d\phi\,d\theta}\right)$$

## Common Patterns

| Pattern | Order | DI (dB) | Description |
|---------|-------|---------|-------------|
| Omnidirectional | 0th | 0 | Equal sensitivity in all directions |
| Cardioid | 1st | 4.77 | Heart-shaped, null at rear |
| Hypercardioid | - | 6.0 | Narrower front lobe |
| Supercardioid | - | 5.7 | Maximum front-to-back ratio |
| 6th-order Cardioid | 6th | 11.14 | Highly directional |

## R-th Order DMA Pattern

A general $R$-th order differential microphone array pattern steered towards $\vartheta_0$ (Elko 2004; Benesty, Chen & Cohen 2015):

$$
S[\vartheta, f] = \sum_{r=0}^{R} a_r \cos^{r}(\vartheta - \vartheta_0) \quad \forall f,$$

i.e., frequency-invariant by construction. Examples from [[concepts/neural-directional-filtering|NDF]]: a 1st-order cardioid ($a_0 = a_1 = \frac{1}{2}$, realizable as a 3-microphone CDMA) and a 3rd-order pattern ($a_0 = 0,\ a_1 = \frac{1}{6},\ a_2 = \frac{1}{2},\ a_3 = \frac{1}{3}$, realizable as a 6-microphone CDMA).

## J-th Order Cardioid

$$\Lambda(\theta,\phi)=\left(0.5+0.5(\sin\phi\sin\phi_s\cos(\theta-\theta_s)+\cos\phi\cos\phi_s)\right)^J$$

where $(\theta_s,\phi_s)$ specifies the target look direction.

## Kronecker Product Beampatterns

For a Kronecker filter $\mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$ over two virtual arrays, the global pattern factorizes (Cohen, Benesty & Chen 2019):

$$\mathcal{B}_\theta(\mathbf{h}) = \mathcal{B}_{1,\theta}(\mathbf{h}_1) \times \mathcal{B}_{2,\theta}(\mathbf{h}_2)$$

As a polynomial in two variables, it has at most $M_1 + M_2 - 2$ distinct nulls, versus $M_1 M_2 - 1$ for a conventional filter of the same length — a structural restriction that is also the source of the design's robustness. The first-order pattern families (cardioid, dipole, hypercardioid, supercardioid) each have Kronecker product realizations; see [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019]] and [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]].

## Cosine-Based Pattern with Configurable Main-Lobe Width

For hearing-device NDF, Uphaus et al. 2026 replace DMA-pattern training objectives (whose main-lobe width cannot be specified angularly) with a cosine-based pattern whose main-lobe width $W$ is configurable and whose maximum attenuation is capped at $M$ to preserve spatial awareness:

$$
\Lambda(\theta)=\begin{cases}\left|\cos\!\left(\frac{\pi}{W}\angle e^{j(\theta-\theta_{d})}\right)\right|,& |\angle e^{j(\theta-\theta_{d})}|\le\frac{W}{2}\\
M,& \text{else}\end{cases}
$$

with orientation $\theta_d$ relative to the head; $M=-20$ dB and $W=90°$ in their experiments.

## Related Concepts

- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/cohen-2019-differential-kronecker-beamforming|Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming]] — beampattern factorization under Kronecker filters
- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods for Speech Communication and Interaction]] — Chinese-language review elevating beampattern frequency invariance to a co-equal design axis with DF and WNG across six beamforming families
- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — R-th order DMA pattern formulation and neural realization
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
- [[sources/huang-2025-steerable-neural-directional-filtering|Huang, Halimeh, Chetupalli, Thiergart & Habets 2025: Steerable Neural Directional Filtering]]
- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — cosine-based pattern with configurable main-lobe width $W$ and capped attenuation $M$ for hearing devices

