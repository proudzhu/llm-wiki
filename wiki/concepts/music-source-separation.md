---
type: concept
created: 2026-09-15
updated: 2026-09-16
sources:
  - raw/papers/kim-2021-kuielab-mdx-net/full-text.md
  - raw/papers/luo-2022-band-split-rnn/full-text.md
tags:
  - music-source-separation
  - source-separation
  - real-time-processing
  - band-split
---

# Music Source Separation

Music source separation (MSS) is the task of decomposing a mixed music recording into its constituent stems — conventionally vocals, drums, bass, and other — on MUSDB18(-HQ), the standard benchmark corpus. Unlike speech enhancement, MSS must produce four *correlated* outputs and a decoder that reconstructs every stem, making it harder at a given compute budget than speech-oriented separation.

## Performance–Compute Trade-off in Offline MSS

Compute constraints on offline MSS predate embedded deployment. The ISMIR 2021 Music Demixing Challenge enforced a separation-time limit that accuracy-focused state-of-the-art systems (LaSAFT-Net) could not meet; [[sources/kim-2021-kuielab-mdx-net|Kim et al. 2021]]'s [[concepts/kuielab-mdx-net|KUIELab-MDX-Net]] (2nd place Leaderboard A) was explicitly designed for this budget: a downsized [[concepts/tfc-tdf-unet|TFC-TDF U-Net]] v2 ensemble blended with a frozen pretrained time-domain Demucs. Despite the downsizing it achieved the best BSSEval-v4 median SDR of all compared systems on vocals (9.00), drums (7.33), and other (5.95 dB) on MUSDB18 — an early demonstration that the accuracy frontier of offline MSS is not reserved for the largest models, and that frequency-domain and waveform-domain errors are complementary enough to profit from simple weighted-average blending.

## Band-Split Frequency-Domain Modeling

[[sources/luo-2022-band-split-rnn|Luo & Yu 2022]]'s [[concepts/band-split-rnn|BSRNN]] marked the point where MSS architectures were designed around music-signal characteristics rather than imported from speech or vision: the mixture spectrogram is split into subbands with instrument-specific, non-uniform bandwidths (fine 100 Hz bands below 1 kHz for vocals, 50 Hz bands below 500 Hz for bass) and modeled by interleaved sequence-level and band-level residual BLSTMs. Trained only on MUSDB18-HQ, it outperformed every MDX Challenge 2021 top system on vocals (10.01 vs. 8.97 cSDR for KUIELab-MDX-Net), drums, and other; a semi-supervised self-boosting finetuning pipeline on 1750 unlabeled songs lifted vocals to 10.47 dB cSDR and added ~1 dB cSDR on bass and drums. The band-split bandwidth schedule itself is a first-class design lever — uniform 1 kHz splitting plateaus at ~8.1 dB vocal uSDR while fine low-frequency splitting reaches 10.04 dB — and the design migrated back into speech processing (full-band and personalized speech enhancement, BSDB-Net).

## Real-Time and Embedded MSS

The strongest systems (Hybrid Demucs, band-split RNN/transformer models) are large and offline, consuming a whole track at once. The real-time regime is much sparser: HS-TasNet demixes at 23 ms latency, and RT-STT matches that latency with ~0.4 M parameters. Both separate *algorithmic latency* from *computational efficiency* and report per-frame processing time — but on i7-class CPUs and RTX-class GPUs, not the low-power audio DSPs that hearing aids, in-ear monitors, and live-sound processors actually run on.

[[sources/li-2026-realtime-music-separation-dsp|Li et al. 2026]] showed that no published real-time MSS system satisfies the two constraints of a commercial audio DSP (2 MB SRAM, 2.07 GMAC/s measured): weight memory rules out the 16–51 M parameter TasNet/X-UMX family by 8.0–25.5×, while per-frame compute rules out RT-STT, which needs 5.5× the available MAC rate. Parameter count predicts neither failure (see [[concepts/weight-reuse-factor|weight reuse factor]]). They then built the first MSS system demonstrated on such a device: a causal [[concepts/tfc-tdf-unet|TFC-TDF U-Net]] with a gated [[concepts/deep-filtering|deep-filter]] head, trained with [[concepts/continuous-context-training|continuous-context training]], reaching 4.70 dB cSDR on MUSDB18-HQ in 10.43 ms of an 11.6 ms frame deadline.

## Evaluation Caveats

MSS quality metrics are not uniform across papers: cSDR (median over 1 s windows, silent reference windows gated) is a plain energy ratio and differs from BSSEval-v4 by up to ±1.3 dB per stem with inconsistent sign, so cross-paper comparisons are indicative only. Weight memory comparisons should assume int8 (the most generous case for the baselines); the deployed model of Li et al. 2026 uses float32 weights.

## Related Concepts

- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/band-split-rnn|Band-Split RNN]]
- [[concepts/tfc-tdf-unet|TFC-TDF U-Net]]
- [[concepts/kuielab-mdx-net|KUIELab-MDX-Net]]
- [[concepts/deep-filtering|Deep Filtering]]
- [[concepts/weight-reuse-factor|Weight Reuse Factor]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]

## Related Sources

- [[sources/li-2026-realtime-music-separation-dsp|Li, Liu, Malsky & Yi 2026: Real-Time Music Source Separation on a Low-Power Audio DSP]]
- [[sources/kim-2021-kuielab-mdx-net|Kim, Choi, Chung, Lee & Jung 2021: KUIELab-MDX-Net — A Two-Stream Neural Network for Music Demixing]]
- [[sources/luo-2022-band-split-rnn|Luo & Yu 2022: Music Source Separation with Band-Split RNN]]
