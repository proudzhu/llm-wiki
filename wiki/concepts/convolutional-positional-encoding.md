---
type: concept
created: 2026-11-22
updated: 2026-11-22
sources:
  - raw/papers/fu-2020-metricgan-post-processing/full-text.md
tags:
  - transformer
  - positional-encoding
  - speech-enhancement
  - causal-model
---

# Convolutional Positional Encoding

**Convolutional positional encoding** replaces the Transformer's additive positional encoding with a stack of (causal) 1-D convolutional layers that inject *relative* location information into the frame sequence. [[sources/fu-2020-metricgan-post-processing|Fu et al. (APSIPA ASC 2020)]] propose it for causal speech enhancement and show that the standard fixed positional encoding is not merely unnecessary for SE but actively harmful.

## Motivation

Self-attention is permutation-equivariant, so a Transformer needs some positional signal. The two standard options each fail a requirement of streaming SE:

| Option | Problem for SE |
|:--|:--|
| Learned positional embeddings | Fixed maximum sequence length — cannot handle utterances longer than those seen in training |
| Fixed (sinusoidal) encoding | Length-flexible, but handcrafted features "may not be rich enough for embedding"; added to every frame's spectrum regardless of local content |

A convolutional stack instead derives location information from the local spectro-temporal context itself: flexible in sequence length, learned rather than handcrafted, and causal when the convolutions only look backwards.

## Formulation (Fu et al. 2020)

The noisy log1p-compressed magnitude spectrogram (257 bins, 16 ms hop) passes through four causal 1-D convs — (1024, k3, s1) → (512, k3, s1) → (128, k3, s1) → (256, k3, s1) — before the attention blocks. Causality is completed by two further mechanisms:

- **Future-masked attention**: $\mathrm{Attention}(Q_h,K_h,V_h)=\mathrm{softmax}\big(M + Q_hK_h^{T}/\sqrt{d_k}\big)V_h$ with $M$ strictly upper-triangular $-\infty$, zeroing attention to future frames.
- **Channel-only layer normalization**: moments computed across the channel dimension only, never across time, so normalization cannot leak future statistics.

## Evidence

On the DNS Challenge 2020 synthetic no-reverb validation set, the *same* Transformer with additive fixed positional encoding versus the convolutional encoding:

| Variant | PESQ | STOI |
|:--|:--|:--|
| Noisy input | 2.454 | 0.915 |
| Transformer (fixed additive PE) | 2.429 | 0.894 |
| Transformer (conv encoding) | 2.966 | 0.932 |

The PE variant falls **below the noisy input** on PESQ — a rare measured negative result for a standard Transformer component. The conv-encoding swap is worth +0.537 PESQ / +0.038 STOI, dwarfing the +0.138 PESQ that MetricGAN fine-tuning adds on top.

The design echoes convolutional sequence-to-sequence learning (Gehring et al., ICML 2017, cited as [18]) and precedes the convolution-augmented attention of the Conformer family, though the paper frames it as positional-information injection rather than local-feature modeling.

## Related Concepts

- [[concepts/attention-mechanism|Attention Mechanism]] — the masked MHSA this encoding feeds
- [[concepts/metricgan|MetricGAN]] — the fine-tuning framework applied on top of this backbone
- [[concepts/dns-challenge|DNS Challenge]] — the evaluation setting
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/fu-2020-metricgan-post-processing|Fu et al. 2020: Boosting Objective Scores by MetricGAN Post-Processing]] — introduces the causal conv encoding for SE and measures the fixed-PE penalty
