---
type: source
created: 2026-07-23
updated: 2026-07-23
sources:
  - raw/papers/harma-2000-frequency-warped-signal-processing/full-text.md
  - zotero://select/items/0_H64BZGKP
tags:
  - frequency-warping
  - audio-signal-processing
  - psychoacoustics
  - filter-design
  - linear-prediction
  - tutorial
---

# Härmä, Karjalainen & Savioja 2000: Frequency-Warped Signal Processing for Audio Applications

**Authors**: [[entities/aki-harma|Aki Härmä]]¹, [[entities/matti-karjalainen|Matti Karjalainen]]¹ (AES Fellow), [[entities/lauri-savioja|Lauri Savioja]]² (AES Member), [[entities/vesa-valimaki|Vesa Välimäki]]¹ (AES Member), [[entities/unto-k-laine|Unto K. Laine]]¹ (AES Member), [[entities/jyri-huopaniemi|Jyri Huopaniemi]]³ (AES Member)

**Affiliations**: ¹ Helsinki University of Technology, Laboratory of Acoustics and Audio Signal Processing, Espoo, Finland; ² Helsinki University of Technology, Telecommunications Software and Multimedia Laboratory, Espoo, Finland; ³ Nokia Research Center, Speech and Audio Systems Laboratory, Helsinki, Finland

**Venue**: Journal of the Audio Engineering Society, Vol. 48, No. 11

**Year**: 2000 (November)

**Type**: Tutorial / Review Article

**Zotero**: [zotero://select/items/0_H64BZGKP](zotero://select/items/0_H64BZGKP)

## Summary

This tutorial paper presents **frequency-warped digital signal processing** as a methodology for designing and implementing DSP algorithms directly on a nonuniform frequency scale that approximates human auditory resolution (the Bark scale). By replacing unit delays $z^{-1}$ with first-order all-pass elements $D(z)$, practically any DSP algorithm — FIR/IIR filters, FFT, linear prediction, adaptive filters — can be "warped" so that its frequency resolution automatically follows psychoacoustic scales. The paper surveys applications to audio coding, loudspeaker equalization, guitar-body physical modeling, binaural (HRTF) filter design, and digital waveguide mesh dispersion correction, demonstrating consistent reductions in filter order and computational cost.

## Problem Formulation

Conventional DSP systems have **uniform frequency resolution** from dc to the Nyquist limit because the unit delay $z^{-1}$ delays all frequencies equally. Human hearing, however, is characterized by **nonuniform frequency resolution** — captured by psychoacoustic scales such as the mel, Bark, and ERB rate scales — where low frequencies are resolved more finely than high frequencies. The paper asks: *how can DSP algorithms be designed or implemented so that their inherent frequency resolution matches auditory perception?*

The cochlear frequency-position mapping (Greenwood's formula) relates position $x$ (in mm) on the cochlea to characteristic frequency $f$ (in Hz):

$$f = 165.4 (10^{0.06 x} - 1), \qquad x = \frac{1}{0.06} \log_{10}\left(\frac{f - 165.4}{165.4}\right)$$

The ERB bandwidth and rate scale (Moore, Peters & Glasberg 1990) are:

$$\Delta f_{\mathrm{ERB}} = 24.7 + 0.108 f_c, \qquad x = 21.3 \log\left(1 + \frac{f}{229}\right)$$

The paper notes that the ERB scale matches Greenwood's physiological mapping better than the Bark scale (Bark bands are 2–4× wider than ERBs below 200 Hz and 1.5–2× wider above 5 kHz), motivating ERB-like warping for auditory-matched processing.

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/92378974f56c2fdc4ab0da9b736772b7e3c4c87164193f6ad1b8afc26c703d23.jpg|Bandwidth corresponding to 1 mm on cochlea]]
*Figure 1: Bandwidth corresponding to 1 mm on cochlea, derived from Greenwood's formula, ERB, Bark, and one-third-octave bands as a function of center frequency.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/4b76ffa46943e46edbdbbef6113b955583e9d419e3c6ed4b0b2e05562c78095f.jpg|Difference between bandwidth estimates of an auditory filter]]
*Figure 2: Difference between bandwidth estimates of an auditory filter, illustrated in terms of the ratio between a bandwidth function and the bandwidth derived from Greenwood's mapping (GB).*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/243928ae83a2155d71f60659a3190dd59af7fd5f2a1cf60b06274cb7b5eb6025.jpg|Mapping of Greenwood's formula, ERB rate scale, Bark rate scale, and linear frequency]]
*Figure 3: Mapping of Greenwood's formula, ERB rate scale, Bark rate scale, and linear frequency. All auditory frequency scales are between linear and logarithmic scales.*

