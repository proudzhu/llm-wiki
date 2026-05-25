---
type: source
created: 2026-05-25
updated: 2026-05-25
sources:
  - raw/papers/tan-2018-convolutional-recurrent-network-speech-enhancement/full-text.md
  - https://doi.org/10.21437/Interspeech.2018-1405
  - zotero://select/items/0_F8A8SVLS
tags:
  - speech-enhancement
  - convolutional-recurrent-network
  - real-time-processing
  - causal-system
  - deep-learning
---

# Tan & Wang 2018: A Convolutional Recurrent Neural Network for Real-Time Speech Enhancement

| Field | Details |
|-------|---------|
| **Authors** | [[entities/ke-tan|Ke Tan]], [[entities/deliang-wang|DeLiang Wang]] |
| **Institution** | Department of Computer Science and Engineering / Center for Cognitive and Brain Sciences, The Ohio State University |
| **Venue** | Interspeech 2018, pp. 3229–3233 |
| **Year** | 2018 |
| **Type** | Conference paper |
| **DOI** | [10.21437/Interspeech.2018-1405](https://doi.org/10.21437/Interspeech.2018-1405) |
| **Zotero** | [Link](zotero://select/items/0_F8A8SVLS) |

## Summary

This paper proposes a novel **Convolutional Recurrent Network (CRN)** for real-time monaural speech enhancement, combining a convolutional encoder-decoder (CED) with long short-term memory (LSTM) layers. The architecture uses causal convolutions to ensure the system requires no future information, making it naturally suitable for real-time processing. The model is noise- and speaker-independent — it generalizes to unseen noise types and untrained speakers. Experiments on WSJ0 with babble and cafeteria noises show the CRN consistently outperforms strong LSTM baselines in both STOI and PESQ while using fewer trainable parameters (17.58M vs 30.22–36.81M).

## Problem Formulation

Monaural speech enhancement is formulated as learning a mapping from the **magnitude spectrogram of noisy speech** to the **magnitude spectrogram of clean speech**:

Given a noisy signal $y(t) = s(t) + n(t)$, the goal is to estimate $|\hat{S}(t,f)|$ from $|Y(t,f)|$, where $|Y(t,f)|$ is the STFT magnitude spectrum of the mixture. The 161-dimensional STFT magnitude spectrum of noisy speech serves as input features, and the corresponding clean speech magnitude spectrum serves as the training target.

The system is **causal**: the output at time $t$ must depend only on inputs at times $\leq t$, with no future information permitted. This constraint is critical for real-time applications like hearing aids, where delays as low as 3 ms are noticeable and delays >10 ms are objectionable.

## Methodology

### CRN Architecture

The CRN combines a convolutional encoder-decoder with LSTM layers in a causal framework:

1. **Convolutional Encoder**: Five causal convolutional layers with batch normalization and ELU activation. Kernel sizes of $2 \times 3$ (time $\times$ frequency) with stride $(1,2)$ in frequency. Feature maps: $1 \rightarrow 16 \rightarrow 32 \rightarrow 64 \rightarrow 128 \rightarrow 256$.
2. **LSTM Bottleneck**: Two stacked LSTM layers inserted between encoder and decoder capture long-term temporal dependencies in the latent feature space. The frequency and depth dimensions are flattened before LSTM input and reshaped after.
3. **Deconvolutional Decoder**: Five symmetric transposed convolutional layers mirroring the encoder, with skip connections connecting each encoder layer to its corresponding decoder layer.
4. **Output**: Softplus activation on the final layer to ensure positive magnitude predictions.

### Causal Convolutions

Causal convolutions apply asymmetric zero-padding in the time dimension (past only), ensuring the output at time $t$ depends only on inputs up to $t$. For deconvolutions, causality is automatically preserved since deconvolution is intrinsically a convolution operation.

### LSTM Equations

Standard LSTM with input gate $i_t$, forget gate $f_t$, block input $g_t$, output gate $o_t$, memory cell $c_t$, and hidden state $h_t$:

$$
i_t = \sigma(W_{ii} x_t + b_{ii} + W_{hi} h_{t-1} + b_{hi})
$$

$$
f_t = \sigma(W_{if} x_t + b_{if} + W_{hf} h_{t-1} + b_{hf})
$$

$$
g_t = \tanh(W_{ig} x_t + b_{ig} + W_{hg} h_{t-1} + b_{hg})
$$

$$
o_t = \sigma(W_{io} x_t + b_{io} + W_{ho} h_{t-1} + b_{ho})
$$

$$
c_t = f_t \odot c_{t-1} + i_t \odot g_t
$$

$$
h_t = o_t \odot \tanh(c_t)
$$

### LSTM Baselines

Two baseline LSTM models are constructed for comparison:
- **LSTM-1**: Uses 11-frame feature window (10 past + 1 current) with architecture 1771–1024–1024–1024–1024–161 units.
- **LSTM-2**: No feature window, architecture 161–1024–1024–1024–1024–161 units.
Both are causal systems using no future information.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| **Training data** | WSJ0 SI-84 (7138 utterances, 83 speakers), six speakers held out |
| **Training noise** | 10,000 noises from Sound Ideas library (~126 hours) |
| **Test noises** | Babble, cafeteria (Auditec CD) |
| **Training SNRs** | Randomly sampled from {-5, -4, -3, -2, -1, 0} dB |
| **Test SNRs** | -5 dB, -2 dB |
| **Training mixtures** | 320,000 (~500 hours total) |
| **Optimizer** | Adam, learning rate 0.0002 |
| **Loss function** | Mean squared error (MSE) |
| **Batch size** | 16 (utterance-level, zero-padded) |
| **Input features** | 161-dim STFT magnitude spectrum |
| **Training target** | Clean speech magnitude spectrum |
| **Evaluation metrics** | STOI (%), PESQ |

## Results

### STOI and PESQ Scores

**Table 1 — Trained speakers:**

| Model | Avg. STOI (-5 dB) | Avg. PESQ (-5 dB) | Avg. STOI (-2 dB) | Avg. PESQ (-2 dB) |
|-------|-------------------|-------------------|-------------------|-------------------|
| Unprocessed | 58.18% | 1.50 | 65.75% | 1.67 |
| LSTM-1 | 75.81% | 2.05 | 82.00% | 2.22 |
| LSTM-2 | ~75.8% | ~2.05 | ~82.0% | ~2.22 |
| **CRN (proposed)** | **~77.8%** | **~2.15** | **~83.5%** | **~2.32** |

**Table 2 — Untrained speakers (speaker generalization):**

| Model | Avg. STOI (-5 dB) | Avg. PESQ (-5 dB) | Avg. STOI (-2 dB) | Avg. PESQ (-2 dB) |
|-------|-------------------|-------------------|-------------------|-------------------|
| Unprocessed | 57.86% | 1.52 | 65.08% | 1.66 |
| LSTM-1 | 74.33% | 1.96 | 81.75% | 2.13 |
| LSTM-2 | ~74.3% | ~1.96 | ~81.8% | ~2.13 |
| **CRN (proposed)** | **~76.5%** | **~2.06** | **~83.3%** | **~2.23** |

### Parameter Efficiency

| Model | Parameters (million) |
|-------|---------------------|
| LSTM-1 | 36.81 |
| LSTM-2 | 30.22 |
| **CRN** | **17.58** |

The CRN has roughly half the parameters of LSTM-2 while achieving better performance, attributed to weight sharing in convolutional layers.

### Convergence

The CRN converges faster and achieves lower training and test MSE than both LSTM baselines, demonstrating better optimization properties partly due to batch normalization.

## Key Contributions

1. **Novel CRN architecture** for real-time monaural speech enhancement, combining convolutional encoder-decoder with LSTM for the first time in this domain.
2. **Causal design** using causal convolutions (with asymmetric zero-padding) ensures the system is naturally suitable for real-time applications with no future information.
3. **Noise- and speaker-independent** performance: the model generalizes to unseen noise types and untrained speakers, a critical property for practical deployment.
4. **Superior efficiency**: CRN achieves better STOI and PESQ than LSTM baselines while using ~42–52% fewer parameters (17.58M vs 30.22–36.81M).
5. **Faster convergence** during training, attributed to batch normalization and the architectural inductive bias.

## Related Concepts

- [[concepts/convolutional-recurrent-network|Convolutional Recurrent Network (CRN)]]
- [[concepts/complex-spectrum-mapping|Complex Spectrum Mapping]]
- [[concepts/broadcasted-residual-learning|Broadcasted Residual Learning]]
- [[concepts/gtcrn|GTCRN]]
- [[concepts/causality|Causality]]
- [[concepts/neural-networks|Neural Networks]]
- [[concepts/depthwise-separable-convolution|Depthwise Separable Convolution]]
- [[concepts/subspectral-normalization|Subspectral Normalization]]

## Related Synthesis

- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]]
- [[synthesis/computational-efficiency-evolution|Computational Efficiency Evolution]]
- [[synthesis/ai-driven-anc|AI-Driven ANC]]
