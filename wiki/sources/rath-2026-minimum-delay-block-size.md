---
type: source
created: 2026-07-07
updated: 2026-07-07
sources:
  - raw/papers/rath-2026-minimum-delay-block-size/full-text.txt
tags:
  - audio-signal-processing
  - realtime-processing
  - block-processing
  - latency
  - number-theory
---

# Rath & Geier 2026: Minimum Required Delay for Realtime Block Size Adaptation

**Authors**: [[entities/matthias-rath|Matthias Rath]] (Institute for Advanced Procrastination, Berlin), [[entities/matthias-geier|Matthias Geier]] (ai-coustics, Berlin; portions done at Fraunhofer IIS)
**Venue**: Proceedings of the 20th Linux Audio Conference (LAC-26), Maynooth, Ireland, June 18–20, 2026
**Type**: Conference paper
**Zotero**: zotero://select/items/0_JXB3FSYP

## Summary

This paper derives a simple, closed-form formula for the minimum delay introduced when a realtime audio host application (operating on block size $b_\text{host}$) invokes a plugin that uses a different block size $b_\text{plugin}$. The problem is shown to reduce to elementary number theory, yielding the result $\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})$. This replaces the brute-force iterative algorithm previously used in libraries like PortAudio.

## Problem Formulation

In block-based realtime audio processing:
- The **host** (DAW, audio driver, middleware) processes audio in fixed-size blocks of $b_\text{host}$ samples
- A **plugin** processes audio in fixed-size blocks of $b_\text{plugin}$ samples
- When $b_\text{host} \neq b_\text{plugin}$, buffering ("reblocking") is required between host and plugin
- This buffering introduces latency (delay), and the goal is to find the **minimum possible delay** $\Delta$ that guarantees glitch-free operation

Key insight from the stream model:
- Plugin block $n$ starts at sample $n b_\text{plugin}$
- It can only be processed when the last host block overlapping it has arrived
- The delay for block $n$ is $\Delta_n = m_n b_\text{host} - n b_\text{plugin}$, where $m_n$ is the index of the last overlapping host block
- The global minimum delay is the maximum of all $\Delta_n$ over $n \in \mathbb{N}_0$:
$$\Delta = \max\{\Delta_n \mid n \in \mathbb{N}_0\}$$

## Methodology

The proof proceeds in three main steps:

**1. Upper bound via GCD properties**:
- All $\Delta_n$ are integer linear combinations of $b_\text{host}$ and $b_\text{plugin}$
- By [[concepts/bezouts-identity|Bézout's identity]], all such combinations are multiples of $g = \gcd(b_\text{host}, b_\text{plugin})$
- Since $\Delta_n < b_\text{plugin}$, we get $\Delta \leq b_\text{plugin} - g$

**2. Extended set analysis**:
Define the set $S = \{m b_\text{host} - n b_\text{plugin} \mid m, n \in \mathbb{N}_0\}$ of all differences of non-negative multiples. The paper proves a small generalization of Bézout's lemma:
- $g \in S$ and $-g \in S$
- Consequently, $S$ consists of exactly all integer multiples of $g$: $S = \{z g \mid z \in \mathbb{Z}\}$

**3. Tightness (lower bound)**:
The relevant delays satisfy $b_\text{plugin} - b_\text{host} \leq \delta < b_\text{plugin}$. Since $g$ is in this range (as the largest multiple of $g$ less than $b_\text{plugin}$), the upper bound $b_\text{plugin} - g$ is actually achieved.

## Main Result

The minimum required delay is:

$$\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})$$

### Special cases:
- When $b_\text{plugin}$ divides $b_\text{host}$: $\Delta = 0$ (no delay needed; host can split blocks)
- When block sizes are **coprime** ($\gcd = 1$): $\Delta = b_\text{plugin} - 1$ (worst case)
- When both are powers of two (common in practice): $\Delta = \max(0, b_\text{plugin} - b_\text{host})$

## Example Values

| $b_\text{host}$ | $b_\text{plugin}$ | $\gcd$ | $\Delta$ | Scenario |
|-----------------|-------------------|--------|----------|----------|
| 128 | 128 | 128 | 0 | Equal sizes, trivial |
| 256 | 64 | 64 | 0 | Plugin smaller, host splits |
| 64 | 256 | 64 | 192 | Plugin larger, buffering needed |
| 54 | 90 | 18 | 72 | Neither divides the other |
| 48 | 128 | 16 | 112 | Exercise left to reader |

## Practical Implementation

A stable FIFO-based block adaptation algorithm:
1. Maintain input queue and output queue (ring buffers)
2. Initialize output queue with $\Delta$ zero samples
3. On each host callback:
   - Enqueue $b_\text{host}$ new input samples
   - Process as many full $b_\text{plugin}$ blocks as possible
   - Dequeue $b_\text{host}$ output samples for the audio backend
4. Total samples across both queues is always $\Delta$ between callbacks (buffer underrun guaranteed impossible)

The paper notes that PortAudio previously used an O(LCM) brute-force loop to compute this value iteratively:
```c
// Old PortAudio approach (brute force)
int CalculateFrameShift(int M, int N) {
    int result = 0;
    int lcm = (M * N) / GCD(M, N);
    for (int i = M; i < lcm; i += M) {
        result = MAX(result, i % N);
    }
    return result;
}
```

This can now be replaced with the O(1) closed-form:
```c
// New formula from this paper
int CalculateFrameShift(int M, int N) {
    return N - GCD(M, N);
}
```

## Flexible Block Sizes

The paper also discusses the case where host block size may vary per callback (only a maximum known):
- If plugin supports variable block sizes: no delay needed (process whatever is available)
- If plugin requires fixed $b_\text{plugin}$ but host blocks are variable: the worst-case delay becomes $b_\text{plugin} - 1$, since an overlap of exactly 1 sample can occur

## Key Contributions

1. **Closed-form formula**: Proves $\Delta = b_\text{plugin} - \gcd(b_\text{host}, b_\text{plugin})$ as the minimum delay for arbitrary fixed block sizes
2. **Number-theoretic foundation**: Connects the audio engineering problem to Bézout's identity and linear combinations in elementary number theory
3. **Replaces iterative computation**: The O(1) formula replaces the O(LCM) brute-force method used in PortAudio
4. **Provably correct buffer sizing**: Gives implementers mathematical confidence about required buffer sizes
5. **Practical algorithm**: Provides a concrete FIFO/ring-buffer implementation strategy with stability guarantees

## Related Concepts

- [[concepts/block-size-adaptation|Block Size Adaptation / Reblocking]]
- [[concepts/ring-buffer|Ring Buffer / Circular Buffer]]
- [[concepts/greatest-common-divisor|Greatest Common Divisor (GCD)]]
- [[concepts/bezouts-identity|Bézout's Identity]]
- [[concepts/audio-latency|Audio Latency]]
- [[concepts/fifo-queue|FIFO Queue]]

## References (from paper)

- [1] Gareth A. Jones and J. Mary Jones, *Elementary Number Theory*, Springer-Verlag, 1998.
- [2] Andrew Granville, "It is not 'Bézout's identity'," arXiv [math.HO], 2024, DOI: 10.48550/arXiv.2406.15642.
- [3] Stéphane Letz, "Callback adaptation techniques," Technical report, GRAME, 2001.
- [4] Miller Puckette, *The Theory and Technique of Electronic Music*, World Scientific Publishing Co. Pte. Ltd., 2007. (Describes delay for Pd's power-of-two block sizes)
