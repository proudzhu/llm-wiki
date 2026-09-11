---
type: concept
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/papers/grinstein-2025-tiny-param-mwf/full-text.md
tags:
  - neural-network
  - recurrent
  - efficiency
  - speech-enhancement
---

# SplitGRU

**SplitGRU** (introduced by Tan & Wang 2019, "Learning complex spectral mapping with gated convolutional recurrent networks") is an efficiency-oriented variant of the [[concepts/gated-recurrent-unit|GRU]] that divides the input feature dimension into $R$ segments, processes each segment with one of $R$ parallel (smaller) GRUs, and reorganizes the outputs such that each GRU's output is distributed to all GRUs in the subsequent layer. Employing a split factor of $R$ reduces the computational demand of the recurrent stack by a factor of $R$, at some cost in cross-segment mixing within a layer (which is recovered across layers via the redistribution).

In [[sources/grinstein-2025-tiny-param-mwf|Grinstein et al. 2025]]'s NeuralPMWF, the temporal block uses 3 causal SplitGRU layers with 96 hidden units and 2 splits each — a key ingredient of the system's 164.9k-parameter / 24.95 MMACs/s budget for multi-channel speech enhancement.

SplitGRU belongs to the same family of "grouped/split" recurrent efficiency tricks as the [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network (GRNN)]] used in RT-Tango (partitioning hidden state into $G$ groups for $O(H^2/G)$ complexity) — both trade intra-layer full connectivity for parallel smaller recurrences with cross-layer information recombination.

## Related Concepts

- [[concepts/gated-recurrent-unit|Gated Recurrent Unit (GRU)]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network (GRNN)]]
- [[concepts/recurrent-neural-network|Recurrent Neural Network]]
- [[concepts/neuralpmwf|NeuralPMWF]]

## Related Sources

- [[sources/grinstein-2025-tiny-param-mwf|Grinstein et al. 2025: Controlling the PMWF Using a Tiny Neural Network]]
