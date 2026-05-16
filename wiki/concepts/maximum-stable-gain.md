---
type: concept
created: 2026-05-15
updated: 2026-05-15
sources:
  - raw/papers/zhan-2025-deeppem-afc/full-text.txt
tags:
  - hearing-aids
  - feedback-cancellation
  - stability
---

# Maximum Stable Gain

**Maximum Stable Gain (MSG)** is the maximum amplification gain a hearing aid can provide before the acoustic feedback loop becomes unstable and produces howling.

## Definition

The MSG is determined by the acoustic feedback path transfer function F(k):

```
MSG = -20 · log₁₀(max_k |F(k)|)
```

## Importance

- Limits the effectiveness of hearing aids for severe/profound hearing loss
- Higher MSG allows greater amplification without howling
- AFC methods aim to increase the effective MSG by estimating and canceling the feedback path

## Added Stable Gain (ASG)

**ASG** measures the improvement in stability provided by an AFC method:

```
ASG(l) = -20 · log₁₀(max_k |F(k,l) - F̂(k,l)| / |F(k,l)|)
```

where F̂(k,l) is the estimated feedback path.

## Tracking Time

**Tracking time** is defined as the time required for the average ASG to exceed the MSG by 3 dB following a feedback path change. This metric is critical for evaluating AFC performance in real-world scenarios where the feedback path changes (e.g., hat on/off, phone near ear).

## Related Concepts

- [[../concepts/hearing-aid-feedback-cancellation|Hearing Aid Feedback Cancellation]]
- [[../concepts/acoustic-feedback|Acoustic Feedback]]
- [[../concepts/adaptive-feedback-control|Adaptive Feedback Control]]

## Related Sources

- [[../sources/zhan-2025-deeppem-afc|Zhan 2025: DeepPEM-AFC]] — ASG and tracking time evaluation
