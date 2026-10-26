---
type: synthesis
created: 2026-10-26
updated: 2026-10-26
sources:
  - raw/papers/perez-2018-film-visual-reasoning/full-text.md
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
  - raw/papers/huang-2026-undf-configurable-directivity/full-text.md
  - raw/papers/huang-2026-neural-directional-filtering/full-text.md
  - raw/papers/yang-2026-direction-preserving-anc/full-text.txt
  - raw/papers/yuan-2026-open-ear-anc-smart-glasses/full-text.md
  - raw/papers/li-2026-geometry-conditioned-ssanc/full-text.md
tags:
  - conditioning
  - feature-modulation
  - deep-learning
  - cross-domain-analysis
  - film-layer
---

# FiLM Conditioning Across Domains

> Cross-source synthesis of nine papers spanning 2018–2026 that introduce or apply [[concepts/film-layer|Feature-wise Linear Modulation (FiLM)]] — from its origin as a visual-reasoning conditioning layer (Perez et al. 2018) through its adoption as the de facto conditioning mechanism in target speech extraction, neural directional filtering, and active noise control. The mechanism itself ($\gamma \odot \mathbf{F} + \beta$, two parameters per feature map) never changed; what varies is what gets encoded, where the modulation is injected, and what the conditioned network outputs.

## Sources Synthesized

| Source | Year | Domain | Conditioning input | FiLM generator | Modulated (FiLM-ed) network | Injection point |
|--------|------|--------|-------------------|-----------------|------------------------------|----------------|
| [[sources/perez-2018-film-visual-reasoning\|Perez et al. 2018]] | 2018 | Visual QA | Question text (word sequence) | [[concepts/gated-recurrent-unit\|GRU]], 4096 units + affine projections | CNN visual pipeline (128 maps, ResBlocks) | Per residual block, 4 layers |
| [[sources/zmolikova-2023-neural-target-speech-extraction-overview\|Zmolikova et al. 2023]] | 2023 | TSE (survey) | Clue embedding $\mathbf{E}_s$ (speaker/face/spatial) | Linear maps $L_1, L_2$ | Extraction module (encoder–decoder) | Fusion layers, typically in the lower part |
| [[sources/li-2026-geometry-conditioned-ssanc\|Li 2026 (GC-SSF)]] | 2026 | TSE | Array geometry via [[concepts/doa-microphone-positional-encoding\|DOA-MPE]] | Encoder network | [[concepts/spatially-selective-nonlinear-filter\|SSF]] extraction network | Intermediate features of the spatial filter |
| [[sources/li-2026-geometry-conditioned-tse\|Li & Doclo 2026]] | 2026 | TSE | [[concepts/target-steering-vector\|Target steering vector]] or [[concepts/gcc-phat-spatial-mask\|GCC-PHAT spatial mask]] | Encoder network | Extraction network (same encoder + FiLM integration as GC-SSF) | Same as GC-SSF |
| [[sources/uphaus-2026-directivity-low-latency\|Uphaus et al. 2026]] | 2026 | Neural directional filtering | 72-dim directivity-pattern vector (5° samples) | Linear map to $C=96$ | [[concepts/film-osn\|FiLM-OSN]] narrow-band Mamba blocks | Per narrow-band block, 10 ms latency |
| [[sources/huang-2026-undf-configurable-directivity\|Huang, Chetupalli & Habets 2026]] | 2026 | Neural directional filtering | Steering angle via sinusoidal embedding ($d_{\mathrm{emb}}=72$) | Two linear layers → $(\alpha,\beta)\in\mathbb{R}^{512}$ | [[concepts/film-jnf\|FiLM-JNF]] (FT-JNF backbone) | Per frequency-band block |
| [[sources/huang-2026-neural-directional-filtering\|Huang et al. 2026 (NDF)]] | 2026 | Neural directional filtering | Continuous steering angle | Same FiLM-JNF mechanism | Journal-style NDF, 4-mic 3 cm array | Per frequency-band block, enables off-grid steering |
| [[sources/yang-2026-direction-preserving-anc\|Yang et al. 2026]] | 2026 | ANC | Desired direction $[\cos\theta_d, \sin\theta_d]^T$ | Small MLP + per-block FiLM heads | Acoustic encoder (3 Conv–BN blocks) → decoder emits FIR **filter bank** | Per Conv–BN block; zero-init heads |
| [[sources/yuan-2026-open-ear-anc-smart-glasses\|Yuan, Liu & Xiao 2026]] | 2026 | ANC (open-ear glasses) | Per-user 1024-tap secondary-path estimate → FFT → MLP → 128-d embedding | FiLM head from embedding | U-Net LSTM bottleneck → decoder emits 2048-tap FIR filters | Single point: the LSTM bottleneck |

