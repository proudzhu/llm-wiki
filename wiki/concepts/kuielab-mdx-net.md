---
type: concept
created: 2026-09-15
updated: 2026-09-16
sources:
  - raw/papers/luo-2022-band-split-rnn/full-text.md
tags:
  - music-source-separation
  - neural-networks
  - u-net
  - lightweight-model
---

# KUIELab-MDX-Net

KUIELab-MDX-Net is a two-stream neural network for four-stem music demixing (vocals/drums/bass/other), introduced by Kim et al. (MDX Workshop @ ISMIR 2021). It was designed under the ISMIR 2021 Music Demixing (MDX) Challenge's wall-clock separation limit, which state-of-the-art deep models (e.g., LaSAFT-Net) could not meet, and demonstrates that a compute-constrained ensemble can still reach state-of-the-art MUSDB18 quality.

## Architecture

The system comprises six networks, all trained separately:

- **Time-frequency branch**: four independent [[concepts/tfc-tdf-unet|TFC-TDF U-Net]] v2 models — one per stem, each with source-specific frequency cutoff and $n_{\mathrm{fft}}$ (vocals 6144, drums 4096, bass 16384, other 8192) — followed by a **Mixer**, a single $1\times1$ convolution layer that refines the four estimates (plus mixture) to remove cross-source residuals such as drum snare noise leaking into vocals.
- **Time-domain branch**: a frozen, pretrained Demucs (Défossez et al., 2021), used without fine-tuning.
- **Fusion**: per-source weighted average of the two streams' estimates (*blending*, Uhlich et al. 2017).

The three TFC-TDF-U-Net v2 efficiency modifications (multiplicative instead of concatenative U-connections, removal of all non-U skip connections, channel scaling of 32 per down/upsampling layer) cut parameters with negligible quality loss relative to v1.

## Results

- MUSDB18 median SDR (BSSEval v4): vocals 9.00, drums 7.33, bass 7.86, other 5.95 dB — best of all compared systems on vocals, drums, and other.
- MDX Challenge @ ISMIR 2021: 2nd place Leaderboard A, 3rd place Leaderboard B.

Ablations: v2 alone reaches 8.81/6.52/7.65/5.70; adding the Mixer gives up to +0.55 dB (drums); blending with Demucs up to +0.46 dB (bass); the full system adds both.

The compute-constrained frontier did not last long at the top of the quality ladder: [[sources/luo-2022-band-split-rnn|Luo & Yu 2022]]'s [[concepts/band-split-rnn|BSRNN]], trained only on MUSDB18-HQ, surpassed KUIELab-MDX-Net's cSDR on vocals (10.01 vs. 8.97), drums (9.01 vs. 7.20), and other (6.70 vs. 5.90) — while remaining slightly behind on bass (7.22 vs. 7.83) — establishing band-split modeling as the stronger frequency-domain design when compute is unconstrained.

## Related Concepts

- [[concepts/tfc-tdf-unet|TFC-TDF U-Net]]
- [[concepts/music-source-separation|Music Source Separation]]
- [[concepts/band-split-rnn|Band-Split RNN]]

## Related Sources

- [[sources/kim-2021-kuielab-mdx-net|Kim, Choi, Chung, Lee & Jung 2021: KUIELab-MDX-Net — A Two-Stream Neural Network for Music Demixing]]
- [[sources/luo-2022-band-split-rnn|Luo & Yu 2022: Music Source Separation with Band-Split RNN]]
