---
type: concept
created: 2026-11-20
updated: 2026-11-22
sources:
  - raw/papers/pascual-2017-segan/full-text.md
  - raw/papers/fu-2019-metricgan/full-text.md
  - raw/papers/fu-2021-metricgan-plus/full-text.md
tags:
  - speech-enhancement
  - gan
  - time-domain
  - encoder-decoder
  - waveform-level
---

# SEGAN (Speech Enhancement Generative Adversarial Network)

**SEGAN** is the speech-enhancement [[concepts/generative-vs-discriminative-speech-enhancement|generative]] architecture introduced by [[entities/santiago-pascual|Pascual]], [[entities/antonio-bonafonte|Bonafonte]] & [[entities/joan-serra|Serrà]] ([[sources/pascual-2017-segan|Interspeech 2017]]): an adversarial-trained, fully convolutional encoder–decoder that maps a noisy **raw 16 kHz waveform chunk** plus a latent vector to an enhanced waveform chunk. It is the first GAN applied to speech enhancement and the first end-to-end waveform-level enhancement model.

## Architecture

The generator $G$ is an auto-encoder with no dense layers: **22 one-dimensional strided-conv layers**, filter width 31, stride $N=2$, [[concepts/activation-functions|PReLU]] activations. The encoder compresses 16384 samples (~1 s at 16 kHz) to a **thought vector** $\mathbf{c}$ of shape $8{\times}1024$; $\mathbf{c}$ is concatenated with a latent $\mathbf{z}\sim\mathcal{N}(\mathbf{0},\mathbf{I})$ of the same shape, and the decoder mirrors the encoder with transposed convolutions. Encoder widths (samples × feature maps): $16384{\times}1$, $8192{\times}16$, $4096{\times}32$, $2048{\times}32$, $1024{\times}64$, $512{\times}64$, $256{\times}128$, $128{\times}128$, $64{\times}256$, $32{\times}256$, $16{\times}512$, $8{\times}1024$; decoder maps are doubled because **skip connections** and $\mathbf{z}$ are concatenated at every level. Strided convolutions were chosen over pooling for GAN stability, and skips carry fine-grained waveform detail (phase, alignment) around the bottleneck — the same 1-D instantiation of the [[concepts/u-net|U-Net]] idea.

The discriminator $D$ reuses $G$'s encoder stack as a classifier: two input channels of 16384 samples (real pair $(\tilde{\mathbf{x}}, \mathbf{x})$, fake pair $(\tilde{\mathbf{x}}, \hat{\mathbf{x}})$), conv1d + **virtual batch-norm** + LeakyReLU($\alpha = 0.3$), and a final **1×1 convolution with a single filter and no downsampling** in place of a dense layer — reducing that component from $8{\times}1024=8192$ to 8 parameters and making the channel merge learnable.

## Training Objective

[[concepts/least-squares-gan|Least-squares GAN]] losses (cross-entropy's sigmoid saturates into vanishing gradients), conditioned on the noisy signal, plus an $L_1$ sample-domain anchor:

$$\min_{G} V_{\text{SEGAN}}(G) = \tfrac{1}{2}\mathbb{E}_{\mathbf{z},\tilde{\mathbf{x}}}\left[(D(G(\mathbf{z},\tilde{\mathbf{x}}),\tilde{\mathbf{x}})-1)^2\right] + \lambda\,\lVert G(\mathbf{z},\tilde{\mathbf{x}}) - \mathbf{x}\rVert_1$$

with **$\lambda = 100$**. At $\lambda = 1$ the $L_1$ term sat two orders of magnitude below the adversarial term and had no practical effect; at 100 it minimizes while the adversarial term reaches equilibrium. The pairing of a generative objective with an $L_1$ regression term is the pattern later reused by metric-oriented GAN systems (MetricGAN, CMGAN), and the adversarial objective is what the paper argues is needed because MAE/MSE presuppose a unimodal output distribution and bias the estimate toward the conditional mean.

## Reported Performance (VoiceBank+DEMAND, 824 test files)

| Metric | Noisy | Wiener | SEGAN |
|:-------|:------|:-------|:------|
| PESQ | 1.97 | **2.22** | 2.16 |
| CSIG | 3.35 | 3.23 | **3.48** |
| CBAK | 2.44 | 2.68 | **2.94** |
| COVL | 2.63 | 2.67 | **2.80** |
| SSNR | 1.68 | 5.07 | **7.73** |
| MOS (16 listeners) | 2.09 | 2.70 | **3.18** |

SEGAN trails Wiener on PESQ (attributed to adversarial high-frequency artifacts) but leads on every distortion/intrusiveness metric and on subjective preference (67% vs the noisy signal, 53% vs Wiener).

## Lineage

SEGAN is the opening entry of the [[concepts/time-domain-speech-enhancement|time-domain]] lineage — AECNN, Conv-TasNet and DEMUCS follow it. Its own generator design was reused almost verbatim: [[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019]]'s AECNN is a SEGAN-shaped U-Net trained with STFT-magnitude MAE instead of an adversarial loss, at ~6.4 M parameters versus SEGAN's ~58 M (external estimate), and beats SEGAN on STOI/PESQ — the first evidence that the adversarial term was not the most sample-efficient route to better perceptual metrics. Later generative SE work largely abandoned a latent $\mathbf{z}$ looped through the generator's bottleneck, keeping only the adversarial *objective*. The most consequential successor disagrees even about that: [[sources/fu-2019-metricgan|MetricGAN (2019)]] measures SEGAN's-style conventional adversarial term as *inert* for SE (IRM(CGAN) 2.002 PESQ vs IRM(L1) 2.033 at matched generator, and no listener preference) and replaces the real/fake objective with a **learned surrogate of the evaluation metric** — keeping the adversarial training loop but changing what the discriminator means.

## Related Concepts

- [[concepts/metricgan|MetricGAN]] — the successor that repurposes the discriminator as a metric surrogate

- [[concepts/least-squares-gan|Least-Squares GAN (LSGAN)]] — the objective SEGAN adopts and extends
- [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/u-net|U-Net]] — the skip-connected encoder–decoder topology, in 1-D
- [[concepts/activation-functions|Activation Functions]] — PReLU in $G$, LeakyReLU in $D$
- [[concepts/invalid-stft-problem|Invalid STFT Problem]] — avoided by generating samples directly
- [[concepts/voicebank-demand|VoiceBank+DEMAND]] · [[concepts/pesq|PESQ]]

## Related Sources

- [[sources/pascual-2017-segan|Pascual, Bonafonte & Serrà 2017: SEGAN]] — the original paper
- [[sources/pandey-2019-cnn-speech-enhancement-time-domain|Pandey & Wang 2019: AECNN]] — reuses the generator shape with a frequency-domain loss; benchmarks SEGAN at ~58 M params
- [[sources/shetu-2026-generative-discriminative-comparison|Shetu, Habets & Brendel 2026]] — controlled study showing single-step GAN training is the robustness/efficiency sweet spot among training paradigms
- [[sources/fu-2021-metricgan-plus|Fu et al. 2021: MetricGAN+]] — SEGAN is the 2.16-PESQ baseline in its Table 3; the metric-surrogate line reaches 3.15 with a small BLSTM mask estimator — the benchmark-scale gap between conventional adversarial and metric-oriented training
