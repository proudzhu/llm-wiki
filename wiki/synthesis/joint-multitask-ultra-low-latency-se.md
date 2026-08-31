---
type: synthesis
created: 2026-07-16
updated: 2026-07-22
sources:
  - raw/papers/indenbom-2023-deepvqe/full-text.md
  - raw/papers/ostergaard-2026-own-voice-cancellation/full-text.md
  - raw/papers/benslimane-2026-rt-tango-binaural-speech-enhancement/full-text.md
  - raw/papers/zhao-2026-halo-half-frame-rate-adaptive-operator/full-text.md
  - raw/papers/hao-2025-l3c-deepmfc/full-text.md
  - raw/papers/ashur-2026-acoustic-howling-suppression-fine-tuning/full-text.md
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
  - raw/papers/seidel-2024-bark-scale-nn-residual-suppression/full-text.md
  - raw/papers/chen-2023-ultra-dual-path-compression/full-text.md
  - raw/papers/castelli-2025-embedded-joint-aec-ns/full-text.md
  - raw/papers/li-2025-echofree-neural-aec/full-text.md
  - raw/papers/larraza-2026-fast-ulcnet-speech-enhancement/full-text.md
  - raw/papers/shetu-2026-munet/full-text.md
tags:
  - speech-enhancement
  - multi-task
  - low-latency
  - real-time
  - linear-rnn
  - hearing-aid
  - streaming
---

# Joint Multi-Task Speech Enhancement & Ultra-Low-Latency Realtime Paradigm

> Cross-source synthesis spanning 2023–2026: how task boundary dissolution and sub-10ms latency budgets are jointly reshaping speech-enhancement architecture.

## Motivation: Two Converging Pressures

Two independent trends in 2023–2026 speech enhancement (SE) literature are now colliding in the same models:

1. **Task boundary dissolution** — AEC, NS, dereverberation (DR), own-voice cancellation (OVC), acoustic howling suppression (AHS) were traditionally separate DSP modules. Recent work shows a single neural network can perform several jointly, with shared representations improving all tasks.
2. **Sub-10ms latency budgets** — Hearing aids, earables, and far-field streaming devices impose end-to-end algorithmic latency ceilings of 2–10 ms (perceptual thresholds for own-voice echo: >10 ms disturbing, >15–20 ms severely disturbing). This rules out many high-latency SE architectures and forces algorithmic redesign.

Neither trend is independently novel. The **new insight** from the 2025–2026 corpus is that the two must be co-designed: latency budgets shape which multi-task fusion strategies are viable, and multi-task objectives reshape the latency–quality frontier.

## Sources Synthesized

| Source | Year | Tasks Joint | Latency | Compute | Key Mechanism |
|--------|------|-------------|---------|---------|---------------|
| [[sources/indenbom-2023-deepvqe\|DeepVQE (Indenbom)]] | 2023 | AEC + NS + DR | 20 ms | 7.5M params, 3.66 ms/frame | Cross-attention alignment + CCM |
| [[sources/chen-2023-ultra-dual-path-compression\|Ultra Dual-Path Compression (Chen)]] | 2023 | AEC + NS (joint) | 10 ms hop (20 ms window) | **0.11–0.48M params, 57–1822M MACs/s** (ratio-tunable) | DPT-FSNet + grid-searched time×frequency compression + PostNet |
| [[sources/seidel-2024-bark-scale-nn-residual-suppression\|Bark-AEC (Seidel)]] | 2024 | AEC + NS (hybrid) | 8 ms (frame shift 128 @ 16 kHz) | 1.58M params, 235 MMACs/s | Subband-NLMS LEC + NSNet2-style FC/GRU on 86 Bark bands |
| [[sources/castelli-2025-embedded-joint-aec-ns\|TinyVQE (Castelli)]] | 2024 | AEC + NS (joint) | 16 ms (hop) | **0.11M params, 0.48 MMACs/frame**, 420 KB SRAM | DeepVQE-s compressed; HiFi4 DSP custom CCM intrinsics |
| [[sources/hao-2025-l3c-deepmfc\|L3C-DeepMFC (Hao)]] | 2025 | Hearing-aid feedback cancellation | **4 ms** | 0.31M params, 0.43 G/s MACs | Gain-shape complex mapping + closed-loop FT |
| [[sources/li-2025-echofree-neural-aec\|EchoFree (Li)]] | 2025 | AEC only (lightweight) | — | **0.28M params, 30 MMACs/s** | U-Net on Bark + two-stage WavLM SSL loss |
| [[sources/zhao-2026-halo-half-frame-rate-adaptive-operator\|HALO (Zhao)]] | 2026 | SE backbone accelerator (plug-in) | **0 ms added** | Halves internal frame rate (≈½ MACs) | Dynamic-conv frame-rate reduction |
| [[sources/ashur-2026-acoustic-howling-suppression-fine-tuning\|Ashur & Cohen]] | 2026 | NS + AHS (joint via fine-tuning) | **0 ms added** | Same as Denoiser baseline | Data-mixing fine-tuning (60-40 ratio) |
| [[sources/ostergaard-2026-own-voice-cancellation\|OVC (Østergaard)]] | 2026 | OVC (target-speaker removal) | **2 ms** | 0.33 GMAC/s, RTF 0.82–1.69 | Mamba-MinGRU linear RNN |
| [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement\|RT-Tango (Benslimane)]] | 2026 | Distributed binaural SE | **8 ms** | 35 MMACs/s | ERB + GRNN + FRS + asymmetric STFT |
| [[sources/rath-2026-minimum-delay-block-size\|Rath & Geier]] | 2026 | Theoretical lower bound | — | O(1) closed form | $\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})$ |
| [[sources/larraza-2026-fast-ulcnet-speech-enhancement\|Fast-ULCNet (Larraza)]] | 2026 | NS (single-task) | 16 ms (hop) | **0.338M params, 1.69 MMACs**, RTF 0.60 ARM | GRU→FastGRNN replacement + Comfi-FastGRNN drift correction |

