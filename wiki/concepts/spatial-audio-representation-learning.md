---
type: concept
created: 2026-05-12
updated: 2026-05-12
tags:
  - speech-enhancement
  - virtual-microphone
  - representation-learning
  - spatial-audio
---

# Spatial Audio Representation Learning

**Spatial Audio Representation Learning (SARL)** is a framework that leverages estimated virtual microphone (VM) signals and features to condition a downstream multichannel speech enhancement system, decoupling spatial representation learning from spectral enhancement.

## Two Paradigms

### SARL-S (Signal-Level Augmentation)

Spatial-Magnifier estimates explicit VM signals concatenated with RM signals:

$$\bar{\mathbf{y}} = [\mathbf{r}, \hat{\mathbf{v}}]$$

The augmented signal is directly processed by the MC-SE model. Provides raw waveforms with improved spatial information across the expanded array geometry.

### SARL-F (Feature-Level Augmentation)

Spatial-Magnifier estimates VM features $f_{\hat{\mathbf{v}}} \in \mathbb{R}^{H \times T \times F}$ fused with encoded RM signals via element-wise addition:

$$\hat{\mathbf{x}}^{se_{\bar{\mathbf{y}}}} = \text{MC-SE}_{sep.+dec.}(h_\phi(\mathbf{r}) + f_{\hat{\mathbf{v}}})$$

Operates in latent space as a high-level spatial regularizer, effective even when raw VM waveform reconstruction is challenging.

## Key Properties

- **Same inference cost** as base MC-SE model (VM features computed by lightweight Spatial-Magnifier)
- **Architecture-agnostic**: Works with MCWF, MVDR, SpatialNet, MC-RNN back-ends
- **Multi-task training**: Jointly optimizes Neural-VME accuracy and downstream enhancement performance
- **Decouples spatial from spectral**: Forces the system to learn robust spatial representations that benefit MC-SE

## Comparison with VM-BF

| Aspect | VM-BF | SARL |
|:-------|:------|:-----|
| VM usage | Augmented signal for SCM computation | VM signals and/or features condition MC-SE |
| Processing | Linear beamforming back-end | End-to-end or hybrid |
| Spatial info | Via numerical rank increase of SCM | Via spatial embeddings + signal augmentation |
| Flexibility | Requires beamforming back-end | Works with any MC-SE architecture |

## Related Concepts

- [[concepts/virtual-microphone-estimation|Virtual Microphone Estimation]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Sources

- [[sources/lee-2026-spatial-magnifier-spatial-upsampling|Lee et al. 2026: Spatial-Magnifier]]
