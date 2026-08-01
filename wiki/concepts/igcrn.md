---
type: concept
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2021-igcrn/full-text.md
  - raw/papers/zhao-2024-sicrn/full-text.md
tags:
  - neural-network
  - speech-enhancement
  - multi-channel
  - convolutional-recurrent-network
  - inplace-model
  - beamforming
---

# IGCRN

**IGCRN** (Inplace Gated Convolutional Recurrent Neural Network) is a compact end-to-end model for dual-channel speech enhancement, proposed by Liu & Zhang (Interspeech 2021). It is the foundation of the inplace-CRN model family and the direct predecessor of [[concepts/iccrn|ICCRN]]. The defining idea is the **inplace** design: convolutional kernels use stride 1 on the frequency dimension, so each frequency bin is processed independently throughout the encoder and decoder, preserving per-bin spatial cues that downsampling convolutions would alias away. A single [[concepts/channel-wise-lstm|channel-wise LSTM]] is reused across all frequency bins (analogous to applying one beamformer per bin with shared weights), making the model extremely compact (1.4 M parameters, 19.9 G MACs).

## Motivation: Mirror the Beamforming Pipeline

Traditional multi-channel speech enhancement via beamforming has three stages — DOA estimation, beamforming, and post-filtering — and **beamforming operates per frequency bin** because the spatial filter for each bin depends on the per-bin phase relationship between channels. The standard [[concepts/convolutional-recurrent-network|CRN]] architecture, by contrast, downsamples the frequency dimension with strided convolutions to encode spectral patterns into the channel dimension. For single-channel SE this is effective (it captures harmonic structure), but for multi-channel SE it **aliases spatial cues with spectral patterns**, making it hard for the recurrent layer to extract per-bin spatial information.

IGCRN resolves this by keeping the frequency dimension intact throughout the network (inplace convolutions), so the spatial cues in each bin are preserved explicitly and the recurrent layer can process each bin independently — like a beamformer.

| Traditional beamforming stage | IGCRN component |
|-------------------------------|------------------|
| DOA estimation / spatial cue extraction | Inplace encoder (6× inplace GLU) |
| Beamforming per frequency bin | Channel-wise LSTM (reused across bins) |
| Post-filtering / spectral reconstruction | Inplace decoder (6× inplace transpose GLU) |

The three stages do not exactly correspond to the traditional pipeline because the network is end-to-end — it learns the appropriate intermediate representations rather than relying on hand-crafted interfaces.

## Architecture

IGCRN follows a U-Net structure with skip connections:

1. **Input** — real and imaginary parts of the complex STFT of both channels stacked along the channel dimension, shape `[Batch, 4, F=256, Time]` (two channels × two components). iGLU1 projects this to channel size 2.
2. **Encoder** — 6 cascaded inplace GLU blocks (5×1 kernels, stride 1, output channel 64). Frequency dimension stays at $F = 256$ throughout.
3. **Bottleneck** — 2-layer bidirectional channel-wise LSTM (hidden size 64). The frequency dimension is folded into the batch dimension so the LSTM sees only the per-bin channel (= spatial) feature at each time step.
4. **Decoder** — 6 cascaded inplace transpose GLU blocks with skip connections; two parallel decoders predict (amplitude mask, amplitude mapping) and (phase real, phase imaginary), respectively.
5. **Output** — combined estimated complex spectrum via $X_{est} = A_{est} \otimes P_{est}$.

The inplace GLU is $Y = ELU(BN(iConv(X) \otimes Sigmoid(iConv(X))))$ where $iConv$ is the stride-1 inplace convolution.

The system uses 32 ms frames with 16 ms shift (sqrt-Hann window, 512-point DFT at 16 kHz).

## Training Target: Mask + Mapping + Phase

IGCRN's two-decoder output implements the [[concepts/mask-mapping-amplitude-prediction|mask + mapping + phase]] target:

$$A_{est} = A_{msk} \otimes A_{nsy} + A_{map}$$

$$P_{est} = \frac{P_{est_r} + j P_{est_i}}{\sqrt{P_{est_r}^2 + P_{est_i}^2}}$$

$$X_{est} = A_{est} \otimes P_{est}$$

This combines the complementary strengths of mask-based prediction (good at high SNR, reuses input features) and mapping-based prediction (good at low SNR), together with explicit phase estimation. Training uses the Phasen loss (Yin et al. 2020), a compressed-amplitude RI loss.