## Insight 1: Multi-Task Fusion Strategies Form a Spectrum

The corpus reveals three distinct strategies for combining tasks, each with different latency implications:

### Strategy A — Single-Model Multi-Task via Shared Backbone (DeepVQE)

[[sources/indenbom-2023-deepvqe\|DeepVQE]] processes AEC, NS, and DR through a single residual-CNN autoencoder with a [[concepts/cross-attention-alignment\|cross-attention alignment block]] for mic/far-end soft alignment, a GRU bottleneck, and a [[concepts/complex-convolving-mask\|complex convolving mask (CCM)]] for output reconstruction. A single 7.5M-parameter model wins both ICASSP 2023 AEC Challenge (final 0.854) and DNS Challenge (final 0.582) — competitors used task-specific models.

- **Latency cost**: 20 ms algorithmic (frame size 20 ms + 10 ms hop). Acceptable for Microsoft Teams (deployed to hundreds of millions of users) but **disqualifies hearing-aid / earable use**.
- **Why shared backbone wins**: alignment block stabilizes the delay distribution between mic and far-end; CCM leverages magnitude + phase from neighboring T-F bins. Ablations show alignment and CCM each contribute largest gains.

### Strategy A' — Embedded Compression of a Shared Backbone (Castelli / TinyVQE)

[[sources/castelli-2025-embedded-joint-aec-ns\|Castelli 2024 (NXP)]] provides the corpus's only industrial deployment case study: re-implementing DeepVQE-s at 16 kHz and compressing it through a six-stage pipeline onto an NXP i.MX RT600 MCU with a Cadence HiFi4 DSP (600 MHz, 4.5 MB on-chip SRAM). The pipeline — [[concepts/mobilevqe\|MobileVQE]] (depthwise-separable convs, −7.7× MACs) → parameter cutting → custom HiFi4 intrinsics for the [[concepts/complex-convolving-mask\|CCM]] (−1.8× inference time at unchanged quality) → ReLU replacing ELU (HiFi4 FP32-optimized kernel) → MACs pruning → LayerNorm removal — yields [[concepts/tinyvqe\|TinyVQE]] at 0.11M params / 0.48 MMACs/frame / 2.32 ms per 16 ms frame, with DT EchoMOS within 0.20 of the DeepVQE-s baseline. A rejected 92k-parameter variant shows the practical quality floor (DT Echo 4.24, DT Deg 3.63). This anchors the **deployment-cost** end of the multi-task spectrum: a server-grade joint AEC+NS architecture can be ported to a fixed-point-capable audio MCU if (a) the CCM kernel is rewritten as DSP intrinsics and (b) ~0.1–0.2 MOS degradation is acceptable. The next planned step is 16×8 quantization-aware training, which would exploit the HiFi4's fixed-point MAC path.

### Strategy B — Task Reframing Without Architectural Change (Ashur, OVC)

Instead of bolting tasks onto a shared backbone, **reframe** the task so a pretrained network already handles it:

