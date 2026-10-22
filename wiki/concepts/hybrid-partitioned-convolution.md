---
type: concept
created: 2026-10-22
updated: 2026-10-22
sources:
  - raw/papers/yuan-2026-open-ear-anc-smart-glasses/full-text.md
tags:
  - real-time-dsp
  - anc
  - convolution
  - latency
---

# Hybrid Partitioned Convolution

**Hybrid partitioned convolution** (also called hybrid block convolution) is a real-time FIR filtering scheme that splits a long filter into a **short direct segment** convolved in the time domain on the real-time audio thread, and **longer partitioned segments** processed by frequency-domain (FFT) convolution on a background thread. It combines the minimal latency of direct convolution with the computational efficiency of FFT-based filtering, enabling long filters to run within a strict per-sample time budget.

## Scheme

Given a fundamental block size of $B$ samples:

- **Direct segment**: the first $2B$ taps of the filter, applied as direct time-domain convolution over a circular buffer of the most recent $2B$ input samples, on the real-time audio thread — this is the part that determines latency.
- **Partitioned segments**: the remaining taps are partitioned into blocks of $B$ samples; each new input block is FFT-transformed into a frequency-domain delay line, multiplied by precomputed filter-partition spectra, and reconstructed via IFFT with overlap-add on a lower-priority background task.
- The audio thread sums the direct-segment output with the most recently completed partitioned block to produce the final output sample-by-sample.

Because the background FFT work runs one block ($B$ samples) ahead, the scheme adds at most one block of algorithmic delay to the tail contribution while keeping the *direct* path delay at zero.

## Example: Open-Ear ANC DSP (Yuan et al. 2026)

On a Bela (BeagleBone Black) DSP at $f_s = 22050$ Hz, every sample must be processed within $1/f_s = 45\,\mu$s. For 2048-tap ANC filters with $B = 128$: 256 direct taps (time domain) + 14 partitioned blocks of 128 taps (frequency domain). This achieves a median per-sample processing time of **38 µs** (vs. the 45 µs budget), and an end-to-end microphone-to-speaker latency of **113 µs** (45 µs computation + 68 µs ADC/DAC chain). Pure direct convolution would only meet the budget up to ~1024 taps; pure frequency-domain convolution would add a full block of latency to the direct path. Filter updates from the control filter network are crossfaded over one block to avoid discontinuities.

This latency matters quantitatively: simulated per-sample latencies from 45 µs to 726 µs degrade ANC performance from 11.1 dB to 4.4 dB, since added delay introduces phase errors in the destructive interference.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/virtual-in-ear-sensing|Virtual In-ear Sensing]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]

## Related Sources

- [[sources/yuan-2026-open-ear-anc-smart-glasses|Yuan, Liu & Xiao 2026: Active Noise Cancellation on Open-Ear Smart Glasses]]
