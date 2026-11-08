---
type: synthesis
created: 2026-04-22
updated: 2026-11-08
sources:
  - wiki/sources/tagliasacchi-2020-seanet.md
  - wiki/sources/zhang-2022-bone-conducted-speech-dissertation.md
  - wiki/sources/wang-2022-fusing-bc-ac-complex-domain-se.md
  - wiki/sources/he-2025-vibomni.md
  - wiki/sources/kuang-2024-lightweight-speech-enhancement-bone-air.md
  - wiki/sources/liu-2025-robust-fusion-bc-ac-attention.md
  - wiki/sources/dai-2026-speech-preserving-deep-anc.md
  - wiki/sources/heitkaemper-2026-bcs-speech-enhancement-earbuds.md
  - wiki/sources/heitkaemper-2025-bcs-speech-enhancement-earbuds.md
  - wiki/sources/han-2026-quality-aware-earable-se.md
  - wiki/sources/lugo-2026-diffvqe.md
  - wiki/sources/ohlenbusch-2026-pas-se.md
  - wiki/sources/zhang-2025-mbenet.md
  - wiki/sources/kuang-2025-low-complexity-bc-speech-enhancement.md
  - wiki/sources/wu-2026-dbmif-multimodal-fusion.md
  - zotero://select/items/0_B92ER5KS (Khanagha 2026: Conditional Diffusion)
  - zotero://select/items/0_NIIDMA7J (Contrastive Learning for BC)
tags:
  - bone-conduction
  - multimodal-fusion
  - speech-enhancement
  - deep-learning
  - diffusion-models
  - smart-hearables
  - attention-mechanism
  - sensor-failure-robustness
  - quality-aware-fusion
  - target-speaker-extraction
  - modality-balance
  - gan
---

# Multimodal Smart Hearables: Bone-Conduction Aided Speech Enhancement

This synthesis tracks the evolution of Bone-Conducted (BC) speech integration in smart hearables (headphones, AR glasses), moving from traditional statistical analysis to state-of-the-art generative diffusion models.

## 1. The Multimodal Imperative: AC vs. BC

Traditional Air-Conducted (AC) microphones capture full-band audio but are highly susceptible to background noise. BC sensors (accelerometers) capture vibrations directly from the skull, providing **noise-immune** signals that are intrinsically limited in bandwidth (usually <2 kHz).

| Modality | Bandwidth | Noise Immunity | Limitation |
| :--- | :--- | :--- | :--- |
| **AC (Air)** | Full-band | Low | Unusable at very low SNRs (-10 dB) |
| **BC (Bone)**| Low-pass | **High** | Muffled quality; missing high frequencies |

---

## 2. Technical Evolution of Fusion Strategies

### 2.1 Foundational Era: Multi-modal Waveform Learning (2020)

Early work establishes the feasibility of leveraging non-audio sensor modalities for speech enhancement.

- **[[sources/tagliasacchi-2020-seanet|SEANet]] (Tagliasacchi, INTERSPEECH 2020)**: First work to use **accelerometer data** from earbud-mounted bone-conductance sensors for speech enhancement. The model is a fully convolutional **wave-to-wave UNet** that fuses microphone audio and accelerometer waveforms at the input level, trained with MelGAN-style adversarial + feature losses. Key insight: accelerometer signals are immune to environmental noise because they capture skull vibrations. Achieves **9.6 dB SI-SDRi** in overlapping-speaker scenarios where audio-only models fail (−0.9 dB). Demonstrates that accelerometer bandwidth >400 Hz is needed for speaker separation, while noise suppression remains robust at much lower rates.

### 2.2 Statistical and Mapping Era (2022)

Focuses on "restoring" BC speech or using it as a reference for AC denoising.

- **Pitch Extraction ([[sources/zhang-2022-bone-conducted-speech-dissertation|Zhang, 2022]])**: Combines AC weighted auto-correlation with BC cepstrum (WACF-CEP) to detect pitch in 0 dB SNR environments.
- **[[sources/wang-2022-fusing-bc-ac-complex-domain-se|Complex Spectral Mapping (Wang, Zhang & Wang 2022)]]**: Uses Densely-Connected CRNs (DC-CRN) to fuse AC and BC signals in the [[concepts/complex-spectral-mapping|complex domain]], preserving phase information. Introduces attention-based fusion (AFF) that computes a soft modality-selection mask from local+global features — outperforming early/late fusion by +21.1% STOI at −5 dB. Additionally proposes a CycleGAN-based semi-supervised framework that leverages unpaired AC data, matching fully-supervised performance with only 50% parallel BC data.