- [[sources/ashur-2026-acoustic-howling-suppression-fine-tuning\|Ashur & Cohen 2026]] fine-tune a pretrained [[concepts/denoiser-network\|Denoiser (DEMUCS-derived)]] network by mixing Valentini-Botinhao noise-reduction data with offline-generated howling samples at a 40:60 ratio. No architectural change, no recursive training, **no added inference latency**. Achieves highest PESQ at gains $G \in \{2, 2.5, 3\}$ among all evaluated AHS methods, with PESQ drop of only ~0.05 across gain levels (vs. 0.5–0.6 for HybridAHS and NKal-AHS).
- [[sources/ostergaard-2026-own-voice-cancellation\|OVC (Østergaard 2026)]] reframes target-speaker extraction (TSE) as its complement: remove the enrolled speaker from a mixture, preserve the rest. This reframing aligns the objective with the actual perceptual problem (echo-like own-voice artifacts from streaming round-trip delay) rather than the conventional TSE objective.

**Latency payoff**: reframing carries zero architectural overhead, so the latency budget is dictated entirely by the underlying backbone. OVC achieves 2 ms because the underlying Mamba-MinGRU masker has kernel size $L=32$ at 16 kHz; Ashur adds 0 ms because Denoiser's forward pass is unchanged.

### Strategy C — Distributed Multi-Stage Pipeline (RT-Tango)

[[sources/benslimane-2026-rt-tango-binaural-speech-enhancement\|RT-Tango]] distributes binaural SE across two physically separated ear-nodes in a hearing-aid pair, preserving Tango's two-stage scheme (SN-DNN → SDW-MWF → exchange → MN-DNN → SDW-MWF). Tasks here are spatial filtering + neural masking + multi-channel Wiener filtering, with limited inter-node communication.

- **Latency budget**: 8 ms (asymmetric STFT: 32 ms analysis / 8 ms synthesis window).
- **Efficiency**: 35 MMACs/s — 6× cheaper than GTCRN at the same 4 ms hop, 18× cheaper than Tango baseline.
- **Trade-off**: distributed coordination adds an architectural dimension absent from single-device multi-task models.

### Spectrum Summary

| Strategy | Latency Flexibility | Multi-Task Mechanism | Example |
|----------|---------------------|----------------------|---------|
| A. Shared backbone | Constrained by backbone frame size | Cross-attention / shared encoder | DeepVQE (20 ms) |
| A'. Embedded compression of shared backbone | Constrained by backbone frame size (fixed after deployment) | Same as A, plus stage-wise compression (depthwise conv, intrinsics, ReLU, pruning) | TinyVQE (16 ms hop, HiFi4 DSP) |
| B. Task reframing | Inherited from backbone | Data-mixing / objective redefinition | Ashur (0 ms added), OVC (2 ms) |
| C. Distributed multi-stage | Constrained by inter-node comm | Pipeline of specialized stages | RT-Tango (8 ms) |

**Key takeaway**: Strategy B is the most latency-friendly because it adds zero architectural overhead. Strategy A is most flexible for joint optimization but pays the backbone's latency cost. Strategy C is forced by physical deployment constraints (separated earpieces) and adds an inter-node bandwidth dimension.

## Insight 2: The Latency Budget Drives a New Algorithmic Hierarchy

The 2025–2026 corpus shows a clear stratification of techniques by the latency budget they enable:

### Tier 1 — Frame-Based STFT Processing (≥10 ms)

