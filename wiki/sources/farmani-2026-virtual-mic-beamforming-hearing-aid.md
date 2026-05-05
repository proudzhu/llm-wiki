---
type: source
created: 2026-04-29
updated: 2026-04-29
sources:
  - raw/papers/farmani-2026-virtual-mic-beamforming-hearing-aid/full-text.txt
  - https://ieeexplore.ieee.org/abstract/document/11462612
  - zotero://select/items/0_6EW3W6U6
tags:
  - hearing-aid
  - beamforming
  - virtual-microphone
  - mvdr
  - wdo
  - icassp
---

# Farmani, Feldt & Jensen 2026: Beamforming Using Virtual Microphones for Hearing Aid Applications

**Authors**: [[../entities/mojtaba-farmani|Mojtaba Farmani]], [[../entities/svend-feldt|Svend Feldt]], [[../entities/jesper-jensen|Jesper Jensen]]
**Institutions**: Eriksholm Research Centre, Snekkersten, Denmark; Department of Electronic Systems, Aalborg University, Aalborg, Denmark
**Published**: ICASSP 2026, pp. 15552–15556
**Type**: Conference Paper
**DOI**: [10.1109/ICASSP55912.2026.11462612](https://doi.org/10.1109/ICASSP55912.2026.11462612)
**Zotero**: [6EW3W6U6](zotero://select/items/0_6EW3W6U6)

---

## Summary

Proposes a novel, low-complexity method for synthesizing virtual microphone (VM) signals to enhance beamforming in hearing aid (HA) applications. Leveraging the W-disjoint orthogonality (WDO) assumption, the approach generates additional VM channels from a typical two-microphone setup, potentially eliminating the need for extra hardware. The VM signals are estimated by modeling their relative transfer functions (RTFs) as a power function of the RTF between the physical microphones, enabling both interpolation and extrapolation of VM positions.

---

## Problem Formulation

### Signal Model

Under the WDO assumption, the signal model in the STFT domain:

$$Y_i(k, l) = X(k, l) \cdot D_i(k, l)$$

where $k$ and $l$ denote frequency and time-frame indices, $Y_i(k, l)$ is the signal at microphone $i$, $X(k, l)$ is the dominant source signal, and $D_i(k, l)$ is the RTF between microphone $i$ and the reference microphone.

For M microphones:

$$Y(k, l) = X(k, l) \cdot D(k, l)$$

### W-Disjoint Orthogonality (WDO)

The WDO assumption states that only one sound source is dominant at any given time-frequency point due to sparsity and non-overlap of sound signals, particularly speech. This simplifies the signal model and allows direct estimation of RTFs between microphones.

---

## Methodology

### Virtual Microphone Estimation

The VM RTF is modeled as a power function of the physical inter-microphone RTF:

$$D_{\text{vm}}(k, l) = D_2(k, l)^\lambda$$

where $\lambda$ controls the VM position relative to the physical microphones:
- $\lambda \in (0, 1)$: interpolation between microphones
- $\lambda < 0$ or $\lambda > 1$: extrapolation beyond physical microphones

The VM signal is then synthesized:

$$Y_{\text{vm}}(k, l) = Y_1(k, l) \cdot D_{\text{vm}}(k, l) = Y_1(k, l) \cdot D_2(k, l)^\lambda$$

### MVDR Beamformer Integration

The synthesized VM signals are integrated into an MVDR beamformer:

$$w(k) = \frac{\Phi_{nn}^{-1}(k) d(k)}{d^H(k) \Phi_{nn}^{-1}(k) d(k)}$$

where $d(k)$ is the steering vector including the VM channel, and $\Phi_{nn}(k)$ is the noise covariance matrix.

### Computational Complexity

The method requires only:
- One complex power operation per TF bin
- No neural network inference
- No geometric information (DOA estimation)

This makes it highly suitable for resource-constrained HA devices.

---

## Experimental Setup

| Parameter | Value |
|:----------|:------|
| Microphones | 2 physical (hearing aid form factor) |
| VM positions | λ = −4 (extrapolation, front) |
| Recordings | Realistic HA recordings |
| Noise types | Speech-shaped, babble, canteen, coffee machine, train, street traffic |
| Reverberation | Anechoic, moderate, high |
| SNR range | Various input SNR levels |
| Evaluation metric | ISNR (Input SNR improvement), ESTOI (speech intelligibility) |

---

## Results

### VM Position Optimization

- **Front placement (λ = −0.5)**: Best for frontal targets
- **Rear placement (λ = 1.5)**: Best for targets behind user
- **Optimal λ = −4**: Best overall performance for HA applications (target usually in front)

### Performance Comparison

| Configuration | ISNR Gain |
|:--------------|:----------|
| 2mic (baseline) | — |
| GAI (2mic + vm) | +1–2 dB |
| Ext. GAI (2mic + vm) | +1.5–2.5 dB |
| **Proposed (2mic + vm)** | **+2–3 dB** |
| **Proposed (2mic + 2vm)** | **+3–4 dB** |

The proposed method consistently outperforms GAI-based approaches across all input SNR levels, noise types, and reverberation conditions.

### Robustness

- Maintains robust performance in multi-talker environments (canteen, coffee machine)
- Effective in reverberant rooms despite WDO weakening
- Works well with stationary noise (train, street traffic)

---

## Key Contributions

1. **Low-complexity VM synthesis**: Power-function RTF model requires only one complex power operation per TF bin
2. **WDO-based approach**: Leverages speech sparsity for direct RTF estimation without neural networks or DOA
3. **Flexible VM placement**: Interpolation and extrapolation via λ parameter
4. **HA-ready**: Suitable for resource-constrained hearing aid devices
5. **Scalable**: Adding multiple VMs yields further performance gains

---

## Related Concepts

- [[../concepts/remote-microphone-technique|Remote Microphone Technique]]
- [[../concepts/beamforming|Beamforming]]
- [[../concepts/mvdr-beamformer|MVDR Beamformer]]
- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[../concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Synthesis

- [[../synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]
- [[../synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]
