---
type: concept
created: 2026-04-25
updated: 2026-04-25
sources:
tags:
  - spiking-neural-networks
  - neuromorphic-computing
  - computational-neuroscience
---

# Spiking Neural Networks

Spiking Neural Networks (SNNs) are the **third generation** of neural networks that use biologically realistic spike-based computation. Unlike ANNs that communicate with continuous scalar values, SNNs process information through discrete electrical signals (spikes) in continuous time.

## Key Characteristics

| Property | ANNs | SNNs |
|----------|------|------|
| Information representation | Scalars (firing rates) | Spikes (temporal events) |
| Learning paradigm | Backpropagation | Plasticity / Surrogate gradient BP |
| Platform | VLSI (GPU/CPU) | Neuromorphic VLSI |
| Temporal processing | Explicit (RNN unrolling) | Intrinsic (spike timing) |
| Energy efficiency | High power | Low power (sparse, event-driven) |

## Spiking Neuron Models

Trade-off between biological accuracy and computational cost:

- **Hodgkin-Huxley (HH)**: Most biologically accurate; 4 ODEs modeling Na⁺/K⁺ channel dynamics. Computationally expensive.
- **Izhikevich**: 2 ODEs, 4 parameters; can reproduce 20+ known firing patterns (regular spiking, bursting, chattering, etc.)
- **Leaky Integrate-and-Fire (LIF)**: 1 ODE; simplest useful model. Membrane potential leaks toward rest, fires when threshold reached, then resets.
- **Spike Response Model (SRM)**: Filter-based; membrane potential expressed as kernel convolutions with spike trains.

## Learning Mechanisms

1. **Spike-based backpropagation**: Uses surrogate gradients to approximate non-differentiable spike function. Key methods: SpikeProp, SuperSpike, SLAYER.
2. **STDP**: Unsupervised Hebbian learning based on pre/post-spike timing. Variants: aSTDP, mSTDP, probabilistic STDP, R-STDP.
3. **ANN-to-SNN conversion**: Convert pre-trained ReLU networks to IF neurons. Achieves best accuracy on large-scale tasks but requires many timesteps.

## Spike Encoding

- **Rate encoding**: Information in spike frequency; robust but slow (needs time window)
- **Temporal encoding**: Information in exact spike timing; sparse and fast but noise-vulnerable

## Advantages over ANNs

- **Energy efficiency**: Sparse, event-driven computation on neuromorphic hardware
- **Temporal processing**: Native handling of time-varying signals
- **Biological plausibility**: Compatible with neuroscience findings

## Challenges

- Training deep SNNs remains difficult (non-differentiable spikes, BPTT memory cost)
- Performance on large-scale datasets (ImageNet) still lags ANNs
- Lack of SNN-specific architectures (most work repurposes ANN architectures)

## Related Concepts

- [[neuromorphic-computing|Neuromorphic Computing]]
- [[spike-timing-dependent-plasticity|Spike-Timing-Dependent Plasticity]]
- [[neural-networks|Neural Networks]]
- [[backpropagation-through-time|Backpropagation Through Time]]
- [[real-time-recurrent-learning|Real-Time Recurrent Learning]]

## Related Sources

- [[sources/yamazaki-2022-spiking-nn-review|Yamazaki 2022: Spiking Neural Networks Review]]
