---
type: source
created: 2026-07-10
updated: 2026-07-10
sources:
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
  - https://arxiv.org/abs/2606.23332
  - https://doi.org/10.48550/arXiv.2606.23332
  - zotero://select/items/0_3F6BYI69
tags:
  - speech-enhancement
  - own-voice-cancellation
  - target-speaker-extraction
  - low-latency
  - real-time
  - linear-rnn
  - mamba
  - mingru
  - far-field
  - streaming
---

# Østergaard, Zahid, Ulbæk, Bagge, Olsen & Lindrup 2026: Own-Voice Cancellation

**Authors**: [[entities/mads-ostergaard|Mads Østergaard]]¹**, [[entities/alexander-neergaard-zahid|Alexander Neergaard Zahid]]¹, [[entities/karl-ulbaek|Karl Ulbæk]]¹, [[entities/andreas-hansen-bagge|Andreas Hansen Bagge]]¹², [[entities/kenny-falkjaer-olsen|Kenny Falkjær Olsen]]¹², [[entities/rasmus-malik-hoegh-lindrup|Rasmus Malik Høegh Lindrup]]³
**Affiliations**: ¹ WS Audiology, Lynge, Denmark; ² DTU Compute, Technical University of Denmark, Kgs. Lyngby, Denmark; ³ Verth, Denmark
**Venue**: arXiv preprint
**Year**: 2026
**Type**: Preprint
**DOI**: [10.48550/arXiv.2606.23332](https://doi.org/10.48550/arXiv.2606.23332)
**arXiv**: [2606.23332](https://arxiv.org/abs/2606.23332)
**Zotero**: [3F6BYI69](zotero://select/items/0_3F6BYI69)

## Summary

This paper introduces **own-voice cancellation (OVC)** — the task of removing a target (enrolled) speaker from a noisy multi-speaker mixture while preserving any remaining speech. Framed as the complement of [[concepts/target-speaker-extraction|target speaker extraction (TSE)]], OVC addresses latency-induced own-voice artifacts that arise when a far-field device streams enhanced audio back to the user: the round-trip time easily exceeds the 10 ms perceptual threshold, producing echo-like disturbance. The authors condition a time-domain model with only 2 ms algorithmic latency on a short enrollment utterance, benchmarking TD-SpeakerBeam alongside a lighter [[concepts/mamba-mingru|Mamba-MinGRU]] masker built from Mamba blocks with MinGRU temporal mixing. Replacing the ConvTasNet-based auxiliary network with a linear RNN encoder improves both SDR and predicted MOS while reducing compute, establishing OVC as a practical, low-latency enhancement objective for far-field denoising.

## Problem Formulation

Given an input mixture containing a target speaker $s$ (the own-voice), other speakers $i$, and noise:

$$\mathbf{y} = \mathbf{x}^{s} + \sum_{i \neq s} \mathbf{x}^{i} + \mathbf{n}$$

the goal of OVC is to recover the mixture with the enrolled speaker removed:

$$\bar{\mathbf{y}} = \sum_{i \neq s} \mathbf{x}^{i}$$

This is the complement of [[concepts/target-speaker-extraction|TSE]], which instead aims to recover $\mathbf{x}^{s}$.

![[raw/papers/ostergaard-2026-own-voice-cancellation/figures/f3f7c71afae26b62d3be4d215cf965c065f684d8b3ce8b9b981652b8ad320c05.jpg|Figure 1: OVC vs TSE]]

*Figure 1: Difference between own voice cancellation (OVC) and target speaker extraction (TSE). Given a mixture consisting of multiple speakers recorded in a noisy scene, TSE (right) aims to keep only the enrolled speaker, while OVC (left) removes only the enrolled speaker. Both methods jointly denoise and isolate speakers.*

### Motivation: Latency-Induced Own-Voice Artifacts

When a far-field device (e.g., a table-top microphone) captures, enhances, and streams audio back to the user, the acoustic round-trip time through the pipeline easily exceeds 10 ms. The user's own voice then arrives with a noticeable delay, producing perceptible echo-like artifacts. Delays beyond 15–20 ms are widely reported as disturbing, making own-voice suppression important for any streamed denoising system operating in far field.

## Methodology

### Architecture Overview

![[raw/papers/ostergaard-2026-own-voice-cancellation/figures/81ef8217fa729f13312c7836475d4741f929abc940f5d77f156df76e2b815df1.jpg|Figure 2: High-level architecture]]

*Figure 2: High-level architecture of a time-domain conditioned ConvTasNet. The two encoders do not share parameters. The output of the auxiliary network is an embedding applied using an adaptation layer.*

The system is a time-domain TasNet variant whose masking network is composed solely of Mamba blocks using [[concepts/mingru|MinGRU]] as the temporal mixer (denoted **Mamba-MinGRU**). The baseline is [[concepts/td-speakerbeam|TD-SpeakerBeam]]. The network consists of:

1. **Main network** — performs own-voice cancellation on the mixture waveform
2. **Auxiliary network** — extracts [[concepts/speaker-embedding|speaker embeddings]] from the enrollment utterance to condition the main network

### Mamba-MinGRU Block

![[raw/papers/ostergaard-2026-own-voice-cancellation/figures/bd4c63db88f113dbc6341fee6ea543c19c7b05b33db6e4c627c1ba2b799c55be.jpg|Figure 3: Mamba-MinGRU masker architecture]]

*Figure 3: Detailed architecture of the Mamba-MinGRU masker. It contains an initial normalization layer, followed by a projection to $d_{\mathrm{model}}$, and then N Mamba-MinGRU blocks. A final projection projects the predicted mask back to the encoder dimension and applies a Sigmoid non-linearity.*

Each Mamba-MinGRU block is a pre-norm residual block:

1. LayerNorm
2. Linear expansion by factor $K$, split into $y, z$
3. Short causal depthwise 1-D conv + SiLU
4. [[concepts/mingru|MinGRU]] recurrence as time mixing
5. Gating: $y \odot \text{SiLU}(z)$
6. Linear projection back to input channels

The MinGRU recurrence:

$$\mathbf{h}_{t} = (1 - \mathbf{z}_{t}) \odot \mathbf{h}_{t-1} + \mathbf{z}_{t} \odot \tilde{\mathbf{h}}_{t}$$

can be written as a linear recurrence and implemented using a parallel associative scan:

$$\mathbf{h}_{t} = \text{gates} \odot \mathbf{h}_{t-1} + \text{tokens}$$

Bidirectionality is implemented using Hydra bidirectionality.

### Auxiliary Network and Adaptation

Two auxiliary networks are investigated:

| Type | Configuration |
|------|---------------|
| ConvTasNet-based | Single repetition as in "Listen only to me!" |
| Linear RNN-based | Bidirectional, 5 blocks only |

Adaptation uses element-wise multiplication of the embedding and the intermediate representation. When skip connections are used, the auxiliary network outputs one embedding for the skip path and one for the residual.

### Loss Function

Negative thresholded SDR loss, extended to handle silence:

$$\mathbf{L}_{\mathrm{SDR}}(\hat{\mathbf{x}}, \mathbf{x}, \mathbf{y}) = \begin{cases} \mathcal{L}^{\text{active}}(\hat{\mathbf{x}}, \mathbf{x}), & \text{if } \mathbf{x} \neq \mathbf{0}, \\ \mathcal{L}^{\text{inactive}}(\hat{\mathbf{x}}, \mathbf{y}), & \text{if } \mathbf{x} = \mathbf{0}, \end{cases}$$

The active case (other speaker present):

$$\mathcal{L}^{\mathrm{active}}(\hat{\mathbf{x}}, \mathbf{x}) = -10 \log_{10}\left(\frac{\|\mathbf{x}\|^{2}}{\|\mathbf{x} - \hat{\mathbf{x}}\|^{2} + \tau \|\mathbf{x}\|^{2}}\right)$$

The inactive case (only enrolled speaker, network should predict silence):

$$\mathcal{L}^{\text{inactive}}(\hat{\mathbf{x}}, \mathbf{y}) = 10 \log_{10}\left(\|\hat{\mathbf{x}}\|^{2} + \tau \|\mathbf{y}\|^{2}\right)$$

with soft thresholds $\tau = 10^{-3}$ (active) and $10^{-2}$ (inactive).

## Experimental Setup

| Item | Detail |
|------|--------|
| **Training data** | LibriSpeech train-clean-360 + WHAM! noise (dynamic mixing) |
| **Evaluation data** | LibriSpeech test-clean; LibriMix multi-speaker (3, 4, 5 speakers) |
| **Sample rate** | 16 kHz |
| **Batch** | 2 s enrollment + 3 s mixture, batch size 8 |
| **Training** | 1M steps, AdamW, linear decay-to-zero schedule, lr $5 \times 10^{-4}$ |
| **Speaker drop probabilities** | $p_{o} = p_{e} = 10\%$ |
| **Mixture SNR (training)** | Speech: [−5, 5] dB; Noise: [0, 25] dB |
| **Eval conditions** | (F) full mixture, SNR [10, 20] dB; (D) denoising only, SNR [0, 10] dB |
| **TD-SpeakerBeam hyperparams** | $N=256, L=32, B=256, H=512, P=3, X=8, R=4$ |
| **Mamba-MinGRU (base)** | $K=2.0$, $d_{\mathrm{model}}=192$, 15 blocks, adaptation after 8th |
| **Mamba-MinGRU (small)** | $K=2.0$, $d_{\mathrm{model}}=128$, 15 blocks |
| **Algorithmic latency** | 2 ms (kernel size $L=32$ at 16 kHz) |
| **Metrics** | SDR, pMOS (DistillMOS) |
| **RTF measurement** | Intel Core i7-13700, single thread, ExecuTorch C++ runtime, 1 ms blocks |

## Results

### Main Results (Table 1)

| ID | Method | Task | Causal | RTF | SDR-F | SDR-D | pMOS-F | pMOS-D | Params main | Params aux | MACs main | MACs aux |
|----|--------|------|--------|-----|-------|-------|--------|--------|-------------|------------|-----------|----------|
| — | Mixture | — | — | — | −0.07 | 5.02 | 3.28 | 2.95 | — | — | — | — |
| (a1) | TD-SpeakerBeam | TSE | | | 13.66 | 1.14 | 3.15 | 1.55 | 4.94 | 1.66 | 4.97 | 1.67 |
| (a2) | TD-SpeakerBeam | TSE | ✓ | | 11.01 | 9.18 | 2.56 | 2.30 | 4.94 | 1.66 | 4.94 | 1.67 |
| (b1) | TD-SpeakerBeam | OVC | | | 13.42 | 14.78 | 3.19 | 3.26 | 4.94 | 1.66 | 4.97 | 1.67 |
| (b2) | TD-SpeakerBeam | OVC | ✓ | | 11.13 | 12.09 | 2.66 | 2.64 | 4.94 | 1.66 | 4.94 | 1.67 |
| (c1) | Linear RNN | OVC | | | 13.38 | 14.93 | 3.22 | 3.32 | 4.71 | 1.65 | 0.33 | 1.67 |
| (c2) | + Linear RNN emb. | OVC | | | 13.57 | 9.67 | 3.20 | 2.71 | 4.71 | 1.61 | 0.33 | 0.26 |
| (c3) | Linear RNN | OVC | ✓ | 1.69 | 11.50 | 12.46 | 2.76 | 2.71 | 4.72 | 1.65 | 0.33 | 1.67 |
| (c4) | + Linear RNN emb. | OVC | ✓ | 1.69 | 11.98 | 11.35 | 2.80 | 2.65 | 4.72 | 1.61 | 0.33 | 0.26 |
| (d1) | Linear RNN (small) | OVC | ✓ | 0.82 | 11.21 | 12.33 | 2.66 | 2.63 | 2.17 | 1.65 | 0.18 | 1.66 |
| (d2) | + Linear RNN emb. | OVC | ✓ | 0.82 | 11.47 | 11.25 | 2.71 | 2.55 | 2.17 | 1.63 | 0.18 | 0.26 |

### Key Findings

1. **OVC vs TSE difficulty**: OVC and TSE are comparably difficult (~13 dB SDR in the F condition); causal inference incurs a moderate drop for both.
2. **Mamba-MinGRU efficiency**: (c1) achieves 13.38 dB SDR with only 0.33 GMAC/s vs 4.97 GMAC/s for TD-SpeakerBeam — a 15× compute reduction.
3. **Linear RNN auxiliary encoder**: Replacing ConvTasNet auxiliary with linear RNN reduces auxiliary compute from 1.67 to 0.26 GMAC/s while improving SDR on F in all settings (c2: 13.57 dB). Trade-off: better F performance but drop in D (denoising).
4. **Small variant runs below real-time**: (d2) achieves 11.47 dB SDR at RTF 0.82 (single CPU thread) with 2 ms latency — suitable for real-time streaming.
5. **Comparison to SpeakerBeam-SS**: SpeakerBeam-SS reports RTF < 1 but with 20 ms algorithmic latency, which is above the perceptual threshold for own-voice artifacts. The proposed model achieves 2 ms latency.

### Pitch Analysis (Table 2)

| Condition | SDR (dB) |
|-----------|----------|
| (e1) Same pitch — high (>160 Hz) | 11.09 |
| (e2) Same pitch — low (<160 Hz) | 10.91 |
| (f1) Different pitch — enrolled high | 11.45 |
| (f2) Different pitch — enrolled low | 12.24 |

It is more difficult to remove own voice when both speakers have the same pitch. It appears slightly easier to remove own voice when the enrolled speaker has low $f_0$.

### Multi-Speaker Robustness

For mixtures with 3, 4, and 5 speakers, all evaluated models show ~2 dB SDR degradation with increasing number of speakers, as expected from the increasingly complex acoustic scene.

## Key Contributions

1. **Establish OVC as a novel objective**: Frame own-voice removal from a noisy mixture as a practical approach for mitigating latency-induced distortion in streamed far-field denoising, treating the user's voice as an unwanted signal to be suppressed.
2. **Compute-efficient Mamba-MinGRU architecture**: A linear RNN-based architecture matching ConvTasNet-based performance at a fraction of the compute, with only 2 ms algorithmic latency in all causal configurations.
3. **Linear RNN auxiliary encoders**: Demonstrate that auxiliary linear RNN-based encoders provide better speaker representations than ConvTasNet-based ones for speaker conditioning, at substantially lower compute.

## Related Concepts

- [[concepts/own-voice-cancellation|Own-Voice Cancellation (OVC)]]
- [[concepts/mamba-mingru|Mamba-MinGRU]]
- [[concepts/td-speakerbeam|TD-SpeakerBeam]]
- [[concepts/mingru|MinGRU]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement (PSE)]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/linear-recurrent-unit|Linear Recurrent Unit]]

## Related Synthesis

- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