### 2.3 Lightweight IMU-Based Fusion (2023–2025)

Parallel to the generative trend, a line of work focuses on practical, lightweight multi-modal fusion using commodity IMU sensors already available in earables.

- **[[sources/he-2025-vibomni|He et al. (MobiSys 2023 / arXiv 2025) — VibOmni]]**: Demonstrates that the IMU (accelerometer + gyroscope) already present in commercial earables for head-tracking can capture bone-conducted vibration at ~1.6 kHz sampling rate. The system uses a dual-encoder DPRNN architecture with:
  - **Auxiliary decoder** on the vibration branch to prevent modality collapse (audio dominating training).
  - **Bone Conduction Function (BCF) data augmentation**: Models the audio→vibration transfer function as a Gaussian in the frequency domain, enabling synthetic vibration generation from LibriSpeech with only 4.5% spectrogram error.
  - **Multi-modal SNR estimator** for continual self-supervised learning and adaptive inference.
  - **Key result**: 31× lower latency than FullSubNet on mobile devices, 21% PESQ improvement, ~40% WER reduction — all using existing IMU sensors without additional hardware.

### 2.4 Lightweight T-F Domain Fusion (2024)

Parallel to the IMU-based approach, a line of work focuses on lightweight time-frequency domain fusion using dedicated BC microphones.

