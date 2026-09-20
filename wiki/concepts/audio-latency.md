---
type: concept
created: 2026-07-07
updated: 2026-09-20
tags:
  - audio-signal-processing
  - realtime-processing
  - hearing-aids
sources:
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
  - raw/papers/uphaus-2026-directivity-low-latency/full-text.md
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

## Related Sources

- [[sources/uphaus-2026-directivity-low-latency|Uphaus et al. 2026: Directivity-Conditioned Low-Latency Neural Filtering]] — 10 ms-latency NDF for hearing aids
