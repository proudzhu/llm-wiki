---
type: concept
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/papers/gerkmann-2012-mmse-noise-psd-tracking/full-text.md
tags:
  - cepstral-analysis
  - noise-estimation
  - speech-enhancement
  - power-spectral-density
  - signal-processing
---

# Temporal Cepstrum Smoothing (TCS)

**Temporal Cepstrum Smoothing (TCS)** is a speech spectral estimation technique that smooths a noisy spectral estimate *selectively in the cepstral domain over time*: cepstral coefficients known to carry speech structure are smoothed little (or not at all), while all remaining coefficients — where non-speech-like spectral outliers land — are smoothed strongly. It was introduced by Breithaupt, Gerkmann & Martin (ICASSP 2008) for a priori SNR estimation, extended with an analytic bias analysis and cepstral nulling by Gerkmann & Martin (IEEE TSP 2009), and applied to noise PSD tracking by [[sources/gerkmann-2012-mmse-noise-psd-tracking|Gerkmann & Hendriks (ICASSP 2012)]].

The premise is that speech occupies a **small, predictable set of cepstral coefficients**: the lowest cepstral coefficients represent the speech spectral envelope, and a peak in the quefrency range corresponding to plausible pitch periods represents the fundamental period of voiced speech. Random spectral outliers produced by noise do not share this structure, so suppressing them in the cepstral domain suppresses noise without smearing the speech envelope.

## Formulation

Let $\widehat{\sigma_{\mathrm{S},k}^2}^{\mathrm{pre}}$ be a preliminary (typically limited-ML) speech PSD estimate at frequency bin $k$, computed on a length-$K$ transform. The **real cepstrum** is obtained as the inverse Fourier transform of the log spectrum:

$$\widehat{\sigma_{\mathrm{S},q}^2}^{\mathrm{pre,ceps}} = \frac{1}{K} \sum_{k=0}^{K-1} \log\left(\widehat{\sigma_{\mathrm{S},k}^2}^{\mathrm{pre}}\right) \mathrm{e}^{\,\mathrm{j}2\pi kq/K}$$

Only the lower symmetric half $q \in \{0, \dots, K/2\}$ is needed, since the cepstrum is symmetric about $K/2$.

**Selective smoothing** is a first-order recursion along time, with a bin- and frame-dependent factor $\alpha_q(l)$:

$$\widehat{\sigma_{\mathrm{S},q}^2}^{\mathrm{ceps}}(l) = \alpha_q(l)\, \widehat{\sigma_{\mathrm{S},q}^2}^{\mathrm{ceps}}(l-1) + \left(1 - \alpha_q(l)\right) \widehat{\sigma_{\mathrm{S},q}^2}^{\mathrm{pre,ceps}}(l)$$

Large $\alpha_q$ = heavy smoothing (outlier suppression); small $\alpha_q$ = the coefficient is trusted and passes through.

### Pitch-peak detection

Speech-related bins are found by locating the fundamental-period peak. To make peak picking robust against the low power of voiced sounds at high frequencies, the cepstrum is first convolved with a short Hamming window $w_{\mathrm{H},q}$ of length $\tau_{\mathrm{H}} = f_{\mathrm{s}}/2000\ \mathrm{Hz}$ (i.e. 8 coefficients at 16 kHz):

$$\overline{\sigma_{\mathrm{S},q}^2}^{\mathrm{ceps}}(l) = \widehat{\sigma_{\mathrm{S},q}^2}^{\mathrm{ceps}}(l) * w_{\mathrm{H},q} * w_{\mathrm{H},-q}$$

The peak is searched only within the quefrency window implied by an admissible pitch range $[f_{0,\mathrm{low}}, f_{0,\mathrm{high}}]$, i.e. $q_{\mathrm{low}} = \lfloor f_{\mathrm{s}}/f_{0,\mathrm{high}} \rfloor$ to $q_{\mathrm{high}} = \lfloor f_{\mathrm{s}}/f_{0,\mathrm{low}} \rfloor$:

$$q_0(l) = \arg\max_q \left\{\overline{\sigma_{\mathrm{S},q}^2}^{\mathrm{ceps}}(l) \;\middle|\; q_{\mathrm{low}} \le q \le q_{\mathrm{high}}\right\}$$

A threshold $\Lambda^{\mathrm{thr}}$ decides whether the peak is a genuine voiced fundamental, giving the pitch-bin set

$$\mathbb{Q}_{\mathrm{pitch}}(l) = \begin{cases} \left\{q_0(l) - \Delta q_0, \dots, q_0(l) + \Delta q_0\right\} & \text{if peak} \ge \Lambda^{\mathrm{thr}} \\ \emptyset & \text{otherwise} \end{cases}$$

