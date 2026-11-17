---
type: concept
created: 2026-11-17
updated: 2026-11-17
sources:
  - raw/papers/li-2024-dbccrn/full-text.md
tags:
  - neural-network-architecture
  - speech-enhancement
  - complex-spectrogram
  - dual-branch-network
---

# DBCCRN (Dual-Branch Complex Convolutional Recurrent Network)

DBCCRN (Li, Sun, Zhang & Van hamme 2024) is a dual-branch extension of DCCRN for monaural [[concepts/speech-enhancement|speech enhancement]]: two mirrored complex-valued encoder–decoder branches estimate **clean speech and noise simultaneously** from the noisy complex spectrogram, instead of predicting speech alone. The design descends from the dual-stream speech/noise separation idea of Chen & Zhang (2021) (distinct from DBNet's frequency/waveform dual branches), instantiated entirely in the complex-spectral domain.

## Architecture

- **Front/back-ends**: differentiable Conv-STFT and iSTFT (Hann 512, hop 128, FFT 512 at 16 kHz).
- **Per branch**: 5 complex conv blocks (channels {16, 32, 64, 128, 256}, kernel [3,3], stride [2,1], padding [1,2]; complex conv + complex BN + complex PReLU) → complex LSTM bottleneck (two real LSTMs of 1024 hidden units combined by the complex-linear rule) → 5 complex deconv blocks with skip connections (decoder channels 2× encoder).
- **Bridge blocks**: 1×1 complex convolutions coupling corresponding layers of the two branches bidirectionally — the mechanism that removes noise from the speech branch and speech from the noise branch (orthogonality of representations). Replacing them with element-wise addition costs 0.29 PESQ.
- **Conformer skips**: each block holds two conformers (time-axis and frequency-axis), MHSA 8 heads, linear expand/shrink ×4, three complex conv layers resizing the first feature dimension ×4; they pass local (conv) + global (attention) features from encoder to matching decoder layer.
- **Output**: each decoder's complex mask multiplies the noisy complex spectrogram; iSTFT yields $\hat{s}(t)$ and $\hat{n}(t)$.
- **Size**: 8.31 M parameters total; trained jointly with [[concepts/scale-aware-snr|SA-SNR]] on both branch outputs.

## Evidence (VoiceBank+DEMAND)

| Configuration | Params | PESQ | STOI | COVL |
|---|---|---|---|---|
| DBCCRN (full) | 8.31 M | 3.16 | 0.940 | 3.62 |
| − conformer | 8.09 M | 2.98 | 0.940 | 3.45 |
| − noise branch | 8.09 M | 2.84 | 0.931 | 3.34 |
| − bridge module | 7.40 M | 2.87 | 0.935 | 3.25 |
| DCCRN (capacity-matched, SI-SNR) | 8.40 M | 2.75 | 0.931 | 3.28 |

The noise branch is the cheapest large win (+0.32 PESQ for 0.22 M params, +1.05 CBAK); the estimated noise contains far less speech leakage than a single-branch model's residual. Zero-shot transfer to DNS 2020 matches a DNS-trained DCCRN (PESQ 2.220 vs 2.204); retraining reaches 2.638.

## Related Concepts

- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the CRN/DCCRN family it extends
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — complex-domain estimation (DBCCRN outputs masks, a CRM variant)
- [[concepts/scale-aware-snr|Scale-Aware SNR]] — the loss it is trained with
- [[concepts/scale-error|ScaleError]] — the companion evaluation metric
- [[concepts/si-sdr|SI-SDR / SI-SNR]] — the scale-blind loss family motivating SA-SNR

## Related Sources

- [[sources/li-2024-dbccrn|Li, Sun, Zhang & Van hamme 2024: DBCCRN]] — proposing paper