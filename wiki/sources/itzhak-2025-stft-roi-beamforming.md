---
type: source
created: 2026-10-07
updated: 2026-10-07
sources:
  - raw/papers/itzhak-2025-stft-roi-beamforming/full-text.md
  - https://doi.org/10.1109/TASLPRO.2025.3580986
  - zotero://select/items/0_XN7MFAWM
tags:
  - beamforming
  - roi-beamforming
  - microphone-arrays
  - doa-uncertainty
  - stft
  - speech-enhancement
---

# Itzhak & Cohen 2025: STFT-Domain Least-Distortion Region-of-Interest Beamforming

**Authors**: [[entities/gal-itzhak|Gal Itzhak]], [[entities/israel-cohen|Israel Cohen]]
**Institution**: Andrew and Erna Viterbi Faculty of Electrical and Computer Engineering, Technion — Israel Institute of Technology, Haifa, Israel
**Year**: 2025
**Type**: Journal Article
**Venue**: IEEE Transactions on Audio, Speech, and Language Processing
**DOI**: [10.1109/TASLPRO.2025.3580986](https://doi.org/10.1109/TASLPRO.2025.3580986)
**Zotero**: [XN7MFAWM](zotero://select/items/0_XN7MFAWM)

## Summary

This paper introduces two STFT-domain **least-distortion** beamformers that maximize array gain over a region-of-interest (ROI) — a continuous spatial region from which the desired signal may impinge — while minimizing the average distortion of the desired signal across that region. The **LD-MWNG** and **LD-MDF** beamformers optimize white noise gain and directivity factor respectively, and a single design parameter $K$ (the number of retained eigenvectors) trades array gain against distortion. This is the STFT-domain ROI formulation that [[sources/frank-2026-low-latency-roi-beamforming|Frank & Cohen 2026]] later unified with its time-domain counterpart under the name LDMG ROI beamforming.

## Problem Formulation

A desired source is recorded by $M$ microphones (arbitrary geometry). Under the multiplicative transfer function (MTF) approximation, the convolved desired signal at the $m$th sensor in the STFT domain is $X_m(k,r) = D_m(k, \theta_{\mathrm{d}}, \phi_{\mathrm{d}})\, X_1(k,r)$, giving the vector model $\mathbf{y}(k,r) = \mathbf{d}(k, \theta_{\mathrm{d}}, \phi_{\mathrm{d}}) X_1(k,r) + \mathbf{v}(k,r)$, where $\mathbf{d}$ is the relative transfer function vector with Sensor 1 as reference.

The beamformer applies complex per-sensor gains $\mathbf{h}(k,r) \in \mathbb{C}^M$ per frequency bin. For a single DOA, the classical distortionless constraint is $\mathbf{h}^H \mathbf{d} = 1$. For a **ROI** $\Omega(\phi_{\mathrm{d}} \in \Phi_\Omega, \theta_{\mathrm{d}} \in \Theta_\Omega)$ (far-field, azimuth/elevation only), the paper instead minimizes the **average distortion over the ROI**:

$$
J_{\mathrm{d},\Omega}[\mathbf{h}] = \frac{1}{|\Omega|} \iint_{(\theta,\phi) \in \Omega} |\mathbf{h}^H \mathbf{d}(k,\theta,\phi) - 1|^2 \sin\theta\, \mathrm{d}\phi\, \mathrm{d}\theta
$$

which yields the **ROI-distortion constraint**

$$
\boldsymbol{\Gamma}_{\mathbf{d},\Omega}(k)\, \mathbf{h}(k) = \mathbf{d}_\Omega(k)
$$

where $\mathbf{d}_\Omega(k)$ and $\boldsymbol{\Gamma}_{\mathbf{d},\Omega}(k)$ are the ROI averages of the steering vector and its outer product (computed by numerical integration).

## Methodology

### ROI-Generalized Performance Measures

All classical measures are generalized by replacing the rank-1 steering outer product with the ROI average $\boldsymbol{\Gamma}_{\mathbf{d},\Omega}$:

- **Array gain over ROI**: $\mathcal{G}_\Omega[\mathbf{h}] = \frac{\mathbf{h}^H \boldsymbol{\Gamma}_{\mathbf{d},\Omega} \mathbf{h}}{\mathbf{h}^H \boldsymbol{\Gamma}_{\mathbf{v}} \mathbf{h}}$
- **WNG** (white noise, $\boldsymbol{\Gamma}_{\mathbf{v}} = \mathbf{I}$): $\mathcal{W}_\Omega[\mathbf{h}] = \frac{\mathbf{h}^H \boldsymbol{\Gamma}_{\mathbf{d},\Omega} \mathbf{h}}{\mathbf{h}^H \mathbf{h}}$
- **DF** (diffuse noise with pseudo-correlation $\boldsymbol{\Gamma}_0$): $\mathcal{D}_\Omega[\mathbf{h}] = \frac{\mathbf{h}^H \boldsymbol{\Gamma}_{\mathbf{d},\Omega} \mathbf{h}}{\mathbf{h}^H \boldsymbol{\Gamma}_0 \mathbf{h}}$
- **Desired signal reduction factor**: $\xi_{\mathrm{d},\Omega}[\mathbf{h}] = \frac{1}{\mathbf{h}^H \boldsymbol{\Gamma}_{\mathbf{d},\Omega} \mathbf{h}}$ (closer to 1 = less distortion)

Subband and broadband variants are defined for each.

### Least-Distortion Maximum WNG (LD-MWNG)

Maximize the WNG subject to the ROI-distortion constraint. With the eigendecomposition $\mathbf{Q}^H \boldsymbol{\Gamma}_{\mathbf{d},\Omega} \mathbf{Q} = \boldsymbol{\Lambda}$ (rank $P \leq M$), the optimal weights are

$$
\mathbf{h}_{\mathrm{LD\text{-}MWNG}}(k) = \left[ \sum_{p=1}^{P} \frac{\mathbf{q}_p(k) \mathbf{q}_p^H(k)}{\lambda_p(k)} \right] \mathbf{d}_\Omega(k)
$$

When the ROI shrinks to a single DOA, LD-MWNG reduces to the **delay-and-sum** beamformer.

### Least-Distortion Maximum DF (LD-MDF)

Maximize the DF subject to the same constraint. Jointly diagonalizing $(\boldsymbol{\Gamma}_{\mathbf{d},\Omega}, \boldsymbol{\Gamma}_0)$ via generalized EVD with eigenvectors $\mathbf{t}_p$ gives

$$
\mathbf{h}_{\mathrm{LD\text{-}MDF}}(k) = \left[ \sum_{p=1}^{P} \frac{\mathbf{t}_p(k) \mathbf{t}_p^H(k)}{\lambda_p(k)} \right] \mathbf{d}_\Omega(k)
$$

For a single-DOA ROI, LD-MDF reduces to the classical distortionless maximum-DF (superdirective) beamformer $\mathbf{h}_{\mathrm{MDF}} \propto \boldsymbol{\Gamma}_0^{-1} \mathbf{d}$.

### The Design Parameter K

Both beamformers are truncated to the first $K$ eigenvectors ($1 \leq K \leq P$):

- **Decreasing $K$** → higher WNG/DF (more array gain) but higher average distortion
- $K = 1$ recovers the *unconstrained* maximum-gain beamformer that still minimizes ROI-average distortion
- $K = P$ gives the least-distortion solution
- The larger the ROI, the higher the rank of $\boldsymbol{\Gamma}_{\mathbf{d},\Omega}$ and the larger the usable $K$ (eigenvalue analysis suggests $K \leq 3$ for the smallest ROI tested, $K \leq 7$ for the largest)

## Experimental Setup

![[raw/papers/itzhak-2025-stft-roi-beamforming/figures/6844ef8542ba03f18063cfa99e2a94b69c90e5c9e922c0bb9d8c58d5ff09a011.jpg|Fig. 1]]

*Figure 1: Array geometry — a UCCA (3 rings × 8 microphones) in the x–y plane plus a 7-microphone ULA on the z-axis, $M = 31$; innermost ring radius and z-spacing both 3 cm.*

| Item | Setting |
|------|---------|
| **Array** | UCCA (3 rings × 8 mics) + z-axis ULA (7 mics), $M = 31$, 3 cm spacing |
| **ROIs** | R1: $\Phi_\Omega = [-30°, 30°]$, $\Theta_\Omega = 90°$ · R2: $\Phi_\Omega = [-45°, 45°]$, $\Theta_\Omega = 90°$ · R3: $\Phi_\Omega = [-45°, 45°]$, $\Theta_\Omega = [60°, 105°]$ |
| **K values** | $K \in \{1,2,3\}$ for R1; $K \in \{1,4,7\}$ for R3 |
| **Room / RIRs** | Image-method RIR generator, $8 \times 7 \times 3$ m room, array at $(3,3,1)$ m, $T_{60} \in \{200, 600\}$ ms |
| **Noise fields** | White thermal Gaussian + spherically isotropic diffuse + 2 directional interferences (+z axis; $\phi = 135°$); white noise 30 dB weaker |
| **Speech** | 24 TIMIT utterances (12 per gender), $f_s = 16$ kHz |
| **STFT** | Hamming window, length 512 (32 ms), 75% overlap |
| **Input SNR** | 3 dB (PESQ/STOI study); 10 dB (DNSMOS study) |
| **Baselines** | $\mathbf{h}_{\mathrm{MDF}}$ and $\mathbf{h}_{\mathrm{DS}}$ steered to ROI center; $\mathbf{f}_{\mathrm{MWNG/MDF}}$ (Kronecker-product SCCA, 32 mics); $\mathbf{w}_{\mathrm{robust}}$ (Vorobyov et al. 2003 robust adaptive, 31-mic ULA) |
| **Metrics** | PESQ, STOI, DNSMOS (P.808 + SIG/BAK/OVRL) |
| **Miscalibration** | Position offsets $\sigma_{\mathrm{pos}} = 3$ mm, gain skews $\sigma_{\mathrm{gain}} = 3\%$ (DNSMOS study, planar 24-mic UCCA) |

## Results

### K Trade-off (broadband measures)

![[raw/papers/itzhak-2025-stft-roi-beamforming/figures/f0205270049bd7ed8c1a29fc801c02d289691428a9a857d99b668d295229068f.jpg|Fig. 3a]]

![[raw/papers/itzhak-2025-stft-roi-beamforming/figures/3b67bf04c6e47562dea145d3f5262a1ab08b229ab35d4728f7cebd2d585b09c0.jpg|Fig. 3b]]

![[raw/papers/itzhak-2025-stft-roi-beamforming/figures/c2364db5f6f67835f1fc55e8333f090acbfb3c2ffc10c26e3ca0e75f4d43d776.jpg|Fig. 3c]]

*Figure 3: Broadband (a) WNG, (b) DF, and (c) desired signal reduction factor versus K for the three ROIs. Lower K raises both gains and distortion; LD-MDF is more distortion-sensitive than LD-MWNG.*

- **LD-MDF is more sensitive to desired-signal reduction than LD-MWNG**; the larger the ROI, the greater the potential reduction.
- For the largest ROI no signal reduction is apparent for $K > 7$; for the smallest, already for $K > 3$ — setting practical upper bounds on $K$.
- Beampatterns (3-D at 3 kHz, and azimuth/elevation versus frequency) show $K = 1$ gives high directivity with mild attenuation near ROI edges; larger $K$ reduces edge attenuation at the price of stronger sidelobes.

### Speech Enhancement (PESQ / STOI)

| Scenario | PESQ winner | STOI winner |
|----------|-------------|-------------|
| R1, $T_{60}=200$ ms, no DOA deviation | $\mathbf{f}_{\mathrm{MWNG/MDF}}$ (2.19) | Proposed |
| R1, $T_{60}=200$ ms, deviation $(90°, 20°)$ | **Proposed** ($\mathbf{h}_{\mathrm{LD\text{-}MDF},3}$ = 1.63 vs 1.13 for $\mathbf{f}_{\mathrm{MWNG/MDF}}$) | **Proposed** ($\mathbf{h}_{\mathrm{LD\text{-}MDF},1/2}$ ≈ 0.93/0.91) |
| R1, $T_{60}=600$ ms | Existing ($\mathbf{h}_{\mathrm{MDF}}$) | **Proposed** ($\mathbf{h}_{\mathrm{LD\text{-}MDF},1/2}$ ≈ 0.81) |
| R3, $T_{60}=200$ ms, large deviation $(65°, 40°)$ | **Proposed** ($\mathbf{h}_{\mathrm{LD\text{-}MDF},7}$) | **Proposed** |
| R3, $T_{60}=600$ ms | Mixed | **Proposed** (significant margin) |

Key pattern: with significant DOA deviation and mild reverberation, the proposed beamformers dominate on both metrics; under severe reverberation they still win STOI (intelligibility) while losing PESQ. The best $K$ **grows with the DOA deviation** ($K=1$ at $(80°, 0°)$, $K=4$ at $(80°, 20°)$, $K=7$ at $(65°, 40°)$).

### Robustness to Array Miscalibration (DNSMOS)

- Without DOA deviation, $\mathbf{h}_{\mathrm{MDF}}$ and $\mathbf{f}_{\mathrm{MWNG/MDF}}$ score best on SIG/BAK/OVRL — but $\mathbf{h}_{\mathrm{LD\text{-}MDF},1}$ wins the DNSMOS P.808 score regardless of calibration condition.
- With deviation $(90°, 20°)$, the proposed approach is superior on **both** P.808 and P.835, with a significant gap, and $\mathbf{h}_{\mathrm{LD\text{-}MDF},1}$ / $\mathbf{h}_{\mathrm{LD\text{-}MWNG},1}$ are markedly more robust to miscalibration ($\sigma_{\mathrm{pos}} = 3$ mm, $\sigma_{\mathrm{gain}} = 3\%$) than the baselines.

## Key Contributions

1. **ROI-generalized formulation**: signal model, distortion constraint ($\boldsymbol{\Gamma}_{\mathbf{d},\Omega} \mathbf{h} = \mathbf{d}_\Omega$), and performance measures (subband/broadband WNG, DF, desired-signal reduction factor) that directly account for all directions within the ROI — extending the standard single-direction formulation.
2. **Two least-distortion beamformers**: LD-MWNG (EVD) and LD-MDF (GEVD), each with a single design parameter $K$ trading array gain against average ROI distortion, and each reducing to a classical beamformer (delay-and-sum / maximum-DF) for single-DOA ROIs.
3. **Design guidance for K**: eigenvalue-spectrum analysis linking the ROI size to the rank of $\boldsymbol{\Gamma}_{\mathbf{d},\Omega}$ and to practical upper bounds on $K$; empirically, the best $K$ increases with the actual DOA deviation.
4. **Comprehensive evaluation**: speech experiments across ROIs, reverberation levels ($T_{60}$ 200/600 ms), noise fields, DOA deviations, and array miscalibration artifacts, showing superior intelligibility (STOI), DNSMOS, and robustness over classical (MDF, DS, Vorobyov-robust) and recent (SCCA Kronecker) baselines when DOA deviations are significant and reverberation mild.

## Related Concepts

- [[concepts/roi-beamforming|Region-of-Interest Beamforming]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/white-noise-gain|White Noise Gain]]
- [[concepts/directivity-factor|Directivity Factor]]
- [[concepts/superdirective-beamforming|Superdirective Beamforming]]

## Related Entities

- [[entities/gal-itzhak|Gal Itzhak]]
- [[entities/israel-cohen|Israel Cohen]]

## Related Sources

- [[sources/frank-2026-low-latency-roi-beamforming|Frank & Cohen 2026: Low-latency Audio Front-end ROI Beamforming for Smart Glasses]] — the follow-up that unifies this STFT-domain formulation with its time-domain counterpart (LDMG) and shows the time-domain implementation halves latency

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