## Insight 1: The Mechanism Is Invariant; Everything Else Is a Design Choice

Across nine papers, the modulation equation is literally the same two-parameter-per-feature-map affine transform Perez et al. defined in 2018. What changed is three orthogonal design axes:

1. **What is encoded**: natural-language questions → abstract clue embeddings → array-geometry encodings → physics-derived features (steering vectors, DOA codes) → signal-derived per-user estimates (secondary-path FFTs).
2. **What is modulated**: a vision CNN → extraction networks → narrow-band Mamba blocks → *filter-estimation* networks whose output is itself a control-filter bank.
3. **Where it is injected**: per residual block → per frequency-band block → a single LSTM bottleneck.

The mechanism survived every one of these substitutions without modification — the strongest evidence for the generality claim in the original paper ("a general conditioning layer").

## Insight 2: Modulation Must Start as Identity

Both the original paper and the audio applications converge on the same initialization trick, rediscovered independently: Perez et al. output $\gamma = 1 + \Delta\gamma$ because zero-centered $\gamma$ would zero out activations *and gradients* at initialization; Yang et al. (DP-ANC) **zero-initialize the FiLM heads** so the initial modulation is exactly the identity mapping. The pattern: FiLM is always grafted onto a pretrained-capable base network, and the graft must be transparent until training moves it. Any new FiLM application should adopt one of these two forms.

## Insight 3: What Gets Encoded Matters More Than the Mechanism

Three independent lines of evidence converge on the conclusion that **the conditioning-input representation dominates the modulation mechanism**:

- Zmolikova et al. 2023 report that in TSE, the *choice* among five fusion layers (concatenation, addition, multiplication, FiLM, factorized) has "rather insignificant" impact — with multiplication and FiLM generally performing well.
- Li & Doclo 2026 keep the FiLM mechanism fixed and swap the conditioning input: explicit, physics-derived features ([[concepts/target-steering-vector|TSV]] or [[concepts/gcc-phat-spatial-mask|GCC-PHAT mask]]) beat abstract learned DOA-MPE embeddings on all metrics (+0.31 PESQ).
- Huang, Chetupalli & Habets 2026 compare FiLM conditioning against initial-state conditioning (PV-JNF) with the *same* conditioning goal: PV-JNF collapses on unseen pattern orders, scalings, and steering directions (8.1 vs 19.5 dB SDR), while FiLM degrades gracefully.

FiLM is a commodity; the encoder in front of it is where representational work pays off.

## Insight 4: From Modulating Features to Modulating Filter Generators

The audio lineage shows a clear drift of the conditioned output "up the stack":

1. **Signal-level** (TSE, NDF): FiLM modulates features of a network that outputs *audio samples/spectra* — the conditioned quantity is the enhanced signal itself.
2. **Filter-estimation level** (DP-ANC, open-ear ANC): FiLM modulates a network whose output is a *complete FIR control-filter bank* — the conditioned quantity is a filter, not a signal. Yang et al. make this explicit: the FiLM-ed encoder emits the full multichannel bank in one forward pass (0.00946 GMACs vs ≈29.4 for the analytical solve).

Perez et al.'s observation that FiLM is "a form of hypernetwork" (one network generating parameters of another) anticipates this drift: at the filter-estimation level, FiLM is two hypernetwork levels deep — the FiLM generator conditions a network that is itself generating filter parameters.

## Insight 5: FiLM as Per-Instance State Compression

