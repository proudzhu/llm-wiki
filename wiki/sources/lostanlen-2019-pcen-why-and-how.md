---
type: source
created: 2026-07-31
updated: 2026-07-31
sources:
  - raw/papers/lostanlen-2019-pcen-why-and-how/full-text.md
  - https://doi.org/10.1109/LSP.2018.2878620
  - zotero://select/items/0_X24LMQYC
tags:
  - audio-frontend
  - feature-extraction
  - robust-recognition
  - spectrogram
  - acoustic-scene-classification
  - bioacoustics
---

# Lostanlen, Salamon, Cartwright, McFee, Farnsworth, Kelling & Bello 2019: Per-Channel Energy Normalization: Why and How

**Authors**: [[entities/vincent-lostanlen|Vincent Lostanlen]], [[entities/justin-salamon|Justin Salamon]], [[entities/mark-cartwright|Mark Cartwright]], [[entities/brian-mcfee|Brian McFee]], [[entities/andrew-farnsworth|Andrew Farnsworth]], [[entities/steve-kelling|Steve Kelling]], [[entities/juan-pablo-bello|Juan Pablo Bello]]
**Institutions**: New York University; Cornell Lab of Ornithology
**Venue**: IEEE Signal Processing Letters, vol. 26, no. 1, pp. 39–43, January 2019
**DOI**: [10.1109/LSP.2018.2878620](https://doi.org/10.1109/LSP.2018.2878620)
**Zotero**: [X24LMQYC](zotero://select/items/0_X24LMQYC)

## Summary

Per-channel energy normalization (PCEN) is an adaptive acoustic frontend proposed as an alternative to the pointwise logarithm of the mel-frequency spectrogram (logmelspec) for automatic speech recognition (ASR) and acoustic event detection (AED). This letter answers two questions: *why* PCEN outperforms logmelspec — it empirically **Gaussianizes** the distribution of spectrogram magnitudes and **decorrelates (whitens)** frequency bands, converting a large class of real-world soundscapes toward additive white Gaussian noise (AWGN), the theoretically optimal noise condition for deep networks — and *how* it works — via an asymptotic analysis of its three component operations: temporal integration, adaptive gain control (AGC), and dynamic range compression (DRC). The letter closes with practical guidance for setting PCEN's five parameters $(T, \alpha, \varepsilon, \delta, r)$ and an open-source implementation in `librosa`.

## Problem Formulation

Frequency transposition is a major factor of intra-class variability in sound classification (ASR, AED, bioacoustic species classification). Tuning auditory filters to the perceptual mel scale yields a time-frequency representation in which transpositions of a periodic signal become vertical translations, allowing convolutional operators (CNNs, time-frequency scattering) to extract pitch contours as spectrotemporal patterns regardless of fundamental frequency — a property known as **equivariance**.

In real-world multi-source recordings, background noise is detrimental to this equivariance: intra-class variability transposes the foreground while leaving the background unaffected, but equivariance requires both to be transposed simultaneously. Robustness of deep networks to adversarial additive perturbations is theoretically optimal when background noise is additive, white, and Gaussian (AWGN). However, raw mel-spectrogram magnitudes $\mathbf{E}(t, f)$ of real scenes are sparse and strongly correlated along both time and mel frequency, and are thus not approximable by AWGN.

PCEN (proposed in Wang et al. 2017 for keyword spotting) addresses this by combining dynamic range compression with adaptive gain control preceded by temporal integration:

$$
\mathbf{PCEN}(t, f) = \left(\frac{\mathbf{E}(t, f)}{(\varepsilon + (\mathbf{E} * \phi_T)(t, f))^{\alpha}} + \delta\right)^{r} - \delta^{r}
$$

where $\alpha, \varepsilon, r, \delta$ are positive constants and $\phi_T$ is a low-pass filter at time scale $T$.

![[raw/papers/lostanlen-2019-pcen-why-and-how/figures/b2d364e8634bb756f782ce5e305795b2bd96f90fe2fd3499f20889dcccdc1ffd.jpg|(a) Logarithmic transformation]]

![[raw/papers/lostanlen-2019-pcen-why-and-how/figures/b507a3693bdd09c902e5379429c553a997f30ccb8ea8c149152b4d016d0f3f22.jpg|(b) Per-channel energy normalization (PCEN)]]

*Figure 1: A soundscape comprising bird calls, insect stridulations, and a passing vehicle (BirdVox data). (a) Logmelspec maps all magnitudes to a decibel-like scale; (b) PCEN enhances transient events while discarding stationary noise and slow loudness changes.*

## Methodology

PCEN's ability to Gaussianize and whiten background noise results from three component operations, each analyzed asymptotically.

### Temporal Integration

Filtering each subband with $\phi_T$ estimates the intensity of background noise at that frequency while remaining invariant to foreground intensity. Under the assumption that foreground amplitude modulation (AM) is faster than background AM, $T$ should lie above typical foreground AM periods and below background AM periods — the transition threshold between a stationary (background) and transient (foreground) regime.

The original implementation uses a first-order IIR (AR(1)) filter:

$$
\mathbf{M}(t, f) = (\mathbf{E} * \phi_T)(t, f) = s\,\mathbf{E}(t, f) + (1-s)\,\mathbf{M}(t - \tau, f)
$$

**Proposition III.1**: The AR(1) filter $\phi_T$ is a low-pass filter with 0 dB gain, cutoff frequency $\omega_c = \frac{2\pi\tau}{T} = \arccos\!\left(1 - \frac{s^2}{2(1-s)}\right)$ at 3 dB, and sidelobe falloff of 10 dB per decade near $\omega_c$.

![[raw/papers/lostanlen-2019-pcen-why-and-how/figures/8bcc3441ede183bd40163995b35228271d5040ea78589e075316f9195ee98d00.jpg|Bode plot of the temporal-integration filter]]

*Figure 2: Bode plot of the temporal-integration filter $\lvert\hat{\phi}_T(\omega)\rvert^2$ for $T = 10\cdot 2\tau$, $10^2\cdot 2\tau$, $10^3\cdot 2\tau$ — sidelobe falloff 10 dB/decade (Prop. III.1).*

### Adaptive Gain Control (AGC)

The smoothed spectrogram $\mathbf{M}(t, f)$ adapts the gain level in the denominator:

$$
\mathbf{G}(t, f) = \frac{\mathbf{E}(t, f)}{(\mathbf{M}(t, f) + \varepsilon)^{\alpha}}, \qquad 0 < \alpha < 1,\ \varepsilon > 0
$$

**Proposition III.2**: $\mathbf{G}$ is asymptotically equivalent to (i) $\mathbf{E}/\varepsilon^{\alpha}$ in the quasi-silent regime ($\mathbf{M} \ll \varepsilon$) — nonexpansive — and (ii) $\mathbf{E}/\mathbf{M}^{\alpha}$ in the active regime ($\mathbf{M} \gg \varepsilon$) — strongly compressive. Bringing $\alpha$ closer to 1 yields more cancellation of stationary background.

**Proposition III.3**: In the limit $\varepsilon = 0$, $\alpha = 1$, $\mathbf{G}$ is **invariant to spectral equalization** by the acoustic environment or recording device (impulse response $h$ with $\lvert\hat{h}\rvert(f) = 0$ for $f < 1/T$ and $\lvert\hat{h}\rvert(f) > 0$ across the audible range). This motivates PCEN for remote sensing, where models must be robust to environmental absorption and sensor differences.

![[raw/papers/lostanlen-2019-pcen-why-and-how/figures/34037f46525051e241b15109764f161baf44482a110cce4a9a72d397a3b6a9c8.jpg|AGC static compression characteristic]]

*Figure 3: Static compression characteristic of the AGC gain $\mathbf{M} \mapsto (\varepsilon + \mathbf{M})^{-\alpha}$ for $\alpha = 0.1$, $0.5$, $1.0$ (Prop. III.2).*

### Dynamic Range Compression (DRC)

The final stage adds a positive bias $\delta$ and pointwise-exponentiates:

$$
\mathbf{PCEN}(t, f) = (\mathbf{G}(t, f) + \delta)^{r} - \delta^{r}, \qquad 0 < r < 1,\ \delta > 1
$$

**Proposition III.4**: PCEN is asymptotically equivalent to (i) $r\,\delta^{(r-1)}\,\mathbf{G}$ in the quiet regime ($\mathbf{G} \ll \delta$) — linear — and (ii) $\mathbf{G}^{r}$ in the loud regime ($\mathbf{G} \gg \delta$) — power-law. DRC is stronger for smaller values of $r$.

![[raw/papers/lostanlen-2019-pcen-why-and-how/figures/ccf8396930f7e231bbcd903f9bf98e21b26c2400268b7bf85fd00eedf7ab6357.jpg|DRC static compression characteristic]]

*Figure 4: Static compression characteristic of DRC $\mathbf{G} \mapsto (\mathbf{G} + \delta)^{r} - \delta^{r}$ for $r = 0.25$, $0.5$, $0.75$ (Prop. III.4).*

## Experimental Setup

Comparative statistical analysis of logmelspec vs PCEN on three datasets spanning urban, periurban, and rural conditions:

| Dataset | Environment | Composition | Duration | Coefficients |
|---|---|---|---|---|
| SONYC | urban (NYC) | 66 × 10 s recordings, 51 sensors, 22 sound classes | 660 s | 7.3M |
| DCASE 2013 Scene Classification | periurban (London area) | 100 × 30 s recordings, 10 soundscape classes | 3000 s | 33M |
| BirdVox (curated subset) | rural (Ithaca, NY) | 15 × 60 s recordings from 9 sensors | 900 s | 10M |

Analysis methods: magnitude histograms (500 bins, scaled to null mean and unit variance) + Shapiro–Wilk normality test; covariance matrices across mel-frequency channels.

## Results

**Gaussianization**: logmelspec magnitudes exhibit skewed distributions — left-skewed on BirdVox, right-skewed on SONYC and DCASE 2013 SC. Box-Cox power transforms can improve normality in principle but their two-parameter maximum-likelihood inference is inadequate for real-time use, and both log and adaptive Box-Cox yield leptokurtic distributions. PCEN brings magnitudes close to Gaussian with negligible skewness and kurtosis. The Shapiro–Wilk test rejects logmelspec normality with $p < 0.005$ on all three datasets, while failing to reject normality of PCEN magnitudes.

**Whitening**: the covariance matrix of logmelspec shows strong cross-correlations between non-adjacent mel bands; the PCEN covariance matrix is close to identity, indicating the noise is whitened.

## Practical Recommendations

- **$T$ (time scale)**: choose above the typical period of foreground AM/FM and below that of the background noise. Rule of thumb for AED: $\frac{T \times c \times N}{\mathrm{mel}(f_{\max}) - \mathrm{mel}(f_{\min})} = K$, where $c$ is the chirp rate in mels/s and $K$ is a reverberation-dependent constant ($K \approx 1$ dry, $> 10$ highly reverberant). For constant-Q transforms: $T \times c \times Q = K$.
- **$s$ from $T$ (Prop. IV.1)**: $s = \sqrt{1 - \cos\frac{2\pi\tau}{T}}\left(\sqrt{3 - \cos\frac{2\pi\tau}{T}} - \sqrt{1 - \cos\frac{2\pi\tau}{T}}\right)$.
- **$\alpha$ (AGC exponent)**: closer to 1 → more background cancellation but right-skewed magnitudes; below 1 reduces skewness and brings background closer to AWGN. $T$ and $\alpha$ are the most important parameters.
- **$\varepsilon$**: no effect as long as it is below unit roundoff.
- **$\delta$ (DRC threshold)**: $> 1$; tradeoff between foreground-to-background ratio ($\delta \to +\infty$ in highly noisy applications) and variance of foreground loudness ($\delta \to 1$).
- **$r$ (DRC exponent)**: for a transient source at distance $d$, $\mathbf{PCEN} \sim 1/d^{2r}$; recommend $r = 1/2$ for indoor ($d \lesssim 10$ m) and $r = 1/4$ for outdoor ($d \gtrsim 100$ m) applications.

**Default parameters (librosa v0.6.1, identical to Wang et al. 2017)**: $T = 400$ ms ($s \approx 0.025$, $\tau = 23$ ms), $\varepsilon = 10^{-6}$, $\alpha = 0.98$, $\delta = 2$, $r = 1/2$ — best suited to indoor applications (e.g., smart-home ASR). **Bird-detection settings** (bioacoustics): $T = 60$ ms with $Q = 50$ and $\tau = 1.5$ ms, $\varepsilon = 10^{-6}$, $\alpha = 0.8$, $\delta = 10$, $r = 0.25$.

## Key Contributions

1. **Empirical demonstration** that PCEN Gaussianizes magnitude distributions and decorrelates (whitens) mel-frequency bands across urban, periurban, and rural datasets — converting real-world soundscapes toward the AWGN condition that is theoretically optimal for deep-network robustness.
2. **Asymptotic characterization** of PCEN's three components (temporal integration, AGC, DRC) via Propositions III.1–III.4, giving interpretable regimes: silent vs. active ($\varepsilon$), stationary vs. transient ($T$), quiet vs. loud ($\delta$).
3. **Invariance to spectral equalization** (Prop. III.3): at $\varepsilon = 0$, $\alpha = 1$, PCEN is insensitive to environment/device filtering, supporting remote-sensing applications.
4. **Concrete parameter-setting guidelines** for adapting PCEN to task-specific temporal properties, including the chirp-rate rule of thumb and the closed-form $s(T)$ relation (Prop. IV.1).
5. **Open-source implementation** in `librosa` v0.6.1 with default parameters matching the original keyword-spotting work, plus bird-detection-optimized settings.

## Related Concepts

- [[concepts/per-channel-energy-normalization|Per-Channel Energy Normalization (PCEN)]]
- [[concepts/spectrogram-analysis|Spectrogram Analysis]]
- [[concepts/acoustic-scene-classification|Acoustic Scene Classification]]
- [[concepts/keyword-spotting|Keyword Spotting]]

## Related Synthesis

- No existing synthesis page covers audio frontends / feature extraction for robust recognition; this paper does not update any current synthesis.
