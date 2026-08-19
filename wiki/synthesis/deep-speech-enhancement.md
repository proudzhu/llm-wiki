---
type: synthesis
created: 2026-08-04
updated: 2026-08-19
sources:
  - raw/papers/tan-2018-convolutional-recurrent-network-speech-enhancement/full-text.md
  - raw/papers/pandey-2019-cnn-speech-enhancement-time-domain/full-text.md
  - raw/papers/wang-2018-supervised-speech-separation-deep-learning-overview/full-text.md
  - raw/papers/zheng-2023-survey-frequency-domain-speech-enhancement/full-text.md
  - raw/papers/rong-2024-gtcrn-speech-enhancement-ultralow/full-text.md
  - raw/papers/schroter-2022-deepfilternet/full-text.md
  - raw/papers/indenbom-2023-deepvqe/full-text.md
  - raw/papers/chao-2024-mamba-speech-enhancement/full-text.md
  - raw/papers/xu-2026-drifting-models-speech-enhancement/full-text.md
  - raw/papers/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement/full-text.md
  - raw/papers/liu-2026-array-invariant-speech-enhancement/full-text.md
  - raw/papers/apostolidis-2026-listen-first-output-based-multi-microphone/full-text.md
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
tags:
  - speech-enhancement
  - deep-learning
  - neural-network-architecture
  - survey
  - evolution
---

# Deep Speech Enhancement: Architectural & Methodological Evolution

> Cross-source synthesis tracing how deep learning for speech enhancement (SE) evolved from the 2018 Convolutional Recurrent Network to the 2026 SSM / array-invariant / generative frontier — along six largely independent axes: training target, signal domain, backbone, efficiency, multi-channel integration, and conditioning paradigm.

## Scope and Relationship to Other Syntheses

"Deep speech enhancement" is the broad umbrella under which several specialized synthesis pages in this wiki sit. This page traces the **core architectural and methodological evolution** of the SE problem itself (denoising / separation / dereverberation via neural networks). It deliberately defers to the specialized syntheses for sub-topics:

- **Multi-modal fusion** (BC / AC / IMU) → [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]], [[synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]]
- **Joint multi-task (AEC+NS+DR+OVC+AHS) and sub-10 ms latency tiers** → [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]]
- **ANC computational efficiency / RNN memory bottlenecks** → [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]]

The thesis here is that the field's progress is **not a single replacement story** (e.g. "LSTM → Transformer") but the Cartesian product of six near-orthogonal axes, each of which has its own frontier. A 2026 state-of-the-art system is built by picking one point on each axis.

## Sources Synthesized

| Source | Year | Axis advanced | Key contribution |
|--------|------|---------------|------------------|
| [[sources/wang-2018-supervised-speech-separation-deep-learning-overview\|Wang & Chen 2018]] | 2018 | Target | Survey codifying IBM/IRM/PSM/cIRM training targets for supervised separation |
| [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement\|Tan & Wang 2018 (CRN)]] | 2018 | Backbone | CED + LSTM, causal convolutions; the foundational deep SE architecture (17.58M params) |
| [[sources/pandey-2019-cnn-speech-enhancement-time-domain\|Pandey & Wang 2019 (AECNN)]] | 2019 | Domain | Time-domain U-Net trained with STFT-magnitude loss → frequency-loss-for-time-domain-nets paradigm |
| [[sources/schroter-2022-deepfilternet\|Schröter et al. 2022 (DeepFilterNet)]] | 2022 | Target | Deep Filtering: complex temporal filter generalizing the complex ratio mask |
| [[sources/indenbom-2023-deepvqe\|Indenbom et al. 2023 (DeepVQE)]] | 2023 | Target | Complex Convolving Mask: T-F-neighborhood filter with 120° three-vector weights |
| [[sources/zheng-2023-survey-frequency-domain-speech-enhancement\|Zheng et al. 2023]] | 2023 | All | 60-year survey; five-group taxonomy; magnitude–phase "compensation effect" |
| [[sources/rong-2024-gtcrn-speech-enhancement-ultralow\|Rong et al. 2024 (GTCRN)]] | 2024 | Efficiency | 23.7K params via grouped conv + grouped RNN + ERB compression |
| [[sources/zhao-2024-sicrn\|Zhao, He & Zhang 2024 (SICRN)]] | 2024 | Backbone | S4ND state-space model + inplace conv; near-FullSubNet at 0.14× MACs |
| [[sources/chao-2024-mamba-speech-enhancement\|Chao et al. 2024 (SEMamba)]] | 2024 | Backbone | First Mamba-based SE; SOTA PESQ 3.69 on VoiceBank-DEMAND with PCS |
| [[sources/wang-2025-adaptive-convolution-cnn-speech-enhancement\|Wang et al. 2025 (AdaptCRN)]] | 2025 | Efficiency | Adaptive (dynamic) convolution in the CRN family; 135K params, PESQ 2.98 |
| [[sources/zhu-2026-g-map-se-guided-speech-enhancement\|Zhu et al. 2026 (G-MaP-SE)]] | 2026 | Conditioning | GMM prior matching refines noisy speaker embeddings for PSE |
| [[sources/xu-2026-drifting-models-speech-enhancement\|Xu et al. 2026 (DriftSE)]] | 2026 | Backbone | Drifting models: one-step generative SE without any trajectory |
| [[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement\|Yang et al. 2026 (CoFi-Lite)]] | 2026 | Efficiency | Dual coarse/fine-path CRN; beats GTCRN at 40% of its MACs |
| [[sources/liu-2026-array-invariant-speech-enhancement\|Liu et al. 2026 (Geo-DConv)]] | 2026 | Multi-channel | Geometry-conditioned dynamic conv → array-invariant SE backbones |
| [[sources/apostolidis-2026-listen-first-output-based-multi-microphone\|Apostolidis 2026]] | 2026 | Multi-channel | Output-based SE: select MPDR output by Glimpse Proportion, not input features |
| [[sources/ostergaard-2026-own-voice-cancellation\|Østergaard et al. 2026 (OVC)]] | 2026 | Conditioning | Inverts PSE: remove the enrolled speaker; Mamba-MinGRU at 2 ms |

