---
type: concept
created: 2026-09-16
updated: 2026-09-16
sources:
  - raw/papers/wen-2025-neural-directed-speech-enhancement/full-text.md
tags:
  - directional-speech-enhancement
  - beamforming
  - spatial-filtering
  - multi-channel
---

# Triple-Steering Spatial Selection

**Triple-steering spatial selection** is a spatial selection method for directed multi-channel speech enhancement, proposed by Wen et al. (ICASSP 2025). Instead of steering a single beam toward the target, it generates **three steering vectors** — one at the target angle $\varphi_{target}$ and two at the edge angles $\varphi_{target} \pm \varphi_{width}$ — so that a neural network receives explicit information about both the target direction and the angular extent of the region to be enhanced.

## Mechanism

1. The target angle $\varphi_{target}$ and an **enhancement width** $\varphi_{width}$ (an input parameter) define three directions: the target and its two edges.
2. Three beamformer outputs are computed and, together with the two raw microphone spectra, fed to the [[concepts/cdunet|CDUNet]] (a causal U-Net).
3. By comparing the edge-angle beamformer outputs with the target output, the model discerns the spatial distribution of interfering speech and adapts the enhancement range.

The width input makes this the first directed enhancement framework in which the enhancement region is a **runtime parameter** rather than a fixed training-time property:

- When $\varphi_{width}$ is smaller than the target–interference angular separation, the width acts as a **discriminative boundary** cleanly separating target from interference.
- When $\varphi_{width}$ is too small (3° in the authors' ablation), the edge beams carry little information beyond the target beam.
- When $\varphi_{width}$ exceeds the target–interference separation (>15° in their setup), the boundary can no longer separate the directions and performance degrades.

## Empirical Behavior

In the Wen et al. 2025 evaluation (dual 30 mm microphone array, fixed target at 90°, SNR 0 dB), the optimal input width was $\varphi_{width} = 7^\circ$ (avg. PESQ 2.54 vs. 2.44 for the un-steered U-Net), with monotone degradation as the width moved away from the optimal on either side (3°: 2.49; 15°: 2.51; 20°: 2.45; 60°: 2.38). Because the width is an input, one trained model can be retuned to different interference layouts at inference without retraining.

## Related Concepts

- [[concepts/cdunet|CDUNet]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/neural-beamforming|Neural Beamforming]]
- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/wen-2025-neural-directed-speech-enhancement|Wen et al. 2025: Neural Directed Speech Enhancement with Dual Microphone Array in High Noise Scenario]] — the introducing paper
