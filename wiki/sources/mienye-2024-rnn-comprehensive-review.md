---
type: source
created: 2026-07-18
updated: 2026-07-18
sources:
  - raw/papers/mienye-2024-rnn-comprehensive-review/full-text.md
  - https://doi.org/10.3390/info15090517
  - zotero://select/items/0_7GY9DG4W
tags:
  - deep-learning
  - machine-learning
  - recurrent-neural-network
  - lstm
  - gru
  - bidirectional-rnn
  - echo-state-network
  - attention
  - transformer
  - review
  - natural-language-processing
  - speech-recognition
  - time-series
---

# Mienye, Swart & Obaido 2024: Recurrent Neural Networks — A Comprehensive Review of Architectures, Variants, and Applications

| Field | Value |
|-------|-------|
| **Authors** | [[entities/ibomoiye-domor-mienye\|Ibomoiye Domor Mienye]]<sup>∗,†</sup>, [[entities/theo-g-swart\|Theo G. Swart]]<sup>1,†</sup>, [[entities/george-obaido\|George Obaido]]<sup>2,†</sup> |
| **Institution** | <sup>1</sup>Institute for Intelligent Systems, University of Johannesburg, South Africa; <sup>2</sup>Center for Human-Compatible Artificial Intelligence (CHAI) / Berkeley Institute for Data Science (BIDS), University of California, Berkeley, USA |
| **Published** | Information, 2024, 15(9), 517 |
| **Type** | Journal Article (Review) |
| **DOI** | [10.3390/info15090517](https://doi.org/10.3390/info15090517) |
| **URL** | [https://www.mdpi.com/2078-2489/15/9/517](https://www.mdpi.com/2078-2489/15/9/517) |
| **Zotero** | [7GY9DG4W](zotero://select/items/0_7GY9DG4W) |

## Summary

This is a comprehensive review paper covering **recurrent neural network (RNN) architectures, variants, and applications**. It synthesizes the literature from the original RNN formulation through [[concepts/long-short-term-memory\|LSTM]] and [[concepts/gated-recurrent-unit\|GRU]], to bidirectional, stacked, peephole, echo-state, and independently recurrent variants, and surveys applications across NLP, speech recognition, time-series forecasting, signal processing, bioinformatics, autonomous vehicles, and anomaly detection. The review also covers recent innovations such as hybrid RNN+CNN and RNN+transformer architectures, attention mechanisms, neural architecture search, and advanced optimizers (Adam, gradient clipping), and concludes with open challenges in scalability, interpretability, bias, data dependency, and generalization.

## Problem Formulation

Unlike feedforward networks, RNNs maintain an internal state $\mathbf{h}_t$ that captures information about previous inputs, enabling them to process **sequential data**. At each time step $t$, the standard RNN updates its hidden state by:

$$
\mathbf{h}_t = \sigma_h(\mathbf{W}_{xh}\mathbf{x}_t + \mathbf{W}_{hh}\mathbf{h}_{t-1} + \mathbf{b}_h), \tag{1}
$$

$$
\mathbf{y}_t = \sigma_y(\mathbf{W}_{hy}\mathbf{h}_t + \mathbf{b}_y), \tag{2}
$$

where $\mathbf{W}_{xh}$, $\mathbf{W}_{hh}$, $\mathbf{W}_{hy}$ are the input-to-hidden, recurrent, and hidden-to-output weight matrices, and $\sigma_h$, $\sigma_y$ are activation functions (typically tanh, ReLU, or sigmoid). Training uses [[concepts/backpropagation-through-time\|BPTT]] (backpropagation through time), which unrolls the network across time steps. The central difficulty is the **vanishing/exploding gradient problem**: when computing $\partial \mathbf{h}_t / \partial \mathbf{h}_{t-n} = \prod_{k=t-n}^{t-1} \mathbf{J}_k$, if the eigenvalues of the Jacobians $\mathbf{J}_k$ are < 1, gradients vanish; if > 1, they explode. This motivates the gated variants (LSTM, GRU) reviewed in the paper.

![[raw/papers/mienye-2024-rnn-comprehensive-review/figures/7fa3e4abc5624b24f6f23efa76e927b5df20a6504fa6d63019aa561a29259909.jpg|Basic RNN architecture]]
*Figure 1: Basic RNN architecture, showing the recurrent connection that allows information to cycle within the network.*

## Methodology

The paper is a **literature review** (no new model is proposed). It surveys:

### 1. Fundamental RNN architecture (Section 3)
- Basic RNN with hidden state update (Eq. 1)
- [[concepts/activation-functions\|Activation functions]]: tanh, ReLU, Leaky ReLU, ELU, sigmoid, softmax
- **Vanishing/exploding gradient** analysis via Jacobian eigenvalues
- **Bidirectional RNNs (BiRNNs)**: maintain forward $\overrightarrow{\mathbf{h}}_t$ and backward $\overleftarrow{\mathbf{h}}_t$ hidden states; output is concatenation
- **Deep RNNs**: stack $L$ recurrent layers; $\mathbf{h}_t^{(l)} = \sigma_h(\mathbf{W}_{xh}^{(l)}\mathbf{h}_t^{(l-1)} + \mathbf{W}_{hh}^{(l)}\mathbf{h}_{t-1}^{(l)} + \mathbf{b}_h^{(l)})$

### 2. Advanced RNN variants (Section 4)

**[[concepts/long-short-term-memory\|LSTM]]** (Hochreiter & Schmidhuber, 1997) — three gates (input $\mathbf{i}_t$, forget $\mathbf{f}_t$, output $\mathbf{o}_t$) regulate cell state $\mathbf{c}_t$:

$$
\mathbf{i}_t = \sigma(\mathbf{W}_{xi}\mathbf{x}_t + \mathbf{W}_{hi}\mathbf{h}_{t-1} + \mathbf{b}_i), \quad \mathbf{f}_t = \sigma(\mathbf{W}_{xf}\mathbf{x}_t + \mathbf{W}_{hf}\mathbf{h}_{t-1} + \mathbf{b}_f),
$$

$$
\mathbf{o}_t = \sigma(\mathbf{W}_{xo}\mathbf{x}_t + \mathbf{W}_{ho}\mathbf{h}_{t-1} + \mathbf{b}_o), \quad \mathbf{g}_t = \tanh(\mathbf{W}_{xg}\mathbf{x}_t + \mathbf{W}_{hg}\mathbf{h}_{t-1} + \mathbf{b}_g),
$$

$$
\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \mathbf{g}_t, \quad \mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t).
$$

![[raw/papers/mienye-2024-rnn-comprehensive-review/figures/b9999beb37a8d85a8242708f4dfd79fd9bc0cb4aa46f049c9c675654d4bd4563.jpg|LSTM cell architecture]]
*Figure 2: Architecture of the LSTM network, showing the input, forget, and output gates regulating the cell state.*

**[[concepts/bidirectional-lstm\|Bidirectional LSTM (BiLSTM)]]** — runs LSTM forward and backward; captures both past and future context.

**Stacked LSTM** — stacks multiple LSTM layers; lower layers capture local patterns, higher layers capture abstract long-term dependencies.

**[[concepts/gated-recurrent-unit\|GRU]]** (Cho et al., 2014) — simplifies LSTM with two gates (update $\mathbf{z}_t$, reset $\mathbf{r}_t$) and merged cell/hidden state:

$$
\mathbf{z}_t = \sigma(\mathbf{W}_{xz}\mathbf{x}_t + \mathbf{W}_{hz}\mathbf{h}_{t-1} + \mathbf{b}_z), \quad \mathbf{r}_t = \sigma(\mathbf{W}_{xr}\mathbf{x}_t + \mathbf{W}_{hr}\mathbf{h}_{t-1} + \mathbf{b}_r),
$$

$$
\mathbf{h}_t' = \tanh(\mathbf{W}_{xh}\mathbf{x}_t + \mathbf{r}_t \odot (\mathbf{W}_{hh}\mathbf{h}_{t-1}) + \mathbf{b}_h), \quad \mathbf{h}_t = (1-\mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \mathbf{h}_t'.
$$

GRUs have fewer parameters than LSTM and often achieve comparable performance.

**[[concepts/peephole-lstm\|Peephole LSTM]]** (Gers & Schmidhuber) — gates get direct access to cell state via "peephole" weights $\mathbf{W}_{ci}$, $\mathbf{W}_{cf}$, $\mathbf{W}_{co}$.

**[[concepts/echo-state-network\|Echo State Network (ESN)]]** (Jaeger) — fixed random reservoir $\mathbf{W}_{res}$, only $\mathbf{W}_{out}$ is trained. Variants: Deep ESNs (stacked reservoirs), Ensemble Deep ESNs, ESNs with signal decomposition (e.g., EWT).

**[[concepts/independently-recurrent-neural-network\|Independently Recurrent NN (IndRNN)]]** (Li et al.) — uses element-wise recurrent weights $\mathbf{u} \odot \mathbf{h}_{t-1}$ to decouple neurons, enabling training of very deep RNNs.

### 3. Innovations in architectures and training (Section 5)

- **Hybrid architectures**: CNN+RNN (spatial+temporal), RNN+attention
- **Neural Architecture Search (NAS)**: $\mathcal{A}^* = \arg\max_{\mathcal{A} \in \mathcal{S}} \text{Accuracy}(\mathcal{A})$
- **[[concepts/gradient-clipping\|Gradient clipping]]**: $\mathbf{g} \leftarrow \mathbf{g}/\max(1, \|\mathbf{g}\|/\tau)$
- **[[concepts/adam-optimizer\|Adam optimizer]]**: adaptive moment estimation with bias correction
- **[[concepts/attention-mechanism\|Attention mechanisms]]**: $\mathbf{c}_t = \sum_{i=1}^T \text{softmax}(\mathbf{u}_t)_i \mathbf{h}_i$
- **RNN + Transformer integration**: leverage sequential processing of RNNs and parallel self-attention of transformers

### 4. Public datasets (Section 6)

| Dataset | Application |
|---------|-------------|
| Penn Treebank | NLP / language modeling |
| IMDB Reviews | Sentiment analysis |
| MNIST Sequential | Image recognition (sequence-to-sequence) |
| TIMIT Speech Corpus | Speech recognition |
| Reuters-21578 | Text categorization |
| UCI ML Repository: Time Series | Time series forecasting |
| CORe50 | Continuous object recognition (video) |

## Applications (Section 7)

The paper surveys seven major application areas:

| Domain | Best RNN variant (per paper) | Representative works |
|--------|------------------------------|----------------------|
| **NLP — text generation** | LSTM | Souri 2018 (Arabic), Gajendran 2020 (BiLSTM char-level), Hu 2020 (VAE+RNN), Keskar 2019 (CTRL) |
| **NLP — sentiment analysis** | BiLSTM | Yadav 2023 (LSTM), Abimbola 2024 (LSTM-CNN), Wankhade 2024 (CNN+BiLSTM+attn), Zulqarnain 2024 (GRU+attn) |
| **NLP — machine translation** | LSTM+Transformer hybrid | Wu 2016 (GNMT), Sennrich 2015 (BPE), Vaswani 2017 (Transformer), Yang 2017 (RNN+Transformer), Song 2019 (BERT+MT) |
| **Speech recognition** | LSTM | Hinton 2012, Hannun 2014 (DeepSpeech), Amodei 2016 (DeepSpeech2), Chiu 2018 (RNN-T), Dong 2018 (Speech-Transformer) |
| **Time series forecasting** | LSTM | Fischer & Krauss 2018 (stock returns), Bao 2017 (LSTM+autoencoder), Marulanda 2023 (wind power), Chen 2024 (BiGRU+TCN) |
| **Signal processing** | ESN | Mastoi 2019 (heart rate), [[sources/valin-2021-percepnet-joint-echo-control\|Valin 2021 (PercepNet)]] (speech enhancement), Gao 2021 (EWT+ESN) |
| **Bioinformatics** | BiLSTM | Li 2019 (gene/protein), Zhang 2020 (DeepSite), Xu 2021 (protein secondary), Yadav 2019 (BiLSTM+CNN) |
| **Autonomous vehicles** | LSTM+CNN hybrid | Lee 2020 (end-to-end driving), Altché & de La Fortelle 2017 (trajectory), Codevilla 2018 (imitation learning) |
| **Anomaly detection** | BiLSTM | Matar 2023 (multivariate), Kumaresan 2024 (network), Mini 2023 (ECG), Zhou & Paffenroth 2017 (autoencoder) |

> **Notable cross-reference**: The paper cites [[sources/valin-2021-percepnet-joint-echo-control\|Valin et al. 2021 (PercepNet)]] as a representative application of **echo state networks** in speech signal enhancement — this is the same Valin et al. work already ingested in the wiki as a foundational AEC paper. The review classifies it under "Signal Processing" alongside heart-rate monitoring and EWT-based forecasting.

## Key Contributions

1. **Comprehensive taxonomy** of RNN architectures: basic RNN, LSTM, GRU, BiLSTM, Stacked LSTM, Peephole LSTM, ESN (with Deep/Ensemble/EWT variants), IndRNN — summarized in a comparative table (Table 2) covering key features, gradient stability, and typical applications.
2. **Cross-domain application survey** covering 7 major areas with per-domain "best variant" recommendations and extensive citation tables (Tables 4–6) spanning 2012–2024.
3. **Innovations review** covering hybrid architectures (CNN+RNN, RNN+Transformer), attention mechanisms, NAS, gradient clipping, Adam, and Hessian-free optimization.
4. **Public dataset catalog** (Table 3) for RNN research across NLP, speech, vision, and time series.
5. **Challenges and future directions**: scalability (sequential bottleneck vs. parallel transformers), interpretability (LIME/SHAP, inherent interpretability), bias/fairness, data dependency, and overfitting/generalization.

## Limitations and Caveats

- The review is **non-quantitative** — it does not run benchmarks; "best variant" claims per domain are based on aggregating the conclusions of cited papers rather than head-to-head experiments under matched conditions.
- The review does **not** cover more recent (2024+) efficient RNN variants such as [[concepts/linear-recurrent-unit\|Linear Recurrent Units (LRUs)]], [[concepts/mingru\|MinGRU]], [[concepts/mamba-mingru\|Mamba-MinGRU]], or [[concepts/state-space-model\|State-Space Models]] (Mamba, S4, etc.). These are covered elsewhere in the wiki.
- Coverage of [[concepts/real-time-recurrent-learning\|Real-Time Recurrent Learning]] and [[concepts/backpropagation-through-time\|BPTT]] alternatives is minimal; see [[sources/zucchet-2026-forward-propagation-errors-through-time\|Zucchet 2026]] for a deeper treatment of forward-propagation alternatives.
- The paper's framing of "LSTM as best for X" reflects common practice in the surveyed literature; in many domains (notably machine translation and speech recognition) transformer-based models have since become dominant, and the review acknowledges this shift.

## Related Concepts

- [[concepts/recurrent-neural-network\|Recurrent Neural Network]] — central topic of the review
- [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]]
- [[concepts/gated-recurrent-unit\|Gated Recurrent Unit (GRU)]]
- [[concepts/bidirectional-lstm\|Bidirectional LSTM (BiLSTM)]]
- [[concepts/peephole-lstm\|Peephole LSTM]]
- [[concepts/echo-state-network\|Echo State Network (ESN)]]
- [[concepts/independently-recurrent-neural-network\|Independently Recurrent NN (IndRNN)]]
- [[concepts/backpropagation-through-time\|Backpropagation Through Time (BPTT)]]
- [[concepts/vanishing-gradient-problem\|Vanishing/Exploding Gradient Problem]]
- [[concepts/activation-functions\|Activation Functions]]
- [[concepts/attention-mechanism\|Attention Mechanism]]
- [[concepts/adam-optimizer\|Adam Optimizer]]
- [[concepts/gradient-clipping\|Gradient Clipping]]
- [[concepts/neural-architecture-search\|Neural Architecture Search]]
- [[concepts/grouped-recurrent-neural-network\|Grouped Recurrent Neural Network]] — related efficient RNN variant
- [[concepts/linear-recurrent-unit\|Linear Recurrent Unit]] — modern efficient RNN not covered by the review
- [[concepts/convolutional-recurrent-network\|Convolutional Recurrent Network (CRN)]] — hybrid architecture referenced in the speech recognition section

## Related Synthesis

- (None yet — this review is broad rather than a deep cross-source analysis. Future synthesis pages on efficient sequence modeling or RNN-vs-transformer trade-offs could reference it.)

## Related Sources

- [[sources/valin-2021-percepnet-joint-echo-control\|Valin et al. 2021: PercepNet Joint Echo Control]] — cited in the review as a representative ESN application for speech enhancement
- [[sources/tan-2018-convolutional-recurrent-network-speech-enhancement\|Tan & Wang 2018: CRN for Speech Enhancement]] — CRN architecture (CNN+RNN hybrid) used in speech enhancement
- [[sources/zucchet-2026-forward-propagation-errors-through-time\|Zucchet 2026: Forward Propagation of Errors Through Time]] — deeper treatment of BPTT alternatives
- [[sources/yamazaki-2022-spiking-nn-review\|Yamazaki 2022: Spiking Neural Networks Review]] — third-generation neural networks survey
