---
type: synthesis
created: 2026-08-04
updated: 2026-11-08
sources:
  - raw/papers/boeddeker-2018-neural-mask-beamforming/full-text.md
  - raw/papers/erdogan-2016-improved-mvdr-mask-prediction/full-text.md
  - raw/papers/heymann-2016-neural-spectral-mask-beamforming/full-text.md
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
  - raw/papers/fu-2026-one-model-many-latencies/full-text.md
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
  - raw/papers/tesch-2023-insights-deep-nonlinear-filters/full-text.md
  - raw/papers/shetu-2026-generative-discriminative-comparison/full-text.md
  - raw/papers/li-2020-residual-noise-control/full-text.md
  - raw/papers/ke-2021-low-complexity-artificial-noise-suppression/full-text.md
  - raw/papers/zhao-2026-spectrally-adaptive-loss/full-text.md
  - raw/papers/wang-2021-magnitude-phase-compensation/full-text.md
  - raw/papers/li-2022-embedding-beamforming/full-text.md
  - raw/papers/zhang-2021-adl-mvdr/full-text.md
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
  - raw/papers/yan-2025-lisennet/full-text.md
  - raw/papers/haeb-umbach-2024-microphone-array-deep-learning/full-text.md
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
  - raw/papers/ahn-2026-fastenhancer/full-text.md
  - raw/papers/laroche-2026-lisenet-embedded/full-text.md
  - raw/papers/luo-2022-band-split-rnn/full-text.md
  - raw/papers/liu-2023-iccrn/full-text.md
  - raw/papers/zhao-2024-sicrn/full-text.md
  - raw/papers/wang-2025-adaptive-convolution-cnn-speech-enhancement/full-text.md
  - raw/papers/zhao-2025-lightweight-transformer/full-text.md
tags:
  - speech-enhancement
  - single-channel
  - deep-learning
  - neural-network-architecture
  - encoder-decoder
  - survey
  - evolution
  - low-latency
---

# Deep Speech Enhancement: Architectural & Methodological Evolution

> Cross-source synthesis tracing how deep learning for speech enhancement (SE) evolved from the 2018 Convolutional Recurrent Network to the 2026 SSM / array-invariant / generative frontier — along seven largely independent axes: training target, signal domain, backbone, efficiency, multi-channel integration, conditioning paradigm, and training paradigm (generative vs. discriminative).

## Scope and Relationship to Other Syntheses

"Deep speech enhancement" is the broad umbrella under which several specialized synthesis pages in this wiki sit. This page traces the **core architectural and methodological evolution** of the SE problem itself (denoising / separation / dereverberation via neural networks). It deliberately defers to the specialized syntheses for sub-topics:

- **Multi-modal fusion** (BC / AC / IMU) → [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]], [[synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]]
- **Joint multi-task (AEC+NS+DR+OVC+AHS) and sub-10 ms latency tiers** → [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]]
- **ANC computational efficiency / RNN memory bottlenecks** → [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]]

The thesis here is that the field's progress is **not a single replacement story** (e.g. "LSTM → Transformer") but the Cartesian product of seven near-orthogonal axes, each of which has its own frontier. A 2026 state-of-the-art system is built by picking one point on each axis.

A complementary way to read this page is as a **single-channel (single-microphone) dataflow walkthrough**: given one noisy signal, how do the insights compose into a concrete denoiser? The mapping:

| Dataflow layer | Decision | Treated in |
|----------------|----------|------------|
| ① Input representation | Time-domain waveform / STFT complex spectrum / perceptual-band (Bark/ERB) features | Insight 2 (domain), Insight 5 (band compression) |
| ② Output target & reconstruction | IBM→IRM→cIRM→complex mapping→CCM/DF; mask- vs mapping-style reconstruction | Insight 1, Insight 3 (decoupled output heads) |
| ③ Encoder / decoder | How frequency resolution is compressed and restored: symmetric U-Net / band merge-split / inplace no-downsampling / coarse-fine dual path / dual decoders | **Insight 4a** |
| ④ Backbone | LSTM/GRU → dual-path → Conformer → Mamba/SSM / linear RNN / SNN | Insight 4 |

The single-channel representative-model matrix consolidating all four layers appears after Insight 8.

## Sources Synthesized

