---
type: concept
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/li-2020-geometrically-constrained-iva/full-text.md
  - raw/papers/li-2020-online-gciva/full-text.md
  - raw/papers/goto-2022-iss-gciva/full-text.md
tags:
  - blind-source-separation
  - independent-vector-analysis
  - beamforming
  - speech-enhancement
  - direction-of-arrival
  - online-processing
---

# Geometrically Constrained IVA

**Geometrically Constrained Independent Vector Analysis (GCIVA)** augments the [[concepts/independent-vector-analysis|IVA]] blind-separation objective with linear constraints on the far-field responses of the demixing filters, steering the otherwise blind separation toward desired spatial directions. It merges the high separation performance of [[concepts/blind-source-separation|blind source separation]] with the directional focus of [[concepts/beamforming|beamforming]]: the demixing filter's response toward a chosen direction can be forced toward unity (distortionless, delay-and-sum-like) or toward zero (a spatial null / blocking-matrix behavior).

## Key Formulations

The constraint (from the geometric source separation framework of Parra & Alvino 2002, the same linear-constraint family as the [[concepts/lcmv-beamformer|LCMV beamformer]]) penalizes the deviation of the $j$-th demixing filter's far-field response from a target value $c_j$:

$$
\mathcal{J}_c(\mathcal{W}) = \sum_{j=1}^{J} \lambda_j \sum_{\omega=1}^{\Omega} \left| \boldsymbol{w}_j^{\mathsf{H}}(\omega)\, \boldsymbol{d}_j(\omega,\theta) - c_j \right|^2,
$$

added to the standard IVA objective: $J(\mathcal{W}) = J_{\mathrm{IVA}}(\mathcal{W}) + \mathcal{J}_c(\mathcal{W})$. Here $\boldsymbol{d}_j(\omega,\theta)$ is the steering vector at direction $\theta$, $\lambda_j$ the constraint weight, and $c_j$ the target response ($c_j = 1$: distortionless; $c_j \approx 0$: null).

### GCAV-IVA Algorithm

The linear constraints break the Hybrid Exact-Approximate joint Diagonalization solvability of the AuxIVA stationarity equation, so [[sources/li-2020-geometrically-constrained-iva|Li & Koishida 2020]] derive the **GCAV-IVA** algorithm: an auxiliary-function (majorize-minimize) optimization with closed-form per-row updates obtained via the vectorwise-coordinate-descent cofactor expansion (Mitsui et al. 2018). With $\boldsymbol{D}_j = \boldsymbol{V}_j + \lambda_j \boldsymbol{d}_j \boldsymbol{d}_j^{\mathsf{H}}$ (where $\boldsymbol{V}_j$ is the AuxIVA weighted covariance):

$$
\boldsymbol{u}_j = \boldsymbol{D}_j^{-1}\boldsymbol{W}^{-1}\boldsymbol{e}_j, \quad
\hat{\boldsymbol{u}}_j = \lambda_j c_j \boldsymbol{D}_j^{-1}\boldsymbol{d}_j, \quad
h_j = \boldsymbol{u}_j^{\mathsf{H}}\boldsymbol{D}_j\boldsymbol{u}_j, \quad
\hat{h}_j = \boldsymbol{u}_j^{\mathsf{H}}\boldsymbol{D}_j\hat{\boldsymbol{u}}_j,
$$

$$
\boldsymbol{w}_j = \frac{\hat{h}_j}{2h_j}\left[-1 + \sqrt{1 + \frac{4h_j}{|\hat{h}_j|^2}}\right]\boldsymbol{u}_j + \hat{\boldsymbol{u}}_j
\quad (\text{and } \boldsymbol{w}_j = \tfrac{1}{\sqrt{h_j}}\boldsymbol{u}_j + \hat{\boldsymbol{u}}_j \text{ when } \hat{h}_j = 0).
$$

This inherits AuxIVA's guaranteed monotonic convergence and requires no step-size tuning — addressing the two practical drawbacks of the earlier gradient-based geometrically constrained IVA of Khan et al. (2015), which also needed a relatively large microphone array. GCAV-IVA reduces exactly to AuxIVA when $\lambda_j = 0$.

### Dual-Microphone System

With only two microphones, null constraints ($c_j \approx 0$) are practical:

- The **interference channel** is nulled toward the (known) target DOA, producing an interference/noise reference.
- The **target channel** is nulled toward an interference DOA estimated by a separate standard AuxIVA run, whose directivity-pattern nulls point at the source directions:
  $\hat{\theta}_j = \operatorname{argmin}_\theta \sum_{\omega \le \Omega/2} |\boldsymbol{w}_j^{\mathsf{H}}(\omega)\boldsymbol{d}(\omega,\theta)|$.

