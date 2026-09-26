---
type: source
created: 2026-09-26
updated: 2026-09-26
sources:
  - raw/papers/haeb-umbach-2024-microphone-array-deep-learning/full-text.md
  - https://doi.org/10.1109/MSP.2024.3451653
  - zotero://select/items/0_IMHHP35B
tags:
  - speech-enhancement
  - multi-channel
  - beamforming
  - deep-learning
  - hybrid-processing
  - dereverberation
  - source-separation
---

# Haeb-Umbach, Nakatani, Delcroix, Boeddeker & Ochiai 2024: Microphone Array Signal Processing and Deep Learning for Speech Enhancement

**Authors**: [[entities/reinhold-haeb-umbach|Reinhold Haeb-Umbach]] (Paderborn University, Germany), [[entities/tomohiro-nakatani|Tomohiro Nakatani]], [[entities/marc-delcroix|Marc Delcroix]], [[entities/christoph-boeddeker|Christoph Boeddeker]] (Paderborn University), [[entities/tsubasa-ochiai|Tsubasa Ochiai]] (NTT Corporation, Japan)
**Venue**: IEEE Signal Processing Magazine, November 2024
**Type**: Overview / tutorial article (magazine)
**DOI**: [10.1109/MSP.2024.3451653](https://doi.org/10.1109/MSP.2024.3451653)
**Zotero**: [IMHHP35B](zotero://select/items/0_IMHHP35B)

## Summary

This magazine article contrasts **model-based**, **data-driven**, and **hybrid** approaches to multichannel speech enhancement — noise reduction, source separation, and dereverberation with compact microphone arrays — with the beamforming pipeline as its running example. Its core contribution is a taxonomy of hybrid methods that distinguishes *where* the blending happens: in the **parameter estimation** stage (data-driven estimation of model parameters, or combined model-based + data-driven estimation) or in the **enhancement operation** itself. It closes with a critical discussion of the trend toward purely data-driven ("all-neural") systems, arguing that model-based components act as a kind of "regularizer" that anchors robustness when test data deviate from training statistics.

![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/1d549ad40fbf8cfab8e6eebdc41c2297d55ebd8eed67d4766ddc2000adb9ca9e.jpg|Scenario illustration]]
*Figure 1: The considered scenario — a reverberant enclosure with desired and undesired acoustic sources, captured by a microphone array and processed by a speech enhancement system.*

## Taxonomy

The article organizes enhancement methods along three axes:

1. **Enhancement task**: noise reduction (NR), source separation (SS), dereverberation (DR) — all three formulated on one shared signal model.
2. **Estimation regime** (Fig. 2): every enhancement system consists of **parameter estimation** and the **enhancement operation**. Model-based methods estimate parameters from the very signal to be enhanced (no training phase); data-driven methods estimate them in a separate training stage. Hybrid methods can blend at either stage, or both.
3. **Three classes of hybrid approaches** (Fig. 5):
   - **Class 1 — data-driven estimation of model parameters**: a DNN estimates the parameters (e.g., time-frequency masks) of a model-based enhancement operation (e.g., MVDR beamforming).
   - **Class 2 — combined model-based and data-driven parameter estimation**: both contribute to the estimate (e.g., DNN masks as priors refined by EM, or diarization-guided EM).
   - **Class 3 — joint model-based and data-driven enhancement**: the enhancement operation itself mixes model-based and data-driven modules (e.g., a beamformer sandwiched between two DNNs).

![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/f86a0f0cf61f74a327e0953fed5cb0b4b6943505e1a28abac13c6abc15edd8eb.jpg|Two-operation view of speech enhancement]]
*Figure 2: A speech enhancement system consists of parameter estimation (dashed) and the enhancement operation (solid). Left: parameters estimated from the signal to be enhanced (model-based). Right: parameters estimated in a training stage (data-driven).*

Table I of the paper juxtaposes the three approach classes per task (NR/DR/SS) with their pros and cons:

| | Model-based | Data-driven | Hybrid |
|:--|:--|:--|:--|
| **Examples** | BF with EM-based mask estimation; BSS/ICA; LP / Kalman filter | Spectral mapping and masking by DNN; PIT for SS | BF with DNN(-+EM) mask estimation; DNN-guided SS/LP; DNN-BF-DNN |
| **Pros** | High adaptability, explainability | No model assumptions, high performance | Fewer model assumptions, high performance with high adaptability |
| **Cons** | Restricted by model assumptions | Needs large training data; train-test mismatch sensitivity | Needs large training data; adaptability partly limited by the data-driven part |

## Methodology (Surveyed Methods)

### Signal models of decreasing complexity

The article's common denominator is a ladder of signal models, each a simplification of the full time-domain convolution (Eq. 1): microphone signals = convolution of $K$ sources with acoustic impulse responses (AIRs) + additive noise. In the STFT domain:

- **Convolutive transfer function (CTF)** approximation (Eq. 2): the time-domain convolution becomes a *convolution over the frame index* with a much shorter per-frequency ATF; cross-band filters are neglected. The source spatial image $\mathbf{x}_{k,t,f}$ splits into **early** (direct + early reflections, lags $< \Delta$) and **late** reverberation components — the boundary $\Delta$ defining what dereverberation should remove.
- **Multiplicative transfer function (MTF)/narrowband** approximation (Eq. 5): frame-index convolution collapses to multiplication — valid when the STFT frame length significantly exceeds the AIR length (low reverberation).
- **Anechoic far-field model** (Eq. 6): the ATF vector reduces to complex exponentials of the inter-microphone delays, i.e., a steering vector parameterized only by the directions of arrival (DoAs).

The lesson drawn (quoting George Box): all models are wrong, but some are useful — and decreasing model complexity trades faithfulness for tractability.

### Model-based parameter estimation and enhancement

- **MVDR beamforming** (Eq. 8) with the statistics-only form
  $$\mathbf{w}_f^{\mathrm{MVDR}} = \frac{(\boldsymbol{\Phi}_{\mathbf{n},f})^{-1}\boldsymbol{\Phi}_{\mathbf{x},f}}{\operatorname{tr}\{(\boldsymbol{\Phi}_{\mathbf{n},f})^{-1}\boldsymbol{\Phi}_{\mathbf{x},f}\}}\,\mathbf{u}_1,$$
  where $\boldsymbol{\Phi}_{\mathbf{x},f}$, $\boldsymbol{\Phi}_{\mathbf{n},f}$ are speech and noise spatial covariance matrices (SCMs). The key problem is estimating the SCMs.
