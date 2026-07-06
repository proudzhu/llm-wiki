---
type: concept
created: 2026-07-07
updated: 2026-07-07
tags:
  - audio-signal-processing
  - realtime-processing
  - latency
sources:
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
---

# Block Size Adaptation (Reblocking)

Block size adaptation, also called **reblocking**, is the buffering process required in realtime audio systems when a host application operates on audio blocks of size $b_\text{host}$ and invokes a signal processing plugin that uses a different block size $b_\text{plugin}$. This buffering introduces additional latency (delay) beyond the inherent block size delay.

## Problem Context

In block-based realtime audio processing:
- The audio backend delivers $b_\text{host}$ samples to the host at a time
- The host must return $b_\text{host}$ processed samples within a hard deadline (to avoid audio glitches)
- If the plugin expects/produces blocks of a different size $b_\text{plugin}$, intermediate buffering is required

## Minimum Delay Formula

The minimum delay introduced by reblocking was proven by [[sources/rath-2026-minimum-delay-block-size|Rath & Geier (2026)]] to be:

$$\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})$$

where $\gcd$ is the [[concepts/greatest-common-divisor|greatest common divisor]].

### Key cases:
- When $b_\text{plugin}$ divides $b_\text{host}$ (e.g., host=256, plugin=64): $\Delta = 0$ — no delay needed; host splits its block into plugin-sized chunks
- When $b_\text{host}$ divides $b_\text{plugin}$ (e.g., host=64, plugin=256): $\Delta = b_\text{plugin} - b_\text{host}$ — must buffer until enough samples are available
- When block sizes are **coprime** ($\gcd = 1$): $\Delta = b_\text{plugin} - 1$ — worst-case latency
- When both are powers of two: one always divides the other, so $\Delta = \max(0, b_\text{plugin} - b_\text{host})$

## Implementation

Practical reblocking is typically implemented using a pair of [[concepts/fifo-queue|FIFO queues]] ([[concepts/ring-buffer|ring buffers]]):
1. **Input FIFO**: Buffers incoming host samples until enough are available for a plugin block
2. **Output FIFO**: Buffers plugin output samples until enough are available to satisfy a host block request

The algorithm is stable (never underruns) if the output FIFO is initialized with $\Delta$ zero samples.

## Practical Significance

- Previously, audio libraries like PortAudio computed the required delay using an iterative brute-force algorithm iterating up to $\text{LCM}(b_\text{host}, b_\text{plugin})$ blocks
- The closed-form GCD formula reduces this to an O(1) computation
- Knowing the exact minimum delay allows audio developers to make informed choices about block sizes when balancing latency vs CPU efficiency
- Larger block sizes reduce CPU overhead (fewer function calls, better cache utilization) but increase latency; the formula quantifies the minimum additional latency from mismatched block sizes

## Related Concepts

- [[concepts/ring-buffer|Ring Buffer / Circular Buffer]]
- [[concepts/audio-latency|Audio Latency]]
- [[concepts/greatest-common-divisor|Greatest Common Divisor (GCD)]]
- [[concepts/bezouts-identity|Bézout's Identity]]
- [[concepts/fifo-queue|FIFO Queue]]

## Related Sources

- [[sources/rath-2026-minimum-delay-block-size|Rath & Geier 2026: Minimum Required Delay for Realtime Block Size Adaptation]]