## Insight 1: The Training Target Evolved from Pointwise Masks to Neighborhood Filters

The single clearest lineage in deep SE is the **monotonic generalization of the T-F "mask" into a T-F "filter"**. Each step subsumes the previous as a special case.

| Generation | Target | Operation | Reference |
|------------|--------|-----------|-----------|
| 1 | [[concepts/ideal-binary-mask\|IBM]] | Pointwise binary T-F gate | Wang & Wang 2013 |
| 2 | [[concepts/ideal-ratio-mask\|IRM]] / PSM | Pointwise real gain | Narayanan & Wang 2013; Erdogan 2015 |
| 3 | [[concepts/complex-ratio-mask\|cIRM]] | Pointwise complex gain (magnitude + phase) | Williamson 2016 |
| 4 | [[concepts/complex-spectrum-mapping\|Complex spectrum mapping]] | Direct RI regression (no mask) | Tan & Wang 2019/2020 |
| 5 | [[concepts/complex-convolving-mask\|Complex Convolving Mask (CCM)]] | Convolution over a T-F neighborhood | Indenbom 2023 |
| 6 | [[concepts/deep-filtering\|Deep Filtering (DF)]] | Causal complex temporal filter of order *N* | Schröter 2022 |

The key relation: **CRM = DF with filter order $N=1$ and look-ahead $l=0$**. DF is a strict generalization — it can recover degradations (notch-like zeros, frame zeroing) that pointwise masks structurally cannot, and it outperforms CRMs across all FFT sizes (5–30 ms latency), with the gap widest at low frequency resolution where CRMs degrade. CCM extends in the other direction — across the **frequency** neighborhood — using three weight components at 120° in the complex plane ($1,\ -\tfrac{1}{2}+j\tfrac{\sqrt{3}}{2},\ -\tfrac{1}{2}-j\tfrac{\sqrt{3}}{2}$) for stable complex reconstruction.

**Takeaway**: the field moved from "estimate a gain per bin" to "estimate a filter per bin." Every modern competitive TF-domain system (DeepFilterNet, DeepVQE, DCCRN+) uses a filter-style target rather than a pointwise mask.

## Insight 2: Time-Domain vs TF-Domain Converged on a Hybrid (Time-Domain Arch + Frequency Loss)

A long-running debate — operate on raw waveforms or on STFT — was resolved not by a winner but by **combining the two at the loss level**.

- **TF-domain** methods (CRN, DCCRN, DPCRN) estimate a mask/spectrum and reconstruct with noisy phase. They suffer the [[concepts/invalid-stft-problem\|invalid STFT problem]] (enhanced magnitude + noisy phase may not correspond to any real signal) and phase degradation at low SNR.
- **Time-domain** methods ([[concepts/time-domain-speech-enhancement\|SEGAN, AECNN, Conv-TasNet, DEMUCS]]) generate valid waveforms directly, sidestepping both issues.

