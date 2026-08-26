---
type: source
created: 2026-08-26
updated: 2026-08-26
sources:
  - raw/papers/kang-2019-low-complexity-permutation-alignment/full-text.md
  - https://doi.org/10.1016/j.specom.2019.11.002
  - zotero://select/items/0_IH67EZK3
tags:
  - blind-source-separation
  - audio-source-separation
  - permutation-alignment
  - computational-efficiency
  - signal-processing
---

# Kang, Yang & Yang 2019: A Low-Complexity Permutation Alignment Method for Frequency-Domain BSS

- **Authors**: [[entities/fang-kang|Fang Kang]], [[entities/feiran-yang|Feiran Yang]] (corresponding), [[entities/jun-yang|Jun Yang]]
- **Institution**: Key Laboratory of Noise and Vibration Research / State Key Laboratory of Acoustics, Institute of Acoustics, Chinese Academy of Sciences; University of Chinese Academy of Sciences, Beijing
- **Venue**: Speech Communication, Vol. 112, 2019
- **Type**: Journal article
- **DOI**: [10.1016/j.specom.2019.11.002](https://doi.org/10.1016/j.specom.2019.11.002)
- **Zotero**: [IH67EZK3](zotero://select/items/0_IH67EZK3)

## Summary

Frequency-domain [[concepts/blind-source-separation|blind source separation]] applies ICA independently in each frequency bin, which leaves the source ordering in each bin arbitrary — the well-known **permutation problem**. This paper proposes a low-complexity three-stage permutation alignment method based on the inter-frequency dependence of signal power ratios: (1) bin-wise alignment that only fixes permutations with high correlation confidence, (2) resolution of low-confidence bins against a local centroid computed from high-confidence bins, and (3) a fine global one-centroid clustering that converges in only a few iterations because the first two stages provide an excellent initialization. The method matches the separation quality of the state-of-the-art Sawada and MBMC alignment schemes while cutting runtime dramatically (10.3 s vs. 42.3 s / 54.2 s in a 4-source setup).

## Problem Formulation

A convolutive mixture at the $j$th sensor is

$$x_j(t) = \sum_{i=1}^{N} \sum_{p=0}^{P-1} h_{ji}(p)\, s_i(t-p)$$

which, after an $L$-point STFT, becomes an instantaneous mixture per frequency bin:

$$\mathbf{x}(l, f) = \mathbf{H}(f)\, \mathbf{s}(l, f), \qquad \mathbf{y}(l, f) = \mathbf{W}(f)\, \mathbf{x}(l, f)$$

Ideally $\mathbf{W}(f)\mathbf{H}(f) = \mathbf{I}$, but the ICA solution is only defined up to scaling and permutation, requiring $\mathbf{y}(l,f) \leftarrow \boldsymbol{\Lambda}(f)\, \mathbf{P}(f)\, \mathbf{y}(l,f)$. The scaling ambiguity is resolved by the minimal distortion principle (MDP), $\boldsymbol{\Lambda}(f) = \operatorname{diag}(\mathbf{W}^{-1}(f))$; the hard part — and the subject of the paper — is the per-bin permutation matrix $\mathbf{P}(f)$, since each bin's ICA is blind to the source ordering used by its neighbors. This is the price paid for per-bin ICA instead of permutation-free approaches like [[concepts/independent-vector-analysis|IVA]] or [[concepts/independent-low-rank-matrix-analysis|ILRMA]].

## Methodology

### Inter-frequency dependence measure (Sawada et al. 2007)

With $\mathbf{A}(f) = \mathbf{W}^{-1}(f) = [\mathbf{a}_1, \ldots, \mathbf{a}_N]$, the **power ratio** of the $i$th separated signal in the mixture is

$$v_i(l, f) = \frac{\|\mathbf{a}_i(f)\, Y_i(l, f)\|^2}{\sum_{k=1}^{N} \|\mathbf{a}_k(f)\, Y_k(l, f)\|^2} \in [0, 1]$$

and the correlation coefficient $\rho(\mathbf{v}_i(f_1), \mathbf{v}_j(f_2))$ between two power-ratio sequences (zero-mean, unit-variance normalized) measures inter-frequency dependence: $\rho$ is high when both sequences belong to the same source, especially for neighboring bins.

### Three-stage alignment

**Stage 1 — confidence-thresholded bin-wise alignment.** Sweep bins from $f_2$ to $f_{L/2+1}$, choosing each bin's permutation to maximize the summed adjacent-bin correlation:

$$\Pi_f \leftarrow \arg\max_{\Pi} \sum_{k=1}^{N} \rho(\mathbf{v}_i(f), \mathbf{v}_{i'}(f-1)) \big|_{i = \Pi_f(k),\, i' = \Pi_{f-1}(k)}$$

Crucially, the permutation is **only fixed** when the average correlation $\rho_f \geq U_{th}$; low-confidence bins are left undetermined rather than committed to a possibly wrong neighbor-based guess.

**Stage 2 — local centroid correction.** For each undetermined bin, compute a local centroid from the set of already fixed high-confidence bins $F_l$,

$$\mathbf{m}_k = \frac{1}{N_l} \sum_{f \in F_l} \mathbf{v}_i(f) \big|_{i = \Pi_f(k)}$$

and choose the permutation maximizing $\sum_k \rho(\mathbf{v}_i(f), \mathbf{m}_k)$. This prevents a single unreliable adjacent-bin correlation from propagating misalignment to all subsequent bins (the failure mode of the region-growing approach).

**Stage 3 — fine global optimization.** One-centroid clustering over the fullband: the centroid $\mathbf{C}_k$ acts as a global time-activity reference, and permutations are re-optimized by maximizing $\sum_k \rho(\mathbf{v}_i(f), \mathbf{C}_k)$ for all $f$, iterating until convergence. Because stages 1–2 already leave most bins correctly aligned, this converges in fewer than 5 iterations — versus ~15 for Sawada's and MBMC's global steps, which start from a poor initialization.

### Computational complexity

Counting real multiplications (complex ×4, division ×20, square-root ×40) with STFT length $L$, $B$ frames, $N$ sources, and $N_p$ ICA iterations:

| Step | Cost |
|------|------|
| STFT | $C_1 = 4(L/2)NB\log_2 L$ |
| ICA | $C_2 = 4L N_p N^2 B$ |
| Power ratio | $C_3 = (L/2)NB(8N + 28)$ |
| Permutation | $C_4 = (L/2)N!N(3B + 108)$ |

The proposed method costs $C_1 + C_2 + C_3 + (1 + \theta + N_q)C_4 + BN(N_q + L/2)$, where $\theta$ is the fraction of undetermined bins after stage 1 and $N_q$ the global-clustering iterations (≈5). The advantage over Sawada ($N_r \approx 15$) and MBMC ($N_o \approx 15$, plus multi-centroid and subband clustering terms) grows with the number of sources.

![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/570c9cceba5ad1f3ce02db6dcc425dbf78e09bb215639d322bcf061b33f2c750.jpg|Computational complexity comparison of the three permutation alignment algorithms as a function of the number of sources]]
*Figure 1: Computational complexity comparison. The proposed method has the lowest cost, with the gap widening as the number of sources increases.*

## Experimental Setup

| Item | Value |
|------|-------|
| Room | $7 \times 5 \times 2.75$ m, sources/mics at 1.5 m height (Fig. 2) |
| Data | 180 test files, 10 s each, 450 TIMIT sentences, $f_s = 8$ kHz |
| Mixtures | $2\times2$, $3\times3$, $4\times4$; input SIR 0 / −3 / −5 dB |
| Reverberation | $\mathrm{RT}_{60} = 100$–700 ms |
| STFT | Hanning, 75% overlap; $L = 2048$ ($\mathrm{RT}_{60} \leq 300$ ms), $L = 4096$ (500, 700 ms) |
| ICA | Same complex-valued instantaneous ICA for all alignment methods |
| Metrics | $\mathrm{SIR}_{\mathrm{out}}$, PESQ |
| Baselines | RG (Wang 2011), Sawada (2007), MBMC (Wang 2014), ILRMA (Kitamura 2016) |

![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/cde0dc9b3faa5ef36557b66a79dd280848ab57ac707d141f0ce573e00c737d53.jpg|Simulated room environment with source and microphone positions]]
*Figure 2: Simulated room environment (7 × 5 × 2.75 m) with numbered source positions and microphone array.*

### Execution time (Matlab, i7-7700HQ, $\mathrm{RT}_{60}=100$ ms, $N=4$, 10 s @ 8 kHz)

| Method | ICA | RG | Sawada | MBMC | Proposed | ILRMA |
|--------|-----|-----|--------|------|----------|-------|
| Total runtime | 3.0 s | 6.1 s | 42.3 s | 54.2 s | **10.3 s** | 29.8 s |
| Permutation stage only | — | 3.1 s | 39.3 s | 51.2 s | **7.3 s** | — |

The permutation stage alone can cost an order of magnitude more than the ICA itself, so alignment efficiency matters as much as ICA efficiency.

## Results

### Permutation alignment quality ($\mathrm{RT}_{60} = 200$ ms, sources 1, 2, 5)

The four-panel visualization below traces the source index assigned to each separated signal across frequency. After raw ICA (a) the assignment is essentially random; stage 1 fixes most bins but leaves visible misaligned bands; stage 2 repairs the low-confidence bins using the local centroid; stage 3 only fine-tunes — confirming that the local stages already provide a near-converged initialization.

![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/a99267c3576c35d635f09839767aa76c90e2a92e9ab994c47f7f281e056bc595.jpg|Permutation result after ICA separation]]
![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/d10e371ba4f79603b5ee12be525f3e493ea5f8be6d2fbedae898180dfd9a2c95.jpg|Permutation result after the first step]]
![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/3c19c3fb9f951400092a3b7c1c3cb87ea04554ee6a2ecaea6f5779112f8cc48a.jpg|Permutation result after the second step]]
![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/3b253960b3ae0696a434024b19cab167be536b31388ce572241952f02f6660fa.jpg|Permutation result after the third step]]
*Figure 3: Permutation result of the proposed algorithm — (a) after ICA separation, (b) after stage 1 (bin-wise alignment), (c) after stage 2 (local centroid correction), (d) after stage 3 (global optimization).*

