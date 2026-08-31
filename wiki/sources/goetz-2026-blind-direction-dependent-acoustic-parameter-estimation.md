---
type: source
created: 2026-05-05
updated: 2026-05-05
sources:
  - raw/papers/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation/full-text.md
  - https://doi.org/10.1109/ICASSP55912.2026.11460445
  - zotero://select/items/0_H3HVNSBS
tags:
  - smart-glasses
  - acoustic-parameter-estimation
  - spherical-harmonics
  - beamforming
  - head-rotation
  - augmented-reality
---

# Görtz, Amengual, Calamia, Ananthabhotla, Francl, Schissler & Habets 2026: Blind Direction-Dependent Acoustic Parameter Estimation Using Smart Glasses

**Authors**: [[entities/philipp-goetz|Philipp Görtz]]¹, [[entities/sebastia-amengual|Sebastià V. Amengual]]², [[entities/paul-calamia|Paul Calamia]]², [[entities/ishwarya-ananthabhotla|Ishwarya Ananthabhotla]]², [[entities/andrew-francl|Andrew Francl]]², [[entities/carl-schissler|Carl Schissler]]², [[entities/emanuel-habets|Emanuel A. P. Habets]]¹

**Affiliations**: ¹ Friedrich-Alexander University Erlangen-Nuremberg, Germany · ² Meta Reality Labs, Redmond, WA, USA

**Published**: ICASSP 2026 — IEEE International Conference on Acoustics, Speech and Signal Processing, pp. 22187–22191

**Type**: Conference Paper