The decisive observation came from [[sources/pandey-2019-cnn-speech-enhancement-time-domain\|Pandey & Wang 2019]]: a time-domain AECNN trained with **STFT-magnitude MAE loss** outperforms the same network trained with waveform loss, and beats SEGAN/GRN on TIMIT/IEEE/WSJ0. Spectral losses provide a dramatically better perceptual training signal than waveform losses. The [[concepts/complex-spectrum-mapping\|complex STFT (RI) loss]] variant is best for SI-SDR.

The 60-year survey ([[sources/zheng-2023-survey-frequency-domain-speech-enhancement\|Zheng 2023]]) notes the field historically invested more research effort in frequency-domain methods, partly explaining their lead — but the convergence is now clear: modern systems use **time-domain or learned-encoder representations with multi-resolution STFT / RI losses**, and the choice of loss often matters more than minor architecture changes (the DCCRN(SNR) variant demonstrates loss choice outweighing architecture tweaks).

## Insight 3: The Magnitude–Phase "Compensation Effect" Drove Architectural Decoupling

[[sources/zheng-2023-survey-frequency-domain-speech-enhancement\|Zheng 2023]] crystallizes a recurring failure mode of single-stage complex-spectrum networks: a **compensation effect** where magnitude distortion is traded for phase recovery (and vice versa) within one shared decoder. The architecture response was **decoupling**:

| Architecture | Strategy | Phase handling |
|--------------|----------|----------------|
| DCCRN, GCRN | Single-stage complex mapping | Implicit, traded vs magnitude |
| CTSNet, G2Net/GaGNet, TaylorSENet | Decoupling-style: magnitude + residual complex | Explicit, separately optimized |
| [[concepts/mp-senet\|MP-SENet]] | Separate magnitude and phase decoders | Explicit, dual-decoder |

The decoupling-style group (CTSNet, G2Net, TaylorSENet) is the survey's consistent top performer at low SNR (≤ 0 dB) for normal-hearing listeners, and MP-SENet carries the dual-decoder idea forward as the backbone for both [[concepts/semamba\|SEMamba]] and G-MaP-SE. The same decoupling insight recurs in 2026 multi-channel work — [[sources/apostolidis-2026-listen-first-output-based-multi-microphone\|Apostolidis 2026]] decouples the *decision* (which output) from the *filtering* (MPDR beamforming), evaluating candidates by [[concepts/glimpse-proportion\|Glimpse Proportion]] rather than extracting a single input-conditioned mask.

## Insight 4: The Backbone Succession Is "Wider Context, Cheaper Recurrence"

The sequence-model backbone has turned over five times in eight years, each step expanding the effective context window while cutting per-step recurrence cost:

```
DNN (2014) → LSTM (2017) → CRN/CED+LSTM (2018) → complex CRN/DCCRN (2020)
   → DPRNN/DPCRN (2020/21) → dual-branch/decoupling (2022)
      → Conformer/attention/MP-SENet (2023)
         → SSM/Mamba/SEMamba + S4ND/SICRN (2024)
            → linear RNN/Mamba-MinGRU (2026) → SNN/SSE-Net (2026)
```

- **[[sources/tan-2018-convolutional-recurrent-network-speech-enhancement\|CRN (Tan & Wang 2018)]]** established the CED + LSTM template with causal convolutions; 17.58M params, half the LSTM baseline's parameters at better STOI/PESQ.
- **DPCRN** applied [[concepts/dprnn\|DPRNN]]'s chunked dual-path (intra-frame frequency RNN + inter-frame time RNN) and became the survey's smallest competitive DL model (0.72M params, 0.77 GMAC/s) — better performance did *not* require more compute.
- **Conformer (MP-SENet)** brought attention-based global context, replacing the RNN bottleneck with TF blocks.
- **[[concepts/mamba\|Mamba]] / SSM** is the current frontier: [[concepts/semamba\|SEMamba]] replaces MP-SENet's Conformer with a Time-Frequency Mamba block and matches its PESQ at ~12% lower FLOPs, reaching SOTA PESQ 3.69 on VoiceBank-DEMAND with [[concepts/perceptual-contrast-stretching\|PCS]]. [[concepts/sicrn\|SICRN]] uses a multidimensional SSM (S4ND) global branch and reaches within ~0.05 WB-PESQ of FullSubNet at 0.14× MACs.
- **Linear RNNs** ([[concepts/mamba-mingru\|Mamba-MinGRU]]) push into the 2 ms latency regime in [[sources/ostergaard-2026-own-voice-cancellation\|OVC]], exploiting the associative-scan property (parallel training, $\mathcal{O}(1)$ per inference step).
- **SNN** ([[concepts/sse-net\|SSE-Net]]) is the energy-efficiency extreme: spike-native SE with a 62% lower power proxy than Spiking-FullSubNet.

