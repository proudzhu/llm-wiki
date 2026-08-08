---
type: source
created: 2026-08-08
updated: 2026-08-08
sources:
  - raw/papers/wung-2011-residual-echo-suppression-system/full-text.md
  - https://doi.org/10.1109/ICASSP.2011.5946436
  - zotero://select/items/0_PUI8FYUL
tags:
  - acoustic-echo-cancellation
  - residual-echo-suppression
  - psychoacoustic-postfilter
  - speech-enhancement
  - robust-aec
  - error-recovery-nonlinearity
  - log-spectral-amplitude
  - masking-threshold
  - double-talk
  - hands-free-teleconferencing
---

# Wung, Wada & Juang 2011: A System Approach to Residual Echo Suppression

| Field | Value |
|-------|-------|
| **Authors** | [[entities/jason-wung|Jason Wung]], [[entities/ted-wada|Ted S. Wada]], [[entities/biing-hwang-juang|Biing-Hwang (Fred) Juang]], [[entities/bowon-lee|Bowon Lee]], [[entities/ton-kalker|Ton Kalker]], [[entities/ronald-schafer|Ronald W. Schafer]] |
| **Institution** | Center for Signal and Image Processing, Georgia Institute of Technology; Hewlett-Packard Laboratories |
| **Published** | Proc. IEEE ICASSP 2011, pp. 4456–4459 |
| **Type** | Conference Paper |
| **DOI** | [10.1109/ICASSP.2011.5946436](https://doi.org/10.1109/ICASSP.2011.5946436) |
| **Zotero** | [PUI8FYUL](zotero://select/items/0_PUI8FYUL) |

## Summary

This paper presents a *system approach* to residual echo suppression (RES) for robust hands-free teleconferencing. Rather than treating RES as an isolated post-processing stage, the authors exploit the noise-robustness of their existing [[concepts/acoustic-echo-cancellation|acoustic echo cancellation]] (AEC) system — built on [[concepts/error-recovery-nonlinearity|error recovery nonlinearity]] (ERN) and batch adaptation — to derive a residual echo estimate that closely resembles the true, noise-free residual echo. The estimate is formed as the difference between a nonlinear (log-spectral-amplitude) echo estimate and the linear AEC echo estimate. A [[concepts/psychoacoustic-postfilter|psychoacoustic postfilter]] then suppresses the residual echo as much as possible without introducing audible distortion, leveraging frequency masking from MPEG-1 Psychoacoustic Model 2. The combined system outperforms a traditional equivalent-transfer-function + coherence-function (ETF+CF) baseline on SSRR, LSD, and PESQ, raising PESQ by more than half a point over the unprocessed AEC output.

## Problem Formulation

A single-channel AEC system models the near-end microphone signal as

$$y[n] = d[n] + v[n],$$

where $d = \mathbf{h}^\mathrm{T}\mathbf{x}$ is the acoustic echo (room impulse response $\mathbf{h}$ convolved with the far-end reference $\mathbf{x}$), and $v$ is the near-end signal (speech and/or noise). The adaptive filter $\mathbf{w}$ produces the linear echo estimate $\hat{d} = \mathbf{w}^\mathrm{T}\mathbf{x}$, and the AEC estimation error is

$$e[n] = v[n] + d[n] - \hat{d}[n] = v[n] + b[n],$$

where $b = (\mathbf{h}^\mathrm{T} - \mathbf{w}^\mathrm{T})\mathbf{x}$ is the *true* (noise-free) residual echo. Strong near-end interference $v$ during double talk corrupts $e$ and can cause the adaptive filter to diverge in a conventional AEC; the ERN reduces this disturbance so the linear filter can keep tracking the room response.

The RES stage needs a residual echo variance estimate $\hat{\lambda}_B(k)$ to drive an LSA spectral gain $G_{\mathrm{LSA}}(k) \in [0,1]$ applied to $E_k$. The central difficulty is that $b$ is unobservable and is corrupted by $v$, so estimating $\lambda_B(k)$ accurately — especially during double talk — is the bottleneck of traditional RES.

![[raw/papers/wung-2011-residual-echo-suppression-system/figures/b19c313e461ceb4f945c5a87abda1b9d8ccaf9d119b40ca37a069d2eea3505f0.jpg|Figure 1]]

*Figure 1: AEC system with adaptive filter w, error recovery nonlinearity (ERN), and a psychoacoustic postfilter H.*

## Methodology

The paper's contribution is a *system-level* residual echo estimate that exploits both the linear (AEC) and nonlinear (LSA) echo estimates, analyzed under three operating conditions.

### Robust AEC with Error Recovery Nonlinearity

The robust AEC from the authors' prior work [1] uses ERN and batch adaptation, allowing the adaptive filter to update continuously during double talk **without** a double-talk detector (DTD) or voice activity detector. This robustness is the foundation that makes the proposed RES tractable: after convergence, $|E_k| \approx |V_k|$ because $\lambda_B \ll \lambda_V$ during double talk and $\lambda_B \ll \lambda_D$ during single talk.

### Proposed Residual Echo Estimate

The key idea is to obtain a nonlinear echo estimate $\tilde{d}$ by applying the LSA estimator to the microphone signal $Y$ (treating $v$ as additive noise), then subtracting the AEC's linear estimate $\hat{d}$:

$$\hat{b}[n] = \tilde{d}[n] - \hat{d}[n] = f_{\mathrm{LSA}}\{Y, \lambda_V\} - \hat{d}[n].$$

The LSA estimator uses the decision-directed (DD) a priori SNR estimator with weighting $\alpha = 0.98$:

$$\hat{\xi}_k^{\mathrm{DD}}(m) = \alpha \frac{|\tilde{V}_k(m-1)|^2}{\lambda_B(k, m-1)} + (1-\alpha)\max\{0, \gamma_k(m) - 1\}.$$

The estimate is justified by case analysis:

- **Near-end talk (NT)**: $D_k = 0$, so $Y_k = V_k$; the LSA filter suppresses all near-end signal and $\tilde{D}_k \approx 0$.
- **Single talk (ST)**: $V_k = 0$, so $Y_k = D_k$ and $E_k = B_k$; since $\lambda_D \gg \lambda_B$, $G_{\mathrm{LSA}} \approx 1$ and $\tilde{D}_k \approx D_k$.
- **Double talk (DT)**: $Y_k = D_k + V_k$ and $E_k = V_k + B_k$; since $\lambda_V \gg \lambda_B$ (robust AEC) and $V_k \perp B_k$, $\lambda_E \approx \lambda_V$, so the LSA filter removes mostly $V$ and $\tilde{D}_k \approx D_k$.

Overestimation of $\hat{B}$ during strong double talk is harmless because the masking threshold is also high then.

### Psychoacoustic Postfilter

To suppress the residual echo without audible distortion of near-end speech, a psychoacoustic postfilter [4] sets the gain so that the residual echo distortion equals the masking threshold $T_V(k)$ of the near-end signal:

$$H_k = \min\left\{1, \sqrt{\frac{T_V(k)}{\lambda_B(k)}}\right\}.$$

If the residual echo is already masked by the near-end signal ($T_V(k) > \lambda_B(k)$), then $H_k = 1$ and the near-end signal passes undistorted. The masking threshold is estimated using **MPEG-1 Psychoacoustic Model 2**.

![[raw/papers/wung-2011-residual-echo-suppression-system/figures/9d0326a01edc150046e244b449f94d7e6163841c6fe95b9b9439b2e545146a45.jpg|Figure 2]]

*Figure 2: Block diagram of the psychoacoustic postfilter. The LSA gain produces a rough near-end estimate $\tilde{V}_k$, from which the masking threshold $T_V(k)$ is computed; the postfilter gain $H_k$ is then applied to $E_k$.*

![[raw/papers/wung-2011-residual-echo-suppression-system/figures/acbba0ef968068b131e1262ff843327fec4402859977386efbecdb5fa402f8f3.jpg|Figure 3]]

*Figure 3: Spectrograms (up to 4 kHz) comparing the proposed residual echo estimate $\hat{B}$ to the true residual echo $B$, at 10 dB SSNR air-conditioner noise.*

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Database** | TIMIT (female far-end, male near-end), 16 kHz 16-bit PCM |
| **Echo return loss** | 10 dB (far-end normalized to $[-1,1]$, near-end speech of equal power) |
| **Noise** | Air-conditioner noise at 0–30 dB SSNR (10 dB steps) |
| **Test pairs** | 10 near/far-end pairs, ~20 s each; first 5 s (single talk) reserved for convergence, removed before scoring |
| **Talk pattern** | Far/near-end alternating with 1 s overlap |
| **AEC variants** | Robust AEC [1] (ERN + batch adaptation, no DTD); conventional AEC (no ERN, with DTD, one iteration/block) |
| **RES baselines** | Proposed (system approach); ETF+CF (min of equivalent transfer function & coherence function methods) |
| **Postfilter** | Hamming window, frame 512, 75% overlap; DD $\alpha = 0.98$; masking threshold via MPEG-1 Psychoacoustic Model 2 |
| **Metrics** | tERLE (true echo return loss enhancement, no $v$); SSRR (segmental signal-to-residual-echo ratio, clamped to [10, 35]); LSD (log-spectral distortion); PESQ (wide-band mode) |
| **Note** | Background noise reduction was *not* performed, so RES effects are isolated |

## Results

### AEC Comparison (tERLE)

The robust AEC adds more than 10 dB tERLE over the conventional AEC across all noise conditions.

| Input SSNR | Conv. AEC | Robust AEC |
|------------|-----------|------------|
| 0 dB | 14.69 | **24.88** |
| 10 dB | 18.96 | **27.01** |
| 20 dB | 19.32 | **29.64** |
| 30 dB | 19.48 | **31.21** |

### RES Comparison (SSRR / LSD / PESQ)

Across all metrics, the proposed system approach matches or exceeds the traditional ETF+CF method on both AEC variants. Key findings:

- **SSRR** (higher is better): the proposed method consistently beats ETF+CF; the gap widens at high SSNR (clean near-end) where accurate residual echo estimation matters most.
- **LSD** (lower is better): the postfiltered robust AEC output scores slightly worse than the unprocessed one due to suppression-gain distortion (largely from background-noise suppression), but the proposed method introduces less distortion than ETF+CF after postfiltering.
- **PESQ** (higher is better): the proposed method always improves the score — by up to **0.53** (robust AEC) and **0.79** (conv. AEC) over the unprocessed outputs. The robust AEC + proposed RES delivers the highest overall perceptual quality.

The system meets the ITU-T G.167 recommendations [7]: **>45 dB tERLE during single talk** and **~30 dB tERLE during double talk** when the near-end signal energy is low; tERLE may drop below 30 dB during double talk only when the residual echo is already masked by the near-end signal.

![[raw/papers/wung-2011-residual-echo-suppression-system/figures/b1a3a3684849716ffbfad01e891b701b9741bb17468718b9daddbad72dd22a75.jpg|Figure 4]]

*Figure 4: Spectrograms (up to 4 kHz) of the near-end signal, robust AEC output, and the two postfiltered results at 10 dB SSNR. The proposed method almost completely removes the residual echo.*

![[raw/papers/wung-2011-residual-echo-suppression-system/figures/112f684081aa78cac388d741ce594129a1d321c832dafe01052613468f57e0dd.jpg|Figure 5]]

*Figure 5: Comparison of tERLE at 30 dB SSNR between the robust AEC and the two RES methods; the proposed RES achieves higher overall tERLE.*

## Key Contributions

1. **A system-level residual echo estimate**: $\hat{b} = \tilde{d} - \hat{d}$, the difference between a nonlinear (LSA) echo estimate and the linear AEC echo estimate, which closely represents the true noise-free residual echo because the robust AEC (with ERN) keeps $\lambda_B \ll \lambda_V$.
2. **Case analysis** (NT/ST/DT) showing why the LSA-filtered echo estimate $\tilde{D} \approx D$ under each operating condition, justifying the estimate without needing a double-talk detector.
3. **Integration of a psychoacoustic postfilter** whose masking-threshold-driven gain avoids audible near-end distortion while still suppressing residual echo, with the gain chosen so that residual echo distortion equals the masking threshold $T_V(k)$.
4. **Demonstration that the robust AEC without RES outperforms a conventional AEC *with* RES**, and that the proposed RES adds a further PESQ gain of up to 0.53 on top of the robust AEC.

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation]] — the linear front-end whose robustness underpins the proposed RES.
- [[concepts/residual-echo-suppression|Residual Echo Suppression]] — the central problem addressed; this paper provides a system-level formulation.
- [[concepts/psychoacoustic-postfilter|Psychoacoustic Postfilter]] — the masking-threshold-driven postfilter suppressing residual echo without audible distortion.
- [[concepts/error-recovery-nonlinearity|Error Recovery Nonlinearity (ERN)]] — the nonlinear stage of the robust AEC that enables DTD-free adaptation during double talk.

## Related Synthesis

- [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multitask Ultra-Low-Latency Speech Enhancement]] — this paper is an early (pre-deep-learning) example of jointly designing AEC and RES as a system rather than isolated stages.
