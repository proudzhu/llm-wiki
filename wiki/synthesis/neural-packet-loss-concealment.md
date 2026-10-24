---
type: synthesis
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/lee-2016-dnn-plc/full-text.md
  - raw/papers/valin-2022-real-time-plc/full-text.md
  - raw/papers/nguyen-2023-predictive-plc/full-text.md
  - raw/papers/westhausen-2022-tplcnet/full-text.md
  - raw/papers/mezza-2024-hybrid-plc/full-text.md
tags:
  - packet-loss-concealment
  - real-time
  - speech-coding
  - neural-network
  - lpcnet
  - blind-plc
  - full-band
  - networked-music-performance
  - hybrid-dsp-dnn
  - test-time-adaptation
  - music-plc-challenge
---

# Neural Packet Loss Concealment

> Cross-source synthesis of five neural PLC systems spanning 2016–2024 (plus a 2025–2026 web-survey outlook section covering the music-PLC challenge, test-time adaptation, diffusion inpainting and unified restoration models): DNN frame-feature regression (Lee & Chang 2016), on-demand seq2one time-domain prediction (Westhausen & Meyer 2022), hybrid generative + predictive vocoder concealment (Valin et al. 2022), blind full-band predictive concealment (Nguyen, Nguyen & Khong 2023), and hybrid linear-AR + learned-residual concealment for networked music performance (Mezza et al. 2024). The papers trace the field's evolution along five axes — loss-metadata dependence, sample rate and signal domain (speech vs. music), inference regime (continuous vs. on-demand), what the network is asked to predict (waveform/features vs. a linear model's residual), and how each architecture exploits the model's *own previous output* during consecutive losses.

## The Problem

Voice packets lost in best-effort transport (RTP/UDP) must be concealed at the receiver within the playback deadline. Three constraints shape every design: real-time synthesis on CPU-class hardware; frequent transitions between received and synthesized audio requiring cross-fades and resynchronization; and drift of autoregressive synthesis during long bursts. Beyond ~100 ms of continuous loss, concealment becomes meaningless and the right behavior is to fade out naturally.

## Sources Synthesized

| Source | Year | Loss info | Rate | Architecture | Long-burst handling | Complexity |
|--------|------|-----------|------|--------------|--------------------|------------|
| [[sources/lee-2016-dnn-plc\|Lee & Chang 2016]] | 2016 | Informed | 16 kHz wideband | Two feed-forward DNNs regressing log-power spectra + phase of the missing frame from 11 preceding good frames | Recursive re-feeding of estimated features; cross-fading (roll-off $\alpha=3$) at boundaries; avoids muting-to-zero | Zero algorithmic delay; DNN matrix products, ~40% reducible by pruning |
| [[sources/valin-2022-real-time-plc\|Valin et al. 2022]] | 2022 | Informed | 16 kHz | Predictive GRU RNN estimates LPCNet features → causal LPCNet vocoder synthesizes samples; causal / non-causal (5 ms look-ahead) / Opus-codec modes | Linear decay of predicted $c_0$ after 100 ms, emulating a small room ($\mathrm{RT}_{60}=120$ ms) | 2.58 ms worst-case per 10-ms frame (i7-10810U); 13–14% of one CPU core steady-state |
| [[sources/westhausen-2022-tplcnet\|Westhausen & Meyer 2022]] | 2022 | Informed | 16 kHz | Seq2one BGRU predicts the lost 10-ms frame from a 6-frame (60 ms) context buffer — triggered **only when a loss is detected**; Hann-windowing + overlap-add smooths loss edges | Predicted frame written back to the context buffer; no explicit long-burst fading | Small 2.96 M MACs / 0.57 ms → Large 26.18 M MACs / 3.95 ms per 10-ms frame (i5-7267U); FF baseline 2.49 M MACs / 0.47 ms — cost paid **only during losses** |
| [[sources/nguyen-2023-predictive-plc\|Nguyen, Nguyen & Khong 2023]] | 2023 | **Blind** | **48 kHz full-band** | FRN: encoder (inter-frame RNN + intra-frame MLP on complex STFT) + LSTM predictor on log-Mel magnitude of the previous output + CNN joiner | Predictor reuses the previous *enhanced output* (pre-trained on clean targets); no explicit long-burst fading reported | 9.1M params; 4.1 ms per 10-ms chunk on one i9 3.0 GHz thread (RTF 0.41) |
| [[sources/mezza-2024-hybrid-plc\|Mezza et al. 2024]] | 2024 | Informed (configured for 10% losses) | **32 kHz music** (piano) | [[concepts/parcnet\|PARCnet]]: online AR(128) predictor in parallel with a 416 k feed-forward information-bottleneck network predicting the AR **residual**; 16-sample fade-in envelope + 25% forecast overshoot with linear cross-fade | Not addressed (10% evenly spaced losses; 10 ms packets); the AR branch carries the first samples | 416 k params; 8.1 ms per 10-ms packet at 32 kHz in unoptimized Python/PyTorch on a Ryzen 5900HS |