- **[[sources/kuang-2024-lightweight-speech-enhancement-bone-air|Kuang, Yang & Yang (JASA 2024) — DenGCAN]]**: A lightweight fused BC/AC speech enhancement model using:
  - **[[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]** for coarse-then-refined multi-modal fusion
  - **[[concepts/densely-gated-convolutional-attention-network|DenGCAN]] backbone** with dense blocks (feature reuse), gated convolutions, and sConformer bottleneck
  - **[[concepts/attention-gate|Attention Gate (AG)]] skip-connections** that consider local + global features
  - **Key result**: 1.03M params, 0.859 GMACs, 1.870 wb-PESQ improvement, RTF 0.649 on ARM — lowest compute among all compared models
  - **A4BS dataset**: 4-position BC recordings from 109 speakers (~107 h)

### 2.5 Attention-Driven Robust Fusion (2025)

- **[[sources/liu-2025-robust-fusion-bc-ac-attention|Liu, Chen & Yin (ICASSP 2025) — ATFA Dual-Mask]]**: Reframes BC/AC fusion around two architectural ideas and one training innovation:
  - **Pre-fusion via shared convolution** — extracts common spectral patterns across modalities before encoding (multi-view input).
  - **[[concepts/adaptive-time-frequency-attention|Adaptive Temporal-Frequency Attention (ATFA)]]** — three cascaded blocks of dual-axis MHSA (time + frequency) with adaptive hierarchical fusion (AHA), replacing recurrent middle layers.
  - **Dual-channel mask** — four real masks (RI for AC + RI for BC), applied to the original two complex spectra and summed (beamforming-inspired). Validated to also improve a DCCRN backbone.
  - **Special Training (ST)** — random modality dropout (p = 0.2 per channel) during training. Transforms the model from catastrophically failing under sensor invalidity to **gracefully recovering** (PESQ 1.18 → 2.54 when AC fails). See [[concepts/sensor-failure-robust-fusion|Sensor-Failure Robust Multi-Modal Fusion]].
  - **Key result**: 1.6M params (~5% of Aff-Fusion), +0.2 PESQ / +0.03 STOI over Aff-Fusion across all SNRs from −5 to 15 dB, on the Elevoc ESMB BC corpus.

### 2.6 Generative and Diffusion Era (2025–2026)

Shifts from predicting clean speech to **generating** it using BC signals as guidance.

- **Conditioned Diffusion (Khanagha, 2026)**: The **BCDM** (Bone-Conduction Conditional Diffusion Model) treats clean speech recovery as a stochastic process.
- **Conditioning Strategies**:
    - **Input Concatenation (IC)**: Simple but effective at low computational cost.
    - **Decoder Conditioning (DC)**: Injects BC features directly into the decoder's upsampling layers, providing superior speech naturalness (POLQA/PESQ) at the cost of higher latency.
- **Contrastive Learning (Li, 2025)**: Uses twin-tower networks to minimize the embedding distance between AC and BC modalities, improving cross-modal feature alignment.

### 2.7 Industry Deployment: BCS-Guided ASR (2025–2026)

- **[[sources/heitkaemper-2025-bcs-speech-enhancement-earbuds|Heitkaemper et al. (Google, ICASSP 2025)]]**: The published version of the [[sources/heitkaemper-2026-bcs-speech-enhancement-earbuds|US patent 2026]] system — a streaming Conformer mask estimator for earbud voice assistants that fuses a single-channel ACS with a band-limited BCS (downsampled to 500 Hz and upscaled by a feed-forward projection, cutting earbud-to-device transmission bandwidth to 6.25% for off-device enhancement on the phone). Trained with ASR-loss + SI-SNR ($\lambda_{\text{ASR}} = 10^{-4}$) on 50k h simulated data (BCS simulated by 47-tap FIR low-pass at 500 Hz), then finetuned on only ~6 h of real earbud recordings. Key results on real earbud test sets:
  - A pretrained VAD applied to the BCS **hard-bypasses the enhancer for uninformative BCS** (~30% of realistic recordings, mostly wind) — for examples with <60% detected keyword-BCS activity (~40% of the Hard set), enhancement *degrades* the ACS below unprocessed WER. This is an inference-time modality-validity gate, complementary to Liu 2025's training-time modality dropout (§3.4).
  - At RTF 0.01, outperforms a state-of-the-art multi-channel enhancer (TfCleanformer) finetuned for earbuds on 3 of 4 test sets; beats the 39× costlier large variant on the Dynamic set (WER 10.9 vs 16.4). >15% relative WER reduction under the hardest conditions (noise or wind ≥ 6 m/s).

### 2.8 Quality-Aware Fusion: Addressing Modality Imbalance (2026)

- **[[sources/han-2026-quality-aware-earable-se|Han et al. (IMWUT 2026) — QuaSE]]**: Identifies that [[concepts/ear-canal-deformation|Ear Canal Deformation (ECD)]] induced by articulatory gestures causes air pressure imbalance in the sealed ear canal, degrading in-ear (bone-conducted) speech quality and breaking the cross-channel correlation assumption of prior dual-microphone SE systems. Proposes [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement (QuaSE)]], which:
  - **Self-assesses** in-ear speech quality without reference via an autoencoder trained only on high-quality samples (selected by spectral peak-to-valley matching + DTW alignment)
  - **Generates quality embeddings** via frequency squeeze → FC layers with Sigmoid → unsqueeze, producing per-time-bin weights in [0, 1]
  - **Dynamically weights** in-ear features before cross-modal fusion with airborne speech
  - Uses **content-aware adaptive time masking** for data augmentation, simulating ECD-induced distortion conditioned on spectral energy distribution
  - **Key result**: +9.35% PESQ, +17.68% SI-SDR over best baseline (EarSpeech); QA module is modular and improves EarSpeech by up to +5.48% PESQ
  - **Distinction from Liu 2025 ATFA**: While ATFA handles *binary* sensor failure via random dropout, QuaSE handles *continuous* quality variations via dynamic quality-weighted fusion — a finer-grained approach to modality robustness

### 2.9 Personalization as a Third Clue: PAS-SE (2026)