The open-ear ANC application (Yuan, Liu & Xiao 2026) reveals a deployment pattern the original paper never explored: FiLM as a mechanism for **user adaptation without retraining**. The entire per-user state is a ~512-byte secondary-path estimate (compressed by an MLP into the FiLM conditioning vector), versus ~16 MB of per-user retrained weights. The secondary-path-conditioned system gains +1.6 dB mean reduction with calibration and cuts inter-user variability from 1.5 dB to 0.4 dB std. Generalizing: whenever instance-specific information exists in low-dimensional form (a direction code, a geometry, a path estimate), FiLM converts it into network behavior at negligible memory cost.

## Insight 6: Why Audio Inherited FiLM Rather Than Attention

Perez et al.'s cost analysis explains the adoption pattern in audio: FiLM's cost is **independent of resolution** (two parameters per feature map), while attention and Relation Networks scale quadratically with spatial (or temporal-frequency) resolution. The audio applications that adopted FiLM are precisely the ones under hard latency/compute budgets: 10 ms-latency hearing-aid filtering (FiLM-OSN, 700k params), wearable ANC filter estimation (0.00946 GMACs), and streaming TSE. In these settings, cross-attention conditioning blocks would dominate the compute budget, while a per-block linear projection from a small embedding is nearly free.

## Open Questions

1. **FiLM vs cross-attention in audio**: no ingested paper compares FiLM against transformer-style cross-attention conditioning *on the same audio task* — the vision comparison (Perez 2018 vs Stacked Attention) suggests FiLM wins at equal or lower cost, but audio TF-grids may behave differently.
2. **Where exactly to inject**: TSE evidence says lower layers (Zmolikova 2023); NDF injects per frequency-band block; open-ear ANC injects at a single bottleneck. No systematic placement study exists for audio.
3. **Time-varying conditioning**: Perez 2018 conditions once per question; hearing-aid directivity can vary per frame. Which audio tasks benefit from per-frame vs per-utterance conditioning remains untested.
4. **Analogy-making in parameter space for audio**: Perez 2018's zero-shot linear combination of $(\gamma, \beta)$ has no audio counterpart — could a "steering-angle arithmetic" interpolate unheard array geometries or directivity patterns?

## Related Concepts

- [[concepts/film-layer|FiLM Layer]] — the mechanism this synthesis tracks
- [[concepts/film-osn|FiLM-OSN]] — 10 ms-latency directivity-conditioned filtering
- [[concepts/film-jnf|FiLM-JNF]] — continuous-steering conditioning
- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]] — array-geometry conditioning
- [[concepts/doa-microphone-positional-encoding|DOA-Microphone Positional Encoding (DOA-MPE)]]
- [[concepts/target-steering-vector|Target Steering Vector (TSV) Feature]]
- [[concepts/direction-preserving-anc|Direction-Preserving ANC]] — filter-estimation conditioning
- [[concepts/virtual-in-ear-sensing|Virtual In-Ear Sensing]] — per-user secondary-path conditioning
- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]] — fusion-layer conditioning
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit (GRU)]] — the original FiLM generator

## Related Sources

- [[sources/perez-2018-film-visual-reasoning|Perez, Strub, de Vries, Dumoulin & Courville 2018]] — origin of FiLM; mechanism, ablations, γ/β analysis
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023]] — fusion-layer survey establishing FiLM's place among conditioning alternatives in TSE
- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned SSF]]
- [[sources/li-2026-geometry-conditioned-tse|Li & Doclo 2026: Geometry-Conditioned TSE with Spatial Features]] — conditioning-input ablation (explicit features vs embeddings)
- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: FiLM-OSN]]
- [[sources/huang-2026-undf-configurable-directivity|Huang, Chetupalli & Habets 2026: UNDF]] — FiLM vs initial-state conditioning generalization
- [[sources/huang-2026-neural-directional-filtering|Huang et al. 2026: Neural Directional Filtering]]
- [[sources/yang-2026-direction-preserving-anc|Yang et al. 2026: Direction-Preserving ANC]]
- [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026: Open-Ear ANC Smart Glasses]]
