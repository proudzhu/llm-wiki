---
type: concept
created: 2026-07-07
updated: 2026-07-07
tags:
  - audio-signal-processing
  - realtime-processing
sources:
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
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
