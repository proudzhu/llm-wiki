---
type: concept
created: 2026-10-11
updated: 2026-10-11
sources:
  - raw/papers/boeddeker-2018-neural-mask-beamforming/full-text.md
tags:
  - deep-learning
  - speech-enhancement
  - asr
  - training-criterion
---

# LogMel MSE Loss

The **LogMel MSE loss** is a *feature-level* training criterion for neural mask-based beamforming, introduced by [[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker, Erdogan, Yoshioka & Haeb-Umbach 2018]]: the mean-squared error between the **normalized log-mel ASR features of the beamformed signal** and those of the clean reference. It shifts the mask network's optimization target from mask fidelity to the features the recognizer actually consumes, and is enabled by backpropagating **through the beamforming operation** using complex-valued algorithmic differentiation (Boeddeker et al. 2017).

## Formulation

$$
L(\theta) = \sum_{k} \sum_{t} \sum_{d} \left( \hat{\mathbf{F}}_{d,t}(\theta) - \mathbf{F}^{*}_{d,t,k} \right)^{2}
$$

where:

- $\hat{\mathbf{F}}_{d,t}(\theta)$ — normalized log mel-filterbank feature ($D = 80$ mel filters) computed **from the beamformed output** $\hat{\mathbf{X}}_{f,t} = \mathbf{w}_f^{\mathrm{H}} \mathbf{Y}_{f,t}$, hence a function of the mask-network parameters $\theta$ through the beamformer;
- $\mathbf{F}^{*}_{d,t,k}$ — the same feature computed from the clean reference signal.

The mel features use frame size 1024 samples and frame shift 256 samples (513 frequency bins), matching the STFT of the beamforming front-end.

## Why It Beats Mask-Level Training

The conventional criterion trains the mask network with **binary cross-entropy (BCE)** against ideal binary masks for speech and noise (Heymann et al. 2015). BCE optimizes mask *accuracy*, but the mask is only an intermediate quantity — what matters downstream is the beamformed signal's ASR features. LogMel MSE closes this criterion gap: in [[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker et al. 2018]] it improves WER by **~8% relative** over BCE (7-mic array, offline: 19.19%→17.69% near-field AM, 11.26%→10.42% far-field AM).

This is an instance of the end-to-end-optimization argument of [[concepts/hybrid-speech-enhancement|hybrid speech enhancement]]: a cascaded hybrid's DNN is optimized toward a criterion different from the model-based part, and training the chain (mask DNN → SCM computation → differentiable beamforming → feature extraction) toward a downstream criterion removes that deficit — here without abandoning the modular beamforming structure. Gradients must flow through complex-valued matrix operations (SCM accumulation, eigendecomposition/inversion), for which the complex-valued algorithmic differentiation rules of Boeddeker et al. (2017) supply the backward pass.

One caveat from the same paper: the **frame-level online** configuration favored the BCE-trained model (utterance-level statistics, which the LogMel model's training relies on, are unavailable online), while the offline and segment-level configurations used LogMel MSE.

## Related Concepts

- [[concepts/tf-mask-estimation|TF Mask Estimation]] — the mask network being trained; BCE is the conventional mask-level criterion
- [[concepts/neural-beamforming|Neural Beamforming]] — differentiable beamforming operation the gradient flows through
- [[concepts/hybrid-speech-enhancement|Hybrid Speech Enhancement]] — end-to-end optimization of Class-1 hybrids
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — the beamformer used with this loss in most experiments
- [[concepts/online-mask-based-beamforming|Online Mask-Based Beamforming]] — configuration where BCE-trained masks performed better

## Related Sources

- [[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker, Erdogan, Yoshioka & Haeb-Umbach 2018: Exploring Practical Aspects of Neural Mask-Based Beamforming for Far-Field Speech Recognition]] — introduces the criterion and reports the ~8% relative WER gain over BCE