## Key Results

On simulated dual-channel mixtures (AISHELL-1 train, TIMIT test, NOISEX-92 noise, image-method RIRs at -3/0/3 dB SNR), IGCRN outperforms MVDR (given *true* DOA) and conventional GCRN in every condition. At -3 dB babble, IGCRN achieves STOI 0.96 / PESQ 3.75 / SDR 19.2 vs. GCRN's 0.85 / 2.59 / 3.3 and MVDR's 0.83 / 2.46 / 5.3.

The most striking ablation is the **downsampling sweep** (Table 5 of the paper): performance degrades monotonically as frequency downsampling is added, *even though model complexity grows by orders of magnitude*. `IGCRN64-6DS` has 777 M parameters (556× more than `IGCRN64`) and 430 G MACs (22× more) but worse STOI/PESQ. This is direct evidence that the inplace characteristic — not capacity — drives multi-channel SE performance in the time-frequency domain.

| Method | Params (M) | MAC (G) | -3 dB Babble STOI / PESQ / SDR |
|--------|------------|---------|--------------------------------|
| GCRN | 71.8 | 28.8 | 0.847 / 2.59 / 3.3 |
| **IGCRN64** (proposed) | **1.4** | **19.9** | **0.968 / 3.83 / 19.2** |
| IGCRN64-6DS | 777.3 | 430.8 | 0.949 / 3.51 / — |

## Position in the Inplace-CRN Lineage

- **IGCRN** (Liu & Zhang 2021, Interspeech) — inplace gated CRN for dual-channel SE; channel-wise LSTM preserves per-bin spatial cues. Also applied to mono and stereo AEC.
- **ICCRN** (Liu & Zhang 2023, ICASSP) — replaces GLU with the [[concepts/cepstral-frequency-block|Cepstral Frequency Block (CFB)]]; introduces cepstral-space processing; achieves SOTA low-SNR STOI on WSJ0 SI-84 at minimum complexity.
- **SICRN** (Zhao, He & Zhang 2024, arXiv) — first model outside the original Liu/Zhang line to adopt the inplace design; from the same lab ([[entities/xueliang-zhang|Xueliang Zhang]]'s group at Inner Mongolia University). Replaces standard convolution with the [[concepts/sic-block|SIC block]] (2D inplace conv + [[concepts/s4nd|S4ND]] + sigmoid attention) and addresses the same full-band-modeling gap that ICCRN's CFB addresses — but via a parallel state-space global branch rather than a cepstral transform. Targets single-channel SE on the [[concepts/dns-challenge|DNS Challenge]] rather than multi-channel SE.

The ICCRN paper notes that IGCRN's monaural performance was relatively weak because discarding frequency downsampling also discards full-band modeling capacity; ICCRN recovers that capacity by replacing the GLU with the CFB, which models speech in the cepstral space where harmonic structure is sparsely represented. SICRN tackles the same limitation by augmenting inplace convolution with a global S4ND branch in the SIC block, instead of changing the spectral domain.

## Related Concepts

- [[concepts/inplace-convolution|Inplace Convolution]] — the core architectural choice
- [[concepts/channel-wise-lstm|Channel-wise LSTM with Model Reuse]] — the compact recurrent bottleneck
- [[concepts/mask-mapping-amplitude-prediction|Mask + Mapping + Phase Target]] — the proposed training target
- [[concepts/iccrn|ICCRN]] — successor in the inplace-CRN lineage
- [[concepts/sicrn|SICRN]] — later member of the inplace-CRN lineage (same lab); augments inplace conv with S4ND
- [[concepts/sic-block|SIC Block]] — SICRN's novel module combining inplace conv with S4ND
- [[concepts/s4nd|S4ND]] — the multidimensional state space model used in SICRN's global branch
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — CRN family baseline
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — related training paradigm
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — broader task
- [[concepts/beamforming|Beamforming]] — traditional pipeline IGCRN mirrors
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — oracle baseline

## Related Sources

- [[sources/liu-2021-igcrn|Liu & Zhang 2021: IGCRN — Inplace Gated Convolutional Recurrent Neural Network]]
- [[sources/liu-2023-iccrn|Liu & Zhang 2023: ICCRN — Inplace Cepstral Convolutional Recurrent Neural Network]]
- [[sources/zhao-2024-sicrn|Zhao, He & Zhang 2024: SICRN — State Space Model + Inplace Convolution for Speech Enhancement]]
