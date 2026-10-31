---
type: synthesis
created: 2026-04-25
updated: 2026-10-31
sources:
  - zotero://select/items/0_QVJMFTWC
  - raw/papers/rout-2012-pso-anc-without-secondary-path/full-text.txt
  - raw/papers/maeda-1999-anc-simultaneous-perturbation/full-text.md
  - raw/papers/kajikawa-2003-fdsp-variable-perturbation/full-text.md
  - raw/papers/kuo-2006-anc-headphones/full-text.txt
tags:
  - anc
  - secondary-path
  - system-identification
  - online-modeling
  - offline-modeling
---

# Secondary Path Modeling: From Offline Identification to Model-Free Evolution

## The Core Tension

The secondary path $S(z)$ is the lifeblood of the FXLMS algorithm — the reference signal must be filtered through $\hat{S}(z)$ before the weights can be updated. But $S(z)$ itself is time-varying (earphone placement shifts, temperature drift, airflow changes), and the modeling process interferes with ANC operation. **The entire field of secondary path modeling is devoted to resolving one tension: how to continuously track a constantly changing transfer function without disturbing noise control.**

## Four Technical Routes

### Route 1: Offline Modeling → Periodic Recalibration

The simplest scheme: shut down ANC → inject white noise → LMS identification → fix $\hat{S}(z)$ → restart ANC.

| Advantage | Disadvantage |
|------|------|
| Simple to implement, no interference | Quickly becomes outdated in time-varying environments |
| High identification accuracy (no signal contamination) | Requires downtime, poor user experience |

**Applicable to**: fixed installations (ducts, buildings) where $S(z)$ is quasi-static.

Kuo (1999) gives the standard offline LMS identification procedure; once converged, $\hat{S}(z)$ is fixed. Benois (2020)'s FPGA prototype also uses offline pre-calibration, but notes that in earphone scenarios, $\hat{S}(z)$ deviation caused by fitting changes is the main performance bottleneck.

**Route 1 also has an excitation-signal design problem**: white noise or chirp is audible and annoying during calibration. [[sources/kuo-2006-anc-headphones|Kuo, Mitra & Gan 2006]] resolve it on their AFANC headphone by identifying the 65-tap $\hat{S}(z)$ with **music** instead — spectrally dense frames of "O Fortuna" (near-flat 0–4 kHz; music pieces systematically trade frequency density against bandwidth) produce an estimate matching white-noise and chirp-identified models. This keeps Route 1's simplicity and accuracy while removing its "poor user experience" disadvantage, and the same idea generalizes to any wearable where the training signal is heard.

### Route 2: Additive-Noise Online Modeling

Inject a low-power auxiliary noise $v(n)$ during ANC operation while simultaneously identifying $\hat{S}(z)$.

**Core difficulty**: $v(n)$ must be loud enough for identification, but too loud and the user hears it. Kuo (1999) analyzed the relationship between convergence speed and $\sigma_d^2 / \sigma_v^2$ — online modeling is slower than offline by this ratio.

**Improvement directions**:
- **Eriksson (1989)**: the basic two-filter additive-noise structure, where $v(n)$ appears in the residual error, constraining its power
- **Zhang (2001)**: the three-filter cross-updated method, the best performer among classical approaches
- **Akhtar (2006)**: two filters + MFxLMS + [[concepts/variable-step-size-lms|VSS LMS]] (inverse step-size strategy), achieving better performance with fewer filters, −12.35 dB NMSE
- **Adaptive noise cancellation**: uses an auxiliary filter to remove the interference of $d(n)$ on identification, speeding it up by ~30×
- **RMFxLMS** (Yang 2026): a robust multichannel variant that handles cross-coupling in multichannel scenarios

### Route 3: Auxiliary-Noise-Free Modeling

No extra signal is injected; $\hat{S}(z)$ is identified using only the signals already present during ANC operation.

- **Simultaneous equation method** (Jin 2007, Fujii 1999): forms algebraic equations by differencing the input-output signals and solves them jointly for $\hat{S}(z)$, with no need for $v(n)$
- **Coefficient update method**: back-infers $\hat{S}(z)$ from the implicit information in the FxLMS weight update equations

