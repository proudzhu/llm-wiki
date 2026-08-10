---
type: concept
created: 2026-08-01
updated: 2026-08-10
sources:
  - raw/papers/timcheck-2023-intel-neuromorphic-dns-challenge/full-text.md
tags:
  - challenge
  - speech-enhancement
  - neuromorphic-computing
  - spiking-neural-networks
  - power-efficiency
  - intel
  - loihi
---

# Intel Neuromorphic DNS Challenge

The Intel Neuromorphic Deep Noise Suppression (N-DNS) Challenge (Timcheck et al., arXiv 2023; *Neuromorphic Computing and Engineering*) solicited high-performance **SNN-based speech enhancement models** targeting ultra-low-power deployment on neuromorphic hardware ([[concepts/loihi-2|Intel Loihi 2]]). Introduced by [[sources/timcheck-2023-intel-neuromorphic-dns-challenge|Timcheck et al. 2023]], it is the main benchmark/evaluation framework for SNN-SE work such as [[concepts/sse-net|SSE-Net]] ([[sources/liu-2026-sse-net|Liu et al. 2026]]), whose champion was Spiking-FullSubNet (Hao et al. 2025).

## Power-Proxy Metrics

Because neuromorphic energy scales with fundamental computational operations, the challenge defines:

- **SynOPs** (synaptic operations): $\sum_{l=1}^{L-1}\sum_{i=1}^{\mathcal{N}^l} \mathcal{R}_i^l (\mathcal{N}^{l+1} + \mathcal{N}^l)$ — weighted by per-neuron firing rates $\mathcal{R}_i^l$.
- **NeuronOPs** (neuron operations): $\sum_{l=1}^{L} \mathcal{N}^l$.
- **Power proxy**: $P_{\text{proxy}} = \mathrm{SynOPs} + 10 \times \mathrm{NeuronOPs}$ — based on measurements on Intel Loihi showing one NeuronOP consumes ≈ 10× one SynOP.
- **PDP proxy**: $P_{\text{proxy}} \times \text{Latency}$ — power under delay constraints.
- **Energy cost** (J): physical energy estimate.

## Key Results Landscape (from SSE-Net's comparison)

| System | Power proxy (Ops/s) | PDP proxy (Ops) | Energy cost (J) |
|---|---|---|---|
| CTDNN LAVADL* | 61.37 M | 1.96 M | 1.76 μ |
| PSNN* | 57.24 M | 1.83 M | 1.65 μ |
| Spiking-FullSubNet (winner) | 51.30 M | 1.64 M | 1.48 μ |
| **SSE-Net** | **19.70 M** | **0.63 M** | **1.31 μ** |

\* Top-ranking challenge systems. SSE-Net reports the lowest power proxy of the published landscape (62% below the challenge winner).

## Related Concepts

- [[concepts/loihi-2|Loihi 2]] — the neuromorphic chip targeted by Track 2 of the challenge
- [[concepts/sigma-delta-neural-network|Sigma-Delta Neural Network (SDNN)]] — the released baseline solution
- [[concepts/spiking-neural-networks|Spiking Neural Networks]]
- [[concepts/neuromorphic-computing|Neuromorphic Computing]]
- [[concepts/sse-net|SSE-Net]]
- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/nsnet2|NSNet2]] — Microsoft DNS 2022 baseline used as the conventional comparison point
- [[concepts/dns-challenge|DNS Challenge (Microsoft)]] — the ANN-era predecessor benchmark

## Related Sources

- [[sources/timcheck-2023-intel-neuromorphic-dns-challenge|Timcheck et al. 2023: The Intel Neuromorphic DNS Challenge]] — primary source defining the challenge, tracks, metrics, dataset, and SDNN baseline
- [[sources/liu-2026-sse-net|Liu et al. 2026: SSE-Net]] — SNN-SE model reporting power proxy against the N-DNS Challenge landscape