| Source | Year | Axis advanced | Key contribution |
|--------|------|---------------|------------------|
| [[sources/wang-2018-supervised-speech-separation-deep-learning-overview\|Wang & Chen 2018]] | 2018 | Target | Survey codifying IBM/IRM/PSM/cIRM training targets for supervised separation |
| [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement\|Tan & Wang 2018 (CRN)]] | 2018 | Backbone | CED + LSTM, causal convolutions; the foundational deep SE architecture (17.58M params) |
| [[sources/erdogan-2016-improved-mvdr-mask-prediction\|Erdogan, Hershey, Watanabe, Mandel & Le Roux 2016]] | 2016 | Multi-channel | Concurrent founding paper of mask-based beamforming: single-channel LSTM masks (MSA loss, CHiME-3 CH5 training) drive the noise SCM of the statistics-only Souden-form MVDR — no steering vector or array geometry; single max-combined mask beats per-channel multi-masks; beats WDAS on mismatched-ASR WER |
| [[sources/heymann-2016-neural-spectral-mask-beamforming\|Heymann, Drude & Haeb-Umbach 2016]] | 2016 | Multi-channel | The original mask→PSD→GEV front-end: shared-weight per-channel BLSTMs estimate T-F masks from single-channel magnitudes (array-configuration-independent training), mask-weighted PSD accumulation feeds GEV+BAN/MVDR; GEV beats MVDR by avoiding explicit inversion of the sparsely-supported noise PSD; noise-aware IBM training halves CHiME-3 WER — phase-1 hybrid before end-to-end took over |
| [[sources/boeddeker-2018-neural-mask-beamforming\|Boeddeker et al. 2018]] | 2018 | Multi-channel / training objective | Feature-level LogMel MSE backpropagated through the differentiable mask-based MVDR/GEV beamformer: optimizing DNN masks for downstream ASR features beats mask-level BCE by ~8% rel WER; robustness across arrays, acoustic models, and online operation |
| [[sources/pandey-2019-cnn-speech-enhancement-time-domain\|Pandey & Wang 2019 (AECNN)]] | 2019 | Domain | Time-domain U-Net trained with STFT-magnitude loss → frequency-loss-for-time-domain-nets paradigm |
| [[sources/li-2020-residual-noise-control\|Li et al. 2020 (GL)]] | 2020 | Training objective | [[concepts/generalized-loss-function\|Generalized loss]] with residual noise control; MSE / components loss as special cases; same-net four-loss comparison with subjective validation |
| [[sources/ke-2021-low-complexity-artificial-noise-suppression\|Ke et al. 2021 (ANS)]] | 2021 | Post-processing | Classical MMSE/SPP postfilter on the DNN output suppressing [[concepts/artificial-residual-noise\|artificial residual noise]] — three SPP strategies at 0.0098–0.016 MFLOPs/frame |
| [[sources/li-2022-embedding-beamforming\|Li et al. 2022 (EaBNet)]] | 2022 | Multi-channel | All-neural causal framewise beamformer: implicit spectral-spatial embedding replaces explicit SCM; surpasses oracle-mask MVDR |
| [[sources/wang-2021-magnitude-phase-compensation\|Wang, Wichern & Le Roux 2021]] | 2021 | Training objective (theory) | Names and formulates the [[concepts/magnitude-phase-compensation-effect\|magnitude–phase compensation effect]]; explains why magnitude losses improve perceptual metrics in RI/waveform losses |
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
| [[sources/yan-2025-lisennet\|Yan et al. 2025 (LiSenNet)]] | 2025 | Efficiency | Sub-band conv + causal dual-path GRU + noise detector; 37k params / 56M MACs/s, PESQ 3.07 VBD |
| [[sources/liu-2026-array-invariant-speech-enhancement\|Liu et al. 2026 (Geo-DConv)]] | 2026 | Multi-channel | Geometry-conditioned dynamic conv → array-invariant SE backbones |
| [[sources/uphaus-2026-directivity-low-latency\|Uphaus et al. 2026 (FiLM-OSN)]] | 2026 | Multi-channel | Directivity-conditioned low-latency (10 ms) binaural NDF for hearing aids — FiLM steering of a Mamba-based OSN backbone |
| [[sources/apostolidis-2026-listen-first-output-based-multi-microphone\|Apostolidis 2026]] | 2026 | Multi-channel | Output-based SE: select MPDR output by Glimpse Proportion, not input features |
| [[sources/ostergaard-2026-own-voice-cancellation\|Østergaard et al. 2026 (OVC)]] | 2026 | Conditioning | Inverts PSE: remove the enrolled speaker; Mamba-MinGRU at 2 ms |
| [[sources/shetu-2026-munet\|Shetu et al. 2026 (μNet)]] | 2026 | Efficiency | 46K params / 90 KB static / int8 on HiFi 4 DSP; 4–16 ms latency; [[concepts/noise-attenuation-control\|noise attenuation control]] |
| [[sources/shetu-2026-generative-discriminative-comparison\|Shetu, Habets & Brendel 2026]] | 2026 | Training paradigm | 14-model controlled comparison of discriminative / GAN / diffusion training; same NCSN++ backbone under three objectives |
| [[sources/pan-2025-data-driven-acoustics\|Pan 2025]] | 2025 | Training objective (taxonomy) | Tutorial framing SE as *estimation*; three-level loss hierarchy (filter gain → spectrum → waveform) with SI-SDR–correlation equivalence |
| [[sources/haeb-umbach-2024-microphone-array-deep-learning\|Haeb-Umbach et al. 2024]] | 2024 | Multi-channel (taxonomy) | IEEE SPM overview codifying the model-based/data-driven hybrid landscape: two-operation framing (parameter estimation + enhancement operation), three hybrid classes, and the model-as-regularizer argument |
| [[sources/veluri-2023-semantic-hearing\|Veluri et al. 2023]] | 2023 | Multi-channel / conditioning / efficiency | First binaural target *sound* extraction network — joint two-channel latent masking, class-query conditioning, 0.52M params / 240 MFLOPS / 6.56 ms on smartphone |
| [[sources/ahn-2026-fastenhancer\|Ahn, Han, Woo & Kim 2026 (FastEnhancer)]] | 2026 | Efficiency | RTF-first streaming SE: RNNFormer (time GRU + freq MHSA), time-kernel-1 convs, BN fusion — PESQ 3.13 at RTF 0.022; proves MACs ≠ real speed |
| [[sources/laroche-2026-lisenet-embedded\|Laroche & Olsson 2026 (LiSenNet-NPU)]] | 2026 | Efficiency | NPU-redesigned LiSenNet for STM32N6: static int8 graph, int8 PESQ 3.01 at 4.83 ms/frame; operator set + streaming state as co-design axes |
| [[sources/zhao-2025-lightweight-transformer\|Zhao & Madhu 2025 (LCT-GAN)]] | 2025 | Backbone ordering / efficiency | Sweeps 8 temporal-spectral bottleneck orderings at matched MACs → FTF (freq-time-freq) is the knee; cross-axis parameter sharing + 1 s-capped causal attention yield 0.14 M params / 0.35 G MAC/s at PESQ 3.06 |
| [[sources/fu-2026-one-model-many-latencies\|Fu et al. 2026 (Real-time RE-USE)]] | 2026 | Latency | Makes latency a runtime variable: 30 configurations (look-ahead 0–2 × exit depth 3–12) from one 3.7M-param TF-Mamba checkpoint; 40–80 ms algorithmic, 10–25 ms compute |

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

The decisive observation came from [[sources/pandey-2019-cnn-speech-enhancement-time-domain\|Pandey & Wang 2019]]: a time-domain AECNN trained with **STFT-magnitude MAE loss** outperforms the same network trained with waveform loss, and beats SEGAN/GRN on TIMIT/IEEE/WSJ0. Spectral losses provide a dramatically better perceptual training signal than waveform losses. The [[concepts/complex-spectrum-mapping\|complex STFT (RI) loss]] variant is best for SI-SDR. The **mechanistic explanation** came later from [[sources/wang-2021-magnitude-phase-compensation\|Wang, Wichern & Le Roux 2021]]: a purely waveform-domain loss lets the estimated magnitude compensate for phase errors — which SI-SDR rewards but PESQ/eSTOI/WER punish — so adding a magnitude term trades a little SI-SDR for large perceptual gains (on SMS-WSJ, Wav vs. Wav+Mag: PESQ 1.79 → 2.07, WER 47.5 → 39.2%, SI-SDR 4.22 → 3.42 dB).

The 60-year survey ([[sources/zheng-2023-survey-frequency-domain-speech-enhancement|Zheng 2023]]) notes the field historically invested more research effort in frequency-domain methods, partly explaining their lead — but the convergence is now clear: modern systems use **time-domain or learned-encoder representations with multi-resolution STFT / RI losses**, and the choice of loss often matters more than minor architecture changes (the DCCRN(SNR) variant demonstrates loss choice outweighing architecture tweaks).

