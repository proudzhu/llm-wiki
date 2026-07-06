---
type: concept
created: 2026-07-07
updated: 2026-07-07
tags:
  - data-structures
  - realtime-systems
sources:
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
---

# FIFO Queue (First-In-First-Out)

A **FIFO queue** (first-in, first-out queue) is a data structure where elements are added (enqueued) at one end and removed (dequeued) from the other end, preserving temporal order. In audio processing, FIFO queues (often implemented as [[concepts/ring-buffer|ring buffers]]) are used for buffering between processing stages operating on different block sizes.

## Key Properties

- **Order preservation**: Samples leave the queue in exactly the order they entered
- **Smooth rate mismatches**: Absorbs jitter and adapts between different production/consumption rates
- **Causality**: A FIFO can only delay signals, never advance them
- **Level monitoring**: The fill level (number of elements queued) is used to detect underruns (too few samples to consume) and overruns (no space to enqueue)

## Use in Block Size Adaptation

For [[concepts/block-size-adaptation|block size adaptation]] between host block size $b_\text{host}$ and plugin block size $b_\text{plugin}$, two FIFO queues are maintained:

1. **Input FIFO**: Host enqueues $b_\text{host}$ samples per callback; plugin dequeues $b_\text{plugin}$ samples whenever available
2. **Output FIFO**: Plugin enqueues $b_\text{plugin}$ samples per processing call; host dequeues $b_\text{host}$ samples per callback

If initialized with the correct initial offset ($\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})$ zeros in the output FIFO), the output FIFO will always contain at least $b_\text{host}$ samples when the host needs to dequeue, guaranteeing no buffer underruns.

## Related Concepts

- [[concepts/ring-buffer|Ring Buffer / Circular Buffer]]
- [[concepts/block-size-adaptation|Block Size Adaptation / Reblocking]]
