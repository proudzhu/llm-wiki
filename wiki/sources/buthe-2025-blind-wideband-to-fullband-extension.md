---
type: source
created: 2026-08-14
updated: 2026-08-14
sources:
  - raw/papers/buthe-2025-blind-wideband-to-fullband-extension/full-text.md
  - https://doi.org/10.48550/arXiv.2412.11392
  - zotero://select/items/0_2HT68ITY
tags:
  - bandwidth-extension
  - speech-coding
  - low-complexity
  - hybrid-dsp-dnn
  - adversarial-training
  - robustness
---

# Büthe & Valin 2025: A Lightweight and Robust Method for Blind Wideband-to-Fullband Extension of Speech

| | |
|---|---|
| **Authors** | [[entities/jan-buthe|Jan Büthe]], [[entities/jean-marc-valin|Jean-Marc Valin]] |
| **Affiliation** | Amazon Web Services |
| **Venue** | WASPAA 2025 (5 pages); preprint arXiv:2412.11392 |
| **Year** | 2025 |
| **Type** | Conference paper (preprint) |
| **DOI** | [10.48550/arXiv.2412.11392](https://doi.org/10.48550/arXiv.2412.11392) |
| **Zotero** | [2HT68ITY](zotero://select/items/0_2HT68ITY) |
| **Code** | [BBWENet](https://gitlab.xiph.org/xiph/opus/-/tree/waspaa_2025_bwe) (Python + C, in the Opus tree) |

## Summary

Büthe & Valin propose **BBWENet**, a lightweight blind bandwidth-extension (BWE) model that regenerates the fullband (0–24 kHz, 48 kHz sampling) content of wideband speech (0–8 kHz, 16 kHz sampling) without any side information. The model is a hybrid of classical time-domain BWE signal processing (pre-filtering → upsampling → extension → post-filtering) and a small DNN (~370 K params, ~140 MFLOPS / ~70 MMACS) that steers time-varying filters and sample-wise weights, using only 0.27 ms of lookahead. It combines two complementary extension mechanisms — a novel scale-preserving non-linearity for voiced parts and AdaShape-based spectral folding for unvoiced parts — and is trained with regression + frequency-domain adversarial losses on a 900+-speaker, 34-language TTS mixture with deliberate robustness augmentations. Paired with Opus 1.5, it significantly improves P.808 DCR quality at 6–12 kb/s, and at 9 kb/s statistically matches EVS at 9.6 kb/s and Opus 1.4 at 18 kb/s — a 45–50% bitrate reduction, showing blind BWE can match the quality of classical guided BWE.

## Problem Formulation

**Task.** Given a wideband speech signal $x_{16}(t)$ (16 kHz sampling, ~8 kHz bandwidth), estimate the fullband signal $y_{48}(t)$ (48 kHz sampling, ~24 kHz bandwidth) such that it is perceptually indistinguishable from a natively-recorded fullband signal. "Blind" means no side information about the source — in contrast to guided BWE, where the encoder transmits parameters (e.g., EVS superwideband extension, Opus hybrid highband).

**Why it matters.** Bandwidth reduction is standard practice in low-bitrate speech coding (G.711, AMR-WB, Opus SILK) and low-complexity vocoding (LPCNet). It preserves intelligibility but degrades listening experience and causes listener fatigue; a blind BWE can improve quality for billions of daily listeners, provided it is **low-complexity** (smartphone-class devices) and **robust** (huge input variability in real deployments).

**The gap.** Classical BWE methods (Makhoul & Berouti 1979; spectral folding, non-linear processing) have low complexity but struggle with *blind* highband estimation, working best with side information. DNN-based methods model the highband well but even "low-complexity" ones run at multiple GFLOPS (e.g., ~13 GFLOPS Soltanmohammadi et al. 2023; ~7 GFLOPS Gómez et al. 2023) — too heavy for mobile.

**Ill-posedness.** BWE is inherently ill-posed: the same source yields different recordings depending on acoustic environment and recording device. Fitting a model to a homogeneous dataset generalizes poorly (microphone channels matter critically). The authors therefore prioritize **plausibility and robustness over correctness**.

## Methodology

### Hybrid signal path

The model follows the classical pre-filter → upsampler → extension → post-filter structure [Makhoul & Berouti 1979]. The signal path consists only of classical DSP: a fixed non-linear mapping, fixed and time-varying linear filtering, and time-varying sample-wise weighting. **Only the time-varying filters and weights are adapted by a small DNN** governed by a latent feature sequence from a feature encoder.

- **Adaptive pre/post-filtering** via the [[concepts/adaconv|AdaConv]] module (from LACE, Büthe et al. WASPAA 2023), extended to multiple input/output channels (from NoLACE, ICASSP 2024). AdaConv is like Conv1d but the weights are adapted at a fixed rate (200 Hz) from the latent feature vector.
- **Upsampling** via the libopus 16-to-48-kHz upsampler: stage 1 upsamples ×2 with IIR filters, stage 2 performs 1.5× interpolation with short FIR filters. Low complexity, 13 samples delay at 48 kHz (total signal-path delay). IIR filters approximated by long FIR filters for training.

### Two complementary extension mechanisms

1. **Non-linear extension for voiced parts.** Applies a non-linearity that generates a consistent harmonic extension for quasi-periodic lowbands. The authors deviate from the usual choice (absolute value or ReLU) with a more aggressive non-linearity designed to approximately preserve signal scale and induce similar distortion regardless of input scale:
   $$f(x) = x \sin(\ln |x|)$$

2. **Spectral folding for unvoiced parts**, via the [[concepts/adashape|AdaShape]] module (from NoLACE). "Spectral folding" is used in a broader sense: multiplying the signal with a locally periodic sequence of non-negative weights computed from latent features:
   $$\text{AdaShape}(x(\cdot), \phi(\cdot))(n) = \alpha(n, \phi(\cdot), x(\cdot)) \cdot x(n)$$
   Folding — especially combined with spectral flattening as pre-filtering — effectively extends unvoiced parts. Post-hoc analysis (Figure 3) shows the model indeed uses folding mostly for unvoiced and the non-linearity mostly for voiced parts.

### Feature encoder

Inputs are simple to compute while capturing spectral envelope, pitch, and voicing: a Hanning-window STFT (20 ms window, 10 ms hop) yields a **32-band [[concepts/erb-scale|ERB-scale]] log-magnitude spectrogram** plus **complex phase differences** for the first 40 STFT bins:
$$\Delta\Phi(k,n) = \frac{X(n,k)\, X^{*}(n-1,k)}{|X(n,k)\, X^{*}(n-1,k)|}$$
The 72-dimensional feature vector is upsampled from 100 to 200 Hz and processed by a GRU for context accumulation. Phase differences are included because they proved sufficient for high-accuracy pitch estimation (Subramani et al. ICASSP 2024).

### Training strategy

- **Data**: mixture of high-quality TTS datasets — 900+ speakers, 34 languages. Items with very little high-frequency energy are filtered out (some datasets contain upsampled wideband/SWB recordings). 48 kHz targets are lowpass-filtered at 20 kHz to remove 44.1/48 kHz mixing ambiguity.
- **Robustness augmentations** (applied to the 48 kHz signal, then downsampled via a random lowpass with cutoff 7.5–8 kHz to form the input):
  1. Random EQ constant above 4 kHz on 40% of clips — prevents over-reliance on low frequencies
  2. Stationary wideband noise at random gain on 20% — teaches the model *not* to extend noise (extending noise makes the output sound noisier than the bandlimited input; this is an intentional design decision)
  3. Random RIR from the Aachen Impulse Response Database on 20% — robustness to reverberation
  4. Random DC offset on 10%
- **Pretraining** (regression only, 1 s segments, Adam, batch 256, lr $5\times10^{-4}$, weight decay $2.5\times10^{-5}$, 50 epochs):
  $$\mathcal{L}_{pre} = \tfrac{1}{13}\mathcal{L}_{env} + \tfrac{2}{13}\mathcal{L}_{spec} + \tfrac{10}{13}\mathcal{L}_{tdlp}$$
  where $\mathcal{L}_{env}$ (STFT envelope matching) and $\mathcal{L}_{spec}$ (spectral fine structure) come from LACE and are averaged over STFT resolutions with window sizes $3\cdot 2^n$, $6 \le n \le 11$, and $\mathcal{L}_{tdlp}$ is a time-domain $L^2$ loss on the low-frequency range (15-tap zero-phase lowpass, 4 kHz cutoff) enforcing lowband reconstruction.
- **Adversarial training** (0.9 s segments, batch 64, Adam, constant lr $10^{-4}$, 40 epochs): a *family of frequency-domain discriminators* — multi-layer 2D-conv on log-magnitude spectrograms with frequency-positional embeddings — rather than the common multi-scale/multi-period time-domain discriminators (faster convergence, higher quality). Adapted from NoLACE: STFT sizes ×3 (for the higher sampling rate), frequency-axis kernel 3×3 → 7×3, max channels capped at 64. $\mathcal{L}_{reg} = 0.6\,\mathcal{L}_{pre}$.

## Experimental Setup

| Aspect | Configuration |
|---|---|
| **Task** | Wideband (16 kHz) → fullband (48 kHz) blind BWE |
| **Model size** | ~370 K parameters; ~140 MFLOPS (~70 MMACS) |
| **Latency** | 10 ms frame + 0.27 ms lookahead; 13-sample signal-path delay |
| **Test material** | EARS dataset (regular speech category), 3 random sentence pairs/speaker, loudness-normalized; **EARS not in training data** |
| **Listening test** | Open-source P.808 DCR implementation (Naderi & Cutler 2020) |
| **Conditions** | Opus 1.5 (decoder complexity 10, i.e., with NoLACE enhancement) at 6/9/12 kb/s ± BWE; clean uncoded speech ± BWE; EVS at 9.6 kb/s; Opus 1.4 at 18 kb/s; EnCodec at 6/12 kb/s |
| **Significance** | $p = 0.95$ |

## Results

- **Coded speech**: BWE significantly improves Opus 1.5 at *all* tested bitrates (6/9/12 kb/s) and for clean uncoded input, even though the model was trained only on clean speech. The improvement at 6 kb/s is remarkable given the baseband already exhibits very audible distortion.
- **Matches guided BWE**: Opus 1.5 + BWE at **9 kb/s is statistically tied with 3GPP EVS at 9.6 kb/s** (which uses guided superwideband BWE) and with **Opus 1.4 at 18 kb/s** (hybrid-mode fullband coding). Equivalent quality is likely reached around 10 kb/s — a **45–50% bitrate reduction**.
- **vs. neural codecs**: EnCodec is better at 6 kb/s, but Opus 1.5 wideband at 9 kb/s already significantly outperforms EnCodec at 12 kb/s — likely reflecting EnCodec's lack of robustness to out-of-domain data (its reported quality is much higher). AudioDec degraded severely in pre-tests and was excluded. The authors read this as evidence that **hybrid DSP/DNN approaches are more robust than end-to-end neural codecs**.
- **Clean input**: BWE significantly improves quality vs. the fullband reference, but remains distinguishable from the original.

### Model inspection

Because the extension mixing is linear, the output can be decomposed as a sum of bypass + AdaShape + NonLin contributions:

![[raw/papers/buthe-2025-blind-wideband-to-fullband-extension/figures/fig1.png|Decomposition of y_32(t) and y_48(t) into bypass, AdaShape and NonLin contributions]]

*Figure 3: Decomposition of the intermediate and output signals. Spectrograms show AdaShape extends unvoiced speech, the non-linearity extends voiced speech; in the second (SWB→FB) stage, the extension is mainly AdaShape output plus imaging from the short FIR interpolation filters.*

- The dual approach is validated: omitting either the non-linearity or AdaShape causes audible degradation (informal blind listening).
- The second-stage NonLin could likely be omitted without quality loss, yielding a small complexity saving — suggesting the model mostly uses folding for SWB→FB extension.

## Key Contributions

1. **A lightweight blind BWE model** — ~370 K params, ~140 MFLOPS (~70 MMACS), 10 ms frame + 0.27 ms lookahead — deployable on older smartphones, built around the low-delay libopus upsampler.
2. **Hybrid DSP/DNN design**: classical time-domain BWE signal path (pre-filter → upsample → extension → post-filter) whose only learnable parts are time-varying AdaConv filters and AdaShape weights steered by a small feature-encoder DNN.
3. **Dual extension mechanisms**: a novel scale-preserving non-linearity $f(x) = x\sin(\ln|x|)$ for voiced parts and AdaShape-based spectral folding for unvoiced parts, with post-hoc linear decomposition showing the model indeed uses each where intended.
4. **Robustness-focused training**: 900+-speaker/34-language TTS mixture, EQ/noise/RIR/DC-offset augmentations, and a family of frequency-domain discriminators with frequency-positional embeddings; trained on clean speech yet consistently improves coded speech.
5. **Demonstrated codec benefit**: Opus 1.5 + blind BWE at 9 kb/s matches EVS 9.6 kb/s and Opus 1.4 18 kb/s (statistically tied), enabling backward-compatible quality improvement with 45–50% bitrate savings.

## Related Concepts

- [[concepts/blind-bandwidth-extension|Blind Bandwidth Extension]] — the task; classical vs. DNN methods and this hybrid
- [[concepts/adaconv|AdaConv]] — adaptive convolution module used for pre/post-filtering
- [[concepts/adashape|AdaShape]] — adaptive temporal shaping implementing spectral folding
- [[concepts/erb-scale|ERB Scale]] — 32-band ERB log-magnitude input features
- [[concepts/adaptive-convolution|Adaptive Convolution (Wang et al. 2025)]] — a different, frame-wise dynamic-convolution mechanism for SE; distinct from AdaConv
- [[concepts/percepnet|PercepNet]] — Valin's earlier low-complexity DSP/DNN hybrid for fullband SE

## Related Synthesis

(none — BBWENet is a single-task BWE paper; existing synthesis pages focus on SE model efficiency frontiers (e.g., Computational Efficiency Evolution tracks params/MACs/PESQ of SE models) and ANC/other tasks, none of which is materially advanced by this contribution. Tag-triage found no synthesis page sharing tags with this source.)