## Insight 1: Four Architectural Paradigms in Seven Years

- **Frame-feature regression (2016)** — treat the missing frame as a *prediction target*: regress its spectral features from a fixed window of good frames with a feed-forward DNN. Simple, zero-delay, but no generative model of speech dynamics; excels on short losses with informative context.
- **Hybrid generative + predictive (2022)** — decouple time scales: a *predictive* RNN controls the long-term spectral trajectory while a *generative* vocoder ([[concepts/lpcnet|LPCNet]]) synthesizes plausible samples. Be "creative" in extending a phoneme, never invent new words. This trades regression's brittleness for vocoder complexity.
- **On-demand seq2one prediction (2022)** — [[concepts/tplcnet\|tPLCnet]] inverts the operating regime: a time-domain BGRU runs *only when a loss is detected*, predicting the whole lost frame from a fixed 6-frame context buffer in one shot. Compute scales with the actual loss rate rather than the full audio stream — at the price of a bounded temporal context (which its ablation shows is sufficient: 4–7 frames already near-optimal, 15–20 frames detrimental).
- **Blind TF-domain reconstruction + prediction (2023)** — [[concepts/full-band-recurrent-network|FRN]] keeps everything in the complex STFT domain (no vocoder): an encoder branch reconstructs the current frame, a predictor branch predicts its magnitude from the previous output, and a joiner fuses the two. The RNN-transducer-inspired encoder/predictor/joiner split is the architectural descendant of both earlier ideas: regression (the predictor) and conditioning (the joiner).

The trajectory: as loss-metadata assumptions weakened (informed → blind), sample rate rose (16 → 48 kHz), and the inference regime forked (continuous → on-demand), architectures gained explicit *branches* rather than growing a single monolithic mapper.

A fifth paradigm appears once the *signal domain* changes rather than the metadata regime: **linear prediction + learned residual (2024)**. [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]] observe that music PLC is not speech PLC — sustained instrumental notes are quasi-harmonic, so a plain online $\mathrm{AR}(128)$ beats *every* deep baseline they tested (FRN, TF-GAN, PLAAE, LPCNet) on NMSE, PEAQ and PLCMOS at 32 kHz. The network's job then shrinks from waveform generation to residual estimation: PARCnet sums the AR forecast with a feed-forward prediction of the AR residual, using a 416 k-parameter network that runs in real time in unoptimized Python. In other words, the two branches of the 2022 hybrid are re-cut — not "generative synthesizer + predictive controller" but "linear predictor + nonlinear residual" — with the linear model taking the role LPCNet's excitation model used to play, and the network taking the role the spectral-envelope model used to play.

## Insight 2: Reusing the Previous Output Is the Field's Recurring Motif

All four papers converge on one mechanism — **the model consumes its own previous estimate during loss** — but formalize it differently:

