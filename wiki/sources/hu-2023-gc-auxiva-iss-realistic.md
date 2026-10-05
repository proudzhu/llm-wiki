---
type: source
created: 2026-10-05
updated: 2026-10-05
sources:
  - raw/papers/hu-2023-gc-auxiva-iss-realistic/full-text.md
  - https://doi.org/10.1109/AICIT59054.2023.10277765
  - zotero://select/items/0_6EQ7692Y
tags:
  - blind-source-separation
  - independent-vector-analysis
  - speech-enhancement
  - direction-of-arrival
  - hearing-aids
  - real-world-evaluation
---

# Hu & Chen 2023: The Performance of GC-AuxIVA-ISS Method in a Realistic Environment

**Authors**: [[entities/ziyi-hu|Ziyi Hu]]¹, [[entities/wang-chen|Wang Chen]]¹ (corresponding)
**Affiliations**: ¹Hunan ChipHearing Semiconductor Co., Ltd., Changsha, China
**Venue**: 2023 International Conference on Advanced Communication and Information Technologies (AICIT), IEEE
**Year**: 2023
**Type**: Conference paper (reproduction & evaluation study)
**DOI**: [10.1109/AICIT59054.2023.10277765](https://doi.org/10.1109/AICIT59054.2023.10277765)
**Zotero**: [Open in Zotero](zotero://select/items/0_6EQ7692Y)

## Summary

This paper is an independent industrial reproduction and real-world evaluation of **GC-AuxIVA-ISS** ([[sources/goto-2022-offline-iss-gciva|Goto et al. 2022]]), the inverse-free geometrically constrained IVA algorithm, motivated by hearing-aid applications. The authors re-implemented the method and tested it in simulation (4 sources, 4-mic linear array) and in three realistic recording scenes: two loudspeakers in an anechoic chamber, human voices plus bubble noise in a meeting room (RT60 ≈ 600 ms, 70 dBA noise), and two voices outdoors (~60 dBA background). Simulation confirms the published behavior — the geometric constraints raise SIR from 11.09 to 14.82 dB and enable exact output-channel-order control. Realistic recordings show the method works well in low-reverberation conditions (anechoic, outdoor: DoA estimates within ~1° of truth, clean separation, controllable output order), but in the noisy reverberant meeting room the DoA estimation fails for the two-speaker case and separated outputs remain contaminated, leading the authors to conclude that BSS alone cannot handle such conditions and must be accompanied by dereverberation and denoising pre/post-processing.

## Problem Formulation

Determined BSS setting with $N = M$ sources and microphones. STFT-domain observations $\boldsymbol{x}(\omega, t) \in \mathbb{C}^N$ and estimates $\boldsymbol{y}(\omega, t) = \boldsymbol{W}(\omega)\,\boldsymbol{x}(\omega, t)$ with demixing matrix $\boldsymbol{W}(\omega) = [\boldsymbol{w}_1(\omega), \dots, \boldsymbol{w}_N(\omega)]^{\mathsf{H}}$. [[concepts/independent-vector-analysis|IVA]] minimizes

$$
J_{\mathrm{IVA}}(\mathcal{W}) = \sum_{m=1}^{M} \mathbb{E}\left[ G(\boldsymbol{y}_m(t)) \right] - \sum_{\omega=1}^{\Omega} \log|\det \boldsymbol{W}(\omega)|,
$$

with the spherical contrast function $G(\boldsymbol{y}_m) = G_R(r_m)$, $r_m = \sqrt{\sum_\omega |y_m(\omega, t)|^2}$. The geometric constraint (from [[concepts/geometrically-constrained-iva|GC-AuxIVA]], Li & Koishida 2020, inspired by [[concepts/lcmv-beamformer|LCMV beamforming]]) restricts the far-field response of each demixing filter:

$$
J_c(\mathcal{W}) = \sum_{m=1}^{M} \lambda_m \sum_{\omega=1}^{\Omega} \left| \boldsymbol{w}_m^{\mathsf{H}}(\omega)\, \boldsymbol{d}_m(\omega, \theta) - c_m \right|^2,
$$

with steering vector $\boldsymbol{d}_m(\omega, \theta)$, nonnegative constraint value $c_m$, and weight $\lambda_m$. The total objective is $J(\mathcal{W}) = J_{\mathrm{IVA}}(\mathcal{W}) + J_c(\mathcal{W})$.

The paper addresses the gap that GC-AuxIVA-ISS had only been validated in simulated reverberant conditions, not with real recordings — a prerequisite for hearing-aid deployment, where the outer order permutation problem (undetermined output order of separated sources) must be solved to deliver the target speech at a fixed output channel.

## Methodology

The paper contributes no new algorithm; it re-implements GC-AuxIVA-ISS and evaluates it. The reproduced update rules are summarized here as the authors present them.

### GC-AuxIVA-ISS Updates

Following [[sources/goto-2022-offline-iss-gciva|Goto et al. 2022]], [[concepts/iterative-source-steering|ISS]] replaces the row-wise VCD update (which needs a per-source, per-frequency matrix inversion) with a rank-1 update of the whole demixing matrix:

$$
W_f \leftarrow W_f - v_{mf}\, w_{mf}^{\mathsf{H}},
$$

where $\boldsymbol{v}_{mf}$ is computed in closed form. For the off-diagonal case ($m \neq n$):

$$
v_{nm} = \frac{\sum_t \varphi(r_{nt})\, y_{nt} y_{mt}^{*} + 2 \sum_{\theta \in \Theta} \lambda_{n\theta}\, g_{m\theta}^{*} (g_{n\theta} - c_{n\theta})}{\sum_t \varphi(r_{nt})\, |y_{mt}|^2 + 2 \sum_{\theta \in \Theta} \lambda_{n\theta} |g_{m\theta}|^2},
$$

with far-field response $g_{m\theta} = \boldsymbol{w}_m^{\mathsf{H}} \boldsymbol{d}_\theta$ and $\varphi(r) = G_R'(r)/r$. For the diagonal case ($m = n$), with $\alpha_m = \sum_t \varphi(r_{mt}) |y_{mt}|^2 + 2\sum_\theta \lambda_{m\theta} |g_{m\theta}|^2$ and $\beta_m = \sum_{\theta} \lambda_{m\theta} c_{m\theta} g_{m\theta}$:

$$
v_{mm} = \begin{cases} 1 - \alpha_m^{-1/2} & (\beta_m = 0), \\ 1 - \beta_m^{*} \dfrac{|\beta_m| + \sqrt{|\beta_m|^2 + \alpha_m}}{\alpha_m\, |\beta_m|} & (\beta_m \neq 0). \end{cases}
$$

Outputs and responses then update by the same rank-1 algebra, $\boldsymbol{y}_t \leftarrow \boldsymbol{y}_t - \boldsymbol{v}_m y_{mt}$ and $\boldsymbol{w}_n^{\mathsf{H}}\boldsymbol{d}_\theta \leftarrow \boldsymbol{w}_n^{\mathsf{H}}\boldsymbol{d}_\theta - v_{nm}\, \boldsymbol{w}_m^{\mathsf{H}}\boldsymbol{d}_\theta$ — no matrix inversion anywhere.

### DoA Estimation from the BSS System

Because the BSS system can be viewed as a set of beamformers, the DoA of the $m$-th output channel is read off the demixing filter directly:

$$
\hat{\theta}_m = \underset{\theta}{\mathrm{argmin}} \sum_{\omega=1}^{\Omega/2} \left| w_m^{\mathsf{H}}(\omega)\, d(\omega, \theta) \right|,
$$

i.e., the direction the filter responds to least (a spatial null in the interference direction; equivalently the beamformer's look direction for the target). This [[concepts/direction-of-arrival-estimation|DoA estimate]] is the bridge in the evaluation protocol: AuxIVA-ISS estimates the source directions, which are then fed to GC-AuxIVA-ISS as the constraint set $\Theta$ that pins the output order.

### Evaluation Protocol

Three steps, applied identically in simulation and realistic recordings: (I) estimate the DoA of each source with (unconstrained) AuxIVA-ISS; (II) compare estimated DoAs with the true arrangement; (III) use the estimated DoAs as GC-AuxIVA-ISS constraints to control the output channel order.

## Experimental Setup

| Item | Setting |
|------|---------|
| Sampling / STFT | 16 kHz; Hanning window 32 ms, 16 ms shift |
| **Simulation** | 4 speakers × 15 s (spatial-enhancement corpus of Fernandez et al. 2022); 4-source, 4-channel linear array, 3 cm spacing, RT60 = 50 ms (anechoic-like); source DoAs Θ = [−52°, −27°, 10°, 70°] (female English, female Danish, male English, male Danish) |
| **Anechoic chamber** | 2 loudspeakers ~1 m from the array (male Chinese + female Danish, ~11 s); 4-mic array, 3.5 cm spacing, middle two mics used (2×2 determined); true DoAs ≈ 4° and −32° |
| **Meeting room** | 2 human voices (male + female Chinese) + 2 loudspeakers with stationary bubble noise at ~70 dBA; RT60 ≈ 600 ms; 4-channel separation used |
| **Outdoor** | 2 male Chinese voices + background noise ~60 dBA; open ground, very small RT60 |
| Compared methods | AuxIVA-ISS vs. GC-AuxIVA-ISS (null constraint) |
| Metrics | SIR, SAR via bss-eval (simulation only — no true sources available for real recordings); DoA estimation error; output-order control (informal listening) |

![[raw/papers/hu-2023-gc-auxiva-iss-realistic/figures/9c46da27994b65109361e012e3dc9ef9c51f7cbdbb1f0330de1f12846110565f.jpg|Sources and microphone positions in simulation]]
*Figure 1: Source and microphone positions in the simulation (4 sources, 4-mic linear array, 3 cm spacing).*

![[raw/papers/hu-2023-gc-auxiva-iss-realistic/figures/0564bd6bbdf97ce04a9ae473432db66dc9110892cea07b9e834ccab5c91b1927.jpg|Anechoic chamber setup]]
![[raw/papers/hu-2023-gc-auxiva-iss-realistic/figures/decf135be5f7b21261db320e12ae70d697f69f55b8f634d2097a56ca850a63cc.jpg|Meeting room and outdoor setups]]
*Figure 4: Source and microphone positions for the realistic recordings — anechoic chamber (top), meeting room and outdoor condition (bottom).*

## Results

### Simulation

**Separation (Table I).** The geometric constraints improve separation on top of ISS updates (values as printed in Table I; note the body text mislabels these columns "SDR and SIR" while the table header reads SIR/SAR):

| Method | SIR [dB] | SAR [dB] |
|--------|----------|----------|
| AuxIVA-ISS | 11.09 | 7.97 |
| GC-AuxIVA-ISS (null) | **14.82** | **8.21** |

**DoA estimation (Fig. 2).** The AuxIVA-ISS-extracted DoA map shows peaks matching the arranged directions almost exactly; each output channel locks onto a distinct source (channel 1 → −27°, channel 2 → ~71°, channel 3 → 10°, channel 4 → −52°), and the estimated output order matched listening.

![[raw/papers/hu-2023-gc-auxiva-iss-realistic/figures/d84270a6fdf0e4760df41dfefb3345cf1b95b9a7792716ae0c74007daa0ad9d5.jpg|DoA extracted by AuxIVA-ISS in simulation]]
*Figure 2: DoA extracted by AuxIVA-ISS in simulation — peaks coincide with the arranged source directions.*

**Output-order control (Fig. 3).** With constraints $\Theta_L = [-27°, 70°, 10°, -52°]$ (top row) the GC output order matches plain AuxIVA-ISS; swapping the constraints for channels 1 and 3 ($\Theta_R = [10°, 70°, -27°, -52°]$, bottom row) swaps exactly those two output channels while channels 2 and 4 stay fixed — the order is fully controllable by the constraint arrangement.

![[raw/papers/hu-2023-gc-auxiva-iss-realistic/figures/c1409e8c55396d6397c1f4459cad3ebb6e97a5defd3edeb5856ecd7e90311d97.jpg|Output channel order control in simulation]]
*Figure 3: Output-channel-order control by GC-AuxIVA-ISS in simulation — exchanging the constraint DoAs of channels 1 and 3 swaps exactly those outputs.*

### Realistic Recordings

**Anechoic chamber (Fig. 5).** Estimated DoAs: channel 1 → 3°, channel 2 → −31°, against true ~4° and −32° — within ~1° of the physical arrangement. Output-order control confirmed, matching the simulation behavior.

![[raw/papers/hu-2023-gc-auxiva-iss-realistic/figures/1ac11a99a18996a97fedabe0e0e79f6b28d6e6466a7381087fbce6af745dd167.jpg|DoA estimates, anechoic chamber, channel 1]]
![[raw/papers/hu-2023-gc-auxiva-iss-realistic/figures/980660fd4358a9eb95b388b46e733c38f840e4c46485519686decd7f1b3a2944.jpg|DoA estimates, anechoic chamber, channel 2]]
*Figure 5: DoA extracted by AuxIVA-ISS in the anechoic chamber — 3° and −31° vs. true ~4° and −32°.*

**Meeting room (RT60 ≈ 600 ms, 70 dBA bubble noise).** With one voice + bubble noise, 4-channel separation puts the target male voice in channel 1 (remaining channels: noise) and its DoA is correctly estimated, so the order can be controlled. With two speakers, however, **AuxIVA-ISS cannot produce a correct DoA estimate** — only the louder male voice is localized; separation still partially works but the outputs are mixed with bubble noise, and the high diffuse-noise + reverberation level prevents DoA-based order control entirely.

**Outdoor (best realistic result, Fig. 6).** DoA peaks are obvious and the output order is successfully controlled with the estimated DoAs; each separated channel is "clean and clear," mixed only with a little background noise that the authors deem easily removable in post-processing.

![[raw/papers/hu-2023-gc-auxiva-iss-realistic/figures/08711a4e63a3986ddec999736d0b6e227f9e52b1e59249f4de1ed94b9a1c06e5.jpg|DoA estimates, outdoor, channel 1]]
![[raw/papers/hu-2023-gc-auxiva-iss-realistic/figures/f84235d31c36e31043ad801f4f3b166c54b46ec66b5409cc8e36e1f1118d732a.jpg|DoA estimates, outdoor, channel 2]]
*Figure 6: DoA extracted by AuxIVA-ISS outdoors — distinct peaks, successfully used for output-order control.*

*(Figure 7, the outdoor output-order-control spectrograms, was not extracted as a raster image by MinerU.)*

### Interpretation of the Failure Case

Following Scheibler & Ono 2019 (IVA with more microphones than sources), maximum-likelihood BSS automatically picks the *strongest* sources because they have strongly non-Gaussian distributions, while the mixture of noise and weaker sources is closer to Gaussian and thus not extracted. The meeting-room failure indicates that real bubble noise plus reverberation is *not Gaussian enough* — it competes with speech as an extracted "source", corrupting both separation and the DoA estimates.

## Key Contributions

1. **Independent reproduction**: confirms that GC-AuxIVA-ISS — IVA + beamforming-based geometric constraints + inverse-free ISS rank-1 updates — is reproducible outside the originating group, with simulation behavior (SIR gain from constraints, exact output-order control) matching the original report.
2. **First realistic-environment evaluation across three daily scenes**: anechoic chamber, highly reverberant meeting room (RT60 ≈ 600 ms, 70 dBA diffuse noise), and outdoor — using small linear arrays (3–3.5 cm spacing) directly relevant to hearing-aid form factors.
3. **Boundary of applicability**: identifies the noisy-reverberant regime as where the method breaks — DoA estimation fails with two speakers, separated outputs stay contaminated — and explains it via the Gaussianity argument (noise not Gaussian enough to be ignored by the ML criterion).
4. **Practical guidance for hearing-aid BSS**: single-stage BSS is insufficient in realistic adverse conditions; dereverberation and denoising pre/post-processing must accompany it.

## Related Concepts

- [[concepts/geometrically-constrained-iva|Geometrically Constrained IVA]]
- [[concepts/iterative-source-steering|Iterative Source Steering]]
- [[concepts/independent-vector-analysis|Independent Vector Analysis]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/direction-of-arrival-estimation|Direction of Arrival Estimation]]
- [[concepts/lcmv-beamformer|LCMV Beamformer]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/permutation-alignment|Permutation Alignment]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Related Synthesis

- (No dedicated synthesis page yet; this real-world validation contributes to the emerging picture of where constrained BSS breaks down in practice — candidate topics: real-world robustness of BSS/beamforming pipelines, BSS + dereverberation/denoise cascades for hearing aids.)
