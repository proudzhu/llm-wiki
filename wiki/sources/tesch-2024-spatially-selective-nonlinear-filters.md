---
type: source
created: 2026-08-22
updated: 2026-08-22
sources:
  - raw/papers/tesch-2024-spatially-selective-nonlinear-filters/full-text.md
  - https://doi.org/10.1109/TASLP.2023.3334101
  - zotero://select/items/0_LFX897WM
tags:
  - speech-separation
  - multi-channel
  - spatial-filtering
  - deep-learning
  - microphone-arrays
  - direction-of-arrival
  - target-speaker-extraction
  - nonlinear-filtering
---

# Tesch & Gerkmann 2024: Multi-channel Speech Separation Using Spatially Selective Deep Non-linear Filters

**Authors**: [[entities/kristina-tesch|Kristina Tesch]] (Student Member, IEEE), [[entities/timo-gerkmann|Timo Gerkmann]] (Senior Member, IEEE)
**Affiliation**: Signal Processing Group, Universität Hamburg, Germany
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 32, 2024
**Type**: Journal Article
**DOI**: [10.1109/TASLP.2023.3334101](https://doi.org/10.1109/TASLP.2023.3334101)
**Zotero**: [LFX897WM](zotero://select/items/0_LFX897WM)
**Predecessor**: Tesch & Gerkmann, ICASSP 2023 — "Spatially selective deep non-linear filters for speaker extraction" [26]

## Summary

This paper extends the authors' ICASSP 2023 conference paper [26] and investigates the use of a steerable [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Filter (SSF)]] for multi-channel speech separation: the SSF is repeatedly steered to each speaker's direction-of-arrival (DOA) to recover individual sources from a reverberant mixture. The paper conducts a systematic comparison with a [[concepts/direct-separation|direct separation (DS)]] approach trained with utterance-wise permutation invariant training (PIT) using the same underlying network architectures — the [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filter (JNF)]] [22], [27] and [[concepts/mcnet|McNet]] [34] — and shows that the SSF increasingly outperforms DS as the number of speakers grows, generalizes much better to unseen noise conditions, and decouples per-speaker outputs. It also proposes two blind DoA-estimation strategies (search-based and [[concepts/dnn-based-doa-classifier|DNN-based]]) that match oracle-DoA performance, and studies robustness to DoA errors and microphone-array perturbations.

## Problem Formulation

The paper considers a reverberant multi-channel speech separation scenario with $P$ concurrently speaking persons recorded by an omni-directional microphone array with $C$ channels. The dry speech of speaker $p$, $s_p(t)$, is convolved with a room impulse response (RIR) $h_p^\ell(t)$ to produce the recording at microphone $\ell$:

$$x_p^\ell(t) = s_p(t) * h_p^\ell(t).$$

After STFT, the additive signal model is:

$$Y^\ell(k, i) = \sum_{p=1}^{P} X_p^\ell(k, i) + V^\ell(k, i),$$

where $V^\ell(k, i)$ is sensor/environmental noise. The task is to recover the direct-path dry speech signals $S_p(k, i)$ for each speaker; the propagation delay of the direct path is excluded from the target so that metrics requiring a reference can be computed.

## Methodology

### SSF Principle

The SSF separates localization from extraction: it is given the target speaker's DOA $\varphi_t$ as a steering cue and learns to focus on a single speaker. Per-speaker recovery is obtained by running the same network $P$ times with different target angles. Unlike DS approaches trained with PIT, the SSF does not suffer from a permutation problem because each output is identified by its steering direction.

### Network Architectures

Two joint spatial and tempo-spectral non-linear filter architectures are used:

- **JNF** ([22], [27]) — two stacked LSTM layers: an **F-LSTM** that processes frequency bins independently (sharing weights across time frames) to extract spatial/spectral features, and a **T-LSTM** that processes time independently per frequency bin. Outputs a complex-valued mask $\mathcal{M}_p(k, i) \in [-1, 1]$ which is expanded following [33] and applied to the reference microphone: $\hat{S}_p(k, i) = Y^0(k, i) \cdot \mathcal{M}_p(k, i)$.
- **McNet** ([34]) — extends JNF with two additional single-channel LSTM layers and skip connections (noisy multi-channel signal concatenated to T-LSTM input; noisy reference-channel magnitude concatenated to the two SC-LSTMs), plus feed-forward layers after every LSTM. The same steering mechanism applies because the conditioning targets the first F-LSTM, which is identical in both architectures.

### Proposed Steering Mechanism (Conditioning on Target DOA)

![[raw/papers/tesch-2024-spatially-selective-nonlinear-filters/figures/c796eba64f9fe12320c593b14ed6b21586fccb4f5c426d9f89abf71ace85cde4.jpg|JNF architecture and steering mechanism]]
(a) JNF [22], [27] architecture (left) with steering mechanism (right).

![[raw/papers/tesch-2024-spatially-selective-nonlinear-filters/figures/78c590d2d645277b36a228fae2cf2e48f29f1b296afc27ea5f053d8cd02ebc19.jpg|McNet architecture and steering mechanism]]
(b) McNet [34] architecture (left) with steering mechanism (right).

*Figure 1: Schematic view of a spatially selective filter (SSF) based on the JNF (top) and McNet (bottom) network architectures. The proposed conditioning on the target DOA is depicted on the right side.*

The DOA is encoded as a **one-hot vector** with $2^\circ$ resolution (180 candidates for $360^\circ$), passed through a linear layer that produces an embedding matching the F-LSTM cell-state size (256 units for JNF). The embedding initializes the **forward and backward cell states of the bidirectional F-LSTM**. This design choice avoids a far-field steering-vector assumption (unlike Jenrungrot et al. [30]) and was shown in [26] to outperform time-aligned input shifting. Preliminary experiments showed that conditioning only the first F-LSTM is better than conditioning the T-LSTM or both layers, consistent with [22]'s observation that spatial selectivity is primarily controlled by the F-LSTM.

### Baselines and Variants

- **DS** (Direct Separation) — same network, no DoA conditioning, output dimension scaled to predict $P$ masks, trained with utterance-wise PIT [39].
- **iDS** (DoA-informed DS) — DS extended with DoA information for all speakers via multi-hot encoding using the same conditioning mechanism.
- **MVDR + PF** — oracle MVDR beamformer (RTF from principal eigenvector of generalized eigenvalue problem, time-varying noise covariance by recursive averaging) + single-channel DNN post-filter (two LSTM layers trained on MVDR outputs).
- **McNet-SSF (HCF)** — McNet-SSF with hand-crafted input features instead of raw STFT (real/imag of reference, IPDs, location-guided angle feature [24], [25]).

### Loss Function

All networks trained with an $\ell_1$ loss in time and frequency domain [47]:

$$L(s_p, \hat{s}_p) = \alpha \| s_p - \hat{s}_p \|_1 + \big\| |S_p| - |\hat{S}_p| \big\|_1,$$

with $\alpha = 10$ to balance the two domains. The DS/iDS variants use this loss inside a PIT scheme.

### Blind DoA Estimation Strategies

- **[[concepts/search-based-doa-estimation|Search-based]]** — evaluates the SSF on a candidate-direction grid (4° resolution), computes energy of filtered outputs on 10 ms non-overlapping segments where speech is active (−45 dB detection threshold), then runs a `scipy.signal.find_peaks`-based peak-finding heuristic (Appendix B) to localize speakers. Computationally expensive but reveals the spatial selectivity of the filter.
- **[[concepts/dnn-based-doa-classifier|DNN-based classifier]]** — a separate F-LSTM + two feed-forward layers (256 and 180 hidden units, ELU and sigmoid activations) trained for 100 epochs with binary cross-entropy on two-speaker mixtures to detect (for every 2° bin) whether a speaker is present. Generalizes to other speaker counts without retraining; uses the same peak-finding heuristic on its output.

## Experimental Setup

| Aspect | Configuration |
|:-------|:--------------|
| **Rooms** | Rectangular, dimensions and $T_{60}$ uniformly sampled (W 2.5–5 m, L 3–9 m, H 2.2–3.5 m, $T_{60}$ 0.2–0.5 s); image-source method via `pyroomacoustics` [36], [37] |
| **Microphone array** | Circular, 3 omni-directional mics, 10 cm diameter, random rotation $\varphi_m \in [0, 2\pi)$, fixed height 1.5 m, ≥1.2 m from walls |
| **Speakers** | Target + 5 interfering during training; min 0.8 m / max 1.2 m from array; 10° angular exclusion zone around target; one interfering speaker per equally-spaced gray-segment; speaker height $\sim \mathcal{N}(1.6, 0.08^2)$ m |
| **Training data** | 54 000 examples (180 target directions × 300 examples), 2° angular resolution |
| **Validation/Test** | 2 700 / 1 800 examples |
| **Speech corpus** | WSJ0 [38] (no train/val/test overlap), 16 kHz |
| **Acoustic conditions** | DRR avg 0.8 dB, 95% in [−5.9, 4.8] dB; SNR per task: 2 spk [−9.4, 9.4] dB, 3 spk [−11.8, 4.9] dB, 5 spk [−14.5, 0.5] dB |
| **STFT** | 32 ms windows, 50% overlap, sqrt-Hann analysis + synthesis |
| **Optimizer** | Adam [48], initial lr 0.001, ×0.75 every 50 epochs, 500 epochs max, best weights by validation loss |
| **Metrics** | ΔPOLQA [40], ΔSI-SDR [41], DNSMOS (P.835 overall quality) [42] |

![[raw/papers/tesch-2024-spatially-selective-nonlinear-filters/figures/c570b14c5199c2387a5c6339546b6b22a561f4df1516b021c7c35416870fcbb9.jpg|Dataset generation geometry]]
*Figure 2: Illustration of the dataset generation. The target source is marked with a red cross and its DoA angle $\varphi_t$ is computed relative to the microphone orientation $\varphi_m$. Interfering sources are placed in the gray area.*

## Results

### Speech Separation Performance (Table II)

| No. | Method | DoA | 2 spk ΔPOLQA | 2 spk ΔSI-SDR | 2 spk DNSMOS | 3 spk ΔPOLQA | 3 spk ΔSI-SDR | 3 spk DNSMOS | 5 spk ΔPOLQA | 5 spk ΔSI-SDR | 5 spk DNSMOS |
|:----|:-------|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|
| 1 | JNF-DS | – | 1.20 | 11.7 | 2.80 | 0.87 | 11.5 | 2.46 | 0.53 | 10.7 | 2.11 |
| 2 | JNF-SSF | oracle | 1.41 | 12.7 | 2.94 | 1.30 | 14.2 | 2.79 | 0.96 | 15.1 | 2.52 |
| 3 | JNF-SSF | search | 1.40 | 12.6 | 2.94 | 1.29 | 13.9 | 2.78 | 0.93 | 14.4 | 2.51 |
| 4 | McNet-DS | – | 1.82 | 15.0 | 3.03 | 1.40 | 15.4 | 2.79 | 0.87 | 14.2 | 2.39 |
| 5 | McNet-iDS | oracle | 1.82 | 15.7 | 3.07 | 1.61 | 15.9 | 2.85 | 0.96 | 15.0 | 2.43 |
| 6 | McNet-SSF | oracle | 1.85 | 14.7 | 3.13 | 1.76 | 16.3 | 3.04 | 1.43 | 17.3 | 2.84 |
| 7 | McNet-SSF | search | 1.91 | 15.0 | 3.15 | 1.80 | 16.3 | 3.06 | 1.43 | 16.6 | 2.85 |
| 8 | McNet-SSF | DNN | 1.85 | 14.7 | 3.13 | 1.76 | 16.2 | 3.04 | 1.42 | 16.9 | 2.84 |
| 9 | MVDR + PF | oracle | 0.42 | 3.8 | 2.47 | 0.23 | 2.8 | 2.20 | 0.14 | 3.1 | 1.90 |
| 10 | McNet-SSF (HCF) | oracle | 1.49 | 11.6 | 2.90 | 1.38 | 12.6 | 2.78 | 1.03 | 12.4 | 2.53 |

**Key takeaways:**

- The SSF advantage grows with the number of speakers: for JNF, the ΔPOLQA gap over DS widens from 0.21 (2 spk) to 0.43 (3 and 5 spk); for McNet, from 0.03 (2 spk) to 0.56 (5 spk).
- Both blind DoA strategies (search-based and DNN classifier) match oracle-DoA performance — for McNet-SSF the search-based results are even slightly *better* than oracle, because slight uncorrelated DoA deviations correlate with the filter's spatial response (Sec. VI-A).
- The MVDR + PF baseline collapses on 5-speaker mixtures (ΔPOLQA 0.14, DNSMOS 1.90), confirming the limitation of linear spatial filters in dense reverberant conditions.
- Hand-crafted features (row 10) underperform the proposed raw-STFT + one-hot conditioning by ≈0.4 ΔPOLQA across all speaker counts.

**Parameter-controlled comparison (Table III):** scaling JNF-DS LSTM units to match the per-speaker parameter count of JNF-SSF (2.4 / 3.6 / 6.0 M params for 2/3/5 speakers vs. $1.2 \times P$ M) does not close the gap — JNF-SSF still wins by 0.17–0.36 ΔPOLQA.

![[raw/papers/tesch-2024-spatially-selective-nonlinear-filters/figures/293db75a2343419c652fd55af89c5e64616c26f2974aad0b0a2f1a282bdd979e.jpg|Listening experiment preference results]]
*Figure 3: Listening experiment (10 subjects, 8 examples × 4 comparisons, blind) preference between SSF and DS results — more than 55% of SSF examples preferred vs. ≈10% for DS.*

### Localization Accuracy (Table IV)

Mean angular error with 95% confidence interval:

| DoA estimation | 2 spk | 3 spk | 5 spk |
|:---------------|:------|:------|:------|
| search (JNF-SSF) | 1.57 ± 0.12° | 2.06 ± 0.19° | 3.54 ± 0.25° |
| search (McNet-SSF) | 2.07 ± 0.07° | 2.53 ± 0.15° | 3.99 ± 0.23° |
| DNN classifier | **1.06 ± 0.03°** | **1.24 ± 0.09°** | **2.13 ± 0.19°** |

The DNN classifier is both more efficient (one forward pass vs. 180 SSF evaluations) and more accurate (up to 1.86° lower mean error for 5 speakers). The JNF-SSF yields tighter search-based localization than McNet-SSF, attributable to JNF's stronger spatial selectivity (cf. Figure 4 peak widths).

![[raw/papers/tesch-2024-spatially-selective-nonlinear-filters/figures/16c1e15b5d8071d21738a432b90c2ca585e0dcae147dd6651ac5e3c4668310ec.jpg|Search-based localization example — 2 speakers]]
![[raw/papers/tesch-2024-spatially-selective-nonlinear-filters/figures/638f0eb0039eef6396b1bbb640e1ad507bacef53d93f62c87a97318336eac7f4.jpg|Search-based localization example — 3 speakers]]
*Figure 4: Examples for blind speaker separation and localization by peak-searching for a mixture of two, three and five speakers using non-linear filters steered in all candidate directions. Vertical dashed gray lines mark true speaker positions; green crosses mark the energy-peak-based estimates. Bottom-row POLQA scores per candidate direction illustrate the spatial selectivity of the SSF.*

### Robustness Experiments (Sec. VI)

**DoA estimation errors (Fig. 5):** For a McNet-SSF trained on exact DoAs, a 2° error costs ≈3–7% POLQA — surprisingly the harder 5-speaker case is least affected (wider peaks in Fig. 4 absorb the error). Training with up to 4° DoA noise flattens the sensitivity curve for ≤4° errors but slightly reduces peak performance — there is a tunable sensitivity/robustness trade-off.

**Microphone placement perturbations (Fig. 6):** Adding zero-mean Gaussian noise (σ = 0.1–1 cm) to each mic coordinate: SSF tolerates 1 mm perturbations without significant loss but degrades sharply beyond; DS is largely insensitive but performs far below the SSF's peak. The authors interpret DS's flatness as evidence that DS under-exploits spatial information rather than being genuinely robust — DS underperforms even with perturbed SSF for 3+ speakers.

### Generalization Experiments (Sec. VII)

- **Far-field vs near-field (Fig. 7):** A McNet-SSF trained at 0.8–1.2 m source distance degrades outside that range; re-training with near-field data (0.3–1.0 m, as in [26]) markedly improves close-source performance but reduces far-source performance — the network spends capacity modeling near-field spatial structure.
- **Sources with similar DoA (Fig. 8):** With two speakers within ±20° of each other and a third at 60°, neither SSF nor DS separates the collocated pair well. But the SSF still cleanly extracts the third speaker (avg. ΔPOLQA improves by ≈0.5), while the DS approach's per-speaker outputs are all of low quality — the SSF decouples failure across speakers; the DS approach couples them. iDS does not achieve this decoupling, showing that providing DoA info to a PIT-trained network is insufficient.
- **Unseen music-noise source (Table V):** Adding an unseen music source (5 dB SNR, MUSAN jamendo) to a 2-speaker mixture: McNet-SSF (oracle DoA) degrades by ≈10% POLQA but reliably excludes the music; McNet-DS trained on 2-speaker mixtures fails badly (ΔPOLQA 0.65, DNSMOS 2.28); McNet-iDS improves with oracle DoAs but still trails SSF by 0.82 ΔPOLQA. Training DS on 3-speaker mixtures recovers much of the lost performance but still trails McNet-SSF by 0.15 ΔPOLQA / 0.4 dB SI-SDR / 0.18 DNSMOS — while requiring DoA estimation for the noise source, which is impractical.

## Key Contributions

1. **Systematic SSF vs DS comparison under matched architectures**: Uses JNF and McNet as shared backbones to isolate the effect of explicit (SSF, DoA-steered) vs. implicit (DS, PIT-trained) spatial filtering. The SSF's advantage scales with the number of speakers and is not explained by per-speaker parameter count (Table III).
2. **One-hot DoA conditioning via F-LSTM cell-state initialization**: Encodes the target direction as a $2^\circ$-resolution one-hot vector projected through a linear layer to initialize the bidirectional F-LSTM cell state — avoids far-field assumptions and outperforms time-aligned-input steering [30] and hand-crafted input features [24], [25].
3. **Two blind DoA-estimation strategies making the SSF practical**: (i) a search-based strategy that exploits the SSF's spatial selectivity by peak-finding on filtered-signal energy, and (ii) a compact DNN-based classifier (F-LSTM + 2 FF layers) that is both more efficient and more accurate than search-based localization. Both match oracle-DoA separation performance.
4. **Empirical evidence that explicit spatial filtering exploits spatial information better**: The DS approach's flat robustness to microphone perturbations is re-interpreted as under-exploitation of spatial cues rather than robustness — DS performs below the perturbed SSF peak for 3+ speakers.
5. **Per-speaker output decoupling and superior unseen-noise generalization**: SSF decouples failure modes across speakers (close-DoA experiment) and generalizes far better to unseen music-noise sources than DS, including DoA-informed DS.
6. **Tutorial-style robustness characterization**: DoA-error sensitivity is trainable (up to 4° training noise flattens the response); far-field/near-field trade-offs are tunable via training-data distance range; array-geometry perturbations above 1 mm are not tolerated without explicit geometry conditioning (cf. [[concepts/geometry-conditioned-ssf|GC-SSF]]).

## Related Concepts

- [[concepts/spatially-selective-nonlinear-filter|Spatially Selective Non-Linear Filter (SSF)]]
- [[concepts/joint-nonlinear-filtering|Joint Nonlinear Filtering (JNF / FT-JNF)]]
- [[concepts/mcnet|McNet (Multi-Cue Network)]]
- [[concepts/direct-separation|Direct Separation (DS) with PIT]]
- [[concepts/doa-informed-direct-separation|DoA-Informed Direct Separation (iDS)]]
- [[concepts/search-based-doa-estimation|Search-based DoA Estimation]]
- [[concepts/dnn-based-doa-classifier|DNN-based DoA Classifier]]
- [[concepts/beamforming|Beamforming]] (MVDR baseline, Delay-and-Sum)
- [[concepts/target-speaker-extraction|Target Speaker Extraction]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/geometry-conditioned-ssf|Geometry-Conditioned SSF (GC-SSF)]]
- Complex Ratio Masking [33] (Williamson & Wang 2016)

## Related Sources

- [[sources/li-2026-geometry-conditioned-ssanc|Li 2026: Geometry-Conditioned Spatially Selective Non-Linear Filter]] — extends SSF with FiLM-based geometry conditioning for cross-array generalization
- [[sources/huang-2026-ndf-joint-neural-directional-filtering|Huang 2026: NDF+]] — extends the FT-JNF framework with dual coherent/diffuse masks for VDM reconstruction
- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova 2023: Neural Target Speech Extraction Overview]] — surveys TSE including DOA-based spatial-clue variants
- [[sources/zaidel-2026-linearly-constrained-deep-beamformer|Zaidel 2026: Linearly Constrained Deep Beamformer]] — alternative DNN spatial filter with explicit linear constraints