A complementary early data point: [[sources/li-2020-residual-noise-control|Li et al. 2020]] trained one 0.59M causal U-Net under four objectives (MSE, TMSE, SI-SDR, and their [[concepts/generalized-loss-function|generalized loss]] with residual noise control). The objective metrics and the listeners disagreed: SI-SDR loss achieved the best SDR but a PESQ below even plain MSE, while the residual-noise-controlled loss — only *comparable* on objective scores — won ~70% of pairwise preferences, because MSE-style objectives drive residual noise to zero and leave unnatural artifacts that the metrics miss. Two refinements follow: (i) loss choice dominates not only architecture but also *metric optimization* — each loss optimizes its own metric and degrades the others; (ii) PESQ/SDR are blind to the residual-noise-naturalness failure mode, which is exactly the axis the noise-shaping loss family (and later inference-time NAL, see [[concepts/noise-attenuation-control|Noise Attenuation Control]]) targets.

[[sources/ke-2021-low-complexity-artificial-noise-suppression|Ke et al. 2021]] — the same CAS group — supply the inference-time *classical* counterpart: a psychoacoustic model shows the [[concepts/artificial-residual-noise|artificial residual noise]] of four MSE-trained front-ends exceeds the speech masking threshold by 10–50 dB, and an MMSE noise-PSD postfilter with three re-designed SPP inputs (from the noisy spectrum, from the DNN gain, from a sigmoid of the PSD ratio) removes it at 0.0098–0.016 MFLOPs/frame — again with >60% AB preference far out of proportion to the modest PESQ/segSNR gains. The residual-noise-control design space is thereby mapped at three points: training-time loss (Li 2020), inference-time statistical postfilter (Ke 2021), and inference-time NAL mixing (Shetu 2026).

## Insight 3: The Magnitude–Phase "Compensation Effect" Drove Architectural Decoupling

[[sources/zheng-2023-survey-frequency-domain-speech-enhancement\|Zheng 2023]] crystallizes a recurring failure mode of single-stage complex-spectrum networks: a **compensation effect** where magnitude distortion is traded for phase recovery (and vice versa) within one shared decoder. The effect was in fact named and formulated two years earlier by [[sources/wang-2021-magnitude-phase-compensation\|Wang, Wichern & Le Roux 2021]], who traced it to the projection geometry of complex-/time-domain losses (the estimated magnitude slides toward the projection of the clean spectrum onto the estimated-phase direction, reaching zero at π/2 phase error) and diagnosed it with the [[concepts/magnitude-phase-snr\|mSNR/pSNR]] decomposition — establishing that PESQ/eSTOI/WER track magnitude accuracy while SI-SDR tracks the compensated signal. The architecture response was **decoupling**:

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

**Ordering is an axis, not a detail (Zhao & Madhu 2025).** The DPRNN lineage raised the question of *whether* to model both axes; [[sources/zhao-2025-lightweight-transformer|LCT-GAN]]'s ablation answers *in which order* and *how many stages*, at matched MACs and parameters: TT 2.18 → FF 2.34 → TF 2.55 → FT 2.57 → TFT 2.62 → **FTF 2.68** PESQ, with a fourth stage flat (TFTF 2.68, FTFT 2.69). Three findings that no other source in this corpus isolates: (i) frequency-first beats time-first at equal cost — the time stage should operate on spectrally coherent input; (ii) frequency modelling buys PESQ/STOI/SI-SDR/BAK while time modelling buys SIG, i.e. the two axes trade *different* perceptual errors, which is why neither alone suffices; (iii) three stages is the knee, so "more interleaving" is not a free quality knob. The block also shows the cheapest route to attention in a lightweight model is not operator substitution but **parameter sharing along the unmodelled axis** — the time transformer's GRU runs with frequency as the batch axis, cutting the CRUSE GRU bottleneck's parameters by 98% and MACs by 27%.

## Insight 4a: Encoder/Decoder Designs — Four Philosophies of Frequency-Resolution Handling

The backbone succession above says nothing about *what* the sequence model reads and writes — the encoder/decoder that maps the T-F domain into the feature space and back. Single-channel designs cluster into four philosophies:

### Template: the CRN symmetric encoder–decoder (Tan & Wang 2018)

Convolutional encoder (frequency halved per layer, channels doubled) → recurrent bottleneck → transposed-convolution decoder whose final layer is **linear** (no activation) → U-Net skip connections preserving fine spectral detail (especially phase). Causality via past-only asymmetric padding; ELU preferred over ReLU because spectra contain negative values. See [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]].

### Lineage A — Band-compressed encode, band-split decode ("compress then restore")

- **GTCRN** ([[concepts/gtcrn|GTCRN]]): Band Merging before the encoder (192 high-frequency bins → 64 ERB bands; 65 low-frequency bins kept uncompressed = 129-dim), Band Splitting after the decoder; SFE modules on the skip connections enhance frequency information.
- **CoFi-Lite** ([[concepts/cofi-lite|CoFi-Lite]]): decouples spectral modeling into parallel **coarse** (full-band envelope, ×16 compression) and **fine** (below-2 kHz detail, ×2 compression) paths bridged by Cross-Path Fusion — *more* parameters (83K vs 24K) but 40% of the MACs, and better quality.
- **DeepFilterNet**: two stages inside one network — an ERB encoder/decoder (32 bands) predicts real-valued envelope gains, while a deep-filter head estimates per-bin complex FIR coefficients only up to $f_{DF}$ (periodic components concentrate at low frequencies); grouped linear/GRU layers enforce sparsity.

### Lineage B — Inplace, no downsampling ("preserve per-bin resolution")

The [[concepts/igcrn|IGCRN]] → [[concepts/iccrn|ICCRN]] → [[concepts/sicrn|SICRN]] family: stride-1 frequency-axis convolutions plus a channel-wise LSTM (hidden 64, not 1024) reused across all frequency bins. The frequency axis is never downsampled; IGCRN's downsampling ablation shows the *inplace characteristic*, not capacity, drives performance.

### Lineage C — Non-uniform band allocation ("spend resolution where the signal is")

- **BSRNN** ([[concepts/band-split-rnn|Band-Split RNN]]): signal-specific non-uniform bandwidths; for vocals, splitting only below 1 kHz into 100 Hz bands lifts uSDR from ~8.2 to 9.51 dB. Per-band norm + FC; dual-path modeling unfolded over (time × band).
- **LiSenNet** ([[concepts/lisennet|LiSenNet]]): no merging module at all — [[concepts/sub-band-convolution|sub-band striding]] (stride 1 low, stride 3 high) preserves low-frequency resolution *by construction*.
- **Sub-band + full-band division of labor** ([[concepts/sub-band-full-band-architecture|Kuang 2025]]): 32 ERB sub-band gains (coarse envelope) + full-band N=3 deep filtering (fine suppression) in separate encoder-decoder sets.