Traditional STFT-based SE uses 20–32 ms analysis windows with 50% overlap (10–16 ms hop). This is the regime of DeepVQE (20 ms), original DeepMFC (10 ms), and most CRN/DPCRN variants. Suitable for:
- Desktop / cloud communication (DeepVQE in Teams)
- Smart speakers
- PA systems (Ashur's Denoiser baseline)

### Tier 2 — Asymmetric STFT (4–8 ms)

[[concepts/asymmetric-stft\|Asymmetric STFT]] decouples analysis window length (preserving frequency resolution) from synthesis window length (controlling reconstruction latency). RT-Tango uses 32 ms analysis / 8 ms synthesis → 8 ms total. L3C-DeepMFC uses a modified overlap-add with 2 ms hop → 4 ms total.

The cost: smaller synthesis windows produce more spectral leakage, requiring careful window design (Hanning loss in L3C-DeepMFC outperforms tapered windows by 2+ PESQ points).

### Tier 3 — Time-Domain / Sample-Level (≤2 ms)

[[sources/ostergaard-2026-own-voice-cancellation\|OVC]] achieves 2 ms by abandoning STFT entirely for a time-domain TasNet variant with kernel size $L=32$ at 16 kHz. The encoder is a learned 1-D convolution; the masking network uses [[concepts/mamba-mingru\|Mamba-MinGRU]] blocks. This is the only path to sub-4 ms latency in the corpus.

### Tier 4 — Latency-Neutral Accelerators (0 ms added)

[[sources/zhao-2026-halo-half-frame-rate-adaptive-operator\|HALO]] is a plug-in module that halves the internal frame rate processed by any STFT backbone, freeing compute budget for channel widening. Because the rate-reduction and rate-restoration operators are causal and operate within the existing STFT grid, **algorithmic latency is unchanged**. HALO improves all metrics across GTCRN, DPCRN, LiSenNet, and UL-UNAS backbones at matched MAC/s — a strictly Pareto-improving accelerator.

### Latency Hierarchy Table

| Latency Tier | Representative | Technique | Where Used |
|--------------|----------------|-----------|------------|
| ≥20 ms | DeepVQE | Standard STFT, 20 ms frame | Teams, desktop comms |
| 8–10 ms | RT-Tango, DeepMFC | Asymmetric STFT / standard STFT small hop | Hearing aids (borderline) |
| 4 ms | L3C-DeepMFC | Modified OLA, 2 ms hop | Hearing aids |
| 2 ms | OVC | Time-domain TasNet | Far-field streaming, earables |
| 0 ms added | HALO, Ashur FT | Plug-in / fine-tuning | Any backbone (orthogonal) |

**Key takeaway**: The shift from Tier 1 to Tier 4 is **not** a single architectural substitution but a stack of orthogonal techniques. HALO and Ashur's fine-tuning are latency-neutral and can be combined with any of Tiers 1–3. RT-Tango's asymmetric STFT can in principle be combined with HALO. The frontier is the Cartesian product of these techniques, not a single "best" architecture.

## Insight 3: Linear RNNs / SSMs Are Replacing LSTM/ConvTasNet in Streaming SE

A recurring structural shift across 2026 sources: **linear RNNs and state-space models (SSMs) are taking over streaming SE roles traditionally held by LSTM and ConvTasNet**.

### Evidence

- **OVC** replaces ConvTasNet-based TD-SpeakerBeam auxiliary network with a bidirectional linear RNN encoder — *improving* SDR on the F condition (13.57 vs. 13.42 dB) while cutting auxiliary compute from 1.67 to 0.26 GMAC/s (6.4× reduction). The main masker is built from Mamba blocks with [[concepts/mingru\|MinGRU]] temporal mixing.
- **RT-Tango** uses a [[concepts/grouped-recurrent-neural-network\|Grouped RNN (GRNN)]] that partitions the hidden state into $G$ groups, reducing recurrent complexity from $\mathcal{O}(H^2)$ to $\mathcal{O}(H^2/G)$. Asymmetric grouping ($G=8$ for SN-DNN, $G=2$ for MN-DNN) reflects differing group-sensitivity per stage.
- **HALO** is backbone-agnostic but its largest gains on small backbones (GTCRN, DPCRN-ultralight) suggest that the future of small-model SE lies in **frame-rate reduction + linear-RNN-style efficient temporal mixing**, not deeper ConvTasNet stacks.

### Why Linear RNNs Win in Streaming

1. **Parallel training, linear inference**: MinGRU's recurrence $\mathbf{h}_t = (1-\mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t$ is a linear recurrence expressible as an associative scan — parallelizable on GPU during training, $\mathcal{O}(1)$ per step at inference.
2. **Long context**: Mamba's selective state-space mechanism captures long-range dependencies that LSTMs handle poorly beyond ~100 steps.
3. **Small-state compute**: GRNN's grouped hidden state achieves $\mathcal{O}(H^2/G)$ without sacrificing cross-band modeling (via representation rearrangement).
4. **Causality-preserving**: linear RNNs are naturally causal; bidirectionality (as in OVC's auxiliary encoder) is added via Hydra bidirectionality without breaking streaming.

**Gap in existing synthesis**: [[synthesis/computational-efficiency-evolution\|Computational Efficiency Evolution]] discusses RNN BPTT vs. FEP memory bottlenecks in ANC but does not cover the SSM/linear-RNN replacement strategy. This synthesis fills that gap for SE.

## Insight 4: Temporal Redundancy Is the New Efficiency Frontier

Four independent sources spanning 2023–2026 converge on the same insight: **adjacent STFT frames are highly redundant due to 50% overlap, and exploiting this redundancy is cheaper than slimming the backbone**.

- **Chen et al. 2023 (Ultra Dual-Path Compression)**: [[concepts/frame-skip-prediction\|Frame-Skip Prediction]] runs the heavy mask estimator once every $r$ frames and copies the predicted mask to the $r-1$ skipped frames. Skip prediction alone suffers from unmatched masks (DT WB-PESQ drops from 2.78 to 2.14 at 8×), but a lightweight [[concepts/post-processing-network\|PostNet]] (67K params, 15M MACs/s, 1-layer GRU + convs) recovers +0.33 WB-PESQ at 8×. This is the earliest corpus example of explicit temporal-redundancy exploitation with a learned refinement module.
- **HALO (2026)**: Halves the internal frame rate via dynamic-convolution-based rate reduction/restoration. PESQ +0.097, SI-SNR +0.51 dB on GTCRN at matched MAC/s. Ablation shows simple decimation + duplication is the worst HALO variant — adaptive gating is essential.
- **RT-Tango (2026)**: [[concepts/fixed-rate-skipping\|Fixed-Rate Skipping (FRS)]] runs the mask estimator at 1/4 (SN-DNN) or 1/2 (MN-DNN) rate and reuses the previous mask in between. FRS preserves quality within 0.2 dB of baseline; learned skip gates (Skip RNN, TinyLSTM) degrade MN-DNN SI-SDR from 4.5 to 3.3–3.8 dB despite ~80% effective skip ratios.
- **L3C-DeepMFC (2025)**: Modified overlap-add using only current + next frames (vs. full overlap-add) — explicit recognition that 2 ms hop creates redundancy exploitable for latency reduction.

**Three temporal-redundancy strategies compared**:

| Strategy | Source | Where it operates | Refinement | Cost |
|----------|--------|-------------------|-----------|------|
| Frame-Skip Prediction + PostNet | Chen 2023 | T-F feature inside backbone | Learned (1-layer GRU + convs) | 67K params, 15M MACs/s |
| HALO rate reduction/restoration | Zhao 2026 | T-F feature inside backbone | Learned (dynamic conv) | Larger (adaptive gating) |
| Fixed-Rate Skipping | Benslimane 2026 | Whole backbone invocation | None (fixed schedule) | 0 added params |

**Why FRS beats learned skipping in RT-Tango**: learned skip gates introduce additional MACs to decide whether to skip, and their training signal is noisy. FRS commits to a fixed schedule, eliminating decision overhead.

**Why Chen 2023 uses learned refinement despite RT-Tango's finding**: Chen compresses the **T-F feature** (so the backbone still runs on every frame, just on a shorter feature), whereas FRS skips the whole backbone. The two strategies operate at different levels and are in principle complementary — FRS can be applied on top of any backbone, including one that already uses frame-skip prediction + PostNet internally.

**Combined implication**: HALO's frame-rate reduction, RT-Tango's FRS, and Chen's frame-skip prediction + PostNet are three points on a spectrum of temporal-redundancy exploitation. HALO compresses within the backbone with adaptive gating; Chen compresses within the backbone with fixed copy + learned refinement; FRS skips backbone invocation entirely. A combined HALO + FRS configuration is unexplored but predictably Pareto-improving. Chen + FRS combined would skip both backbone invocation and intra-backbone refinement — also unexplored.

## Insight 5: Training Paradigm Innovations Match Architecture Innovations

The 2025–2026 corpus shows training-side innovations as impactful as architectural ones:

### Cross-Attention Soft Alignment (DeepVQE)

DeepVQE's [[concepts/cross-attention-alignment\|alignment block]] addresses the mic/far-end delay estimation problem — previously the domain of DSP-based delay estimation. The block learns a soft delay distribution $\mathbf{D} \in \mathbb{R}^{t \times d_{\max}}$ via cross-attention with a convolutional stabilizer. Ablation: surpasses both DSP alignment and prior cross-attention methods, especially on WER.

### Closed-Loop Fine Tuning (L3C-DeepMFC)

[[concepts/closed-loop-fine-tuning\|Closed-loop fine tuning]] addresses the training-estimation mismatch in feedback cancellation: open-loop training never sees the closed-loop dynamics of the feedback path. L3C-DeepMFC dynamically generates feedback mixtures in a simulated hearing aid during fine-tuning, recovering performance gap vs. full DeepMFC at 32× fewer parameters.

### Data-Mixing Fine Tuning (Ashur)

Ashur's 60-40 howling/noise mixing ratio is the sweet spot — PESQ drops <1% versus original Denoiser, while AHS robustness improves monotonically up to 60% howling data. Above 60%, the model over-suppresses narrowband components at the expense of broadband speech. This is the first work to **explicitly trade AHS robustness against SE preservation in a controlled manner** — a multi-task trade-off curve, not a single operating point.

### Two-Stage SSL Loss for Lightweight AEC (EchoFree)

[[sources/li-2025-echofree-neural-aec\|EchoFree]] introduces a two-stage training strategy that uses a frozen [[concepts/self-supervised-speech-representation\|WavLM-Large]] as a multi-layer embedding teacher for a 278K-parameter AEC post filter:

- **Stage 1 (coarse)**: SSL loss only — MSE between WavLM embeddings of estimated and ground-truth signals averaged over all $L$ layers.
- **Stage 2 (fine)**: weighted combination $10 \cdot \mathcal{L}_{\text{Bark}} + 0.5 \cdot \mathcal{L}_{\text{SSL}}$ — a perceptual [[concepts/bark-scale-spectral-features\|Bark-scale gain loss]] (fourth-order + second-order + cross-entropy) is added, with SSL loss kept as a representation-fidelity regularizer.

Ablation results on ICASSP 2023 AEC Challenge blind set:

| Training | ST FE EchoMOS | DT EchoMOS | DT DegMOS |
|----------|--------------:|-----------:|----------:|
| Conventional gain loss | 4.15 | 3.74 | 3.52 |
| SSL loss only | 4.15 | **3.91** | 3.46 |
| Two-stage (SSL → SSL+Bark) | **4.20** | 3.88 | **3.53** |

**Two key findings**: (1) SSL-only training beats conventional gain loss on double-talk echo suppression (+0.17 EchoMOS), confirming that SSL embeddings carry information useful for residual echo suppression beyond what a hand-crafted gain target provides. (2) Stage-2 fine-tuning with the perceptual Bark loss recovers ST FE / ST NE / DT Deg performance while sacrificing a small amount of DT EchoMOS — a controllable trade-off via the loss weights.

**Distinction from L3C-DeepMFC's closed-loop FT**: Both are two-stage strategies, but L3C-DeepMFC's second stage changes the **data distribution** (closed-loop simulated feedback) while keeping the loss fixed. EchoFree's second stage keeps the data fixed and **changes the loss** (adds perceptual Bark term). The two strategies are orthogonal and could in principle be combined.

### Negative Thresholded SDR with Silence Handling (OVC)

OVC extends SDR loss to handle silence (when only the enrolled speaker is present, the network should predict silence):

$$\mathbf{L}_{\mathrm{SDR}} = \begin{cases} \mathcal{L}^{\text{active}}(\hat{\mathbf{x}}, \mathbf{x}), & \text{if } \mathbf{x} \neq \mathbf{0} \\ \mathcal{L}^{\text{inactive}}(\hat{\mathbf{x}}, \mathbf{y}), & \text{if } \mathbf{x} = \mathbf{0} \end{cases}$$

This is necessary because OVC's "negative" objective (remove target speaker) means the target output is often silence — a case standard SDR loss handles pathologically.

## Insight 6: Theoretical Lower Bound Anchors the Engineering Frontier

[[sources/rath-2026-minimum-delay-block-size\|Rath & Geier 2026]] provides the **theoretical lower bound** for block-size adaptation latency:

$$
\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})
$$

