---
type: concept
created: 2026-09-26
updated: 2026-09-26
sources:
  - raw/papers/haeb-umbach-2024-microphone-array-deep-learning/full-text.md
tags:
  - source-separation
  - speech-enhancement
  - diarization
  - em-algorithm
  - multi-channel
---

# Guided Source Separation (GSS)

**Guided Source Separation (GSS)** is a hybrid (Class 2) multichannel source separation method in which a **diarization front-end** (data-driven) constrains a model-based EM mask estimator, producing time-frequency masks that drive beamformers. It was introduced for the CHiME-5 dinner-party scenario (Boeddeker et al. 2018) and became the standard front-end of most — including top-performing — CHiME-6 and CHiME-7 challenge systems ([[sources/haeb-umbach-2024-microphone-array-deep-learning|Haeb-Umbach et al. 2024]]).

## Mechanism

GSS estimates TF masks in a two-step procedure:

1. **Diarization stage (data-driven)**: a DNN estimates per-speaker activity $m_{k,t}$ at *time* resolution. Simple variants detect speech overlap and exclude those segments; stronger variants such as [[concepts/target-speaker-vad|TS-VAD]] identify each speaker active in overlapped speech.
2. **EM refinement stage (model-based)**: a [[concepts/tf-mask-estimation|spatial mixture model]] fit with EM refines the activities to TF resolution, *guided* by the diarization output — the posterior is constrained to be non-zero only where the target speaker is active:

$$
m_{k,t,f} = \frac{m_{k,t}\,\mathbb{E}[z_{k,t,f}\mid \mathbf{y}_{t,f}]}{\sum_{\tilde{k}=1}^{K} m_{\tilde{k},t}\,\mathbb{E}[z_{\tilde{k},t,f}\mid \mathbf{y}_{t,f}]}
$$

The refined masks yield per-source speech and noise [[concepts/spatial-covariance-matrix|SCMs]], from which [[concepts/mvdr-beamformer|MVDR]]-class beamformers extract each speaker.

## Why It Is Robust

GSS exemplifies the "best of both worlds" of hybrid parameter estimation: the DNN contributes spectro-temporal discrimination and overlap-aware diarization that per-frequency spatial clustering cannot do, while the EM stage contributes unsupervised adaptation to the *test utterance's* spatial statistics — so the system retains adaptability that purely trained systems lack. This combination is credited for its robustness under the highly challenging recording conditions of the CHiME dinner-party challenges, and for why Haeb-Umbach et al. single it out as the model-as-regularizer success story.

## Related Concepts

- [[concepts/tf-mask-estimation|TF Mask Estimation]]
- [[concepts/target-speaker-vad|Target-Speaker Voice Activity Detection (TS-VAD)]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/hybrid-speech-enhancement|Hybrid Speech Enhancement]]
- [[concepts/blind-source-separation|Blind Source Separation]]

## Related Sources

- [[sources/haeb-umbach-2024-microphone-array-deep-learning|Haeb-Umbach et al. 2024: Microphone Array Signal Processing and Deep Learning for Speech Enhancement]] — Section IV-B formulation and CHiME-6/7 evidence