### Lineage D — Decoupled output heads (decoder-level compensation-effect fix)

- **MP-SENet / SEMamba**: after the TF blocks, *two separate decoders* — magnitude and phase — each a dilated DenseNet + deconvolution + 2D-conv head. The dual-decoder template carries the architectural decoupling of Insight 3 down to the decoder level.
- **CTSNet / G2Net / TaylorSENet**: magnitude path + residual-complex path as two output heads.

### Counterexample: discard the frequency-domain codec entirely

Time-domain systems (Conv-TasNet lineage, OVC) use a **learned 1-D convolutional encoder** + masking network + convolutional decoder, bypassing the STFT and its window-length latency; OVC reaches 2 ms with kernel L=32 at 16 kHz. The [[concepts/asymmetric-stft|asymmetric STFT]] (RT-Tango) keeps the STFT but shortens analysis-vs-synthesis windows to reach 8 ms.

**Cross-lineage principle**: low-frequency resolution deserves explicit design — BSRNN's 100 Hz low bands, LiSenNet's stride-1 low bands, GTCRN's 65 uncompressed low bins, and DeepFilterNet's low-frequency-only deep filtering are four engineering expressions of the same prior (F0 and the first harmonics live at low frequencies).

## Insight 5: The Efficiency Frontier Moved ~1000× via Four Orthogonal Techniques

Parameter counts for competitive monaural SE collapsed from ~18M (CRN, 2018) to 23.7K (GTCRN, 2024) — roughly 750× — and compute kept falling through 2026. The collapse is the product of four largely independent techniques:

