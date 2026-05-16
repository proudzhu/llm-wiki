---
type: concept
created: 2026-05-02
updated: 2026-05-15
sources:
  - raw/papers/zhang-2024-neural-kalman-howling/full-text.txt
  - raw/papers/zhang-2023-hybrid-ahs/full-text.txt
tags:
  - kalman-filter
  - frequency-domain
  - adaptive-filtering
  - signal-processing
---

# Frequency-Domain Kalman Filter

The **Frequency-Domain Kalman Filter (FDKF)** is a variant of the Kalman filter that operates in the frequency domain, estimating the acoustic path using an adaptive filter $W(k)$ with per-frequency-bin state updates.

## Core Algorithm

FDKF operates in a two-step predictor-corrector cycle:

### Prediction Step

$$\hat{S}(k) = Y(k) - X(k)\hat{W}(k)$$

Estimates the near-end signal by subtracting the predicted echo from the microphone signal.

### Update Step

$$\hat{W}(k+1) = A[\hat{W}(k) + K(k)\hat{S}(k)]$$

Updates the acoustic path estimate using the Kalman gain $K(k)$:

$$K(k) = P(k)X^H(k)[X(k)P(k)X^H(k) + \Psi_{vv}(k)]^{-1}$$

$$P(k+1) = A^2[I - \alpha K(k)X(k)]P(k) + \Psi_{\Delta\Delta}(k)$$

where:
- $A$ is the transition factor
- $\alpha$ is a leakage factor
- $\Psi_{vv}(k)$ is the observation noise covariance (approximated by $\Psi_{\hat{s}\hat{s}}(k)$)
- $\Psi_{\Delta\Delta}(k)$ is the process noise covariance (approximated by $\Psi_{\hat{W}\hat{W}}(k)$)
- $P(k)$ is the state estimation error covariance

## Applications

- **Acoustic Echo Cancellation (AEC)**: Estimating and subtracting echo path
- **Acoustic Howling Suppression (AHS)**: Breaking the positive feedback loop
- **Secondary Path Modeling**: Online identification of the secondary transfer function in ANC

## Hybrid and NN-Augmented Variants

Recent work extends FDKF in two complementary directions:
- **Hybrid AHS**: cascades FDKF with a self-attentive recurrent neural network, using Kalman-preprocessed signals as auxiliary neural inputs and feeding the DNN output back as the Kalman reference during streaming inference
- **Reference signal refinement**: LSTM-based ratio mask to improve reference quality
- **Covariance matrix estimation**: replacing static approximations with learned dynamic estimates
- **Nonlinear transition modeling**: capturing hardware nonlinearities and residual leakage

Key insight: FDKF remains a strong adaptive backbone, while neural components are most useful when they compensate for nonlinear distortion, reference mismatch, or poorly modeled covariance terms.

## Related Concepts

- [[../concepts/kalman-filter|Kalman Filter]] — time-domain general framework
- [[../concepts/acoustic-howling-suppression|Acoustic Howling Suppression]] — primary application
- [[../concepts/adaptive-filtering|Adaptive Filtering]] — broader adaptive filtering context
- [[../concepts/frequency-domain-anc|Frequency-Domain ANC]] — frequency-domain processing in ANC
- [[../concepts/self-attentive-recurrent-neural-network|Self-Attentive Recurrent Neural Network]] — Hybrid AHS neural module

## Related Sources

- [[../sources/zhang-2023-hybrid-ahs|Zhang 2023: Hybrid AHS]]
- [[../sources/zhang-2024-neural-kalman-howling|Zhang 2024: Neural Network Augmented Kalman Filter for AHS]]