**DOI**: [10.1109/ICASSP55912.2026.11460445](https://doi.org/10.1109/ICASSP55912.2026.11460445)

**Zotero**: [H3HVNSBS](zotero://select/items/0_H3HVNSBS)

## Summary

Proposes the first multimodal method for blind [[concepts/direction-dependent-acoustic-parameters|direction-dependent acoustic parameter]] (DDAP) estimation using smart glasses. A dual-network architecture — convolutional encoder + transformer aggregation with FiLM conditioning — exploits natural head rotations to overcome the limited spatial resolution of compact microphone arrays. Validated on direction-dependent decay time T₂₀ and directional acoustic energy E across four octave bands, achieving PCC of 0.82 at 0.5 kHz for T₂₀ and 0.92 for E.

## Problem Formulation

The core challenge: existing blind acoustic parameter estimation methods neglect the **spatial or directional dependency** of parameters like reverberation time and energy. This dependency is essential for realistic spatial audio rendering of virtual sources in [[concepts/auditory-augmented-reality|auditory augmented reality]] (AAR), particularly in domestic environments with non-uniform absorption and anisotropic energy decay.

Wearable devices with compact microphone arrays suffer from **limited spatial resolution and directional ambiguities**, making DDAP estimation from reverberant signals challenging. The key insight: natural head rotations during AAR use can be exploited to aggregate spatial information across multiple viewing orientations.

**Signal model**: A reverberant sound field from a single active source $S$ captured by $K$ microphones:

$$\mathbf{x}[n] = \sum_{n'=0}^{N_h-1} \mathbf{h}[n'] s[n-n'] \in \mathbb{R}^K$$

where $\mathbf{h}[n]$ is the array room impulse response (RIR) and $s[n]$ is the anechoic source signal.

**Target parameters**: Direction-dependent decay time $\mathrm{T}_{20}(\boldsymbol{\theta})$ and directional acoustic energy $E(\boldsymbol{\theta})$, estimated in the [[concepts/spherical-harmonic-transform|spherical harmonic]] domain up to order $L$.

## Methodology

### Ground Truth Computation

DDAPs are computed in four octave bands with center frequencies [0.5, 1, 2, 4] kHz. A maximum radial energy ($\max\text{-}\mathbf{r}_E$) [[concepts/beamforming|beamformer]] is oriented towards each control direction $\boldsymbol{\theta}_j$ in a spherical 15th-order $t$-design to obtain the directional RIR:

$$h_{\boldsymbol{\theta}_j}[n] = \sum_{l=0}^{L} \sum_{m=-l}^{l} w_l Y_{lm}(\boldsymbol{\theta}_j) \mathbf{h}_{lm}^{(\circ)}[n]$$

where $w_l$ are the $\max\text{-}\mathbf{r}_E$ modal weights. The directional energy decay curve is:

$$\mathrm{EDC}_{\boldsymbol{\theta}_j}[n] = 10\log_{10}\left(\frac{\sum_{n'=n}^{N-1} h_{\boldsymbol{\theta}_j}^2[n']}{\sum_{n'=0}^{N-1} h_{\boldsymbol{\theta}_j}^2[n']}\right)$$

from which $\mathrm{T}_{20}$ is extracted (decay from −5 to −25 dB, extrapolated to 60 dB). Directional energy:

$$E(\boldsymbol{\theta}_j) = 10\log_{10}\left(\frac{1}{N}\sum_{n=0}^{N-1} h_{\boldsymbol{\theta}_j}^2[n]\right)$$

$\mathrm{T}_{20}$ is preferred over $\mathrm{T}_{60}$ because it exhibits substantially stronger directional dependence — the sound field becomes more diffuse and isotropic over time.

### Orientation-Aware Estimation Architecture

![Overview of the proposed method](raw/papers/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation/figures/99e61fdae5a49e6cffeecf003dcabaea8bcb96b9d7ad453287ae1cc06b28ecdd.jpg)
*Figure 3: Overview of the proposed method — encoder extracts spatial embeddings from reverberant signals; aggregation module estimates DDAPs from the embedding set conditioned on orientation.*

**Input features**: For each time-frequency bin, inter-channel phase differences (sine/cosine encoded) are stacked with magnitude-compressed signals to form $\mathbf{V} \in \mathbb{R}^{C \times F \times N_f}$ where $C = K + 2(K-1)$. Each $\mathbf{V}$ is associated with a device orientation via rotation matrix $\mathbf{R}(\alpha, \beta, \gamma)$ and unit quaternion $\mathbf{q}(\mathbf{R}) \in \mathbb{R}^4$.

**Encoder** $\mathcal{E}$ (676,288 parameters): Convolutional layers extract local spatio-temporal features → attention-based temporal pooling → fixed-size embedding $\mathbf{z} \in \mathbb{R}^D$.

**Aggregation model** $\mathcal{F}$ (294,992 parameters): Transformer encoder processes the set $\mathcal{I} = \{\mathbf{z}_i \mid \mathbf{q}(\mathbf{R}_i)\mathbf{q}(\mathbf{R}_1)^{-1}\}_{i=1}^I$ of orientation-conditioned embeddings via **Feature-wise Linear Modulation (FiLM)**. Positional encoding is omitted to treat embeddings as an unordered set. A random anchor $\mathbf{q}(\mathbf{R}_1)$ is selected during training; all other orientations are expressed relative to it.

**Loss function**: MSE in the spatial domain over control directions $\mathcal{J}$:

$$\mathcal{L} = \sum_{j \in \mathcal{J}} \left\| \sum_{l=0}^{L} \sum_{m=-l}^{l} \widehat{\Gamma}_{lm} Y_{lm}(\boldsymbol{\theta}_j) - \overline{\Gamma}(\boldsymbol{\theta}_j) \right\|_2^2$$

Estimating DDAPs in the SH domain yields a compact, continuous representation evaluable at arbitrary angles, with $L$ controlling spatial resolution.

## Experimental Setup

| Aspect | Configuration |
|--------|--------------|
| **Device** | Smart glasses with 5 built-in microphones |
| **RIR generation** | Measured anechoic transfer functions + Treble Acoustics simulated spatial RIRs |
| **Environments** | 400 simulated (280 train / 60 val / 60 test) |
| **Source-receiver distance** | ≥ 0.5 m from each other and boundaries |
| **Orientation sampling** | $\alpha_0 \sim \mathcal{U}[0, 2\pi]$, $\beta_0 \sim \mathcal{U}[-\pi/4, \pi/4]$, $\gamma_0 = 0$; offsets $\alpha \sim \mathcal{U}[-\pi/2, \pi/2]$, $\beta \sim \mathcal{U}[-\pi/8, \pi/8]$, $\gamma \sim \mathcal{U}[-\pi/12, \pi/12]$ |
| **Speech data** | EARS dataset anechoic recordings, ~34 hours |
| **Sampling rate** | 16 kHz |
| **Octave bands** | [0.5, 1, 2, 4] kHz |
| **SH orders** | $L \in \{1, 2, 3, 4\}$ |
| **Total parameters** | 971,280 (encoder: 676,288 + aggregation: 294,992) |

## Results

### T₂₀ Estimation (MAPE, median [IQR])

| SH Order | 0.5 kHz | 1 kHz | 2 kHz | 4 kHz |
|----------|---------|-------|-------|-------|
| L=1 | 20.0 (20.6) | 28.3 (27.3) | 30.0 (30.4) | 34.2 (49.5) |
| L=2 | 18.4 (16.3) | 24.7 (20.6) | 28.9 (31.1) | 33.8 (33.3) |
| L=3 | 17.9 (13.0) | 25.6 (20.9) | 30.9 (30.5) | 34.8 (31.4) |
| L=4 | 16.4 (13.3) | 25.4 (18.6) | 29.6 (26.8) | 31.3 (27.2) |

### E Estimation (MAE, mean ± std)

| SH Order | 0.5 kHz | 1 kHz | 2 kHz | 4 kHz |
|----------|---------|-------|-------|-------|
| L=1 | 1.71 ± 0.96 | 1.94 ± 0.75 | 2.26 ± 0.84 | 2.60 ± 0.90 |
| L=2 | 1.70 ± 0.87 | 1.82 ± 0.70 | 2.25 ± 0.80 | 2.68 ± 0.96 |
| L=3 | 1.85 ± 0.91 | 2.06 ± 0.93 | 2.40 ± 0.87 | 2.94 ± 1.13 |
| L=4 | 2.16 ± 1.15 | 2.53 ± 1.21 | 2.68 ± 1.13 | 3.31 ± 1.41 |

### Pearson Correlation Coefficient (PCC)

| SH Order | T₂₀ 0.5 kHz | T₂₀ 1 kHz | T₂₀ 2 kHz | T₂₀ 4 kHz | E 0.5 kHz | E 1 kHz | E 2 kHz | E 4 kHz |
|----------|-------------|-----------|-----------|-----------|-----------|---------|---------|---------|
| L=1 | 0.82 | 0.73 | 0.60 | 0.62 | 0.90 | 0.89 | 0.86 | 0.84 |
| L=2 | 0.81 | 0.73 | 0.64 | 0.64 | 0.92 | 0.90 | 0.86 | 0.83 |
| L=3 | 0.83 | 0.73 | 0.64 | 0.62 | 0.90 | 0.89 | 0.83 | 0.82 |
| L=4 | 0.79 | 0.68 | 0.58 | 0.58 | 0.86 | 0.85 | 0.79 | 0.77 |

**Key findings**:
- T₂₀ MAPE decreases with increasing SH order (better absolute accuracy at higher $L$), but PCC also decreases (worse directional pattern capture at higher $L$)
- E estimation achieves higher PCC than T₂₀ across all bands, with best performance at L=2 (PCC 0.92 at 0.5 kHz)
- Higher SH orders $L$ increase estimation error for $E$ due to more coefficients to estimate from limited spatial information
- L=1–2 offers the best tradeoff between spatial resolution and estimation accuracy

## Key Contributions

1. **First multimodal approach for blind DDAP estimation** using a wearable device, combining acoustic and orientation (IMU) information
2. **Head rotation exploitation**: Aggregating spatial information across multiple viewing orientations overcomes the limited spatial resolution of compact arrays
3. **SH domain estimation**: DDAPs are estimated as spherical harmonic coefficients, yielding a compact, continuous representation evaluable at arbitrary angles with controllable spatial resolution via $L$
4. **Dual-network architecture**: Encoder–aggregation framework with FiLM-conditioned transformer that processes orientation-conditioned embeddings as an unordered set
5. **Joint octave-band estimation**: All four octave bands estimated simultaneously using all five microphones

## Related Concepts

- [[concepts/direction-dependent-acoustic-parameters|Direction-Dependent Acoustic Parameters]] — the core estimation target
- [[concepts/spherical-harmonic-transform|Spherical Harmonic Transform]] — mathematical framework for spatial representation
- [[concepts/auditory-augmented-reality|Auditory Augmented Reality]] — application domain motivating DDAP estimation
- [[concepts/beamforming|Beamforming]] — max-rE beamformer used for ground truth computation
- [[concepts/head-orientation-from-imu|Head Orientation from IMU]] — orientation information exploited by the aggregation module
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]] — related spatial estimation task
- [[concepts/inertial-measurement-unit|Inertial Measurement Unit]] — source of head orientation data

## Related Synthesis

- [[synthesis/modern-headphone-anc-systems|Modern Headphone ANC Systems]] — smart glasses as wearable audio platform