**Cost**: slower convergence, worse stability, and sensitivity to SNR.

### Route 4: Bypassing $S(z)$ Identification

The most radical route — do not model $\hat{S}(z)$ at all, and eliminate the dependence on it at the algorithm level.

| Method | Principle | Cost |
|------|------|------|
| **Stochastic perturbation** (Maeda 1999) | Random $\pm c$ sign perturbations of all taps measure the gradient of block error power from the error mic alone — one (TDSP) or two (SP) measurements per update | Perturbation noise in the output; block-granular convergence; demonstrated only on a 5-tap FIR / sinusoidal noise |
| **FDSP + variable perturbation** (Kajikawa 2003) | Frequency-domain per-bin gradient estimation from perturbed/unperturbed half-block error FFTs; perturbation magnitude scaled to error power, permitting a ~75× larger step size at ~3× lower cost than FxLMS | Needs the scalar secondary-path *gain* $G$ (not the full model); perturbation still injected into the output; block-granular updates |
| **SPR condition** (Zhou 2007) | Strictly positive-real condition guarantees stability without $\hat{S}(z)$ | The condition is stringent and hard to satisfy in practice |
| **Evolutionary search** (GA/PSO) | Genetic algorithm / particle swarm directly searches for the optimal $W(z)$ | Large population computational overhead (e.g., $P=200$ parallel filters); update granularity is per generation, not per sample |
| **Careful Control** (Lopes 2022) | Dual-control framework with alternating least squares | Slow convergence, but no need for $\hat{S}(z)$ |
| **Meta-learning initialization** (Yang 2026) | MAML pre-trains the initial $W(z)$ | Requires large amounts of offline data |
| **MPC** (Liang 2026, Wills 2008) | State-space model embeds $S(z)$; QP solving bypasses explicit identification | Requires an accurate plant model |

Evolutionary search is not inherently incapable of real-time operation: Rout (2012)'s online PSO-ANC scheme uses MUX/DMUX to route the real-time reference signal to each filter in the population in turn (each filter gets $M \ge 2N$ fresh samples per generation), uses block mean-square error as the fitness, and runs in real time on the actual noise stream, with no need for $\hat{S}(z)$ at any point. Its [[concepts/conditional-reinitialized-pso|CRPSO]] variant detects abrupt changes in $S(z)$ or $P(z)$ by detecting jumps in the gbest error and reinitializes the population; 10/10 runs recovered the global optimum after the change — precisely the scenario where gradient-based methods are most fragile. The costs remain, however: the population size ($P=200$) imposes significant filter overhead, and weight updates are generation-granular, unable to achieve the per-sample adaptivity of FxLMS.

The stochastic-perturbation entry is among the earliest on this route: [[sources/maeda-1999-anc-simultaneous-perturbation|Maeda & Yoshida 1999]] (ACTIVE 99) adapted the control filter with [[concepts/simultaneous-perturbation|simultaneous perturbation]] — a stochastic-approximation scheme from neuro-control (Spall's SPSA, Maeda's learning rules) that *measures* the error-surface gradient by perturbing all taps at once. Kajikawa & Nomura pursued a closely related perturbation ANC in parallel (IEICE J82-A 1999; ISCAS 2000). Because the gradient is measured, neither $\hat{S}(z)$ nor a filtered reference is needed, and the one-measurement time-difference variant (TDSP) halves the evaluation cost (~25 dB vs ~15 dB at 200 Hz in their TMS320C30 duct experiment). The lineage's structural upgrade came with [[sources/kajikawa-2003-fdsp-variable-perturbation|Kajikawa & Nomura 2003]] (ICASSP): estimating the gradient **per frequency bin** from perturbed/unperturbed half-block error FFTs (instead of Maeda's single scalar difference shared by all taps), and scaling the perturbation magnitude to the error power ($c = \sqrt{\alpha P_{e2}/G^2 P_x}$) so the step size can grow ~75× — resolving the fixed-perturbation speed/cancellation trade-off while staying ~3× cheaper than FxLMS and recovering quickly from an abrupt secondary-path change. Notably, the "no secondary-path model" claim is there slightly qualified: the variable-perturbation rule needs the secondary-path *gain* $G$, a scalar. Later extensions include Tokoro, Kajikawa & Nomura's stability improvements (2007), establishing the perturbation branch of Route 4 alongside the later population-based one.

