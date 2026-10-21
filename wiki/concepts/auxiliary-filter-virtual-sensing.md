---
type: concept
created: 2026-10-21
updated: 2026-10-21
sources:
  - raw/papers/peled-2026-anc-ar-glasses-directional-robustness/full-text.md
tags:
  - active-noise-control
  - virtual-sensing
  - adaptive-filtering
---

# Auxiliary Filter Virtual Sensing (AF-VS)

**Auxiliary Filter Virtual Sensing (AF-VS)** is a virtual sensing method for feedforward [[concepts/active-noise-control|ANC]] in which an auxiliary filter $H(\omega)$, trained during a calibration stage, corrects the *physical* monitoring microphone's error signal so that a standard FxLMS update converges to the control filter that is optimal at the *virtual* microphone (the location without a physical sensor, e.g., the wearer's ear).

Not to be confused with the "auxiliary filter" of the [[concepts/auxiliary-filter|Simultaneous Equations Method]] — a different ANC concept sharing the same name.

## Formulation

The system comprises a reference microphone, a monitoring microphone, a control loudspeaker, and a virtual microphone (physical only during training). During control, the adaptation error signal is:

$$
E_h(\omega) = E_m(\omega) - H(\omega) X(\omega)
$$

The **optimal auxiliary filter** is:

$$
H_0(\omega) = P_m(\omega) - \frac{S_v(\omega)}{S_m(\omega)} P_v(\omega)
$$

where $P_m, S_m$ are the primary/secondary paths to the monitoring microphone and $P_v, S_v$ those to the virtual microphone. With $H = H_0$, $E_h$ tends to zero exactly when the control filter converges to the virtual-optimal $W_0(\omega) = -P_v(\omega)/S_v(\omega)$. The AF is typically calibrated with the LMS algorithm and then fixed during control ([[sources/shi-2020-active-noise-control-casing-virtual-sensing|Shi et al. 2020]]).

Within the [[concepts/relative-path-virtual-sensing|RP-VS]] framework, AF-VS is the degenerate case under **invariant primary paths** — effective when the primary paths do not change between calibration and control, and (unlike RM-VS) able to leverage online secondary path modeling.

## Directional Sensitivity

[[sources/peled-2026-anc-ar-glasses-directional-robustness|Peled & Rafaely 2026]] derived the sensitivity of the optimal AF to noise-source DOA $\phi$ under a free-field, plane-wave model:

$$
\left| \frac{\partial H_0}{\partial \phi} \right| \approx \frac{\omega}{c} \left| d_m - G(\omega) d_v \right| \cdot |\sin(\phi - \phi_0)|
$$

where $d_m, d_v$ are the reference–monitor and reference–virtual distances, $G = S_v/S_m$, and $\phi_0$ is the reference–monitor axis angle. Sensitivity is **minimal at $\phi = \phi_0$** and maximal at $\phi_0 \pm 90°$: a fixed AF calibrated on-axis tolerates wider DOA mismatch than one calibrated off-axis (validated in simulation: the near-calibrated performance region is wider for the AF calibrated at $\phi_0$ than at $\phi_0 + 60°$).

## AF Bank for DOA Robustness

To mitigate DOA mismatch without per-DOA recalibration, a **finite bank of AFs** is calibrated at uniformly spaced DOAs within the causal range $[\phi_0 - 90°, \phi_0 + 90°]$; during control the AF whose calibration DOA is closest to the estimated noise direction is selected. In free-field AR-glasses simulation (Project Aria geometry, 100–800 Hz): bank of 3 → 22.7 dB, 5 → 25.3 dB, 7 → 26.5 dB mean attenuation, vs 29.1 dB for full per-DOA calibration — a 5-filter bank recovers most of the performance. This connects to the broader lineage of bank/selection-based VS techniques (selective VS, cognitive VS, metric-learning transferable VS).

## Related Concepts

- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/relative-path-virtual-sensing|Relative Path Virtual Sensing]]
- [[concepts/remote-microphone-technique|Remote Microphone Technique]]
- [[concepts/anc-for-ar-glasses|ANC for AR Glasses]]
- [[concepts/primary-path-variability|Primary Path Variability]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/auxiliary-filter|Auxiliary Filter (SEM)]] — namesake, different concept

## Related Sources

- [[sources/peled-2026-anc-ar-glasses-directional-robustness|Peled & Rafaely 2026: ANC for AR Glasses with Directional Robustness]] — DOA sensitivity theory and AF bank
- [[sources/shi-2020-active-noise-control-casing-virtual-sensing|Shi, Jia, Xie & Li 2020: ANC Casing with RP-VS]] — calibration procedure and RP-VS unification
- [[sources/wang-2024-metric-learning-virtual-sensing|Wang 2024: Transferable Selective Virtual Sensing Based on Metric Learning]] — bank-of-AFs selection lineage
