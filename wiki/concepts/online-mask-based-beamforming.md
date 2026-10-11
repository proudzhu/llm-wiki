---
type: concept
created: 2026-10-11
updated: 2026-10-11
sources:
  - raw/papers/boeddeker-2018-neural-mask-beamforming/full-text.md
tags:
  - beamforming
  - online-processing
  - speech-enhancement
  - asr
---

# Online Mask-Based Beamforming

**Online mask-based beamforming** removes the whole-utterance assumptions of the offline neural mask-based beamformer (utterance-level input normalization, whole-utterance [[concepts/spatial-covariance-matrix|SCM]] accumulation, SNR-maximizing reference selection) so the front-end can run causally for streaming far-field ASR. [[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker, Erdogan, Yoshioka & Haeb-Umbach 2018]] develop and compare two schemes.

## Frame-Level Online Beamforming

Beamforming coefficients are recomputed **per frame** from recursively accumulated statistics. Three offline assumptions must be replaced:

1. **Input normalization** — the offline model uses utterance-based batch normalization (per-frequency mean/variance over the whole utterance, learned $\gamma$, $\beta$). Online alternatives:
   - **Online batch normalization**: recursive per-frequency mean/variance estimation with a forgetting factor $\alpha$ (Eq. 2 of the paper);
   - **Intra-frame normalization**: statistics computed along the **frequency axis within each frame** (Eq. 3) — needs no history at all, but uses a different statistical axis than training.
2. **SCM estimation** — the offline mask-weighted accumulation (Eq. 1) is replaced by a **recursive SCM estimate with a burn-in period** $T_{\mathrm{init}}$ (Eq. 4): during burn-in (≈0.64 s in the experiments) the statistics are not yet trusted / the noise SCM could be singular; afterwards the recursion updates with zero latency.
3. **Reference selection** — the offline system picks the reference microphone per frequency bin to maximize output SNR; online this is **fixed to the first channel**, because a time-dependent reference makes the output signal statistics vary over time in ways the acoustic model has never seen.

**Cost**: the fully online configuration degrades WER by **≈16% relative** versus offline (far-field AM, 7-mic: 11.26% → 13.08% with intra-frame normalization), with both the covariance-estimation and the normalization changes contributing. Notably, the BCE-trained mask network performed *better* than the LogMel-MSE-trained one in this configuration. The online mask-based beamformer matches the engineered online differential beamformer on the near-field AM and is slightly worse on the far-field AM.

## Segment-Level Online (Streaming) Beamforming

The recording is processed in **fixed-duration segments** of $T_s$ seconds, each with a preceding context window of $T_c$ seconds:

- Masks predicted on the context+segment span are weighted by **exponentially decaying scales** over time — $e^{-t/\tau_x}$ for speech, $e^{-t/\tau_n}$ for noise — with $\tau_n > \tau_x$: noise statistics change more slowly, so more context is exploited for noise than for speech.
- SCM accumulation and beamforming coefficients are computed **per segment** and applied to the central segment, incurring a processing delay of $T_s$; a **zero-delay variant** instead applies the coefficients to the *next* segment.
- Chosen parameters: $T_s = 0.7$ s, $T_c = 5$ s, $\tau_n = 5$ s, $\tau_x = 0.5$ s.

**Advantage over frame-level**: the offline-trained model (with utterance batch normalization) can still be used, and previous context — fair to assume available in streaming scenarios — is exploited. With the far-field acoustic model, segment-level processing **nearly matches the offline system** (7-mic at 0.7 s delay: 11.29% vs. 11.26%; 8-mic: 11.42% vs. 11.39%), and the zero-delay variant also performs well (11.84–12.04%). Offline remains better with the near-field AM (utterance boundaries help when the AM is less noise-robust).

## Related Concepts

- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]] — recursive online SCM estimation with burn-in period
- [[concepts/tf-mask-estimation|TF Mask Estimation]] — the per-channel masks consolidated by a median operation
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — beamformer used (MVDR+BAN, fixed reference)
- [[concepts/logmel-mse-loss|LogMel MSE Loss]] — training criterion for the segment-level/offline models; BCE favored frame-level
- [[concepts/beamforming|Beamforming]] — parent topic

## Related Sources

- [[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker, Erdogan, Yoshioka & Haeb-Umbach 2018: Exploring Practical Aspects of Neural Mask-Based Beamforming for Far-Field Speech Recognition]] — develops both schemes and quantifies their degradation vs. offline
- [[sources/souden-2011-online-noise-tracking|Souden, Chen, Benesty & Affes 2011: An Integrated Solution for Online Multichannel Noise Tracking and Reduction]] — a complementary model-based route to online statistics-only beamforming via MC-SPP noise PSD tracking