- **[[sources/ohlenbusch-2026-pas-se|Ohlenbusch, Kegler & Stamenovic (ICASSP 2026) — PAS-SE]]**: Adds **speaker enrollment** to the fusion mix — an FT-JNF mask network taking OM + in-ear-microphone magnitude STFTs ([[concepts/as-se|AS-SE]]) is multiplicatively conditioned on a 128-dim embedding from a jointly-trained SpeakerBeam-style encoder (1.810M params). Key contributions to the BC-fusion lineage:
  - **Training-config augmentation**: with no recorded in-ear interferer data, approximating the in-ear interferer as an attenuated OM interferer ($a \cdot V_o$, $a \in [0.001,1]$) during training enables cross-device generalization — the array-transfer-function analogue of VibOmni's BCF augmentation (§2.3) and Heitkaemper's FIR-simulated BCS (§2.7). Skipping in-ear noise modeling entirely (config A) collapses the AS-SE system.
  - **Enrollment-sensor choice**: recording the enrollment utterance with the acoustically shielded in-ear microphone retains personalization benefits down to −10 dB enrollment SNR, while OM enrollment breaks below 0 dB — a sensor-selection insight paralleling QuaSE's quality-aware weighting.
  - **Key result**: cross-dataset interferer SI-SDR 8.34 dB (PAS-SE with in-ear enrollment) vs. 7.20 dB AS-SE-only — outperforming even AS-SE baselines trained fully in-domain on the evaluation dataset.

### 2.10 From Enhancement to Extraction: BC-Guided TSE (2025)