Comparing final results across methods, RG retains severe ambiguity in many bins, while Sawada and MBMC reach the same near-perfect alignment as the proposed method.

![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/24b5020880e13b5294de0c2699025fb8d1337221e40ebcc90bc70dfa21982b0a.jpg|Final permutation result of the RG method]]
![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/4528ee21e9a7aa66924b97edb79e27023fb762e8c93cda797f89a152c74a5c95.jpg|Final permutation result of Sawada's method]]
![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/b55f91eecfc9d88741ac621f0665df87c4b8ecb53397f4a6989f0df6dd0d1cba.jpg|Final permutation result of the MBMC method]]
*Figure 4: Final permutation results of the three existing methods — (a) RG, (b) Sawada's, (c) MBMC.*

### Separation performance ($\mathrm{RT}_{60} = 100$ ms, averaged over 20 file combinations)

Average $\mathrm{SIR}_{\mathrm{out}}$ (dB) — a subset of source-location cases:

| Source locations | 1, 10 | 2, 7 | 9, 10 | 5, 6 | 1, 2, 5 | 4, 6, 8 | 1, 2, 7, 9 | 2, 3, 5, 7 |
|------------------|-------|------|-------|------|---------|---------|-------------|-------------|
| ILRMA | 24.8 | 29.2 | 10.8 | 12.1 | 15.6 | 14.4 | 8.5 | 15.5 |
| RG | 21.4 | 23.8 | 8.1 | 8.8 | 20.2 | 10.6 | 14.3 | 13.1 |
| Sawada | 21.7 | 23.9 | 11.8 | 12.0 | 20.1 | 11.1 | 14.5 | 13.2 |
| MBMC | 21.8 | 23.7 | 11.9 | 12.0 | 20.1 | 10.9 | 15.0 | 6.2 |
| **Proposed** | 21.8 | 23.9 | 11.4 | 11.9 | 19.9 | 11.0 | 14.3 | 13.1 |

