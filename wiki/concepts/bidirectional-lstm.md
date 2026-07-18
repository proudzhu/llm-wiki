---
type: concept
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
tags:
  - deep-learning
  - recurrent-neural-network
  - bidirectional
  - context-modeling
---

# Bidirectional LSTM

**Bidirectional LSTM (BiLSTM)** extends the standard [[concepts/long-short-term-memory\|LSTM]] architecture by processing the input sequence in both forward and backward directions. This allows the network to capture context from both the past and the future, enhancing its ability to understand dependencies in the sequence.

## Architecture

BiLSTM maintains two separate hidden states for each time step: one for the forward pass $\overrightarrow{\mathbf{h}}_t$ and one for the backward pass $\overleftarrow{\mathbf{h}}_t$. These are computed using the standard LSTM equations (see [[concepts/long-short-term-memory\|LSTM]]) but in opposite directions:

$$
\overrightarrow{\mathbf{h}}_t = \text{LSTM}_{\text{fwd}}(\mathbf{x}_t, \overrightarrow{\mathbf{h}}_{t-1}), \quad \overleftarrow{\mathbf{h}}_t = \text{LSTM}_{\text{bwd}}(\mathbf{x}_t, \overleftarrow{\mathbf{h}}_{t+1}).
$$

The output at time $t$ is computed by concatenating the two hidden states:

$$
\mathbf{y}_t = \sigma_y(\mathbf{W}_{hy}[\overrightarrow{\mathbf{h}}_t; \overleftarrow{\mathbf{h}}_t] + \mathbf{b}_y),
$$

where $[;]$ denotes concatenation. BiLSTM features **external recurrence** between layers as it processes the input in both directions, maintaining separate hidden states for each.

## Why Bidirectional?

For tasks where understanding both the preceding and succeeding elements is crucial — named entity recognition, machine translation, speech recognition, sentiment analysis — bidirectional processing captures the full context of a sequence. For instance, in language modeling, understanding surrounding words significantly enhances the accuracy of predicting the next word.

## Cost

BiLSTM requires roughly **twice the computational resources** of unidirectional LSTM because the sequence is processed twice (forward and backward). It also cannot be used in real-time streaming applications where only past context is available (the backward pass requires future inputs).

## Applications

Per [[sources/mienye-2024-rnn-comprehensive-review\|Mienye et al. 2024]], BiLSTM is identified as the most effective RNN variant for:
- **Sentiment analysis** — bidirectional processing captures intrinsic sentiment; Sangeetha & Kumaran 2023, Wankhade et al. 2024 (CNN+BiLSTM+attention)
- **Bioinformatics** — Zhang et al. 2020 (DeepSite, DNA-binding prediction), Yadav et al. 2019 (BiLSTM+CNN for protein sequences)
- **Anomaly detection** — Matar et al. 2023 (multivariate time series); BiLSTM captures temporal dependencies in both directions

Other uses in the surveyed literature:
- Character-level text generation (Gajendran et al. 2020)
- Financial forecasting (Luo et al. 2024 — attention-based CNN-BiLSTM)
- ECG anomaly detection (Mini et al. 2023)

## Distinction from Unidirectional LSTM

BiLSTM should not be used when:
- Future context is unavailable at inference time (streaming/online applications)
- Latency constraints make the 2× compute cost prohibitive
- The task does not benefit from future context (e.g., pure autoregressive generation)

For streaming speech enhancement or AEC applications (e.g., [[concepts/percepnet\|PercepNet]], [[concepts/nsnet2\|NSNet2]]), **unidirectional** LSTM/GRU is used instead.

## Related Concepts

- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/recurrent-neural-network\|Recurrent Neural Network]]
- [[concepts/gated-recurrent-unit\|Gated Recurrent Unit (GRU)]]
- [[concepts/attention-mechanism\|Attention Mechanism]]
- [[concepts/convolutional-recurrent-network\|Convolutional Recurrent Network]]

## Related Sources

- [[sources/mienye-2024-rnn-comprehensive-review\|Mienye, Swart & Obaido 2024: RNN Comprehensive Review]] — surveys BiLSTM applications across sentiment analysis, bioinformatics, and anomaly detection