**Why Mamba/SSM wins in streaming**: parallel training via associative scan, long context that LSTMs handle poorly beyond ~100 steps, naturally causal, and small-state compute. This mirrors the linear-RNN replacement documented for joint multi-task SE in [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]] (Insight 3).

## Insight 5: The Efficiency Frontier Moved ~1000× via Four Orthogonal Techniques

Parameter counts for competitive monaural SE collapsed from ~18M (CRN, 2018) to 23.7K (GTCRN, 2024) — roughly 750× — and compute kept falling through 2026. The collapse is the product of four largely independent techniques:

| Technique | Mechanism | Origin / exemplar |
|-----------|-----------|-------------------|
| Perceptual band compression | ERB / Bark-scale feature reduction (e.g. 192→64 bands) | DeepFilterNet, GTCRN, PercepNet |
| Grouped conv + grouped RNN | Split channels / hidden states into groups; ShuffleNet-style units | [[concepts/gtcrn\|GTCRN]] (G-DPRNN), [[concepts/cofi-lite\|CoFi-Lite]] |
| Inplace convolution | Stride-1 freq-axis conv + channel-wise LSTM reused across bins | [[concepts/igcrn\|IGCRN]] → [[concepts/iccrn\|ICCRN]] → [[concepts/sicrn\|SICRN]] |
| Adaptive (dynamic) convolution | Frame-wise kernels conditioned on input | [[concepts/adaptcrn\|AdaptCRN]] (135K params, PESQ 2.98) |

The **inplace-CRN family** is its own lineage: [[concepts/igcrn\|IGCRN]] (2021, 1.4M, the founder) → [[concepts/iccrn\|ICCRN]] (2023, 0.46M, cepstral-space branch) → [[concepts/sicrn\|SICRN]] (2024, 2.16M, S4ND global branch). The throughline is preserving **per-bin spatial cues** via channel-wise LSTM (hidden 64 vs the conventional 1024) — IGCRN's downsampling ablation shows the inplace characteristic, not capacity, drives multi-channel SE performance.

The 2026 efficiency frontier is **CoFi-Lite** ([[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement\|Yang 2026]]): it reuses GTCRN's ERB/SFE/TRA machinery but decouples spectral modeling into parallel coarse (full-band envelope, ×16 compression) and fine (low-frequency detail below 2 kHz, ×2 compression) paths bridged by Cross-Path Fusion. It **outperforms GTCRN** (PESQ 2.16 vs 2.07 on DNS3) at 40% of its MACs (12.87M vs 31.97M MACs/s) — trading a higher parameter count (83K vs 24K) for drastically lower compute. The same lab lineage (GTCRN → CoFi-Lite → AdaptCRN) shows the techniques compose.

A second life for these ultralight models: [[sources/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction\|Huang 2026 (LGTSE)]] reuses GTCRN not as a standalone enhancer but as a **pluggable denoiser front-end** for target speech extraction, adding negligible overhead (6.08M → 6.13M params) while delivering +0.89 dB SI-SDR.

## Insight 6: Multi-Channel SE Went "Estimate SCM → Beamform" → End-to-End → Array-Invariant

The multi-channel arc has three phases, each relaxing an assumption of the previous:

1. **Hybrid DNN-guided linear filters** — [[sources/oviste-2026-neural-vslf-speech-enhancement\|Neural VSLF (Oviste 2026)]]: a DNN predicts clean-speech SCM, noise SCM, and a distortion/noise tradeoff parameter, then classical [[concepts/variable-span-linear-filter\|VSLF]] weights are computed (MWF/MVDR are special cases). Interpretable, controllable, but array-specific.
2. **End-to-end neural beamforming** — [[concepts/neural-beamforming\|neural beamformers]] and [[sources/zaidel-2026-linearly-constrained-deep-beamformer\|Zaidel 2026]]'s linearly-constrained deep beamformer learn the whole filter via differentiable constraint losses, outperforming LCMV. Highest quality, but bound to one array geometry.
3. **Array-invariant conditioning** — [[sources/liu-2026-array-invariant-speech-enhancement\|Geo-DConv (Liu 2026)]]: a universal front-end (Geo-DConv + [[concepts/topology-aware-coordinate-transformer\|TACT]]) converts *any* fixed-array SE backbone (SpatialNet, TF-GridNet) into an array-invariant system by generating geometry-specific convolution kernels from microphone coordinates. It matches USES2-comp quality at ~10× lower MACs and **zero-shot generalizes to CHiME-4**.

