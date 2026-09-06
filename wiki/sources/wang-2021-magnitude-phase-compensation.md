---
type: source
created: 2026-09-06
updated: 2026-09-06
sources:
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
  - https://doi.org/10.1109/LSP.2021.3116502
  - zotero://select/items/0_7734ZCDJ
tags:
  - speech-separation
  - speech-enhancement
  - deep-learning
  - loss-function
  - phase-estimation
  - evaluation-metrics
---

# Wang, Wichern & Le Roux 2021: On the Compensation Between Magnitude and Phase in Speech Separation

**Authors**: [[entities/zhong-qiu-wang|Zhong-Qiu Wang]], [[entities/gordon-wichern|Gordon Wichern]], [[entities/jonathan-le-roux|Jonathan Le Roux]]
**Affiliation**: Mitsubishi Electric Research Laboratories (MERL), Cambridge, MA
**Venue**: IEEE Signal Processing Letters, vol. 28, 2021
**Type**: Journal article (analysis)
**DOI**: [10.1109/LSP.2021.3116502](https://doi.org/10.1109/LSP.2021.3116502)
**arXiv**: [2108.05470](https://arxiv.org/abs/2108.05470)
**Zotero**: [7734ZCDJ](zotero://select/items/0_7734ZCDJ)

## Summary

Many end-to-end speech separation systems define their training loss solely in the time domain (SI-SDR, waveform $L_1$) or complex domain (real-imaginary distance). This paper explains a widely observed but poorly understood phenomenon — adding a magnitude-domain loss improves PESQ, eSTOI, and ASR word error rates while slightly degrading SI-SDR — through the lens of an **implicit magnitude-phase compensation**: when phase cannot be accurately estimated, a complex- or time-domain loss is minimized by a magnitude that *compensates* for the phase error (the projection of the clean spectrum onto the estimated-phase direction), sacrificing magnitude accuracy. The authors validate this view on noisy-reverberant speech enhancement (WHAMR!), speaker separation (SMS-WSJ), and robust ASR, using two decomposition metrics — magnitude SNR (mSNR) and phase SNR (pSNR) — to isolate magnitude vs. phase estimation quality.

## Problem Formulation

The monaural mixture model in the time domain is $y[n]=s[n]+v[n]$, and in the STFT domain:

$$Y(t,f)=S(t,f)+V(t,f).$$

Two families of end-to-end approaches are analyzed:

1. **Complex-domain separation** ([[concepts/complex-spectral-mapping|complex spectral mapping]]): predict target real-imaginary (RI) components from mixture RI components, e.g. with the loss
$$\mathcal{L}_{\text{RI}}=\|\hat{R}-\text{Real}(S)\|_{1}+\|\hat{I}-\text{Imag}(S)\|_{1}.$$
2. **Time-domain separation**: predict the target waveform directly, e.g. $\mathcal{L}_{\text{Wav}}=\|\hat{s}-s\|_{1}$.

**The phenomenon to explain**: adding a magnitude loss to either family (e.g. $\mathcal{L}_{\text{RI+Mag}}=\mathcal{L}_{\text{RI}}+\||\hat{R}+j\hat{I}|-|S|\|_{1}$) is repeatedly reported to yield clear gains in PESQ, eSTOI, and WER, at the cost of slightly worse SI-SDR. Prior studies observed this empirically but did not accurately explain its fundamental cause.

## Methodology

### The Compensation Problem

At each T-F unit, a complex- or time-domain loss drives the estimate $\hat{S}(t,f)$ toward the clean $S(t,f)$. Because phase is difficult to estimate, $\angle\hat{S}(t,f)$ typically differs from $\angle S(t,f)$ (especially at low SNR). The closest approximation of $S(t,f)$ *along the direction of* $\angle\hat{S}(t,f)$ is the **projection** $|S(t,f)|\cos(\angle S-\angle\hat{S})$ — an estimate that is **incapable of recovering the clean magnitude**. The magnitude error grows as the phase error grows, and if the phase error exceeds $\pi/2$, the optimal projection magnitude is **zero** (the paper's Fig. 1 complex-plane illustration; a vector graphic not extractable from the arXiv HTML).

Consequences per metric:

- **PESQ** first time-aligns the signal with the reference segment-wise, then compares short-time Bark-scale power spectra — it favors an *accurate magnitude*, tolerating phase/time misalignment.
- **eSTOI/STOI** only look at the magnitude envelope.
- **SI-SDR** measures sample-level time-domain error — it *favors a compensated magnitude* that compensates for the inaccurate phase.

This explains both sides of the observed phenomenon: a magnitude loss balances complex- and magnitude-domain approximation (better PESQ/eSTOI/WER), while pushing $\hat{S}$ away from the projection along $\angle\hat{S}$ degrades SI-SDR.

The view is motivated by the [[concepts/phase-sensitive-mask|phase-sensitive mask (PSM)]] $|S|/|Y|\cos(\angle S-\angle Y)$ (Erdogan et al. 2015), which *explicitly* computes the compensated magnitude for re-synthesis with mixture phase. The paper's key claim is that this compensation **implicitly exists in many end-to-end approaches** that improve upon mixture phase but still cannot reconstruct clean phase — an analysis absent from Erdogan et al. and prior work.

### Magnitude Spectrogram Approximation (MSA)

When only a good magnitude is needed (e.g. robust ASR on magnitude features), it may be better *not* to model magnitude and phase simultaneously. Direct magnitude spectrogram approximation uses

$$\mathcal{L}_{\text{MSA}}=\|\hat{M}-|S|\|_{1},$$

which the paper reinterprets as **teacher forcing** (assuming the estimated speech has the target phase):

$$\mathcal{L}_{\text{MSA}}=\|\hat{M}e^{j\angle S}-|S|e^{j\angle S}\|_{1}.$$

The best approximation of $S(t,f)$ along $\angle S(t,f)$ is exactly $|S(t,f)|$, so the implicit compensation is avoided — and MSA achieves the best mSNR among learned models. Drawback: with signal re-synthesis (mixture phase + [[concepts/stft-consistency|phase inconsistency]]), the re-synthesized magnitude degrades, explaining why extracting ASR features directly from estimated magnitudes outperforms re-synthesis.

Two magnitude-only variants of end-to-end models: set the time-domain loss weight to zero — $\mathcal{L}_{\text{(RI-iSTFT)}\times 0+\text{Mag}}$ (loss on $|\text{STFT}(\text{iSTFT}(\hat{S}))|$) and $\mathcal{L}_{\text{Wav}\times 0+\text{Mag}}$ (loss on $|\text{STFT}(\hat{s})|$) — which train the model to output a time-domain signal with good magnitude.

### Phase Spectrogram Approximation

Conversely, when only phase estimates are needed, supply oracle magnitudes and define a phase-only loss:

$$\mathcal{L}_{\text{Phase}}=\|\text{Real}(|S|e^{j\angle(\hat{R}+j\hat{I})})-\text{Real}(S)\|_{1}+\|\text{Imag}(|S|e^{j\angle(\hat{R}+j\hat{I})})-\text{Imag}(S)\|_{1}.$$

### Model Structure, Inputs, and Outputs

The paper is an analysis paper re-using established architectures rather than proposing a new one:

```mermaid
flowchart TB
    subgraph A["Complex-domain separation (DenseUNet-TCN)"]
        A1["Mixture RI components<br/>Real(Y), Imag(Y)"] --> A2["DenseUNet-TCN"]
        A2 --> A3["Predicted RI components R-hat, I-hat"]
        A3 --> A4["iSTFT re-synthesis"]
        A4 --> A5["Estimated waveform s-hat"]
    end
    subgraph B["Magnitude-domain estimation (MSA / PSA)"]
        B1["Mixture magnitude |Y|"] --> B2["DenseUNet-TCN"]
        B2 --> B3["Estimated magnitude M-hat"]
        B3 --> B4["Optional re-synthesis<br/>with mixture phase"]
    end
    subgraph C["Time-domain separation (Conv-TasNet)"]
        C1["Mixture waveform y"] --> C2["Conv-TasNet"]
        C2 --> C3["Estimated waveform s-hat"]
    end
```

| Network | Structure | Input | Output | Training data | Role |
|---------|-----------|-------|--------|----------------|------|
| DenseUNet-TCN (CSM) | DenseUNet + TCN (Wang & Wang 2020) | Mixture RI components; 32/8 ms (WHAMR!) or 25/10 ms (SMS-WSJ) WL/HL STFT | Target RI components (2-channel), same frame rate | WHAMR! (16 kHz) / SMS-WSJ (8 kHz), target = direct sound | Complex spectral mapping; jointly models magnitude and phase |
| DenseUNet-TCN (MSA/PSA) | Same as above | Mixture magnitude $\|Y\|$ | Estimated magnitude $\hat{M}$ | Same as above | Magnitude-domain baselines (MSA, PSA) |
| Conv-TasNet | Temporal convolutional network (Luo & Mesgarani 2019) | Mixture waveform, 5/2.5 ms window/hop | Target waveform (one per speaker via PIT) | Same as above | Time-domain separation baseline |

For speaker separation, losses are combined with [[concepts/permutation-invariant-training|permutation invariant training]]. The ASR backend is a Kaldi-based recognizer trained on single-speaker noisy-reverberant speech (25/10 ms WL/HL feature extraction).

### Training Losses

All losses are $L_1$ norms. The configurations compared (equation numbers follow the paper):

| Loss | Equation | Domain |
|------|----------|--------|
| RI | (2) | Complex (RI components) |
| RI+Mag | (3) | Complex + magnitude |
| RI-iSTFT | (4) | Time (through iSTFT) |
| RI-iSTFT+Mag | (5) | Time + magnitude after iSTFT |
| Mag+RI-iSTFT | (6) | Magnitude before iSTFT + time |
| Wav | (7) | Time |
| Wav+Mag | (8) | Time + magnitude |
| MSA | (9)/(10) | Magnitude (teacher-forced target phase) |
| (RI-iSTFT)×0+Mag | (11) | Magnitude only (zero time loss) |
| Wav×0+Mag | (12) | Magnitude only (zero time loss) |
| Phase | (13) | Phase only (oracle magnitude) |
| PSA | (14) | Magnitude, PSM-style truncated-cosine target |

## Experimental Setup

| Item | WHAMR! enhancement | SMS-WSJ separation + ASR |
|------|--------------------|--------------------------|
| Corpus | WHAMR! (min, 16 kHz), 2-speaker noisy-reverberant mixtures with the second speaker removed; first channel | SMS-WSJ (8 kHz), simulated reverberant 2-speaker mixtures; first channel |
| Task | Joint dereverberation + denoising | Joint dereverberation + denoising + separation; ASR with Kaldi backend |
| Target | Direct sound | Direct sound |
| STFT (CSM/MSA/PSA) | 32/8 ms WL/HL | 25/10 ms WL/HL (aligned with ASR backend) |
| Time-domain model | Conv-TasNet, 5/2.5 ms WL/HL | Conv-TasNet, 5/2.5 ms WL/HL |
| Separation criterion | — | [[concepts/permutation-invariant-training|PIT]] |

**Metrics**: SI-SDR, [[concepts/pesq|PESQ]], eSTOI, WER, plus the decomposition metrics [[concepts/magnitude-phase-snr|mSNR and pSNR]]:

$$\text{mSNR}=10\,\text{log}_{10}\frac{\sum_{t,f}|S(t,f)|^{2}}{\sum_{t,f}\big||S(t,f)|-|\hat{S}(t,f)|\big|^{2}},\qquad
\text{pSNR}=10\,\text{log}_{10}\frac{\sum_{t,f}|S(t,f)|^{2}}{\sum_{t,f}\big|S(t,f)-|S(t,f)|e^{j\angle\hat{S}(t,f)}\big|^{2}}$$

(pSNR computed with oracle magnitude supplied).

## Results

### WHAMR! enhancement (Table I, selected rows)

| Approach | Eq. | Re-syn? | SI-SDR (dB) | PESQ | eSTOI (%) | mSNR (dB) | pSNR (dB) |
|----------|-----|---------|-------------|------|-----------|-----------|-----------|
| Unprocessed | – | – | −2.7 | 1.53 | 45.1 | −1.63 | −2.8 |
| MSA | (9) | yes | 4.4 | 2.72 | 78.5 | 11.34 | 6.29 |
| MSA | (9) | no | – | – | – | **13.05** | – |
| RI | (2) | yes | 9.1 | 2.49 | 80.3 | 12.66 | 10.8 |
| RI+Mag | (3) | yes | 8.6 | **2.92** | 81.9 | 12.84 | 10.35 |
| RI-iSTFT | (4) | yes | 8.80 | 2.46 | 79.0 | 12.08 | 10.79 |
| RI-iSTFT+Mag | (5) | yes | 8.56 | 2.86 | 81.7 | 12.64 | 10.46 |
| (RI-iSTFT)×0+Mag | (11) | yes | 7.3 | 2.91 | **82.7** | 12.9 | 9.1 |
| Phase | (13) | no | – | – | – | – | **12.4** |
| Wav | (7) | yes | 7.7 | 2.20 | 78.0 | 11.22 | 10.14 |
| Wav+Mag | (8) | yes | 7.5 | 2.58 | 80.1 | 11.43 | 9.90 |
| Wav×0+Mag | (12) | yes | −9.09 | 2.67 | 80.6 | 11.36 | −3.64 |
| PSA | (14) | yes | 5.6 | 2.36 | 76.3 | 10.2 | 7.2 |
| PSM (oracle) | – | yes | 8.43 | 3.82 | 91.1 | 13.40 | 9.63 |
| IAM (oracle) | – | yes | 5.37 | 3.47 | 89.7 | 14.85 | 6.52 |

### SMS-WSJ separation + ASR (Table II, selected rows)

| Approach | Eq. | Re-syn? | SI-SDR (dB) | PESQ | eSTOI (%) | mSNR (dB) | WER (%) |
|----------|-----|---------|-------------|------|-----------|-----------|---------|
| Unprocessed | – | – | −5.5 | 1.50 | 44.1 | −4.44 | 79.43 |
| MSA | (9) | yes | 0.25 | 2.20 | 69.8 | 8.42 | 32.84 |
| MSA | (9) | no | – | – | – | 9.57 | 33.87 |
| RI | (2) | yes | 4.64 | 1.97 | 70.1 | 8.72 | 42.26 |
| RI+Mag | (3) | yes | 3.23 | 2.21 | 70.1 | 8.59 | 35.97 |
| RI-iSTFT | (4) | yes | 4.51 | 1.87 | 67.8 | 8.00 | 44.58 |
| RI-iSTFT+Mag | (5) | yes | 3.46 | 2.24 | 71.3 | 9.01 | 33.66 |
| (RI-iSTFT)×0+Mag | (11) | yes | 1.96 | 2.29 | 72.08 | 9.04 | **32.38** |
| Wav | (7) | yes | 4.22 | 1.79 | 66.3 | 8.33 | 47.50 |
| Wav+Mag | (8) | yes | 3.42 | 2.07 | 68.9 | 8.33 | 39.22 |
| Wav×0+Mag | (12) | yes | −4.15 | 2.11 | 69.58 | 8.24 | 37.91 |
| PSM (oracle) | – | yes | 5.79 | 3.64 | 89.7 | 10.46 | 5.84 |
| IAM (oracle) | – | yes | 1.53 | 3.37 | 91.1 | 13.11 | 5.71 |

![[raw/papers/wang-2021-magnitude-phase-compensation/figures/fig1.png|2D histograms of phase difference vs. magnitude ratio for MSA, RI, RI+Mag, Wav, Wav+Mag]]

*Figure 2: 2D histograms of phase difference $\cos(\angle S-\angle Y)$ (x-axis) vs. magnitude ratio $\hat{M}/|S|$ truncated to $[0,2]$ (y-axis), on a test mixture of WHAMR! (mixture mSNR −2.3 dB). MSA's magnitude ratios cluster near the perfect-estimation dashed line; RI compresses magnitudes toward zero where phases differ, and RI+Mag partially remedies this.*

**Key findings**:

1. **Magnitude-loss trade-off confirmed and explained**: RI vs. RI+Mag, RI-iSTFT vs. RI-iSTFT+Mag, Wav vs. Wav+Mag — adding a magnitude loss consistently improves PESQ, eSTOI, mSNR (and WER), at a small SI-SDR cost. The estimated magnitude otherwise compensates for the inaccurate phase.
2. **MSA gives the best magnitude**: without re-synthesis, MSA reaches the best learned mSNR (13.05 dB on WHAMR!) because it avoids compensation entirely (teacher-forced target phase); with re-synthesis its SI-SDR drops since mixture phase is used.
3. **Phase gains come from the model, not the magnitude loss**: the Phase model achieves the best pSNR (12.4 dB); adding a magnitude loss *degrades* pSNR (10.8 vs. 10.4 dB for RI vs. RI+Mag). Improvements over mixture phase stem from strong complex/time-domain DNN prediction.
4. **Magnitude-only end-to-end training works**: (RI-iSTFT)×0+Mag beats RI-iSTFT+Mag on PESQ/eSTOI/mSNR with no time-domain loss — the complex-domain model implicitly finds a reasonably good phase; Wav×0+Mag retains good PESQ/eSTOI/mSNR despite SI-SDR −9.09 dB and pSNR −3.64 dB (likely due to Conv-TasNet's short 5 ms window), showing **PESQ/eSTOI depend largely on magnitude alone**.
5. **Oracle masks**: PSM (compensated step along $\angle Y$) obtains better SI-SDR; IAM (aggressive oracle step $|S|$ along $\angle Y$) obtains better mSNR and WER, and MSA beats PSA on all magnitude-favoring metrics.

## Key Contributions

1. **Novel explanation of the magnitude-loss phenomenon**: the implicit compensation between estimated magnitude and phase — complex/time-domain losses are minimized by a magnitude that projects the clean spectrum onto the (inaccurate) estimated-phase direction, sacrificing magnitude accuracy.
2. **First comprehensive metric-level analysis**: decomposes quality into mSNR/pSNR and shows why PESQ/eSTOI (magnitude-dominant, alignment-forgiving) vs. SI-SDR (phase-sensitive, compensation-favoring) respond oppositely to magnitude losses.
3. **Practical guidance**: (i) time-domain benchmark models evaluated with PESQ/STOI/WER should be trained with a combined time + magnitude loss; (ii) for magnitude-only consumers such as robust ASR, direct magnitude estimation (MSA) without re-synthesis avoids compensation; (iii) separators feeding energy-feature detectors (e.g. sound event detection) should include magnitude losses or be trained jointly with the detector.

## Related Concepts

- [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] — the central concept this paper names and analyzes
- [[concepts/phase-sensitive-mask|Phase-Sensitive Mask (PSM)]] — the magnitude-domain training target that explicitly encodes compensation
- [[concepts/magnitude-phase-snr|mSNR and pSNR]] — the decomposition metrics introduced for the analysis
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]]
- [[concepts/frequency-domain-loss|Frequency Domain Loss for Time-Domain Networks]]
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]]
- [[concepts/pesq|PESQ]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training]]
- [[concepts/stft-consistency|STFT Consistency]]
- [[concepts/teacher-forcing|Teacher Forcing]] — MSA reinterpreted as teacher forcing with target phase
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Synthesis

- [[synthesis/deep-speech-enhancement|Deep Speech Enhancement]]
