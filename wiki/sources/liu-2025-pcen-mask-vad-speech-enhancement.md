---
type: source
created: 2026-08-01
updated: 2026-08-01
sources:
  - raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/full-text.md
  - https://patents.google.com/patent/CN119404249A/en/
  - zotero://select/items/0_9KQXCFTE
tags:
  - speech-enhancement
  - training-target
  - pcen
  - voice-activity-detection
  - loss-function
  - patent
  - dolby
---

# Liu, Figin, Zhou & Li 2025: PCEN-Based Mask Thresholding and VAD for DNN Speech Enhancement Training

**Inventors**: [[entities/xiaoyu-liu|Xiaoyu Liu]] (刘晓宇), R. M. Figin (R·M·菲金, romanized from the CN patent), [[entities/cong-zhou|Cong Zhou]] (周聪), [[entities/kai-li|Kai Li]] (李凯)
**Assignee**: Dolby Laboratories Licensing Corporation, San Francisco, CA, USA
**Type**: Patent (invention patent application)
**Publication**: CN 119404249 A (published 2025-02-07); PCT publication WO 2023/205240 A1 (published 2023-10-26)
**Application**: PCT/US2023/019105, filed 2023-04-19; CN national phase entry 2024-12-19
**Priority**: US 63/437,273 (2023-01-05); US 63/493,979 (2023-04-03); PCT/CN2022/087983 (2022-04-20)
**Zotero**: [9KQXCFTE](zotero://select/items/0_9KQXCFTE)

> [!info] Source type
> This is a **patent** rather than a conference/journal paper. It discloses three training-time mechanisms but, like most patents, reports no comparative benchmark tables — the "results" are illustrative figures and exemplary parameter values. Sections below adapt the academic template to a patent's structure (Background & Problems / Methodology / Exemplary Parameters / Claims Overview).

## Summary

This Dolby Laboratories patent proposes three **training-time-only** mechanisms for mask-based DNN speech-enhancement models, all built on Per-Channel Energy Normalization (PCEN): (1) PCEN-based mask thresholding that zeroes the ideal ratio mask (IRM) on time-frequency bands dominated by stationary noise buried in the "clean" training target; (2) a PCEN-based voice activity detector (PCEN-VAD) that classifies frames as speech/non-speech from a frame-level PCEN energy; and (3) a speech-aware, asymmetric loss function whose gradient is made more aggressive on non-speech frames by flipping the sign of the prediction error. The three techniques can be used independently or together, and generalize to multi-task models predicting several IRMs. Crucially, PCEN is used **only to derive thresholds and drive the loss** — it never replaces $S(t,f)$ inside the IRM itself, and it is never applied at inference time.

## Background and Problems

A conventional DNN-based speech-enhancement system (Figure 1) takes a noisy mixture, applies a spectral transform and optional banding, and predicts a per time-frequency band mask — typically the ideal ratio mask:

$$IRM(t,f) = \frac{S(t,f)}{S(t,f) + N(t,f) + E(t,f)} \tag{1}$$

where $S(t,f)$, $N(t,f)$, $E(t,f)$ are the time-frequency band energies of clean speech, noise, and echo. The patent identifies three problems with training against this conventional IRM:

![[raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/figures/306c0b5479d474118977ad55a4abe64ecf373647f196e38586d49f63b60a9a66.jpg|Figure 1: Conventional DNN-based audio processing system — spectral transform and banding feed a DNN that predicts a per-band mask trained against an IRM target.]]
*Figure 1: Conventional DNN-based audio processing system (patent Fig. 1).*

1. **Stationary noise in the "clean" target.** Collecting studio-quality clean speech is hard; recordings usually carry some stationary noise (recording-equipment noise, room noise). Because $S(t,f)$ in Eq. (1) then includes that stationary noise, the IRM is systematically too large, and a DNN trained against it fails to remove the stationary noise at inference.
2. **Low-energy speech bands inflate target variability.** Some speech bands have negligible energy and are perceptually insignificant; omitting them (setting IRM = 0) would reduce target variability and let the model focus on meaningful bands. But a careless global threshold on raw $S(t,f)$ over-suppresses speech — especially in high-frequency bands, which are much quieter than low-frequency ones.
3. **Implicit VAD burden.** A speech-enhancement DNN must behave differently in speech vs. non-speech regions: preserve speech (favoring over-preservation of speech over noise removal) in speech frames, but aggressively suppress artifacts in non-speech frames. This forces the network to implicitly learn a voice activity detector (VAD).

## Methodology

The patent addresses all three problems with PCEN-based techniques. PCEN is introduced as a spectral-normalization front end that, per frequency band $f$, divides the instantaneous energy by a smoothed running average, acting as a **high-pass filter in the log-energy domain** that subtracts slowly varying (mostly stationary-noise) components.

### Per-Channel Energy Normalization (PCEN)

Given the clean-target band-energy spectrogram $S(t,f)$, PCEN is computed per band:

$$PCEN(t,f) = \left(\frac{S(t,f)}{(\varepsilon + M(t,f))^{\alpha}} + \delta\right)^{r} - \delta^{r} \tag{2}$$

$$M(t,f) = (1-s)\cdot M(t-1,f) + s\cdot S(t,f) \tag{3}$$

Because $M(t,f)$ is a smoothed version of $S(t,f)$, the division in Eq. (2) **normalizes each band's loudness**, producing a much narrower dynamic range than raw $S(t,f)$ — every band ends up at a roughly comparable level (Figure 2, lower panel). Rewriting the core term as $\exp(\log S(t,f) - \alpha\log(\varepsilon + M(t,f)))$ makes the high-pass interpretation explicit: the slowly varying $M(t,f)$, which is dominated by stationary noise, is subtracted in the log domain.

![[raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/figures/89686fcab0846302ccc6c415a2e27ea83a6fe21126a32980819185a53ae64afb.jpg|Figure 2: Band energy with stationary noise (top, ~15–20 s) versus its PCEN version (bottom), where the stationary noise is essentially removed.]]
*Figure 2: PCEN removes the stationary-noise floor buried in the "clean" target (patent Fig. 2). Top: raw band energy; bottom: PCEN-normalized energy.*

> [!important] PCEN is used for thresholding, not as a replacement target
> The patent explicitly does **not** define the ideal mask by substituting the PCEN-processed signal for $S(t,f)$ in Eq. (1) — doing so would lose speech (PCEN can drop speech components, as visible in Fig. 2). Instead, PCEN is used only to **decide where to zero the IRM** and to **drive the loss function**. PCEN is computed only at training time.

### Technique 1 — PCEN-Based Mask Thresholding (Problems 1 & 2)

Compute the standard IRM (Eq. 1) and the PCEN metric (Eqs. 2–3). For each time-frequency band, if $PCEN(t,f) < TH_\text{band}$, set $IRM(t,f) = 0$; otherwise leave the IRM unchanged. Because PCEN has already normalized loudness across bands, a single **global** threshold is valid — unlike a threshold on raw $S(t,f)$, which would over-suppress high-frequency speech. The patent recommends choosing $TH_\text{band}$ from a histogram of PCEN band energies as the largest small value that does not zero out meaningful speech.

Zeroing the IRM on stationary-noise bands trains the DNN to **learn to remove** that stationary noise (which the conventional IRM cannot). Zeroing it on perceptually insignificant low-energy bands reduces target variability.

### Technique 2 — PCEN-Based VAD (Problem 3)

A simple frame-level VAD is built on top of the band-level PCEN. For each frame $t$, compute the frame energy $E(t) = \sum_f PCEN(t,f)$. If $E(t) > TH_\text{frame}$, classify the frame as speech; otherwise non-speech. The frame threshold is set empirically as:

$$TH_\text{frame} \approx TH_\text{band} \cdot N \tag{4}$$

where $N$ is the number of bands per frame. All bands in a non-speech frame have their IRM set to 0, further reducing target variability. The patent notes any VAD (e.g., WebRTC VAD) can be substituted, but the PCEN-VAD reuses the same PCEN computation as Technique 1 for free.

### Technique 3 — Speech-Aware Asymmetric Loss (Problem 3)

The loss is designed so that **over-suppression of speech is penalized more than under-suppression of noise**, and so that non-speech frames are suppressed more aggressively than speech frames. Per time-frequency band:

$$\text{loss} = a^{\text{diff}} - \text{diff} - 1 \tag{5}$$

For **speech frames**, the error is the standard signed difference, which lands on the over-suppression (positive `diff`) side with the steeper gradient:

$$\text{diff}_\text{speech} = IRM^{\gamma} - mask_\text{est}^{\gamma} \tag{6}$$

For **non-speech frames** (where the IRM has been zeroed by PCEN-VAD), the sign of `diff` is **flipped** so the prediction always sits on the steeper-gradient (positive `diff`) side, driving the predicted mask aggressively toward 0:

$$\text{diff}_\text{nonspeech} = mask_\text{est}^{\gamma} - IRM^{\gamma} = mask_\text{est}^{\gamma} \tag{7}$$

![[raw/papers/liu-2025-pcen-mask-vad-speech-enhancement/figures/bb35fb15cdaec609f0a25336791f03ef274c41c724f402f01e29304b09860043.jpg|Figure 3: Loss as a function of diff. The positive side (over-suppression of speech, diff > 0) is steeper than the negative side (under-suppression of noise, diff < 0).]]
*Figure 3: Asymmetric loss — over-suppression of speech incurs a larger gradient than under-suppression of noise (patent Fig. 3).*

The final loss is the mean over all time-frequency bands. The patent generalizes this idea: different $(a, \gamma)$ may be used for speech vs. non-speech frames (larger $a$, smaller $\gamma$ for non-speech to sharpen suppression), and the sign-flipping trick extends from frame-level VAD decisions to **sub-band speech-presence-probability (SPP)** decisions within speech frames.

### Multi-Task Extension

The model may predict $K$ IRM heads, each tied to a different audio-processing aspect — e.g., one mask removes all artifacts (noise + reverberation + echo), a second removes all artifacts except reverberation (so $S(t,f)$ is reverberant speech), and a third preserves music/speech. PCEN thresholding and PCEN-VAD can be applied to any subset of these IRM tasks.

## Exemplary Parameters

The patent gives the following illustrative values (stressed to be non-limiting):

| Parameter | Symbol | Value | Role |
|---|---|---|---|
| PCEN stabilization | $\varepsilon$ | $10^{-6}$ | prevents division by zero |
| PCEN gain | $\alpha$ | 0.98 | exponent on the smoothed denominator |
| PCEN bias | $\delta$ | 2 | offset |
| PCEN power | $r$ | 0.5 | compresses dynamic range |
| PCEN smoothing factor | $s$ | 0.2 | running-average update; **larger than the conventional 0.025** |
| Band threshold | $TH_\text{band}$ | $10^{-5}$ | zero IRM where $PCEN < TH_\text{band}$ |
| Bands per frame | $N$ | 56 | gives $TH_\text{frame} \approx 0.0005$ |
| Loss base | $a$ | 2.7 | exponent in Eq. (5) |
| Loss power | $\gamma$ | 0.5 | maps IRM/mask to perceptual scale |

The smoothing factor $s = 0.2$ (vs. the conventional 0.025) is called out as empirically better in this application; a smaller $s$ removes more noise but blurs speech harmonics.

## Claims Overview

The patent has 28 claims across five aspects:

- **Aspect 1 (Claims 1–14)** — Determining at least one mask for training a DNN-based mask model: obtain the target signal's T-F representation, compute its PCEN metric, derive the mask from the PCEN metric. Dependent claims cover the clean-target-as-ground-truth setting, the IRM-adjustment-via-PCEN procedure, the band-level threshold (Claim 9), the frame-level PCEN-VAD classification (Claims 10–12), the explicit PCEN formula (Claim 13), and the multi-task extension (Claim 14).
- **Aspect 2 (Claims 15–23)** — Determining a speech-aware loss function: use a VAD process to determine speech presence, then control the loss gradient accordingly. Dependent claims cover frame/band-level VAD presence (Claims 16–18), the over-suppression-penalized-more design (Claim 19), the explicit loss formula with sign-flipped `diff` for non-speech frames (Claims 20–21), and reusing the Aspect-1 mask as the IRM in the loss (Claim 22).
- **Aspect 3 (Claim 24)** — Training method using the Aspect-1 mask and/or the Aspect-2 loss.
- **Aspect 4 (Claim 25)** — Standalone VAD classification of an audio frame as speech/non-speech from a frame-level PCEN metric.
- **Aspects 5–7 (Claims 26–28)** — Apparatus, computer program, and computer-readable storage medium.

The patent also enumerates 16 "Enumerated Example Embodiments" (EEEs) that restate the three techniques and their combinations in plain language.

## Key Contributions

1. **Repurposing PCEN as a training-time threshold oracle.** PCEN — originally a robust front-end feature for sound-event detection — is used not as an input feature or as a replacement target, but as a per-band loudness normalizer that makes a single global threshold safe, letting the trainer zero stationary noise and perceptually insignificant bands in the IRM.
2. **A self-consistent PCEN-VAD.** A frame-level VAD built by summing band-level PCEN energies, reusing the same PCEN computation as the mask thresholding, with a threshold derived analytically from the band threshold ($TH_\text{frame} \approx TH_\text{band}\cdot N$).
3. **A sign-flipped asymmetric loss for VAD-conditioned training.** A single exponential loss $a^\text{diff}-\text{diff}-1$ with one signed `diff` for speech frames and the opposite sign for non-speech frames, so each region sits on the steeper-gradient side of the curve — preserving speech in speech frames and aggressively suppressing artifacts in non-speech frames. The trick generalizes from frame-level VAD to sub-band speech-presence-probability control.
4. **Multi-task IRM training with selective PCEN application.** The PCEN-thresholding and PCEN-VAD mechanisms apply to any subset of $K$ IRM heads, each targeting a different denoising/dereverberation/echo-suppression aspect.
5. **Training-only scope.** All three mechanisms operate exclusively at training time; the inference-time DNN is unchanged, so the techniques impose no runtime cost.

## Related Concepts

- [[concepts/per-channel-energy-normalization|Per-Channel Energy Normalization (PCEN)]] — the spectral-normalization technique this patent repurposes for training-target thresholding
- [[concepts/ideal-ratio-mask|Ideal Ratio Mask (IRM)]] — the base training target that the PCEN thresholding modifies
- [[concepts/voice-activity-detection|Voice Activity Detection]] — the PCEN-VAD is a training-time VAD used to gate the loss, distinct from inference-time VADs
- [[concepts/output-based-speech-enhancement|Output-Based Speech Enhancement]] — another training-target/loss design approach in the wiki
- Ideal binary mask, complex ratio mask — related mask training targets (plain text; see [[concepts/ideal-binary-mask|IBM]] and [[concepts/complex-ratio-mask|cRM]] pages)

## Related Synthesis

No synthesis page currently incorporates this source. The patent reports no comparative benchmarks (it is a training-target/loss design disclosure, not a system evaluation), so it does not add a row to the multi-task or low-latency comparison tables in [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task Ultra-Low-Latency Speech Enhancement]]. Its multi-task IRM extension is a training-strategy note rather than a low-latency architecture contribution.