This is relevant to the multi-task / low-latency synthesis in two ways:

1. **Engineering implications**: When a multi-task SE model is deployed as a plugin inside a host (DAW, hearing-aid DSP, OS audio stack), the host/plugin block-size mismatch adds an irreducible latency $\Delta$. For power-of-two block sizes (common in audio), $\Delta = \max(0, b_\text{plugin} - b_\text{host})$ — so a 64-sample plugin inside a 256-sample host adds 0 ms, but a 256-sample plugin inside a 64-sample host adds 192 samples (~12 ms at 16 kHz).
2. **Plugin size selection**: For sub-10ms hearing-aid budgets, the plugin block size must be small enough that $\Delta$ stays within budget. At 16 kHz, a 32-sample plugin (2 ms) inside any host with $\gcd \geq 1$ contributes at most 31 samples (~2 ms) of reblocking latency — consistent with OVC's 2 ms algorithmic latency target.

**Synthesis implication**: Rath & Geier's formula is the **floor** against which all engineering-tier techniques (asymmetric STFT, time-domain, FRS) are measured. Algorithmic latency improvements below the reblocking floor are masked by host/plugin buffering. This is why OVC's 2 ms is significant: it sits at the edge of what is theoretically achievable in a generic plugin host.

## Insight 7: Training-Stable RNNs Can Drift at Inference on Long Sequences

