---
type: concept
created: 2026-08-15
updated: 2026-08-15
sources:
  - raw/papers/tashev-2008-sound-capture-spatial-filter/full-text.md
tags:
  - spatial-filter
  - speech-enhancement
  - statistical-model
  - mmse
  - non-linear-post-filter
  - microphone-array
---

# Probability-Based Spatial Filter

A **probability-based spatial filter** is a non-linear microphone-array post-processor that estimates, per time frame and per frequency bin, the *posterior probability* that the captured signal originates from a desired direction, and applies that probability directly as the suppression gain. The formulation was introduced by Tashev, Mihov, Gleghorn & Acero (2008) as the post-beamformer stage of their small-device sound-capture system, and is an **MMSE estimator** of the time-domain waveform.

## Pipeline

Given two beamformer outputs (front $Y_F$ and rear $Y_R$) from a [[concepts/back-to-back-microphone-array\|back-to-back microphone array]] or other two-beam geometry, the post-filter operates as:

1. A [[concepts/voice-activity-detection\|binary VAD]] gates which frames update the noise model (non-voiced frames) vs. the speech models (voiced frames).
2. **Features** are extracted from the beam pair. Tashev et al. used four:
   - Per-frame level difference (RMS)
   - Per-bin level difference (magnitude per frequency bin)
   - Per-frame time delay (PHAT-weighted GCC, see [[concepts/beamforming\|GCC-PHAT]])
   - Per-bin time delay (phase difference)
3. For each feature, **three statistical models** are tracked in real time: front-source, rear-source, and noise. Each has its own adaptation time constant ($\tau_W, \tau_{Wb}, \tau_D, \tau_{Db}$).
4. For each feature, a **posterior probability** that the source is in the desired direction is computed via Bayesian competition across the three PDFs.
5. The four per-feature posteriors are **fused multiplicatively** with per-feature gains $G_i \in [0,1]$ (gain = 1 disables a feature; gain = 0 gives it full weight).
6. The fused probability is applied directly as the per-bin suppression gain.

## Asymmetric PDF for Level Differences

For the per-frame level-difference feature, the front-source PDF is asymmetric: **exponential** for positive differences (the front beam is louder, consistent with a front source) and **Gaussian** for negative differences (consistent with a rear source or noise):

$$
p_{FW}(\Delta L_W \mid \theta_{FW},\sigma_W) =
\begin{cases}
\dfrac{1}{\theta_{FW}}\exp\!\left(-\dfrac{\Delta L_W}{\theta_{FW}}\right) & \Delta L_W > 0 \\[6pt]
\dfrac{1}{\theta_{FW}}\exp\!\left(-\dfrac{\Delta L_W^2}{2\sigma_W^2}\right) & \text{otherwise}
\end{cases}
$$

The exponential scale $\theta_{FW}$ is estimated during voiced frames with positive level differences; the rear-source parameter $\theta_{RW}$ is estimated symmetrically for negative differences. The noise model is a zero-mean Gaussian whose mean $L_C$ and variance $\sigma_W^2$ are tracked during VAD-flagged non-voiced frames.

## Posterior Probability and Fusion

For feature $i$ and current observation $x_i^{(n)}$, the posterior probability of a front source is:

$$
\hat{P}_i^{(n)} = \frac{p_{F,i}(x_i^{(n)})}{p_{F,i}(x_i^{(n)}) + p_{R,i}(x_i^{(n)}) + p_{N,i}(x_i^{(n)})}
$$

The four posteriors are fused multiplicatively, with each feature attenuated toward 1 by its gain $G_i$:

$$
P_k^{(n)} = \prod_{i=1}^{4} \left((1-G_i)\,\hat{P}_i^{(n)}(k) + G_i\right)
$$

The fused $P_k^{(n)}$ is applied directly as the gain on time-frequency bin $(n, k)$. Because $P_k^{(n)}$ is a Bayesian posterior and the time-domain waveform estimator $\hat{X} = P \cdot Y$ minimizes MSE under the corresponding source-distribution assumptions, the post-filter is an MMSE estimator [McAulay & Malpass 1980].

## Offline Parameter Optimization via Wiener Reference

The eight non-estimable parameters (four adaptation time constants $\tau$ and four feature gains $G_i$) cannot be derived from the input statistics; they are tuned offline by **steepest-gradient descent** minimizing the MSE between the probability-based gain and an **oracle [[concepts/wiener-filter\|Wiener gain]]**:

$$
H_w^{(n)}(k) = \frac{|X_k^{(n)}|^2}{|X_k^{(n)}|^2 + |N_k^{(n)}|^2}
$$

computed from separately recorded clean speech $X$ and noise $N$ (the mixture is formed by summation, so the per-bin clean and noise components are known). Because the probability estimator is itself an MMSE estimator, this objective drives the tunable posterior toward the optimal Wiener gain. Constrained bounds on $\tau$ and $G$ are enforced via punishing functions; the training/test split is 80/20 per file with an early-stopping rule (no test-set improvement for 5 iterations) to prevent overfitting.

## Empirical Findings (Tashev et al. 2008)

On the 9.6 mm back-to-back array at 16 kHz, the optimizer **disabled both delay-based features** ($G_\text{Del/fr} = 0.89$, $G_\text{Del/bin} = 0.99$). The system effectively relies on **level-difference features only**. The level-difference-only configuration achieved 10.43 dB SNR improvement (vs. 11.06 dB for all four features), and the delay features individually contributed only 6.21 dB (per-frame) and 1.96 dB (per-bin) — confirming that on very small baselines, time-delay features are unreliable and the back-to-back directional-microphone geometry (which produces a strong level-difference cue) is the right design choice.

## Related Concepts

- [[concepts/back-to-back-microphone-array\|Back-to-Back Microphone Array]]
- [[concepts/beamforming\|Beamforming]]
- [[concepts/voice-activity-detection\|Voice Activity Detection]]
- [[concepts/wiener-filter\|Wiener Filter]]
- [[concepts/multi-channel-speech-enhancement\|Multi-Channel Speech Enhancement]]
- [[concepts/speech-enhancement\|Speech Enhancement]]
- [[concepts/multi-channel-wiener-filter\|Multi-Channel Wiener Filter]]
- [[concepts/ideal-ratio-mask\|Ideal Ratio Mask]] — also a per-bin multiplicative mask, but derived from clean/noise separation rather than spatial statistics
- [[concepts/mmse\|MMSE]] (mentioned conceptually)

## Related Sources

- [[sources/tashev-2008-sound-capture-spatial-filter|Tashev, Mihov, Gleghorn & Acero 2008: Sound Capture System and Spatial Filter for Small Devices]]