- **EM-based mask estimation via a spatial mixture model** (Eqs. 9–13): exploiting sparseness / w-disjoint orthogonality of speech in the STFT domain, a latent one-hot dominance variable $\mathbf{z}_{t,f}$ is introduced; a spatial mixture model $p(\mathbf{y}_{t,f}) = \sum_k \pi_k p(\mathbf{y}_{t,f};\boldsymbol{\theta}_k)$ is fit with EM, and the posterior $m_{k,t,f} = \mathbb{E}[z_{k,t,f} \mid \mathbf{y}_{t,f}]$ serves as a (soft) mask from which the SCMs are computed by mask-weighted outer products.
- **Blind source separation (BSS) / ICA** as the second model-based separation family.
- **Dereverberation**: (i) a state-space view of the CTF model (Eq. 14–17) yielding an EM algorithm whose E-step is a **Kalman filter** (Schwartz, Gannot & Habets 2014); and (ii) **weighted prediction error (WPE)** (Eqs. 18–20), which models late reverberation as an auto-regressive process over past observation frames with prediction lag $\Delta$ (to avoid whitening speech's own AR structure), assuming a zero-mean complex Gaussian early-speech component with time-varying variance $\lambda_{t,f}$.

**Properties emphasized**: no train-test mismatch (parameters estimated from the test utterance itself); adaptation to new acoustic environments within seconds; proven optimality *under the model assumptions*; explainability (e.g., analytic SNR-gain predictions). EM is batch/iterative, but recursive EM formulations allow low-latency processing. Robustness is evidenced by the choice of the spatial-mixture-model mask estimator and WPE for the **CHiME-6 and CHiME-7 challenge baselines** (extremely adverse dinner-party acoustics).

### Data-driven parameter estimation and enhancement

- Evolution of the **spectral target representation**: magnitude-only regression (noisy phase reused) → **complex spectral mapping** (stacking real/imaginary components of the input STFT and regressing the target RI components) → **complex ratio masking**. Time-domain processing replaces the STFT by learned encoder–decoder modules with ~2 ms windows (Conv-TasNet lineage).
- **Spatial features for DNNs**: spatial information manifests as inter-channel phase differences, which real-valued networks initially handled poorly; remedies include explicit IPD features appended to spectral features, and RI stacking across channels — the multichannel input becomes a (time × frequency × channel × RI) tensor.
- **Fullband/subband processing** (Fig. 4): alternating network layers operating along the time axis (per frequency bin, "subband") and along the frequency axis (per frame, "fullband") — the latter particularly effective for spatial information, since a DoA produces a characteristic phase-change pattern along frequency.
- **Permutation invariant training (PIT)**: for denoising, speech/noise masks are distinguishable by their distinct spectral patterns; for speaker separation the per-speaker outputs are permutation-ambiguous, and PIT resolves this by minimizing the training loss over the optimal permutation.
- **Dereverberation by DNN** mirrors denoising (late reverberation is additive in the CTF model); systems up to joint denoising + dereverberation + separation exist.
- **Training data**: supervised training needs *paired* clean/degraded data, rarely recordable in real environments — hence simulation per Eq. (1) with image-source-method AIRs plus data augmentation. Known gaps: simulated AIRs are almost exclusively time-invariant (real AIRs vary with speaker motion); unsupervised alternatives include mixture invariant training (MixIT) and unsupervised domain adaptation. Residual risks: train-test mismatch, out-of-distribution fragility (small input perturbations → surprisingly poor output), black-box behavior, higher compute/memory cost.

![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/2017f06932a70fb7dcca604e2f2eb53ef62089fa46169561172cc4bc0a7e83d8.jpg|LibriCSS observation spectrogram]]
![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/302dad87b4b25b40f97457754214f70bcdcf9c23dc277ba09ac890ef4cbde63b.jpg|Mask of first active speaker]]
![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/6c7ab5e060bb4fba90d452fb7171c7512c3e47f8eebf98a05d94fba619c89846.jpg|Mask of second active speaker]]
![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/7f57f4821993b7081ab95f7fa0846244903e757f0a63df6667f319d4c136736c.jpg|Noise mask]]
*Figure 3: A 4.25 s speech segment from the LibriCSS corpus (two partially overlapping speakers + noise): (1) observation, (2)–(3) per-speaker masks, (4) noise mask, all estimated by a DNN.*

![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/76b00d129cf2811c19db2ec980e2c9562d65a0b2223986148b1b2f7e61cfc76c.jpg|Spectral (fullband) processing within a frame]]
![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/540a26e5622eb0f87ab9494e041c8a62916d996bb429339d22a7f49e0d7c71c9.jpg|Temporal (subband) processing across frames]]
*Figure 4: Spectral (fullband) processing within a frame (left) vs. temporal (subband) processing across frames (right); red arrows mark the sequence axis of each processing layer.*

### Hybrid approaches (the taxonomy's substance)

![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/28985bf2aebb8b0696a4965f29bd45578889af5000ba2b82c78dfdf6c2a0af80.jpg|Three classes of hybrid approaches]]
*Figure 5: Three classes of hybrid approaches (left to right): data-driven parameter estimation for model-based enhancement; combined model-based and data-driven parameter estimation; joint model-based and data-driven enhancement.*

