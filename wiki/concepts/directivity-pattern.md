---
type: concept
created: 2026-05-13
updated: 2026-05-13
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

## J-th Order Cardioid

$$\Lambda(\theta,\phi)=\left(0.5+0.5(\sin\phi\sin\phi_s\cos(\theta-\theta_s)+\cos\phi\cos\phi_s)\right)^J$$

where $(\theta_s,\phi_s)$ specifies the target look direction.

## Related Concepts

- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/beamforming|Beamforming]]

## Related Sources

- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
