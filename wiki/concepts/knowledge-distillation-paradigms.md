---
type: concept
created: 2026-08-09
updated: 2026-08-09
sources:
  - raw/papers/liu-2024-lightweight-dl-survey/full-text.md
tags:
  - knowledge-distillation
  - model-compression
  - deep-learning
  - taxonomy
  - efficient-deep-learning
---

# Knowledge Distillation Paradigms

**Knowledge Distillation (KD) Paradigms** is a three-way taxonomy of KD methods, organized by **how the teacher model is defined and trained relative to the student**. The taxonomy is cleanly laid out by [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024]] (Figure 6) and structures the diverse KD literature into offline, online, and self-distillation families — each with distinct practical implications for when a pre-trained teacher is available, whether multi-GPU training is feasible, and how much labeled data is on hand.

## Core Mechanism

Vanilla KD (Hinton et al. 2015): a large pre-trained **teacher** generates soft labels (logits over-temperature-scaled softmax); a smaller **student** trains against both ground-truth labels and the teacher's soft predictions. The student thereby attains performance comparable to the teacher using fewer parameters.

## The Three Paradigms

### 1. Offline Distillation

- **Teacher**: pre-trained, frozen before student training begins.
- **Pipeline**: sequential (train teacher → train student against teacher's predictions).
- **Strengths**: simple to implement; well-understood.
- **Limitations**: requires the time/compute overhead of training a large teacher first.
- **Representative methods**: vanilla KD (Hinton et al.), SimKD (reuses teacher's classifier, L2 feature alignment), SemCKD (feature-embedding similarity preservation), SRRL.
- **When to use**: a large teacher can be trained or is already available.

### 2. Online Distillation

- **Teacher**: trained concurrently with the student; sometimes the "teacher" is just one of several peer models.
- **Pipeline**: end-to-end joint training; no pre-trained teacher needed.
- **Strengths**: no teacher pre-training overhead; can improve the teacher itself (large networks benefit from knowledge distilled from smaller peers).
- **Limitations**: requires multi-GPU training of multiple networks simultaneously.
- **Representative methods**:
  - **Deep Mutual Learning (DML)**: cohort of networks, each incorporates others' predictions into its loss; the WRN-28-10 improves 0.27% even when paired with a ResNet32 that has 10% lower accuracy.
  - **FFSD**, **KDCL**: refinements of the mutual-learning approach.
  - **Mean-teacher framework**: teacher = exponential moving average (EMA) of student weights; widely adopted for unsupervised pseudo-label generation.
- **When to use**: no pre-trained teacher available; multi-GPU training of small models is feasible; labeled data is scarce or noisy (pseudo-labels).

### 3. Self-Distillation

- **Teacher**: the model itself — across layers (deeper → shallower), across epochs (past → present), or via self-referential regularization.
- **Pipeline**: single model simultaneously acts as teacher and student.
- **Strengths**: only one model needed; no extra training infrastructure.
- **Limitations**: weaker gains than offline/online KD (e.g., PS-KD: +3.36% on ResNet18); should be paired with other compression methods for maximum effect.
- **Representative methods**:
  - **SD** (Zhang et al.): self-distillation from deeper to shallower layers.
  - **Tf-KD** (Yuan et al., Teacher-free KD): relates KD to Label Smoothing Regularization (LSR); uses self-training or manually-designed regularization when a powerful teacher is unavailable.
  - **PS-KD** (Kim et al.): progressive framework with adaptive gradient rescaling for hard-example mining.
- **When to use**: single-model constraint; complement to other compression methods.

## Practical Selection (per Liu et al. 2024)

| Scenario | Recommended Paradigm |
|----------|---------------------|
| Large teacher can be trained first | Offline KD |
| No pre-trained teacher; multi-GPU available | Online KD (DML) |
| Scarce or noisy labels | Online KD (mean-teacher for pseudo-labels) |
| Single-model constraint | Self-distillation (pair with other methods) |

## Cross-Paradigm Insight

The three paradigms are not mutually exclusive — modern compression pipelines often combine them (e.g., self-distillation pre-training followed by offline KD from a final large teacher). Performance heavily depends on implementation details, so Liu et al. 2024 advocate for **adopting the strategy that is easiest to implement and aligns most logically with the ongoing development objectives**, rather than chasing the absolute best-reported accuracy.

## Related Concepts

- [[concepts/neural-architecture-search|Neural Architecture Search]] — complementary compression method often combined with KD
- [[concepts/post-training-quantization|Post-Training Quantization]] — another compression method; pipelines often combine KD + quantization
- [[concepts/tinyml|TinyML]] — KD is one of the algorithm-side TinyML compression levers
- [[concepts/lightweight-cnn-families|Lightweight CNN Families]] — KD is used by DeiT to distill inductive bias from CNN teachers into transformer students

## Related Sources

- [[sources/liu-2024-lightweight-dl-survey|Liu et al. 2024: Lightweight Deep Learning for Resource-Constrained Environments]] — introduces the three-paradigm taxonomy with comparison table (Table 6)