[[sources/larraza-2026-fast-ulcnet-speech-enhancement\|Larraza & de Koeijer 2026]] document a failure mode absent from the rest of the corpus: **a gated RNN whose training-time stability guarantee does not transfer to the inference-time forward pass over long streaming sequences**. The specific finding:

- [[concepts/fastgrnn\|FastGRNN]] (Kusupati et al., NeurIPS 2018) is provably stable during training, but its original length-invariance claim was validated only on sequences up to 1.63 s.
- Applied to >60 s audio signals for SE, FastGRNN's mean hidden-state magnitude drifts monotonically over time during inference, and SE quality degrades measurably (e.g., on the 90 s DNS Challenge test set, BAKMOS drops 3.95 → 3.62, SI-SDR drops 16.89 → 13.58).
- The root cause is structural: the FastGRNN state-update coefficients do not satisfy a sum-to-one constraint, so the state lacks a contraction guarantee over long horizons. This is a training-vs-inference gap, not a training failure.
- The proposed [[concepts/comfi-fastgrnn\|Comfi-FastGRNN]] adds two scalar trainable parameters ($\gamma$, $\lambda$) inspired by complementary filters in inertial-sensor fusion, and fully recovers long-sequence performance at essentially zero parameter/MAC cost.

**Synthesis implication**: The 2023–2026 SE corpus repeatedly replaces LSTM/GRU with linear RNNs / SSMs (Mamba-MinGRU in OVC, GRNN in RT-Tango) and praises their streaming properties — but none of those works validate on sequences longer than the standard ~10 s DNS test clip. Larraza & de Koeijer's result is a caution: **length-invariance claims validated on short test clips do not generalize to streaming deployment**. The standard 10 s DNS evaluation window is too short to surface state-drift failure modes. Future low-complexity SE works targeting real-time deployment should report long-sequence (>60 s) evaluation as a separate condition, and consider whether their chosen recurrent unit has a contraction guarantee on the forward pass (not just during training). Comfi-FastGRNN's complementary-filter approach is one parameter-efficient fix; whether the same drift affects Mamba-MinGRU, GRNN, and other linear-RNN replacements at streaming scale is an open question.

