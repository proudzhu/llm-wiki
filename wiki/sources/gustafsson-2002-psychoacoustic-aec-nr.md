---
type: source
created: 2026-10-19
updated: 2026-10-19
sources:
  - raw/papers/gustafsson-2002-psychoacoustic-aec-nr/full-text.md
  - https://doi.org/10.1109/TSA.2002.800553
  - zotero://select/items/0_TJ5JEH8W
tags:
  - acoustic-echo-cancellation
  - residual-echo-suppression
  - noise-reduction
  - psychoacoustic-postfilter
  - masking-threshold
  - speech-enhancement
  - hands-free-telephony
---

# Gustafsson, Martin, Jax & Vary 2002: A Psychoacoustic Approach to Combined Acoustic Echo Cancellation and Noise Reduction

| Field | Value |
|-------|-------|
| **Authors** | [[entities/stefan-gustafsson|Stefan Gustafsson]], [[entities/rainer-martin|Rainer Martin]], [[entities/peter-jax|Peter Jax]], [[entities/peter-vary|Peter Vary]] |
| **Institution** | Institute of Communication Systems and Data Processing (IND), RWTH Aachen University, Germany |
| **Published** | IEEE Transactions on Speech and Audio Processing, vol. 10, no. 5, pp. 245–256, July 2002 |
| **Type** | Journal Article |
| **DOI** | [10.1109/TSA.2002.800553](https://doi.org/10.1109/TSA.2002.800553) |
| **Zotero** | [TJ5JEH8W](zotero://select/items/0_TJ5JEH8W) |

**Venue**: IEEE Transactions on Speech and Audio Processing, vol. 10, no. 5, pp. 245–256, July 2002

## Summary

This paper presents and compares two frequency-domain postfilter weighting rules that, placed in the sending path behind a conventional (NLMS-adapted) acoustic echo canceler, jointly attenuate the residual echo and the background noise of hands-free telephones. The first rule extends the MMSE-LSA noise-reduction estimator to residual echo by estimating separate SNRs against echo and noise and combining them; the second is a psychoacoustically motivated rule that attenuates echo and noise by predefined factors while keeping the resulting distortions just below the masking threshold of the near-end speech. Instrumental measures show the two rules perform about equally, but listening tests strongly prefer the psychoacoustic rule (97% preference in stationary double talk) for its more natural near-end speech and less annoying residual noise.

## Problem Formulation

Hands-free telephony suffers from two impairments at once: the acoustic echo picked up from the loudspeaker (critical under the long round-trip delays of mobile networks, e.g. ~180 ms in GSM) and background noise (a car cabin typically yields ~20 dB lower SNR than a handset). The microphone signal is

$$y(k) = s(k) + n(k) + d(k),$$

and the echo canceler $C$ produces $\hat{d}(k)$, leaving the echo-canceled signal

$$e(k) = s(k) + n(k) + \underbrace{d(k) - \hat{d}(k)}_{b(k)},$$

where $b(k)$ is the residual echo. The postfilter operates frame-wise in the frequency domain: frames of $M$ samples (every $L$ samples), Hamming-windowed, zero-padded to $N$, transformed by DFT, multiplied by real gains $H^{(\lambda)}(\Omega_i) \geq 0$, and resynthesized by overlap-and-add:

$$\hat{S}^{(\lambda)}(\Omega_i) = H^{(\lambda)}(\Omega_i)\, E^{(\lambda)}(\Omega_i).$$

The postfilter deliberately relieves the echo canceler: because $H$ cleans up the residual echo, $C$ can use a much lower filter order — it converges faster, is more robust to noise and double talk, and the *total* system complexity can drop while echo attenuation rises.

![[raw/papers/gustafsson-2002-psychoacoustic-aec-nr/figures/3b1481fbdc4f947e5bc495ef809eba2caf7131b79a4e8d036ad339745dccace0.jpg|Figure 1]]

*Figure 1: System with echo canceler C and postfilter H. The postfilter is placed in the sending path to attenuate both residual echo and noise.*

## Methodology

### Residual Echo PSD Estimation

The postfilter needs the residual echo PSD $R_{bb}(\Omega)$, which is unobservable and speech-like (time-variant). Two observations from extensive simulations motivate the estimators:

1. When the adaptive filter tracks the room well, the magnitude and phase errors are small, but the residual phase can be arbitrary.
2. When the filter is misadjusted (interference or echo-path change), the residual echo is dominated by the *magnitude* error and the phase error is near $0$ or $\pi$, so at frequencies where attenuation matters, $\arg B(\Omega) \approx \arg D(\Omega)$.

![[raw/papers/gustafsson-2002-psychoacoustic-aec-nr/figures/8d9c610dba53c3670daa7af16ac9d2f573c35dd5d84eb418df058874214c143e.jpg|Figure 2]]

*Figure 2: Frequency-domain vector representation of the echo $D(\Omega)$, the estimated echo $\hat{D}(\Omega)$, the residual echo $B(\Omega)$, the phase error $\phi(\Omega)$, and the phase deviation $\psi(\Omega)$ for an arbitrary frequency.*

The phase observation lets the echo cancellation be modeled as a *virtual* real-valued system $F(\Omega)$ with $B(\Omega) = F(\Omega) D(\Omega)$, which yields two residual echo PSD estimators:

- **Equivalent transfer function (ETF) method** — $F(\Omega)$ is expressed purely in terms of PSDs of *measurable* signals (microphone, echo-canceled, estimated echo):

$$F(\Omega) = \frac{R_{yy}(\Omega) - R_{ee}(\Omega) - R_{\hat d\hat d}(\Omega)}{R_{yy}(\Omega) - R_{ee}(\Omega) + R_{\hat d\hat d}(\Omega)},\qquad
\hat R_{bb}^{(F)}(\Omega) = \left(\frac{\hat F(\Omega)}{1-\hat F(\Omega)}\right)^{2} R_{\hat d\hat d}(\Omega).$$

- **Coherence method** — driven by the magnitude-squared coherence between the far-end signal and the echo-canceled signal:

$$\hat R_{bb}^{(C)}(\Omega) = \Gamma_{xe}(\Omega)\, R_{ee}(\Omega),\qquad
\Gamma_{xe}(\Omega) = \frac{|R_{xe}(\Omega)|^2}{R_{xx}(\Omega) R_{ee}(\Omega)}.$$

Since both estimators are error-prone in different ways, the final estimate is the conservative minimum of the two:

$$\hat R_{bb}(\Omega) = \min\!\left(\hat R_{bb}^{(F)}(\Omega),\, \hat R_{bb}^{(C)}(\Omega)\right).$$

### Conventional Baseline: MMSE-LSA for Combined Residual Echo and Noise

The MMSE-LSA weighting rule (Ephraim & Malah 1985) is extended from noise-only to joint residual echo + noise by treating the two interferences *separately*. Individual a priori / a posteriori SNRs are defined against $b$ and $n$ alone ($SNR_b^s = R_{ss}/R_{bb}$, $SNR_n^s = R_{ss}/R_{nn}$, $\gamma_b^e = |E|^2/R_{bb}$, $\gamma_n^e = |E|^2/R_{nn}$) and combined by the parallel ("resistor") rule

$$SNR_{b+n}^s = \frac{1}{\left[SNR_b^s\right]^{-1} + \left[SNR_n^s\right]^{-1}},\qquad
\gamma_{b+n}^e = \frac{1}{\left[\gamma_b^e\right]^{-1} + \left[\gamma_n^e\right]^{-1}},$$

then inserted into the LSA gain

$$H^{LSA}(\Omega) = \frac{SNR_{b+n}^s}{SNR_{b+n}^s + 1}\exp\!\left(\frac{1}{2}\int_{\Psi}^{\infty}\frac{e^{-\tau}}{\tau}\,d\tau\right),\qquad
\Psi(\Omega) = \frac{SNR_{b+n}^s}{1+SNR_{b+n}^s}\,\gamma_{b+n}^e.$$

The individual a priori SNRs are estimated by the decision-directed approach with *different* smoothing factors for the two interferences ($\alpha_n = 0.98$, $\alpha_b = 0.90$), reflecting their different statistics. To keep the residual background noise level constant, the SNR estimates are floored before combination: the noise SNR by a constant threshold $T_n$ (0.16 in the evaluation), and the residual echo SNR by an *adaptive* threshold $\tilde T_b(\Omega_i) = 2T_b / (1 + 2\hat R_{bb}/\hat R_{nn})$ that rises with the noise level — when noise is strong it already masks the echo, so extra echo attenuation would only cause unpleasant fluctuations.

![[raw/papers/gustafsson-2002-psychoacoustic-aec-nr/figures/925dd51a477f50657ccf3eab496ca33b63893bd2c217cf1ab392be23bdc9fbac.jpg|Figure 4]]

*Figure 4: Block diagram of a system for combined residual echo and noise reduction. The noise PSD is estimated with the minimum statistics method; the residual echo PSD with the ETF/coherence estimators.*

### Psychoacoustically Motivated Weighting Rule $\tilde H^{IND}$

The design goal is *not* complete removal: residual echo and noise should be attenuated by predefined factors $\zeta_b, \zeta_n \in [0,1]$ (e.g. $\zeta_b = 0.0003 \widehat{=} -35$ dB, $\zeta_n = 0.01 \widehat{=} -40$ dB in the evaluation), preserving the natural character of the remaining noise. With desired output $\check S = S + \zeta_b B + \zeta_n N$, the error against the actual output $H(S+B+N)$ splits into three independent distortion components:

$$R_{qq} = \underbrace{(1-H)^2 R_{ss}}_{\text{speech distortion}} + \underbrace{(\zeta_b - H)^2 R_{bb}}_{\text{excess residual echo}} + \underbrace{(\zeta_n - H)^2 R_{nn}}_{\text{excess noise}}.$$

The **design objective** is to make the excess residual echo plus excess noise *just masked* by the near-end speech — i.e. equal to the masking threshold $R_{TT}(\Omega)$ — with minimum impact on the speech. Solving the resulting quadratic (with the practical simplification $|\zeta_b - \zeta_n|^2 R_{bb} R_{nn} \ll (R_{bb}+R_{nn})R_{TT}$) gives

$$\tilde H^{IND}(\Omega) = \min\!\left(1,\ \sqrt{\frac{R_{TT}(\Omega)}{R_{bb}(\Omega) + R_{nn}(\Omega)}} + \frac{\zeta_n R_{nn}(\Omega) + \zeta_b R_{bb}(\Omega)}{R_{nn}(\Omega) + R_{bb}(\Omega)}\right),$$

where "IND" stands for **inaudible noise distortion**. Key properties:

- If excess echo and noise are already masked by near-end speech, $\tilde H^{IND} = 1$ — the speech is *not* distorted, unlike conventional rules.
- If neither near-end speech nor residual echo is present, $\tilde H^{IND} = \zeta_n$ for all $\Omega$ — the output is a constant-scaled copy of the input, which structurally rules out musical noise.
- The masking threshold $R_{TT}(\Omega)$ is computed with **MPEG-1 Psychoacoustic Model 2** (adapted to 8 kHz) from a *preliminary* near-end estimate $S'(\Omega)$ obtained by a conventional combined rule (the LSA rule of the previous subsection).

![[raw/papers/gustafsson-2002-psychoacoustic-aec-nr/figures/2bd1490c10439eaac10f8eb55dd7c38d2a488f85f9832e2a7bdfd37ecf6691cd.jpg|Figure 5]]

*Figure 5: Block diagram of the combined residual echo and noise reduction system using the psychoacoustically motivated weighting rule. A preliminary speech estimate drives the masking threshold estimation; the final weighting uses $\tilde H^{IND}$.*

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Platform** | C++ implementation on a general-purpose computer; real-time (floating point) on a 600 MHz Alpha PC |
| **Sampling / STFT** | 8 kHz; frame $M = 256$, hop $L = 128$, zero-padded DFT $N = 512$, Hamming window |
| **Echo path** | Time-invariant FIR (≈400 coefficients) measured in a small car |
| **Echo canceler** | NLMS with variable step-size control (Frenzel) + prewhitening filters (Antweiler); filter length $N_c = 200$ (deliberately half the necessary order) |
| **Noise PSD** | Minimum statistics (R. Martin 1994) — VAD-free |
| **Masking threshold** | MPEG-1 Psychoacoustic Model 2, adapted to 8 kHz |
| **Parameters $\tilde H^{IND}$** | $\zeta_n = 0.01$, $\zeta_b = 0.0003$ |
| **Parameters $H^{LSA}$** | $T_n = 0.16$, $T_b = 0.025$, tuned to match $\tilde H^{IND}$'s double-talk attenuation at 0 dB SNR |
| **DD smoothing** | $\alpha_n = 0.98$, $\alpha_b = 0.90$ |
| **Speech material** | 8 phonetically balanced sentences per condition (male + female), per operating mode |
| **Noise** | Car noise recorded at ~100 km/h on a dry highway |
| **Operating modes** | Noise reduction (far-end silent); Single talk (near-end silent); Double talk (both active, echo power = near-end speech power) |
| **SNR range** | Input segmental SNR 5–30 dB (noise and single talk); echo-to-noise ratio 5–30 dB |
| **Instrumental metrics** | Noise attenuation (NA), speech attenuation (SA), segmental SNR, cepstral distance, $ERLE_C$ (canceler alone), $ERLE_{CH}$ (canceler + postfilter) |
| **Listening tests** | 9 expert listeners (1 familiar with AEC), 8 samples per condition, stationary and rapidly changing echo paths |

## Results

### Instrumental (all measures cross-plotted vs. SNR in Figs. 6–8 of the paper)

- **Noise reduction**: for $SEGSNR \geq 5$ dB, $\tilde H^{IND}$ gives ~1 dB *less* noise reduction than $H^{LSA}$ — masked noise need not be removed — but clearly higher segmental SNR (less speech distortion) at high input SNR, and lower speech attenuation.
- **Single talk**: the under-modeled canceler achieves only $ERLE_C = 10$–$20$ dB; with the postfilter the system reaches **~40 dB total echo attenuation** for both rules (target per ITU-T G.167: 45 dB single talk / 30 dB double talk). The postfilter's contribution falls short of the full 35 dB target due to residual echo PSD estimation error and noise. Strong noise *lowers* the additional attenuation — desired, since noise masks the residual echo. Noise attenuation for $\tilde H^{IND}$: 15–20 dB.
- **Double talk**: $ERLE_{CH}$ and NA are practically identical for both rules; $ERLE_C$ is lower than in single talk (near-end speech interferes with adaptation), and the postfilter adds less attenuation — again desired, as near-end speech masks part of the residual echo. Overall speech attenuation is lower for $\tilde H^{IND}$.

### Auditive (listening tests)

- **Noise reduction mode**: $\tilde H^{IND}$ yields more natural speech; with both rules the residual noise sounds like an attenuated version of the original (no artifacts for stationary noise).
- **Single talk without near-end noise**: no significant difference; both suppress the residual echo well.
- **Double talk** (differences most notable): the psychoacoustic rule was preferred in **97%** of judgments under stationary conditions (0 dB SNR) and in **75%** under rapidly changing echo paths. Listeners reported more natural near-end speech and a more noise-like, less annoying residual echo; the $H^{LSA}$ residual echo was clearly recognizable as speech and the near-end speech sounded more metallic. The authors attribute part of the improvement to computing the masking threshold in the critical-band domain, which smooths annoying echo/noise fluctuations.

## Key Contributions

1. **Combined AEC + postfilter structure for hands-free telephony** — a joint residual echo and noise reduction postfilter in the sending path that lets the echo canceler run at deliberately reduced order (half the room response length), improving convergence and robustness while reducing total complexity.
2. **Residual echo PSD estimation** — a frequency-domain phase analysis ($\arg B \approx \arg D$ where attenuation matters) leading to the equivalent-transfer-function estimator, combined conservatively (minimum) with the coherence estimator.
3. **Separate-SNR extension of MMSE-LSA** — treating residual echo and noise as separate interferences with individual DD-estimated SNRs ($\alpha_b \neq \alpha_n$), combined by a parallel rule, with an adaptive echo-SNR threshold that keeps the background noise level constant.
4. **The $\tilde H^{IND}$ psychoacoustic weighting rule** — attenuating residual echo and noise by predefined factors $\zeta_b, \zeta_n$ while constraining the *excess* distortions to equal the masking threshold (MPEG-1 Model 2) of the near-end speech; structurally immune to musical noise and leaving masked components untouched.
5. **Evidence that perceptual rules win where instrumental measures tie** — after parameter matching, all instrumental measures coincide (except less speech distortion at high SNR for $\tilde H^{IND}$), yet listeners strongly prefer the psychoacoustic rule (97% / 75% in double talk).

## Related Concepts

- [[concepts/psychoacoustic-postfilter|Psychoacoustic Postfilter]] — this paper is the original derivation of the $\tilde H^{IND}$ masking-threshold weighting rule for *combined* residual echo and noise.
- [[concepts/residual-echo-suppression|Residual Echo Suppression]] — the postfilter's residual-echo function; the paper's ETF + coherence estimators are the "traditional baseline" of later RES work.
- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]] — the upstream NLMS canceler whose demands the postfilter relaxes.
- [[concepts/decision-directed-a-priori-snr|Decision-Directed A Priori SNR Estimation]] — used with interference-specific smoothing factors ($\alpha_b = 0.90$, $\alpha_n = 0.98$).
- [[concepts/minimum-statistics|Minimum Statistics]] — supplies the VAD-free noise PSD estimate for the postfilter.
- [[concepts/echo-return-loss-enhancement|Echo Return Loss Enhancement (ERLE)]] — evaluated in the two-stage form $ERLE_C$ (canceler) and $ERLE_{CH}$ (canceler + postfilter).
