---
type: concept
created: 2026-11-10
updated: 2026-11-10
sources:
  - raw/papers/zhao-2025-lightweight-transformer/full-text.md
tags:
  - speech-enhancement
  - transformer
  - attention
  - streaming
  - causal
  - efficiency
---

# Trapezoidal Causal Masking

**Trapezoidal causal masking** is the attention mask used by Zhao & Madhu (EUSIPCO 2025) in the time-axis transformer of the [[concepts/ftf-transformer|FTF transformer]]: a causal mask whose attention window is additionally capped at a fixed maximum context (1 s of frames). Unlike the usual triangular causal mask, which allows every past frame to attend to every earlier one, the permitted region of the attention matrix is a **trapezoid** — a lower triangle truncated at a fixed look-back distance.

## Formulation

For query frame $t$ and key frame $\tau$, the mask admits

$$
A_{t,\tau} \;\text{is allowed} \iff t - L \;\le\; \tau \;\le\; t,
$$

with look-back $L$ capped at 1 s of frames instead of the standard causal condition $\tau \le t$. Two consequences follow:

1. **Bounded complexity** — attention cost per frame is $O(L)$ rather than $O(t)$, so total cost is **linear in utterance length and independent of it per frame**. Without the cap, attention in a streaming model accumulates cost and key/value memory linearly with session length.
2. **Bounded state** — the key/value cache holds a fixed $L$ frames, which is what makes an attention block deployable in a frame-by-frame streaming model at all.

Causality is preserved because $\tau \le t$ still holds; only distant history is discarded. The implicit claim is that beyond ~1 s, temporal context for speech enhancement is better carried by the GRU's compressed recurrent state (which is unbounded in history but constant in size) than by explicit attention.

## Why It Matters

The alternative to a bounded causal mask is either (a) full causal attention, whose per-frame cost grows with session length and whose cache never stops growing, or (b) no attention in the time direction at all, i.e. a pure RNN — sacrificing the parallel, content-addressable retrieval that attention provides. The trapezoid gets attention's expressiveness at RNN-like bounded cost. It is the enabling trick behind the [[concepts/ftf-transformer|FTF transformer]]'s ability to place an MHA block in the time direction of a 32 ms-latency streaming model.

## Related Concepts

- [[concepts/ftf-transformer|Frequency–Time–Frequency (FTF) Transformer]] — the architecture that uses the mask
- [[concepts/attention-mechanism|Attention Mechanism]] — the underlying operation
- [[concepts/gated-recurrent-unit|Gated Recurrent Unit]] — supplies unbounded-history context from constant-size state
- [[concepts/dprnn|Dual-Path RNN (DPRNN)]] — the attention-free interleaved alternative
- [[concepts/rnnformer|RNNFormer]] — the alternative resolution: no attention on the time axis at all, GRU instead
- [[concepts/hyst-net|HyST-Net]] — successor that drops the time-axis MHA entirely

## Related Sources

- [[sources/zhao-2025-lightweight-transformer|Zhao & Madhu 2025: Study of Lightweight Transformer Architectures for Single-Channel Speech Enhancement]] — introduces the mask in the FTF time transformer
