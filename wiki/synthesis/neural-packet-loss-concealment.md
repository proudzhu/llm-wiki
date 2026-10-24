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
---

# Neural Packet Loss Concealment

> Cross-source synthesis of five neural PLC systems spanning 2016–2024: DNN frame-feature regression (Lee & Chang 2016), on-demand seq2one time-domain prediction (Westhausen & Meyer 2022), hybrid generative + predictive vocoder concealment (Valin et al. 2022), blind full-band predictive concealment (Nguyen, Nguyen & Khong 2023), and hybrid linear-AR + learned-residual concealment for networked music performance (Mezza et al. 2024). The papers trace the field's evolution along five axes — loss-metadata dependence, sample rate and signal domain (speech vs. music), inference regime (continuous vs. on-demand), what the network is asked to predict (waveform/features vs. a linear model's residual), and how each architecture exploits the model's *own previous output* during consecutive losses.

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

## Open Questions

1. **Blind PLC inside a stateful codec**: Valin's codec mode shows concealed audio must reconstruct decoder state — incompatible with non-causal resync. Can a blind model (which by definition cannot know *where* loss begins/ends) be integrated into Opus-class codecs, or does codec integration structurally require loss metadata?
2. **Long-burst behavior of blind predictors**: FRN's predictor-on-previous-output recursion is the same mechanism that motivated Valin's drift analysis. Does the pre-trained-on-clean-targets predictor drift during >100 ms bursts, and does it need a Valin-style fading rule?
3. **Full-band vocoder PLC**: FRN avoids the vocoder at 48 kHz partly for efficiency; a full-band LPCNet-style hybrid would face 3× the sample rate. Is the vocoder route viable at 48 kHz within real-time budgets?
4. **A shared benchmark**: re-evaluating all four paradigms on one corpus, one sample rate, and one loss-trace set (including the challenge traces) would settle the vocoder-vs-no-vocoder and continuous-vs-on-demand forks the way the AEC challenge settled AEC rankings.
5. **Music PLC without a music corpus**: every music-PLC result so far comes from a single instrument family (MAESTRO piano). Do the linear-prediction and residual-learning claims hold for polyphonic mixtures, percussive onsets and attack transients, where the all-pole assumption is weakest and loss concealment is perceptually most exposed?
6. **Objective metrics across domains**: speech-trained PLCMOS and codec-oriented PEAQ were both validated here against MUSHRA on *piano* signals (r = 0.899 and 0.957), while mel-spectral convergence failed to correlate at all — so which objective proxy should music-PLC work report, and does the speech-PLC convention of PLCMOS-only reporting survive at 32–48 kHz?

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
