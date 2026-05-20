---
type: concept
created: 2026-05-20
updated: 2026-05-20
tags:
  - speech-separation
  - close-talk
  - far-field
  - self-supervised-learning
  - conversational-speech
---

# Cross-Talk Reduction

**Cross-talk reduction (CTR)** aims to isolate each speaker's own close-talk speech from their close-talk microphone mixture in multi-speaker conversational settings. Close-talk microphones (e.g., lapel mics) capture the wearer's speech at high energy but also pick up cross-talk from other speakers and ambient noise. CTR removes these interferences to recover clean close-talk speech, which can then serve as pseudo-labels for downstream tasks like far-field speech separation.

## Motivation

In conversational speech separation datasets, each speaker typically wears a close-talk microphone alongside far-field recording arrays. While close-talk mixtures have high SNR for the wearer, they contain significant cross-talk from other speakers — making them unsuitable as direct supervision signals. CTR bridges this gap.

## Formulation as Blind Deconvolution

Close-talk speech $Z(d)$ (mic $d$'s wearer) is treated as the dry source. Cross-talk from speaker $c$ at close-talk mic $d$ ($c \neq d$) is modeled as linear convolution:

$$X_d(c,t,f) \approx \mathbf{g}_d(c,f)^{\mathsf{H}} \widetilde{\mathbf{Z}}(c,t,f)$$

where $\widetilde{\mathbf{Z}}(c,t,f)$ stacks a time window of STFT coefficients and $\mathbf{g}_d(c,f)$ is a relative transfer function (RTF). The same $Z(c)$, when filtered through $\mathbf{g}_p(c,f)$, reconstructs far-field observations.

The blind deconvolution problem jointly estimates both the linear filters and the close-talk speech signals from observed close-talk and far-field mixtures.

## CTRnet

**CTRnet** is a DNN-based approach trained via:
- **Unsupervised**: Mixture-constraint (MC) loss — checks if estimated close-talk signals, when linearly filtered, reconstruct the observed mixtures. Uses Forward Convolutive Prediction (FCP) for filter estimation.
- **Weakly-supervised**: Adds speaker-activity timestamps via frame muting + speaker-activity (SA) loss to penalize non-speech output
- **Semi-supervised**: Combines supervised loss on simulated data with weakly-supervised loss on real data

Optional extensions include noise modeling (predict additional noise outputs) and reverberation modeling (predict with delay $\Delta$).

## PuLSS Framework

**Pseudo-label based far-field speech separation (PuLSS)** uses CTRnet-estimated close-talk speech as pseudo-labels for training supervised far-field separation models. A cross-talk error (CTE) loss ensures separated outputs don't leak cross-talk. This is the first neural method to substantially outperform guided source separation (GSS) on real conversational data (CHiME-6).

## Related Concepts

- [[concepts/beamforming|Beamforming]]
- [[concepts/self-supervised-speech-representation|Self-Supervised Speech Representation]]
- Guided Source Separation (GSS)

## Related Sources

- [[sources/wang-2026-cross-talk-speech-reduction-separation|Wang & Cornell 2026: Cross-Talk Speech Reduction, by Separation, for Separation]]
