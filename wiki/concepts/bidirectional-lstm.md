---
type: concept
created: 2026-07-18
updated: 2026-11-22
sources:
  - raw/papers/heymann-2016-neural-spectral-mask-beamforming/full-text.md
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
  - raw/papers/fu-2019-metricgan/full-text.md
  - raw/papers/fu-2021-metricgan-plus/full-text.md
  - raw/papers/close-2022-metricgan-plus-minus/full-text.md
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

Beyond the survey's scope, BLSTMs were the workhorse of early neural speech-enhancement front-ends: [[sources/heymann-2016-neural-spectral-mask-beamforming|Heymann, Drude & Haeb-Umbach 2016]] use one (256 BLSTM units → 2×513 FF → sigmoid output) to estimate speech/noise spectral masks for acoustic beamforming, where temporal context lets it distinguish speech from high-energy stationary noise that fools per-frequency parametric estimators. Notably, a tiny feed-forward network (single hidden layer, single-frame input) nearly matched the BLSTM when both were trained on clean speech only — bidirectional temporal context matters most under noise-aware training.

[[sources/fu-2019-metricgan|Fu et al. 2019 (MetricGAN, ICML)]] mark the other end of that era: a 2-layer BLSTM (200 units/direction) → FC 300 LeakyReLU → FC 257 sigmoid emits the magnitude mask, floored at 0.05 to suppress musical noise, and the network's *capacity* was deliberately held fixed while the training objective varied. That control is what makes the result usable as evidence — the BLSTM is not the contribution, it is the fixture that lets a mask-based generator be compared fairly under $L_1$, conventional adversarial, RL, and metric-surrogate objectives (2.033 / 2.002 / 2.098 / 2.133 PESQ respectively on TIMIT).

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
- [[sources/heymann-2016-neural-spectral-mask-beamforming|Heymann, Drude & Haeb-Umbach 2016: Neural Network Based Spectral Mask Estimation for Acoustic Beamforming]] — BLSTM spectral-mask estimation for beamforming; temporal context most valuable under noise-aware training
- [[sources/fu-2019-metricgan|Fu, Liao, Tsao & Lin 2019: MetricGAN]] — a 2-layer BLSTM mask estimator held fixed as a fixture across four training objectives (L1 / CGAN / RL / metric surrogate), isolating the loss function from the architecture
- [[sources/fu-2021-metricgan-plus|Fu et al. 2021: MetricGAN+]] — same 2-layer BLSTM (200 units) fixture as MetricGAN, mask head swapped to a learnable sigmoid: PESQ 2.71 (MSE) → 3.15 (metric surrogate + training techniques) on VoiceBank+DEMAND, beating attention and phase-aware systems without changing the backbone
- [[sources/close-2022-metricgan-plus-minus|Close, Hain & Goetze 2022: MetricGAN+/-]] — the same 2×200 BLSTM mask estimator instantiated *twice*: enhancer (target score 1) and de-generator (target score w < 1), the latter manufacturing degraded training data for the metric surrogate