- Lee & Chang 2016 *re-feed* the estimated features of a reconstructed frame as input for the next missing frame (recursive inference, no retraining).
- Valin et al. 2022 give the prediction RNN the previous *predicted* feature vectors during a burst, with asymmetric perceptual losses biasing the recursion toward safe predictions.
- Westhausen & Meyer 2022 transplant the idea to raw samples at the buffer level: the predicted 10-ms output frame is *written back into the context buffer*, so consecutive-loss predictions consume earlier predictions — Lee & Chang's recursive re-feeding, minus the DFT-domain feature detour.
- Nguyen et al. 2023 promote the idea to a **dedicated, pre-trained network branch** (the log-Mel LSTM predictor), explicitly citing both the decision-directed SNR estimator ([[concepts/decision-directed-a-priori-snr|Ephraim & Malah 1984]]) as the classical precedent and the RNN-transducer (Graves 2012) as the architectural pattern — and their ablation quantifies its value (real-trace LSD 1.081 → 0.946 over the encoder alone).

The ablation result gives the motif empirical teeth: reusing the previous output is not an inference-time trick but a first-class architectural component worth ~12% LSD on realistic traces.

## Insight 3: Loss-Mask Metadata Is Worth Less Than Model Capability

FRN is blind — no loss mask, no packet-size metadata, arbitrary packet sizes — yet it outperforms the *informed* tPLCnet ('Large', 3rd place Interspeech 2022 PLC Challenge) on PLCMOS, LSD, STOI, and PESQ at all tested loss rates (e.g., real-trace PESQ 2.797 vs. 2.532; 40%-loss STOI 0.746 vs. 0.704). The caveats are honest: FRN is bigger (9.1M vs. 5.7M params) and slower (4.1 vs. 2.7 ms per frame). The primary source adds a subtler caveat: tPLCnet's per-frame cost (26.18 M MACs for Large) is paid **only during losses**, whereas FRN's continuous-inference cost is paid for *every* received frame — so the efficiency comparison between on-demand and continuous regimes depends on the loss rate, and at low loss rates the seq2one design is cheaper despite the higher peak complexity.

Synthesis implication: for deployment contexts where packet metadata is unavailable (audio pipelines with underflow/overflow, non-RTP transports), a blind causal model is not a compromise — it can be the *better* engineering choice, since alignment between audio and packet streams is itself a failure-prone assumption that blind PLC eliminates.

## Insight 4: The Evaluation Ecosystem Grew Around the Interspeech 2022 Challenge

The papers share a converging evaluation substrate: two-state **Markov-chain loss generation** (parameterized by intra-state transition probabilities $(p_N, p_L)$ in FRN; burst losses in Lee & Chang) for controlled loss rates, plus **real loss traces collected from actual calls** for realism. tPLCnet serves as the bridge datum: a challenge top performer (3rd place tied, informed) that Valin et al. 2022 competed against and Nguyen et al. 2023 reimplemented as a baseline. Its primary source ([[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022]]) quantifies the challenge's objective-vs-subjective divergence: tPLCnet logged the **second-best PLC-MOS of all submissions (3.976)** — above the 2nd-place system's 3.744 — yet placed behind it on crowd-sourced CCR-MOS (−0.838 vs. −0.638), which the authors attribute to the 2nd-ranked model's additional speech enhancement. Objective PLC proxies and human preference can diverge even at 16 kHz, not only across sample-rate boundaries.

**Metric blind spots matter at full band.** PLCMOS, STOI, and PESQ only evaluate bands up to 8 kHz (STOI 5 kHz); only LSD covers the entire 24 kHz band of 48 kHz speech. FRN's case is instructive: its PLCMOS advantage over the offline GAN baseline TFGAN *disappears at high loss rates* (TFGAN wins PLCMOS at 20%/40%), yet FRN dominates LSD by ~250% (e.g., 1.682 vs. 3.714 at 40%) — the full-band metric and the ≤8 kHz metrics tell opposite stories about the same pair of systems. Full-band PLC papers must therefore report at least one full-band metric (LSD) alongside the standard proxies.

## Insight 5: Vocoder vs. No-Vocoder Is the Open Architectural Fork

