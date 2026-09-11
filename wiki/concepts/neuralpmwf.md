---
type: concept
created: 2026-09-11
updated: 2026-09-11
sources:
  - raw/papers/grinstein-2025-tiny-param-mwf/full-text.md
tags:
  - speech-enhancement
  - multi-channel
  - wiener-filter
  - hybrid-dsp-dnn
  - lightweight-model
---

# NeuralPMWF

**NeuralPMWF** (Grinstein et al. 2025) is a hybrid multi-channel speech enhancement system in which a tiny neural network (164.9k parameters, 24.95 MMACs/s, 16 ms algorithmic latency) *fully controls* the [[concepts/parametric-multi-channel-wiener-filter|parameterized multi-channel Wiener filter (PMWF)]] — every quantity the classical filter needs (speech/noise covariances, smoothing speeds, and the distortion trade-off $\beta$) is produced or scheduled by the network and trained end-to-end through the differentiable filter.

## System Structure

The pipeline has one network (MaskDNN) plus classical DSP:

1. **Mask estimation** — MaskDNN maps the real/imag parts of the $M$-channel STFT to a multi-channel complex-valued T-F mask $\mathbf{G}$ (spatial block: per-frequency convolutions mimicking Filter-And-Sum; temporal block: causal [[concepts/splitgru|SplitGRU]] layers).
2. **Covariance estimation** — $\hat{\mathbf{S}}_0 = \mathbf{G}\odot\mathbf{Y}$ and $\hat{\mathbf{N}}_0 = \mathbf{Y}-\hat{\mathbf{S}}_0$ feed exponentially smoothed [[concepts/spatial-covariance-matrix|covariance matrices]] with learned frequency-dependent speeds $\alpha_{ss}[w], \alpha_{nn}[w] = \text{sigmoid}(\alpha^{(0)}[w])$ (trained, then fixed at inference).
3. **Filter computation** — the PMWF $\mathbf{h}[t,w]=\boldsymbol{\gamma}[t,w][:,0]/(\beta[t,w]+\text{trace}\,\boldsymbol{\gamma}[t,w])$ with $\boldsymbol{\gamma}=\mathbf{\Phi}_{nn}^{-1}\mathbf{\Phi}_{ss}$.
4. **Dynamic distortion control** — an SPP proxy $\hat{p}[t,w]=\text{sigmoid}(\mathbf{p}^{(a)}[w]|\mathbf{G}[t,w,0]|+\mathbf{p}^{(b)}[w])$ schedules the trade-off parameter $\beta[t,w]=\beta^{(0)}[w](1-\hat{p}[t,w])$: near-distortionless filtering when speech is present, aggressive suppression ($\beta>30$ learned) when speech is certainly absent.

The per-frequency gain vectors $\mathbf{p}^{(a)},\mathbf{p}^{(b)},\boldsymbol{\alpha}^{(0)}_{ss},\boldsymbol{\alpha}^{(0)}_{nn},\boldsymbol{\beta}^{(0)}\in\mathbb{R}^{F}$ are learned jointly with the mask network (as element-wise gains, not fully-connected layers — the latter were found more expensive and less stable).

## Key Findings

- On a simulated 5-microphone Rayban-Meta-style smart-glasses scenario (DNS Challenge 2020 material, image-method rooms), NeuralPMWF beats comparably-sized hybrid baselines (TinyGRU+MWF, GTCRN+MWF, MCCRN+MWF) on STOI, SI-SDR, SNR, and NB-PESQ: 74.3 / 5.5 dB / 6.91 dB / 2.12.
- Ablations show the **SPP-driven dynamic $\beta$ is the dominant contribution** (+4.5 STOI over any fixed or frequency-dependent-only $\beta$); MVDR ($\beta=0$) and MWF ($\beta=1$) perform nearly identically, and aggressive fixed $\beta=10$ is worst.
- Smoothing ablation: cumulative-mean covariances are worst; exponential smoothing variants are similar, with trained frequency-dependent $\alpha$ marginally best. The learned $\alpha_{ss}>\alpha_{nn}$, reproducing the classical assumption that speech statistics change faster than noise — a built-in explainability property.
- Prior dynamic PMWF control required specialized parameter tuning (Braun et al. 2015; Bagheri & Giacobello 2019; Ngo et al. 2009); NeuralPMWF replaces the hand-tuned schedule with a learned one, making dynamic control practical.

## Positioning

NeuralPMWF sits at the intersection of three wiki threads: (i) the [[concepts/parametric-multi-channel-wiener-filter|PMWF]] control lineage, where the SPP-driven $\beta$ generalizes [[concepts/multi-channel-speech-presence-probability|MC-SPP]]-based trade-off control from hand-crafted schedules to end-to-end learning; (ii) [[concepts/neural-beamforming|neural beamforming]], as a differentiable classical filter whose statistics are network-estimated; and (iii) the low-compute SE frontier alongside [[concepts/gtcrn|GTCRN]] and [[concepts/munet|μNet]]. Its inference-time $\beta$ schedule is the PMWF-family analogue of [[concepts/noise-attenuation-control|Noise Attenuation Control]] — but learned and SPP-driven rather than a user-facing knob.

## Related Concepts

- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter (PMWF)]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/speech-presence-probability|Speech Presence Probability (SPP)]]
- [[concepts/multi-channel-speech-presence-probability|Multi-Channel Speech Presence Probability (MC-SPP)]]
- [[concepts/splitgru|SplitGRU]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/complex-ratio-mask|Complex Ratio Mask]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/neural-beamforming|Neural Beamforming]]
- [[concepts/noise-attenuation-control|Noise Attenuation Control]]

## Related Sources

- [[sources/grinstein-2025-tiny-param-mwf|Grinstein et al. 2025: Controlling the PMWF Using a Tiny Neural Network]]
- [[sources/bagheri-2019-pmwf-spp|Bagheri & Giacobello 2019: Exploiting MC-SPP in Parametric Multi-Channel Wiener Filter]] — hand-tuned SPP-driven $\beta$ predecessor
- [[sources/braun-2015-residual-noise-control|Braun, Kowalczyk & Habets 2015: Residual Noise Control PMWF]] — parametric PMWF control via residual-noise target
