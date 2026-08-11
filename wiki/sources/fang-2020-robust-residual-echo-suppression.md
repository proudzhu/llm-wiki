---
type: source
created: 2026-08-11
updated: 2026-08-11
sources:
  - raw/papers/fang-2020-robust-residual-echo-suppression/full-text.md
  - https://doi.org/10.1109/ICICSP50920.2020.9232011
  - zotero://select/items/0_PCS7RXHC
tags:
  - acoustic-echo-cancellation
  - residual-echo-suppression
  - power-spectral-density
  - double-talk
  - statistical-correlation
  - speech-enhancement
  - traditional-signal-processing
---

# Fang 2020: A Robust Residual Echo Suppression Algorithm Even During Double Talk

| Field | Value |
|-------|-------|
| **Authors** | [[entities/bingxiao-fang\|Bingxiao Fang]] |
| **Institution** | Beijing Sabine Technologies Co., Ltd, Beijing, China |
| **Published** | Proc. IEEE ICICS 2020 (Information, Communications and Signal Processing), Sep. 2020 |
| **Type** | Conference Paper |
| **DOI** | [10.1109/ICICSP50920.2020.9232011](https://doi.org/10.1109/ICICSP50920.2020.9232011) |
| **Zotero** | [PCS7RXHC](zotero://select/items/0_PCS7RXHC) |

## Summary

This paper proposes a [[concepts/residual-echo-suppression\|residual echo suppression]] (RES) algorithm that estimates the residual echo power spectral density (PSD) from the *statistical normalized correlation* between the AEC error signal and the echo replica, rather than relying on a voice activity detector (VAD / double-talk detector) or [[concepts/minimum-statistics\|minimum statistics]]. The estimate feeds an Ephraim-Malah-style spectral gain. Real recordings in a meeting room show the method outperforms a slow-attach-and-fast-decay baseline on both [[concepts/echo-return-loss-enhancement\|ERLE]] and [[concepts/speech-to-speech-distortion-ratio\|SSDR]], with improved robustness during double talk.

## Problem Formulation

The single-channel AEC signal model in the time and STFT domains is

$$y[n] = \mathbf{h}^\mathrm{T}[n]\,\mathbf{x}[n] = d[n] + s[n], \qquad Y(i,k) = X(i,k)^\mathrm{T} H(i,k) + S(i,k),$$

where $\mathbf{x}$ is the far-end reference, $d$ the acoustic echo, $s$ the near-end speech, and $\mathbf{h}$ the room impulse response. An NLMS adaptive filter $\mathbf{w}$ produces the echo replica $\hat{d} = \mathbf{w}^\mathrm{T}\mathbf{x}$, and the AEC error signal is

$$e[n] = s[n] - (\mathbf{h}-\mathbf{w})^\mathrm{T}\mathbf{x}[n] = s[n] - r[n],$$

where $r[n] = \mathrm{ISTFT}\{(H-W)^\mathrm{T}X\}$ is the *residual echo* — the portion of the echo the linear filter failed to remove. Residual echo persists because (1) the adaptive filter length is finite while the real RIR is long, and (2) tracking disturbances (people/objects moving) cause misalignment.

The RES task is to apply a spectral gain $G(i,k)$ to $E(i,k)$ that suppresses $r$ while preserving $s$. This requires an estimate of the residual echo PSD $\lambda_R(i,k) = \mathcal{E}\{|R(i,k)|^2\}$, which is unobservable and corrupted by near-end speech — especially during double talk.

## Methodology

### System Architecture

The system follows the standard AEC + RES cascade. The AEC stage uses a [[concepts/multidelay-block-frequency-domain-adaptive-filter\|generalized multidelay block frequency-domain (GMDF) adaptive filter]] (Moulines, Ait Amrane & Grenier 1995), chosen for its flexibility in independently selecting FFT size and block delay.

![[raw/papers/fang-2020-robust-residual-echo-suppression/figures/0b7289707a862bf6458edb68e48ec8ea41cfa45979ca17280c78c059bcca31cd.jpg|Figure 1]]

*Figure 1: Echo cancellation system architecture — far-end signal $x$, adaptive filter $W$, echo replica $\hat{d}$, residual echo $r$, near-end speech $s$, and the RES stage applied to the AEC error $e$.*

### Residual Echo PSD via Statistical Normalized Correlation

The core contribution is a residual echo PSD estimator that does **not** require VAD (near-end talk / single talk / double-talk detection) or minimum statistics. Instead it exploits the statistical correlation between the echo replica $\hat{D}$ and the AEC error $E$, after mean removal:

$$\tilde{D}(i,k) = \hat{D}(i,k) - \mathcal{E}\{\hat{D}(i,k)\}, \qquad \tilde{E}(i,k) = E(i,k) - \mathcal{E}\{E(i,k)\}.$$

The smoothed cross- and auto-PSDs are

$$r^{de}(i,k) = \alpha\, r^{de}(i{-}1,k) + (1{-}\alpha)\,|\tilde{D}^{*}(i,k)\,\tilde{E}(i,k)|,$$

$$r^{dd}(i,k) = \alpha\, r^{dd}(i{-}1,k) + (1{-}\alpha)\,|\tilde{D}^{*}(i,k)\,\tilde{D}(i,k)|,$$

and the residual echo PSD estimate is the normalized cross-spectrum (see [[concepts/statistical-normalized-correlation\|Statistical Normalized Correlation]]):

$$\hat{\lambda}_R(i,k) \;=\; r^{drdr}(i,k) \;=\; \frac{r^{de}(i,k)\cdot r^{de}(i,k)}{r^{dd}(i,k)}.$$

**Justification (single talk):** When $s=0$, $e=r$, so $\tilde{E}\approx \tilde{R}$ and the estimate reduces to $|R(i,k)|^2\cos\theta$, where $\cos\theta$ is the coherence between $\tilde{D}$ and $R$. Because $R = (H-W)X$ and $\hat{D}=WX$ share the same excitation $X$, $\cos\theta \approx 1$ in single talk, so $\hat{\lambda}_R \approx |R|^2$.

**Justification (double talk):** When $s\neq 0$, near-end speech $S$ is assumed statistically uncorrelated with $\hat{D}$ over the smoothing window, so the cross-term $\tilde{D}^{*}S$ averages out and the estimator still tracks $|R|^2\cos\theta$ rather than $|S+R|^2$.

### Spectral Suppression Gain

The PSD estimate drives priori and posteriori signal-to-echo ratios (SER):

$$\xi^{\mathrm{priori}}(i,k) = \frac{|E(i,k)|^2 - \beta\,\hat{\lambda}_R(i,k)}{|E(i,k)|^2}, \qquad \xi^{\mathrm{post}}(i,k) = \frac{|E(i,k)|^2}{\hat{\lambda}_R(i,k)} - 1,$$

with the decision-directed (DD) recursion (Ephraim & Malah 1983):

$$\xi^{\mathrm{priori}}(i,k) = \beta\,\hat{\xi}^{\mathrm{priori}}(i{-}1,k) + (1-\beta)\max\!\big(\xi^{\mathrm{post}}(i,k),\,0\big).$$

The final gain is a Wiener-type rule with a spectral floor $G_{\min}$:

$$G(i,k) = \max\!\left(\frac{\xi^{\mathrm{priori}}(i,k)}{\xi^{\mathrm{priori}}(i,k)+1},\; G_{\min}\right), \qquad \hat{S}(i,k) = E(i,k)\,G(i,k),$$

where $G_{\min}$ preserves background-noise modulation. Time-domain reconstruction uses IFFT + overlap-add.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Room** | Real meeting room, $5 \times 8 \times 3$ m |
| **Sampling rate** | 16 kHz |
| **Frame length** | 20 ms, 50% overlap |
| **AEC** | GMDF (generalized multidelay block frequency-domain adaptive filter) |
| **Signals** | Real echo recordings (loudspeaker playback captured by mic) + near-end speech, summed |
| **Baseline** | Slow-attach-and-fast-decay residual echo PSD tracker (Hoshuyama & Sugiyama 2006) |
| **Metrics** | [[concepts/echo-return-loss-enhancement\|ERLE]] (single talk), [[concepts/speech-to-speech-distortion-ratio\|SSDR]] (double talk) |
| **Test segments** | Far-end-only segment + DTD segment (near-end only / echo only / double talk) |

## Results

### ERLE (Far-End Only)

![[raw/papers/fang-2020-robust-residual-echo-suppression/figures/b93f944a00fe6e3e7394f8ba13c402ad4d3a9fa8ec34746f828af7bf8837534a.jpg|Figure 2]]

*Figure 2: ERLE comparison in the far-end-only (single talk) situation. Blue: AEC output only; green: AEC + baseline RES; red: AEC + proposed RES. Both RES methods improve on AEC alone, and the proposed correlation-based method achieves higher ERLE than the baseline.*

Both RES methods substantially improve ERLE over the AEC-only output, and the proposed method outperforms the baseline throughout, owing to more timely tracking of the residual echo PSD.

### SSDR (Double Talk)

The segmental SSDR over the double-talk region is reported in Table I.

| AEC only | AEC + baseline RES | AEC + proposed RES |
|----------|--------------------|--------------------|
| 3.8976 dB | 4.6797 dB | **4.8270 dB** |

The proposed method introduces less near-end speech distortion than the baseline while simultaneously achieving higher echo suppression, confirming the robustness of the correlation-based PSD estimate during double talk.

### Waveform Comparison (Double Talk)

![[raw/papers/fang-2020-robust-residual-echo-suppression/figures/49982fd5e4809cdfd0217eb42f2913c0df5433dbd9bca57fe3021566eea0d44f.jpg|Figure 4]]

*Figure 4: Waveform comparison in the DTD scenario. Top to bottom: far-end speech, microphone signal, desired near-end speech, AEC output, AEC + baseline RES output, AEC + proposed RES output. The proposed method suppresses echo more aggressively while preserving the near-end speech segment.*

## Key Contributions

1. **A VAD-free residual echo PSD estimator** based on the statistical normalized cross-correlation between the AEC error and the echo replica (mean-removed), avoiding the need for double-talk detection or minimum statistics.
2. **Case analysis** showing the estimator reduces to $|R|^2\cos\theta$ in single talk (with $\cos\theta \approx 1$) and remains robust in double talk because near-end speech is uncorrelated with the echo replica over the smoothing window.
3. **Integration with an Ephraim-Malah-style spectral gain** (DD priori SER + Wiener floor) to produce the final RES stage.
4. **Real-recording validation** showing simultaneous improvements in both ERLE (single talk) and SSDR (double talk) over a slow-attach-and-fast-decay baseline — the proposed method suppresses echo more aggressively while introducing *less* near-end distortion.

## Related Concepts

- [[concepts/residual-echo-suppression\|Residual Echo Suppression]] — the central problem; this paper provides a correlation-based PSD estimator as an alternative to VAD- or minimum-statistics-based approaches.
- [[concepts/statistical-normalized-correlation\|Statistical Normalized Correlation]] — the novel estimator introduced by this paper.
- [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]] — the linear front-end (NLMS / GMDF) whose residual echo this method suppresses.
- [[concepts/echo-return-loss-enhancement\|Echo Return Loss Enhancement (ERLE)]] — single-talk evaluation metric.
- [[concepts/speech-to-speech-distortion-ratio\|Speech-to-Speech-Distortion power Ratio (SSDR)]] — double-talk evaluation metric.
- [[concepts/multidelay-block-frequency-domain-adaptive-filter\|Multidelay Block Frequency-Domain Adaptive Filter (MDF)]] — the AEC algorithm used in the front-end.
- [[concepts/minimum-statistics\|Minimum Statistics]] — a baseline PSD-estimation approach this method replaces.

## Related Synthesis

*(None yet — this is a single-method traditional signal-processing paper. See the Wung 2011 source page for a related system-level RES approach.)*
