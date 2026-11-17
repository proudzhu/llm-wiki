---
type: concept
created: 2026-11-17
updated: 2026-11-17
sources:
  - raw/papers/li-2024-dbccrn/full-text.md
tags:
  - evaluation-metric
  - speech-enhancement
  - scale-preservation
---

# ScaleError (and the Scaled Test Set)

ScaleError (Li et al. 2024) measures the **amplitude drift** between enhanced and clean speech — a failure mode invisible to PESQ/STOI/COVL, which tolerate arbitrary output scaling when evaluated on level-controlled test sets.

## Formulation

$$
\text{ScaleError}(\hat{s}, s) = \Bigl(\max_{0 \le i \le n} |\hat{s}_i| - \max_{0 \le i \le n} |s_i|\Bigr)^2
$$

Squared difference of peak amplitudes; lower is better (reported in % in the paper's tables). Peak-based rather than energy-based, because clipping in playback is driven by peaks exceeding $[-1,1]$.

## Scaled-test-set recipe

The companion evaluation protocol: peak-normalize every test waveform into $[-1,1]$ (the **scaled test set**) and re-evaluate. Models trained with scale-blind losses ([[concepts/si-sdr|SI-SNR]], OSI-SNR) degrade sharply because their output scale tracks the input scale; scale-aware models barely move. On VoiceBank+DEMAND (DBCCRN):

| Loss | PESQ original → scaled | ScaleError original → scaled (%) |
|---|---|---|
| SI-SNR | 2.89 → 2.50 | 18.653 → 5.769 |
| OSI-SNR | 2.96 → 2.49 | 19.791 → 5.962 |
| [[concepts/scale-aware-snr\|SA-SNR]] | 3.16 → 3.15 | 0.014 → 0.057 |

(SI-SNR's ScaleError *drops* on the scaled set only because normalized inputs cap the output overshoot — PESQ still collapses.) The recipe simulates real-world input-level variation without new recordings.

## Why it matters

Standard SE benchmarks mix at fixed SNRs with level-controlled waveforms, so a model can score well while emitting speech at 4× the input amplitude — which clips in any $[-1,1]$ audio pipeline. ScaleError + the scaled test set make this measurable; [[concepts/scale-aware-snr|SA-SNR]] is the paper's training-side fix, and Table 5 shows the common inference-side fix (per-segment normalization) is worse than the disease in streaming (SSNR −7.96 dB).

## Related Concepts

- [[concepts/scale-aware-snr|Scale-Aware SNR]] — the loss that minimizes scale drift
- [[concepts/si-sdr|SI-SDR / SI-SNR]] — scale-blind losses this metric exposes
- [[concepts/pesq|PESQ]] — quality metric that misses scale errors
- [[concepts/dbccrn|DBCCRN]] — model evaluated with this recipe

## Related Sources

- [[sources/li-2024-dbccrn|Li, Sun, Zhang & Van hamme 2024: DBCCRN]] — proposing paper