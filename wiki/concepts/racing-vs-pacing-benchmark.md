---
type: concept
created: 2026-11-07
updated: 2026-11-07
tags:
  - efficiency
  - on-device-inference
  - benchmarking
  - speech-enhancement
  - energy-efficiency
---

# Racing vs. Pacing Benchmark

A benchmarking distinction for real-time audio inference, introduced by [[sources/kim-2026-faster-enhancer|Kim 2026]]: how a compute workload is *fed* to the CPU changes both the measured per-frame cost and the energy consumed, even when the executed work is bit-identical.

## Definitions

- **Racing**: frames are fed as fast as the core accepts them. The core sits at its maximum clock throughout. This is what a throughput benchmark (file in, file out) measures — and it is what nearly all RTF tables in the speech-enhancement literature report.
- **Pacing**: frames arrive on the audio callback's deadline (one every 6.67 ms for a 320-sample hop at 48 kHz) and the core idles in between. The CPU governor responds to the duty cycle by dropping the clock; each frame starts after an idle gap.

The deployed reality of a streaming enhancer is pacing: it holds a fraction of a core for as long as the microphone is open. **Real-time factor is therefore a duty cycle, not a latency** — a benchmark races through a file; an audio callback does not.

## Key Findings (Apple M2, FastEnhancer-Medium int8)

| Quantity | Racing | Paced | Delta |
|----------|--------|-------|-------|
| Per-frame cost (RTF, P-core) | 0.068 | 0.286 | **4.2×** |
| Energy per audio-second (P-core) | 387 mJ | 198 mJ | **−49%** |
| Deadline misses (P-core) | — | 0.05% | — |

Three consequences:

1. **The racing figure is a floor on what a real audio callback pays per frame.** Pacing raises per-frame cost 4.2× because the clock is lower and each frame starts cold after an idle gap.
2. **Race-to-idle is the wrong instinct.** The core finishes sooner at 3.5 GHz, but the voltage that clock costs is never repaid by the idle that follows — pacing saves 49% of the energy for bit-identical work.
3. **Core-placement conclusions invert between protocols.** On a Galaxy S23+, racing spreads core placements by 5.7× (little cluster looks unusable), but pacing collapses the spread to 1.06× — near 10% duty, the governor holds every cluster at its floor. Conversely, the *cheapest* placement by energy (E-core, 95–101 mJ) misses **96% of its deadlines** because timer coalescing delays the wake-up: the compute fits (median frame 3.5 ms of the 6.67 ms budget); the wake-up does not.

The sustained-operation corollary (30 minutes, 270,000 frames): both devices degrade from short runs, but only the phone crosses its deadline budget (p99 RTF 1.0139, 1.77% misses, widening tail attributed to scheduler behaviour rather than heat) — so **deployment validation must run at deployment duration**.

## Protocol Requirements

- Pacing must be measured with the same binary and audio as racing.
- Core placement is controlled via QOS classes (macOS) or affinity masks (Android `taskset` — which sets affinity without touching the scheduling class, unlike macOS QOS).
- Energy integrates package power over the run window minus an idle baseline, with the window located in the trace rather than assumed.
- Deadline-miss rate is reported wherever it exceeds 1%.

## Related Concepts

- [[concepts/faster-enhancer-c|faster-enhancer.c]]
- [[concepts/audio-latency|Audio Latency]]

## Related Sources

- [[sources/kim-2026-faster-enhancer|Kim 2026: faster-enhancer.c]]
