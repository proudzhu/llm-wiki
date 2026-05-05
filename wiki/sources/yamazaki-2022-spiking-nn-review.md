---
type: source
created: 2026-04-25
updated: 2026-04-25
sources:
tags:
  - spiking-neural-networks
  - neuromorphic-computing
  - computer-vision
  - robotics
  - review
  - biological-neural-networks
aliases:
  - 'Yamazaki 2022: Spiking Neural Networks Review'
---

# Yamazaki 2022: Spiking Neural Networks and Their Applications: A Review

**Authors**: Kashu Yamazaki, Viet-Khoa Vo-Ho, Darshan Bulsara, Ngan Le
**Published**: Brain Sciences, 12(7):863, 2022-06-30
**DOI**: [10.3390/brainsci12070863](https://doi.org/10.3390/brainsci12070863)
**📎 Zotero**: [zotero://select/items/0_3EGFJDGI](zotero://select/items/0_3EGFJDGI)
**Open Access**: [PMC9313413](https://pmc.ncbi.nlm.nih.gov/articles/PMC9313413/)

## Summary

Comprehensive review covering the full SNN stack: from biological neuron fundamentals (membrane potential, action potentials) through spiking neuron models (Hodgkin-Huxley, LIF, Izhikevich, SRM), synapse models, learning mechanisms (spike backpropagation, STDP and variants, ANN-to-SNN conversion), spike encoding schemes, and applications in computer vision and robotics. The paper positions SNNs as the "third generation" of neural networks that bridge neuroscience and machine learning by using biologically realistic spike-based computation.

## Core Contributions

### 1. Biological Neuron Fundamentals (§2)

Derives membrane potential from Goldman-Hodgkin-Katz equation, calculates resting potential ($-70.15$ mV) and action potential peak ($38.43$ mV) from ion channel permeabilities. Describes the four neuron components: dendrites (input), soma (integration), axon (transmission), synapses (chemical/electrical).

### 2. ANN Models (§3)

Reviews rate-based neuron models from perceptron to modern DNNs. Key equation: $r = f(Wu + b)$. Covers CNNs, RNNs (LSTM/GRU), and attention mechanisms (Transformers).

### 3. Spiking Neuron Models (§4)

Trade-off spectrum from biologically accurate to computationally efficient:

| Model | Biological Accuracy | Computational Cost |
|-------|-------------------|-------------------|
| Hodgkin-Huxley (HH) | Highest | Very high (4 ODEs) |
| Izhikevich | High | Moderate (2 ODEs) |
| LIF | Low | Very low (1 ODE) |
| SRM | Low | Low |

**LIF model** is the workhorse: $τ_m \frac{dv_m}{dt} = -(v_m - v_{rest}) + R_m I_{syn}$, with reset after spike.

**Izhikevich model** can reproduce 20+ firing patterns with just 2 equations and 4 parameters.

### 4. Synapse Models (§4.2)

Current-based (COBA/CUBA) and conductance-based synapse models. Double exponential kernel for post-synaptic currents with rise time $τ_r$ and decay time $τ_d$.

### 5. SNN Learning Mechanisms (§5)

Three paradigms:

- **Spike-based backpropagation**: SpikeProp, SuperSpike, SLAYER — approximate $\frac{∂s}{∂w}$ using smooth surrogate gradients
- **STDP and variants**: Hebbian learning based on spike timing; covers aSTDP, mSTDP, probabilistic STDP, R-STDP (reward-modulated)
- **ANN-to-SNN conversion**: Convert ReLU networks to IF neurons; state-of-the-art results but requires many timesteps

### 6. Spike Encoding (§6)

- **Rate encoding**: Information in spike frequency over time window; Poisson process sampling
- **Temporal encoding**: Information in exact spike timing; sparser but noise-vulnerable

### 7. Computer Vision Applications (§7)

Image classification (MNIST, N-MNIST, ImageNet), object detection, object tracking (SiamSNN), optical flow (Spike-FlowNet), semantic segmentation (UNet-based SNN on Loihi). Event cameras (DVS) are a natural fit for SNNs.

### 8. Robotics Applications (§8)

- **Locomotion**: Spiking CPG (sCPG) on SpiNNaker for hexapod robots
- **Flight control**: Loihi-based SNN for drone landing via optic flow divergence
- **Navigation**: SLAM via spike-based Bayesian inference on Loihi; hippocampus-inspired place/grid cells on SpiNNaker
- **Mapless navigation**: Spiking DDPG (SDDPG) with R-STDP

### 9. Software Frameworks (§9)

| Framework | Training Paradigm | Notes |
|-----------|------------------|-------|
| Brian2 | STDP | Widely-used simulator |
| NEST | STDP/R-STDP | Medical/biological focus |
| Nengo | STDP/PES | NEF-based, large-scale |
| SpykeTorch | STDP/R-STDP | PyTorch-based |
| SLAYER | Backprop | GPU-accelerated |
| snnTorch | Backprop/Conversion | PyTorch-compatible |
| BindsNET | STDP/R-STDP | Reinforcement learning |

### 10. Future Perspectives (§10)

- **Training**: Gradient vanishing/explosion in deep SNNs; BPTT memory cost; RTRL + LIP as promising direction
- **Architecture**: NAS for SNN-specific architectures
- **Large-scale performance**: Still lags ANNs on ImageNet; residual learning for deep SNNs

## Key Equations

- **LIF dynamics**: $τ_m \frac{dv_m}{dt} = -(v_m - v_{rest}) + R_m I_{syn}$
- **STDP weight update**: $Δw = A_+ \exp(\frac{t_{pre} - t_{post}}{τ_+})$ if $t_{pre} \leq t_{post}$, else $-A_- \exp(-\frac{t_{pre} - t_{post}}{τ_-})$
- **Spike backprop surrogate**: $\frac{∂s}{∂w} ≈ σ'(v_m) \cdot (ε × s_{pre})$
- **Rate encoding**: $s = 1$ if $ξ ∼ U(0,1) < rΔt$, else $0$

## Related Concepts

- [[../concepts/spiking-neural-networks|Spiking Neural Networks]]
- [[../concepts/neuromorphic-computing|Neuromorphic Computing]]
- [[../concepts/spike-timing-dependent-plasticity|Spike-Timing-Dependent Plasticity]]
- [[../concepts/neural-networks|Neural Networks]]
- [[../concepts/backpropagation-through-time|Backpropagation Through Time]]
- [[../concepts/real-time-recurrent-learning|Real-Time Recurrent Learning]]

## Related Entities

- [[../entities/kashu-yamazaki|Kashu Yamazaki]]
- [[../entities/viet-khoa-vo-ho|Viet-Khoa Vo-Ho]]
- [[../entities/darshan-bulsara|Darshan Bulsara]]
- [[../entities/ngan-le|Ngan Le]]
