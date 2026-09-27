---
type: source
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/watanabe-2026-low-frequency-harmonic-control/full-text.md
  - https://doi.org/10.1109/ICASSP55912.2026.11464695
  - zotero://select/items/0_CXS5AJK6
tags:
  - post-filter
  - harmonic-emphasis
  - low-complexity
  - intelligibility
  - open-ear-headphones
  - speech-processing
---

# Watanabe, Chiba, Kamamoto & Kako 2026: Low-Frequency Harmonic Control for Speech Intelligibility in Open-Ear Headphones

**Authors**: [[entities/yuki-watanabe|Yuki Watanabe]], [[entities/hironobu-chiba|Hironobu Chiba]], [[entities/yutaka-kamamoto|Yutaka Kamamoto]], [[entities/tatsuya-kako|Tatsuya Kako]]
**Affiliation**: NTT Inc., Tokyo, Japan
**Venue**: IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) 2026
**Year**: 2026
**Type**: Conference paper
**DOI**: [10.1109/ICASSP55912.2026.11464695](https://doi.org/10.1109/ICASSP55912.2026.11464695)
**Zotero**: [CXS5AJK6](zotero://select/items/0_CXS5AJK6)

## Summary

This paper presents **Low-Frequency Harmonic Control (LFHC)**, a low-complexity post-filter that improves the intelligibility of speech played back through [[concepts/open-ear-headphones|open-ear headphones]] in noisy environments without amplifying volume. The method suppresses the fundamental frequency and reinforces the second and third harmonics, reallocating speech energy into bands that are less masked by low-frequency environmental noise and less constrained by the weak low-frequency output of the small loudspeaker units in open-ear designs. In a MUSHRA-like subjective evaluation under Brown noise at 69 dB SPL, LFHC with weighting factor $\alpha = 0.6$ significantly improved intelligibility for 3 of 6 utterances while not reducing it for the others, with the benefit largest for speech whose low-order harmonics are weak relative to the fundamental.

## Problem Formulation

Open-ear headphones do not occlude the ear canal, providing breathability, long-term comfort, and high acoustic transparency — but the small speaker units this design requires have a high lowest resonant frequency and therefore poor output below resonance. Two constraints frame the problem:

1. **Masking**: urban and bustling noise has large low-frequency components, so the (weak) fundamental of replayed speech is strongly masked.
2. **Output limitation**: emphasizing the fundamental to overcome masking is limited by the loudspeaker's low-frequency output, and naive amplification causes distortion; nonlinear-distortion compensation (e.g., Klippel-style) is too computationally complex for the small DSP inside open-ear housings.

The design target is therefore a method that (i) improves intelligibility **beyond simple volume amplification** by suppressing energy that does not contribute to intelligibility (the masked fundamental) and emphasizing energy that does (the low-order harmonics), (ii) is implementable in real time on a resource-constrained DSP (motivating post-filtering, as used in speech coding), and (iii) minimally disturbs the formant frequencies that carry phonetic information.

## Methodology

LFHC adapts the conventional pitch-enhancement post-filter from speech coding (comb filter with delay $\tau_0$, the estimated pitch period, plus low-pass weighting). Pitch period $\tau_0$ is estimated per frame (several tens of milliseconds) via autocorrelation.

![[raw/papers/watanabe-2026-low-frequency-harmonic-control/figures/6d84f3d9c49613569216d2086889dda57ebcde99211174504a1ff1fdfee0dee1.jpg|Block diagram of pitch emphasis processing]]
*Figure 1: Block diagram of pitch emphasis processing (Watanabe et al. 2026, Fig. 1).*

**Single-tap FIR comb filter.** The delayed signal is

$$r[n] = \alpha\, s[n - \tau]$$

where $\alpha$ ($0 < \alpha < 1$) is the weighting factor; larger $\alpha$ means stronger emphasis. In conventional pitch enhancement $\tau = \tau_0$ (which enhances the fundamental); LFHC instead uses $\tau = \tau_0 / 2.5$, which **suppresses the fundamental and emphasizes the second and third harmonics**. The delay choice follows two considerations:

- If $\tau \approx \tau_0/2$, the comb nulls align with the fundamental *and its odd-order harmonics*, suppressing too much.
- If $\tau \approx \tau_0/3$, emphasis falls on the third harmonic, which carries less energy than the second due to the average spectral tilt of speech.

**Low-pass weighting.** A moving-average FIR low-pass filter with cutoff $F_C = 5 f_0$ confines emphasis to at most the third harmonic, minimizing influence on formant frequencies. The filter length is approximated as $N \approx F_S / (2 F_C)$ ($F_S$ = sampling frequency), and the group delay $\tau_g = (N-1)/2$ it introduces is compensated in the comb delay:

$$\tau = \frac{\tau_0}{2.5} - \frac{N-1}{2}$$

**Output.** The final signal adds the original and the low-pass-filtered delayed signal:

$$s_{\mathrm{out}}[n] = s[n] + r_{\mathrm{LP}}[n]$$

![[raw/papers/watanabe-2026-low-frequency-harmonic-control/figures/a8674a0fe01798f3a827587903e2895b52613214a3e507f9b45b8933c392d7c9.jpg|Spectrogram difference before and after processing]]
![[raw/papers/watanabe-2026-low-frequency-harmonic-control/figures/9a8e7b4c284588163fb46d83ad78bf9e51246974f003c4616922c985d9ed7c45.jpg|Spectral envelope of processed speech]]
*Figure 2: Spectrogram difference before and after processing (left) and spectral envelope of the processed speech (right, first 1 s of the left audio) — the fundamental is suppressed while the second and third harmonics are emphasized (Watanabe et al. 2026, Fig. 2).*

## Experimental Setup

| Item | Detail |
|------|--------|
| Room | Reverberation time RT ≈ 0.1 s |
| Noise | Brown noise (−6 dB/oct., same spectral tilt as outdoor bustle noise), 69 dB SPL / 60 dB(A) at listening point, 48 kHz, via Genelec 8030C loudspeakers |
| Playback device | Open-ear headphone "nwm wired" (lowest resonant frequency ≈ 290 Hz) |
| Speech | 16 kHz (web-meeting scenario); 6 samples, one per talker (3 female F1–F3, 3 male M1–M3), selected from 30 sentence pairs as the utterance with the *lowest* mean energy ratio of 2nd/3rd harmonic to $f_0$ |
| Pitch estimator | MATLAB `pitch` function (PEF method) |
| Conditions | OR (60 dB), OR-3 (57 dB), OR-6 (54 dB), LFHC-3(0.6) ($\alpha = 0.6$, 57 dB), LFHC-3(0.9) ($\alpha = 0.9$, 57 dB) |
| Evaluation | MUSHRA-like (intelligibility criterion, low-intelligibility anchors, < 20 listeners); Intelligibility Score = condition score − OR-3 score |
| Listeners | 8 well-trained (5M/3F, mean age 35.9, SD 9.2) |
| SNR | ≈ −5 dB(A) (speech 54–56 dB(A) vs noise 60 dB(A)) |

![[raw/papers/watanabe-2026-low-frequency-harmonic-control/figures/098e3bb1f3a6bea237133e7b707438f480838f9332bdaaff9720b7f7760e09a3.jpg|Headphone transfer function of the earphone used]]
*Figure 3: Headphone transfer function of the open-ear earphone used (nwm wired), showing weak output below the ≈ 290 Hz resonance (Watanabe et al. 2026, Fig. 4).*

## Results

![[raw/papers/watanabe-2026-low-frequency-harmonic-control/figures/507e1ab21e66260ad2fef5c8f2ab61cd37b7a00670acf36112dde59244b68714.jpg|Results of the subjective evaluation experiment]]
*Figure 4: Results of the subjective evaluation experiment — mean Intelligibility Scores with 95% confidence intervals (Watanabe et al. 2026, Fig. 5).*

- **LFHC-3(0.6)**: significantly *more* intelligible than the unprocessed OR-3 condition for **3 of 6** speech samples; **not reduced** for the remaining 3.
- **LFHC-3(0.9)**: significantly *less* intelligible for **2 of 6** samples. Two hypothesized causes: excessive suppression/enhancement degrading the harmonic structure, and artifacts from incorrect harmonic control under pitch estimation errors becoming more prominent at higher $\alpha$.

![[raw/papers/watanabe-2026-low-frequency-harmonic-control/figures/115223859470711ad732bd405290ca13b16e3598bb5ea3bd01eb4e2e74db5540.jpg|Scatter plot of harmonic energy ratio vs Intelligibility Score]]
*Figure 5: Scatter plot of the mean energy ratio of the low-order harmonics relative to the fundamental vs. the Intelligibility Score ($\alpha = 0.6$); correlation coefficient −0.93 (Watanabe et al. 2026, Fig. 6).*

- The processing benefit **correlates −0.93** with the pre-processing mean energy ratio of the 2nd/3rd harmonics to the fundamental: LFHC helps most for speech whose low-order harmonics are weak relative to the fundamental, and has little effect when they are already strong. The authors propose adapting the processing based on this energy ratio as future work.

## Key Contributions

1. **LFHC method**: a low-delay, low-complexity post-filter that suppresses the fundamental and emphasizes the 2nd/3rd harmonics via a single-tap FIR comb filter ($\tau = \tau_0/2.5$) with group-delay-compensated moving-average low-pass weighting ($F_C = 5 f_0$) — implementable on the small DSP inside open-ear headphone housings.
2. **Energy-reallocation principle**: instead of amplifying speech into a masked, output-limited low-frequency band, move energy to bands that are less masked by environmental noise and less constrained by the loudspeaker — improving intelligibility without volume increase.
3. **Subjective validation**: under Brown noise at 69 dB SPL (SNR ≈ −5 dB(A)), $\alpha = 0.6$ significantly improved intelligibility for 3/6 utterances and degraded none; $\alpha = 0.9$ over-processed.
4. **Predictive insight for adaptation**: the Intelligibility Score correlates −0.93 with the pre-processing 2nd/3rd-harmonic-to-fundamental energy ratio, motivating per-signal adaptation of the processing.

## Related Concepts

- [[concepts/low-frequency-harmonic-control|Low-Frequency Harmonic Control (LFHC)]]
- [[concepts/open-ear-headphones|Open-Ear Headphones]]
- [[concepts/hearables|Hearables]]
- [[concepts/psychoacoustic-postfilter|Psychoacoustic Postfilter]]

## Related Synthesis

- [[synthesis/application-specific-anc|Application-Specific ANC]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
