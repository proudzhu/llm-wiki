---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - virtual-directional-microphone
  - spatial-audio
  - beamforming
---

# Virtual Directional Microphone

A virtual directional microphone (VDM) is a computationally synthesized microphone with a specified directivity pattern, positioned at a desired location within an acoustic scene. VDMs are reconstructed from physical microphone array recordings using beamforming or neural methods.

## Directivity Pattern

The directivity pattern $\Lambda(\theta,\phi)$ defines the directional sensitivity of a beamformer or directional microphone, describing how spatial responses vary for sounds arriving from different directions. Common patterns include:

- **Omnidirectional**: Equal sensitivity in all directions
- **Cardioid**: Heart-shaped pattern with null at rear
- **Hypercardioid/Supercardioid**: Narrower front lobe with rear lobe
- **Figure-8 (Dipole)**: Bidirectional with nulls at sides

The $J^{\text{th}}$-order Cardioid is defined as:

$$\Lambda(\theta,\phi)=\left(0.5+0.5(\sin\phi\sin\phi_s\cos(\theta-\theta_s)+\cos\phi\cos\phi_s)\right)^J$$

## VDM Signal Decomposition

The VDM signal decomposes into coherent and diffuse components:

$$Z_{\mathrm{vdm}}(f,t)=Z_{\mathrm{coh}}(f,t)+\beta\,Z_{\mathrm{diff}}(f,t)$$

where $\beta=10^{-\frac{\mathrm{DI}}{20}}$ is determined by the directivity index (DI), $Z_{\mathrm{coh}}$ contains direct sound and early reflections, and $Z_{\mathrm{diff}}$ represents late reverberant diffuse sound.

## Reconstruction Methods

| Method | Description | Limitations |
|--------|-------------|-------------|
| DMA | Differential microphone array beamforming | Limited by array size and microphone count |
| Superdirective beamforming | Maximizes directivity factor | Noise amplification at low frequencies |
| NDF | Neural network-based VDM reconstruction | Requires training data |
| NDF+ | Joint VDM + diffuse sound extraction | Extended dual-task capability |

## Applications

- Spatial sound capture and rendering
- Stereo recording (X-Y technique)
- Hearing aid processing
- Virtual reality audio

## Related Concepts

- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/diffuse-sound-extraction|Diffuse Sound Extraction]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/white-noise-gain|White Noise Gain]]

## Related Sources

- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