## Methodology

### All-Pass Filter Chain and Bilinear Warping

The core building block is a first-order all-pass filter:

$$D(z) = \frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}$$

where $\lambda \in (-1, 1)$ is the **warping parameter**. Cascading $N$ such elements forms an all-pass chain (Fig. 6) where low-frequency components propagate slower and high-frequency components faster than in a unit-delay chain, producing a frequency-dependent resampling of the signal.

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/fe7ed028be95a216b7d254f6411f3bcf3ee05e246fca634d1d9a19ca4464daca.jpg|Phase response of first-order all-pass filter]]
*Figure 4: Phase response of first-order all-pass filter for various real values of $\lambda$.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/53c63c9825cca857f0a64d60023f37f7dc1bedfb0bf01ff78fb723948603a28a.jpg|Group delay of first-order all-pass filter]]
*Figure 5: Group delay of first-order all-pass filter. For $\lambda = 0.723$, the group delay is approximately 6 samples at low frequencies but less than 0.2 sample at very high frequencies.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/7bd549cb4b904cd74b431101c479ad622bf57177cd9961eb89ed13c1552550c7.jpg|Direct-form II implementation of all-pass chain]]
*Figure 6: Direct-form II implementation of all-pass chain — the core building block of frequency-warped DSP.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/6ccb858a8bc296861ce76586aa5d13bd7b299c709e81ec510bff8e5f94fa985b.jpg|Set of sinusoidal signals and their sum spectrum]]
*Figure 7: Set of sinusoidal signals and their sum spectrum — input to the all-pass chain.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/3da8b075bd2f318b8ab94867e3ffaaf65f7f27551ef7dd873586218253627d5b.jpg|Set of warped signals and their sum spectrum]]
*Figure 8: Set of warped signals and their sum spectrum — output of a 1000-element all-pass chain with $\lambda = 0.723$. Low-frequency components are shorter and high-frequency components longer than the original.*

The frequency mapping is governed by the phase function of $D(z)$:

$$\omega' = \arctan \frac{(1 - \lambda^2) \sin(\omega)}{(1 + \lambda^2)\cos(\omega) - 2\lambda}$$

This is a **conformal bilinear mapping** from the unit disk onto itself. The **turning-point frequency** $f_{tp}$ (where warping leaves frequency unchanged) is:

$$f_{tp} = \pm \frac{f_s}{2\pi} \arccos(\lambda)$$

### Warping as a Conformal Bilinear Mapping

The z-transform of a signal $s(n)$ is $S(z) = \sum_{n=0}^{\infty} s(n) z^{-n}$. Replacing unit delays with all-pass elements corresponds to the bilinear transformation $z^{-1} \to \tilde{z}^{-1} = D(z)$ and its inverse $\tilde{z}^{-1} \to z^{-1} = \frac{\tilde{z}^{-1} + \lambda}{1 + \lambda z^{-1}}$. This yields a warped representation:

$$S(z) = \sum_{k=0}^{\infty} w(k) \tilde{z}^{-k} = \sum_{k=0}^{\infty} w(k) \left(\frac{z^{-1} - \lambda}{1 - \lambda z^{-1}}\right)^k$$

where $w(k)$ are samples of the warped impulse response. Mapping the entire equation to the warped z-domain:

$$\sum_{n=0}^{\infty} s(n) \left(\frac{\tilde{z}^{-1} + \lambda}{1 + \lambda z^{-1}}\right)^n = \sum_{k=0}^{\infty} w(k) \tilde{z}^{-k}$$

The paper distinguishes **two views of warping**:
1. **Signal warping**: warp a signal segment (as in Fig. 8) — produces signals with strange characteristics, to be used with care.
2. **Transfer function / coefficient warping**: warp a transfer function, coefficient sequence, or impulse response — more straightforward, and the approach used in all application examples of the paper.

