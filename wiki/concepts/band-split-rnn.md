---
type: concept
created: 2026-09-16
updated: 2026-09-16
sources:
  - raw/papers/luo-2022-band-split-rnn/full-text.md
tags:
  - music-source-separation
  - source-separation
  - neural-network
  - band-split
  - frequency-domain
---

# Band-Split RNN (BSRNN)

**Band-Split RNN (BSRNN)** is a frequency-domain neural architecture for music source separation (MSS) introduced by Luo & Yu (2022). It splits the mixture spectrogram into subbands with **instrument-specific, non-uniform bandwidths** and models them with interleaved sequence-level and band-level residual BLSTMs — an instantiation of [[concepts/dprnn|dual-path]] modeling along the frequency axis rather than over time chunks. It was the first MSS architecture designed explicitly around music-signal characteristics (44.1 kHz super-wideband spectra, instrument-dependent frequency ranges and harmonics) instead of importing speech- or vision-designed architectures unchanged.

## Architecture

Three modules operate on the complex STFT $\mathbf{X} \in \mathbb{C}^{F \times T}$ (2048-point window, 512 hop, Hanning):

1. **Band split** — $\mathbf{X}$ is divided into $K$ subbands with bandwidths $\{G_i\}$, $\sum_i G_i = F$. Each band has its own layer-norm + FC mapping to a shared feature dimension $N = 128$, giving $\mathbf{Z} \in \mathbb{R}^{N \times K \times T}$. Because bandwidths differ, per-band normalization/FC layers are required.
2. **Band and sequence modeling** — 12 stacked modules, each a sequence-level RNN over $T$ (shared across the $K$ bands for parameter efficiency and parallelism) followed by a band-level RNN over $K$ (capturing cross-band dependencies per frame). Each is a residual block: group norm → BLSTM (hidden $2N = 256$) → FC.
3. **Mask estimation** — per-band layer norm + MLP (hidden $4N = 512$, tanh, GLU output) produces complex-valued T-F masks, merged into $\mathbf{M} \in \mathbb{C}^{F \times T}$; the target estimate is $\mathbf{S} = \mathbf{M} \odot \mathbf{X}$, inverted by iSTFT.

One model is trained per stem (vocals, bass, drums, other) — MSS cast as source extraction.

## Band-Split Schemes as Prior Knowledge

The central design lever is the **bandwidth schedule**, which encodes a priori knowledge of the target instrument:

| Stem | Scheme (finest first) | Bands |
|------|----------------------|-------|
| Vocals / other | 100 Hz below 1 kHz; 250 Hz to 4 kHz; 500 Hz to 8 kHz; 1 kHz to 16 kHz; 2 kHz to 20 kHz; rest as one band | 41 |
| Bass | 50 Hz below 500 Hz; 100 Hz to 1 kHz; 500 Hz to 4 kHz; 1 kHz to 8 kHz; 2 kHz to 16 kHz; rest as one band | 30 |
| Drums | 50 Hz below 1 kHz; 100 Hz to 2 kHz; 250 Hz to 4 kHz; 500 Hz to 8 kHz; 1 kHz to 16 kHz; rest as one band | 55 |

The ablation (V1–V7, vocal uSDR on MUSDB18-HQ) shows uniform 1 kHz splitting plateaus at ~8.1–8.2 dB, while merely splitting below 1 kHz into 100 Hz bands (V4) jumps to 9.51 dB — the low band carries the vocal F0 and first harmonics — and progressively finer low-frequency schemes reach 10.04 dB (V7). Different instruments favor different schedules.

## Relation to Prior Architectures

- **vs. DPRNN**: dual-path RNNs chunk the *time* axis for time-domain separation; with large STFT windows the chunking is less essential, and replacing the plain BLSTM by a dual-path RNN in BSRNN's sequence module gives no gain. BSRNN instead makes the *frequency* axis the second modeling dimension.
- **vs. group communication** ([[concepts/grouped-recurrent-neural-network|GRNN]]): group splitting was designed for time-domain features without frequency structure, so its intra-group modeling ignores sub-band order. BSRNN deliberately uses an order-sensitive band-level RNN because instruments have distinct frequency ranges and timbres.
- **vs. super-wideband speech models**: prior two-band (low/high) splits are coarse and leave intra-band dependencies unmodeled; BSRNN uses fine-grained splitting but stops short of per-frequency-bin modeling (as in some ASR/fullband-SE systems) to control complexity.

## Semi-Supervised Self-Boosting Finetuning

BSRNN ships with a finetuning pipeline that uses the pre-trained model $P$ as **both** source activity detector and pseudo-label generator: unlabeled segments where the mixture-to-separated energy difference exceeds 30 dB are taken as clean target/residual segments; the separated signals otherwise serve as pseudo-labels. A student $Q$ initialized from $P$ replaces $P$ whenever it wins on validation. On 1750 unlabeled songs this improved all four stems (~1 dB cSDR on bass and drums).

## Influence

BSRNN set a new MUSDB18-HQ state of the art (10.47 dB vocal uSDR with finetuning vs. 8.13 for Hybrid Demucs) and the band-split design migrated back into speech processing — e.g., high-fidelity full-band and personalized speech enhancement (Yu et al., Interspeech 2022) and band-split dual-branch models such as BSDB-Net (Fan et al., AAAI 2025). It is cited as the canonical example of "large and offline" MSS systems in real-time/embedded MSS analyses.

## Related Concepts

- [[concepts/music-source-separation|Music Source Separation]]
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/bidirectional-lstm|Bidirectional LSTM]]

## Related Sources

- [[sources/luo-2022-band-split-rnn|Luo & Yu 2022: Music Source Separation with Band-Split RNN]]