| Technique | Mechanism | Origin / exemplar |
|-----------|-----------|-------------------|
| Perceptual band compression | ERB / Bark-scale feature reduction (e.g. 192→64 bands) | DeepFilterNet, GTCRN, PercepNet, [[concepts/sub-band-convolution|LiSenNet's sub-band striding]] |
| Grouped conv + grouped RNN | Split channels / hidden states into groups; ShuffleNet-style units | [[concepts/gtcrn\|GTCRN]] (G-DPRNN), [[concepts/cofi-lite\|CoFi-Lite]] |
| Inplace convolution | Stride-1 freq-axis conv + channel-wise LSTM reused across bins | [[concepts/igcrn\|IGCRN]] → [[concepts/iccrn\|ICCRN]] → [[concepts/sicrn\|SICRN]] |
| Adaptive (dynamic) convolution | Frame-wise kernels conditioned on input | [[concepts/adaptcrn\|AdaptCRN]] (135K params, PESQ 2.98) |

The **inplace-CRN family** is its own lineage: [[concepts/igcrn\|IGCRN]] (2021, 1.4M, the founder) → [[concepts/iccrn\|ICCRN]] (2023, 0.46M, cepstral-space branch) → [[concepts/sicrn\|SICRN]] (2024, 2.16M, S4ND global branch). The throughline is preserving **per-bin spatial cues** via channel-wise LSTM (hidden 64 vs the conventional 1024) — IGCRN's downsampling ablation shows the inplace characteristic, not capacity, drives multi-channel SE performance.

The 2026 efficiency frontier is **CoFi-Lite** ([[sources/yang-2026-cofi-lite-ultra-lightweight-speech-enhancement\|Yang 2026]]): it reuses GTCRN's ERB/SFE/TRA machinery but decouples spectral modeling into parallel coarse (full-band envelope, ×16 compression) and fine (low-frequency detail below 2 kHz, ×2 compression) paths bridged by Cross-Path Fusion. It **outperforms GTCRN** (PESQ 2.16 vs. 2.07 on DNS3) at 40% of its MACs (12.87M vs. 31.97M MACs/s) — trading a higher parameter count (83K vs. 24K) for drastically lower compute. The same lab lineage (GTCRN → CoFi-Lite → AdaptCRN) shows the techniques compose.

Between GTCRN (2024) and CoFi-Lite (2026) sits **LiSenNet** ([[sources/yan-2025-lisennet\|Yan et al. 2025]], ICASSP): 37k params / 56M MACs/s at PESQ 3.07 on VoiceBank+DEMAND — beating FSPEN's PESQ by 0.10 with 47% of its parameters. Its distinctive techniques along the axis above: [[concepts/sub-band-convolution|sub-band convolutions]] (stride 1 below, stride 3 above — low-frequency resolution preserved by construction rather than by an ERB merging module), a [[concepts/convglu|ConvGLU]] channel mixer compensating tiny GRU states in a causal dual-path bottleneck, and — uniquely in the corpus — a [[concepts/noise-detector|noise detector]] front-end that makes compute *proportional to noise content* (15–70M MACs/s). LiSenNet subsequently became the standard second baseline (beside GTCRN) for 2026 lightweight-SE evaluations (AdaptCRN, CoFi-Lite, HALO, μNet) — and the subject of a deployment-study sequel: [[sources/laroche-2026-lisenet-embedded\|Laroche & Olsson 2026]] redesigned it for the STM32N6 Neural-ART NPU, replacing the dual-path GRU with convolutional mixers and every unsupported operator with NPU-compatible ones ([[concepts/lisennet-npu\|LiSenNet-NPU]]) — *raising* int8 PESQ from 2.93 to 3.01 at 4.83 ms/frame, i.e., the deployment redesign is free-to-positive in quality on this benchmark.

A second life for these ultralight models: [[sources/huang-2026-lightweight-speech-enhancement-guided-target-speech-extraction\|Huang 2026 (LGTSE)]] reuses GTCRN not as a standalone enhancer but as a **pluggable denoiser front-end** for target speech extraction, adding negligible overhead (6.08M → 6.13M params) while delivering +0.89 dB SI-SDR.

The efficiency frontier also has a **deployment axis** that params/MACs tables hide: [[concepts/munet\|μNet (Shetu 2026)]] argues that once a model must run int8-quantized on a consumer DSP (Cadence Tensilica HiFi 4), the binding constraints become static memory (μNet: 90 KB) and memory-access patterns, not MAC counts. μNet *reverts* ULCNet's depthwise separable convolutions to standard convolutions precisely because fragmented memory access makes "cheaper" convolutions slower in wall-clock DSP cycles — the inverse of the DSConv2D choice in the lightS4 line, showing that the right convolution type is target-hardware-dependent, not a universal constant.

[[sources/ahn-2026-fastenhancer\|FastEnhancer (Ahn 2026)]] generalizes that deployment argument from the DSP tier to the **single-CPU-thread tier** and turns it into the primary optimization target: its entire architecture — time-axis kernel size 1 (no frame caching), BN fused at inference, fixed filterbank bridges, and the [[concepts/rnnformer\|RNNFormer]] bottleneck (time GRU + frequency MHSA) — is chosen to minimize RTF, accepting *more* MACs (FastEnhancer-B: 262M vs GTCRN's 40M) in exchange for 3× lower wall-clock latency and better quality (PESQ 3.13 vs 2.87 on Voicebank-Demand). The μNet finding (memory-access patterns beat MAC counts on DSP) and the FastEnhancer finding (memory operations beat MAC counts on CPU) are the same lesson measured on two hardware tiers — and [[sources/laroche-2026-lisenet-embedded\|Laroche & Olsson 2026]] add the third tier, the MCU **NPU**: there the binding constraint is the *operator set* (recurrence, runtime normalization, and rank-5 reshapes compile away or stall; unsupported ops fall back to the host CPU whose overheads dominate), plus a state-computation trade-off — convolutional FIFO state costs 200× fewer MACs than receptive-field recomputation but its 154 KiB exceeds the 45 KiB weights (see [[concepts/mcu-npu-deployment\|MCU NPU Deployment]] and [[concepts/stateful-streaming-inference\|stateful streaming inference]]). Params/MACs tables are deployment-blind on all three tiers, and the 2026 frontier is a *measured RTF curve* (FastEnhancer T–L spans RTF 0.012–0.313 on Xeon), not a complexity point.

**Latency becomes a model dimension (Fu et al. 2026).** Every system above fixes one operating point, so a deployment with a different budget needs a retrained model — the frontier is drawn as a *set* of models. [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026]] collapse that set into one checkpoint: [[concepts/parallel-look-ahead-convolutions|parallel look-ahead conv branches]] set algorithmic latency (40/60/80 ms) and [[concepts/early-exit-speech-enhancement|exit depth]] sets computational latency (2.0M–3.7M params, 10.09–25.05 ms/frame on an A100), giving 30 configurations that prune to a specialized-size sub-graph once the budget is chosen. Two results sharpen the rest of this synthesis: (i) the deepest 12-block configuration runs at RTF 1.25 for a 20 ms hop, so **a good params/MACs point does not imply real-time operation** — the FastEnhancer MACs-vs-RTF inversion restated as the hard constraint $l_{\text{Compute}} \le h$; and (ii) depth and look-ahead are not interchangeable — extra depth raises UTMOS, whereas one look-ahead frame delivers nearly all the available ASR-accuracy gain and a second frame almost none. The frontier has a third coordinate (latency budget) in which the *allocation* between look-ahead and depth, not the total, decides downstream performance.

## Insight 6: Multi-Channel SE Went "Estimate SCM → Beamform" → End-to-End → Array-Invariant

The multi-channel arc has three phases, each relaxing an assumption of the previous:

1. **Hybrid DNN-guided linear filters** — [[sources/oviste-2026-neural-vslf-speech-enhancement|Neural VSLF (Oviste 2026)]]: a DNN predicts clean-speech SCM, noise SCM, and a distortion/noise tradeoff parameter, then classical [[concepts/variable-span-linear-filter|VSLF]] weights are computed (MWF/MVDR are special cases). Interpretable, controllable, but array-specific.
2. **End-to-end neural beamforming** — [[concepts/neural-beamforming|neural beamformers]] and [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel 2026]]'s linearly-constrained deep beamformer learn the whole filter via differentiable constraint losses, outperforming LCMV. Highest quality, but bound to one array geometry. The earliest decisive evidence for this phase is [[sources/li-2022-embedding-beamforming|Li et al. 2022 (EaBNet)]]: a causal framewise beamformer whose learned spectral-spatial embedding skips SCM computation entirely and *surpasses an oracle-IRM MB-MVDR* (avg. PESQ 3.52 vs. 3.10 on a 9-channel DNS setup) at 2.84M params — and whose EaBNet* ablation shows that *reinserting* explicit SCM computation from predicted masks degrades results, pinning the tandem scheme's bottleneck on the statistical stage itself rather than on mask-estimation error.
3. **Array-invariant conditioning** — [[sources/liu-2026-array-invariant-speech-enhancement|Geo-DConv (Liu 2026)]]: a universal front-end (Geo-DConv + [[concepts/topology-aware-coordinate-transformer|TACT]]) converts *any* fixed-array SE backbone (SpatialNet, TF-GridNet) into an array-invariant system by generating geometry-specific convolution kernels from microphone coordinates. It matches USES2-comp quality at ~10× lower MACs and **zero-shot generalizes to CHiME-4**.

The conceptual move from phase 2 to phase 3 is from "learn the beamformer" to "condition a backbone on geometry." A parallel reframing appears in [[sources/apostolidis-2026-listen-first-output-based-multi-microphone\|Apostolidis 2026]]'s [[concepts/output-based-speech-enhancement\|output-based SE]]: instead of extracting features from the noisy input to predict a filter, evaluate the SI/SQ of *candidate outputs* and select the best — outperforming input-based MVDR especially at low SNR. Both 2026 works invert a long-standing assumption: the relevant signal is the *output* (or the geometry), not the input spectrum.

**The taxonomy that names this arc (Haeb-Umbach et al. 2024)**: the multi-channel phases above receive their canonical formulation in [[sources/haeb-umbach-2024-microphone-array-deep-learning|Haeb-Umbach et al. 2024]]'s IEEE SPM overview — the two-operation framing (every enhancement system = parameter estimation + enhancement operation) and a three-class hybrid taxonomy: Class 1, data-driven parameter estimation for model-based enhancement (Neural VSLF; [[concepts/weighted-prediction-error|WPE]] with neural PSD estimates); Class 2, combined model-based + data-driven estimation ([[concepts/guided-source-separation|GSS]]'s diarization-constrained EM); Class 3, joint enhancement ([[concepts/tf-gridnet|TF-GridNet]]'s DNN–BF–DNN). The overview also supplies both theoretical bookends of the arc: MVDR is a *sufficient statistic* when the noise is Gaussian (Balan & Rosca 2002) — the formal sense in which phase-1 hybrids lose nothing — while non-Gaussian distortions (reverberation, interfering speech) make the optimal filter a non-decomposable nonlinear MMSE estimator, the regime where phase-2/3 end-to-end networks win. Its **model-as-regularizer** argument — classical structure keeps data-driven components within physically reasonable behavior on unexpected inputs — explains why hybrid systems keep outperforming their end-to-end rivals in deployment and robustness studies (Sun 2024's real-world transfer; R-MWF's no-DNN win) even when benchmarks favor all-neural systems. See [[concepts/hybrid-speech-enhancement|Hybrid Speech Enhancement]].

A complementary datapoint on *how* to wire the channels together comes from [[sources/veluri-2023-semantic-hearing\|Veluri et al. 2023]]'s binaural target sound extraction: mapping both ears into a **shared latent representation** with one mask estimator (dual-channel) matches parallel per-channel branches with cross-communication (Han et al. 2020) on SI-SNRi and ΔITD, beats them on ΔILD (0.88 vs 1.08 dB — the shared representation preserves inter-channel amplitude relations), and halves runtime (6.56 vs 13.35 ms). They also show that the *loss* must be channel-aware: the scale-sensitive SNR loss averaged over L/R prevents the inter-channel gain collapse that SI-SNR-containing losses permit (their Conv-TasNet baseline's ΔILD diverged to infinity). The lesson for end-to-end multi-channel SE: the channel-fusion topology and the scale sensitivity of the loss jointly determine whether spatial cues survive.