Since the warping effect is generally **shift-variant**, this approach works easily only for finite or truncated impulse responses or coefficient sequences.

### Bark Bilinear Mapping (Smith & Abel 1999)

Smith and Abel derived an analytic expression for $\lambda$ that best matches the Bark scale for a given sampling frequency $f_s$:

$$\lambda_{f_s} \approx 1.0674 \left[\frac{2}{\pi} \arctan(0.06583 f_s)\right]^{1/2} - 0.1916$$

At $f_s = 44.1$ kHz this yields $\lambda = 0.756$. A slightly higher value ($\lambda \approx 0.78$) best matches Greenwood's low-frequency mapping.

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/e885d41df912e3ceef15d07d26bcc94d749a8e8201d88880eec0c6980b6ae4b8.jpg|Bark rate scale mapping and frequency transformation in an all-pass chain for various lambda]]
*Figure 9: Bark rate scale mapping and frequency transformation in an all-pass chain for various $\lambda$. Globally the closest match is at $\lambda \approx 0.74$; for low frequencies $\lambda \approx 0.8$.*

### Warped FIR (WFIR) Filters

A WFIR filter is obtained by replacing each unit delay of a conventional FIR structure with $D(z)$ (Fig. 11):

$$H_{\mathrm{WFIR}}(z) = \sum_{n=0}^{M} h^{-}(n) \tilde{z}^{-n} = \sum_{n=0}^{M} \beta_n \{D(z)\}^n$$

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/6370b32c722dff5f9ba0b3438969d2204758ffad2cefe84ae6b26f250e86e9b8.jpg|WFIR filter structure]]
*Figure 11: WFIR filter where unit delays of a conventional filter are replaced with first-order all-pass filters $D(z)$.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/2e363a40a8e64d95214ee1355116bbd2ba9c1058b0f92f0bfa6326d1ad9d606d.jpg|Network for computing warped impulse response]]
*Figure 10: Network for computing warped impulse response $w(n)$ (coefficient sequence of a WFIR filter) from an impulse response $s(n)$. Input is unit impulse $\delta(n)$; the chain uses $-\lambda$ (dewarping).*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/0351b1de372a11737d780e23284235b717b56416c4fa4a265dcefef1f3a47067.jpg|WFIR lattice filter structure]]
*Figure 12: WFIR lattice filter structure.*

Although structurally FIR-like, the WFIR has an infinite impulse response. Coefficients can be derived from a nonwarped FIR via the analysis (dewarping) network, which uses $-\lambda$ instead of $\lambda$.

### Warped IIR (WIIR) Filters

The general WIIR transfer function is:

$$H_{\mathrm{WIR}}(z) = \frac{\sum_{i=0}^{M} \beta_i [D(z)]^i}{1 + \sum_{i=1}^{R} \alpha_i [D(z)]^i}$$

A direct implementation contains **delay-free recursive loops** that cannot be realized. The paper presents two solutions: (1) a two-step technique that computes the output first and then updates internal states, and (2) a modified structure (Fig. 13b) that eliminates the delay-free loops via a coefficient transformation from $\alpha_i$ to $\sigma_i$. Poles $p_k$ and zeros $m_k$ of an ordinary IIR filter can be mapped explicitly to the warped domain:

$$\tilde{p}_k = \frac{p_k + \lambda}{1 + p_k \lambda}, \qquad \tilde{m}_k = \frac{m_k + \lambda}{1 + m_k \lambda}$$

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/7ee3b03cddd174c4dca09e3d37617f92840b4c039ff720572306af47753d9e98.jpg|WIIR filter with delay-free recursive loops]]
*Figure 13(a): WIIR filter — cannot be implemented directly because it has delay-free recursive loops.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/b7bfbc2ec259d375d63daca9684d8adbd2098c741a420b3d2771ae9c380b193a.jpg|Directly realizable WIIR filter]]
*Figure 13(b): Directly realizable WIIR filter — the modified structure eliminates delay-free loops via coefficient transformation $\alpha_i \to \sigma_i$.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/b894317654050018d7e43959240c8ee90284620053947e4432bde7321efcea44.jpg|WIIR lattice filter]]
*Figure 14: WIIR lattice filter — (a) contains delay-free recursive loops; (b) is the directly realizable modified structure.*

