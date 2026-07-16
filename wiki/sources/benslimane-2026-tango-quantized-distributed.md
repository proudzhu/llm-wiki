---
type: source
created: 2026-07-16
updated: 2026-07-16
sources:
  - raw/papers/benslimane-2026-tango-quantized-distributed/full-text.md
  - https://arxiv.org/abs/2607.08645
  - https://doi.org/10.48550/arXiv.2607.08645
  - zotero://select/items/0_FN59JY3C
tags:
  - speech-enhancement
  - distributed
  - binaural
  - hearing-aid
  - quantization
  - quantization-aware-training
  - post-training-quantization
  - knowledge-distillation
  - model-compression
  - low-compute
  - low-memory
  - grouped-rnn
  - erb
  - end-to-end
---

# Benslimane, Chouteau, Poreba, Auzanneau, Szczepanski, Chersi &amp; Serizel 2026: Quantized TANGO / MN-TANGO

**Authors**: [[entities/zahra-benslimane|Zahra Benslimane]]¹†, [[entities/pierre-chouteau|Pierre Chouteau]]¹, [[entities/martyna-poreba|Martyna Poreba]]¹, [[entities/fabrice-auzanneau|Fabrice Auzanneau]]¹, [[entities/michal-szczepanski|Michal Szczepanski]]¹, [[entities/fabian-chersi|Fabian Chersi]]¹, [[entities/romain-serizel|Romain Serizel]]²
**Affiliations**: ¹ Université Paris-Saclay, CEA, List, F-91120 Palaiseau, France; ² Université de Lorraine, CNRS, Inria, LORIA, F-54000 Nancy, France
**Venue**: arXiv preprint
**Year**: 2026
**Type**: Preprint
**DOI**: [10.48550/arXiv.2607.08645](https://doi.org/10.48550/arXiv.2607.08645)
**arXiv**: [2607.08645](https://arxiv.org/abs/2607.08645)
**Zotero**: [FN59JY3C](zotero://select/items/0_FN59JY3C)

## Summary

This paper investigates low-precision inference for the [[concepts/tango-framework|TANGO]] hybrid distributed binaural speech enhancement (SE) system. The authors evaluate [[concepts/post-training-quantization|dynamic post-training quantization (DPTQ)]] and [[concepts/quantization-aware-training|quantization-aware training (QAT)]] for the neural mask estimators, and analyze how quantization errors in the mask estimators propagate through the downstream [[concepts/multi-channel-wiener-filter|SDW-MWF]] / [[concepts/gevd-spatial-filtering|GEVD]] spatial filtering stage. Their key finding is that, although quantization degrades intermediate mask estimates, the spatial filtering stage compensates for most quantization-induced errors. Leveraging this robustness, they simplify TANGO into [[concepts/mn-tango|MN-TANGO]] (removing the first-stage SN-DNN entirely), and combine INT8 weight-and-activation quantization with [[concepts/erb-scale|ERB]] compression and [[concepts/grouped-recurrent-neural-network|grouped recurrent]] layers to reach as little as 4.65 MMAC/s and 0.177 MB.

## Problem Formulation

[[concepts/distributed-binaural-speech-enhancement|Distributed binaural SE]] systems such as TANGO achieve strong performance but their computational and memory requirements limit deployment on resource-constrained hearing-aid hardware. Prior model-compression work for SE has focused almost exclusively on single-channel, purely neural models; hybrid multichannel neural+spatial systems remained unexplored. This paper asks:

1. Can the neural component of a hybrid neural-spatial SE system be quantized to INT8 without losing final enhancement quality?
2. Does the downstream spatial filter compensate for quantization-induced mask errors?
3. Can the original two-stage TANGO architecture be simplified while preserving performance, and how far can the simplified model be compressed?

## Methodology

![[raw/papers/benslimane-2026-tango-quantized-distributed/figures/0d7b5d9f269fa471769383d66e24ea96165993938ca9078596698a41de282b8b.jpg|Figure 1: TANGO variants]]

*Figure 1: Overview of the evaluated TANGO variants. (a) Original two-stage TANGO with SN-DNN followed by MN-DNN processing. (b) Inverted TANGO with MN-DNN processing before the SN-DNN stage; the dotted lines indicate the two alternative inputs to the second-stage SN-DNN: (B†) uses the output of the first spatial filtering stage, whereas (B⋆) uses the local reference signal. (c) MN-TANGO with only the MN-DNN stage.*

### Baseline TANGO Architecture

The baseline [[concepts/tango-framework|TANGO]] (Furnon et al., 2021) is a two-stage distributed binaural SE system. In Stage 1, each ear-node independently estimates speech and noise time-frequency masks using a Single-Node DNN (SN-DNN); these masks drive a [[concepts/gevd-spatial-filtering|GEVD-based]] Speech Distortion Weighted Multichannel Wiener Filter (SDW-MWF) that produces an ear-specific compressed signal transmitted to the contra-lateral ear-node. In Stage 2, a Multi-Node DNN (MN-DNN) refines the masks using both local signals and the exchanged representation, and a final SDW-MWF generates the enhanced binaural output.

### From TANGO to MN-TANGO

Three architectural variants are investigated (Fig. 1):

- **Inverted TANGO (B†)**: Swaps the stage order — MN-DNN first, then SN-DNN. The second-stage SN-DNN uses the output of the first spatial filtering stage.
- **Inverted TANGO (B⋆)**: Same as (B†), but the second-stage SN-DNN uses only the local reference signal of the corresponding node.
- **[[concepts/mn-tango|MN-TANGO]]**: Removes the SN-DNN stage entirely, keeping only the MN-DNN plus the final spatial filtering stage. This tests whether the first single-node stage is necessary once inter-node information is available.

### End-to-End Training with Differentiable Spatial Filtering

The original TANGO optimizes mask estimators with mask-level MSE only. This work introduces **end-to-end training** that includes the spatial filtering stage in the training loop via a differentiable SDW-MWF, allowing gradients to flow from an enhanced-STFT loss back to the mask estimators. At inference, the GEVD-based implementation is used. The combined objective is:

$$\mathcal{L}_{\mathrm{task}} = \alpha \mathcal{L}_{\mathrm{mask}} + (1 - \alpha) \mathcal{L}_{\mathrm{STFT}}$$

with $\alpha = 0.3$. The per-ear enhanced-STFT loss combines magnitude and complex-domain MSE terms controlled by $\beta = 0.3$:

$$\ell_{\mathrm{STFT}}(\tilde{S}_c, S_c) = (1 - \beta) \mathrm{MSE}(|\tilde{S}_c|, |S_c|) + \beta \left( \mathrm{MSE}(\mathrm{Re}\{\tilde{S}_c\}, \mathrm{Re}\{S_c\}) + \mathrm{MSE}(\mathrm{Im}\{\tilde{S}_c\}, \mathrm{Im}\{S_c\}) \right)$$

### Low-Precision Quantization

[[concepts/post-training-quantization|DPTQ]] uses PyTorch eager-mode dynamic quantization (INT8 weights, FP32 activations). [[concepts/quantization-aware-training|QAT]] inserts fake-quantization modules in the forward pass during training, with gradients approximated by a straight-through estimator. The main configuration is **W8A8**: trainable weights and internal activations quantized to 8 bits, while input and output mask tensors are 16-bit. Weights use a symmetric signed quantizer; activations use an asymmetric affine quantizer with observer-based range initialization. The authors additionally apply **knowledge distillation (KD)** with floating-point TANGO as teacher and the quantized model as student, combining mask-level and enhanced-STFT KD losses.

### Low-Compute Architectural Compression

Architectural compression reuses the strategy from [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|RT-Tango]]: [[concepts/erb-scale|ERB]] feature compression (64 low-frequency linear bins + 64 ERB bands → 128-dim recurrent input) and [[concepts/grouped-recurrent-neural-network|grouped LSTM]] layers (hidden state partitioned into $G$ groups with deterministic interleaving between layers). The original 3-layer unidirectional LSTM (128 hidden units) is replaced with a 2-layer grouped LSTM (128 hidden units, $G \in \{1, 2, 4, 6, 8, 10\}$).

## Experimental Setup

| Item | Detail |
|------|--------|
| **Training data** | Simulated binaural mixtures (Monir et al. protocol); 4-mic hearing-aid config (2 mics/ear); LibriSpeech speech + speech-shaped & real environmental noise |
| **Evaluation data** | BinauRec subset: 1,200 binaural mixtures; measured RIRs from a portable hearing laboratory (PHL) with behind-the-ear hearing aids on a dummy head |
| **Target/noise geometry** | Target in front; noise at 45° and 90° right (lower SIR at right ear) |
| **Input SNRs** | −5, 0, 5 dB |
| **STFT** | 512-point FFT, 512-sample Hann window, 256-sample hop at 16 kHz (62.5 frames/s), 257-bin magnitude features |
| **Optimizer** | Adam; lr $5 \times 10^{-4}$ (FP32 end-to-end), $10^{-4}$ (QAT fine-tuning) |
| **Loss weights** | $\alpha = 0.3$, $\beta = 0.3$; KD: $\lambda_{\mathrm{KD}} = 0.3$, $\lambda_{\mathrm{task}} = 0.7$; SDW-MWF trade-off $\mu = 1$ |
| **SN-DNN** | 3-layer unidirectional LSTM, 128 hidden units, FC head (256 → 257) |
| **MN-DNN** | Point-wise conv + GELU + LayerNorm + 3-layer unidirectional LSTM (128) + sigmoid FC head (257) |
| **Grouped MN-DNN** | 2-layer unidirectional grouped LSTM (128 hidden units); ERB projection 64+64 → 128 (adjusted for divisibility by $G$) |
| **Quantization** | DPTQ (PyTorch dynamic); QAT W8A8 (symmetric weights, asymmetric activations, 16-bit I/O); bias in accumulator domain |
| **Baselines** | Float32 TANGO; DPTQ TANGO; QAT TANGO (W8A8 with INT16 I/O) |
| **Metrics** | SI-SDR, SI-SIR, SI-SAR (dB); STOI, PESQ; MMACs/s; #Params; Memory (MB) |

## Results

### Quantization scheme comparison on full TANGO (Table I)

| Quant. scheme | W | A | I/O | Memory (MB) | SI-SIR L/R | SI-SDR L/R | STOI L/R | PESQ L/R |
|---------------|---|---|-----|-------------|------------|------------|----------|----------|
| Float32 | FP32 | FP32 | FP32 | 4.03 | 22.8 / 26.2 | 4.7 / 5.0 | 0.842 / 0.850 | 1.731 / 1.770 |
| DPTQ | INT8 | FP32 | FP32 | 1.01 | 18.4 / 20.9 | 2.7 / 2.9 | 0.811 / 0.813 | 1.585 / 1.614 |
| QAT | INT8 | FP32 | FP32 | 1.083 | 22.8 / 26.2 | 4.7 / 5.0 | 0.843 / 0.851 | 1.729 / 1.765 |
| QAT | INT8 | INT8 | INT16 | 1.083 | 23.0 / 25.9 | 3.7 / 4.5 | 0.828 / 0.842 | 1.735 / 1.753 |

DPTQ heavily degrades performance (LSTM activations span different dynamic ranges). Weight-only QAT preserves FP32 performance almost exactly. Adding activation+I/O quantization slightly degrades SI-SDR/SI-SAR but preserves STOI/PESQ.

### Stage-wise TANGO variants in FP32 (Table II, final GEVD rows)

| Method | MMACs/s | #Params | SI-SIR L/R | SI-SDR L/R | STOI L/R | PESQ L/R |
|--------|---------|---------|------------|------------|----------|----------|
| TANGO | 65.65 | 1 M | 24.3 / 25.6 | 5.3 / 4.9 | 0.85 / 0.85 | 1.76 / 1.68 |
| Inverted (B†) | 65.65 | 1 M | 24.2 / 24.9 | 5.2 / 4.9 | 0.85 / 0.84 | 1.71 / 1.67 |
| Inverted (B⋆) | 65.65 | 1 M | 23.2 / 23.6 | 6.7 / 5.5 | 0.88 / 0.84 | 1.84 / 1.77 |
| **MN-TANGO (GEVD)** | **30.79** | **0.5 M** | 23.7 / 24.2 | 6.1 / 5.5 | 0.86 / 0.84 | 1.79 / 1.73 |
| MN-TANGO (SDW-MWF) | 30.79 | 0.5 M | 12.5 / 10.4 | 6.9 / 5.5 | 0.83 / 0.76 | 1.56 / 1.37 |

The largest performance jump consistently occurs after the **final spatial filtering stage**, not within the neural mask estimators — confirming that the spatial filter contributes most of the final enhancement. MN-TANGO matches or exceeds the full TANGO in SI-SDR/STOI/PESQ while halving parameters and compute. The best single-number SI-SIR is achieved by Inverted (B⋆), but MN-TANGO offers the best overall trade-off.

### W8A8 quantization + KD on MN-TANGO (Table III)

| Output | Precision | KD | SI-SIR L/R | SI-SDR L/R | STOI L/R | PESQ L/R |
|--------|-----------|----|------------|------------|----------|----------|
| MN-DNN | FP32 | — | 12.2 / 8.9 | 4.2 / 2.0 | 0.67 / 0.61 | 1.19 / 1.13 |
| MN-DNN | W8A8 | ✘ | 10.7 / 7.1 | 3.7 / 1.4 | 0.66 / 0.59 | 1.18 / 1.12 |
| MN-DNN | W8A8 | ✓ | 10.6 / 7.0 | 3.6 / 1.3 | 0.65 / 0.59 | 1.18 / 1.12 |
| Final (GEVD) | FP32 | — | 23.7 / 24.2 | 6.1 / 5.5 | 0.86 / 0.84 | 1.79 / 1.73 |
| Final (GEVD) | W8A8 | ✘ | 23.6 / 24.8 | 5.8 / 5.4 | 0.86 / 0.84 | 1.77 / 1.71 |
| Final (GEVD) | W8A8 | ✓ | 23.9 / 25.2 | 5.8 / 5.3 | 0.86 / 0.84 | 1.77 / 1.72 |

W8A8 quantization noticeably degrades the **intermediate MN-DNN output**, but most of the degradation disappears after GEVD filtering — confirming the spatial filter is robust to 8-bit quantization. KD provides only marginal improvements.

### Grouped recurrent complexity (Table IV)

| G | PW | LSTM | ERB+Inv. | FC | Total/frame (kMAC) | Total/s (MMAC) |
|---|-----|------|----------|-----|--------------------|----------------|
| 1 | 0.51 | 459.26 | — | 32.90 | 492.67 | 30.79 |
| 2 | 0.51 | 131.07 | 24.70 | 16.38 | 172.67 | 10.79 |
| 4 | 0.51 | 65.54 | 24.70 | 16.38 | 107.14 | 6.70 |
| 6 | 0.51 | 42.34 | 23.93 | 15.88 | 82.66 | 5.17 |
| 8 | 0.51 | 32.77 | 24.70 | 16.38 | 74.37 | 4.65 |
| 10 | 0.51 | 27.04 | 25.48 | 16.90 | 69.93 | 4.37 |

The LSTM dominates neural compute (459 → 27 kMAC/frame as $G: 1 \to 10$). Grouping effect is **not strictly monotonic**: $G=2$ is best, $G=4$/$6$ degrade noticeably, $G=8$/$10$ partially recover.

### Performance-complexity trade-off (Table V)

| Method | G | MMACs/s | #Params | Memory | SI-SIR L/R | SI-SDR L/R | STOI L/R | PESQ L/R |
|--------|---|---------|---------|--------|------------|------------|----------|----------|
| TANGO (FP32) | — | 65.65 | 1 M | 4.03 MB | 24.3 / 25.6 | 5.3 / 4.9 | 0.85 / 0.85 | 1.76 / 1.68 |
| MN-TANGO W8A8 | — | 30.79 | 0.5 M | 0.508 MB | 23.7 / 24.2 | 6.1 / 5.5 | 0.86 / 0.84 | 1.79 / 1.73 |
| MN-TANGO W8A8 | 2 | **10.79** | 0.179 M | 0.274 MB | 22.7 / 22.8 | 5.7 / 5.0 | 0.85 / 0.83 | 1.74 / 1.66 |
| MN-TANGO W8A8 | 8 | **4.65** | 0.081 M | **0.177 MB** | 21.2 / 21.3 | 5.2 / 4.4 | 0.84 / 0.82 | 1.68 / 1.60 |

### Key findings

- **The final spatial filtering stage provides most of the enhancement**, not the neural mask estimators. For full TANGO, GEVD lifts SI-SIR from 13.0/7.8 dB (after MN-DNN) to 24.3/25.6 dB.
- **Spatial filtering mitigates quantization-induced errors.** W8A8 degrades MN-DNN SI-SIR by ~1.5 dB, but the final GEVD output is within 0.1–0.6 dB of the FP32 baseline.
- **MN-TANGO preserves performance with ~50% fewer parameters and MACs.** Removing the SN-DNN stage is justified once inter-node information is available.
- **Knowledge distillation brings only marginal benefit** once the downstream spatial filter compensates for most quantization artifacts.
- **Grouped recurrence offers large savings** with a non-monotonic quality trade-off; $G=2$ is the best quality/compute operating point, $G=8$ the most compact.
- **Best trade-off**: $G=2$ → 10.79 MMAC/s, 0.179 M params, 0.274 MB — a ~6× compute reduction vs. FP32 TANGO.
- **Most compact**: $G=8$ → 4.65 MMAC/s, 0.081 M params, 0.177 MB — a ~14× compute reduction and ~23× memory reduction vs. FP32 TANGO.
- **Train-test filter mismatch**: SDW-MWF inference yields higher SI-SDR/SI-SAR but lower SI-SIR/STOI/PESQ than GEVD inference, validating differentiable SDW-MWF as an optimization surrogate while GEVD remains preferable at deployment.

## Key Contributions

1. First systematic study of **low-precision inference for a hybrid neural-spatial multichannel SE system**, showing that the hybrid structure is inherently robust to neural quantization because the downstream spatial filter compensates for mask errors.
2. Introduction of **MN-TANGO**, a simplified single-stage variant that removes the SN-DNN and halves parameters/compute while preserving final enhancement quality.
3. **End-to-end training with a differentiable SDW-MWF**, aligning optimization with the final enhanced-signal objective while keeping GEVD-based inference at deployment.
4. A **W8A8 QAT pipeline with optional knowledge distillation** for the neural mask estimators, including asymmetric activation quantization and observer-based range initialization.
5. A **combined INT8 + ERB + grouped-LSTM compression** yielding a 6–14× compute reduction and up to 23× memory reduction relative to FP32 TANGO, with minimal quality loss.

## Related Concepts

- [[concepts/tango-framework|Tango Framework]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/quantization-aware-training|Quantization-Aware Training (QAT)]]
- [[concepts/post-training-quantization|Post-Training Quantization (DPTQ)]]
- [[concepts/gevd-spatial-filtering|GEVD-Based Spatial Filtering]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network (GRNN)]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/erb-scale|ERB Scale]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/audio-latency|Audio Latency]]

## Related Synthesis

- [[synthesis/computational-efficiency-evolution|Computational Efficiency in ANC: From O(N²) to GPU-Accelerated DSP]]
