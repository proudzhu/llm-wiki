---
type: source
created: 2026-09-17
updated: 2026-09-17
sources:
  - raw/papers/cohen-2019-differential-kronecker-beamforming/full-text.txt
  - https://doi.org/10.1109/TASLP.2019.2895241
  - zotero://select/items/0_QVUNYXL6
tags:
  - beamforming
  - microphone-arrays
  - kronecker-product
  - differential-beamforming
  - fixed-beamformer
  - superdirective-beamforming
---

# Cohen, Benesty & Chen 2019: Differential Kronecker Product Beamforming

**Authors**: [[entities/israel-cohen|Israel Cohen]], [[entities/jacob-benesty|Jacob Benesty]], [[entities/jingdong-chen|Jingdong Chen]]
**Affiliations**: Andrew and Erna Viterbi Faculty of Electrical Engineering, Technion — Israel Institute of Technology, Haifa, Israel; INRS-EMT, University of Quebec, Montreal, Canada; Northwestern Polytechnical University, Xi'an, China
**Venue**: IEEE/ACM Transactions on Audio, Speech, and Language Processing, vol. 27, no. 5, pp. 892–902, May 2019
**Type**: Journal article
**DOI**: [10.1109/TASLP.2019.2895241](https://doi.org/10.1109/TASLP.2019.2895241)
**Zotero**: [QVUNYXL6](zotero://select/items/0_QVUNYXL6)
**Funding**: Israel Science Foundation Grant 576/16; ISF-NSFC joint research program Grants 2514/17 and 61761146001

## Summary

This paper introduces **differential Kronecker product (KP) beamformers**: for a class of microphone arrays whose steering vector decomposes as a Kronecker product of two smaller *virtual* array steering vectors ($M = M_1 M_2$), the differential beamformer is decomposed accordingly as $\mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$, estimating only $M_1 + M_2$ coefficients instead of $M_1 M_2$ and inverting smaller matrices. The authors show that the global beampattern and [[concepts/white-noise-gain|white noise gain]] factorize as products of the virtual-array counterparts, while the directivity factor and front-to-back ratio do not — which leads to iterative alternating algorithms for the KP hypercardioid and supercardioid. This is the original formulation of [[concepts/kronecker-product-beamforming|Kronecker product beamforming]], later generalized to arbitrary geometries (sum-of-products representation, [[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021]]) and to $N$-way rank-$P$ decompositions ([[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025]]).

## Problem Formulation

Two virtual uniform linear arrays (ULAs) lie on the same line: **ULA 1** has $M_1$ microphones with interelement spacing $M_2\delta$, and **ULA 2** has $M_2$ microphones with spacing $\delta$ (unit spacing). For a far-field plane wave from azimuth $\theta$ ($c = 340$ m/s), the virtual steering vectors are

$$\mathbf{d}_{1,\theta}(\omega) = [1,\; e^{-jM_2\varpi\cos\theta},\; \dots,\; e^{-j(M_1-1)M_2\varpi\cos\theta}]^T, \qquad \mathbf{d}_{2,\theta}(\omega) = [1,\; e^{-j\varpi\cos\theta},\; \dots,\; e^{-j(M_2-1)\varpi\cos\theta}]^T$$

with $\varpi = \omega\delta/c$. The physical *global* ULA has $M = M_1 M_2$ microphones with spacing $\delta$ and steering vector $\mathbf{d}_\theta(\omega) = \mathbf{d}_{1,\theta}(\omega) \otimes \mathbf{d}_{2,\theta}(\omega)$ — satisfied whenever the physical array can be obtained by replicating one virtual array at the microphone positions of the other. With the desired source at endfire ($\theta = 0$), the observation and its covariance are

$$\mathbf{y} = \mathbf{d}_0 X + \mathbf{v}, \qquad \boldsymbol{\Phi}_y = \phi_X \mathbf{d}_0 \mathbf{d}_0^H + \phi_{V_1} \boldsymbol{\Gamma}_v$$

where $\boldsymbol{\Gamma}_v$ is the noise pseudo-coherence matrix; for a spherically isotropic (diffuse) field, $[\boldsymbol{\Gamma}(\omega)]_{mn} = \mathrm{sinc}[(m-n)\varpi]$.

**KP beamforming** applies a filter that follows the steering-vector decomposition:

$$Z = \mathbf{h}^H \mathbf{y}, \qquad \mathbf{h} = \mathbf{h}_1 \otimes \mathbf{h}_2$$

so only $M_1 + M_2$ coefficients are estimated instead of $M_1 M_2$, with the distortionless constraint $\mathbf{h}^H \mathbf{d}_0 = (\mathbf{h}_1^H \mathbf{d}_{1,0})(\mathbf{h}_2^H \mathbf{d}_{2,0}) = 1$ enforced by choosing each factor distortionless. A similar decomposition appeared earlier only in MIMO radar (Abramovich, Frazer & Johnson 2010).

## Methodology

### Performance measures under KP filters

Two separation identities make all derivations possible:

$$\mathbf{h}_1 \otimes \mathbf{h}_2 = (\mathbf{h}_1 \otimes \mathbf{I}_{M_2})\,\mathbf{h}_2 = (\mathbf{I}_{M_1} \otimes \mathbf{h}_2)\,\mathbf{h}_1$$

- **Beampattern factorizes**: $\mathcal{B}_\theta(\mathbf{h}) = \mathcal{B}_{1,\theta}(\mathbf{h}_1) \times \mathcal{B}_{2,\theta}(\mathbf{h}_2)$ — the global [[concepts/directivity-pattern|beampattern]] is a product of two polynomials, hence has at most $M_1 + M_2 - 2$ distinct nulls (vs. $M_1 M_2 - 1$ for the conventional approach).
- **WNG factorizes**: $W(\mathbf{h}) = W_1(\mathbf{h}_1) \times W_2(\mathbf{h}_2) \leq M_1 M_2$.
- **DF does not factorize**: $D(\mathbf{h}) \neq D_1(\mathbf{h}_1) \times D_2(\mathbf{h}_2)$ because $\boldsymbol{\Gamma} \neq \boldsymbol{\Gamma}_1 \otimes \boldsymbol{\Gamma}_2$. With $\mathbf{h}_2$ fixed, $D(\mathbf{h}_1|\mathbf{h}_2) = |\mathbf{h}_1^H \mathbf{d}_{1,0}|^2 / (\mathbf{h}_1^H \boldsymbol{\Gamma}_{\mathbf{h}_2} \mathbf{h}_1)$ with $\boldsymbol{\Gamma}_{\mathbf{h}_2} = (\mathbf{I}_{M_1} \otimes \mathbf{h}_2)^H \boldsymbol{\Gamma} (\mathbf{I}_{M_1} \otimes \mathbf{h}_2)$ (and symmetrically for $\mathbf{h}_1$ fixed).
- **FBR does not factorize**: the front-to-back ratio $F(\mathbf{h}) = \mathbf{h}^H \boldsymbol{\Gamma}_f \mathbf{h} / \mathbf{h}^H \boldsymbol{\Gamma}_b \mathbf{h}$ admits the same conditional form with $\boldsymbol{\Gamma}_{f,\mathbf{h}_2}, \boldsymbol{\Gamma}_{b,\mathbf{h}_2}$.

### KP cardioid (closed-form)

The $(M_2 - 1)$th-order cardioid places a null of multiplicity $M_2 - 1$ at $\pi$; combining the derivative constraints $\mathcal{B}^{[i]}_{2,\pi}(\mathbf{h}_2) = 0$ with the distortionless constraint gives a linear system whose solution is $\mathbf{h}_{2,C} = \mathbf{D}_{2,\pi}^{-H} \mathbf{i}$. Taking the delay-and-sum beamformer $\mathbf{h}_{1,\mathrm{DS}} = \mathbf{d}_{1,0}/M_1$ (which maximizes WNG) for ULA 1, the KP cardioid is $\mathbf{h}_C = \mathbf{h}_{1,\mathrm{DS}} \otimes \mathbf{h}_{2,C}$. A **robust KP cardioid** trades DF against WNG via Tikhonov-style regularization of the null constraints:

$$\min_{\mathbf{h}_2} \mathbf{h}_2^H (\mathbf{D}'_{2,\pi} \mathbf{D}_{2,\pi}^{\prime H} + \epsilon_2 \mathbf{I}_{M_2}) \mathbf{h}_2 \quad \text{subject to} \quad \mathbf{C}_{2,\pi}^H \mathbf{h}_2 = \mathbf{i}_c$$

where $\epsilon_2 \geq 0$ controls the tradeoff (larger $\epsilon_2$ raises WNG but lowers DF).

### KP dipole (closed-form)

The dipole of order $M_2 - 1$ has its multiplicity-$(M_2-1)$ null at $\pi/2$: $\mathbf{h}_{2,D} = \mathbf{D}_{2,\pi/2}^{-H} \mathbf{i}$. Since the dipole also has unit response at $\pi$, ULA 1 must satisfy $\mathbf{C}_{1,\pi}^H \mathbf{h}_1 = [1,\; 1]^T$, and maximizing its WNG under this constraint yields the minimum-norm beamformer $\mathbf{h}_{1,\mathrm{MN}} = \mathbf{C}_{1,\pi}(\mathbf{C}_{1,\pi}^H \mathbf{C}_{1,\pi})^{-1}[1,\;1]^T$. The KP dipole is $\mathbf{h}_D = \mathbf{h}_{1,\mathrm{MN}} \otimes \mathbf{h}_{2,D}$, with a robust $\epsilon_2$-regularized variant analogous to the cardioid.

### KP hypercardioid (iterative DF maximization)

Since $D(\mathbf{h})$ cannot be maximized directly, an alternating iteration maximizes the conditional DFs: initialize $\mathbf{h}_2^{(0)} = \boldsymbol{\Gamma}_2^{-1}\mathbf{d}_{2,0}/(\mathbf{d}_{2,0}^H \boldsymbol{\Gamma}_2^{-1}\mathbf{d}_{2,0})$ (the virtual-array hypercardioid), then alternate

$$\mathbf{h}_1^{(n)} = \frac{\boldsymbol{\Gamma}_{\mathbf{h}_2^{(n-1)}}^{-1} \mathbf{d}_{1,0}}{\mathbf{d}_{1,0}^H \boldsymbol{\Gamma}_{\mathbf{h}_2^{(n-1)}}^{-1} \mathbf{d}_{1,0}}, \qquad \mathbf{h}_2^{(n)} = \frac{\boldsymbol{\Gamma}_{\mathbf{h}_1^{(n)}}^{-1} \mathbf{d}_{2,0}}{\mathbf{d}_{2,0}^H \boldsymbol{\Gamma}_{\mathbf{h}_1^{(n)}}^{-1} \mathbf{d}_{2,0}}$$

with $\boldsymbol{\Gamma}_{\mathbf{h}_2} = (\mathbf{I}_{M_1} \otimes \mathbf{h}_2)^H \boldsymbol{\Gamma} (\mathbf{I}_{M_1} \otimes \mathbf{h}_2)$ and $\boldsymbol{\Gamma}_{\mathbf{h}_1} = (\mathbf{h}_1 \otimes \mathbf{I}_{M_2})^H \boldsymbol{\Gamma} (\mathbf{h}_1 \otimes \mathbf{I}_{M_2})$, giving $\mathbf{h}_H^{(n)} = \mathbf{h}_1^{(n)} \otimes \mathbf{h}_2^{(n)}$.

### KP supercardioid (iterative FBR maximization)

Analogously, maximizing the FBR alternates generalized eigenvector updates: each subfilter is $\mathbf{t}/(\mathbf{d}_{i,0}^H \mathbf{t})$ where $\mathbf{t}$ is the eigenvector of the maximum eigenvalue of $\boldsymbol{\Gamma}_{b,\mathbf{h}_j}^{-1} \boldsymbol{\Gamma}_{f,\mathbf{h}_j}$ built from the other (fixed) subfilter, giving $\mathbf{h}_S^{(n)} = \mathbf{h}_1^{(n)} \otimes \mathbf{h}_2^{(n)}$.

## Experimental Setup

The paper is a design/analysis study evaluated by beampattern simulation (no recorded speech):

| Item | Value |
|:-----|:------|
| Array geometry | Global ULA of $M = M_1 M_2$ mics, spacing $\delta$; virtual ULA 1 ($M_1$ mics, spacing $M_2\delta$), virtual ULA 2 ($M_2$ mics, spacing $\delta$) |
| Look direction | Endfire ($\theta = 0$) |
| Noise field | Spherically isotropic (diffuse) for DF; spatially white for WNG |
| Spacings | $\delta = 1$ cm (cardioid, dipole); $\delta = 5$ mm (hypercardioid, supercardioid) |
| Configurations | $M_1, M_2 \in \{2, 3, 4, 8\}$ (e.g., $M_1 = M_2 = 4$; $M_1 = 2, M_2 = 8$; $M_1 = M_2 = 3$; $M_1 = M_2 = 2$) |
| Regularization | $\epsilon_2 \in \{0.001, 0.01, 0.1, 1\}$ (robust cardioid); $\epsilon_2 = 10^{-8}$ (dipole plots) |
| Metrics | Directivity factor (DF), white noise gain (WNG), front-to-back ratio (FBR) vs. frequency; beampatterns at $f = 3$ kHz |
| Baselines | Traditional cardioid/dipole; minimum-norm (MN) cardioid/dipole with the same total $M$ |

## Results

- **KP cardioid** (Figs. 2–4): DF and WNG of the third-order KP cardioid exceed those of the traditional third-order cardioid, and both increase with $M_1$. Against the MN cardioid with the same total $M = 16$: the MN cardioid achieves the maximum WNG but its low-frequency DF drops below even the 4-mic traditional cardioid; KP cardioids give a more moderate WNG increase while also raising DF — a more flexible DF–WNG tradeoff.
- **Robust KP cardioid** (Fig. 5): increasing $\epsilon_2$ monotonically raises WNG at the cost of DF.
- **KP dipole** (Figs. 6–7): the MN dipole has the highest WNG but the worst low-frequency DF; KP dipoles offer moderate WNG increases and different DF-vs-frequency shapes.
- **KP hypercardioid** (Fig. 8, $M_1 = M_2 = 3$, $\delta = 5$ mm): DF increases at each alternating iteration and roughly converges after **five iterations**, while WNG decreases at each iteration.
- **KP supercardioid** (Fig. 9, $M_1 = M_2 = 2$, $\delta = 5$ mm): FBR increases each iteration and converges after roughly **three iterations**; DF also rises while WNG stays almost unchanged.

## Key Contributions

1. **Introduced differential Kronecker product beamforming** — the first formulation decomposing a differential beamformer into two virtual-array subfilters following the Kronecker structure of the steering vector ($M_1 + M_2$ coefficients instead of $M_1 M_2$, smaller matrix inversions). This is the origin of the Kronecker product beamforming line later extended to sum-of-products arbitrary-geometry filters ([[sources/wang-2021-kronecker-adaptive-beamforming|Wang et al. 2021]]) and $N$-way rank-$P$ robust superdirective designs ([[sources/zhu-2025-kronecker-superdirective-beamforming|Zhu et al. 2025]]).
2. **Factorization theory for KP filters** — proved that the global beampattern and WNG factorize as products of the virtual-array quantities, while the DF and FBR do not ($\boldsymbol{\Gamma} \neq \boldsymbol{\Gamma}_1 \otimes \boldsymbol{\Gamma}_2$), and derived the conditional forms $D(\mathbf{h}_1|\mathbf{h}_2)$, $F(\mathbf{h}_1|\mathbf{h}_2)$ via the separation identities.
3. **Four concrete differential KP designs** — cardioid and dipole in closed form (with $\epsilon_2$-regularized robust variants), hypercardioid by alternating DF maximization (~5 iterations), supercardioid by alternating generalized-eigenvalue FBR maximization (~3 iterations).
4. **Design flexibility** — KP designs beat the traditional differential beamformers in both DF and WNG and occupy a more favorable region of the DF–WNG tradeoff than minimum-norm designs, adding a new axis of control beyond the number of microphones.

## Related Concepts

- [[concepts/kronecker-product-beamforming|Kronecker Product Beamforming]]
- [[concepts/differential-microphone-array|Differential Microphone Array]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/directivity-pattern|Directivity Pattern]]
- [[concepts/fixed-beamformer|Fixed Beamformer]]
- [[concepts/diagonal-loading|Diagonal Loading]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/beamforming|Beamforming]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
