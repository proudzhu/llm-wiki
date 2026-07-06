---
type: concept
created: 2026-07-07
updated: 2026-07-07
tags:
  - data-structures
  - audio-programming
  - realtime-systems
sources:
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
---

# Ring Buffer (Circular Buffer)

A **ring buffer** (also called circular buffer or circular queue) is a fixed-size data structure that uses a single, contiguous buffer as if it were connected end-to-end, with two indices (read pointer and write pointer) that wrap around when reaching the end. It is the standard data structure for implementing [[concepts/fifo-queue|FIFO queues]] in realtime audio processing.

## Key Properties

- **Fixed capacity**: Memory is preallocated; no dynamic allocation in the audio processing thread
- **O(1) operations**: Enqueue and dequeue are constant time without data movement
- **Lock-free friendly**: Well-suited for single-producer/single-consumer (SPSC) scenarios without mutexes in realtime threads
- **No fragmentation**: Memory reuse is automatic as pointers wrap around

## Use in Block Size Adaptation

In [[concepts/block-size-adaptation|block size adaptation (reblocking)]], two ring buffers are used:

1. **Input ring buffer**: Stores samples arriving from the host (in chunks of $b_\text{host}$) until a full plugin block ($b_\text{plugin}$) can be assembled for processing
2. **Output ring buffer**: Stores processed samples from the plugin (in chunks of $b_\text{plugin}$) until a full host block ($b_\text{host}$) is available for output

To provide contiguous memory to plugins that require it (avoiding wrap-around reads), the buffer size is typically chosen as a multiple of $b_\text{plugin}$ (the plugin block size). This does not increase latency but requires slightly more memory.

## Capacity Requirements

For reblocking between $b_\text{host}$ and $b_\text{plugin}$ with minimum delay $\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})$:
- Minimum usable capacity (accounting for wrap-around): $b_\text{host} + \Delta$ samples
- Contiguous-block capacity (multiple of $b_\text{plugin}$): $\text{next multiple of } b_\text{plugin} \text{ above } b_\text{host} + \Delta$

## Related Concepts

- [[concepts/block-size-adaptation|Block Size Adaptation / Reblocking]]
- [[concepts/fifo-queue|FIFO Queue]]
- [[concepts/audio-latency|Audio Latency]]

## Related Sources

- [[sources/rath-2026-minimum-delay-block-size|Rath & Geier 2026: Minimum Required Delay for Realtime Block Size Adaptation]]
