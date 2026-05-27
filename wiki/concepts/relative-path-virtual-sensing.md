---
type: concept
created: 2026-05-27
updated: 2026-05-27
tags:
  - active-noise-control
  - virtual-sensing
  - multi-channel
  - feedforward
---

# Relative Path Virtual Sensing

**Relative Path Virtual Sensing (RP-VS)** is a virtual sensing method for active noise control that estimates both the disturbance signal and the anti-noise signal at the target zone of quiet (ZoQ) using two separately trained relative path models — a relative primary path $C_p(z)$ and a relative secondary path $C_s(z)$.

## Formulation

### Relative Path Models

During a tuning stage (temporal microphones placed at the target ZoQ), two relative path models are estimated:

**Relative primary path** — maps disturbance from monitoring mic to virtual mic:

$$C_p(z) = \frac{P_v(z)}{P_m(z)}$$

**Relative secondary path** — maps anti-noise from monitoring mic to virtual mic:

$$C_s(z) = \frac{S_v(z)}{S_m(z)}$$

### Control Stage Estimation

In the control stage (temporal microphones removed), the virtual error signal is estimated as:

$$\widehat{E}_{v'}(z) = C_p(z) \widehat{D}_{m'}(z) + C_s(z) S_{m'}(z) Y'(z)$$

### Converged Control Filter

$$W_{RP}(z) = -\frac{C_p(z) P_{m'}(z)}{C_s(z) S_{m'}(z)}$$

### Multi-Channel Extension

For a system with $I$ reference, $J$ secondary, $K$ monitoring, and $L$ virtual channels:

$$\mathbf{W}_{RP}(z) = \left[\mathbf{S}_{m'}^{(K \times J)}\right]^\dagger \mathbf{S}_m^{(K \times J)} \mathbf{W}_o^{(J \times I)} \left[\mathbf{P}_m^{(K \times I)}\right]^\dagger \mathbf{P}_{m'}^{(K \times I)}$$

## Relationship to Other VS Methods

| Condition | RP-VS degenerates to |
|-----------|---------------------|
| Invariant secondary paths ($S_{m'} = S_m$) | [[concepts/remote-microphone-technique\|RM-VS]] ($W_{RP} \to W_{RM}$) |
| Invariant primary paths ($P_{m'} = P_m$) | AF-VS ($W_{RP} \to W_{AF}$) |
| No path changes | Optimal solution $W_o$ |

## Advantages

- **Robust to primary path changes**: Behaves like RM-VS under secondary path invariance
- **Robust to secondary path changes**: Behaves like AF-VS under primary path invariance
- **Best average performance under all-paths-varying**: When both primary and secondary paths change, RP-VS outperforms both AF-VS and RM-VS
- **Robust to varying noise frequency bands**: RP-VS produces control filters with closest phase response to optimal across different testing bands

## Limitations

- Requires training of two relative path models (vs. one for RM-VS)
- Performance in multi-channel systems is more sensitive due to cross-channel acoustic path errors
- Effectiveness cannot be guaranteed under arbitrary path changes — balanced relative path changes are needed

## Related Concepts

- [[concepts/virtual-sensing|Virtual Sensing]]
- [[concepts/remote-microphone-technique|Remote Microphone Technique]]
- [[concepts/multi-channel-anc|Multi-Channel ANC]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/active-noise-control|Active Noise Control]]

## Related Sources

- [[sources/shi-2020-active-noise-control-casing-virtual-sensing|Shi, Jia, Xie & Li 2020: ANC Casing with RP-VS]]
