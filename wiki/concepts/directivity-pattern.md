---
type: concept
created: 2026-05-13
updated: 2026-09-04
sources:
  - raw/papers/wechsler-2024-neural-directional-filtering/full-text.md
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

## Related Concepts

- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/wechsler-2024-neural-directional-filtering|Wechsler et al. 2024: Neural Directional Filtering]] — R-th order DMA pattern formulation and neural realization
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
