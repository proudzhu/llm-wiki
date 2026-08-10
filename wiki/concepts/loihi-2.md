---
type: concept
created: 2026-08-10
updated: 2026-08-10
sources:
  - raw/papers/timcheck-2023-intel-neuromorphic-dns-challenge/full-text.md
tags:
  - neuromorphic-computing
  - hardware
  - intel
  - spiking-neural-networks
---

# Loihi 2

Loihi 2 is a state-of-the-art neuromorphic chip designed by Intel to efficiently compute temporal dynamics in sparse networks using sparse, event-based communication. It is the target hardware for Track 2 of the [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]] and the platform on which the challenge's power/latency/resource evaluation methodology is grounded.

## Architecture

Like its predecessor Loihi 1, Loihi 2 consists of **neuron cores** that compute the temporal dynamics of stateful neural models, interconnected by a **communication mesh optimized for spike-based communication**. Loihi 2 generalizes and optimizes the Loihi 1 design based on lessons learned during first-generation use.

## Key Features

| Feature | Description |
|---------|-------------|
| **Microcode-programmed neuron models** | Enable a much wider variety of neuron models — both biologically inspired and novel algorithmic — with promising computational benefits in heterogeneous networks |
| **Graded spikes** | Spikes carry an integer value rather than being strictly binary; only marginally more costly than binary spikes in digital hardware but offer straightforward gains in algorithmic precision and processing speed |
| **Enhanced on-chip learning** | Arbitrary local modulating factors ("third factors") may be computed by postsynaptic neuron microcode, generalizing Loihi 1's learning support |
| **Sparse, event-based communication** | Computation only when spikes arrive → minimal data movement and idle power |
| **On-chip memory** | All network configuration embedded on-chip (synaptic weights, routing tables, neuron parameters) — bounded by available state but avoids off-chip memory bottlenecks |

## Synaptic Precision

Loihi 2 supports a range of **1–8 bit synaptic weights**, allowing two networks with the same parameter count to have very different model sizes. This motivates the Intel N-DNS Challenge's distinction between *parameter count* and *model size* (in bytes) as separate Track 1 chip-resource metrics, and rewards quantization-aware training.

## Performant Neuromorphic Features

The Intel N-DNS Challenge enumerates the Loihi 2 features that are performant for neuromorphic algorithms:

- Sparse activity
- Sparse connectivity
- Recurrence
- Stateful neurons
- Neuron temporal dynamics
- Synaptic plasticity
- Graded spikes
- Delay as computational element

The N-DNS baseline SDNN solution exploits only 4 of these 8 (sparse activity, stateful neurons, graded spikes, axonal delays) — leaving substantial room for challenge participants to improve power and model size by incorporating the remaining features.

## Energy Model (Power Proxy Calibration)

Empirical measurements on the Loihi architecture show that **one neuron operation costs approximately 10× one synaptic operation** in energy. This 10× weighting underlies the Intel N-DNS Challenge Track 1 power proxy:

$$
P_{\text{proxy}} = \text{SynOPS} + 10 \times \text{NeuronOPS}.
$$

The same calibration is reused by subsequent SNN-SE work (e.g., [[concepts/sse-net|SSE-Net]], [[sources/liu-2026-sse-net|Liu et al. 2026]]) for fair power-proxy reporting against the N-DNS baseline landscape.

## Related Concepts

- [[concepts/neuromorphic-computing|Neuromorphic Computing]]
- [[concepts/spiking-neural-networks|Spiking Neural Networks]]
- [[concepts/intel-neuromorphic-dns-challenge|Intel Neuromorphic DNS Challenge]]
- [[concepts/sigma-delta-neural-network|Sigma-Delta Neural Network (SDNN)]] — the N-DNS baseline, designed to run on Loihi 2

## Related Sources

- [[sources/timcheck-2023-intel-neuromorphic-dns-challenge|Timcheck et al. 2023: The Intel Neuromorphic DNS Challenge]] — introduces Loihi 2 as the challenge's hardware target and enumerates its performant features