The conceptual move from phase 2 to phase 3 is from "learn the beamformer" to "condition a backbone on geometry." A parallel reframing appears in [[sources/apostolidis-2026-listen-first-output-based-multi-microphone\|Apostolidis 2026]]'s [[concepts/output-based-speech-enhancement\|output-based SE]]: instead of extracting features from the noisy input to predict a filter, evaluate the SI/SQ of *candidate outputs* and select the best — outperforming input-based MVDR especially at low SNR. Both 2026 works invert a long-standing assumption: the relevant signal is the *output* (or the geometry), not the input spectrum.

## Insight 7: Generative SE Crossed the One-Step Barrier in 2026 — but Discriminative Still Competes

[[concepts/diffusion-models-for-speech\|Diffusion models]] established SOTA SE quality via score-based reverse dynamics, but their iterative inference (10–100 NFE) was a real-time blocker. The 2026 corpus shows the one-step barrier finally crossed:

| Method | NFE | PESQ (VB-DEMAND) | Approach |
|--------|-----|------------------|----------|
| SGMSE+ | 30 | 2.90 | Score-based diffusion |
| ROSE-CD | 1 | 3.49 | Consistency distillation |
| SBCTM | 1 | 3.56 | Schrödinger bridge + consistency |
| MeanFlowSE | 1 | 2.81 | Mean flow |
| [[concepts/drifting-models\|DriftSE]] | 1 | 3.15 | Distributional equilibrium (no trajectory) |

Yet **discriminative** [[concepts/semamba\|SEMamba]] + PCS still holds SOTA PESQ 3.69 — higher than every one-step generative method. The practical split is clear: **generative methods win on unseen-noise / generalization robustness** (they model the clean-speech distribution, not a mapping), while **discriminative methods win on latency and MACs** (single forward pass, no NFE budget). The two are converging via hybrid predictive + few-step refinement (Storm, Diffusion-GAN), but as of 2026 the discriminative frontier remains the quality leader on standard benchmarks.

## Insight 8: Personalization Reframed as Enrollment-Conditioned Extraction — and Its Complement

Conditioning SE on a speaker embedding has bifurcated into two complementary tasks sharing the same machinery:

- **[[concepts/personalized-speech-enhancement\|PSE]]** — preserve the enrolled speaker, suppress the rest.
- **[[concepts/target-speaker-extraction\|Target Speech Extraction (TSE)]]** — extract the enrolled speaker from a mixture (LGTSE/D-LGTSE reuse GTCRN as the conditioning front-end).
- **[[concepts/own-voice-cancellation\|Own-Voice Cancellation (OVC)]]** — *invert* PSE: remove the enrolled (self) speaker, preserve everyone else.

[[sources/ostergaard-2026-own-voice-cancellation\|OVC (Østergaard 2026)]] makes the complementarity explicit — the same [[concepts/td-speakerbeam\|TD-SpeakerBeam]] / [[concepts/mamba-mingru\|Mamba-MinGRU]] conditioning runs forward (PSE) and backward (OVC), differing only in the objective. The conditioning signal itself is the hard part: [[sources/zhu-2026-g-map-se-guided-speech-enhancement\|G-MaP-SE (Zhu 2026)]] shows that **noisy enrollment embeddings** degrade PSE, and fixes it with GMM-based [[concepts/prior-matching\|prior matching]] to refine the embedding before conditioning (+0.03 WB-PESQ over noisy conditioning on DNS2020 at 0.025M added params). The lesson generalizes: in enrollment-conditioned SE, the *quality of the embedding* is as decisive as the enhancement backbone.

The canonical survey for the TSE half of this complementarity is [[sources/zmolikova-2023-neural-target-speech-extraction-overview\|Zmolikova et al. 2023 (IEEE SPM)]]: it factors TSE into a single framework (clue encoder + mixture encoder + fusion layer + target extractor) that subsumes audio/visual/spatial clue variants, and explicitly notes that TSE internally solves two sub-tasks (identify the target + estimate its speech), the same two sub-tasks that OVC/PSE later split asymmetrically (preserve-target vs. suppress-target). The survey also reports that direct TSE consistently outperforms the cascade BSS-then-speaker-ID alternative, especially in adverse conditions, and that multi-clue (audio-visual-spatial) attention fusion outperforms any single-clue system under clue corruption — both findings directly motivate the 2026 LGTSE/D-LGTSE focus on enrollment-conditioning robustness.

