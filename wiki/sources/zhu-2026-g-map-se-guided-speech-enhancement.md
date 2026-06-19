---
type: source
created: 2026-06-19
updated: 2026-06-19
sources:
  - raw/papers/zhu-2026-g-map-se-guided-speech-enhancement/full-text.md
  - https://doi.org/10.48550/arXiv.2606.08580
  - zotero://select/items/N5AZRUJV
tags:
  - speech-enhancement
  - speaker-embedding
  - gaussian-mixture-model
  - prior-matching
  - interspeech-2026
---

# Zhu, Wang, Liu, Li, Chen, Xia, Huang & Xie 2026: G-MaP-SE

**Authors**: [[entities/yike-zhu|Yike Zhu]], [[entities/ziqian-wang|Ziqian Wang]], [[entities/zikai-liu|Zikai Liu]], [[entities/xingchen-li|Xingchen Li]], [[entities/zhuangqi-chen|Zhuangqi Chen]], [[entities/xianjun-xia|Xianjun Xia]], [[entities/chuanzeng-huang|Chuanzeng Huang]], [[entities/lei-xie|Lei Xie]]
**Affiliations**: Audio, Speech and Language Processing Group (ASLP@NPU), School of Software, Northwestern Polytechnical University, Xi'an, China
**Venue**: Interspeech 2026
**Year**: 2026
**Type**: Conference Paper (arXiv preprint)
**DOI**: [10.48550/arXiv.2606.08580](https://doi.org/10.48550/arXiv.2606.08580)
**Zotero**: [Link](zotero://select/items/N5AZRUJV)
**arXiv**: [2606.08580](https://arxiv.org/abs/2606.08580)
**Code**: Available online (see paper)

## Summary

G-MaP-SE is a guided speech enhancement framework that refines noisy speaker-conditioning embeddings by matching them to a clean-speech GMM prior. The method builds a Gaussian Mixture Model (GMM) on clean-speech speaker embeddings offline, then at inference time matches the noisy embedding to this prior via soft cosine-similarity weighting over GMM components. The refined prior embedding is injected into an MP-SENet backbone through a lightweight gated fusion module. Experiments on VoiceBank+DEMAND and DNS Challenge 2020 show consistent gains over noisy conditioning under domain shift, narrowing the gap to oracle clean conditioning without requiring any enrollment audio at inference time.

## Problem Formulation

Let $x \in \mathbb{R}^{T}$ denote clean speech, $y \in \mathbb{R}^{T}$ the noisy observation, and $n$ additive noise such that:

$$
y = x + n
$$

The goal of speech enhancement is to estimate $\hat{x}$ from $y$. The paper addresses the problem of using speaker embeddings as conditioning signals to guide the enhancement process, where existing approaches either require clean enrollment audio (impractical) or extract embeddings from noisy speech (fragile under noise and domain shift).

**Key idea**: Replace the noisy conditioning embedding $e_{\text{noisy}}$ with a refined prior embedding $e_{\text{prior}}$ obtained by matching $e_{\text{noisy}}$ against a clean-speech GMM prior $P$.

## Methodology

![[raw/papers/zhu-2026-g-map-se-guided-speech-enhancement/figures/x1.png|Overview of G-MaP-SE framework]]
*Figure 1: Overview of G-MaP-SE. The noisy input is fed to both the SE model and a frozen feature extractor. The MaP module matches the noisy embedding to a precomputed GMM prior and produces a refined prior embedding, which is injected into the backbone via gated fusion.*

### GMM Prior Construction

A GMM with $K$ diagonal-covariance components is fit via EM on $\ell_2$-normalized speaker embeddings extracted from clean speech using a frozen ECAPA-TDNN extractor:

$$
p(e) = \sum_{k=1}^{K} \pi_k \, \mathcal{N}(e; \mu_k, \Sigma_k)
$$

The prior $P$ is represented by the $K$ GMM means $\{\mu_k\}_{k=1}^{K}$.

### Matching Module (MaP)

Given a noisy embedding $e_{\text{noisy}} = f(y)$, the MaP module computes soft assignment weights via cosine similarity with temperature $\tau$:

$$
a_k = \frac{\tilde{e}^{\top} \tilde{\mu}_k}{\tau}, \quad
\gamma_k = \frac{\exp(a_k)}{\sum_{j=1}^K \exp(a_j)}
$$

The matched prior embedding is a weighted combination of GMM means:

$$
e_{\text{prior}} = \sum_{k=1}^K \gamma_k \mu_k
$$

### Gated Fusion Module

The prior embedding is injected into intermediate features of the MP-SENet backbone via a learned gate:

$$
g = \sigma(W [Y, E]), \quad
\hat{Y} = (1-g) \odot Y + g \odot E
$$

where $Y$ and $E$ are the projected SE feature map and projected conditioning embedding after broadcast, $W$ is a learnable projection, $\sigma$ is sigmoid, and $\odot$ is element-wise multiplication.

### Feature Extractor

A frozen ECAPA-TDNN model outputs 192-dimensional $\ell_2$-normalized speaker embeddings. The extractor remains frozen during training to keep the embedding space consistent with the GMM prior.

## Experimental Setup

| Setting | Value |
|---------|-------|
| **Backbone** | MP-SENet (4 TF blocks, 64 channels, 4 attention heads) |
| **Feature Extractor** | ECAPA-TDNN (frozen, 192-d embeddings) |
| **GMM Components $K$** | 192 |
| **Temperature $\tau$** | 0.2 |
| **Train Dataset** | VoiceBank+DEMAND (VBD) training split |
| **In-domain Test** | VBD test set (2 unseen speakers) |
| **Cross-domain Test** | DNS Challenge 2020 (w/o reverb) |
| **Loss** | Multi-component: $L_{\text{pesq}} + L_{\text{stft}} + L_{\text{mag}} + L_{\text{com}} + L_{\text{pha}} + L_{\text{time}}$ |
| **Optimizer** | AdamW ($\beta_1=0.8$, $\beta_2=0.99$, weight decay 0.01) |
| **Learning Rate** | 0.0005, decayed 0.99 per epoch |
| **Training Steps** | 500k |
| **Batch Size** | 4 |
| **GPU** | Single NVIDIA V100 (32 GB) |
| **Params (Backbone)** | 2.263M (MP-SENet) / 2.288M (G-MaP-SE, +0.025M for fusion) |
| **Audio Preprocessing** | 16 kHz, 2-second segments, STFT with 25ms window/6.25ms hop, magnitude compression $\gamma=0.3$ |
| **Metrics (VBD)** | WB-PESQ, CSIG, CBAK, COVL, STOI, SSNR |
| **Metrics (DNS2020)** | WB-PESQ, NB-PESQ, STOI, SI-SDR |

## Results

| Model | VBD WB-PESQ | VBD CSIG | VBD CBAK | VBD COVL | VBD STOI(%) | VBD SSNR(dB) | DNS2020 WB-PESQ | DNS2020 NB-PESQ | DNS2020 STOI(%) | DNS2020 SI-SDR(dB) |
|-------|:-----------:|:--------:|:---------:|:---------:|:-----------:|:------------:|:--------------:|:--------------:|:--------------:|:-----------------:|
| Noisy | 1.97 | 3.49 | 2.55 | 2.74 | 92.11 | 1.68 | 1.582 | 2.161 | 91.519 | 9.230 |
| MP-SENet | 3.60 | 4.81 | 3.99 | 4.34 | 96.12 | 10.39 | 2.790 | 3.303 | 95.878 | 16.277 |
| MP-SENet$^*$ | 3.59 | 4.80 | 4.00 | 4.34 | 96.11 | 10.39 | 2.789 | 3.302 | 95.876 | 16.280 |
| +Oracle-Cond | 3.58 | 4.80 | 4.00 | 4.33 | 96.05 | 10.73 | 2.796 | 3.352 | 96.090 | 16.455 |
| +Noisy-Cond | 3.56 | 4.79 | 4.00 | 4.31 | 96.09 | 10.66 | 2.765 | 3.323 | 95.908 | 16.340 |
| **+G-MaP ($P_{\text{VBD}}$)** | **3.59** | **4.80** | **4.00** | **4.33** | **96.10** | **10.67** | **2.794** | **3.349** | **96.065** | **16.454** |
| **+G-MaP ($P_{\text{DNS}}$)** | **3.58** | **4.80** | **3.99** | **4.32** | **96.07** | **10.67** | **2.794** | **3.350** | **96.072** | **16.454** |

*$^*$ denotes reproduced result. Oracle-Cond and Noisy-Cond condition on clean and noisy embeddings, respectively. G-MaP matches noisy embedding to clean GMM prior.*

**Key Findings**:
- On VBD (in-domain), G-MaP improves slightly over noisy conditioning and approaches oracle conditioning
- On DNS2020 (cross-domain), G-MaP provides **consistent gains across all metrics** and substantially narrows the gap to oracle conditioning
- Swapping the prior from $P_{\text{VBD}}$ to $P_{\text{DNS}}$ further improves cross-domain performance **without retraining the backbone**, demonstrating plug-and-play adaptability
- The MaP module has **zero trainable parameters**; only 0.025M parameters added by the fusion block

### Ablation Study

- **Temperature $\tau$**: Performance peaks at $\tau = 0.2$. Lower values over-commit to a single prototype; higher values over-smooth toward a mean prototype.
- **GMM components $K$**: Mild peak at $K = 192$. Performance is more sensitive to $\tau$ than $K$ within reasonable ranges.
![[raw/papers/zhu-2026-g-map-se-guided-speech-enhancement/figures/x3.png|Ablation study on temperature and GMM components]]
*Figure 3: Ablation on VBD with respect to matching temperature $	au$ (left, $K=192$) and number of GMM components $K$ (right, $	au=0.2$). Performance peaks at $	au=0.2$ and $K=192$.*


### Embedding Analysis

![[raw/papers/zhu-2026-g-map-se-guided-speech-enhancement/figures/x2.png|Embedding cosine similarity distributions]]
*Figure 2: Cosine similarity between noisy/clean embeddings (left) and matched-prior/clean embeddings (right). The matched embedding shifts toward higher similarity with clean embeddings, validating the noise-correction effect of GMM matching.*

G-MaP shifts the cosine similarity distribution between noisy and clean embeddings toward higher similarity, confirming that GMM matching corrects noise-induced distortions. Some utterances see limited improvement due to suboptimal prototype assignment, but the matched embedding stays in the clean embedding space, reducing noise artifacts.

## Key Contributions

1. **GMM-based prior matching** for refining noisy speaker-conditioning embeddings in speech enhancement, requiring no enrollment audio at inference time.
2. **Lightweight gated fusion module** that injects the matched prior embedding into a TF-domain backbone with only 0.025M added parameters.
3. **Zero-parameter matching module** — the MaP module has no trainable parameters; the prior is a fixed $K \times D$ prototype matrix.
4. **Plug-and-play domain adaptation** — the GMM prior can be swapped across datasets without retraining the enhancement backbone, enabling easy adaptation to target domains.
5. **Comprehensive evaluation** on both in-domain (VoiceBank+DEMAND) and cross-domain (DNS Challenge 2020) benchmarks, demonstrating consistent improvements over noisy conditioning.

## Related Concepts

- [[concepts/speech-enhancement|Speech Enhancement]]
- [[concepts/gaussian-mixture-model|Gaussian Mixture Model (GMM)]]
- [[concepts/speaker-embedding|Speaker Embedding]]
- [[concepts/prior-matching|Prior Matching]]
- [[concepts/ecapa-tdnn|ECAPA-TDNN]]
- [[concepts/mp-senet|MP-SENet]]
- [[concepts/personalized-speech-enhancement|Personalized Speech Enhancement]]
- [[concepts/voicebank-demand|VoiceBank+DEMAND]]
- [[concepts/dns-challenge|DNS Challenge]]
- [[concepts/pesq|PESQ]]

## Related Synthesis

- [[synthesis/multi-modal-speech-enhancement|Multi-Modal Speech Enhancement]]