- **[[sources/zhang-2025-mbenet|Zhang, Feng, Liu, Zhang & Li (ASRU 2025) — MBENet]]**: The first BC-AC fusion model for [[concepts/target-speaker-extraction|target speaker extraction]] — extending the lineage from speech enhancement to the TSE task, where the BC signal replaces the enrollment utterance as the speaker clue. The architecture:
  - **Bone-conduction enhancement module** — a causal [[concepts/convolutional-recurrent-network|CRN]] (3 conv enc / GRU-64 bottleneck / 3 transposed-conv dec, dense skips) extends the BC bandwidth, trained as an **auxiliary task** (MSE on magnitude vs. clean target speech, weight $\gamma = 15$) alongside the SI-SDR extraction loss — multi-task learning in the same spirit as VibOmni's auxiliary decoder preventing modality collapse (§2.3), but aimed at spectral completeness.
  - **Shared-weight [[concepts/band-split-rnn|band-split]] fusion** — AC and enhanced-BC spectrograms are split into 31 subbands by the *same* per-band linear + layer-norm projections (parameter sharing across modalities, echoing Liu 2025's shared-conv pre-fusion), then concatenated and processed by 6 dual-axis (time/band) LSTM blocks with band-merge mask decoding.
  - **Key results** (simulated ABCS-2Mix, Mandarin, SIR 0–2 dB + MUSAN noise −5…10 dB): causal 3.8M params beats pBSRNN/SpEx+/MMINet/CRN on SI-SDR, PESQ and DNSMOS at every SNR, with the PESQ margin *growing* as SNR drops (+2.74% at 10 dB → +6.03% at −5 dB); the BC cue beats a speaker-embedding AC-only ablation by +5.48 dB SI-SDR (16.67 vs 11.19 dB) — direct evidence that under strong noise a concurrent noise-immune observation of the target is more informative than a pre-recorded enrollment embedding.
  - **Distinction from the SE lineage**: MBENet's mask is applied to the **AC mixture only** (single output), unlike the dual-mask/dual-decoder designs of Liu 2025 and VibOmni — in TSE the BC channel is a *cue*, not an output to be enhanced.

  **Baseline comparison (Table I averages, adapted baselines)** — no prior BC-AC TSE model existed, so classic TSE/SE models were re-purposed for the task:

  | Method | Params (M) | Avg SI-SDR / PESQ | Adaptation for BC-AC TSE |
  |---------|-----------:|-------------------:|--------------------------|
  | CRN | 1.6 | 10.58 / 2.54 | SE model; magnitude prediction → mask branch, AC+BC concatenated input |
  | SpEx+ | 11.1 | 15.06 / 2.91 | Time-domain TSE; BC replaces the enrollment utterance |
  | MMINet | 5.2 | 15.81 / 2.92 | Time-domain AC-BC fusion SE |
  | pBSRNN | 3.8 | 15.77 / 3.03 | T-F domain TSE; BC replaces the enrollment utterance |
  | **MBENet** | **3.8** | **16.67 / 3.17** | — |

  The parameter efficiency is the notable point: MBENet ties pBSRNN at 3.8M params (the gain comes from the auxiliary task + fusion design, not capacity) and leads SpEx+ by 1.6 dB with 1/3 the parameters. Full comparison in [[queries/mbenet-vs-other-ac-bc-approaches|the MBENet-vs-other-AC+BC query]].

  **Limitations**: evaluated only on the simulated ABCS-2Mix benchmark (Mandarin, 100 speakers) — no real-device recordings or cross-lingual validation; no sensor-failure handling (unlike Liu 2025's Special Training or Heitkaemper 2025's VAD gating); no RTF/MACs figures despite the causality and efficiency claims, so compute cannot be compared against e.g. DenGCAN's 0.859 GMACs.

### 2.11 Band-Compression Meets BC Fusion (2025)

- **[[sources/kuang-2025-low-complexity-bc-speech-enhancement|Kuang, Yang, Wang & Yang (Applied Acoustics 2025) — Sub-Band + Full-Band]]**: The same group's successor to DenGCAN (§2.4) brings monaural band-compression efficiency (the PercepNet/DeepFilterNet/GTCRN lineage) into the BC-aided setting. The [[concepts/sub-band-full-band-architecture|two-step architecture]] pairs 32 full-range ERB sub-band gains (coarse spectral-envelope correction, ~2.5 MMACs) with full-band $N{=}3$ [[concepts/deep-filtering|deep filtering]] (fine suppression), each estimated by its own encoder-decoder set sharing a grouped-sConformer bottleneck, with early + intermediate [[concepts/iterative-attentional-feature-fusion|iAFF]] fusion of BC/AC at both granularities:
  - **Key result**: best wb-PESQ (2.396 mid-SNR avg) and eSTOI among GTCRN, DeepFilterNet, DC-CRN, and DenGCAN at the lowest MACs (40.3 M) — DenGCAN needs 4× the compute for less quality
  - **GTCRN-AC ablation**: the AC-only variant isolates the BC contribution (+0.61 wb-PESQ at [−15,−9] dB) — the sensor, not the architecture, is the dominant quality lever at very low SNR
  - **RTF insight**: sConformer bottleneck parallelizes far better than GTCRN's DPRNN at equal MACs (RTF 0.159 vs. 0.446 on ARM), at the cost of Q/K cache memory — the params/MACs-vs-wall-clock lesson recurring in the multi-modal setting (§3.2)
  - **Fusion finding**: iAFF beats cross attention on *both* cost and quality (40.26 vs. 44.21 MMACs; wb-PESQ 2.396 vs. 2.337)

### 2.12 Iterative Rebalancing: Attacking Modality Dominance (2026)

- **[[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. (Applied Intelligence 2026) — DBMIF]]**: The first entry in this lineage to attack **[[concepts/modality-dominance|modality dominance]]** as a first-class training problem rather than as a sensor-failure or quality-variation issue. Their diagnosis: at low training SNR the AC channel's clean target is nearly unlearnable, so the noise-immune BC branch produces the larger immediate loss reduction, its gradients dominate the shared fusion stream, and the representation collapses onto the spectrally impoverished modality — after which single-stage fusion has no mechanism left to re-introduce the AC information. The response is a coarse-to-fine chain of three balancing mechanisms plus a frequency axis to balance along:
  - **[[concepts/pseudo-qmf-bank|PQMF]] front-end** — 4 subbands ($L = 64$ prototype) for both modalities, so fusion weights can be frequency-selective. Verified: the learned weight is low in the lowest subband (pitch anchored on BC) and high in the upper subbands (AC supplies bandwidth), with the mid band the most dynamic.
  - **[[concepts/deep-iterative-attention-fusion|DIAF]]** (early) — parameter-free sum initialisation refined by $K{=}3$ rounds of channel attention that condition on the evolving fusion, so the gate is not stuck with its first, noise-driven estimate; mean $w^{(3)}$ rises monotonically with SNR.
  - **[[concepts/cross-branch-gated-interaction|CBGI]]** (every encoder scale) — bidirectional sigmoid gating: fusion→branch modulation plus branch→fusion feedback, closing the loop so dominance is renegotiated throughout the network. Largest ablation contributor (~6–7 absolute CER on both ASR backends); a standard GMU performed worse in preliminary experiments.
  - **[[concepts/deep-balanced-interaction|DBI]]** (bottleneck) — weight-tied fixed-point iteration over three modality states with a best-equilibrium selection rule ($k^\star = \arg\min \delta_k$, $K_{\max}{=}50$, median $k^\star{=}5$), refining the balance at zero parameter cost.
  - **Subband-aware adversarial supervision** — a full-band [[concepts/multi-scale-discriminator|discriminator]] plus three dilated critics on the same PQMF subbands, in the MelGAN feature-matching tradition ($\lambda = 1000$); DBMIF reports **no explicit reconstruction loss**, unlike every discriminative system in §2.1–2.11.
  - **Key result**: best of nine systems on all five objective metrics — SI-SDR 12.42 dB, PESQ 2.70, STOI 0.90, ESTOI 0.85, DNSMOS 3.35 — and CER 15.84%/12.07% (Whisper/WeNet) vs. 19.46%/14.50% for DC-CRN, i.e. ≥2.5% absolute CER reduction. Ablation of branch count isolates the mechanism: single-branch (early fusion, shared encoder–decoder) SI-SDR 0.86 dB at −15 dB vs. 7.15 dB dual-branch vs. 9.27 dB three-branch — the payoff from keeping modalities separate grows exactly where dominance would bite.
  - **Where it sits vs. the rest of this synthesis**: the same corpus (100-speaker ABCS) and the same baselines (DenGCAN, DC-CRN, MMINet, FCN, EBEN) as earlier entries, so its numbers are directly comparable — it beats DenGCAN by +1.67 dB SI-SDR and +0.72 PESQ. DBMIF reports no params/MACs in the paper, but the released code measures **10.41 M generator params / 2.60 GMACs/s / RTF 0.085 (CPU)** — roughly **6× DenGCAN's parameters and 3000× its MACs**, and ~40000× the MACs of the Kuang 2025 band-compression design. It is therefore the *most expensive* entry in §4 by a wide margin and the clearest counter-example to the embedded-device framing that dominates the rest of this lineage: the quality lead is bought with ~3 GMACs/s, not with a smarter use of the same budget. Unlike the quality-aware (§2.8) and sensor-failure (§3.4) strands, DBMIF assumes both sensors are healthy and instead fixes the *optimisation* imbalance; unlike the generative strand (§2.6), it is GAN-trained but not a generative *model* in the diffusion sense — it is a time-domain enhancer with an adversarial loss **plus** (per the released code, though not the paper) two $L_1$ reconstruction anchors.
  - **Limitations**: non-causal and computationally heavy (authors' own statement, now quantified at 2.60 GMACs/s / RTF 0.085 CPU), single Mandarin corpus, no sensor-failure handling, and several paper-vs-code discrepancies (PQMF $L$=32 not 64; tanh not sigmoid gates; hidden $L_1$ reconstruction terms) that make the method section unreliable for re-implementation.

---

## 3. Core Technical Challenges

### 3.1 The Bandwidth Gap (Super-Resolution)

Because BC speech is missing frequencies above 2 kHz, multimodal systems must perform **Guided Super-Resolution**. Generative models (GANs and Diffusion) excel here by hallucinating plausible high-frequency details that match the low-frequency "skeleton" provided by the BC sensor. The converse also holds for transmission: Heitkaemper et al. 2025 exploit the low-pass characteristic to **discard** the BC signal above 500 Hz before transmission from the earbuds (restoring dimensionality with a learned upscaling projection), paying <1.5% absolute WER for 6.25% of the bandwidth — bandwidth thrift rather than bandwidth extension. A third option is now demonstrated for extraction: MBENet (Zhang et al. 2025) makes BC bandwidth extension a **training-time auxiliary task** whose output feeds fusion — the extension quality matters only insofar as it helps the final extraction, sidestepping the hallucination risk of generative super-resolution while still closing the spectral gap (ablation: +0.55 dB SI-SDR / +0.14 PESQ over the no-extension variant).

### 3.2 Real-time Implementation & Latency

- **STFT vs. Time-Domain**: Frequency-domain methods (STFT) introduce frame-level latency (~32-64ms).
- **Embedded Constraints**: Diffusion models require multiple reverse steps (e.g., $N=60$), making them challenging for low-power DSPs. Recent work (Liang, 2026) emphasizes **Analytic/Closed-form** solutions to minimize these overheads.
- **Single-step hybrid diffusion**: [[sources/lugo-2026-diffvqe|DiffVQE (Lugo et al. 2026)]] refines the multi-step constraint: a discriminative Cond DNN initializes the reverse process at $t = T$ and a score-based Score DNN applies exactly **one** correction step (1 NFE, RTF 0.172–0.185 on a single CPU thread) for joint AEC + denoising — no distillation teacher required. Hybrid design, not NFE, may thus be the practical route to real-time generative SE.

### 3.3 Data Scarcity

Parallel AC-BC data is difficult to collect. **Semi-supervised frameworks** (using CycleGANs) allow models to learn from non-parallel AC and BC datasets, significantly lowering the barrier for training robust production models.

### 3.4 Sensor-Failure Robustness

When one modality degrades or fails entirely (e.g., BC sensor contact loss, AC microphone clipping), naïvely-fused models suffer catastrophic performance drops. The **Special Training** strategy from Liu 2025 (random per-channel dropout during training) is the first principled solution, enabling graceful degradation. See [[concepts/sensor-failure-robust-fusion|Sensor-Failure Robust Multi-Modal Fusion]].

### 3.5 Optimisation Imbalance (Distinct from Sensor Failure)

§3.4 concerns a modality that *stops working*. A subtler and more pervasive problem is a modality that works but is *too easy*: at low SNR, BC's noise immunity means it alone reduces the loss, so its gradients crowd out the AC branch and the fused representation collapses toward BC's muffled spectrum. This is orthogonal to sensor health — both sensors can be perfectly good while the fusion is effectively unimodal — and it is invisible in aggregate metrics, showing up only as an unexplained ceiling on high-frequency quality. Wu et al. 2026 name it [[concepts/modality-dominance|modality dominance]] and treat it with iterative rebalancing (§2.12); the diagnostic signature is an *asymmetric* ablation in which removing the difficult modality barely changes performance, and a fusion weight that saturates at one extreme. Quality-aware fusion (§2.8) and quality-aware gating are complementary — they detect *bad* inputs, whereas dominance correction detects *good but over-weighted* ones.

---

## 4. Key Performance Benchmarks

| Method | Year | Params | PESQ Gain | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **SEANet** | 2020 | — | 9.6 dB SI-SDRi | Speaker separation with IMU |
| **DC-CRN + AFF (Wang)** | 2022 | — | +21.1% STOI | Complex-domain fusion; semi-supervised |
| **VibOmni** | 2023 | — | +21% PESQ | Low-latency on-device (IMU) |
| **DenGCAN (Kuang)** | 2024 | 1.03M | +1.870 wb-PESQ | Minimum compute on ARM |
| **ATFA (Liu)** | 2025 | 1.6M | +0.2 PESQ | Robust to sensor failure |
| **MBENet (Zhang)** | 2025 | 3.8M | 16.67 dB SI-SDR / 3.17 PESQ (ABCS-2Mix avg) | First BC-AC fusion **TSE**; causal; margin over pBSRNN grows as SNR drops |
| **Sub-band + full-band (Kuang)** | 2025 | 256.4K | 2.396 wb-PESQ (A4BS mid-SNR avg) | 40.3 MMACs; RTF 0.159 ARM — band-compression efficiency in BC-aided SE |
| **BCS-guided SE (Heitkaemper)** | 2025 | — | >15% rel. WER | Voice-assistant ASR on earbuds; RTF 0.01, off-device |
| **BCDM (Khanagha)** | 2026 | — | **High** | Extreme noise (-10 dB SNR) |
| **QuaSE (Han)** | 2026 | — | +9.35% PESQ | Quality-varying in-ear modality |
| **PAS-SE (Ohlenbusch)** | 2026 | 3.2M | 8.34 dB SI-SDR (V, cross-dataset) | Interferer suppression; cross-device generalization; enrollment as third clue |
| **DBMIF (Wu)** | 2026 | **10.41M** | 12.42 dB SI-SDR / 2.70 PESQ, CER 15.84% | Modality-dominance correction via iterative fusion (DIAF/CBGI/DBI); GAN-trained, non-causal; 2.60 GMACs/s, RTF 0.085 CPU |

---

## Related Concepts

- [[concepts/bcs-guided-speech-enhancement|BCS-Guided Speech Enhancement]]
- [[concepts/bone-conduction|Bone Conduction]]
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]]
- [[concepts/densely-gated-convolutional-attention-network|DenGCAN]]
- [[concepts/iterative-attentional-feature-fusion|Iterative Attentional Feature Fusion (iAFF)]]
- [[concepts/attention-gate|Attention Gate (AG)]]
- [[concepts/adaptive-time-frequency-attention|Adaptive Temporal-Frequency Attention (ATFA)]]
- [[concepts/sensor-failure-robust-fusion|Sensor-Failure Robust Multi-Modal Fusion]]
- [[concepts/quality-aware-speech-enhancement|Quality-Aware Speech Enhancement]]
- [[concepts/ear-canal-deformation|Ear Canal Deformation]]
- [[concepts/dprnn|DPRNN]]
- [[concepts/mbenet|MBENet]]
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/modality-dominance|Modality Dominance]]
- [[concepts/deep-iterative-attention-fusion|Deep Iterative Attention Fusion (DIAF)]]
- [[concepts/cross-branch-gated-interaction|Cross-Branch Gated Interaction (CBGI)]]
- [[concepts/deep-balanced-interaction|Deep Balanced Interaction (DBI)]]
- [[concepts/pseudo-qmf-bank|Pseudo-QMF Bank]]
- [[concepts/multi-scale-discriminator|Multi-Scale Discriminator]]