### Warped Linear Prediction (WLP)

WLP replaces the unit-delay shift register of conventional LPC with an all-pass chain, yielding a **warped all-pole spectral model**. The prediction error filter is:

$$A(z) = 1 - \sum_{k=1}^{N} a_k D(z)^k$$

The normal equations retain the Wiener–Hopf structure because $D(z)$ is all-pass (so correlation values are shift-invariant along the chain), and can be solved with the Levinson–Durbin algorithm. In the spectral domain, WLP matches the signal's power spectrum on the warped (Bark) frequency scale, yielding much finer low-frequency resolution than conventional LPC at the same model order (see Fig. 19).

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/542a34265be96767fd57e6b85c609ca721682f438b2d2da84fe821fa323e9794.jpg|Warped autocorrelation network]]
*Figure 18: Warped autocorrelation network — computes N-tap warped autocorrelation values continuously from input sequence $s(n)$.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/2c7ee6f106b2490341b8540759e30b0643d25a8a5a4593c6eb89226ace945df5.jpg|Power spectrum on linear frequency scale]]
*Figure 19(a): Power spectrum of a clarinet sound and spectral estimates given by conventional LPC and WLPC of 40th order — linear frequency scale.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/78f2ce806c70262ec54a8e967140cbcaf907788139d62ec50d303262e48950f6.jpg|Power spectrum on warped frequency scale]]
*Figure 19(b): Same data on a warped (Bark) frequency scale. The WLPC model has significantly better low-frequency resolution; conventional LPC pays too much attention to high-frequency details.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/ccfd6852906dd3501cd0ef6ee3c7fd4cd1f4ef96a57f9fc280248951ee59d35a.jpg|Noise processes in WLP coding]]
*Figure 20: Noise processes in WLP coding. The error has the same spectral shape as the original signal (open-loop coding), automatically utilizing frequency masking. The MPEG I layer 3 coding error is plotted for comparison (dashed).*

## Applications Survey

The paper surveys seven application areas where frequency warping provides advantages:

| Application | Warped Structure | Key Benefit | Comparison Baseline |
|-------------|-----------------|-------------|---------------------|
| Warped FFT / filter banks | All-pass chain + FFT | Automatic auditory filter bank; 16-channel Bark-warped bank | Conventional uniform FFT |
| Warped linear prediction (audio coding) | WLP-D*PCM | ~6 dB lower residual SNR needed (1 bit/sample savings) at 32–48 kHz | Conventional LPC-D*PCM |
| Warped adaptive filtering | Backward-adaptive warped lattice | One-sample coding delay; automatic noise masking | Conventional backward-adaptive coders |
| Loudspeaker equalization | WIIR (warped Prony) | Order-24 WIIR ≈ order-105 FIR; better low-freq matching | FIR, IIR equalizers |
| Guitar body physical modeling | WIIR (LP in warped domain) | Denominator order 100–200 vs. FIR order 2000–5000 | FIR, IIR, LP filters |
| Binaural (HRTF) filter design | WIIR (Prony, $\lambda=0.65$) | Lower filter order with perceptual tradeoff | FIR, IIR (Prony) |
| Digital waveguide mesh | Warped interpolated mesh ($\lambda=-0.327$) | Dispersion error reduced at high frequencies | Rectangular/interpolated mesh |

### Warped FFT and Filter Banks

A frequency-warped spectrum is computed by applying the FFT to the outputs of an all-pass filter chain (Fig. 15). This yields a **nonuniform-resolution filter bank** that approximates auditory frequency analysis. A Bark-warped filter bank with 16 channels is computationally very efficient and easy to design, but the sidebands have too high a level for many practical audio applications. Enhancements include: using a longer all-pass chain and combining neighboring channels (Laine & Härmä 1996); using more suitable window functions for sidelobe attenuation; and designing IIR-type warped filter banks directly — a set of 24 fifth-order warped Butterworth filters with 1-Bark bandwidth each.