## Cross-Cutting Takeaways

1. **Progress is a Cartesian product, not a ladder.** A 2026 system picks one option per axis: target (DF/CCM), domain (hybrid loss), backbone (Mamba/linear RNN), efficiency technique (grouped + adaptive conv), multi-channel strategy (array-invariant), conditioning (PSE/OVC). The six axes are near-orthogonal, so most combinations are unexplored.
2. **Loss choice often dominates architecture choice.** Pandey & Wang 2019 (frequency loss for time-domain nets) and the DCCRN(SNR) variant both show that the training signal can outweigh backbone tweaks. PCEN-based mask thresholding ([[sources/liu-2025-pcen-mask-vad-speech-enhancement\|Liu 2025]]) and [[concepts/perceptual-contrast-stretching\|PCS]] post-processing extend this into the training-data / post-processing regime.
3. **The efficiency frontier is technique-composition, not model-shrinking.** GTCRN's 750× reduction is the product of four orthogonal techniques; CoFi-Lite and AdaptCRN extend it by adding path-decoupling and dynamic convolution rather than shrinking the backbone further.
4. **2026 inverts input-centric assumptions.** Output-based SE (evaluate outputs, not inputs) and array-invariant SE (condition on geometry, not array-specific SCM) both move the decision from the input side to the output / context side.

## Open Questions and Gaps

- **Generative vs discriminative on unseen-noise robustness** is not yet benchmarked head-to-head at matched MACs; the corpus suggests generative wins here but lacks a unified comparison.
- **Inplace-CRN + Mamba** is unexplored: SICRN uses S4ND as a *branch*, but a fully Mamba-based inplace CRN (channel-wise Mamba reused across frequency bins) is not in the corpus.
- **Array-invariant + personalized conditioning** (Geo-DConv + OVC/PSE) is the obvious multi-channel + conditioning combination but unpublished.
- **Sub-4 ms generative SE** remains impossible (1 NFE still costs more than one discriminative forward pass); the drifting-models trajectory is the closest approach.
- The 60-year survey's open challenges — sub-4 ms hearing-aid latency, theoretical interpretation of DL "black boxes", multitalker scenarios, subjective validation for hearing-impaired listeners — remain only partially addressed by the 2026 corpus.

## Related Synthesis

- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]] — BC/AC/IMU fusion (the modality axis, deferred)
- [[synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]] — BC integration evolution
- [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]] — task dissolution + latency tiers + linear-RNN replacement (the task/latency axis)
- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]] — ANC efficiency + RNN BPTT vs FEP memory bottlenecks

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]] — foundational concept
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the CRN template
- [[concepts/complex-ratio-mask|Complex Ratio Mask]] · [[concepts/complex-convolving-mask|Complex Convolving Mask]] · [[concepts/deep-filtering|Deep Filtering]] — target lineage
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]] · [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — domain choice
- [[concepts/dprnn|Dual-Path RNN]] · [[concepts/mp-senet|MP-SENet]] · [[concepts/semamba|SEMamba]] · [[concepts/mamba-mingru|Mamba-MinGRU]] · [[concepts/sse-net|SSE-Net]] — backbone lineage
- [[concepts/gtcrn|GTCRN]] · [[concepts/cofi-lite|CoFi-Lite]] · [[concepts/adaptcrn|AdaptCRN]] · [[concepts/igcrn|IGCRN]] · [[concepts/iccrn|ICCRN]] · [[concepts/sicrn|SICRN]] — efficiency frontier
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] · [[concepts/neural-beamforming|Neural Beamforming]] · [[concepts/array-invariant-speech-enhancement|Array-Invariant SE]] · [[concepts/geometry-aware-dynamic-convolution|Geo-DConv]] · [[concepts/output-based-speech-enhancement|Output-based SE]]
- [[concepts/personalized-speech-enhancement|Personalized SE]] · [[concepts/target-speaker-extraction|Target Speaker Extraction]] · [[concepts/own-voice-cancellation|Own-Voice Cancellation]] · [[concepts/prior-matching|Prior Matching]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech]] · [[concepts/drifting-models|Drifting Models]]