PESQ shows the same pattern: the proposed method is within 0.01–0.02 of Sawada/MBMC in almost every condition (e.g., 3.38 / 3.48 / 2.74 / 2.78 for the first four columns), while MBMC collapses on sources 2, 3, 5, 7 (PESQ 2.33 vs. 2.79 for proposed). Key observations:

- **Comparable quality at a fraction of the cost**: proposed ≈ Sawada ≈ MBMC in SIR/PESQ, but 4–5× faster.
- **Close sources hurt everyone** (sources 9, 10 and 5, 6): all algorithms degrade; the paper notes no theoretical explanation exists yet.
- **RG is unstable for close sources** — its empirically chosen region-partition threshold discards low-correlation frequencies, whereas the proposed method handles them explicitly via the local centroid.
- **ILRMA is strongest in most conditions** but is neither the cheapest nor universally best (inferior on sources 1, 2, 5 and 1, 2, 7, 9).

### Robustness to reverberation (3×3, sources 1, 2, 5)

All methods degrade as $\mathrm{RT}_{60}$ increases from 100 to 700 ms; the proposed, Sawada, and MBMC methods stay together and retain roughly 9 dB of improvement even at $\mathrm{RT}_{60} = 700$ ms, while RG falls off badly and ILRMA sits between.

![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/66eef361c93fdc5f332568e114c7f2265923409c13fdd2351b345fea0f58105b.jpg|Average SIR out versus reverberation time for five algorithms]]
![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/86b23bea00d388a509f1079b1fa13ecc098b70f99903ba6eaa89ccba6fbbeae5.jpg|Average PESQ versus reverberation time for five algorithms]]
*Figure 5: Separation performance of five algorithms as a function of reverberation time — (a) average $\mathrm{SIR}_{\mathrm{out}}$ (dB), (b) average PESQ.*