The main limitation of warped filter banks is that they are based on IIR filters, so **critical subsampling with perfect reconstruction is impossible** in most cases. Two partial solutions exist: Laine's block-recursive FAMlet algorithm (approximately perfect reconstruction, small approximation error in typical applications) and Evangelista & Cavaliere's frequency-warped wavelet transform (true perfect reconstruction, but requires time reversal of the entire signal, precluding real-time use).

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/09eb97812626da96c4a1843c66fd654732b9e8aef6b9f6b02b61320a28d759d9.jpg|Network for computing warped FFT spectrum]]
*Figure 15: Network for computing warped FFT spectrum — applying the FFT to the outputs of an all-pass chain yields a nonuniform-resolution (Bark-warped) spectrum.*

### Warped Linear Prediction (Audio Coding)

[[concepts/warped-linear-prediction|WLP]] replaces the unit-delay shift register of conventional LPC with an all-pass chain, yielding a warped all-pole spectral model that matches the signal's power spectrum on the Bark scale. The normal equations retain the Wiener–Hopf structure and can be solved with the Levinson–Durbin algorithm. A characteristic of D*PCM (residual-driven) LPC is that the quantization error spectrum inherits the spectral shape of the all-pole model — in WLP this automatic noise masking is more pronounced, producing noise spectra comparable to MPEG-1 Layer 3 **without any separate auditory model**.

The listening test results (Fig. 21) are the most quantitatively detailed finding. Test material: 12 steady-state musical/speech sounds. Sampling rates: 8, 16, 32, 48 kHz. Model orders: 20, 40, 50 (plus 10th-order at 8 kHz). The method of adjustment was used: listeners adjusted the SNR of the residual signal in real time to find the threshold of audibility of coding artifacts.

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/3c0491873b28931da57866ebbc098fd33447e6e156e97c6b1f7d1b34f85182c9.jpg|Listening test results comparing WLPC and LPC residual SNR thresholds at four sampling rates]]
*Figure 21: Average listening test results at four sampling rates as a function of LPC/WLPC model order. Lower SNR = better (less bits needed for the residual).*

At 32 and 48 kHz, WLP requires approximately **6 dB lower residual SNR** than LPC — corresponding to **1 bit/sample savings** (48 kbit/s at 48 kHz, 32 kbit/s at 32 kHz). At 16 kHz the gain vanishes for orders ≥ 50; at 8 kHz it vanishes for orders ≥ 35. For a 10th-order model at 8 kHz, WLP still yields ~3 dB gain (0.5 bit/sample). The SNR threshold maps to bit rate via $\mathrm{SNR}/\mathrm{dB} = 6b + \gamma$, where $b$ is bits per sample.

### Warped Adaptive Filtering

Warped (Laguerre) adaptive filtering shares the same frequency-resolution characteristics as WLP. Several variants exist: Den Brinker's LMS-type algorithm with Laguerre filters; Tokuda et al.'s adaptive mel-cepstral analysis; and Fejzo & Lev-Ari's gradient adaptive lattice (GAL) warped lattice filter.

A key application is a **perceptual audio codec based on backward-adaptive Bark-warped lattice** (Härmä, Laine & Karjalainen 1998). Because the codec is warped, it automatically utilizes the ear's noise-masking characteristics (as in WLP). Because it uses backward adaptation, it achieves a **coding delay of one sample period** — far lower than conventional audio coders where the auditory model is a separate block requiring long-term FFT spectra. This is a fundamental advantage of warped DSP: the auditory model is incorporated *into* the coding process rather than bolted on as a separate stage.

### Loudspeaker Equalization

Loudspeaker response equalization by digital inverse filtering is typically done with FIR or IIR filters, applied to magnitude response only or to both magnitude and phase. FIR filters are efficient at high frequencies (uniform resolution matches log-scale specifications poorly at low frequencies), while IIR filters are harder to design but avoid some low-frequency problems.

[[concepts/warped-iir-filter|WIIR]] and [[concepts/warped-fir-filter|WFIR]] structures are strong competitors. The WIIR equalizer (inverse filter) is designed via the **warped Prony method**. Fig. 22 shows magnitude responses for a less-than-medium-quality loudspeaker: very low WIIR filter orders (less than 10) already show good overall equalization, and a WIIR of order 24 achieves about the same degree of equalization as an FIR of order 105. The WIIR works best at middle-to-low frequencies; the FIR does the best job at high frequencies.

