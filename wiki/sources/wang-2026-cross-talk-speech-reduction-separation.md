---
type: source
created: 2026-05-20
updated: 2026-05-20
sources:
  - raw/papers/wang-2026-cross-talk-speech-reduction-separation/full-text.md
  - https://arxiv.org/abs/2605.19695v1
  - zotero://select/items/0_MNP3G55C
tags:
  - speech-separation
  - cross-talk-reduction
  - pseudo-labeling
  - chime-6
  - conversational-speech
  - self-supervised-learning
aliases:
  - Wang & Cornell 2026: CTRnet and PuLSS for Cross-Talk Reduction
---

# Wang & Cornell 2026: Cross-Talk Speech Reduction, by Separation, for Separation

**Authors**: Zhong-Qiu Wang, Samuele Cornell
**Institutions**: Southern University of Science and Technology (Wang); Carnegie Mellon University (Cornell)
**Published**: arXiv preprint, May 2026. Extended version of IJCAI 2026 conference paper.
**arXiv**: [2605.19695](https://arxiv.org/abs/2605.19695v1)
**📎 Zotero**: [zotero://select/items/0_MNP3G55C](zotero://select/items/0_MNP3G55C)

## Summary

Proposes a framework for **cross-talk reduction (CTR)** on close-talk microphone recordings in conversational scenarios, and **pseudo-label based far-field speech separation (PuLSS)**. CTRnet is trained directly on real-recorded pairs of close-talk and far-field mixtures via **unsupervised/weakly-supervised learning** using a mixture-constraint (MC) loss based on blind deconvolution. The estimated clean close-talk speech serves as pseudo-labels for training supervised far-field separation models. On CHiME-6, achieves state-of-the-art ASR (22.1% cpWER with oracle diarization), surpassing all CHiME-{7,8} challenge submissions and being the first neural method to substantially outperform guided source separation (GSS) on real conversational data.

## Problem Formulation

### Signal Model

For $C$ speakers each wearing a close-talk mic, and $P$ far-field mics:

Close-talk mixture: $$Y_d(t,f) = \sum_{c=1}^C X_d(c,t,f) + V_d(t,f)$$

Far-field mixture: $$Y_p(t,f) = \sum_{c=1}^C X_p(c,t,f) + V_p(t,f)$$

where $X_d(c)$ is speaker $c$'s reverberant speech at close-talk mic $d$, and $X_{d(=c)}(c)$ is the **close-talk speech** (wearer's own speech).

### CTR as Blind Deconvolution

Close-talk speech $Z(d)$ of mic $d$ is modeled as the dry source. Cross-talk speech of speaker $c$ at mic $d$ ($c \neq d$) is approximated as linear convolution:

$$X_d(c,t,f) \approx \mathbf{g}_d(c,f)^{\mathsf{H}} \widetilde{\mathbf{Z}}(c,t,f)$$

where $\widetilde{\mathbf{Z}}(c,t,f)$ stacks $I+1+J$ STFT frames, and $\mathbf{g}_d(c,f)$ is an RTF filter. The same close-talk speech $Z(c)$, when filtered through $\mathbf{g}_p(c,f)$, reconstructs the far-field observation.

## Methodology

### CTRnet (Cross-Talk Reduction Network)

- **Architecture**: DNN taking all $C$ close-talk mixtures as input, outputting estimates $\hat{Z}(c)$ for each speaker
- **Training**: Unsupervised via **mixture-constraint (MC) loss** — checks if estimates satisfy the physical models by:
  1. Linearly filtering $\hat{Z}(c)$ via **Forward Convolutive Prediction (FCP)** to reconstruct cross-talk and far-field contributions
  2. Computing reconstruction loss between reconstructed and observed mixtures
  3. Loss function: absolute loss on real, imaginary, and magnitude components with compression factor $\alpha$
- **Weakly-supervised**: Adds speaker-activity timestamps via **frame muting** (mask DNN outputs in silent regions) + **speaker-activity (SA) loss** to push silent outputs toward zero
- **Semi-supervised**: Combines supervised loss (on simulated data) with weakly-supervised loss (on real data)
- **Noise modeling**: DNN additionally predicts noise at each close-talk mic
- **Reverberation modeling**: Predicts close-talk speech with a delay $\Delta$ to focus on early arrivals

### PuLSS (Pseudo-Label based Far-Field Speech Separation)

- Uses CTRnet-estimated close-talk speech as **pseudo-labels** for training far-field separation models
- **Cross-talk error (CTE) loss**: Ensures separated outputs don't contain cross-talk from other speakers by checking reconstruction of other speakers' close-talk mixtures
- **Adaptive feature-weight normalization (AFWN)**: Balances losses across high-energy and low-energy T-F units
- At inference: PuLSS model separates far-field mixtures $\rightarrow$ ASR transcribes

### Evaluation Results

**CTRnet on close-talk mixtures** (cpWER on CHiME-6 test set):

| System | cpWER |
|--------|-------|
| Unprocessed mixture | 29.4% |
| Semi-supervised CTRnet (best) | **21.8%** |
| Supervised CTRnet (simulated only) | 37.9% |
| GSS (8-ch) on close-talk | 28.2% |

**PuLSS on far-field mixtures** (cpWER with oracle diarization):

| System | cpWER |
|--------|-------|
| Mixture | 62.6% |
| GSS (24-ch) | 38.5% |
| Supervised (simulated only) | 49.0% |
| PuLSS | **22.1%** |

PuLSS achieves **state-of-the-art** on CHiME-6 under both oracle and estimated speaker diarization, outperforming all CHiME-{7,8} challenge submissions including GSS-based systems.

## Key Contributions

1. **CTR task definition**: Formulates cross-talk reduction on close-talk mixtures as a blind deconvolution problem
2. **CTRnet**: Unsupervised/weakly-supervised training via mixture-constraint loss on real-recorded pairs, avoiding domain mismatch
3. **PuLSS framework**: First neural separation method to substantially outperform GSS on real conversational data
4. **Practical components**: FCP-based filter estimation, frame muting, noise/reverberation modeling, cross-talk error loss, adaptive feature-weight normalization
5. **State-of-the-art results**: 22.1% cpWER on CHiME-6 far-field test set with oracle diarization

## Related Concepts

- [[concepts/cross-talk-reduction|Cross-Talk Reduction]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/self-supervised-speech-representation|Self-Supervised Speech Representation]]

## Related Entities

- [[entities/zhong-qiu-wang|Zhong-Qiu Wang]]
- [[entities/samuele-cornell|Samuele Cornell]]
