---
type: concept
created: 2026-07-10
updated: 2026-07-10
tags:
  - signal-processing
  - stft
  - low-latency
  - speech-enhancement
  - real-time
---

# Asymmetric STFT

An **asymmetric STFT** configuration uses a long analysis window (aW) to preserve frequency resolution while applying a shorter synthesis window (sW) to reduce reconstruction (algorithmic) latency. This decouples spectral resolution from algorithmic delay, enabling low-latency real-time streaming without sacrificing the frequency detail needed for speech enhancement.

## Motivation

In conventional STFT processing, the analysis and synthesis windows have equal length, so the algorithmic latency is bounded by the window/hop size. Reducing the window to lower latency also reduces frequency resolution, degrading enhancement quality. The asymmetric configuration breaks this coupling: a long analysis window retains fine frequency resolution for mask estimation, while a short synthesis window reconstructs the output with minimal delay.

## Window Choice

- **Square-root Hann** windows degrade rapidly when the synthesis window is shortened, because the analysis-synthesis pair no longer satisfies perfect-reconstruction conditions.
- **Asymmetric Hann** windows (Wood & Rouat, 2019) maintain better SI-SDR and SI-SAR at short synthesis lengths, offering a favorable latency–quality compromise.

## Application in RT-Tango

In [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|RT-Tango (Benslimane et al., 2026)]], an asymmetric STFT with a 32 ms analysis window and an 8 ms asymmetric Hann synthesis window achieves an **8 ms algorithmic latency** in the streaming variant RT-Tango-OS. Reducing the synthesis window to 4 ms further decreases latency but degrades performance. The 8 ms configuration is selected as the best trade-off.

Combined with a 4 ms hop size, this enables operation at ~250 STFT frames/s while keeping the algorithmic delay within hearing-aid tolerances.

## Related Concepts

- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/audio-latency|Audio Latency]]
- [[concepts/block-size-adaptation|Block Size Adaptation (Reblocking)]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]

## Related Sources

- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