**The phase-1→2 transition began at the training criterion, not the structure (Boeddeker 2018)**: phase 1 itself — the Class-1 hybrid of NN masks → PSD statistics → GEV/MVDR beamformer — originates with [[sources/heymann-2016-neural-spectral-mask-beamforming|Heymann, Drude & Haeb-Umbach 2016]]: per-channel BLSTMs with shared weights and single-channel magnitude input (making training array-configuration-independent) estimate speech/noise masks whose weighted PSD accumulation feeds GEV+BAN; the paper's condition-number analysis showed GEV consistently beats MVDR because sparse masks make the explicitly-inverted noise PSD matrix ill-conditioned, and its noise-aware IBM training (vs. clean-speech-only) halved CHiME-3 WER — establishing the mask-statistics-filter decomposition and its training-target question that Boeddeker 2018 would reopen. The phase-1 origin is concurrent: [[sources/erdogan-2016-improved-mvdr-mask-prediction|Erdogan et al. 2016]] (independently and in the same year) instead drive the **statistics-only (Souden-form) MVDR** from a single max-combined LSTM mask — no speech SCM, no steering vector, no array geometry — and show that a single shared mask beats per-channel multi-masks precisely because partially-observed spatial vectors destabilize the noise SCM; their MSA loss (vs. Heymann's mask-approximation training) is the first training-objective fork in the mask-based beamforming line. Although the phases above are exemplified by 2021–2026 systems, [[sources/boeddeker-2018-neural-mask-beamforming\|Boeddeker et al. 2018]] already blurred the phase-1/phase-2 boundary from the loss side: keeping the model-based MVDR/GEV beamformer intact, they backpropagated **through the differentiable beamforming operation** (complex-valued algorithmic differentiation) to train the mask NN on an **ASR-feature-level MSE** (normalized log-mel of the beamformed signal vs. clean reference) — ~8% relative WER better than the mask-level BCE loss, because the mask NN is optimized for what the recognizer consumes rather than for mask fidelity. This is end-to-end optimization of a model-based filter four years before all-neural beamformers (EaBNet) removed the filter structure itself — evidence that the *criterion* moved "downstream" before the *architecture* did. The same paper supplies phase 1's commercial-scale robustness evidence: the CHiME-3-trained mask NN transfers across two microphone arrays, two large-data acoustic models, and a real conference room with moving speakers, and its online (frame-level/segment-level) variants retain most of the offline gain.

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

[[sources/shetu-2026-generative-discriminative-comparison\|Shetu, Habets & Brendel 2026]] sharpen this picture with the first controlled training-paradigm comparison (14 models, ~1000-h DNS-derived data, matched high/low-SNR and mismatched conditions, the same NCSN++ backbone trained with diffusion, GAN, and discriminative objectives). Their findings split the "generative" category: **single-step GAN training is the robustness + efficiency sweet spot** — NCSN++ (GAN) beats every diffusion/flow/consistency model on PESQ, SI-SDR, and FwSegSNR in matched *and* mismatched low-SNR conditions, trains in ~250k steps vs ~400k for diffusion, peaks with 50 h of data vs ≥200 h, and costs 60–100× fewer GMACs than iterative diffusion — while diffusion's only wins are DNSMOS (a generative-quality proxy) and comparable ΔSI-SDR. The training objective, not the backbone, drives the gains; because noise-reduction SE is strongly conditioned on $\mathbf{y}$, the iterative generative machinery buys nothing measurable, and the authors expect diffusion to pay off only where conditioning is weak (synthesis, bandwidth extension). On the hallucination side (WER/CER/LPS), generative methods stay close to the noisy reference at moderate SNR but hallucinate below -7 dB — see [[concepts/speech-enhancement-hallucination\|Speech Enhancement Hallucination]] and [[concepts/generative-vs-discriminative-speech-enhancement\|Generative vs. Discriminative Speech Enhancement]].

## Insight 8: Personalization Reframed as Enrollment-Conditioned Extraction — and Its Complement

Conditioning SE on a speaker embedding has bifurcated into two complementary tasks sharing the same machinery:

- **[[concepts/personalized-speech-enhancement\|PSE]]** — preserve the enrolled speaker, suppress the rest.
- **[[concepts/target-speaker-extraction\|Target Speech Extraction (TSE)]]** — extract the enrolled speaker from a mixture (LGTSE/D-LGTSE reuse GTCRN as the conditioning front-end).
- **[[concepts/own-voice-cancellation\|Own-Voice Cancellation (OVC)]]** — *invert* PSE: remove the enrolled (self) speaker, preserve everyone else.

[[sources/ostergaard-2026-own-voice-cancellation\|OVC (Østergaard 2026)]] makes the complementarity explicit — the same [[concepts/td-speakerbeam\|TD-SpeakerBeam]] / [[concepts/mamba-mingru\|Mamba-MinGRU]] conditioning runs forward (PSE) and backward (OVC), differing only in the objective. The conditioning signal itself is the hard part: [[sources/zhu-2026-g-map-se-guided-speech-enhancement\|G-MaP-SE (Zhu 2026)]] shows that **noisy enrollment embeddings** degrade PSE, and fixes it with GMM-based [[concepts/prior-matching\|prior matching]] to refine the embedding before conditioning (+0.03 WB-PESQ over noisy conditioning on DNS2020 at 0.025M added params). The lesson generalizes: in enrollment-conditioned SE, the *quality of the embedding* is as decisive as the enhancement backbone.

