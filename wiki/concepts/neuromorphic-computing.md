---
type: concept
created: 2026-04-25
updated: 2026-08-10
sources:
  - raw/papers/liu-2026-sse-net/full-text.md
  - raw/papers/timcheck-2023-intel-neuromorphic-dns-challenge/full-text.md
tags:
  - neuromorphic-computing
  - hardware
  - spiking-neural-networks
---

# Neuromorphic Computing

Computing paradigm inspired by the brain's architecture, using spiking neurons and event-driven processing on specialized hardware (neuromorphic chips). Enables energy-efficient deployment of [[spiking-neural-networks|Spiking Neural Networks]].

## Key Neuromorphic Platforms

| Platform | Institution | Key Feature |
|----------|------------|-------------|
| **TrueNorth** | IBM | 1M spiking neurons, 256M synapses, 70mW |
| **Loihi** | Intel | On-chip learning, programmable learning rules |
| **SpiNNaker** | U. Manchester | Real-time biological neural simulation |
| **NeuroGrid** | Stanford | Mixed analog-digital, 1M neurons |

## Why Neuromorphic Hardware?

- **Energy efficiency**: Spikes are sparse binary events → minimal data movement
- **Event-driven**: Computation only when spikes arrive (no idle power waste)
- **Parallelism**: Massively parallel architecture matching neural computation
- **Online learning**: Some platforms (Loihi) support on-chip plasticity

## Applications

- Robotics: real-time perception and control on low-power platforms
- Edge AI: always-on sensing with battery constraints
- Brain simulation: real-time or faster-than-real-time neural simulation
- Low-power speech enhancement: SNN-based SE models like [[concepts/sse-net|SSE-Net]] report power proxies of ~20 M Ops/s (≈1 μJ energy cost) on Loihi-class energy accounting — 1–2 orders of magnitude below ANN SE baselines

## Related Concepts

- [[spiking-neural-networks|Spiking Neural Networks]]
- [[spike-timing-dependent-plasticity|Spike-Timing-Dependent Plasticity]]
- [[concepts/loihi-2|Loihi 2]] — Intel neuromorphic chip targeted by the Intel N-DNS Challenge
- [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]] — benchmark for SNN-based real-time audio denoising

## Related Sources

- [[sources/yamazaki-2022-spiking-nn-review|Yamazaki 2022: Spiking Neural Networks Review]]
- [[sources/timcheck-2023-intel-neuromorphic-dns-challenge|Timcheck et al. 2023: The Intel Neuromorphic DNS Challenge]] — defines a neuromorphic benchmark for real-time audio denoising on Loihi 2 with power/latency/resource evaluation methodology
- [[sources/liu-2026-sse-net|Liu et al. 2026: SSE-Net]] — SNN speech enhancement targeting neuromorphic deployment