### Smoothing-factor rules

Two mechanisms keep the pitch peak safe:

$$\alpha_q(l) = \begin{cases} \alpha_{\mathrm{pitch}} & \text{if } q \in \mathbb{Q}_{\mathrm{pitch}} \\ \beta\, \alpha_q(l-1) + (1-\beta)\, \alpha_q^{\mathrm{const}} & \text{otherwise} \end{cases}$$

- **$\alpha_{\mathrm{pitch}}$ (small, e.g. 0.2)** protects the fundamental-period peak from being smoothed away.
- **The forgetting factor $\beta$ (e.g. 0.96)** makes $\alpha_q$ relax back toward $\alpha_q^{\mathrm{const}}$ gradually, so that a *pitch-detection error in a single frame does not immediately cause strong smoothing of the peak*.
- **$\alpha_q^{\mathrm{const}}$** is a quefrency-dependent constant: near zero for the lowest coefficients (envelope, must pass through), moderate for the low-to-mid range, and large (e.g. 0.85) for upper coefficients where non-speech-like structure dominates.

### Return to the frequency domain and bias compensation

$$\widehat{\sigma_{\mathrm{S},k}^2}(l) = \mathcal{B} \cdot \exp\left(\sum_{q=0}^{K-1} \widehat{\sigma_{\mathrm{S},q}^2}^{\mathrm{ceps}}(l)\, \mathrm{e}^{-\mathrm{j}2\pi kq/K}\right)$$

The correction $\mathcal{B}$ is required because the log compression followed by smoothing in the log domain biases the back-transformed estimate. Gerkmann & Martin (TSP 2009) derived it analytically from distributional assumptions on the speech DFT coefficients and Hann-windowed frames:

$$\mathcal{B} = \frac{\exp\left(\psi(\bar{\mu}) + C\right)}{\bar{\mu}}$$

with Euler's constant $C = 0.5772$ and Euler's psi function $\psi(\cdot)$; $\bar{\mu}$ is a function of the effective smoothing $\alpha_q(l)$. For the parameter set used by Gerkmann & Hendriks (2012) the bias typically falls in $1.45 < \mathcal{B} < 1.55$. Because it is *analytic*, TCS needs no second speech estimate to correct its bias — the property that makes it attractive as the speech-PSD front end of an [[concepts/mmse-based-noise-psd-estimation|MMSE-based noise PSD tracker]].

## Cost

TCS adds two real-valued Fourier transforms (the cepstral transform and its inverse) per frame. Gerkmann & Martin (ITG Sprachkommunikation 2010) show the cost can be reduced with pruned Fourier transforms.

## Applications in the Wiki

- **[[sources/gerkmann-2012-mmse-noise-psd-tracking|Gerkmann & Hendriks 2012]] — noise PSD tracking.** TCS supplies the single speech PSD estimate needed to evaluate the conditional noise-periodogram expectation $\mathrm{E}[|N|^2 \mid y]$, replacing the limited-ML + DD pair of the earlier MMSE-based tracker and eliminating its explicit bias-compensation branch. Lower log noise-estimation error than both the original MMSE approach and [[concepts/minimum-statistics|minimum statistics]], with ~1 dB segmental-SNR gain in babble noise at 0 dB input SNR.
- **Breithaupt, Gerkmann & Martin 2008 — a priori SNR estimation**, via selective cepstro-temporal smoothing (the original introduction).
- **Gerkmann & Martin 2009 — statistics of TCS-processed amplitudes**, providing the analytic bias correction $\mathcal{B}$ and the related *cepstral nulling* operation.

## Related Concepts

- [[concepts/mmse-based-noise-psd-estimation|MMSE-Based Noise PSD Estimation]] — the estimator family that consumes the TCS speech PSD estimate
- [[concepts/decision-directed-a-priori-snr|Decision-Directed A Priori SNR Estimation]] — the speech-PSD estimator TCS replaces in that pipeline
- [[concepts/minimum-statistics|Minimum Statistics]] — the spectral-minima alternative for noise tracking
- [[concepts/speech-presence-probability|Speech Presence Probability (SPP)]] — soft-decision alternative for noise PSD updates
- [[concepts/cepstral-space-speech-enhancement|Cepstral-Space Speech Enhancement]] — the neural counterpart exploiting cepstral-domain structure
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Sources

- [[sources/gerkmann-2012-mmse-noise-psd-tracking|Gerkmann & Hendriks 2012: Improved MMSE-Based Noise PSD Tracking Using Temporal Cepstrum Smoothing]] — applies TCS to speech PSD estimation inside an MMSE noise tracker and specifies the full pitch-protecting smoothing rule