Valin et al. 2022 demonstrate the vocoder route's strengths: natural-sounding synthesis under uncertainty, codec integration (replacing SILK PLC in Opus, seeding decoder state on the first received packet), and principled long-burst fading. Its costs: a GAN-style generative model's complexity budget and careful causal surgery on the vocoder's look-ahead.

FRN shows the vocoder-free route: a purely spectral complex-domain model trained end-to-end with a [[concepts/frequency-domain-loss|multi-resolution STFT loss]] ($\alpha = 0.3$ compression) — no adversarial training, no sampling loop — suffices to beat informed challenge systems at 48 kHz. What it gives up is precisely what the vocoder provides beyond ~100 ms bursts: FRN reports no long-burst fading mechanism, and its behavior past the 100 ms regime (where Valin's $c_0$ decay and Lee & Chang's muting-avoidance are explicitly designed) is untested.

tPLCnet marks the **discriminative extreme** of the no-vocoder route: a purely regression-based frame predictor with no generative component at all, whose feed-forward baseline already reaches PLC-MOS 3.81 (2.49 M MACs) — evidence that a large share of PLC quality comes from the framing/training setup rather than generative modeling, with the vocoder's "creativity" buying its margin on top of that floor.

**The fork acquires a third option on music.** [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]] run the comparison in the opposite domain — 32 kHz piano instead of 16 kHz speech — and the ranking changes materially. LPCNet's PLC variant, retrained on the same corpus, is comfortably real time (7.1 ms per packet, optimized C) but only mid-pack on quality; a plain $\mathrm{AR}(128)$ predictor beats it on every metric; and the residual-learning hybrid beats *all* deep baselines by large margins (MUSHRA +21.7 points over $\mathrm{AR}(128)$, and the only method inside the "perceptible but not annoying" PEAQ band and above the PLCMOS 2.0 threshold). Two conclusions follow for this synthesis. First, the "vocoder vs. no-vocoder" question is domain-dependent: LPCNet's learned-excitation machinery is tuned to source–filter speech, and on quasi-harmonic instrumental signals the classical all-pole model already explains most of the structure. Second, the *feed-forward → seam-click* penalty documented above is not intrinsic to feed-forward models — it is intrinsic to feed-forward models that generate the waveform; summing a feed-forward residual onto a smooth linear forecast plus a 16-sample fade-in removes the click without giving up parallel inference.

## Cross-Paper Comparability Caveat

The systems were **not all evaluated on a common benchmark**: Lee & Chang on a Korean/English speech corpus at 16 kHz against AMR-WB/HMM baselines; Valin et al. and Westhausen & Meyer on the *same* PLC Challenge blind test set (16 kHz, CMOS/WAcc — 2nd place, final score 0.835, vs. 3rd-tied, 0.790, so those two are directly comparable); Nguyen et al. on VCTK + challenge real traces (48 kHz); Mezza et al. on a 28 h MAESTRO piano subset at 32 kHz with 10% evenly spaced losses and a MUSHRA test rather than CMOS/WAcc — a different corpus, rate, loss model *and* evaluation paradigm (subjective audio quality instead of intelligibility). Numbers in the table above are indicative of each paper's *relative* findings, not a five-way ranking. A single-corpus, single-rate, single-trace comparison of regression / on-demand / hybrid-vocoder / blind-predictive / linear-residual architectures remains an open experiment.

## Outlook: 2025–2026 Developments (Web Survey)

> **Status**: the items in this section come from a web survey performed on 2026-10-24 (abstract/press-level facts, no full-text ingest). They are **not** in `raw/` and have **no wiki pages yet**, so they are referenced by external link rather than wikilink. Promote them to wikilinks as they get ingested. Everything above this section is sourced from ingested papers.

### 1. Music PLC now has its own challenge — but a small one

