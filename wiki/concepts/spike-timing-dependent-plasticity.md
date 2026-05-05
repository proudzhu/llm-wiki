---
type: concept
created: 2026-04-25
updated: 2026-04-25
sources:
tags:
  - learning-rule
  - spiking-neural-networks
  - hebbian-learning
  - unsupervised-learning
---

# Spike-Timing-Dependent Plasticity

STDP is an unsupervised Hebbian learning mechanism that adjusts synaptic weight based on the temporal order of pre- and post-synaptic spikes. It is the primary biologically plausible learning rule for [[spiking-neural-networks|Spiking Neural Networks]].

## Core Rule

$$Δw = A_+ \exp\left(\frac{t_{pre} - t_{post}}{τ_+}\right) \quad \text{if } t_{pre} \leq t_{post} \quad \text{(LTP)}$$

$$Δw = -A_- \exp\left(-\frac{t_{pre} - t_{post}}{τ_-}\right) \quad \text{if } t_{pre} > t_{post} \quad \text{(LTD)}$$

- **LTP** (Long-Term Potentiation): Pre before post → weight increase (causal, Hebbian)
- **LTD** (Long-Term Depression): Post before pre → weight decrease (anti-causal)

## Stability: Homeostatic Scaling

Unbounded weight modification is biologically unrealistic. **Weight-dependent exponential rule** regularizes updates:

$$A_+(w) = η_+ \exp(w_{init} - w), \quad A_-(w) = η_- \exp(w - w_{init})$$

Combined with spike traces, this yields **Stable STDP (S-STDP)**.

## Efficient Implementation: Spike Traces

Instead of storing all spike times, maintain decaying traces:

$$\frac{dx_{pre}}{dt} = -\frac{x_{pre}}{τ_+} + δ(t), \quad \frac{dx_{post}}{dt} = -\frac{x_{post}}{τ_-} + δ(t)$$

$$\frac{dw}{dt} = A_+ x_{pre} · δ_{post} - A_- x_{post} · δ_{pre}$$

## STDP Variants

| Variant | Key Difference | Use Case |
|---------|---------------|----------|
| **aSTDP** | Reversed temporal order (anti-Hebbian) | Cerebellum-like structures |
| **mSTDP** | Combines STDP + aSTDP for symmetric FF/FB | Autoencoders |
| **Probabilistic STDP** | LTP probability depends on current weight | Robust across neuron models |
| **R-STDP** | STDP modulated by reward signal | Reinforcement learning |

## Biological Interpretation

- $x_{pre}$: Opening rate of NMDA receptors
- $x_{post}$: Ca²⁺ influx through voltage-gated channels activated by backpropagating action potential (bAP)

## Related Concepts

- [[spiking-neural-networks|Spiking Neural Networks]]
- [[neuromorphic-computing|Neuromorphic Computing]]

## Related Sources

- [[../sources/yamazaki-2022-spiking-nn-review|Yamazaki 2022: Spiking Neural Networks Review]]