## Related Sources

- [[sources/tagliasacchi-2020-seanet|Tagliasacchi et al. 2020: SEANet]]
- [[sources/zhang-2022-bone-conducted-speech-dissertation|Zhang 2022: BC Statistical Analysis]]
- [[sources/wang-2022-fusing-bc-ac-complex-domain-se|Wang, Zhang & Wang 2022: Fusing BC and AC for Complex-Domain SE]]
- [[sources/he-2025-vibomni|He et al. 2025: VibOmni]]
- [[sources/kuang-2024-lightweight-speech-enhancement-bone-air|Kuang, Yang & Yang 2024: DenGCAN]]
- [[sources/liu-2025-robust-fusion-bc-ac-attention|Liu, Chen & Yin 2025: Robust BC/AC Fusion with ATFA]]
- [[sources/dai-2026-speech-preserving-deep-anc|Dai 2026: Speech-Preserving Deep ANC]]
- [[sources/heitkaemper-2026-bcs-speech-enhancement-earbuds|Heitkaemper et al. 2026: BCS-Guided SE for Earbuds]]
- [[sources/heitkaemper-2025-bcs-speech-enhancement-earbuds|Heitkaemper et al. 2025: BCS-Guided Speech Enhancement for Voice Assistant on Earbuds]] — ICASSP publication of the patent system, with WER/RTF evaluation (§2.7, §3.1, §4)
- [[sources/han-2026-quality-aware-earable-se|Han et al. 2026: QuaSE — Quality-Aware Earable Dual-Microphone SE]]
- [[sources/lugo-2026-diffvqe|Lugo et al. 2026: DiffVQE]] — single-step hybrid diffusion evidence for real-time generative SE (§3.2)
- [[sources/ohlenbusch-2026-pas-se|Ohlenbusch, Kegler & Stamenovic 2026: PAS-SE]] — enrollment as third clue; in-ear enrollment robustness (§2.9)
- [[sources/zhang-2025-mbenet|Zhang, Feng, Liu, Zhang & Li 2025: MBENet]] — first BC-AC fusion TSE; BC bandwidth extension as auxiliary task (§2.10, §3.1, §4)
- [[sources/kuang-2025-low-complexity-bc-speech-enhancement|Kuang, Yang, Wang & Yang 2025: Low-Complexity BC-Aided Speech Enhancement Leveraging Sub-Band and Full-Band Architecture]] — band-compression efficiency meets BC fusion (§2.11, §4)
- [[sources/wu-2026-dbmif-multimodal-fusion|Wu et al. 2026: DBMIF]] — iterative rebalancing against modality dominance (§2.12, §4)

## Related Synthesis

- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]
- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]]