**Class 1 — data-driven estimation of model parameters.** The EM/spatial-mixture-model mask estimator of the model-based pipeline is replaced or supplemented by a DNN trained with (binary) cross-entropy on the dominance labels. Unlike the per-frequency spatial mixture model (which introduces a frequency permutation problem), the DNN sees all frequencies jointly and learns spectro-temporal patterns. For **dynamic acoustic environments**, block-wise time-invariant SCM estimates (Eq. 12) fail when speakers move; the recursive tracker
$$\hat{\boldsymbol{\Phi}}_{\mathbf{x}_k,t,f} = \beta\,\hat{\boldsymbol{\Phi}}_{\mathbf{x}_k,t-1,f} + \hat{\boldsymbol{\Psi}}_{\mathbf{x}_k,t,f}, \qquad 0 < \beta < 1,$$
with instantaneous SCMs $\hat{\boldsymbol{\Psi}}_{\mathbf{x}_k,t,f} = m_{k,t,f}\mathbf{y}_{t,f}\mathbf{y}_{t,f}^{\mathsf{H}}$, generalizes to
$$\hat{\boldsymbol{\Phi}}_{\mathbf{x}_k,t,f} = \sum_{t'} c_{\mathbf{x}_k,t,t'}\,\hat{\boldsymbol{\Psi}}_{\mathbf{x}_k,t',f},$$
which has the form of a (self-)attention mechanism — so attention networks can *learn* the accumulation weights $c$ that a fixed forgetting factor $\beta$ would hard-code (Ochiai et al. 2023).

**Class 2 — combined estimation.** The two mask estimators are complementary (spatial clustering: unsupervised, per-utterance, exploits spatial diversity; DNN: trained, exploits spectro-temporal patterns). Integration patterns surveyed:
- DNN masks as the *a priori* probability of the spatial mixture model, refined by EM as the posterior (Nakatani et al. 2017) — unsupervised adaptation of DNN masks on the test utterance.
- The reverse direction: mixture-model posteriors as *training targets* for the DNN mask estimator — improving separation and enabling single-channel separation learned from multi-channel recordings (Drude et al. 2019; Tzinis et al. 2019).
- **Diarization-guided two-step estimation**: a DNN diarization front-end (up to TS-VAD, which handles overlapped speech) produces time-resolution activities $m_{k,t}$, which constrain the EM refinement to TF resolution:
  $$m_{k,t,f} = \frac{m_{k,t}\,\mathbb{E}[z_{k,t,f}\mid \mathbf{y}_{t,f}]}{\sum_{\tilde{k}} m_{\tilde{k},t}\,\mathbb{E}[z_{\tilde{k},t,f}\mid \mathbf{y}_{t,f}]}$$
  — the formulation of **guided source separation (GSS)**, used by most (including top) CHiME-6/7 systems.
- Neural estimators substituting iterative model-based parameter loops: a DNN estimating the PSD $\lambda_{t,f}$ inside WPE (Kinoshita et al. 2017); neural source models coupled to ICA/IVA/IVE for joint dereverberation and separation (Nakatani et al. 2021; Saijo & Scheibler 2022).

**Class 3 — joint enhancement.** Beamformers exploit spatial information optimally under Gaussian assumptions; DNNs capture spectro-temporal structure without model constraints. The prototypical system combining both is **TF-GridNet**: alternating full-/sub-band layers, self-attention across frames, and a **DNN–BF–DNN** structure in which a (multi-frame Wiener) beamformer is sandwiched between two DNNs — performing joint denoising, dereverberation, and separation.

**End-to-end optimization.** A deficit of hybrids is that the DNN is optimized toward a criterion different from the model-based part. End-to-end training optimizes the whole chain (DNN mask estimator → SCM computation → beamforming → inverse STFT) toward a single time-domain loss, backpropagating through the (differentiable) beamforming operation (Fig. 6, Boeddeker et al. 2021). Training against a *downstream* loss (e.g., ASR) additionally removes the need for paired enhancement data — ordinary transcribed speech suffices. Caveats: training from scratch may fail (carefully designed curricula or fine-tuning of pretrained components are needed), and modularity is lost (a system tuned for one ASR engine may underperform with another).

![[raw/papers/haeb-umbach-2024-microphone-array-deep-learning/figures/8984ed835dbe4f71a34e25ddfd09ac9d0ee63404f0a15f2225d77a180c62bc15.jpg|End-to-end training through the beamformer]]
*Figure 6: End-to-end training — the gradient of a time-domain loss is backpropagated through the inverse STFT, the beamforming operation, and the SCM computation to the DNN mask estimator.*

### The trend toward purely data-driven multichannel enhancement

Using beamforming as the case study, the article traces the progressive replacement of model-based components:

1. DNN mask estimation + model-based MVDR (Class 1 hybrid);
2. **RNN-estimated SCMs** — more reliable under time-varying statistics (ADL-MVDR, Zhang et al. 2021);
3. Direct neural estimation of beamformer coefficients (Xiao et al. 2016 — not successful);
4. **Learnable filterbanks** replacing the STFT, with time-domain beamforming (Gu et al. 2022) — only the beamforming operation remains model-based;
5. **Abandoning beamforming entirely** (Tesch & Gerkmann 2022): nonlinear neural spatial-spectral filters.

The theoretical backdrop for step 5: under *Gaussian* noise, the MVDR output is a **sufficient statistic** for estimating clean speech, $p(s \mid \mathbf{y}) = p(s \mid \hat{x}^{\mathrm{MVDR}})$ (Balan & Rosca 2002) — linear spatial filtering loses no information. But for *non-Gaussian* distortions (e.g., competing speakers), Hendriks et al. (2009) showed the MMSE-optimal estimator is a **nonlinear, jointly spatial-spectral filter** that cannot be decomposed into a cascade of spatial and spectral stages. The optimal nonlinear processor is intractable to implement model-based — and the DNN is the natural surrogate, with architectures like Tesch & Gerkmann's achieving gains over beamforming.

## Applications Survey

| Task | Model-based representative | Data-driven representative | Hybrid representative | Field evidence |
|:-----|:---------------------------|:---------------------------|:----------------------|:---------------|
| Noise reduction (NR) | MVDR with EM masks | Spectral mapping/masking by DNN | DNN-mask MVDR; attention-tracked SCMs | — |
| Source separation (SS) | BSS/ICA; spatial mixture model + BF | PIT-trained separators | **GSS** (diarization-guided EM) | GSS used by most/top CHiME-6/7 systems |
| Dereverberation (DR) | Kalman/EM; WPE | DNN autoencoder mapping (Weninger et al. 2014 and successors) | Neural PSD estimation inside WPE; IVA/IVE with neural source model | WPE + spatial mixture model chosen as CHiME-6/7 baselines |

The "best variant" recommendation is deliberately conditional: purely data-driven methods top single-channel leaderboards and are increasingly competitive multichannel, but cross-paper comparison is difficult because results are reported on different corpora. The article's own verdict favors hybrids where robustness across diverse conditions matters — GSS being the flagship example of a hybrid that boosts performance while *preserving* the model-based part's adaptability to the test data.

## Key Contributions

1. **Two-operation framing** (Fig. 2): every enhancement system = parameter estimation + enhancement operation; the three approach classes differ in how each operation is realized — the cleanest lens the wiki has seen for classifying hybrid systems.
2. **Three-class taxonomy of hybrid approaches** (Fig. 5): data-driven parameter estimation / combined parameter estimation / joint enhancement — each class populated with concrete NR/DR/SS instances (Table I).
3. **Signal-model ladder** (Eqs. 1–7): time-domain → CTF → MTF/narrowband → anechoic far-field, each with its validity conditions, plus the early/late reverberation split at lag $\Delta$.
4. **Unified view of SCM accumulation** (Eqs. 21–23): block averaging, recursive forgetting-factor tracking, and attention-based tracking are the same weighted-accumulation operator with different coefficient choices — connecting classical SCM tracking to self-attention.
5. **GSS formulation** (Eq. 24): diarization-constrained EM mask refinement as the canonical Class-2 hybrid, with CHiME-6/7 field evidence.
6. **Sufficient-statistic argument for the all-neural trend**: MVDR is sufficient under Gaussian noise (Balan & Rosca 2002) but not under non-Gaussian distortions, where the MMSE-optimal filter is a non-decomposable nonlinear joint spatial-spectral operation (Hendriks et al. 2009) — the theoretical justification for replacing beamformers with DNNs.
7. **The "model as regularizer" argument**: a model-based component may be inferior on the datasets a learnt module is optimized for, yet adds robustness by injecting valid physical knowledge, preventing the data-driven component from deviating too far from physically reasonable behavior.

## Limitations and Caveats

- **Not a comprehensive survey**: the article explicitly compares the three approach classes via selected examples rather than exhaustively cataloging the field; many important techniques are omitted for space.
- **No original experiments**: all performance claims are qualitative or borrowed from the cited literature; quantitative cross-class comparisons are confounded by different evaluation corpora ("difficult to compare ... because the reported results had been obtained on different data sets").
- **Speech-focused**: surveyed methods often apply to music or other audio, but the treatment restricts to speech; compact-array, far-field scenarios are assumed (no close-talking, no large/spread arrays).
- **Snapshot predates the newest generation** of all-neural multichannel systems (e.g., large-scale foundation-model-era enhancement), so the "trend" analysis is a 2024-literature snapshot.
- The authors' own reservations about the data-driven trend (representativeness of training data; ever-larger networks demanding ever-more data) are argued qualitatively, not empirically substantiated within the article.

## Related Concepts

- [[concepts/hybrid-speech-enhancement|Hybrid Speech Enhancement]] — the three-class taxonomy this article introduces
- [[concepts/guided-source-separation|Guided Source Separation (GSS)]]
- [[concepts/weighted-prediction-error|Weighted Prediction Error (WPE)]]
- [[concepts/tf-gridnet|TF-GridNet]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/tf-mask-estimation|TF Mask Estimation]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/adl-mvdr|ADL-MVDR]]
- [[concepts/complex-spectral-mapping|Complex Spectral Mapping]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training (PIT)]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/target-speaker-vad|Target-Speaker Voice Activity Detection (TS-VAD)]]
- [[concepts/deep-learning-for-signal-processing|Deep Learning for Signal Processing]]