Liang (2026)'s delayed MPC is an interesting case: the MPC state-space model requires a parameterized form of $S(z)$ (obtained via vector fitting), but once the model is built, the QP solver directly outputs the optimal control signal — the step of filtering the reference signal through $\hat{S}(z)$ is no longer needed. **$S(z)$ degrades from "a filter used every sample" to "a model parameter calibrated once."**

## Decision Matrix

| Scenario | Recommended route | Rationale |
|------|---------|------|
| Fixed installation, quasi-static $S(z)$ | Route 1 (offline) | Simple and reliable, no online overhead |
| Earphones/wearables, slowly varying $S(z)$ | Route 2 (additive noise) | Balances accuracy and real-time operation |
| Sensitive to auxiliary noise (hearing aids) | Route 3 (auxiliary-noise-free) | Introduces no audible noise |
| Earphones, abrupt $S(z)$ changes (leakage/removal) | Route 5 (constraint checking) | 6-MAC detection + smooth fallback, no auxiliary noise needed |
| Severe nonlinearity/nonstationarity | Route 4 (MPC or meta-learning) | Bypasses the $S(z)$ identification bottleneck |

## The Impact Chain of Modeling Error

$\hat{S}(z)$ error affects the system through the following chain:

```
Phase error > 90° → FXLMS diverges (instability)
Phase error 40°-90° → reduced convergence speed, increased steady-state residual
Magnitude error → equivalent step-size scaling, slower convergence but no instability
Time-varying deviation → periodic oscillation, requires online tracking
```

Kuo (1999)'s classic result: under slow-adaptation conditions, FXLMS can tolerate ~90° of phase error, and errors within 40° have almost no effect on convergence. This means **a rough $\hat{S}(z)$ is usually good enough** — but in time-varying environments, "rough" itself is continually degrading.

## Evolution Trends

1. **From offline to online**: driven by wearable devices, time-varying $S(z)$ becomes the norm
2. **From explicit to implicit**: methods such as MPC and meta-learning embed $S(z)$ into the model, avoiding per-sample filtering
3. **From single to hybrid**: Luo (2026)'s GFANC-FxNLMS uses a generative model to provide the initial filter, with FxNLMS fine-tuning online — the accuracy requirement on $\hat{S}(z)$ is thereby lowered
4. **From identification to bypass**: the ultimate goal is to eliminate the dependence on $\hat{S}(z)$ entirely — stochastic perturbation (Maeda 1999 / Kajikawa & Nomura 1999–2000, in parallel) achieved it first by *measuring* the gradient, evolutionary search (Rout 2012's online PSO/CRPSO) from a population-based gradient-free angle, while MPC approaches this goal under specific conditions
5. **From iterative to deep learning**: Fareedha (2026)'s [[concepts/deep-secondary-path-estimation|DeepSPE]] replaces iterative adaptation with Conv1D + BiLSTM + Attention, achieving −16.27 dB NMSE with frame-level inference, a 3.92 dB improvement over Akhtar's VSS-LMS

## Related Pages

- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/online-secondary-path-modeling|Online Secondary-Path Modeling]]
- [[concepts/offline-secondary-path-modeling|Offline Secondary-Path Modeling]]
- [[concepts/filtered-x-lms-algorithm|Filtered-x LMS Algorithm]]
- [[concepts/variable-step-size-lms|Variable Step Size LMS]]
- [[concepts/deep-secondary-path-estimation|Deep Secondary Path Estimation]]
- [[concepts/conditional-reinitialized-pso|Conditional Reinitialized PSO]]
- [[concepts/simultaneous-perturbation|Simultaneous Perturbation]] — the earliest Route 4 method (Maeda & Yoshida 1999)
- [[synthesis/mpc-vs-fxlms-for-anc|MPC vs Traditional ANC]]
- [[synthesis/anc-architecture-evolution|ANC Architecture Evolution]] — where the Kuo/Mitra/Gan AFANC headphone serves as the IMC hardware benchmark
- [[queries/how-to-estimate-secondary-path|如何估计次级通道]]
