---
type: concept
created: 2026-04-25
updated: 2026-04-25
sources:
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

## Related Concepts

- [[spiking-neural-networks|Spiking Neural Networks]]
- [[spike-timing-dependent-plasticity|Spike-Timing-Dependent Plasticity]]

## Related Sources

- [[../sources/yamazaki-2022-spiking-nn-review|Yamazaki 2022: Spiking Neural Networks Review]]
