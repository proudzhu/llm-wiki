---
type: concept
created: 2026-06-06
updated: 2026-06-06
tags:
  - speech-enhancement
  - echo-cancellation
  - signal-processing
---

# Acoustic Echo Cancellation (AEC)

**Acoustic Echo Cancellation (AEC)** removes acoustic echo from microphone signals in communication systems. Echo occurs when the far-end signal played through a loudspeaker is picked up by the microphone via room reflections, degrading call quality.

## Problem Formulation

The microphone signal contains:
- Near-end speech (desired)
- Acoustic echo from far-end signal (undesired)
- Background noise
- Reverberation

The goal is to estimate and subtract the echo component, or equivalently learn a filter that suppresses echo while preserving near-end speech.

## Traditional Approaches

| Method | Description | Key Property |
|--------|-------------|--------------|
| **Adaptive filtering (NLMS, RLS)** | Estimates echo path impulse response | Requires double-talk detection |
| **Linear echo canceller (LAEC)** | DSP-based adaptive filter | Foundation for hybrid systems |
| **Delay compensation** | Aligns mic and far-end signals | Critical for AEC performance |

## Deep Learning Approaches

| Method | Description | Key Property |
|--------|-------------|--------------|
| **Hybrid DL+AEC** | DL post-processor after LAEC | Combines interpretability with learning |
| **End-to-end DL** | Pure neural network AEC | No explicit echo path estimation |
| **Cross-attention alignment** | Soft alignment in feature space | Replaces DSP delay compensator |

## Key Challenges

- **Double-talk scenarios**: Near-end and far-end speech overlap
- **Time-varying echo paths**: Room acoustics change with movement
- **Long delays**: Echo delays up to 1 second in large rooms
- **Nonlinear distortion**: Loudspeaker and microphone nonlinearities

## Evaluation Metrics

- **ERLE** (Echo Return Loss Enhancement): Measures echo suppression in far-end single-talk
- **AECMOS**: MOS-based echo quality score for both single-talk and double-talk
- **WER** (Word Error Rate): ASR-based intelligibility metric

## Related Concepts

- [[concepts/cross-attention-alignment|Cross-Attention Alignment]]
- [[concepts/complex-convolving-mask|Complex Convolving Mask]]
- [[concepts/dereverberation|Dereverberation]]

## Related Sources

- [[sources/indenbom-2023-deepvqe|Indenbom et al. 2023: DeepVQE]]
