---
type: concept
created: 2026-10-23
updated: 2026-10-24
sources:
  - raw/papers/lee-2016-dnn-plc/full-text.md
  - raw/papers/nguyen-2023-predictive-plc/full-text.md
tags:
  - packet-loss-concealment
  - deep-neural-network
  - regression
  - speech-coding
  - audio-signal-processing
---

# DNN Regression PLC

**DNN regression PLC** conceals lost speech packets by training a feed-forward deep neural network to *regress* the acoustic features of a missing frame from the features of the preceding correctly received frames. Introduced by [[sources/lee-2016-dnn-plc|Lee & Chang 2016]] — the earliest application of DNN regression to [[concepts/packet-loss-concealment|packet loss concealment]] — it treats PLC as a frame-to-frame feature prediction problem rather than a generative synthesis problem.

## Key Formulations

Two separate DNNs are trained, one for the log-power spectra (LPS) and one for the phases in the DFT domain. For a 512-point DFT with a Hamming window on 20 ms frames, each frame yields 257-dim LPS $Y^l(k) = \log |Y^f(k)|^2$ and phase features; the input is the 11 previous frames' features and the output is the missing frame's features (11 chosen because the regression MSE saturates there).

Training follows the classic deep-learning recipe of the era: RBM-based layer-wise unsupervised pre-training (Gaussian-Bernoulli RBM on the real-valued input, stacked Bernoulli-Bernoulli RBMs, contrastive divergence), then supervised back-propagation fine-tuning with an MMSE objective. For the LPS network the error is made **asymmetric** to penalize overestimation, since overestimated spectral components are perceptually more annoying than underestimated ones:

$$\widetilde{e}_{\mathrm{lps}} = \begin{cases} e_{\mathrm{lps}}, & e_{\mathrm{lps}} \leq 0 \\ \sqrt{2}\, e_{\mathrm{lps}}, & e_{\mathrm{lps}} > 0 \end{cases}$$

At concealment time the estimated spectrum is rebuilt as $\hat{X}^f(k) = e^{\hat{X}^l(k)/2} e^{j \angle \hat{X}^f(k)}$ and inverse-transformed; **cross-fading** (roll-off $\alpha = 3$) smooths the boundaries with adjacent good frames. For **burst losses**, the estimated features of a reconstructed frame are recursively re-fed as input for the next missing frame, so no muting-to-zero occurs.

## Design Rationale (Lee & Chang 2016)

- **DFT LPS + phase over codec parameters**: ISF/LSF contours are sensitive to regression error (small errors → non-smooth contours → severe distortion); MDCT coefficients have too high a dynamic range for DNN regression.
- **Two networks over one**: LPS is strongly correlated across frames while phase is not; a single network estimating both performs worse than the sum of two separate networks.
- **Depth matters**: 1-hidden-layer DNNs underperform even the AMR-WB Appendix I baseline; 4 hidden layers × 2048 nodes gives the best LSD/PESQ.
- **Phase must be regressed, not copied**: copying the previous frame's phase produces audible waveform repetition during the loss period.

## Position in PLC Evolution

DNN regression PLC predates the neural vocoder-based approaches ([[concepts/lpcnet|LPCNet]]-hybrid and WaveNetEQ-style generative PLC surveyed on the [[concepts/packet-loss-concealment|PLC concept page]]). Its frame-feature regression paradigm contrasts with the later generative + predictive decomposition: regression predicts deterministic acoustic features from a fixed causal context, which excels when the loss is short and the context is informative, but lacks a generative model's ability to synthesize plausible novel content during long bursts. Its **recursive re-feeding** for burst losses — feeding the estimated features of a reconstructed frame back as input for the next missing frame — anticipates the dedicated predictor branch of [[concepts/full-band-recurrent-network|FRN]] ([[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023]]), which promotes the idea into a separately pre-trained network predicting the current frame from the previous *enhanced output*. The approach also has **no algorithmic delay** and was shown to serve as an effective front-end for network speech recognition (WER 87.8% → 61.6% at 30% loss vs. AMR-WB App. I).

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — the umbrella task
- [[concepts/pesq|PESQ]] — objective quality metric used to evaluate the method
- [[concepts/lpcnet|LPCNet]] — later autoregressive vocoder used by generative PLC approaches
- [[concepts/full-band-recurrent-network|Full-Band Recurrent Network (FRN)]] — blind full-band descendant whose predictor branch formalizes recursive re-feeding

## Related Sources

- [[sources/lee-2016-dnn-plc|Lee & Chang 2016: DNN-Based Packet Loss Concealment]] — introduces the method
- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time PLC]] — later hybrid generative + predictive neural PLC for comparison
- [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023: Full-Band Blind PLC]] — blind 48 kHz PLC that turns recursive re-feeding into a pre-trained predictor branch