PLC for [[concepts/networked-music-performance|networked music performance]] moved from a handful of isolated papers to a recurring benchmark: the **IEEE-IS² Music Packet Loss Concealment Challenge**, run as a satellite of the IEEE International Symposium on the Internet of Sounds (sponsored by Sennheiser, organized by the Politecnico di Milano ISPL group that authored [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]]). Its 2025 edition ([challenge paper](https://doi.org/10.1109/is264627.2025.11284631), [dataset](https://zenodo.org/records/23041207), [repo](https://github.com/polimi-ispl/2025-music-plc-challenge)) differs from the speech challenge in three telling ways:

| Aspect | Interspeech 2022 speech challenge | IEEE-IS² 2025 music challenge |
|--------|-----------------------------------|-------------------------------|
| Causality | 5 ms look-ahead allowed (non-causal mode) | **strictly causal — look-ahead disqualifies a submission** |
| Packet size | 10 ms frames at 16 kHz | 512 samples ≈ **11.6 ms at 44.1 kHz** |
| Material | speech, wideband | **solo-instrument music, 16-bit 44.1 kHz** |
| Loss traces | own traces | Interspeech 2022 traces reused (burst subsets ≤6 and 6–16 packets; the 16–50-packet subset is not sampled) |
| Field size | dozens of submissions | **three submissions** (2025): Aironi et al. (UnivPM + CMU) placed 1st; Daniotti & Turchet (Trento); Severi (PoliTo) |
| Data release | blind test held back | clean references now released for reproducible evaluation |

Why it matters for this synthesis: the "no shared benchmark for music PLC" caveat stated above is now dated — but only partially. The music benchmark exists and is *harder* (strict causality at a higher rate), yet with three submissions its numbers are still not a ranking of the field the way the 16 kHz challenge became one. Also note the causality inversion: the music community forbids exactly the 5 ms look-ahead that [[sources/valin-2022-real-time-plc|Valin et al. 2022]] used to win second place in the speech challenge.

### 2. The linear-prediction + residual family is being extended

The [[concepts/parcnet|PARCnet]] skeleton (online AR predictor + learned residual) is turning into the de facto music-PLC baseline, with follow-up work attacking its three components:

- **Sparser linear branch** — *Sparse Linear Prediction for Packet Loss Concealment in Networked Music Performances* ([IEEE IS² 2025](https://doi.org/10.1109/is264627.2025.11284650)) selects **non-contiguous lags** with orthogonal matching pursuit instead of a dense AR($p$), reaching sub-millisecond model fitting on ARM and tens of nanoseconds per predicted sample. This is the classical sparse-LP line (Giacobello, Christensen) arriving in PLC: more effective model order for the same arithmetic budget.
- **Alternative residual backbones** — a 2026 Brno University of Technology dissertation ([thesis](https://hdl.handle.net/11012/257743)) rebuilds the PARCnet recipe with **(a)** an S4D state-space branch (AR-SSM) and **(b)** a convolutional encoder/decoder with recurrent bottleneck on spectral features (AR-GCRN). On Medley-solos-DB, AR-GCRN is on par with PARCnet overall and better on spectral/psychoacoustic metrics while meeting real-time constraints — whereas **AR-SSM failed the real-time requirement**, a useful negative result: state-space backbones are not automatically cheaper than convolutional ones at these packet rates.
- **Perceptual training objective** — *Tilt loss* ([EURASIP JASMP 2026](https://doi.org/10.1186/s13636-025-00442-1), Daniotti, Vignati & Turchet) replaces the multi-resolution spectrogram loss with a perceptual "tilt" loss that costs nothing at inference, beats the previous state of the art under human evaluation — but **degrades on unpitched instruments**, and the authors explicitly call for objective metrics designed for PLC rather than borrowed from codec evaluation.

The last point is the same metric indictment this page reaches independently below (PEAQ was built for codecs, PLCMOS for speech); it is now being made from inside the music-PLC community.

### 3. A new axis: inference-time adaptation

*TTT-PLC: Self-Supervised Test-Time Tuning for Packet Loss Concealment* ([arXiv 2607.01823](https://arxiv.org/html/2607.01823v1), Dissen & Keshet, Technion, 2026-07) adds a dimension this page did not track: **is the model static at deployment?** The recipe masks a subset of the *actually received* packets, adapts the pretrained PLC model on them with its own native loss, then conceals the real losses — no clean reference, no extra data, no architecture change. Its two backbones are exactly the two poles of this synthesis: **FRN** (speech, 48 kHz) and **PARCnet** (music, 32 kHz), whose code the authors also maintain.

Reported behaviour:

- **PARCnet, in-domain (MAESTRO piano, full 50-min file)**: frozen packet NMSE −4.28…−5.28 dB → causal adaptation −5.52/−5.12/−4.40 dB at 10/20/30% loss; two-pass ≈ causal; multi-epoch reaches −5.94/−5.49/−4.55 dB but perceptual metrics "remain mixed". Held-out snapshot selection lands within a mean 0.02 dB of the oracle.
- **PARCnet, out-of-domain (LibriSpeech-40 at 32 kHz)**: frozen −0.06…+0.30 dB — i.e. **essentially no concealment benefit at all** — improving to −1.63/−1.57/−1.39 dB causally and −1.84/−1.76/−1.59 dB two-pass. This is the sharpest evidence yet that PARCnet is a *domain-invariant only within* quasi-harmonic instrumental signals: an AR(128) predictor fitted on speech plus a network trained on piano transfers poorly.
- **FRN**: causal block-replay adaptation recovers **84–85% of the non-causal gain on STOI/PESQ and 77–88% on both PLCMOS heads**, improving every metric on the 966-file PLC Challenge test set, plateauing after ~60–70 s of audio.
- **Cost**: PARCnet frozen RTF 0.075 → **3.10** with one update per packet (≈1.03 if every third packet), ≈**15** for five-epoch adaptation. So test-time tuning is currently an offline/near-line tool, not a real-time one — the opposite trade-off from the sequence-lesson of Section III (fixed, tiny, causal models).

Conceptual consequence: adaptation partially **substitutes for the loss metadata** that separated informed from blind systems above — received packets carry speaker/instrument/channel information that a per-call adaptation can exploit. It also gives Insight 2's "reuse your own output" motif a stronger form: the model reuses its own *loss function* on the current signal.

### 4. Generative modelling: diffusion and single-shot long-gap synthesis

The 2022–2023 generative fork (autoregressive vocoder) is being challenged on the exact weakness this page identified — long bursts and AR drift:

- **Token-based audio inpainting via discrete diffusion** ([ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/file/20888d00c5df685de2c09790040e0327-Paper-Conference.pdf)) runs discrete diffusion over tokens from a pretrained audio tokenizer, restoring gaps **up to 750 ms** on MAESTRO/MusicNet with derivative-based temporal regularization and span-based absorbing transitions. This is the first credible route to the >100 ms regime that Valin's $c_0$-decay heuristic only *simulates*.
- **Diffusion PLC with explicit loss conditioning** — Hanyang University patent [WO2026101081A1](https://eureka.patsnap.com/patent/WO2026101081A1) (published 2026-05) conditions a diffusion residual stack on two FiLM embeddings: local signal context and a **packet-loss embedding**, i.e. re-introducing loss-mask information into a generative sampler.
- **One-shot adversarial autoencoders** — [US20250356859A1](https://www.patents-review.com/a/20250356859-real-time-packet-loss-concealment-deep-generative-networks.html) (published 2025-11) pairs a causal adversarial autoencoder with a generative prior over its quantized latent, explicitly claiming **>100 ms of loss in a single feed-forward step, non-autoregressively** — the direct answer to the AR-loop drift problem.
- **GAN + selective state space** ([Archives of Acoustics 2026](https://doi.org/10.24423/archacoust.2026.4269)) combines a Mamba-style selective SSM, efficient attention and a large pretrained model inside a U-shaped time-frequency inpainting generator.

On the speech side the mainstream is still incremental rather than paradigm-shifting: **DDSN** ([Interspeech 2026 digest](https://nanless.github.io/audio-paper-digest-blog/posts/conference-interspeech-2026-conference-paper-id-tian26b-interspeech-39b5abc2b7/)) — a wrapped-phase-aware decoupled dual-stream network with a shared TCN bottleneck and additive (rather than multiplicative) residual guidance — reports PESQ 3.25 / PLCMOS 4.08 on the 2022 blind test versus 3.16 / 3.95 for cplx-bin2bin, and PLCMOS 3.76 vs 2.42 at 50% loss on VCTK, still at 16 kHz read speech with Gilbert–Elliot bursts. Phase coherence and seam continuity remain the productive battleground, exactly as in Insight 5.

### 5. Two slower paradigm shifts

- **PLC as one task among many** — *SEFlow* presents a single causal, sampling-rate-agnostic network whose width and depth can be sliced at inference (FlexAttention, FlexRMSNorm, early exit) to cover denoising, dereverberation, declipping **and** PLC, with sub-networks as small as 1% of the full model still usable. If this line matures, dedicated PLC architectures become special cases of a general audio-restoration backbone — the same consolidation that happened to AEC and SE.
- **PLC inside semantic communication** — *Glaris* ([arXiv 2512.08203](http://arxiv.org/abs/2512.08203), 2025-12) places resilient coding in a generative latent space so the receiver performs PLC with a generative prior, trading forward-error-correction redundancy for latent-space reconstruction, and flags a structural constraint this page should record: neural PLC's requirement that each frame be independently decodable **blocks entropy coding**, which is why PLC and codec compression efficiency remain in tension.

### What this changes in the analysis above

1. **Insight 1** gains a sixth family (one-shot / diffusion generative inpainting) and, more importantly, a *meta*-axis: **static vs. test-time-adapted** deployment.
2. **Insight 5**'s vocoder fork is being reopened from a third side: not "vocoder vs. no vocoder" but "autoregressive loop vs. one feed-forward generative step" (adversarial AEs, token diffusion), motivated precisely by drift.
3. **The comparability caveat** needs one more line: the music community now has a shared causal benchmark, but its three-submission field cannot yet rank architectures the way the 16 kHz speech challenge could.
4. **Metric caution is now consensus**: two independent 2026 works (TTT-PLC and Tilt loss) arrive at this page's conclusion that PLCMOS and PEAQ are proxies of convenience outside speech codec evaluation.

## Open Questions

1. **Blind PLC inside a stateful codec**: Valin's codec mode shows concealed audio must reconstruct decoder state — incompatible with non-causal resync. Can a blind model (which by definition cannot know *where* loss begins/ends) be integrated into Opus-class codecs, or does codec integration structurally require loss metadata?
2. **Long-burst behavior of blind predictors**: FRN's predictor-on-previous-output recursion is the same mechanism that motivated Valin's drift analysis. Does the pre-trained-on-clean-targets predictor drift during >100 ms bursts, and does it need a Valin-style fading rule?
3. **Full-band vocoder PLC**: FRN avoids the vocoder at 48 kHz partly for efficiency; a full-band LPCNet-style hybrid would face 3× the sample rate. Is the vocoder route viable at 48 kHz within real-time budgets?
4. **A shared benchmark**: re-evaluating all four paradigms on one corpus, one sample rate, and one loss-trace set (including the challenge traces) would settle the vocoder-vs-no-vocoder and continuous-vs-on-demand forks the way the AEC challenge settled AEC rankings.
5. **Music PLC without a music corpus**: every music-PLC result so far comes from a single instrument family (MAESTRO piano). Do the linear-prediction and residual-learning claims hold for polyphonic mixtures, percussive onsets and attack transients, where the all-pole assumption is weakest and loss concealment is perceptually most exposed?
6. **Objective metrics across domains**: speech-trained PLCMOS and codec-oriented PEAQ were both validated here against MUSHRA on *piano* signals (r = 0.899 and 0.957), while mel-spectral convergence failed to correlate at all — so which objective proxy should music-PLC work report, and does the speech-PLC convention of PLCMOS-only reporting survive at 32–48 kHz?
7. **Static vs. adapted models**: TTT-PLC shows per-file self-supervised adaptation beats a frozen model by 1–2 dB NMSE, at 40× the inference cost. Where on the cost/quality curve does adaptation actually pay off in production — per call, per file, never — and does it make the informed/blind distinction obsolete?
8. **One-shot generative long-gap synthesis**: adversarial autoencoders and token diffusion claim >100 ms (up to 750 ms) reconstruction in one step, where classical and AR systems fade out by design. Do they actually restore *musical* structure, or plausible-sounding hallucination? The PLC community has no established protocol for measuring "correct vs. plausible" past 100 ms.

**Status of these questions as of the 2025–2026 survey above**: Q4 is partially answered on the music side (IEEE-IS² benchmark, but a three-submission field) and still open for speech (no post-2022 rerun); Q5 is now addressable but untested at scale (multi-instrument challenge data exists, hybrid-residual follow-ups still evaluate on piano/solos datasets); Q6 is being made from inside the music community (Tilt loss) and independently by TTT-PLC; Q2 has a partial negative answer for non-drift reasons — FRN's metric gains under adaptation plateau after ~60–70 s with no late-file drift.

## Related Concepts

- [[concepts/packet-loss-concealment|Packet Loss Concealment]] — the umbrella task (informed/blind taxonomy, evaluation)
- [[concepts/dnn-regression-plc|DNN Regression PLC]] — the 2016 paradigm
- [[concepts/tplcnet|tPLCnet]] — the 2022 on-demand seq2one paradigm
- [[concepts/full-band-recurrent-network|Full-Band Recurrent Network (FRN)]] — the 2023 blind full-band paradigm
- [[concepts/lpcnet|LPCNet]] — the generative vocoder behind the 2022 hybrid
- [[concepts/decision-directed-a-priori-snr|Decision-Directed A Priori SNR Estimation]] — the classical precedent for reusing the previous estimate
- [[concepts/frequency-domain-loss|Frequency Domain Loss]] — FRN's training objective
- [[concepts/opus-codec|Opus Audio Codec]] — the stateful-codec integration target
- [[concepts/burg-spectral-estimation|Burg Spectral Estimation]] — Valin's half-frame conditioning features
- [[concepts/parcnet|PARCnet]] — the 2024 linear-AR + learned-residual paradigm
- [[concepts/networked-music-performance|Networked Music Performance]] — the high-fidelity domain that reorders the paradigm ranking
- [[concepts/mushra-listening-test|MUSHRA Listening Test]] — the music-PLC subjective protocol (replacing CMOS/WAcc)
- [[concepts/peaq|PEAQ]] — objective perceptual audio metric that tracked MUSHRA best in the music study
- [[concepts/plcmos|PLCMOS]] — the cross-domain constant metric in this comparison

## Related Sources

- [[sources/lee-2016-dnn-plc|Lee & Chang 2016: DNN-Based Packet Loss Concealment]] — earliest DNN-regression PLC; recursive burst re-feeding; ASR front-end evaluation
- [[sources/valin-2022-real-time-plc|Valin et al. 2022: Real-Time Packet Loss Concealment With Mixed Generative and Predictive Model]] — hybrid vocoder PLC, 2nd place Interspeech 2022 PLC Challenge, Opus integration
- [[sources/westhausen-2022-tplcnet|Westhausen & Meyer 2022: tPLCnet — Real-Time Deep Packet Loss Concealment in the Time Domain]] — on-demand seq2one PLC, 3rd place (tied) in the same challenge; the informed baseline FRN benchmarks against
- [[sources/nguyen-2023-predictive-plc|Nguyen, Nguyen & Khong 2023: Full-Band Blind Packet-Loss Concealment With Predictive Network]] — blind full-band FRN; beats informed tPLCnet without loss metadata
- [[sources/mezza-2024-hybrid-plc|Mezza, Amerena, Bernardini & Sarti 2024: Hybrid Packet Loss Concealment for Real-Time Networked Music Applications]] — music/NMP PLC at 32 kHz; AR(128) beats every deep baseline and PARCnet learns its residual, winning MUSHRA by 21.7 points at 416 k params in real time
