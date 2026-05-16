---
type: source
created: 2026-05-06
updated: 2026-05-06
sources:
  - raw/patents/us20260073929a1/full-text.md
  - https://patents.google.com/patent/US20260073929A1/en
  - zotero://select/items/0_Q833LYDX
tags:
  - bone-conduction
  - speech-enhancement
  - asr
  - conformer
  - earbuds
  - google
  - patent
---

# Heitkaemper et al. 2026: BCS-Guided Speech Enhancement for Voice Assistant on Earbuds

**Inventors**: [[entities/jens-heitkaemper|Jens Heitkaemper]], [[entities/joseph-caroselli-jr|Joseph Peter Caroselli Jr.]], [[entities/max-mckinnon|Max McKinnon]], [[entities/arun-narayanan|Arun Narayanan]], [[entities/nathan-howard|Nathan David Howard]]
**Assignee**: Google LLC
**Type**: US Patent Application
**Patent Number**: US20260073929A1
**Filed**: 2025-07-25
**Published**: 2026-03-12
**URL**: [Google Patents](https://patents.google.com/patent/US20260073929A1/en)
**Zotero**: [Q833LYDX](zotero://select/items/0_Q833LYDX)

## Summary

Proposes a [[concepts/bcs-guided-speech-enhancement|BCS-guided speech enhancement]] model for earbud voice assistants that fuses a single-channel noisy air-conducted signal with an upscaled [[concepts/bone-conduction|bone conducted signal]] (BCS) from an accelerometer in a Conformer-based architecture. The model estimates an ideal ratio mask via a stack of self-attention blocks, reconstructs enhanced speech via inverse STFT, and uses a BCS-based [[concepts/voice-activity-detection|VAD]] to gate ASR processing. Training uses a two-stage approach: pre-training on spectral + ASR loss, then fine-tuning with the BCS upscaling pathway.

## Problem Formulation

Earbud-based ASR systems degrade severely in low-SNR and overlapping-speech environments. Air-conducted microphones capture both target speech and ambient noise, while [[concepts/bone-conduction|BCS]] accelerometers capture primarily the user's own voice but are band-limited (typically < 1–2 kHz). The challenge is to effectively fuse these complementary modalities for robust speech enhancement.

**Input signals**:
- $x_{\text{air}}[n]$: single-channel noisy air-conducted signal (microphone)
- $x_{\text{BCS}}[n]$: bone conducted signal (accelerometer)

**Goal**: Estimate enhanced speech $\hat{s}[n]$ corresponding to the target utterance, optimized for downstream ASR performance.

## Methodology

### Architecture Overview

The speech enhancement model 300 comprises five components:

1. **Down-sampling block** (310): Reduces BCS STFT bandwidth by multiplying the maximum frequency bin by a factor of two
2. **Feed-forward upscaling projection layer** (320): Projects band-limited BCS features into a higher-dimensional space matching the air-conducted signal dimensionality
3. **Stack of Conformer blocks** (330): Self-attention-based processing of concatenated air + upscaled BCS features
4. **Masking layer** (340): Generates an estimated ratio mask from the Conformer output
5. **Inverse STFT layer** (350): Reconstructs enhanced waveform from masked STFT

### Processing Pipeline

```
BCS STFT → Down-sampling → FF Upscaling ──┐
                                            ├→ Concatenate → Conformer Stack → Masking Layer → iSTFT → Enhanced Speech
Air-conducted STFT ────────────────────────┘
```

**Key design choices**:
- **Single-channel air signal**: Model is agnostic to the number of microphones in the earbud array; uses a single channel (selected or combined)
- **BCS upscaling**: Band-limited BCS is projected to full bandwidth via learned feed-forward layer, not simple interpolation
- **Ratio mask estimation**: Model estimates an ideal ratio mask applied to the original STFT coefficients, preserving phase information

### Training: Two-Stage Approach

**Stage 1 — Pre-training**:
- Train: Conformer stack + masking layer
- Loss: $\mathcal{L}_{\text{spectral}} = L_1(\hat{M}, M_{\text{ideal}}) + L_2(\hat{M}, M_{\text{ideal}})$
- Ideal ratio mask $M_{\text{ideal}}$ computed using reverberant speech and reverberant noise
- ASR loss: Compare ASR encoder outputs for enhanced vs. target speech features
- BCS upscaling pathway NOT trained in this stage

**Stage 2 — Fine-tuning**:
- Train: FF upscaling projection + Conformer stack + masking layer
- Same spectral + ASR loss
- BCS upscaling pathway now included in training

### VAD Gating

A pre-trained [[concepts/voice-activity-detection|VAD]] processes the BCS to determine if the user is speaking:
- **VAD active** (speech detected): ASR processes enhanced speech features
- **VAD inactive** (no speech): ASR processes raw single-channel noisy signal directly (bypassing enhancement)

This prevents the enhancement model from introducing artifacts during non-speech segments.

## Key Contributions

1. **BCS-air fusion via Conformer**: First patent to propose concatenating upscaled BCS STFT with air-conducted STFT in a Conformer-based architecture for earbud speech enhancement
2. **BCS upscaling pathway**: Feed-forward projection layer that maps band-limited BCS features to full-bandwidth representation, enabling effective fusion with air-conducted features
3. **Two-stage training**: Pre-train without BCS upscaling, then fine-tune with it — stabilizes training by first learning the core masking behavior
4. **Mic-agnostic design**: Single-channel input makes the model compatible with any earbud regardless of microphone count
5. **BCS-based VAD gating**: Uses the noise-robust BCS for speech detection to control ASR pathway selection
6. **Joint spectral + ASR loss**: Optimizes for both signal-level quality and downstream recognition accuracy

## Related Concepts

- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]

## Related Synthesis

- [[synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]]
