---
type: concept
created: 2026-07-18
updated: 2026-08-09
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
  - raw/papers/lin-2020-mcunet/full-text.md
  - raw/papers/lin-2021-mcunetv2/full-text.md
  - raw/papers/liu-2024-lightweight-dl-survey/full-text.md
tags:
  - deep-learning
  - neural-networks
  - architecture-search
  - automation
  - tinyml
---

# Neural Architecture Search (NAS)

**Neural Architecture Search (NAS)** automates the design of neural network architectures, enabling the discovery of more efficient and powerful models than manually designed ones. NAS techniques explore various combinations of layers, activation functions, and hyperparameters to find optimal configurations.

## Formulation

NAS is formulated as an optimization problem:

$$
\mathcal{A}^* = \arg\max_{\mathcal{A} \in \mathcal{S}} \text{Accuracy}(\mathcal{A}), \tag{1}
$$

where $\mathcal{A}$ represents an architecture, $\mathcal{S}$ is the search space, and $\mathcal{A}^*$ is the optimal architecture.

## Components

1. **Search space** — defines the set of possible architectures (layer types, connectivity patterns, hyperparameters)
2. **Search strategy** — how the space is explored (random search, reinforcement learning, evolutionary algorithms, gradient-based methods like DARTS)
3. **Performance estimation** — how candidate architectures are evaluated (full training, early stopping, weight sharing)

## Pioneering Work

Zoph and Le (2016) pioneered NAS using reinforcement learning, where a controller RNN generates architecture descriptions and is rewarded based on the validation accuracy of the generated architectures.

## Applications to RNNs

Per [[sources/mienye-2024-rnn-comprehensive-review\|Mienye et al. 2024]], NAS has been applied to discover RNN architectures that outperform manually designed ones. The search space can include:
- Recurrent cell types (LSTM, GRU, custom cells)
- Number of layers and hidden units
- Activation functions
- Connectivity patterns (skip connections, dense connections)
- Hyperparameters (learning rate, dropout rate)

## Search-Space Optimization for Resource-Constrained Devices

Most NAS assumes a fixed mobile search space and targets FLOPs or latency. For [[concepts/tinyml\|TinyML]] on microcontrollers, the binding constraints are **peak SRAM and Flash**, not FLOPs, and there are no standard MCU search spaces. [[concepts/tinynas\|TinyNAS]] (Lin et al. 2020) addresses this by making search-space *optimization* a first-class NAS stage: it scales resolution and width over 108 configurations, samples 1000 networks per configuration, keeps only those satisfying the memory budget (measured by the co-designed [[concepts/tinyengine\|TinyEngine]] inference engine), and selects the configuration whose satisfying models have the largest mean FLOPs — the intuition being that within a model family, larger FLOPs implies larger capacity. It then runs one-shot super-network + evolution search within the selected space. This cut design cost 133× vs. MnasNet (40,000 → 300 GPU hours) and enabled the first >70% ImageNet accuracy on a commercial MCU.

[[sources/lin-2021-mcunetv2\|MCUNetV2 (Lin et al. 2021)]] extends this by merging the two-stage search-space optimization into a single stage: per-block width multiplier $w_{[\,]}$ and input resolution $r$ are added *directly to the search space*, alongside **inference-scheduling knobs** (patch count $p$, patch-stage depth $n$) that enable [[concepts/patch-based-inference\|patch-based inference]] and [[concepts/receptive-field-redistribution\|receptive field redistribution]]. The joint architecture + inference-scheduling search discovers models that cut peak SRAM 4–8× and set a record 71.8% ImageNet top-1 on MCU, unlocking object detection on MCUs.

## Algorithm-Family Taxonomy (per Liu et al. 2024)

[[sources/liu-2024-lightweight-dl-survey\|Liu et al. 2024]] organizes the broader NAS literature into four families by **search algorithm**:

1. **RL-based NAS** — Zoph et al.'s RNN controller generates candidate architectures and updates itself from the accuracy reward; MnasNet adds a factorized hierarchical search space and Pareto-optimizes for latency.
2. **EA-based NAS** — population-based evolution with mutation (AmoebaNet); encoding mechanisms (Sun et al.) and queue-based crossover (Xue et al.) accelerate the evolution.
3. **Gradient-based NAS** — converts the discrete search space to a continuous, differentiable one. DARTS makes structural parameters differentiable; FBNet's DNAS pipeline uses a stochastic supernetwork optimized by SGD with a latency-aware loss $L(a, w_a) = CE(a, w_a) \cdot \alpha \log(LAT(a))^\beta$, where $LAT(\cdot)$ is a per-layer latency lookup table. **Hardware-aware NAS** (FBNet, NetAdapt, NetAdaptV2) belongs here and is the appropriate choice when memory/energy/latency are key constraints and compute is limited.
4. **Other NAS** — symbolic rule-based tuning (Symbolic DNN-Tuner), zero-cost proxies for single-forward-pass scoring (Abdelfattah et al.).

**Practical selection rule** (per the survey): when GPU budget is limited, prefer gradient-based NAS (DARTS, FBNet); when ample compute is available, RL/EA-based NAS yields superior performance; when memory/energy/latency are the binding constraints, use hardware-aware NAS (FBNet, NetAdapt, NetAdaptV2).

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/neural-networks\|Neural Networks]]
- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/activation-functions\|Activation Functions]]
- [[concepts/tinynas\|TinyNAS]] — resource-constrained NAS with automated search-space optimization for MCUs
- [[concepts/patch-based-inference\|Patch-based Inference]] — inference-scheduling strategy co-optimized by MCUNetV2's NAS
- [[concepts/receptive-field-redistribution\|Receptive Field Redistribution]] — automated by MCUNetV2's joint search
- [[concepts/tinyml\|TinyML]] — TinyML problem domain where SRAM/Flash, not FLOPs, drive the search

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — Section 5.2 covers NAS as an innovation in RNN architecture design
- [[sources/lin-2020-mcunet\|Lin et al. 2020: MCUNet — Tiny Deep Learning on IoT Devices]] — introduces TinyNAS, a two-stage NAS that auto-optimizes the search space for MCU memory constraints
- [[sources/lin-2021-mcunetv2\|Lin et al. 2021: MCUNetV2 — Memory-Efficient Patch-based Inference for Tiny Deep Learning]] — merges search-space optimization into one stage and co-optimizes inference scheduling (patch count, patch-stage depth)
- [[sources/liu-2024-lightweight-dl-survey\|Liu et al. 2024: Lightweight Deep Learning for Resource-Constrained Environments]] — surveys NAS by algorithm family (RL / EA / gradient / hardware-aware) with practical selection rules; Figures 7–9 illustrate the RL controller loop, the DNAS/FBNet pipeline, and NetAdapt's layer-wise lookup table
