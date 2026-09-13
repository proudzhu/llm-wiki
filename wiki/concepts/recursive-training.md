---
type: concept
created: 2026-09-13
updated: 2026-09-13
sources:
  - raw/papers/zhang-2024-enhanced-hybrid-ahs/full-text.md
tags:
  - deep-learning
  - training-strategy
  - acoustic-howling
  - closed-loop-systems
---

# Recursive Training

**Recursive training** is a training strategy for neural networks deployed inside feedback loops, in which the training signals themselves are generated *recursively through the model being trained*: each processed frame is fed back into the loop to synthesize the next frame's input, so the training distribution matches the closed-loop inference distribution exactly.

## The Problem It Solves

In [[concepts/acoustic-howling-suppression|acoustic howling suppression]], the deployed system sits inside an acoustic loop — the microphone signal at time $t$ depends on the AHS output at $t - \Delta t$:

$$y(t) = s(t) + [\hat{s}(t - \Delta t) \cdot G] * h(t)$$

Offline training strategies must synthesize microphone signals without the model in the loop:

- **Open-loop generation** (DeepMFC): use the unprocessed signal $y(t-\Delta t)$ — ignores AHS entirely
- **[[concepts/teacher-forcing|Teacher forcing]]** (DeepAHS, HybridAHS_v1): replace $\hat{s}$ with the ground-truth $s$ — tractable but still mismatched, since the deployed model's leakage differs from the clean teacher signal

Because howling is *self-reinforcing*, any residual leakage error compounds through the loop at inference — the mismatch does not stay bounded, it amplifies. Empirically this manifests as huge per-utterance variance (offline-trained models show ±5–15 dB SDR standard deviations vs ±1–2 dB for recursively trained ones) and collapse at high loop gain.

## The Method

During recursive training, the NN module is inserted into the simulated acoustic loop:

1. Process frame $m$: $\mathbf{E}_m \leftarrow \mathbb{K}(\mathbf{Y}_m, \mathbf{R}_m)$, then $\hat{\mathbf{S}}_m \leftarrow \mathbb{NN}(\mathbf{Y}_m, \mathbf{E}_m)$
2. Drive the loop with the model's own output: $\mathbf{R}_{m+1} \leftarrow$ delayed $\hat{\mathbf{S}}_m \cdot G$, and $\mathbf{Y}_{m+1} = \mathbf{S}_{m+1} + \mathbf{X}_m \cdot \mathbf{H}$
3. After the full utterance, compute the loss (utterance-level, over the frame-recursive forward pass) and update the NN parameters

Training and inference then execute the *identical* signal-generation procedure — the mismatch is eliminated by construction rather than mitigated.

## Trainability Strategies

Recursive training is unstable at initialization: a randomly initialized NN provides no suppression, so loop energy accumulates until floating-point overflow produces NaNs that poison the entire training batch. Two strategies make it converge ([[sources/zhang-2024-enhanced-hybrid-ahs|Zhang et al. 2024]]):

1. **Howling detection guard**: monitor the microphone amplitude; when it exceeds a threshold for ~100 consecutive samples, halt the utterance and compute the loss on the already-processed prefix — see [[concepts/howling-detection|howling detection]] repurposed from a deployment front-end to a training-time safety mechanism
2. **Offline-model initialization**: initialize the NN from a teacher-forced offline pre-trained model (HybridAHS_v1), turning recursive training into a *recursive fine-tuning* stage — the same two-stage pattern as [[concepts/closed-loop-fine-tuning|closed-loop fine tuning]] for hearing-aid DeepMFC

## Evidence

In Zhang et al. 2024 (TASLP), recursive training (HybridAHS_v2, NeuralKalmanAHS) is the only approach with positive SDR at loop gain $G=3$ where every offline-trained baseline is negative, with order-of-magnitude lower variance, and remains stable across the full gain range where the offline model collapses beyond $G \approx 2.2$.

## Scope and Related Ideas

- Recursive training generalizes [[concepts/teacher-forcing|teacher forcing]]'s domain: teacher forcing stabilizes training at the cost of mismatch; recursive training removes the mismatch at the cost of trainability (hence the guard strategies)
- It is the acoustic-loop instance of a broader pattern — training a component under the closed-loop dynamics it will face at deployment (cf. [[concepts/closed-loop-fine-tuning|closed-loop fine tuning]], [[concepts/real-time-recurrent-learning|real-time recurrent learning]], [[concepts/backpropagation-through-time|backpropagation through time]] for unrolled loops)

## Related Concepts

- [[concepts/teacher-forcing|Teacher Forcing]] — the offline alternative it supersedes
- [[concepts/closed-loop-fine-tuning|Closed-Loop Fine Tuning]] — the two-stage open-loop-then-closed-loop pattern
- [[concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — the application domain
- [[concepts/howling-detection|Howling Detection]] — trainability guard
- [[concepts/frequency-domain-kalman-filter|Frequency-Domain Kalman Filter]] — the adaptive module in the hybrid systems trained this way
- [[concepts/exposure-bias|Exposure Bias]] — the analogous mismatch in sequence generation

## Related Sources

- [[sources/zhang-2024-enhanced-hybrid-ahs|Zhang, Zhang, Yu & Yu 2024: Enhanced Acoustic Howling Suppression via Hybrid Kalman Filter and Deep Learning]] — introduces the paradigm, trainability strategies, and evidence
- [[sources/zhang-2024-neural-kalman-howling|Zhang 2024: Neural Network Augmented Kalman Filter for AHS]] — companion paper using streaming closed-loop training for NeuralKalmanAHS
- [[sources/zhang-2023-hybrid-ahs|Zhang 2023: Hybrid AHS]] — the offline (teacher-forced) precursor