## Insight 8: Compression-Ratio Flexibility Is a First-Class Design Axis

[[sources/chen-2023-ultra-dual-path-compression\|Chen et al. 2023]] articulate a design axis that the rest of the corpus treats only implicitly: **the ability to tune computational cost over a wide range (4×–32×) without resizing the model**. Most works in the corpus fix a single operating point — DeepVQE at 7.5M params, RT-Tango at 35 MMACs/s, OVC at 0.33 GMAC/s, EchoFree at 30 MMACs/s. Chen et al. instead present a single 109K-parameter base architecture whose MACs/s can be tuned from 57M to 1822M by changing only the compression ratio, with model size staying under 0.5M parameters throughout.

**Why this matters for deployment**: real-world SE deployment targets span an order of magnitude in compute budget — from cloud communication (DeepVQE's 7.5M params) to embedded MCUs (Castelli's TinyVQE at 114K params). A compression-ratio-flexible architecture lets a single R&D investment cover multiple deployment tiers without re-training or re-architecting.

**Three flexibility strategies in the corpus**:

| Strategy | Source | Range | Model size change |
|----------|--------|-------|-------------------|
| Dual-path compression (T×F grid search) | Chen 2023 | 4×–32× (57M–1822M MACs/s) | <500K params throughout |
| Stage-wise surgical compression | Castelli 2024 | 610K → 114K params | Each stage re-trained |
| Backbone replacement (GRU→FastGRNN) | Larraza 2026 | Single point (0.338M params) | Single retrain |

**Trade-off**: Chen's compression-ratio flexibility comes at the cost of compression/decompression module overhead — at ratios >32× these modules begin to dominate cost. Castelli's stage-wise approach achieves higher per-stage compression (610K→114K = 5.4× param reduction) but each stage requires retraining and the operating point is fixed after deployment. The two strategies are complementary: Chen's dual-path compression can be applied to a Castelli-style compressed backbone to get ratio-flexibility at the embedded tier.

**Synthesis implication**: future low-complexity SE works should report a **compression-ratio curve** (quality vs. MACs/s) rather than a single operating point, so practitioners can choose the right point for their deployment tier. Chen et al. 2023 is the only source in the corpus that does this explicitly.

## Cross-Cutting Decision Matrix

For a practitioner choosing a multi-task SE architecture under a latency budget $L$:

| Latency Budget $L$ | Recommended Architecture | Multi-Task Strategy | Linear RNN? | Accelerator |
|--------------------|--------------------------|---------------------|-------------|-------------|
| $L \geq 20$ ms | DeepVQE-style shared backbone | A (shared encoder) | Optional | HALO |
| $10 \leq L < 20$ ms | Asymmetric STFT (RT-Tango-style) | A or C | GRNN recommended | HALO + FRS |
| $4 \leq L < 10$ ms | Modified OLA (L3C-DeepMFC) or asymmetric STFT | B (reframing) or C | Yes (GRNN/MinGRU) | FRS |
| $L < 4$ ms | Time-domain TasNet (OVC-style) | B (reframing) | Yes (Mamba-MinGRU) | — |
| Any | + Ashur-style fine-tuning for AHS / NS joint | B (data mixing) | — | Orthogonal |