### Threshold selection ($\mathrm{RT}_{60} = 300$ ms)

Sweeping $U_{th}$ from 0 to 0.9 shows separation quality is insensitive to the threshold (the global stage repairs residual errors), but complexity is not: too small admits unreliable bins into the local centroid; too large discards reliable ones. Either extreme worsens the initialization and inflates the iteration count. **$0.5 \leq U_{th} \leq 0.7$** balances quality and cost.

![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/7dbb5fff9cc906cd766595d59283157228e435881afd1ad3cdd551c5188b5204.jpg|Average SIR out as a function of threshold U_th]]
![[raw/papers/kang-2019-low-complexity-permutation-alignment/figures/a56edba81c1859d9b94556bc7fccd519874c6f268e3d939f2585ea1f86692a06.jpg|Average number of one-centroid clustering iterations as a function of threshold U_th]]
*Figure 6: (a) Average $\mathrm{SIR}_{\mathrm{out}}$ and (b) average number of one-centroid clustering iterations as a function of the threshold $U_{th}$.*

## Key Contributions

1. **Confidence-thresholded bin-wise alignment**: instead of committing every bin to its neighbor-correlation argmax (RG's approach), only fix permutations whose average adjacent-bin correlation exceeds $U_{th}$, explicitly deferring unreliable bins rather than risking misalignment spread.
2. **Local centroid correction**: undetermined bins are resolved by correlating their power-ratio sequences against a centroid of high-confidence bins, which repairs isolated failures without iterating.
3. **Initialization-driven complexity reduction**: by running cheap local alignment *before* global one-centroid clustering (rather than after it, as in Sawada/MBMC), the global stage converges in <5 iterations instead of ~15, cutting total permutation-stage runtime from 39–51 s to 7.3 s in the 4-source benchmark at equal separation quality.

## Related Concepts

- [[concepts/permutation-alignment|Permutation Alignment]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis]]
- [[concepts/permutation-invariant-training|Permutation Invariant Training]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
