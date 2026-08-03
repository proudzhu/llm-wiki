---
type: concept
created: 2026-08-03
updated: 2026-08-03
sources:
  - raw/papers/jiang-2026-lightweight-speech-enhancement-ssm-dsc/full-text.md
tags:
  - deep-learning
  - speech-enhancement
  - loss-function
  - speaker-classification
  - auxiliary-loss
---

# Classifier Loss

The **Classifier Loss** is an auxiliary speaker-classification loss introduced by Jiang, Gao, Wang, Zou & Liu (2026) for speech enhancement under human-voice interference. It attaches a lightweight speaker classifier to the masked feature representation and trains it jointly with the enhancement objective, forcing the encoder to capture speaker-discriminative features that anchor the target voice while suppressing competing talkers.

## Motivation

Speech enhancement under multi-talker interference is fundamentally harder than under stationary environmental noise — competing voices overlap spectrally with the target, making mask-based separation difficult. Prior work (UltraSpeech, Ding et al. 2022) showed that identifying speaker-related features enables the model to adapt to specific acoustic characteristics and improve separation performance.

The Classifier Loss leverages this insight as an auxiliary objective: rather than explicitly performing speaker separation, it forces the enhancement encoder to learn universal acoustic signatures of a single vocal identity during training, which at inference acts as a "perceptual filter" that groups coherent spectral components while discarding disjointed interference.

## Mathematical Formulation

The classifier module consists of two fully connected layers followed by a softmax activation, outputting a probability distribution over speakers. It is optimized using standard cross-entropy:

$$
\mathcal{L}_{\mathrm{Classifier}} = - \frac{1}{N} \sum_{i=1}^{N} \sum_{j=1}^{C} g_{i,j} \log(p_{i,j})
$$

where $N$ is the batch size, $C$ is the total number of speakers, $g_{i,j}$ is the ground-truth label (1 if sample $i$ belongs to speaker $j$, 0 otherwise), and $p_{i,j}$ is the predicted probability that sample $i$ belongs to speaker $j$.

### Integration with Generator Loss

The Classifier Loss is one of five components in the total generator loss:

$$
\mathcal{L}_G = \lambda_1 \mathcal{L}_{\mathrm{Mag}} + \lambda_2 \mathcal{L}_{\mathrm{Con}} + \lambda_3 \mathcal{L}_{\mathrm{Com}} + \lambda_4 \mathcal{L}_{\mathrm{Metric}} + \lambda_5 \mathcal{L}_{\mathrm{Classifier}}
$$

with weight $\lambda_5 = 0.1$ (alongside $\lambda_1 = 0.9$ for magnitude, $\lambda_2 = 0.1$ for STFT consistency, $\lambda_3 = 0.1$ for complex spectrum, $\lambda_4 = 0.05$ for metric).

## Two Complementary Mechanisms

The Classifier Loss enhances speech reconstruction through two distinct yet complementary pathways:

### 1. Speaker-Discriminative Guidance (Vocal Interference)

In multi-talker scenarios, the classification task during training forces the encoder to capture **universal acoustic signatures** that define a single vocal identity. At inference, the model acts as a perceptual filter:
- Identifies the most dominant timbre signature as an "acoustic anchor"
- Groups coherent spectral components belonging to that voice
- Discards disjointed interference from competing speakers

Additionally, it encourages **identity-aware energy allocation** in the feature space — by concentrating energy on the discriminative harmonic patterns of the target speaker, the model can effectively suppress competing voices even within overlapping frequency bands.

### 2. Structural Regularizer (Non-Vocal Noise)

In the presence of non-human noise, the Classifier Loss acts as a **structural regularizer**:
- Joint optimization for enhancement + identification guides the model to prioritize reconstruction of fundamental harmonic structures and phonetic integrity inherent to human speech
- This prior knowledge prevents overfitting to unstructured or stationary environmental noise patterns
- Non-human noise is recognized as lacking human-like acoustic coherence and is suppressed

The relative improvement is lower than in vocal scenarios because non-human noise already exhibits significant spectral disparity from speech, making the discriminative advantage of the classifier a secondary factor rather than a primary driver.

## Empirical Impact

The ablation in Table 4 of the source paper shows the Classifier Loss's differential impact:

| Condition | w/o Classifier Loss | w/ Classifier Loss | Δ PESQ |
|---|---|---|---|
| Vocal interference | 3.02 | 3.18 | **+0.16** |
| Non-vocal noise | 3.39 | 3.46 | +0.07 |

The **2.3× larger gain under vocal interference** (+0.16 vs +0.07) empirically validates the dual-mechanism hypothesis: speaker-discriminative guidance is the primary benefit, with structural regularization providing a smaller secondary benefit for non-vocal noise.

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]] — application domain
- [[concepts/state-space-model|State-Space Model]] — main backbone in the source paper
- [[concepts/lights4|lightS4]] — sequence module whose masked features feed the classifier

## Related Sources

- [[sources/jiang-2026-lightweight-speech-enhancement-ssm-dsc|Jiang, Gao, Wang, Zou & Liu 2026: Lightweight SE with SSM and DSConv]] — introduces the Classifier Loss