A useful characteristic is that selecting a proper $\lambda$ value **focuses the best resolution to a desired part of the audio range**. For two- or three-way loudspeakers with crossover networks, each subband can have an optimized $\lambda$ value. Warping can also be combined with multirate techniques.

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/08582d6ce20cd16511cc2a2d7333e2f042565e40ca9b04a5c8926f287d8a6090.jpg|Loudspeaker equalization curves]]
*Figure 22: Loudspeaker equalization curves. orig — original magnitude response; WIIR4, WIIR24 — WIIR equalization at filter orders 4 and 24; FIR105 — FIR filter equalization at order 105. Low-order WIIR achieves comparable quality to high-order FIR, especially at low frequencies.*

### Physical Modeling of the Guitar Body

Model-based synthesis of the acoustic guitar requires simulating the body as a digital filter (the string vibration is well understood and can be commuted via the body response as excitation). A typical guitar body magnitude response (measured by impact hammer excitation at the bridge, recorded 1 m in front of the sound hole) has sharp low-frequency resonances that decay slowly, while high-frequency modes are broader and decay faster.

At $f_s = 22$ kHz:
- **FIR approximation**: requires filter order 2000–5000 for good results (sharp low-frequency peaks)
- **IIR (linear prediction) all-pole model**: order 500–1000 works relatively well
- **WFIR** (order 500, $\lambda = 0.63$): comparable in quality to the above
- **WIIR** (LP in warped domain): denominator order **100–200** is comparable in quality — the lowest-order approximation

Warping provides a **double advantage** here: (1) physically, it balances the resonance Q values so sharp low-frequency peaks are broadened to resemble high-frequency Q values; (2) perceptually, it matches the auditory Bark scale so the filter order is minimized. Despite the structural complexity of warped filters, the small efficiency advantage remains on typical DSP processors due to the order reduction.

### Binaural (HRTF) Filter Design

Real-time digital modeling of spatial hearing cues (3-D sound) relies on head-related transfer functions (HRTFs). Traditionally designed via minimum-phase reconstruction with FIR and IIR methods. The use of warped filters in binaural and crosstalk-canceled binaural filter design was investigated by Huopaniemi et al. (1997, 1999).

Two implementation strategies exist:
1. **Dewarped WIIR**: expand the warped transfer function to yield equivalent traditional IIR filters (e.g., direct-form II). This outperforms traditional FIR and IIR design methods.
2. **Direct warped-domain implementation**: use WFIR and WIIR structures directly (the authors' preferred approach).

Fig. 24 compares IIR design methods with and without warping using a Cortex MK2 dummy head HRTF, filter orders 20 and 6, designed via Prony's method, with $\lambda = 0.65$. The WIIR designs show enhanced low-frequency fit at the cost of reduced high-frequency matching — a tradeoff that is **psychoacoustically tolerable**. In summary, auditorily motivated filter design in 3-D sound has a clear computational advantage without sacrificing perceptual accuracy.

### Digital Waveguide Mesh Dispersion Correction

The digital waveguide mesh (Van Duyne & Smith 1993) is a finite-difference time-domain simulation where a vibrating surface is discretized on a rectangular grid, with each node updated from its four neighbors. The **main weakness** is direction-dependent dispersion error that increases with frequency: standing waves in the diagonal direction are exact, but frequencies in other directions are too small, with higher modes displaced more than lower ones.

Solutions include the triangular mesh (equilateral triangle sampling) and the **interpolated mesh** (Savioja & Välimäki 1997), which inserts hypothetical nodes and spreads their contribution over existing neighbors — a multidimensional application of fractional delay filters.

Frequency warping provides an additional correction: by applying a **negative** warping parameter ($\lambda = -0.327358$), the dispersion error at high frequencies is significantly reduced. Figs. 25 and 27 show the ideal square membrane response, the original mesh, the interpolated mesh, and the warped interpolated mesh. The warped version brings the simulated eigenmode frequencies much closer to the analytically solved ideal frequencies (dashed vertical lines).

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/bd1ddb2256d31dc165b69e85ef7cb6df2add2162da1c08dc677e01b191879578.jpg|Digital waveguide mesh dispersion correction]]
*Figure 25: Digital waveguide mesh suffers from frequency-dependent dispersion. (a) Ideal response. (b) Simulation result. (c) Dispersion reduced by frequency warping.*