The canonical survey for the TSE half of this complementarity is [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023 (IEEE SPM)]]: it factors TSE into a single framework (clue encoder + mixture encoder + fusion layer + target extractor) that subsumes audio/visual/spatial clue variants, and explicitly notes that TSE internally solves two sub-tasks (identify the target + estimate its speech), the same two sub-tasks that OVC/PSE later split asymmetrically (preserve-target vs. suppress-target). The survey also reports that direct TSE consistently outperforms the cascade BSS-then-speaker-ID alternative, especially in adverse conditions, and that multi-clue (audio-visual-spatial) attention fusion outperforms any single-clue system under clue corruption — both findings directly motivate the 2026 LGTSE/D-LGTSE focus on enrollment-conditioning robustness.

The clue axis also extends beyond speakers: [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023]] condition extraction on a **sound-class query** (one-hot over 20 classes) rather than an enrollment embedding, and demonstrate the same preserve/suppress asymmetry operationally — for a speech target mixed with impulsive interference, *extracting the interference and subtracting it* beat extracting the speech directly by 0.91 MOS (avoiding over-attenuation dips), the class-query analog of OVC's inversion.

## The Single-Channel Representative-Model Matrix

Consolidating the four dataflow layers (input / output target / encoder-decoder / backbone) for the corpus's representative monaural denoisers:

| Model (year) | Input | Output target | Encoder/decoder | Backbone | Scale / latency |
|---|---|---|---|---|---|
| CRN (2018) | Complex STFT (RI) | cRM | CED + transposed conv + skips | LSTM bottleneck | 17.58M |
| DPCRN (2021) | Complex spectrum | Mask | Symmetric conv codec | Dual-path RNN | **0.72M / 0.77 GMAC/s** |
| DeepFilterNet (2022) | ERB bands + complex (≤ f_DF) | ERB gains + Deep Filtering (N-th-order complex FIR) | ERB codec + DF head | Grouped conv/GRU | Ultralight; multi-latency |
| MP-SENet (2023) | log1p magnitude + phase | Magnitude + phase (**dual decoders**) | DenseNet encoder + dual decoders | Conformer TF blocks | ~2.6M |
| GTCRN (2024) | ERB-compressed 64 bands | cRM | Band-Merge/GT-Conv + Band-Split | G-DPRNN (grouped dual-path GRU) | **23.7K / 39.6 MMAC/s** |
| LiSenNet (2025) | Sub-band-strided spectrum | Mask | Sub-band conv codec | Causal dual-path GRU + noise detector | 37k / 56M; PESQ 3.07 |
| LCT-GAN (2025) | Compressed magnitude ($c=0.3$) | Compressed real IRM | 3-layer causal conv codec | **FTF transformers** (freq Bi-GRU+MHA / time shared GRU+MHA / freq) | **0.14M / 0.35 GMAC/s**; PESQ 3.06 (3.20 +PCS); 32 ms |
| CoFi-Lite (2026) | Coarse/fine dual-path spectrum | Mask | Coarse (×16) / fine (×2) + CPF | GTCRN-style | 83K / **12.87M MACs/s** |
| AdaptCRN (2025) | ERB-compressed spectrum | Mask | ConvNeXt/StarNet-style codec | Grouped DPRNN + dynamic conv | 135K / 41 MMAC/s |
| SEMamba (2024) | log1p magnitude + phase | Magnitude + phase (dual decoders) | DenseNet + dual decoders | **TF-Mamba** | SOTA PESQ **3.69** (+PCS) |
| FastEnhancer-B (2026) | ERB spectrum | Mask | Time-kernel-1 conv + BN fusion | RNNFormer | 92k / 262M / **RTF 0.022** |
| OVC (2026) | Time-domain waveform (L=32) | Time-domain mask | Learned 1-D conv codec | Mamba-MinGRU | **2 ms** / 0.33 GMAC/s |

## Cross-Cutting Takeaways

1. **Progress is a Cartesian product, not a ladder.** A 2026 system picks one option per axis: target (DF/CCM), domain (hybrid loss), backbone (Mamba/linear RNN), efficiency technique (grouped + adaptive conv), multi-channel strategy (array-invariant), conditioning (PSE/OVC), training paradigm (discriminative / GAN / diffusion). The seven axes are near-orthogonal, so most combinations are unexplored.
2. **Loss choice often dominates architecture choice.** Pandey & Wang 2019 (frequency loss for time-domain nets) and the DCCRN(SNR) variant both show that the training signal can outweigh backbone tweaks. [[sources/li-2020-residual-noise-control\|Li et al. 2020]] is the corpus's earliest same-architecture loss comparison (2020, one U-Net × four losses), adding the caveat that objective metrics can miss the differences listeners hear — the residual-noise-control advantage appeared in listening tests, not in PESQ/SDR. [[sources/shetu-2026-generative-discriminative-comparison\|Shetu 2026]] makes this controlled: the *same* NCSN++ backbone ranks differently under discriminative, GAN, and diffusion objectives — the objective, not the architecture, decides robustness, convergence speed, and cost. PCEN-based mask thresholding ([[sources/liu-2025-pcen-mask-vad-speech-enhancement\|Liu 2025]]) and [[concepts/perceptual-contrast-stretching\|PCS]] post-processing extend this into the training-data / post-processing regime. [[sources/zhao-2026-spectrally-adaptive-loss\|Zhao & Madhu 2026]] add the spectral-weighting dimension: three losses on the *same* [[concepts/hyst-net\|HyST-Net]] backbone differ only in how the phase-aware term is weighted (scalar vs. frequency-sigmoid vs. signal-dependent), and the differences appear exclusively in band-conditional metrics. [[sources/pan-2025-data-driven-acoustics\|Pan 2025]] supplies the unifying tutorial frame: noise reduction is an *estimation/filtering* task whose loss can be constructed at three levels — the filter gain itself, the spectrum, or the waveform — and the SI-SDR loss is mathematically equivalent to maximizing the squared correlation coefficient between target and estimate, explaining *why* each loss level shapes a different aspect of the output (see [[concepts/si-sdr\|SI-SDR]]).
3. **The efficiency frontier is technique-composition, not model-shrinking.** GTCRN's 750× reduction is the product of four orthogonal techniques; CoFi-Lite and AdaptCRN extend it by adding path-decoupling and dynamic convolution rather than shrinking the backbone further.
4. **2026 inverts input-centric assumptions.** Output-based SE (evaluate outputs, not inputs) and array-invariant SE (condition on geometry, not array-specific SCM) both move the decision from the input side to the output / context side.
5. **Low-frequency resolution deserves explicit design.** BSRNN's 100 Hz low bands (+1.3 dB uSDR from low-band splitting alone), LiSenNet's stride-1 low bands, GTCRN's 65 uncompressed low bins, and DeepFilterNet's low-frequency-only deep filtering are four engineering expressions of the same prior: F0 and the first harmonics live at low frequencies.

## Open Questions and Gaps

