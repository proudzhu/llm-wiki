---
type: concept
created: 2026-08-30
updated: 2026-08-30
sources:
  - raw/papers/valin-2018-lpcnet/full-text.md
tags:
  - signal-processing
  - speech-coding
  - source-filter-model
  - hybrid-dsp-dnn
---

# Linear Prediction

**Linear prediction (LP)** is the classical speech-analysis technique in which each speech sample is predicted as a linear combination of the $M$ previous samples, so that an all-pole filter models the vocal-tract (spectral-envelope) response of the source–filter speech production model. It has been the backbone of low-bitrate speech coding since Atal & Hanauer (1971) and the LPC vocoder of Markel & Gray (1974), and — via CELP — remains the core of modern codecs such as Opus/SILK.

## Key Formulations

The one-step prediction of the signal $s_t$ from its past is

$$
p_{t}=\sum_{k=1}^{M}a_{k}\,s_{t-k},
$$

where $a_{k}$ are the $M$-th order linear prediction coefficients (LPC) for the current frame. The **excitation** (prediction residual) is the prediction error $e_{t}=s_{t}-p_{t}$; conversely, synthesis reconstructs the signal by filtering the excitation with the all-pole synthesis filter

$$
s = \frac{e}{1-P(z)},\qquad P(z)=\sum_{k=1}^{M}a_{k}z^{-k}.
$$

The coefficients are conventionally computed per frame with the autocorrelation method and the **Levinson-Durbin** recursion (Makhoul's 1975 tutorial review remains the standard reference).

### LPC from a cepstrum

When the predictor must be derived from compact conditioning features rather than the signal itself, the LPC analysis chain is: cepstral coefficients → linear-frequency power spectral density → auto-correlation (via inverse FFT) → Levinson-Durbin. This is how [[concepts/lpcnet|LPCNet]] obtains its predictor from the 18-band Bark-frequency cepstrum, so that no information beyond the conditioning features needs to be transmitted or synthesized. The resulting analysis is less accurate than one computed on the signal (the cepstrum's resolution is low), but a neural network trained alongside it learns to compensate — an advantage over *open-loop* filtering approaches that apply a fixed filter to a separately generated excitation.

## Linear Prediction as a Neural-Network Complement

Classical low-bitrate vocoders modeled the spectral envelope efficiently with linear prediction but had no good model for the **excitation** — the reason their quality was "severely limited". Neural vocoders (WaveNet, WaveRNN, SampleRNN) inverted the trade-off: they model the entire production process including the excitation, at very high computational cost. The hybrid idea underlying LPCNet is to let the linear predictor handle what it does well (the spectral envelope) and dedicate the network's capacity to what has no simple model (the spectrally flat excitation):

| Approach | Spectral envelope | Excitation |
|----------|------------------|------------|
| Classical LPC vocoder | Linear prediction | Crude (voiced/unvoiced model) |
| Pure neural vocoder | Learned (expensive) | Learned |
| **LPCNet hybrid** | Linear prediction (from features) | Learned (GRU network) |

The same philosophy appears in CELP (code-excited linear prediction), where an analysis-by-synthesis search replaces the learned excitation; LPCNet's training-time noise injection is explicitly designed to mimic the error-minimizing behavior of analysis-by-synthesis.

## Related Concepts

- [[concepts/lpcnet|LPCNet]] — the WaveRNN + linear prediction hybrid vocoder
- [[concepts/wavernn|WaveRNN]] — the neural backbone that learns the excitation
- [[concepts/warped-linear-prediction|Warped Linear Prediction]] — frequency-warped LP variant approximating the Bark scale
- [[concepts/burg-spectral-estimation|Burg Spectral Estimation]] — maximum-entropy (LP-based) spectral estimation, an alternative LPC analysis route
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — the cepstral representation LPCNet derives its predictor from

## Related Sources

- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]] — the paper that recombined linear prediction with WaveRNN for sub-3-GFLOPS speech synthesis
