---
type: concept
created: 2026-05-13
updated: 2026-05-13
tags:
  - diffuse-sound
  - spatial-audio
  - reverberation
---

# Diffuse Sound Extraction

Diffuse sound extraction refers to the task of isolating the late reverberant, spatially diffuse component from an acoustic scene. In spatial audio processing, controlling the diffuse component is essential for managing spatial cues and immersive audio quality.

## Problem Definition

The diffuse sound component $Z_{\mathrm{diff}}(f,t)$ represents the late reverberant portion captured by an omnidirectional microphone at the VDM position:

$$Z_{\mathrm{diff}}(f,t)=\sum_{n=1}^{N}H_{\mathrm{diff},n}(f)\,X_{n}(f,t)$$

where $H_{\mathrm{diff},n}(f)$ corresponds to the late reverberant portion of the room transfer function.

## Target Signal Generation

The diffuse component RIR is approximated by applying an inverse window to the reference microphone RIR:

$$w_{\mathrm{inv}}[k]=1-w_{\mathrm{coh}}[k],\quad k=0,1,\dots,K-1$$

where $w_{\mathrm{coh}}[k]$ is the coherent component window that preserves direct path and early reflections.

## Applications

- **Stereo recording**: Controlling inter-channel level differences via diffuse sound adjustment
- **Spatial audio rendering**: Managing diffuseness for immersive experiences
- **VDM reconstruction**: Explicit control over diffuse component in final output

## Related Concepts

- [[concepts/virtual-directional-microphone|Virtual Directional Microphone]]
- [[concepts/neural-directional-filtering|Neural Directional Filtering]]
- [[concepts/room-transfer-function|Room Transfer Function]]
- [[concepts/room-impulse-response|Room Impulse Response]]

## Related Sources

- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang et al. 2026: NDF+]]
