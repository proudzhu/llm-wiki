---
type: source
created: 2026-10-21
updated: 2026-10-21
sources:
  - raw/papers/peled-2026-anc-ar-glasses-directional-robustness/full-text.md
  - https://www.eurasip.org/Proceedings/Eusipco/Eusipco2026/pdfs/0000966.pdf
  - zotero://select/items/0_X5D9KRGJ
tags:
  - active-noise-control
  - virtual-sensing
  - augmented-reality
  - directional-robustness
---

# Peled & Rafaely 2026: ANC for AR Glasses with Directional Robustness

**Authors**: [[entities/nitay-peled|Nitay Peled]], [[entities/boaz-rafaely|Boaz Rafaely]]
**Institution**: School of Electrical and Computer Engineering, Ben-Gurion University of the Negev, Beer-Sheva, Israel
**Venue**: EUSIPCO 2026
**Year**: 2026
**Type**: Conference paper
**URL**: https://www.eurasip.org/Proceedings/Eusipco/Eusipco2026/pdfs/0000966.pdf
**Zotero**: [X5D9KRGJ](zotero://select/items/0_X5D9KRGJ)

## Summary

This paper applies virtual sensing ANC to augmented reality (AR) glasses, where no physical error microphone exists at the wearer's ear. Using the Auxiliary Filter (AF) method with microphone positions taken from the Project Aria glasses geometry, the authors derive a theoretical sensitivity analysis showing that the optimal AF is least sensitive to noise direction-of-arrival (DOA) changes along the reference–monitor axis, and confirm the prediction in free-field simulations. To mitigate DOA mismatch, they propose selecting the AF from a finite bank of filters calibrated at uniformly spaced DOAs — a bank of just 5 filters recovers mean attenuation to within 3.7 dB of per-DOA full calibration, offering a practical alternative to continuous recalibration.

## Problem Formulation

AR glasses can host microphones and loudspeakers on the frame, but typically have **no microphone at the ear** where the quiet zone is desired. Additionally, frame-fixed microphones introduce a **causality issue**: for source directions where the wavefront reaches the ear before the frame microphone, the required controller is non-causal and all algorithms degrade.

The ANC system uses a reference microphone, a monitoring microphone (on the frame above the ear, as in the Project Aria design), a control loudspeaker, and a virtual microphone at the ear (physical only during training, inaccessible during control). The virtual microphone signal in the frequency domain is:

$$
E_v(\omega) = P_v(\omega) X(\omega) + S_v(\omega) W(\omega) X(\omega)
$$

where $X(\omega)$ is the reference signal, $P_v(\omega)$ and $S_v(\omega)$ are the virtual primary and secondary paths, and $W(\omega)$ is the control filter.

## Methodology

### Auxiliary Filter Method

During control, the controller is adapted with a modified FxLMS algorithm using the error signal:

$$
E_h(\omega) = E_m(\omega) - H(\omega) X(\omega)
$$

where $H(\omega)$ is the auxiliary filter trained during calibration (via LMS, following [[sources/shi-2020-active-noise-control-casing-virtual-sensing|Shi et al. 2020]]). The optimal AF is:

$$
H_0(\omega) = P_m(\omega) - \frac{S_v(\omega)}{S_m(\omega)} P_v(\omega)
$$

With the optimal AF, $E_h(\omega)$ tends to zero when the control filter converges to the optimum $W_0(\omega) = -P_v(\omega)/S_v(\omega)$ that minimizes the error at the virtual microphone. The adaptation reference is prefiltered with an estimate of the virtual secondary path.

![[raw/papers/peled-2026-anc-ar-glasses-directional-robustness/figures/09f248babab91e321f2c39df1ee1a19dd9749118fe31923139cbf81ab7153a46.jpg|Block diagram of the ANC system including the AF]]
*Figure 1: Block diagram of the ANC system including the AF.*

![[raw/papers/peled-2026-anc-ar-glasses-directional-robustness/figures/0670fdb03cc6014bb15896305ae10df0ab79489dd3077e23682cdc0608214326.jpg|AR glasses setup with microphones, primary and secondary sources]]
*Figure 2: AR glasses setup illustrating the positions of the microphones, along with the primary and secondary sources.*

### Theoretical DOA Sensitivity Analysis

Under a free-field model with point sources and plane-wave approximation of the primary disturbance (source at 3 m), the optimal AF becomes:

$$
H_0(\omega, \phi) = e^{-j\frac{\omega}{c} d_m \cos(\phi_m)} - G(\omega)\, e^{-j\frac{\omega}{c} d_v \cos(\phi_v)}
$$

where $G(\omega) = S_v(\omega)/S_m(\omega)$, and $\phi_m$, $\phi_v$ are the source angles relative to the reference–monitor and reference–virtual axes. Assuming the monitor sits above the ear ($\phi_m \approx \phi_v$) and $|d_v - d_m|$ is small relative to wavelength, the derivative magnitude simplifies to:

$$
\left| \frac{\partial H_0}{\partial \phi} \right| \approx |F(\omega)|\, |\sin(\phi - \phi_0)|, \qquad |F(\omega)| = \frac{\omega}{c} \left| d_m - G(\omega) d_v \right|
$$

**Prediction**: the AF is *least* sensitive to DOA changes at $\phi = \phi_0$ (the reference–monitor axis) and *most* sensitive at $\phi = \phi_0 + 90°$. A fixed AF calibrated on-axis should therefore tolerate wider DOA mismatch than one calibrated off-axis.

### Finite AF Bank

As a practical alternative to per-DOA recalibration, a **bank of AFs** is calibrated at uniformly spaced DOAs within the causal range $[\phi_0 - 90°, \phi_0 + 90°]$. During control, the AF closest in calibration DOA to the estimated noise-source direction is selected.

## Experimental Setup

| Parameter | Value |
|-----------|-------|
| Geometry | Project Aria glasses microphone positions (CHiME-8 MMCSG specs) |
| Environment | Free-field simulation, point sources, source distance 3 m |
| Virtual microphone | At the ear location |
| Sampling rate | 24 kHz |
| Noise signal | Gaussian white noise, band-limited 100–800 Hz (4th-order Butterworth) |
| Adaptive algorithm | Normalized FxLMS (NFxLMS) |
| Filter length | 256-coefficient FIR, zero-initialized |
| AF calibration | LMS, then fixed during control |
| Step sizes | $\mu \in \{10^{-4}, 10^{-3}, 10^{-2}, 10^{-1}\}$ (best reported) |
| Secondary path estimate | Assumed perfectly known |
| Realization length | 5 s per azimuth; attenuation over last 15% (steady state) |

![[raw/papers/peled-2026-anc-ar-glasses-directional-robustness/figures/a74f442a0a1155df562f67435eb9f3103fe378541219de9f5222e986591d6147.jpg|Project Aria glasses geometric layout with loudspeaker and virtual microphone]]
*Figure 3: Geometric layout based on the Project Aria glasses geometry, including the loudspeaker and virtual microphone (coordinates in cm).*

## Results

### Necessity of the Virtual Microphone

Comparing (i) monitor-based NFxLMS, (ii) virtual-based NFxLMS (ground truth), and (iii) AF control calibrated per azimuth: the large gap between monitor-based and virtual-based NFxLMS confirms a virtual sensing technique is **necessary**; the AF method nearly bridges the gap. Attenuation is approximately symmetric around $\phi_0 \approx 327°$, where the reference-to-monitor propagation delay is maximal (favorable causality). Beyond $\pm 90°$ from $\phi_0$ the noise reaches the monitor/virtual microphone before the reference, requiring a non-causal controller — all algorithms degrade there.

![[raw/papers/peled-2026-anc-ar-glasses-directional-robustness/figures/e8eb8c92a9ba7a4789b01cd1157ed5bb49258a8d5acc4b7eb2738069e61930e3.jpg|Polar plot: monitor NFxLMS vs virtual NFxLMS vs per-DOA AF control]]
*Figure 4: Attenuation at the virtual microphone vs source azimuth — monitor-based NFxLMS, virtual NFxLMS, and AF control calibrated separately for each azimuth.*

### AF Sensitivity to DOA Mismatch

Applying an AF calibrated at a single DOA to other DOAs: the angular region of near-fully-calibrated performance is wider for the AF calibrated at $\phi_0$ than for one calibrated at $\phi_0 + 60°$ (caption: comparisons at $\phi_0$, $\phi_0 + 30°$, $\phi_0 + 70°$) — consistent with the $|\sin(\phi - \phi_0)|$ sensitivity prediction.

![[raw/papers/peled-2026-anc-ar-glasses-directional-robustness/figures/ffbb7f5660f48db6a40fe84d83a0a1645c080772a8d3e1e307fbc583b3f992a2.jpg|Polar plot: fixed AF calibrated at different DOAs vs per-DOA calibration]]
*Figure 5: Attenuation vs azimuth — AF calibrated per-DOA vs a single fixed AF calibrated at $\phi_0$, $\phi_0 + 30°$, or $\phi_0 + 70°$.*

### Finite AF Bank

Selecting the AF from a finite bank significantly improves over a single fixed AF. Mean attenuation over the causal range $\phi_0 \pm 90°$:

| AF Bank Size | Mean Attenuation [dB] | Gap to Fully Calibrated [dB] |
|--------------|----------------------|------------------------------|
| 3 | 22.7 | 6.3 |
| 4 | 24.0 | 5.0 |
| 5 | 25.3 | 3.7 |
| 6 | 26.0 | 3.0 |
| 7 | 26.5 | 2.5 |
| Fully calibrated | 29.1 | 0 |

![[raw/papers/peled-2026-anc-ar-glasses-directional-robustness/figures/970d6a8ed392e7cdb48dde3b949021bb0e52537068bd6070a9a6cc894f01f249.jpg|Polar plot: AF bank of size 5 vs fully calibrated AF]]
*Figure 6: Attenuation vs azimuth — AF selected from a finite bank of size 5 vs fully calibrated per-DOA AF control.*

## Key Contributions

1. **Necessity of virtual sensing for AR glasses**: first demonstration (in simulation, Project Aria geometry) that monitor-based ANC falls far short of ear-position attenuation, establishing virtual sensing as a requirement for AR-glasses ANC.
2. **Theoretical DOA sensitivity framework**: closed-form analysis showing the optimal AF's sensitivity to noise DOA is proportional to $|\sin(\phi - \phi_0)|$ — minimal along the reference–monitor axis, maximal at $\pm 90°$ — enabling prediction of fixed-AF robustness before deployment; validated by simulation.
3. **Finite AF bank strategy**: DOA-based selection from a bank of pre-calibrated AFs recovers most of the per-DOA calibration performance (bank of 5: within 3.7 dB averaged over the causal range), a practical alternative to continuous recalibration in dynamic acoustic environments.

## Limitations

- Single-channel, single noise source, free-field simulation only — reverberation, multiple sources, and multichannel control are left for future work.
- The AF bank requires knowledge of the noise-source DOA during control.
- Secondary path assumed perfectly known; no processing or hardware delay modeled.

## Related Concepts

- [[concepts/anc-for-ar-glasses|ANC for AR Glasses]]
- [[concepts/auxiliary-filter-virtual-sensing|Auxiliary Filter Virtual Sensing (AF-VS)]]
- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/relative-path-virtual-sensing|Relative Path Virtual Sensing]]
- [[concepts/primary-path-variability|Primary Path Variability]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/auxiliary-filter|Auxiliary Filter (SEM)]] — distinct simultaneous-equations sense of "auxiliary filter"

## Related Synthesis

- [[synthesis/virtual-sensing-evolution|Evolution of Virtual Sensing in ANC]]

## Related Sources

- [[sources/shi-2020-active-noise-control-casing-virtual-sensing|Shi, Jia, Xie & Li 2020: ANC Casing with RP-VS]] — basis of the AF method and calibration procedure used here
- [[sources/xiao-2023-spatially-selective-anc|Xiao, Xu & Zhao 2023: Spatially Selective ANC]] — prior AR-glasses ANC simulation, relied on binaural error microphones
- [[sources/wang-2024-metric-learning-virtual-sensing|Wang 2024: Transferable Selective Virtual Sensing Based on Metric Learning]] — bank-of-AFs lineage for condition-varying VS
- [[sources/lu-2021-survey-active-noise-control-linear|Lu et al. 2021: Survey on ANC Part I]] — general ANC background