On VCC2018 speech with image-method RIRs (RT60 200/470 ms), DEMAND diffuse noise, and a 5 cm two-microphone array, this dual-mic GCAV-IVA system outperformed both an [[concepts/mpdr-beamformer|MPDR beamformer]] and oracle-channel-selected AuxIVA in SDR/SIR (e.g., 8.80 dB SDR / 11.69 dB SIR vs. AuxIVA's 7.12 / 8.98 in the 2-speaker, 200 ms condition). Constraining both channels beat constraining one, and the AuxIVA-estimated interference DOA slightly outperformed the oracle DOA.

### Online Extension (oGCAV-IVA)

[[sources/li-2020-online-gciva|Li, Koishida & Makino 2020]] extend GCAV-IVA to a **real-time online algorithm** by replacing the full-sample expectation in the auxiliary weighted covariance $\boldsymbol{V}_j$ with an [[concepts/online-iva|autoregressive recursion]] over short blocks ($L = 1$ frame, forgetting factor $\alpha = 0.96$); since the geometric constraints are linear, they pass through this modification unchanged. In the dual-microphone system the online algorithm runs at < 16 ms per 16 ms frame on a desktop CPU (≈ 5 ms without, ≈ 15 ms with the parallel online-AuxIVA DOA estimator) and outperforms online AuxIVA for both fixed and moving interference — including an underdetermined noisy condition where online AuxIVA nearly fails (SDR 6.86 dB vs. 1.70 dB). For fixed sources, the system with AuxIVA-estimated interference DOA beats the one using the *true* DOA by more than 4 dB, but for moving sources the reverse holds: online DOA estimation degrades (the paper shows failure examples), and an inappropriate constraint then hurts more than no target-channel constraint at all — making the unconstrained variant (a) the safer choice under source motion.

### Inverse-Free Online Updates via ISS (oGC-AuxIVA-ISS)

The VCD-based updates (offline and online) require a matrix inversion $\boldsymbol{D}_{jf}^{-1}$ per frequency, source, and iteration. [[sources/goto-2022-iss-gciva|Goto et al. 2022]] replace VCD with [[concepts/iterative-source-steering|iterative source steering]]: the whole demixing matrix receives a rank-1 update $\boldsymbol{W}_{fn} \leftarrow \boldsymbol{W}_{fn} - \boldsymbol{v}_{jfn}\boldsymbol{w}_{jfn}^{\mathsf{H}}$ per source, and the geometric constraints enter the closed-form ISS coefficients directly — through the response $g_{jf\theta n} = \boldsymbol{w}_{jfn}^{\mathsf{H}}\boldsymbol{d}_{f\theta}$ in the off-diagonal update $v_{ijfn}$, and through the scalars $p_{jfn}$, $q_{jfn}$ in the diagonal update $v_{jjfn}$ — so **no matrix inversion appears anywhere**. The look directions $\Theta_n$ may be time-varying, letting the constraints track estimated DOAs of moving sources. On a fixed-target/moving-interference task (ATR speech, 2 mics, RT60 200 ms), online GC-AuxIVA-ISS matched online GC-AuxIVA-VCD in SDR/SIR (with 100% output-order accuracy) while cutting execution time by 25–75%, depending on how often DOAs are estimated. The interference DOAs themselves are estimated by MUSIC applied to projection-back source images, with a 5-frame moving average ("MUSIC smooth") beating per-frame and blockwise estimates by > 0.7 dB SDR.

## Relation to Other Spatially Guided BSS

GCIVA belongs to the broader family of methods that inject prior spatial information into BSS, alongside [[concepts/spatial-regularization|spatial regularization]] (penalizing demixing-vector distance from DOA-derived steering vectors, used in SR-ILRMA/SR-SwIVA) and spatially informed MAP priors on demixing matrices (Brendel et al. 2019). Its distinguishing feature is that the constraints are **hard linear response constraints** in the LCMV sense rather than quadratic proximity penalties, and that they enable deliberate spatial shaping (nulls, distortionless responses) of specific output channels — including blocking-matrix behavior for interference reference generation.

## Related Concepts

- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/spatial-regularization|Spatial Regularization]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/lcmv-beamformer|LCMV Beamformer]]
- [[concepts/mpdr-beamformer|MPDR Beamformer]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
- [[concepts/online-iva|Online IVA]]

## Related Sources

- [[sources/li-2020-geometrically-constrained-iva|Li & Koishida 2020: Geometrically Constrained IVA for Directional Speech Enhancement]]
- [[sources/li-2020-online-gciva|Li, Koishida & Makino 2020: Online Directional Speech Enhancement Using Geometrically Constrained IVA]] — real-time online extension (oGCAV-IVA) and the three interference-DOA system variants
- [[sources/goto-2022-iss-gciva|Goto, Ueda, Li, Yamada & Makino 2022: Accelerating Online GC-IVA with Iterative Source Steering]] — inverse-free online GC-AuxIVA-ISS (ISS rank-1 updates with constraints in the closed-form coefficients) and MUSIC-based interference DOA estimation
