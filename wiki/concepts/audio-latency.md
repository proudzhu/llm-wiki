---
type: concept
created: 2026-07-07
updated: 2026-11-11
tags:
  - audio-signal-processing
  - realtime-processing
  - hearing-aids
sources:
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
  - raw/papers/chiba-2027-wideband-anc-coaxial-loudspeaker/full-text.txt
  - raw/papers/fu-2026-one-model-many-latencies/full-text.md
---

# Audio Latency

**Audio latency** is the time delay between an audio signal entering a system and the corresponding processed signal exiting. In realtime interactive audio systems (DAWs, live performance, hearing aids, ANC headphones), low latency is critical for usability.

## Sources of Latency in Block-Based Processing

In block-based digital audio systems, latency accumulates from several sources:

1. **Block size delay**: Inherent delay from processing audio in blocks rather than sample-by-sample. Processing a block of size $b$ introduces at least $b$ samples of delay (the system must wait for $b$ samples to arrive before processing).
2. **AD/DA conversion**: Analog-to-digital and digital-to-analog conversion adds small but nonzero delay
3. **[[concepts/block-size-adaptation|Block size adaptation (reblocking)]]**: When host and plugin block sizes differ, additional buffering is needed. The minimum additional delay from this source is given by $\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})$.
4. **Buffering for resampling**: Sample rate conversion introduces latency
5. **System/OS scheduling**: Operating system interrupt handling and scheduling jitter
6. **Algorithm-specific delay**: Look-ahead in compressors, FFT windowing in frequency-domain processing, etc.

## The Latency vs CPU Tradeoff

- Smaller block sizes → lower latency, but higher CPU overhead (more frequent function calls, worse cache efficiency)
- Larger block sizes → better CPU efficiency, but higher latency
- [[concepts/block-size-adaptation|Block size mismatches]] between host and plugins add extra latency on top of the base block delay, quantifiable via the GCD formula

## Hearing-Device Latency Constraints

Hearing aids impose a strict total latency limit of **≤ 10 ms** (Stone & Moore 2003). For STFT-based algorithms the latency decomposes into:

- **Algorithmic latency** — the STFT synthesis window length (the signal is only fully reconstructable after one window);
- **Processing latency** — the time to process one segment, which must not exceed the STFT hop size for real-time operation.

This constraint is a key obstacle for [[concepts/neural-directional-filtering|neural directional filtering]]: prior NDF approaches carry 40–50 ms total latency. [[concepts/film-osn|FiLM-OSN]] (Uphaus et al. 2026) meets the hearing-aid budget with an 8 ms window and 2 ms hop (10 ms total), showing that a Mamba-based backbone tolerates such short windows where an LSTM-based FT-JNF loses 0.38 PESQ and 1.7 dB SI-SDR.

For [[concepts/hearables|hearables]] with live playback to the ear (augmented audio), the budget loosens to **20–50 ms** end-to-end so output stays synced with the user's visual senses. Within that budget, semantic hearing (Veluri et al. 2023) decomposes its latency into: microphone buffer (chunk) duration + algorithmic lookahead + network processing time + OS audio I/O (~4 ms on iOS). Its binaural extraction network processes 10 ms chunks (416 samples at 44.1 kHz, stride 32, lookahead 0.7 ms → ~10.1 ms algorithmic latency) in **6.56 ms** on a smartphone (0.52 M params, 240 MFLOPS), and degrades gracefully down to 1.4 ms algorithmic latency (6.59 vs 7.42 dB SI-SNRi), suggesting ASIC implementations could reach ultra-low-latency operation.

## Algorithmic vs. Computational Latency (Streaming SE)

For frequency-domain deep SE, latency splits into two terms with different owners (Fu et al. 2026):

$$
l_{\text{Total}} = \underbrace{w + N_{\text{LA}} \cdot h}_{\text{algorithmic}} + l_{\text{Compute}}
$$

where $w$ is the STFT window, $h$ the hop, and $N_{\text{LA}}$ the number of look-ahead frames. **Algorithmic latency** is structural — how much input the model must buffer before it can emit the first output unit — and is set by window size, hop, and look-ahead. **Computational latency** is hardware- and depth-dependent; it must satisfy $l_{\text{Compute}} \le h$ for latency not to accumulate (RTF $<1$).

Two measurement pitfalls the decomposition exposes:

- **Offline RTF understates streaming RTF.** Whole-utterance evaluation exploits time-axis parallelism and large-tensor GPU kernels; a model that reports RTF $\ll 1$ offline can still miss the per-hop deadline frame by frame.
- **Algorithmic latency alone is not a real-time guarantee.** Fu et al. 2026's 12-block TF-Mamba has 40 ms algorithmic latency yet 25.05 ms compute per 20 ms hop on an A100 (RTF 1.25) — it *cannot* run in real time on that GPU despite a modest algorithmic budget.

Because the two terms are controlled by different mechanisms ([[concepts/parallel-look-ahead-convolutions|look-ahead branches]] vs. [[concepts/early-exit-speech-enhancement|exit depth]]), the allocation between them is a design variable: for perceptual quality extra depth pays better than extra look-ahead, whereas for ASR accuracy one look-ahead frame buys most of the available gain.

## ANC-Specific Latency: The Causality Budget

In feedforward ANC the latency budget is far tighter than the perceptual budgets above — it is set by the [[concepts/causality|causality constraint]]: the total secondary-path delay must stay below the primary-minus-reference acoustic delay difference, typically tens to hundreds of µs in headphones. Within that budget, [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba et al. 2027]] decompose the delay as electronic + acoustic + mechanical and note that the **loudspeaker mechanical term** (group delay near the compact driver's fundamental resonance, hundreds of Hz) and the **acoustic propagation term** (diaphragm-to-ear distance) are delay sources specific to wearable ANC hardware — reducible by loudspeaker design ([[concepts/delay-oriented-driver-allocation|delay-oriented driver allocation]]) rather than by faster codecs or smaller blocks. Their ADSP-21569 platform evidence: 192 kHz / 8-sample frames with 24 kHz internal processing sustain an 83.3 µs pass-through peak, with foreground (27.7 µs of a 41.7 µs frame deadline) and background (≤ 79.7% of block deadline) processes both meeting deadlines under adaptive load.

## Related Sources

- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — 10 ms-latency NDF for hearing aids
- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]] — 20–50 ms hearable latency budget; 6.56 ms on-smartphone binaural extraction of 10 ms chunks, graceful degradation to 1.4 ms algorithmic latency
- [[sources/chiba-2027-wideband-anc-coaxial-loudspeaker|Chiba, Kamado, Kako & Noguchi 2027: Wideband ANC for Open-Ear Headphones with a Coaxial Loudspeaker]] — µs-scale ANC causality budget decomposed into electronic/acoustic/mechanical terms; DSP frame-schedule and execution-time evidence at 83.3 µs pass-through
- [[sources/fu-2026-one-model-many-latencies|Fu et al. 2026: One Model, Many Latencies]] — explicit algorithmic/computational latency decomposition; 30 selectable latency configurations in one model; 12-block config violates RTF < 1 at 20 ms hop
