---
type: concept
created: 2026-08-30
updated: 2026-10-24
sources:
  - raw/papers/valin-2018-lpcnet/full-text.md
  - raw/papers/mezza-2024-hybrid-plc/full-text.md
tags:
  - signal-processing
  - speech-coding
  - source-filter-model
  - hybrid-dsp-dnn
  - packet-loss-concealment
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

## Linear Prediction as a Residual-Prediction PLC Model

PLC is the setting where linear prediction stops being merely a vocoder component and becomes a predictor in its own right. If a short-time signal follows $y[n]=\sum_{i=1}^{p}\varphi_i y[n-i]+\varepsilon[n]$, a receiver can fit $\{\varphi_i\}$ *online* on the received context (autocorrelation method + Levinson–Durbin over a sliding 100 ms window with 10 ms stride, conditioned by [[concepts/diagonal-loading|diagonal loading]]) and forecast the missing samples with $\varepsilon[n]=0$. Music is an unusually favourable case: sustained instrumental notes are quasi-harmonic outside attack transients, so a high-order all-pole model captures most of the short-time structure — [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]] find $\mathrm{AR}(128)$ alone beating every deep PLC baseline (FRN, TF-GAN, PLAAE, LPCNet) on NMSE, PEAQ and PLCMOS at 32 kHz, at ~1.8 ms per 10 ms packet.

What the linear model cannot supply is the **residual**, which is far from white for a finite-memory predictor. That is precisely the division of labor of [[concepts/parcnet|PARCnet]]: a feed-forward neural network predicts $\varepsilon[n]$ from the past $N$ samples and the result is added to the linear forecast. This is the same LPC-plus-learned-excitation philosophy as [[concepts/lpcnet|LPCNet]], but transposed from *synthesis* (where the network generates the excitation sample by sample) to *concealment* (where a frame-wise network estimates the excitation of an unknown packet). Linear prediction also earns its keep at the seams: the AR forecast continues the signal smoothly from the first predicted sample, which is why it can carry the first samples while the neural contribution is faded in.

## Related Concepts

- [[concepts/parcnet|PARCnet]] — PLC system whose learned branch models the linear predictor's residual
- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — online AR fitting as a standalone concealer (music/NMP)
- [[concepts/diagonal-loading|Diagonal Loading]] — white-noise compensation that conditions high-order AR fitting
- [[concepts/lpcnet|LPCNet]] — the WaveRNN + linear prediction hybrid vocoder
- [[concepts/wavernn|WaveRNN]] — the neural backbone that learns the excitation
- [[concepts/warped-linear-prediction|Warped Linear Prediction]] — frequency-warped LP variant approximating the Bark scale
- [[concepts/burg-spectral-estimation|Burg Spectral Estimation]] — maximum-entropy (LP-based) spectral estimation, an alternative LPC analysis route
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — the cepstral representation LPCNet derives its predictor from

## Related Sources

- [[sources/mezza-2024-hybrid-plc|Mezza, Amerena, Bernardini & Sarti 2024: Hybrid Packet Loss Concealment for Real-Time Networked Music Applications]] — online AR(32/64/128) PLC on music; AR(128) alone beats deep baselines, and its residual is learned by PARCnet
- [[sources/valin-2018-lpcnet|Valin & Skoglund 2018: LPCNet]] — the paper that recombined linear prediction with WaveRNN for sub-3-GFLOPS speech synthesis