- **Generative vs discriminative robustness** has now been benchmarked head-to-head at matched backbone by [[sources/shetu-2026-generative-discriminative-comparison\|Shetu 2026]] (matched/mismatched *SNR*, 60–100× GMAC gap) — GAN training wins on both robustness and cost, contradicting the simple "generative robust, discriminative cheap" split — but the comparison is SNR-mismatch, not *unseen-noise* generalization, and covers a single backbone family.
- **Inplace-CRN + Mamba** is unexplored: SICRN uses S4ND as a *branch*, but a fully Mamba-based inplace CRN (channel-wise Mamba reused across frequency bins) is not in the corpus.
- **Array-invariant + personalized conditioning** (Geo-DConv + OVC/PSE) is the obvious multi-channel + conditioning combination but unpublished.
- **Sub-4 ms generative SE** remains impossible (1 NFE still costs more than one discriminative forward pass); the drifting-models trajectory is the closest approach.
- The 60-year survey's open challenges — sub-4 ms hearing-aid latency, theoretical interpretation of DL "black boxes", multitalker scenarios, subjective validation for hearing-impaired listeners — remain only partially addressed by the 2026 corpus.

## Related Synthesis

- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]] — BC/AC/IMU fusion (the modality axis, deferred)
- [[synthesis/multimodal-bc-speech-enhancement|Multimodal BC Speech Enhancement]] — BC integration evolution
- [[synthesis/joint-multitask-ultra-low-latency-se|Joint Multi-Task SE & Ultra-Low-Latency Paradigm]] — task dissolution + latency tiers + linear-RNN replacement (the task/latency axis)
- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]] — ANC efficiency + RNN BPTT vs FEP memory bottlenecks
- [[synthesis/low-complexity-neural-vocoders|Low-Complexity Neural Vocoders]] — the shared "move structure out of the network" principle behind lightweight SE and vocoder design alike

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]] — foundational concept
- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network]] — the CRN template
- [[concepts/complex-ratio-mask|Complex Ratio Mask]] · [[concepts/complex-convolving-mask|Complex Convolving Mask]] · [[concepts/deep-filtering|Deep Filtering]] — target lineage
- [[concepts/time-domain-speech-enhancement|Time-Domain Speech Enhancement]] · [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]] — domain choice
- [[concepts/dprnn|Dual-Path RNN]] · [[concepts/mp-senet|MP-SENet]] · [[concepts/semamba|SEMamba]] · [[concepts/mamba-mingru|Mamba-MinGRU]] · [[concepts/sse-net|SSE-Net]] — backbone lineage
- [[concepts/gtcrn|GTCRN]] · [[concepts/lisennet|LiSenNet]] · [[concepts/cofi-lite|CoFi-Lite]] · [[concepts/adaptcrn|AdaptCRN]] · [[concepts/igcrn|IGCRN]] · [[concepts/iccrn|ICCRN]] · [[concepts/sicrn|SICRN]] — efficiency frontier
- [[concepts/band-split-rnn|Band-Split RNN]] · [[concepts/sub-band-full-band-architecture|Sub-Band-Full-Band Architecture]] · [[concepts/erb-scale|ERB Scale]] · [[concepts/asymmetric-stft|Asymmetric STFT]] — encoder/decoder lineages (Insight 4a)
- [[concepts/tf-mask-estimation|TF-Mask Estimation]] · [[concepts/power-law-compression|Power-Law Compression]] · [[concepts/per-channel-energy-normalization|Per-Channel Energy Normalization]] — input representation and masking
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] · [[concepts/neural-beamforming|Neural Beamforming]] · [[concepts/array-invariant-speech-enhancement|Array-Invariant SE]] · [[concepts/geometry-aware-dynamic-convolution|Geo-DConv]] · [[concepts/output-based-speech-enhancement|Output-Based SE]] · [[concepts/hybrid-speech-enhancement|Hybrid Speech Enhancement]]
- [[concepts/personalized-speech-enhancement|Personalized SE]] · [[concepts/target-speaker-extraction|Target Speaker Extraction]] · [[concepts/own-voice-cancellation|Own-Voice Cancellation]] · [[concepts/prior-matching|Prior Matching]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech]] · [[concepts/drifting-models|Drifting Models]] · [[concepts/generative-vs-discriminative-speech-enhancement|Generative vs. Discriminative Speech Enhancement]] · [[concepts/speech-enhancement-hallucination|Speech Enhancement Hallucination]] · [[concepts/one-step-generative-models|One-Step Generative Models]]
- [[concepts/generalized-loss-function|Generalized Loss Function]] · [[concepts/frequency-domain-loss|Frequency-Domain Loss]] · [[concepts/noise-attenuation-control|Noise Attenuation Control]] · [[concepts/artificial-residual-noise|Artificial Residual Noise]] — training-objective / noise-control lineage
- [[concepts/spectrally-adaptive-loss|Spectrally Adaptive Loss]] · [[concepts/magnitude-phase-compensation-effect|Magnitude-Phase Compensation Effect]] · [[concepts/hyst-net|HyST-Net]] — loss-side compensation-effect remedy and its streaming backbone
- [[concepts/lisennet|LiSenNet]] · [[concepts/noise-detector|Noise Detector]] · [[concepts/gla-phase-refinement|GLA Phase Refinement]] · [[concepts/sub-band-convolution|Sub-band Convolution]] — the 2025 lightweight-SE design point and its components
- [[concepts/rnnformer|RNNFormer]] — RTF-first dual-path block (time GRU + frequency MHSA); FastEnhancer's bottleneck
- [[concepts/ftf-transformer|FTF Transformer]] · [[concepts/trapezoidal-causal-masking|Trapezoidal Causal Masking]] — the frequency–time–frequency bottleneck and its bounded-context attention, from LCT-GAN
- [[concepts/universal-speech-enhancement|Universal SE]] · [[concepts/early-exit-speech-enhancement|Early-Exit SE]] · [[concepts/parallel-look-ahead-convolutions|Parallel Look-Ahead Convolutions]] — the latency-budget axis (Fu 2026)

## Related Sources

- [[sources/yan-2025-lisennet|Yan, Zhang, Fan, Zhou & Liu 2025 (LiSenNet)]] — sub-band conv + causal dual-path GRU + noise detector; the 37k/56M MACs/s operating point between GTCRN and CoFi-Lite
- [[sources/ahn-2026-fastenhancer|Ahn, Han, Woo & Kim 2026 (FastEnhancer)]] — RTF-first streaming SE: RNNFormer bottleneck, time-kernel-1 convolutions, BN fusion; new quality-vs-speed Pareto frontier on Voicebank-Demand