![[raw/papers/harma-2000-frequency-warped-signal-processing/figures/3d854d1675352ba9c9044ebff1f6792cd4f87f2e2377bf6e8cf1762fe89f0d02.jpg|Simulated magnitude responses of ideal square membrane]]
*Figure 27: Simulated magnitude responses of ideal square membrane. (a) Original digital waveguide mesh. (b) Interpolated mesh. (c) Warped interpolated mesh ($\lambda = -0.327358$). Dashed vertical lines — analytically solved ideal eigenmode frequencies.*

### Other Applications

The paper briefly surveys additional uses of warped techniques:
- **Warped cepstral analysis**: Imai's mel-cepstral analysis (1983), later generalized by Kobayashi et al. to mel-generalized cepstral analysis, used in speech analysis and coding.
- **Speaker verification**: frequency-warped spectral distance measures (Noda 1988).
- **Objective quality measurement of coded speech**: auditory distortion measures (Wang, Sekey & Gersho 1991).
- **Speech enhancement**: warped filter banks for psychoacoustically motivated noise reduction (Böß & Alexander 1999).
- **Speech synthesis**: WLP reduces filter order, aiding parametric control of text-to-speech (Karjalainen, Altosaar & Vainio 1998).

### Implementation Notes

- WFIR filters are typically 3–4× slower per order than FIR on DSP processors; WIIRs are 2–2.5× slower per order than IIRs.
- Warping can reduce filter order by a factor of ~5 or more, so the net computational cost favors warped structures.
- Warped filters are less sensitive to coefficient quantization (poles spread more uniformly), aiding fixed-point implementations.
- Mapping back to a traditional IIR form works for orders < 20 but fails above order ~30 even in double precision due to pole clustering.

## Key Contributions

1. **Unified tutorial** of frequency-warped DSP methodology — from all-pass chain theory through WFIR/WIIR filter design to applications, in a single reference.
2. **Modified WIIR structures** that eliminate delay-free recursive loops, enabling direct implementation of warped IIR filters.
3. **Quantitative WLP vs. LPC comparison** via listening tests, showing ~6 dB (1 bit/sample) residual SNR savings at wideband sampling rates (32–48 kHz).
4. **Application catalog** demonstrating order reductions across loudspeaker equalization (24 vs. 105), guitar body modeling (100–200 vs. 2000–5000), and HRTF filtering.
5. **Dispersion correction** for digital waveguide meshes via negative-$\lambda$ warping.
6. Released a **free MATLAB toolbox** for frequency-warped signal processing.

## Limitations and Caveats

- The Bark bilinear mapping (first-order all-pass) **cannot exactly match** Greenwood's cochlear mapping or the ERB scale globally — it is only a good approximation. Exact matches require higher-order all-pass filter banks (briefly noted but not developed).
- Warped filter banks based on IIR filters **cannot achieve perfect reconstruction** with critical subsampling in most cases (the Laine block-recursive and Evangelista–Cavaliere wavelet approaches have limitations: the latter requires time reversal of the entire signal, precluding real-time use).
- WLP gains diminish at low sampling rates (8 kHz) and high model orders — the advantage is most pronounced for wideband audio.
- The listening tests use only 2 subjects and 11 test signals — the authors label them "preliminary."

## Related Concepts

- [[concepts/frequency-warping|Frequency Warping]] — the core methodology surveyed by this paper
- [[concepts/all-pass-filter|All-Pass Filter]] — the first-order all-pass element $D(z)$ used as the warping building block
- [[concepts/warped-fir-filter|Warped FIR Filter]] — WFIR structures and design
- [[concepts/warped-iir-filter|Warped IIR Filter]] — WIIR structures with delay-free loop elimination
- [[concepts/warped-linear-prediction|Warped Linear Prediction]] — WLP and its application to audio coding
- [[concepts/erb-scale|ERB Scale]] — psychoacoustic scale that better matches Greenwood's cochlear mapping than Bark
- [[concepts/bark-scale-spectral-features|Bark-Scale Spectral Features]] — later use of the Bark scale in neural AEC post-filters

## Related Sources

- [[sources/seo-2016-feedback-anc-constrained-optimization|Seo et al. 2016: Feedback ANC via Constrained Optimization]] — later application of WFIR + Q-parameterization to headphone ANC, citing this paper's warping methodology
