---
type: source
created: 2026-05-20
updated: 2026-05-20
sources:
  - raw/papers/nishikori-2026-fast-multichannel-nmf-block-diagonal-scm-bss/full-text.md
  - https://arxiv.org/abs/2605.19388v1
  - zotero://select/items/0_XYXBN3H5
tags:
  - blind-source-separation
  - distributed-microphone-arrays
  - fastmnf
  - nonnegative-matrix-factorization
  - spatial-covariance-matrix
aliases:
  - Nishikori et al. 2026: Distributed FastMNMF for BSS
---

# Nishikori, Ito, Yamaoka, Takamune & Saruwatari 2026: Distributed FastMNMF for Efficient BSS Using Distributed Microphone Arrays

**Authors**: Hirotaka Nishikori, Nobutaka Ito, Kouei Yamaoka, Norihiro Takamune, Hiroshi Saruwatari
**Institutions**: The University of Tokyo (Nishikori, Yamaoka, Takamune, Saruwatari); AIST (Ito)
**Published**: arXiv preprint, May 2026
**arXiv**: [2605.19388](https://arxiv.org/abs/2605.19388v1)
**📎 Zotero**: [zotero://select/items/0_XYXBN3H5](zotero://select/items/0_XYXBN3H5)

## Summary

Proposes **Distributed FastMNMF**, a blind source separation method for distributed microphone arrays that imposes a **block-diagonal structure** on the source spatial covariance matrices (SCMs), with each block corresponding to one subarray. This reduces matrix inversion complexity from $\mathcal{O}(M^4)$ to $\mathcal{O}(\sum_l M^{(l)4})$ per iteration per frequency bin, while sharing the NMF-based source spectrogram model across subarrays. In simulated experiments (3 subarrays × 4 mics, 3-5 sources), the method achieved ~2.95× speedup over full-array FastMNMF and ~0.5-0.8 dB SDR improvement over single-subarray FastMNMF.

## Problem Formulation

### FastMNMF Background

The observed STFT coefficients $\mathbf{x}_{ij} \in \mathbb{C}^M$ are modeled as:

$$p(\mathbf{x}_{ij}) = \mathcal{N}_{\mathbb{C}}\left(\mathbf{x}_{ij}; \mathbf{0}, \sum_n h_{ijn}\mathbf{R}_{in}\right)$$

where $h_{ijn} = \sum_k t_{ikn}v_{kjn}$ (NMF model) and $\mathbf{R}_{in}$ is the source SCM. FastMNMF assumes joint diagonalizability of SCMs across sources:

$$\mathbf{W}_i^{\mathsf{H}}\mathbf{R}_{in}\mathbf{W}_i = \mathbf{\Lambda}_{in}, \quad \forall n$$

reducing computational cost by diagonalizing the $M \times M$ matrices.

### Distributed FastMNMF

For $L$ subarrays with $M^{(l)}$ microphones each ($M = \sum_l M^{(l)}$), the SCMs are constrained to be block-diagonal:

$$\mathbf{R}_{in} = \operatorname{blkdiag}\left(\mathbf{R}_{in}^{(1)}, \dots, \mathbf{R}_{in}^{(L)}\right)$$

Equivalently, $\mathbf{W}_i$ is constrained to be block-diagonal: $\mathbf{W}_i = \operatorname{blkdiag}(\mathbf{W}_i^{(1)}, \dots, \mathbf{W}_i^{(L)})$. Joint diagonalization and iterative projection (IP) updates are performed independently per subarray, while the NMF variables $t_{ikn}, v_{kjn}$ are shared globally.

The negative log-likelihood cost function becomes:

$$\sum_l\Biggl[\sum_{i,j,\mu}\Biggl(\frac{|y_{ij\mu}^{(l)}|^2}{\sum_{k,n}t_{ikn}v_{kjn}[\mathbf{\Lambda}_{in}^{(l)}]_{\mu\mu}} + \ln\sum_{k,n}t_{ikn}v_{kjn}[\mathbf{\Lambda}_{in}^{(l)}]_{\mu\mu}\Biggr) - \sum_i J\ln|\det\mathbf{W}_i^{(l)}|^2\Biggr]$$

## Methodology

### Update Rules

- **$\mathbf{W}_i^{(l)}$** updated via iterative projection (IP) independently per subarray (Eqs. 14-16)
- **$t_{ikn}, v_{kjn}, \mathbf{\Lambda}_{in}^{(l)}$** updated via MM algorithm using conventional FastMNMF rules (Eqs. 8-10) but applied to the decorrelated signals $y_{ij\mu}^{(l)}$
- After estimation, source images at each subarray obtained via multichannel Wiener filter

### Computational Complexity

| Operation | FastMNMF (all) | Distributed FastMNMF |
|-----------|----------------|----------------------|
| $\mathbf{W}_i$ update | $\mathcal{O}(M^4 + JM^3)$ | $\mathcal{O}(\sum_l M^{(l)4} + J\sum_l M^{(l)3})$ |
| NMF/SCM update | $\mathcal{O}(JM^2 + JN(K+M))$ | $\mathcal{O}(J\sum_l M^{(l)2} + JN(K+M))$ |
| **Total per freq** | $\mathcal{O}(M^4 + JM^3 + JN(K+M))$ | $\mathcal{O}(\sum_l M^{(l)4} + J\sum_l M^{(l)3} + JN(K+M))$ |

## Experimental Setup

- **Room**: $6 \times 4 \times 2.5$ m, RT60 = 300 ms
- **Arrays**: 3 subarrays, each 4 mics in tetrahedron (4.2 cm edge), 12 mics total
- **Sources**: 3 or 5 speech sources (JNAS corpus), 10 s at 16 kHz
- **STFT**: Hann window 256 ms, 64 ms shift
- **NMF**: $K = 16$, 200 iterations
- **Evaluation**: SDR improvement at reference microphone (left subarray)
- **Mixtures**: 120 mixtures × 10 NMF initializations = 1200 trials

## Results

### SDR Improvement

| Condition | Distributed FastMNMF | FastMNMF (one subarray) | FastMNMF (all subarrays) |
|-----------|---------------------|-------------------------|-------------------------|
| 3 sources | **13.4 dB** (med: 13.9) | 12.5 dB (med: 13.0) | 15.7 dB (med: 15.9) |
| 5 sources | **6.3 dB** (med: 5.9) | 5.8 dB (med: 5.4) | 7.3 dB (med: 6.9) |

Distributed FastMNMF gained +0.8 dB (3 src) / +0.5 dB (5 src) over single-subarray, and was ~2.95× faster than full-array FastMNMF (235 s vs 694 s).

### Computation Time

| Method | Time (s) |
|--------|----------|
| FastMNMF (one subarray) | $109.3 \pm 0.3$ |
| FastMNMF (all subarrays) | $694.0 \pm 0.7$ |
| Distributed FastMNMF | $235.3 \pm 2.4$ |

## Key Contributions

1. **Block-diagonal SCM constraint** for distributed microphone arrays within FastMNMF framework
2. **Shared source spectrogram model** across subarrays while discarding inter-subarray covariance �?enables information aggregation without full matrix operations
3. **Provably equivalent** to conventional FastMNMF with block-diagonal $\mathbf{W}_i$ constraint
4. **Computational trade-off analysis**: $L^3$ reduction in matrix inversion cost, $L^2$ reduction in scalar-matrix multiplication cost vs. full-array approach
5. **Locally underdetermined capability**: Works with 5 sources over 4-mic subarrays by sharing spectrogram information across subarrays

## Related Concepts

- [[concepts/fastmnmf|FastMNMF]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/distributed-anc|Distributed ANC]] (related distributed processing paradigm)
- Blind Source Separation (BSS)

## Related Entities

- [[entities/hirotaka-nishikori|Hirotaka Nishikori]]
- [[entities/nobutaka-ito|Nobutaka Ito]]
- [[entities/kouei-yamaoka|Kouei Yamaoka]]
- [[entities/norihiro-takamune|Norihiro Takamune]]
- [[entities/hiroshi-saruwatari|Hiroshi Saruwatari]]