## Open Questions & Future Directions

1. **Combined HALO + FRS**: HALO compresses within the backbone; FRS skips backbone invocations. Their interaction is unexplored. Predicted to be Pareto-improving but with diminishing returns on highly optimized backbones (UL-UNAS).
2. **Multi-task OVC + AHS + NS**: OVC handles own-voice, Ashur handles howling, DeepVQE handles AEC/NS/DR. No work combines all into a single model. The challenge is training data — each task requires distinct synthesis pipelines.
3. **Linear RNN for distributed binaural SE**: RT-Tango uses GRNN (grouped LSTM); Mamba-MinGRU has not been tried in a distributed two-stage pipeline. Potential for further MACs reduction at matched quality.
4. **Rath & Geier's formula as a deployment constraint**: No source in the corpus explicitly designs around the reblocking floor. A model co-designed with the host block size in mind (e.g., choosing $b_\text{plugin}$ to maximize $\gcd(b_\text{host}, b_\text{plugin})$) could recover otherwise-wasted latency budget.
5. **Cross-task trade-off curves**: Ashur's 60-40 ratio is a single point on a multi-task trade-off curve. No work systematically maps the Pareto frontier of (AHS robustness, NS quality, latency, compute) jointly.
6. **Pitch-aware OVC**: OVC's pitch analysis shows ~1 dB SDR difference depending on enrolled speaker's $f_0$ relative to other speakers. Pitch-conditioned adaptation is unexplored.

## Related Synthesis

- [[synthesis/computational-efficiency-evolution\|Computational Efficiency Evolution]] — RNN BPTT vs. FEP memory bottlenecks in ANC (this synthesis extends to SE and covers SSM/linear-RNN alternatives)
- [[synthesis/multi-modal-speech-enhancement\|Multi-Modal Speech Enhancement]] — BC/AC/IMU combination (complementary modality axis)
- [[synthesis/modern-headphone-anc-systems\|Modern Headphone ANC Systems]] — Hybrid ANC + BC + VAD + transparency (overlapping hardware target)
- [[synthesis/application-specific-anc\|Application-Specific ANC]] — Form-factor-driven ANC design (parallel SE-side story)

## Related Concepts

- [[concepts/cross-attention-alignment\|Cross-Attention Alignment]]
- [[concepts/complex-convolving-mask\|Complex Convolving Mask]]
- [[concepts/mamba-mingru\|Mamba-MinGRU]]
- [[concepts/mingru\|MinGRU]]
- [[concepts/asymmetric-stft\|Asymmetric STFT]]
- [[concepts/erb-scale\|ERB Scale]]
- [[concepts/grouped-recurrent-neural-network\|Grouped Recurrent Neural Network]]
- [[concepts/fixed-rate-skipping\|Fixed-Rate Skipping]]
- [[concepts/complex-spectrum-mapping\|Complex Spectrum Mapping]]
- [[concepts/closed-loop-fine-tuning\|Closed-Loop Fine Tuning]]
- [[concepts/deep-marginal-feedback-cancellation\|Deep Marginal Feedback Cancellation]]
- [[concepts/audio-latency\|Audio Latency]]
- [[concepts/acoustic-howling-suppression\|Acoustic Howling Suppression]]
- [[concepts/denoiser-network\|Denoiser Network]]
- [[concepts/block-size-adaptation\|Block Size Adaptation]]
- [[concepts/bezouts-identity\|Bézout's Identity]]
- [[concepts/gtcrn\|GTCRN]]
- [[concepts/td-speakerbeam\|TD-SpeakerBeam]]
- [[concepts/fast-ulcnet\|Fast-ULCNet]]
- [[concepts/munet\|μNet]]
- [[concepts/fastgrnn\|FastGRNN]]
- [[concepts/comfi-fastgrnn\|Comfi-FastGRNN]]
- [[concepts/dpt-fsnet\|DPT-FSNet]]
- [[concepts/dual-path-compression\|Dual-Path Compression]]
- [[concepts/trainable-frequency-compression\|Trainable Frequency Compression]]
- [[concepts/frame-skip-prediction\|Frame-Skip Prediction]]
- [[concepts/post-processing-network\|Post-Processing Network]]
