---
type: concept
created: 2026-05-16
updated: 2026-05-16
tags:
  - neural-network
  - speech-separation
  - speech-enhancement
  - rnn
---

# Dual-Path RNN (DPRNN)

**Dual-Path RNN (DPRNN)** is a lightweight neural network architecture for sequence modeling, originally proposed for single-channel speech separation. It partitions a long input sequence into short overlapping chunks and applies two RNNs along different dimensions to capture both local and global dependencies.

## Architecture

DPRNN operates on a 2D representation of the input (e.g., a time-frequency feature tensor of shape $T \times F$):

1. **Intra-block RNN**: Applied along the frequency/feature dimension within each chunk — captures local spectral patterns.
2. **Inter-block RNN**: Applied along the time/chunk dimension — captures global temporal dependencies across chunks.

The input sequence is first split into $S$ chunks of length $L$ (with overlap), then processed as:

```
Input: (T, F) → Chunking: (S, L, F) → Intra-RNN: (S, L, D) → Inter-RNN: (S, L, D) → Overlap-add: (T, D)
```

## Advantages

- **Efficient**: Avoids quadratic complexity of self-attention while capturing long-range dependencies.
- **Lightweight**: Uses simple RNN cells (typically GRU or LSTM) rather than large transformer blocks.
- **Streaming-friendly**: Can be configured with unidirectional RNNs for frame-by-frame inference.

## Applications in VibOmni

In [[../sources/he-2025-vibomni|VibOmni]], DPRNN is used as the core separator module in the multi-modal speech enhancement network:

- Receives concatenated audio and vibration features from dual encoders.
- Separates speech from noise at the feature level using inter/intra-block RNN modeling.
- Configured with unidirectional RNNs and causal convolutions for real-time inference.
- Model depth (number of separator blocks) is dynamically adjusted during adaptive inference based on estimated noise level.

## Key References

- Y. Luo, Z. Chen, and T. Yoshioka, "Dual-path RNN: efficient long sequence modeling for time-domain single-channel speech separation," in *ICASSP 2020*.

## Related Concepts

- [[../concepts/convolutional-recurrent-network|Convolutional Recurrent Network]]
- [[../concepts/self-attentive-recurrent-neural-network|Self-Attentive Recurrent Neural Network]]
- [[../concepts/neural-networks|Neural Networks]]
- [[../concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[../sources/he-2025-vibomni|He, Guo, Hou & Yan 2025: VibOmni]]
