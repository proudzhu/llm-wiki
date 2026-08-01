---
type: concept
created: 2026-08-01
updated: 2026-08-01
tags:
  - speech-enhancement
  - spiking-neural-networks
  - architecture
  - low-power
---

# SSE-Net

SSE-Net (**S**piking **S**peech **E**nhancement **N**etwork) is a monaural speech enhancement architecture whose modules are **designed natively for spike signals** — unlike prior SNN-SE models that convert ANN models by swapping activation functions. It was proposed by Enrui Liu, Andong Li, Cunhang Fan et al. (IEEE/ACM TASLP 2026) — [[sources/liu-2026-sse-net|Liu et al. 2026]].

## Architecture

- **Input**: STFT complex spectrum with real/imaginary parts stacked on the channel axis, **replicated K times** along a new spiking time-step dimension ($K$ = time steps; K=1 chosen after ablation).
- **Encoder**: shallow Conv2D → N Spiking Feature Extraction Groups ([[concepts/spiking-feature-extraction-block|SFEB]] + DownSampling Block: LIF → Conv2D → GroupNorm), channels 24→48→96, frequency axis 161→81→41.
- **Decoder**: symmetric SFEB + UpSampling, skip connections (channel concatenation), restoring full resolution.
- **Refinement**: an [[concepts/information-transformation-block|Information Transformation Block (ITB)]] converts discrete spike features back to continuous representations.
- **Output**: Conv2D mask estimation applied to the original spectrum, then ISTFT.

## Design Rationale

The two prior SNN-SE failure modes addressed: (1) ANN→SNN conversion keeps redundant ANN layers and causes training difficulty/information mismatch; (2) binary (0/1) activation inherently loses information. SSE-Net counters both with spike-native blocks and a continuous residual path inside each SFEB, plus a continuous-domain refinement stage (ITB) at the decoder output.

## Training

Sigmoid surrogate gradient $\sigma(x) = 1/(1+e^{-\alpha x})$ with scale $\alpha$ (backprop instead of conversion), and RI + magnitude loss $\mathcal{L} = 0.5\mathcal{L}_{RI} + 0.5\mathcal{L}_{Mag}$.

## Results

- SOTA among SNN-SE models: WB-PESQ 2.89 / STOI 94% / CSIG 4.03 on VoiceBank+DEMAND; PESQ 2.65 on WSJ0-SI84+DNS (causal).
- Power proxy 19.70 M Ops/s — 62% below Spiking-FullSubNet ([[concepts/intel-neuromorphic-dns-challenge|Intel N-DNS Challenge]] winner); energy cost 1.31 μJ.
- 0.44 G/s MACs — ~17× below the average ANN baseline; causal variant loses only ~0.15 PESQ vs non-causal.

The authors note the architecture currently resembles a "spiking-quantized CNN encoder-decoder" rather than a fully temporally dynamic SNN — future work targets frame-history-conditioned temporal encoding.

## Related Concepts

- [[concepts/spiking-feature-extraction-block|Spiking Feature Extraction Block (SFEB/SFEG)]]
- [[concepts/information-transformation-block|Information Transformation Block (ITB)]]
- [[concepts/spiking-neural-networks|Spiking Neural Networks]]
- [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]]
- [[concepts/neuromorphic-computing|Neuromorphic Computing]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/liu-2026-sse-net|Liu et al. 2026: SSE-Net — Toward Low-Power-Consumption Spiking Neural Network for Monaural Speech Enhancement]]
