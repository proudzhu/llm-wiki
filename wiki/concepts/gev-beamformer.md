---
type: concept
created: 2026-10-11
updated: 2026-10-11
sources:
  - raw/papers/heymann-2016-neural-spectral-mask-beamforming/full-text.md
  - raw/papers/boeddeker-2018-neural-mask-beamforming/full-text.md
tags:
  - beamforming
  - speech-enhancement
  - array-processing
---

# GEV Beamformer

The **Generalized Eigenvalue (GEV) beamformer** (also **max-SNR beamformer**) selects beamforming coefficients $\mathbf{w}_f$ that maximize the output signal-to-noise ratio at each frequency bin. Along with the [[concepts/mvdr-beamformer|MVDR beamformer]], it is one of the two standard beamformers driven by mask-estimated [[concepts/spatial-covariance-matrix|spatial covariance matrices]] in neural mask-based beamforming, and it was part of the front-ends of CHiME challenge winning systems.

## Formulation

At frequency bin $f$, the GEV beamformer is the solution of

$$
\max_{\mathbf{w}_f} \frac{\mathbf{w}_f^{\mathrm{H}} \boldsymbol{\Phi}_{\mathbf{XX}f} \mathbf{w}_f}{\mathbf{w}_f^{\mathrm{H}} \boldsymbol{\Phi}_{\mathbf{NN}f} \mathbf{w}_f},
$$

which is given by the **principal generalized eigenvector** of the speech/noise SCM pair $(\boldsymbol{\Phi}_{\mathbf{XX}f}, \boldsymbol{\Phi}_{\mathbf{NN}f})$.

### Normalization

The GEV solution is defined only up to an arbitrary complex scale per frequency bin, so its raw output has an arbitrary magnitude *and* phase response. Two normalization filters compensate:

- **Blind Analytic Normalization (BAN)** — a post-filter that fixes the arbitrary magnitude response analytically from the SCMs.
- **Group delay normalization** — equalizes the arbitrary phase/group-delay response, important for ASR features that are sensitive to phase misalignment across frequency.

## Relation to Other Beamformers

- The MVDR is the distortionless counterpart: it constrains the response toward the target while minimizing noise power, whereas the GEV freely trades distortion for output SNR.
- Like the statistics-only MVDR form, the GEV needs **no steering vector or array geometry** — only the speech and noise SCMs, which is exactly what makes both compatible with DNN mask-based SCM estimation ([[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker et al. 2018]]).
- Distinct from [[concepts/gevd-spatial-filtering|GEVD spatial filtering]], which uses the *generalized eigenvalue decomposition* of SCMs to parameterize an SDW-MWF, rather than taking the principal generalized eigenvector as the beamformer itself.

## Practical Notes

[[sources/heymann-2016-neural-spectral-mask-beamforming|Heymann, Drude & Haeb-Umbach 2016]] — where this front-end family originated — found the GEV **consistently better than the MVDR** despite their theoretical equivalence (GEV+BAN coincides with the MVDR under perfect distortion removal): with sparse neural masks the noise SCM becomes ill-conditioned, and the MVDR's explicit $\boldsymbol{\Phi}_{\mathbf{NN}}^{-1}$ then hurts, while the GEV's generalized eigenvalue problem stays numerically stable (see [[concepts/condition-number|Condition Number]]). All of their CHiME-3 results therefore use GEV — with BAN for PESQ evaluation, and *without* BAN for ASR, where a matched acoustic model compensates the GEV distortions slightly better than the post-filter does.

In [[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker, Erdogan, Yoshioka & Haeb-Umbach 2018]], the GEV+BAN+group-delay variant is evaluated alongside MVDR+BAN for far-field ASR; MVDR+BAN gave the best results in the authors' experiments and was used for most of them. The paper's feature-level [[concepts/logmel-mse-loss|LogMel MSE]] training criterion and [[concepts/online-mask-based-beamforming|online operation]] schemes apply to either beamformer.

## Related Concepts

- [[concepts/mvdr-beamformer|MVDR Beamformer]] — distortionless counterpart used in most experiments
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]] — mask-weighted SCM estimation feeds the generalized eigenproblem
- [[concepts/tf-mask-estimation|TF Mask Estimation]] — DNN masks weight the SCM accumulation
- [[concepts/neural-beamforming|Neural Beamforming]] — the differentiable, mask-driven beamforming framework the GEV belongs to
- [[concepts/beamforming|Beamforming]] — parent topic
- [[concepts/gevd-spatial-filtering|GEVD Spatial Filtering]] — related GEVD-of-SCM technique for SDW-MWF design

## Related Sources

- [[sources/heymann-2016-neural-spectral-mask-beamforming|Heymann, Drude & Haeb-Umbach 2016: Neural Network Based Spectral Mask Estimation for Acoustic Beamforming]] — origin of the front-end; GEV consistently beats MVDR under sparse masks (condition-number analysis), CHiME-3 WER halved
- [[sources/boeddeker-2018-neural-mask-beamforming|Boeddeker, Erdogan, Yoshioka & Haeb-Umbach 2018: Exploring Practical Aspects of Neural Mask-Based Beamforming for Far-Field Speech Recognition]] — GEV with BAN + group delay normalization as one of two mask-driven beamformers in a practical far-field ASR evaluation