## Related Synthesis

- [[synthesis/deep-speech-enhancement|Deep Speech Enhancement]]
- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Sources

- [[sources/zhang-2021-adl-mvdr|Zhang et al. 2021: ADL-MVDR]] — the RNN-SCM step in the all-neural progression (Section IV-E)
- [[sources/tesch-2023-insights-deep-nonlinear-filters|Tesch & Gerkmann 2023: Insights into Deep Nonlinear Filters]] — the "abandon beamforming" endpoint of the progression
- [[sources/wang-2018-supervised-speech-separation-deep-learning-overview|Wang & Chen 2018: Supervised Speech Separation Based on Deep Learning]] — the data-driven survey the article builds on
- [[sources/sawada-2019-bss-ilrma-review|Sawada et al. 2019: BSS Review (ICA and NMF routes to ILRMA)]] — the model-based BSS family
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova, Delcroix & Ochiai 2023: Neural Target Speech Extraction: An Overview]] — companion SPM overview sharing three of this article's authors
- [[sources/richard-2023-audio-signal-processing-21st-century|Richard et al. 2023: Audio Signal Processing in the 21st Century]] — the 25-year retrospective whose "model-based + data-driven hybrids" prediction this article elaborates
- [[sources/pan-2020-microphone-array-beamforming|Pan, Huang & Chen 2020: Microphone Array Beamforming Methods]] — beamforming-family review complementing this article's enhancement-task perspective
