---
type: concept
created: 2026-11-08
updated: 2026-11-08
sources:
  - raw/papers/wang-2025-multi-modal-deep-filtering-bc/full-text.md
tags:
  - speech-enhancement
  - bone-conduction
  - multi-modal-fusion
  - deep-filtering
---

# Multi-Modal Deep Filtering

**Multi-modal deep filtering** extends [[concepts/deep-filtering|deep filtering]] from a per-bin temporal filter over one input spectrum to a **multi-input filter bank whose coefficients are the modality weights**. Instead of fusing modalities in a feature space (concatenation, attention, gating) and then filtering, the filter itself accepts every modality's spectrum and learns a separate coefficient set per modality — so the fusion is expressed as part of the linear-combination structure of the enhancement filter.

## Formulation

For a D-order causal filter over a two-modality observation (e.g. noisy air-conducted spectrum $\mathbf{X}^{a}$ and bone-conducted spectrum $\mathbf{X}^{b}$):

$$
\hat{\mathbf{S}}_{\mathrm{STFT}}(k,f) = \sum_{j=0}^{D}\mathbf{c}^{a}(k,j,f)\,\mathbf{X}^{a}_{\mathrm{STFT}}(k-j,f) + \sum_{j=0}^{D}\mathbf{c}^{b}(k,j,f)\,\mathbf{X}^{b}_{\mathrm{STFT}}(k-j,f)
$$

Each $\mathbf{c}^{m} \in \mathbb{C}^{D+1}$ is predicted by the network per time-frequency bin. Two degenerate cases fall out of the same equation:

- $\mathbf{c}^{b} = 0$ → single-modal AC enhancement (the plain [[concepts/deep-filtering|DeepFilterNet]] case)
- $\mathbf{c}^{a} = 0$ → BC-only enhancement

The network therefore *interpolates* between single-modal systems per bin and per tap, driven by the instantaneous SNR of each modality, rather than committing to a fixed fusion ratio at training time.

## Why This Differs From Feature-Level Fusion

| Aspect | Feature-level fusion (concat / iAFF / attention) | Multi-modal deep filtering |
|--------|------------------------------------------------|---------------------------|
| Where modalities meet | In a learned embedding | In the filter coefficients |
| Fusion granularity | Per feature map / per channel | **Per frequency bin, per filter tap** |
| Temporal context of the fusion decision | Whatever the recurrent/attention layers model | The filter order $D$ — explicit and bounded |
| Degenerate single-modal case | Requires an explicit ablation model | Emitted by the same parameters ($\mathbf{c}^b = 0$) |
| Phase handling | Depends on the output target (mask vs. mapping) | Implicit in the complex coefficients |

The cost is that the fusion cannot exploit any nonlinear cross-modality interaction beyond what the coefficient predictor learns: the combination itself is linear in the input spectra. Feature-level fusion can in principle represent arbitrary cross-modal interactions, which is likely why heavier attention-based designs (DC-CRN, DenGCAN) still lead on raw enhancement metrics.

## MDFNet (Wang et al. 2025)

[[sources/wang-2025-multi-modal-deep-filtering-bc|Wang, Kuang, Li, Yang, Bai & Liu 2025]] introduce the formulation in **MDFNet**, using it only for the **low-frequency band**, where the BC spectrum is intact:

- **Low band**: multi-modal deep filtering of AC + BC complex spectra (this page's formulation).
- **High band**: [[concepts/erb-scale|ERB]]-band gains applied to the **AC spectrum only**, since BC carries almost no high-frequency energy — the multimodal filter would have nothing to filter there.

The model is described as sharing its structure with [[sources/schroter-2022-deepfilternet|DeepFilterNet]] (UNet-like [[concepts/depthwise-separable-convolution|depthwise separable]] encoder, [[concepts/grouped-recurrent-neural-network|grouped GRU]] temporal modeling, ERB decoder plus a filtering decoder), with two separate offline decoders rather than one shared head. Reported on the 100-speaker ABCS corpus at 16 kHz, SNR ∈ [−15, 5] dB: PESQ 3.21 / STOI 0.79 / ESTOI 0.69 / CER 24.8%, versus 2.37 / 0.69 / 0.54 / 57.0% for the AC-only deep-filtering ablation (AC-DFNet) — the largest gain in the paper's table comes from adding the BC modality *inside the filter*. The paper does not report $D$, the band-split frequency, or any parameter/MAC count.

## Relationship to Other Multi-Modal Because-of-a-Linear-Filter Designs

- **Beamforming** is the spatial analog: an MVDR/GSC beamformer linearly combines *channels of the same physical modality* with weights derived from covariance statistics. Multi-modal deep filtering combines *different physical modalities* with learned weights, without any spatial model.
- **[[concepts/iterative-attentional-feature-fusion|iAFF]]** (Kuang 2024/2025) fuses before the enhancement network and then predicts a mask/filter from the fused features — the fusion and the filtering are separate stages, in contrast with the single-stage formulation here.
- **[[concepts/adl-mvdr|ADL-MVDR]]**-style 2-D complex ratio filtering (cRF) also fuses information through coefficients, but across *neighbouring bins and frames* of one input rather than across modalities.

## Related Concepts

- [[concepts/deep-filtering|Deep Filtering]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]

## Related Sources

- [[sources/wang-2025-multi-modal-deep-filtering-bc|Wang, Kuang, Li, Yang, Bai & Liu 2025: Multi-Modal Deep-Filtering-Based Speech Enhancement via Bone-Conducted Speech]] — introduces the formulation (MDFNet)
- [[sources/schroter-2022-deepfilternet|Schröter et al. 2022: DeepFilterNet]] — the single-modal deep-filtering original MDFNet's architecture and losses follow
- [[sources/kuang-2025-low-complexity-bc-speech-enhancement|Kuang, Yang, Wang & Yang 2025: Low-Complexity BC-Aided Speech Enhancement]] — the same research group's deep filtering on *fused* BC/AC features rather than per-modality coefficients
