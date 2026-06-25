---
type: source
created: 2026-06-25
updated: 2026-06-25
sources:
  - raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/full-text.md
  - https://doi.org/10.1109/ICASSP48485.2024.10447208
  - zotero://select/items/0_PYI2K3NS
tags:
  - active-noise-control
  - soundfield-interpolation
  - physics-informed-neural-network
  - pinn
  - virtual-sensing
  - remote-microphone-technique
  - icassp-2024
---

# Zhang, Ma, Abhayapala, Samarasinghe & Bastine 2024: An Active Noise Control System Based on Soundfield Interpolation Using a Physics-Informed Neural Network

**Authors**: [[entities/yile-angela-zhang|Yile (Angela) Zhang]], [[entities/fei-ma|Fei Ma]], [[entities/thushara-d-abhayapala|Thushara D. Abhayapala]], [[entities/prasanga-n-samarasinghe|Prasanga N. Samarasinghe]], [[entities/amy-bastine|Amy Bastine]]
**Affiliation**: Audio and Acoustic Signal Processing Group, The Australian National University, Australia
**Venue**: ICASSP 2024, pp. 506-510
**Type**: Conference paper
**Year**: 2024
**DOI**: [10.1109/ICASSP48485.2024.10447208](https://doi.org/10.1109/ICASSP48485.2024.10447208)
**Zotero**: [PYI2K3NS](zotero://select/items/0_PYI2K3NS)

## Summary

Conventional multiple-point [[concepts/active-noise-control|active noise control]] (ANC) systems require placing error microphones within the region of interest (ROI), which is inconvenient for users. This paper proposes placing monitoring microphones *outside* the ROI and interpolating the soundfield within the ROI using a [[concepts/physics-informed-neural-network|physics-informed neural network]] (PINN). The PINN exploits the acoustic wave equation to assist soundfield interpolation with a limited number of monitoring microphones, outperforming the [[concepts/spherical-harmonic-transform|spherical harmonics]] (SH) method in simulations. When combined with a multi-channel [[concepts/filtered-x-lms-algorithm|FxLMS]] controller, the PINN-assisted ANC system achieves better noise reduction than the multiple-point ANC baseline.

![[raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/figures/ef504d008ed2321bc3448976da516c336138082de64844589a0b63a6b47a12cb.jpg|System setup: primary noise source, reference sensor, secondary sources, and monitoring microphones around the ROI]]
*Figure 1: System setup. A primary noise source generates the primary noise field and is detected by the reference sensor. An ANC system cancels the primary noise field at the ROI (user's ears) by superimposing it with a secondary noise field produced by the secondary sources.*

## Problem Formulation

Consider an ANC system (Fig. 1) with $L$ secondary sources and $Q$ monitoring microphones. A reference sensor close to the primary noise source produces signal $x(n)$. Let $d_\ell(n)$, $\ell = 1, \ldots, L$ be the secondary source signals and $e_q^{(\mathrm{M})}(n)$, $q = 1, \ldots, Q$ be the received signal at the $q$-th monitoring microphone located at $(x_q, y_q, z_q)$:

$$
e_q^{(\mathrm{M})}(n) = p_q(n) + \sum_{\ell=1}^{L} s_{\ell,q}(n) * d_\ell(n), \tag{1}
$$

where $*$ is convolution, $p_q(n)$ is the primary signal at the $q$-th monitoring microphone, and $s_{\ell,q}(n)$ is the impulse response of the secondary path from the $\ell$-th secondary source to the $q$-th monitoring microphone.

Consider $V$ virtual microphones positioned at or close to the two ears (ROI) at $(x_v, y_v, z_v)$ with signal $e_v^{(\mathrm{V})}(n)$, $v = 1, \ldots, V$. Although these virtual signals cannot be measured directly, they can be interpolated from the monitoring microphone measurements:

$$
e_v^{(\mathrm{V})}(n) = \mathcal{I}\bigl(e_q^{(\mathrm{M})}(n)\bigr), \tag{2}
$$

where $\mathcal{I}(\cdot)$ is the interpolation function. The aims of the paper are twofold:

1. **Interpolate** the virtual microphone signals $e_v^{(\mathrm{V})}$ based on the monitoring signals $e_q^{(\mathrm{M})}$ using a PINN.
2. **Set up an ANC system** to reduce noise at the ROI using the FxLMS algorithm and the interpolated signals $e_v^{(\mathrm{V})}$.

## Methodology

The two ANC systems compared in this work are depicted in Fig. 2.

![[raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/figures/e5a305731e2fde0841efb35e6bd9731b70c4e5054a4bee9b24df4a6913985307.jpg|Block diagram of multiple-point ANC system and PINN-assisted ANC system]]
*Figure 2: Block diagram of multiple-point ANC system and PINN-assisted ANC system, which differ by the error signal used in the FxLMS algorithm.*

### Multiple-point ANC System (Baseline)

The standard single-reference, multiple-output [[concepts/filtered-x-lms-algorithm|FxLMS]] algorithm updates the adaptive filter weights for the $\ell$-th secondary source iteratively:

$$
\mathbf{w}_\ell(n+1) = \mathbf{w}_\ell(n) + \mu \sum_{q=1}^{Q} \mathbf{x}_{\ell,q}'(n)\, e_q^{(\mathrm{M})}(n), \tag{3}
$$

with step-size $\mu$ and filtered reference signal

$$
\mathbf{x}_{\ell,q}'(n) = s_{\ell,q}(n) * \mathbf{x}(n), \qquad \mathbf{x}(n) = [x(n), x(n-1), \ldots, x(n-N+1)], \tag{4}
$$

where $N$ is the filter length. The multiple-point ANC system aims to reduce $e_q^{(\mathrm{M})}(n)$ at the monitoring microphones themselves.

### PINN-assisted ANC System (Proposed)

A fully connected feed-forward network takes time $n$ and Cartesian coordinates $(\mathbf{x}, \mathbf{y}, \mathbf{z})$ as input and outputs the estimated primary signal $\hat{p}(n, \mathbf{x}, \mathbf{y}, \mathbf{z})$ at that point and time. The PINN minimizes a composite loss:

$$
\mathcal{L} = \underbrace{\frac{1}{Q}\sum_{q=1}^{Q}\bigl(\hat{p}(n_q, x_q, y_q, z_q) - p(n_q, x_q, y_q, z_q)\bigr)^2}_{\mathcal{L}_\text{data}} + \underbrace{\frac{1}{A}\sum_{a=1}^{A}\biggl(c^2 \nabla^2 \hat{p}(n_a, x_a, y_a, z_a) - \frac{\partial^2}{\partial n^2}\hat{p}(n_a, x_a, y_a, z_a)\biggr)^2}_{\mathcal{L}_\text{PDE}}, \tag{5}
$$

- $\mathcal{L}_\text{data}$: mean squared error between PINN estimate and ground truth at the $Q$ monitoring microphone positions.
- $\mathcal{L}_\text{PDE}$: residual of the acoustic wave equation at $A$ randomly selected collocation points around the ROI:

$$
\nabla^2 p - \frac{1}{c^2}\frac{\partial^2 p}{\partial t^2} = 0, \tag{6}
$$

where $\nabla^2 \equiv \partial^2/\partial x^2 + \partial^2/\partial y^2 + \partial^2/\partial z^2$ is the Laplacian, $\partial^2/\partial t^2$ is the second partial derivative with respect to time, and $c$ is the speed of sound. Partial derivatives are computed via TensorFlow automatic differentiation.

The trained PINN interpolates the primary signal at the virtual microphones, producing $e_v^{(\mathrm{V})}(n)$. The PINN-assisted ANC system replaces $e_q^{(\mathrm{M})}(n)$ in Eq. (3) with $e_v^{(\mathrm{V})}(n)$, driving the FxLMS update to reduce noise at the virtual (ear) positions rather than at the monitoring microphones.

### Spherical Harmonics Interpolation (Comparison Baseline)

Sound pressure on a sphere of radius $r$ is decomposed onto [[concepts/spherical-harmonic-transform|spherical harmonics]]:

$$
p(n, r, \theta_q, \phi_q) \approx \sum_{u=0}^{U}\sum_{v=-u}^{u} \alpha_{u,v}(n, r)\, Y_u^v(\theta_q, \phi_q), \tag{7}
$$

with maximum order $U = \lceil 2\pi f_\mathrm{m} r / c \rceil$ where $f_\mathrm{m}$ is the highest frequency of interest. Sound pressure at an arbitrary point $(r_s, \theta, \phi)$ is interpolated via radial extrapolation using spherical Bessel functions $j_u(\cdot)$:

$$
p_s(n, r_s, \theta, \phi) \approx \sum_{u=0}^{U}\sum_{v=-u}^{u} \alpha_{u,v}(n, r) * \mathcal{F}^{-1}\!\left[\frac{j_u(2\pi f_\mathrm{m} r_s / c)}{j_u(2\pi f_\mathrm{m} r / c)}\right] Y_u^v(\theta, \phi). \tag{8}
$$

Accurate SH estimation up to order $U$ requires $Q > (U+1)^2$ microphones; with $Q = 8$ the authors use $U = 2$.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Secondary sources $L$ | 2 at $(0, \pm 0.5, 0)$ m |
| Virtual microphones $V$ | 2 at $(0, \pm 0.1, 0)$ m (ear positions) |
| Monitoring microphones $Q$ | 8 on $r = 0.26$ m sphere at $(\pm 0.15, \pm 0.15, \pm 0.15)$ m |
| Primary source | Single, at $(0.6, 0.8, 1)$ m |
| Primary noise | Tonal: 300, 400, 500 Hz sinusoids with random phase |
| Speed of sound $c$ | 343 m/s |
| Sampling rate | 24 kHz |
| Signal duration | 0.1 s |
| Primary/secondary path model | Free-field Green's function |
| FxLMS step size $\mu$ | $1 \times 10^{-5}$ |
| FxLMS iterations | 10 000 |
| PINN hidden layers $L$ | 1 |
| PINN neurons per layer $N$ | 16 |
| PINN activation | tanh |
| PINN initializer | Glorot normal |
| PINN optimizer | Adam, lr = 0.001 |
| PINN training epochs | $5 \times 10^5$ |
| Collocation points $A$ | 100 (8 monitoring + 92 random in $r=0.26$ m sphere) |
| SH max order $U$ | 2 (closest fit to $Q > (U+1)^2$ with $Q=8$) |
| Interpolation evaluation | 400 uniform points per sphere, $r_s \in [0.1, 0.4]$ m |
| ANC evaluation grid | 441 points in xy-plane, $-0.2$ to $0.2$ m |

## Results

### Soundfield Interpolation Error

The normalized interpolation error at radius $r$ is

$$
\epsilon_r = \frac{\sum_{b=1}^{400}\bigl(p(n_b, x_b, y_b, z_b) - \hat{p}(n_b, x_b, y_b, z_b)\bigr)^2}{\sum_{b=1}^{400} p(n_b, x_b, y_b, z_b)^2}. \tag{9}
$$

For $r_s$ from 0.2 m to 0.4 m, the PINN method outperformed SH by approximately **8 dB** in interpolation error. The gap is smaller for $r_s < 0.2$ m, but PINN consistently achieves lower error. Because of this clear advantage, the authors omit ANC evaluation using SH-interpolated signals.

### ANC Noise Reduction

Noise reduction level at the two ear locations is defined as

$$
\varepsilon = \frac{\sum_{v=1}^{2} e_v^{(\mathrm{V})}(n)^2}{\sum_{v=1}^{2} p_v(n)^2}. \tag{10}
$$

Both ANC systems use FxLMS with $\mu = 1 \times 10^{-5}$ over 10 000 iterations. The initial noise power reduction rate in the first 500 iterations is similar for both systems, but the PINN-assisted ANC achieves **−13 dB more steady-state noise power reduction** than the multiple-point ANC system.

![[raw/papers/zhang-2024-active-noise-control-soundfield-interpolation-pinn/figures/e44aea7027cd1e8357c7f158954b3330cb77c3acf4b3c4cc528337e40be8c7ca.jpg|Noise power reduction at the two ear locations for multiple-point ANC vs. PINN-assisted ANC]]
*Figure 4: Noise power reduction at the two ear locations achieved by the multiple-point ANC and the PINN-assisted ANC system. The PINN-assisted system reaches approximately −13 dB lower steady-state residual noise.*

### Spatial Noise Field (xy-plane)

Evaluating signal power after FxLMS convergence on a 441-point grid in the xy-plane ($-0.2$ m to $0.2$ m):

- **Fig. 5(a)**: Original primary noise field.
- **Fig. 5(b)**: Residual noise power for the multiple-point ANC system.
- **Fig. 5(c)**: Residual noise power for the PINN-assisted ANC system.

In the dotted region (projection of monitoring microphones), the PINN-assisted ANC shows overall better noise reduction than the multiple-point ANC, with **−10 dB lower residual noise field around the two ear regions**. This is because the multiple-point ANC minimizes noise at the monitoring microphones (outside the ROI), whereas the PINN-assisted ANC minimizes noise at the virtual error microphones positioned at the two ears — directly inside the ROI.

## Key Contributions

1. **Practical monitoring microphone placement**: Microphones are placed outside the ROI, giving users more freedom of movement compared to spherical or circular array configurations required by SH-based methods.
2. **PINN-based soundfield interpolation**: The acoustic wave equation is integrated as a PDE residual loss, enabling accurate interpolation with a limited number of monitoring microphones.
3. **PINN-assisted ANC system**: The interpolated virtual microphone signals replace physical error microphone signals in the FxLMS update, achieving better noise reduction at the ear positions than a multiple-point ANC system canceling at monitoring microphones.
4. **Computationally efficient**: The PINN model uses a simple architecture (1 hidden layer, 16 neurons) compared to deep neural networks.
5. **PINN > SH**: PINN achieves ~8 dB lower interpolation error than SH at distances 0.2–0.4 m.

## Limitations and Future Work

The authors note the following planned extensions:

- Quantitative comparison with additional soundfield interpolation methods and evaluation of PINN's computational advantage.
- Extension to **spatial ANC** (creating a broader zone of quiet rather than just at the two ear positions).
- Replacement of the FxLMS controller with a **machine learning-based controller**, such as [[sources/zhang-2023-deep-mcanc|Deep MCANC]] or DNoiseNet.

## Related Concepts

- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/physics-informed-neural-network|Physics-Informed Neural Network]]
- [[concepts/soundfield-interpolation|Soundfield Interpolation]]
- [[concepts/spherical-harmonic-transform|Spherical Harmonic Transform]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/remote-microphone-technique|Remote Microphone Technique]]
- [[concepts/feedforward-anc|Feedforward ANC]]
- [[concepts/neural-networks|Neural Networks]]

## Related Synthesis

- [[synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in Active Noise Control]]
