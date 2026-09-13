---
type: source
created: 2026-09-13
updated: 2026-09-13
sources:
  - raw/papers/souden-2010-pmwf/full-text.md
  - https://doi.org/10.1109/TASL.2009.2025790
  - zotero://select/items/0_SHZJBBAL
tags:
  - speech-enhancement
  - noise-reduction
  - beamforming
  - wiener-filter
  - multi-channel
  - microphone-arrays
---

# Souden, Benesty & Affes 2010: On Optimal Frequency-Domain Multichannel Linear Filtering for Noise Reduction

**Authors**: [[entities/mehrez-souden|Mehrez Souden]], [[entities/jacob-benesty|Jacob Benesty]], [[entities/sofienne-affes|Sofiène Affes]]
**Institution**: INRS-EMT, University of Quebec, Montreal, QC, Canada
**Venue**: IEEE Transactions on Audio, Speech, and Language Processing, vol. 18, no. 1, 2010
**Type**: Journal article
**DOI**: [10.1109/TASL.2009.2025790](https://doi.org/10.1109/TASL.2009.2025790)
**Zotero**: [SHZJBBAL](zotero://select/items/0_SHZJBBAL)

## Summary

This is the foundational paper of the **parameterized multichannel non-causal Wiener filter (PMWF)**. It provides the first clear unifying theoretical analysis of frequency-domain multichannel linear filtering for noise reduction, showing formally that the MVDR beamformer is the $\beta = 0$ particular case of the PMWF, deriving new simplified expressions for the PMWF, MVDR, and GSC that depend on signal statistics only (explicitly independent of channel transfer function ratios), and establishing closed-form performance measures that quantify the multichannel speech-distortion versus noise-reduction tradeoff. It also proves, via the magnitude squared coherence, that all filters in the PMWF family improve the output SNR.

## Problem Formulation

A speech source impinges on an array of $N$ microphones with arbitrary geometry. In the frequency domain, the observations are

$$Y_n(j\omega) = G_n(j\omega) S(j\omega) + V_n(j\omega) = X_n(j\omega) + V_n(j\omega)$$

The goal is to estimate the noise-free reverberant component $X_{n_0}(j\omega)$ at a reference microphone $n_0$ by applying a linear filter $\mathbf{h}_{n_0}(j\omega)$ to the observation vector $\mathbf{y}(j\omega)$. Two error signals are defined: the residual signal distortion $\mathcal{E}_{x,n_0}$ and the residual noise $\mathcal{E}_{v,n_0}$.

The key move is to **switch the constraint and objective** of the traditional parameterized-filter program: instead of minimizing speech distortion subject to a residual-noise bound (Doclo & Moonen, Spriet et al.), minimize the residual noise subject to an upper bound on signal distortion:

$$\min_{\mathbf{h}_{n_0}} E\{|\mathcal{E}_{v,n_0}|^2\} \quad \text{s.t.} \quad E\{|\mathcal{E}_{x,n_0}|^2\} \leq \sigma^2(\omega)$$

This yields the same filter (the Lagrangians are equal up to a constant scaling) but makes the continuum to the distortionless case $\sigma(\omega) = 0$ (MVDR) explicit.

Performance measures (local, at each frequency), following Chen et al.'s single-channel analysis:
- **Signal distortion index**: $v_{\mathrm{sd}} = E\{|\mathcal{E}_{x,n_0}|^2\} / E\{|X_{n_0}|^2\}$
- **Noise reduction factor**: $\xi_{\mathrm{nr}} = E\{|V_{n_0}|^2\} / E\{|\mathcal{E}_{v,n_0}|^2\}$
- **Output SNR**: $\mathrm{SNR}_o = E\{|D_{n_0}|^2\} / E\{|\mathcal{E}_{v,n_0}|^2\}$

## Methodology

### PMWF and the Statistics-Only Closed Forms

The Lagrangian solution of the constrained program is the PMWF:

$$\mathbf{h}_{\mathrm{W}\beta, n_0}(j\omega) = [\Phi_{xx}(j\omega) + \beta\,\Phi_{vv}(j\omega)]^{-1} \Phi_{xx}(j\omega)\, \mathbf{u}_{n_0}$$

where $\beta = 1/\gamma$ is the tuning parameter and $\mathbf{u}_{n_0}$ selects the reference channel. Because $\Phi_{xx} = \phi_{ss} \mathbf{g}\mathbf{g}^H$ is rank one, the Woodbury identity gives two key properties: the matrix $\Phi_{vv}^{-1}\Phi_{xx}$ has a unique positive eigenvalue

$$\lambda(\omega) = \mathrm{tr}\{\Phi_{vv}^{-1}\Phi_{xx}\} = \mathrm{tr}\{\Phi_{vv}^{-1}\Phi_{yy}\} - N$$

and the inverse $[\Phi_{xx} + \beta\Phi_{vv}]^{-1}$ admits a simplified form. The resulting **new expression** for the PMWF is

$$\mathbf{h}_{\mathrm{W}\beta, n_0}(j\omega) = \frac{\Phi_{vv}^{-1}(j\omega)\,\Phi_{xx}(j\omega)}{\beta + \lambda(\omega)}\, \mathbf{u}_{n_0} = \frac{\Phi_{vv}^{-1}(j\omega)\,\Phi_{yy}(j\omega) - \mathbf{I}_N}{\beta + \lambda(\omega)}\, \mathbf{u}_{n_0}$$

which requires only the PSD matrices $\Phi_{yy}$ and $\Phi_{vv}$ — no channel transfer functions, no array geometry, no source location. Particular cases:
- $\beta = 0$: **MVDR** $\mathbf{h}_{\mathrm{MVDR}} = \frac{\Phi_{vv}^{-1}\Phi_{xx}}{\lambda}\mathbf{u}_{n_0}$ — formally shown to be the distortionless limit of the PMWF
- $\beta = 1$: **non-causal multichannel Wiener filter** (MWF)

The GSC is the statistically equivalent unconstrained implementation of the MVDR.

### Statistics-Only GSC

![[raw/papers/souden-2010-pmwf/figures/8e4070da0ad7dd4250437623a136527873905747768d30bd004bc09933a36948.jpg|GSC structure]]
*Figure 1: GSC structure (particular case $n_0 = 1$) — fixed distortionless beamformer branch plus blocking-matrix + noise-canceller branch.*

Three statistics-only components replace the classical delay-and-sum / transfer-function-ratio components:

1. **Distortionless beamformer** (matched filter): $\mathbf{f}(j\omega) = \frac{\Phi_{xx}(j\omega)}{\mathrm{tr}\{\Phi_{xx}(j\omega)\}}\mathbf{u}_{n_0}$ — passes $X_{n_0}$ undistorted.
2. **Blocking matrix** $\mathbf{B}(j\omega)$ spanning the subspace orthogonal to $\boldsymbol{\chi}(j\omega) = \Phi_{xx}(j\omega)\mathbf{u}_{n_0} = \phi_{ss} G_{n_0}^* \mathbf{g}$ — theoretically equivalent to using the true channel transfer-function ratios (since $\chi_k^*/\chi_{n_0}^* = G_k^*/G_{n_0}^*$), but available directly from the speech PSD matrix. Unlike Gannot et al.'s TFR-GSC it needs no least-squares ratio estimation, and unlike Warsitz et al.'s GEV-GSC it needs no generalized eigenvector decomposition.
3. **Noise canceller**: $\mathbf{n}(j\omega) = [\mathbf{B}^H\Phi_{vv}\mathbf{B}]^{-1}\mathbf{B}^H\Phi_{vv}\mathbf{f}$.

### Closed-Form Performance Measures

Using the rank-one decomposition, the local performance measures of the PMWF-$\beta$ reduce to remarkably simple expressions:

$$v_{\mathrm{sd}}[\mathbf{h}_{\mathrm{W}\beta}] = \frac{\beta^2}{[\beta + \lambda(\omega)]^2}, \qquad \xi_{\mathrm{nr}}[\mathbf{h}_{\mathrm{W}\beta}] = \frac{[\beta + \lambda(\omega)]^2}{\mathrm{SNR}(\omega)\,\lambda(\omega)}, \qquad \mathrm{SNR}_o[\mathbf{h}_{\mathrm{W}\beta}] = \lambda(\omega)$$

Key consequences:
- **The output SNR is independent of $\beta$** — all filters in the PMWF family (Wiener, MVDR, GSC, and also maximum-likelihood and maximum-SNR filters, which are equal up to a frequency-dependent scaling) achieve the same local output SNR $\lambda(\omega)$. The parameter $\beta$ trades distortion against noise-reduction *factor*, not output SNR.
- For the MVDR: $v_{\mathrm{sd}} = 0$ and $\xi_{\mathrm{nr}} = \lambda/\mathrm{SNR}(\omega)$ — noise reduction with zero distortion is possible in the multichannel case (impossible single-channel).
- The $\beta$–$\sigma$ link: $\beta \leq \frac{\tilde{\sigma}(\omega)}{1 - \tilde{\sigma}(\omega)}\lambda(\omega)$, enabling psychoacoustically-motivated frequency-dependent distortion bounds.
- In the anechoic/incoherent-noise case, $\lambda(\omega) = \mathrm{SNR}(\omega)[1 + R_{n_0}(\omega)]$ with $R_{n_0} = \sum_{n \neq n_0}|G_n|^2/|G_{n_0}|^2$, so more microphones monotonically increase the output SNR and decrease distortion; the Wiener and MVDR are related by $\mathbf{h}_{\mathrm{MVDR}} = \frac{1+\lambda}{\lambda}\mathbf{h}_{\mathrm{W}}$, converging in behavior at high SNR or many microphones.
- **Coherent versus incoherent noise**: with $\Phi_{vv} = \mathbf{c}\mathbf{c}^H + \delta\mathbf{I}$, $\lambda = \frac{\phi_{ss}\|\mathbf{g}\|^2}{\delta}[1 - \alpha]$ where $\alpha$ grows with the collinearity between the coherent-noise and target propagation vectors (placing the noise source near the speaker hurts) and shrinks as coherent noise dominates over incoherent noise. With purely coherent noise off-axis, the noise is totally removed without distortion.

### Proof of Output SNR Improvement

A new, simple proof using the magnitude squared coherence (MSC) $\rho_{xy}^2(\omega) = |\phi_{xy}|^2/(\phi_{xx}\phi_{yy}) \in [0, 1]$: bounding the MSC between the reference clean signal and the output on both sides yields

$$\mathrm{SNR}_o[\mathbf{h}_{\mathrm{W}, n_0}(j\omega)] \geq \mathrm{SNR}(\omega)$$

which applies to every filter equal to the Wiener filter up to a scaling factor — i.e., the entire PMWF family including MVDR and GSC.

## Experimental Setup

| Item | Value |
|------|-------|
| Room | $6.7 \times 6.1 \times 2.9$ m, image-method RIRs (0.5 s each) |
| Reverberation | $T_{60} \approx 0$ ms (anechoic) and $T_{60} \approx 270$ ms |
| Array | Uniform linear, $N = 2$–$10$ microphones, spacing 0.2 m |
| Source | ~2-min female speech, 8 kHz sampling |
| Noise | Computer-generated white Gaussian, long-term input SNR 0 and 10 dB (at reference mic) |
| Analysis | 256-ms frames ($L = 2048$), 75% overlap, Welch modified periodogram |
| Statistics | Batch mode, noise samples known (estimation accuracy set aside) |
| Non-causality | Frequency → time → truncate FIR → frequency |
| Compared filters | PMWF-1 (Wiener), PMWF-10, PMWF-0 (MVDR), GSC, GEV-GSC, ideal TFR-GSC |

## Results

![[raw/papers/souden-2010-pmwf/figures/466eb16d88def3c1ac39c2c04a52d10b268b9fccbdca4b342b2bd99026dba3fe.jpg|Signal distortion index and noise reduction factor versus beta]]
*(a) Signal distortion index and noise reduction factor versus $\beta$; $N = 2$, input SNR = 0 dB.*
![[raw/papers/souden-2010-pmwf/figures/b1b7e17664b8dd74715960266650749acca9f0040af788e86dec5943d4d8156a.jpg|Scalar coefficient relating PMWF-1 and MVDR]]
*(b) Scalar coefficient relating PMWF-1 and MVDR filters versus input SNR and number of microphones; anechoic environment.*
*Figure 2: Theoretical analysis of the tradeoff and of the Wiener–MVDR scaling.*

![[raw/papers/souden-2010-pmwf/figures/9d8356295e35d0962d50e755641c8dd22326c13f2e2e7f177a0c955732029c00.jpg|Log-likelihood ratio versus number of microphones]]
*(a) Log-likelihood ratio.*
![[raw/papers/souden-2010-pmwf/figures/360599ad78588e2daec88f2d0f3acd4e213db79efeaf7e77e8ce9efed247a1cc.jpg|Signal distortion index versus number of microphones]]
*(b) Signal distortion index.*
*Figure 3: Signal distortion versus number of microphones, anechoic ($T_{60} \approx 0$ ms).*

![[raw/papers/souden-2010-pmwf/figures/2b708102b2841ac233fa614688bb7dfe5a93c32314464d002e4653fcd5b3ad48.jpg|Noise reduction factor versus number of microphones]]
*(a) Noise reduction factor.*
![[raw/papers/souden-2010-pmwf/figures/f78b2e94ded0f4eb0a4a23efb2b6edbcafd3c77110032ef25e2435b98828c864.jpg|Output SNR versus number of microphones]]
*(b) Output SNR.*
*Figure 4: Noise reduction versus number of microphones, anechoic ($T_{60} \approx 0$ ms).*

Global performance (Table I; 10 microphones, input SNR 10 dB):

| Measure | GSC | MVDR | PMWF-1 | PMWF-10 |
|---------|-----|------|--------|---------|
| Anechoic: LLR | 0.075 | 0.070 | 0.116 | 0.43 |
| Anechoic: $v_{\mathrm{sd}}$ [dB] | −27.59 | −27.61 | −27.15 | −19.6 |
| Anechoic: $\xi_{\mathrm{nr}}$ [dB] | 11.8 | 11.68 | 12.35 | 14.19 |
| Anechoic: $\mathrm{SNR}_o$ [dB] | 21.84 | 21.74 | 22.33 | 23.85 |
| $T_{60} \approx 270$ ms: LLR | 0.101 | 0.096 | 0.15 | 0.49 |
| $T_{60} \approx 270$ ms: $v_{\mathrm{sd}}$ [dB] | −16.31 | −16.32 | −16.17 | −14.41 |
| $T_{60} \approx 270$ ms: $\xi_{\mathrm{nr}}$ [dB] | 11.74 | 11.62 | 12.28 | 14.10 |
| $T_{60} \approx 270$ ms: $\mathrm{SNR}_o$ [dB] | 21.42 | 21.30 | 21.90 | 23.36 |

Main findings:

- The multichannel distortion–noise-reduction tradeoff is confirmed: MVDR/GSC give the lowest distortion, PMWF-10 the highest noise reduction and output SNR; the PMWF-1 sits in between and converges to MVDR behavior as $N$ and input SNR grow.
- More microphones reduce distortion and increase output SNR for all $\beta$; in practice, larger PSD matrices bring estimation errors that make MVDR/GSC distortion slightly *grow* with $N$ (theoretically it should stay at zero from $N = 2$).
- The local output SNR is equal across filters in most of the frequency range, confirming $\mathrm{SNR}_o = \lambda$ independent of $\beta$.
- **New GSC vs. alternatives** (Table II): the proposed statistics-only GSC clearly outperforms the GEV-GSC (whose delay-and-sum first branch is sensitive to TDOA errors and ignores reverberation/attenuation): e.g., at input 0 dB anechoic, $v_{\mathrm{sd}} = -18.22$ dB vs. $-4.17$ dB. The ideal TFR-GSC (with *known* channel transfer functions — an impractical assumption) achieves the lowest distortion ($-49.28$ dB) but lower noise reduction; all filters reach similar output SNR.

## Key Contributions

1. **MVDR as PMWF-0**: formally shows the MVDR is a particular case of the PMWF by switching the constraint and objective in the noise-reduction optimization (minimize noise s.t. distortion bound), yielding near-identical closed-form expressions for both filters.
2. **Statistics-only expressions**: new simplified expressions for the PMWF, MVDR, and GSC that depend only on the signal statistics ($\Phi_{yy}$, $\Phi_{vv}$) and are explicitly independent of channel transfer function ratios — no array geometry, source location, TDOA estimation, GEV decomposition, or least-squares ratio fitting required.
3. **Closed-form performance measures**: new simplified expressions for the signal distortion index, noise reduction factor, and output SNR of the PMWF family in terms of $\beta$ and the single parameter $\lambda(\omega)$, establishing the multichannel distortion–noise-reduction tradeoff analytically.
4. **Coherent/incoherent noise analysis**: quantifies the effects of noise spatial structure and of microphone count on $\lambda$ (hence on all three measures), including the incoherent-case factorization $\lambda = \mathrm{SNR}[1 + R_{n_0}]$.
5. **New SNR-improvement proof**: an MSC-based proof that all filters equal to the Wiener filter up to a scaling factor improve the output SNR over the input SNR.

## Related Concepts

- [[concepts/parametric-multi-channel-wiener-filter|Parametric Multi-Channel Wiener Filter (PMWF)]] — the paper's central contribution
- [[concepts/mvdr-beamformer|MVDR Beamformer]] — the $\beta = 0$ distortionless endpoint
- [[concepts/gsc-beamformer|Generalized Sidelobe Canceller]] — statistics-only GSC components
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]] — the $\beta = 1$ endpoint
- [[concepts/speech-distortion-constrained-noise-reduction|Speech-Distortion-Constrained Noise Reduction]] — the optimization framework
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]] — the only required statistics
- [[concepts/wiener-filter|Wiener Filter]] — single-channel counterpart
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]] — classical statistical foundation of the multichannel branch
- [[synthesis/deep-speech-enhancement|Deep Speech Enhancement]] — the PMWF family as the classical precursor that hybrid neural systems (e.g., NeuralPMWF) build upon
