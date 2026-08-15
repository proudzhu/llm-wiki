---
type: source
created: 2026-08-15
updated: 2026-08-15
sources:
  - raw/papers/lugo-2026-diffvqe/full-text.md
  - https://doi.org/10.48550/arXiv.2605.08189
  - zotero://select/items/0_9UTQLQW7
tags:
  - speech-enhancement
  - acoustic-echo-cancellation
  - diffusion-models
  - generative-models
  - voice-quality-enhancement
---

# Lugo, Seidel, Mowlaee, Zhao & Fingscheidt 2026: DiffVQE

| Field | Value |
|-------|-------|
| **Authors** | [[entities/haljan-lugo\|Haljan Lugo]], [[entities/ernst-seidel\|Ernst Seidel]], [[entities/pejman-mowlaee\|Pejman Mowlaee]], [[entities/ziyue-zhao\|Ziyue Zhao]], [[entities/tim-fingscheidt\|Tim Fingscheidt]] |
| **Institution** | Institute for Communications Technology, TU Braunschweig (∗) + GN Advanced Science, Ballerup, Denmark (∘) |
| **Published** | arXiv preprint, 2026-06-17 (v2) |
| **Type** | Preprint |
| **DOI** | [10.48550/arXiv.2605.08189](https://doi.org/10.48550/arXiv.2605.08189) |
| **arXiv** | [2605.08189](https://arxiv.org/abs/2605.08189) |
| **Zotero** | [9UTQLQW7](zotero://select/items/0_9UTQLQW7) |
| **Audio demo** | [DiffVQE supplement](https://ifnspaml.github.io/DiffVQE-Demo/) |

## Summary

DiffVQE is, to the authors' knowledge, the **first fully reproducible diffusion-based acoustic echo control (AEC) model** (still non-causal), jointly suppressing acoustic echo and background noise in a hands-free system. It follows a hybrid discriminative+generative design: a Cond DNN first estimates the near-end speech, then a score-based Score DNN performs a **single-step** diffusion refinement — the topology and single-step formulation adapted from EffDiffSE (Fu et al., WASPAA 2025), with the training-data pipeline based on the published framework of Seidel et al. (2024) and speech/noise corpora from the [[concepts/urgent-challenge|Interspeech 2025 URGENT Challenge]].

Trained on ~623 h of synthetic AEC data, DiffVQE and its smaller variant DiffVQE-S outperform a **retrained DeepVQE baseline** on most quality and intelligibility metrics (PESQ, ESTOI, LPS, AECMOS Other/SIG/BAK) while needing only ~10–13% of DeepVQE's FLOPS and fewer parameters; DeepVQE retains a small edge on the echo-reduction metrics (DT/ST Echo). On the blind ICASSP 2023 AEC Challenge test set, DiffVQE reaches an average rank of 1.17 vs. 2.17 (DiffVQE-S) and 2.67 (DeepVQE).

> **Note on abstract vs. results**: The abstract claims DiffVQE "excels DeepVQE both in echo and noise control performance", but the body (Tables 1–2) shows DeepVQE still ahead on DT Echo and ST Echo (albeit close to the clean reference), with DiffVQE winning on all other metrics. The body's more precise statement should be trusted.

## Problem Formulation

Hands-free signal model (sample index $n$): the far-end signal $x(n)$ is played back through a loudspeaker with nonlinearity $x'(n) = f_{\mathrm{NL}}(x(n))$, and the microphone captures

$$
y(n) = s'(n) + d(n) + n(n),
$$

with near-end speech $s'(n) = h_2(n) * s(n)$, echo $d(n) = h_1(n) * x'(n)$ (convolution with room impulse responses $h_1, h_2$), and background noise $n(n)$. Both far-end and microphone signals are converted to $K$-point STFT frames $\mathbf{X} = (X_\ell(k))$ and $\mathbf{Y} = (Y_\ell(k))$, which feed the hybrid model; the goal is the enhanced near-end estimate $\hat{\mathbf{S}}$ (and time-domain $\hat{s}(n)$ via inverse STFT).

Score-based diffusion is formulated as an Itô SDE over continuous diffusion time $\tilde{t} \in [0, T]$,

$$
\mathrm{d}\mathbf{S}_{\tilde{t}} = \mathbf{f}(\mathbf{S}_{\tilde{t}}, \mathbf{Y}) \, \mathrm{d}\tilde{t} + g(\tilde{t}) \, \mathrm{d}\mathbf{W},
$$

with reverse-time SDE involving the score $\nabla_{\mathbf{S}_{\tilde{t}}} \log p_{\tilde{t}}(\mathbf{S}_{\tilde{t}}|\mathbf{Y})$. Using a **variance-exploding (VE)** SDE ($\mathbf{f} = 0$, $\sigma_{\tilde{t}}^2 = \sigma_{\min}^2 (\sigma_{\max}/\sigma_{\min})^{2\tilde{t}}$), the perturbed state is $\mathbf{S}_{\tilde{t}} = \mathbf{S} + \sigma_{\tilde{t}} \mathbf{Z}$ and the score equals $-\mathbf{Z}/\sigma_{\tilde{t}}$, yielding the denoising score matching objective

$$
J^{\mathrm{SM}}(\mathbf{S}, \sigma_{\tilde{t}}) = \mathbb{E}_{\mathbf{S},\mathbf{Z},\tilde{t}}\left[\left\lVert \mathbf{S}_{\theta}(\mathbf{S} + \sigma_{\tilde{t}}\mathbf{Z} | \sigma_{\tilde{t}}, \mathbf{C}) + \frac{\mathbf{Z}}{\sigma_{\tilde{t}}} \right\rVert^2\right],
$$

with conditioning variable $\mathbf{C}$ provided by the jointly trained Cond DNN.

## Methodology

### Hybrid Cond DNN + Score DNN framework

- **Cond DNN** (discriminative): concatenates the far-end reference $\mathbf{X}$ with the microphone signal $\mathbf{Y}$ (**early fusion**) and outputs the first near-end estimate $\hat{\mathbf{S}}^{\mathrm{cond}}$ plus speech conditions $\mathbf{C}$ for the Score DNN.
- **Score DNN** (generative): performs the diffusion denoising step, producing the final estimate $\hat{\mathbf{S}}$.

### Single-step training and inference

Following EffDiffSE, training uses **matched-condition training at $\tilde{t} = T$** instead of continuous diffusion time. The noise-consistent Langevin dynamics update (with $N$ steps, $\Delta t = T/N$, $\eta = 1 - \gamma^\epsilon$, $\gamma = (\sigma_{\max}/\sigma_{\min})^{-\Delta t}$, $\beta = \sqrt{1 - \gamma^{2(\epsilon-1)}}$) collapses to a **single step**:

$$
\hat{\mathbf{S}} = \mathbf{S}_{T} + \sigma_{T}^{2} \mathbf{S}_{\theta}(\mathbf{S}_{T} | \sigma_{T}, \mathbf{C}), \qquad \mathbf{S}_{T} = \hat{\mathbf{S}}^{\mathrm{cond}} + \sigma_{T} \mathbf{Z}.
$$

Total loss for both networks, with the compressed complex MSE $J^{CC}$ (Braun & Tashev) and hyperparameter $\alpha$:

$$
J = J^{CC}(\hat{\mathbf{S}}^{\mathrm{cond}}, \mathbf{S}) + J^{CC}(\hat{\mathbf{S}}, \mathbf{S}) + \alpha \, J^{\mathrm{SM}}(\mathbf{S}, \sigma_{\tilde{t}}).
$$

Karras et al. **preconditioning** (unit-variance inputs/targets + skip connection) is applied to the Score DNN for training stability, as in Universe++.

### Network architecture

Cond DNN and Score DNN share a U-Net backbone built from strided **DSBlock**/**USBlock** pairs (kernel $k_{\mathrm{T}} \times k_{\mathrm{F}}$, output channels $C_{\mathrm{out}}$, strides $s_{\mathrm{T}} \times s_{\mathrm{F}}$). Key changes vs. EffDiffSE: (1) no strided (transposed) convolution in the first/last U-Net layer; (2) an additional DSBlock/USBlock pair to match down-/upsampling; (3) **sub-pixel convolutions replace transposed convolutions** to alleviate aliasing; (4) early fusion of the far-end reference with the mic signal. Channels $\{11,16,23,33,50\}$ (base) and $\{11,15,21,29,40\}$ (small).

![[raw/papers/lugo-2026-diffvqe/figures/fig1.png|Cond and Score DNN topology]]
*Figure 2: Cond and Score DNN topology (red: Cond-specific, blue: Score-specific), details in Fig. 3.*

![[raw/papers/lugo-2026-diffvqe/figures/fig2.png|Building blocks]]
*Figure 3: Building blocks of the Cond/Score DNNs: DSBlock/USBlock with sub-pixel upsampling.*

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Training data | URGENT 2025 speech + noise corpora (CommonVoice 19.0 excluded), curated via threshold filtering with DNSMOS, SigMOS, UTMOS, NISQA, SQUIM_SDR (Li et al. "Less is More" strategy) |
| Synthetic AEC data | Generation per Seidel et al. 2024 (SER/SNR configs, loudspeaker nonlinearities $f_{\mathrm{NL}}$), with **pyroomacoustics image-source RIRs**; far-end and near-end convolved with **two different RIRs** from matching room configurations |
| Corpus size | 71,777 × 30 s samples ≈ 600 h (URGENT-based) + 8,500 samples ≈ 23 h (ICASSP 2023 AEC Challenge synthetic set) |
| Validation set | TIMIT + ETSI noise + Aachen impulse responses, same-room RIRs for both signals |
| Test set | ICASSP 2023 AEC Challenge blind test set (causal and non-causal delays; **GCC-PHAT** non-causal delay compensation applied) |
| Sampling rate / STFT | 16 kHz; frame 512, hop 128, square-root Hann; bins padded 257 → 260 |
| Diffusion hyperparameters | $T = \tilde{t} = 0.3$, $\sigma_{\min} = 0.01$, $\sigma_{\max} = 5$, $\alpha = 0.005$ |
| Data augmentation | 6.25% of samples remove near-end or far-end speech (explicit STFE/STNE targets); 10% substitute dry for reverberated near-end speech |
| Training | 500k steps, batch 16, 8 s crops, NVIDIA RTX PRO 6000; LR warmup to $8\times10^{-4}$ (7.5k steps), constant to 250k, cosine decay to $1.6\times10^{-6}$ |
| Baseline | DeepVQE retrained on $\mathcal{D}_{\mathrm{train}}$ with original batch size/LR, same epochs for fairness |
| Metrics | AECMOS (DT/ST Echo, DT/ST Other), DNSMOS (OVRL/SIG/BAK), PESQ, ESTOI, LPS (Levenshtein phone similarity, hallucination detection); RTF on single-thread AMD EPYC 9575F @ 3.3 GHz |

## Results

### Validation set (Table 1)

| Method | #Param | FLOPS | RTF | DT Echo | DT Other | DT PESQ | DT LPS | DT ESTOI | STFE Echo | STFE Other | STNE PESQ | STNE LPS | STNE ESTOI | Rank ↓ |
|--------|-------:|------:|----:|--------:|---------:|--------:|-------:|---------:|----------:|-----------:|----------:|---------:|-----------:|-------:|
| Unprocessed | — | — | — | 1.70 | 4.01 | 1.62 | 0.28 | 0.41 | 1.59 | 3.06 | 2.17 | 0.82 | 0.64 | — |
| Clean | — | — | — | 4.58 | 4.21 | 4.64 | 1.00 | 1.00 | 4.68 | 3.98 | 4.64 | 1.00 | 1.00 | — |
| DeepVQE | 5.29M | 42.24G | 0.317 | 4.66 | 3.83 | 2.30 | 0.69 | 0.60 | 4.72 | 3.70 | 2.58 | 0.83 | 0.70 | 2.5 |
| DiffVQE-S | 3.43M | 4.32G | 0.172 | 4.63 | 4.05 | 2.50 | 0.73 | 0.65 | 4.62 | 3.95 | 3.11 | 0.88 | 0.78 | 2.0 |
| **DiffVQE** | 5.13M | 5.37G | 0.185 | 4.65 | **4.10** | **2.63** | **0.75** | **0.68** | 4.60 | **3.97** | **3.14** | **0.88** | **0.79** | **1.3** |

Findings: DeepVQE leads DT/ST Echo (4.66/4.72), but DiffVQE(-S) wins all other metrics. **DiffVQE-S needs only ~10.3% of DeepVQE's FLOPS** (4.32G vs. 42.24G), is smaller and faster (RTF 0.172 vs. 0.317), yet reaches average rank 2.0 vs. DeepVQE's 2.5. DiffVQE secures 8 of 10 best metric values (avg. rank 1.3). Per-SER analysis (Fig. 4): all methods perform similarly and strongly on DT Echo; DiffVQE(-S) leads DeepVQE across the whole SER range in the other five metrics, with DiffVQE consistently slightly ahead of DiffVQE-S in PESQ, ESTOI, and OVRL.

### Blind test set (Table 2)

| Method | DT Echo | DT Other | STFE Echo | STNE Other | STNE SIG | STNE BAK | Rank ↓ |
|--------|--------:|---------:|----------:|-----------:|---------:|---------:|-------:|
| DeepVQE | **4.64** | 3.84 | 4.37 | 3.93 | 3.31 | 4.03 | 2.67 |
| DiffVQE-S | 4.61 | 4.07 | 4.41 | 4.25 | 3.42 | 4.05 | 2.17 |
| **DiffVQE** | 4.62 | **4.10** | **4.43** | **4.26** | **3.43** | **4.07** | **1.17** |

The same pattern generalizes to the blind AEC Challenge 2023 test set — DeepVQE best on DT Echo only (all close), DiffVQE top-ranked on everything else (avg. rank 1.17), confirming that hybrid diffusion AEC is competitive with the discriminative state of the art under an equal training regime.

> **Note on DeepVQE numbers**: The original DeepVQE paper reports 7.5M parameters; the DiffVQE table lists the *retrained* DeepVQE at 5.29M params / 42.24G FLOPS (likely due to the 16 kHz retraining on DiffVQE's data), so parameter counts are not directly comparable with [[sources/indenbom-2023-deepvqe|the original DeepVQE paper]].

## Key Contributions

1. **First fully reproducible diffusion-based AEC system** (DiffVQE): public training data, published network topology, and published training framework (data generation pipeline of Seidel et al. 2024 + diffusion modifications) — unlike the earlier FSD attempt (Liu et al. 2024), which is not reproducible (unstated reference fusion, single-step adaptation without mathematical formulation, private data).
2. **Hybrid single-step diffusion design** adapted from EffDiffSE: discriminative Cond DNN estimate initializes the reverse process at $t = T$, one noise-consistent Langevin correction step from the Score DNN; CCMSE + denoising score matching joint loss; Karras preconditioning.
3. **Topology adaptations**: no strided conv in first/last layers, extra DSBlock/USBlock pair, sub-pixel convolutions replacing transposed convolutions (anti-aliasing), early far-end fusion.
4. **Outperforms DeepVQE** on most AECMOS/DNSMOS quality and PESQ/ESTOI/LPS intelligibility metrics at ~10–13% of the FLOPS, with fewer parameters and lower RTF; DeepVQE retains a marginal echo-suppression (DT/ST Echo) lead.
5. **High-quality training corpus**: URGENT 2025 speech/noise curated with a five-metric threshold strategy (CommonVoice 19.0 excluded), ~623 h total, plus same-room dual-RIR synthetic generation for far- and near-end.

## Related Concepts

- [[concepts/acoustic-echo-cancellation|Acoustic Echo Cancellation (AEC)]]
- [[concepts/diffusion-models-for-speech|Diffusion Models for Speech Enhancement]]
- [[concepts/one-step-generative-models|One-Step Generative Models]]
- [[concepts/urgent-challenge|URGENT Challenge]]
- [[concepts/complex-compressed-mse|Complex Compressed MSE (CCMSE)]]
- [[concepts/sub-pixel-convolution|Sub-Pixel Convolution]]
- [[concepts/speech-enhancement|Speech Enhancement]]

## Related Synthesis

- [[synthesis/multimodal-bc-speech-enhancement|Multimodal Smart Hearables: BC-Aided SE]] — DiffVQE's single-step hybrid diffusion shows generative SE need not be multi-step (NFE 1), refining that synthesis's claim that diffusion models require ~60 reverse steps and are impractical for real-time
