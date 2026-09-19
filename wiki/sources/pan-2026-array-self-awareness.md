---
type: source
created: 2026-09-19
updated: 2026-09-19
sources:
  - raw/papers/pan-2026-array-self-awareness/full-text.md
  - https://doi.org/10.1109/TASLPRO.2026.3653137
  - zotero://select/items/0_DC6MK8NM
tags:
  - microphone-arrays
  - array-processing
  - covariance-matrix-modeling
  - source-extraction
  - speech-enhancement
  - signal-processing
---

# Pan, Chen & Benesty 2026: Microphone Array Self-Awareness via a Residual Model of the Covariance Matrix

**Authors**: [[entities/chao-pan|Chao Pan]], [[entities/jingdong-chen|Jingdong Chen]], [[entities/jacob-benesty|Jacob Benesty]]
**Institution**: Northwestern Polytechnical University, Xi'an, China; University of Quebec, INRS-EMT, Montreal, Canada
**Venue**: IEEE Transactions on Audio, Speech, and Language Processing, 2026
**Type**: Journal article
**DOI**: [10.1109/TASLPRO.2026.3653137](https://doi.org/10.1109/TASLPRO.2026.3653137)
**Zotero**: [Local library](zotero://select/items/0_DC6MK8NM)

## Summary

This paper inverts the classical source-extraction paradigm: instead of defining the *desired* source (by direction, RTF, or coherence matrix) and treating everything else as noise, it defines the *interferences and background noise* through their a priori coherence matrices and treats everything that does not match them as the desired source. The covariance-matrix residual — what remains of $\Phi_{\mathbf{y}}(t)$ after subtracting the modeled interference-plus-noise contribution — is given a parametric model from which the coherence matrix $\Gamma_{\xi}$ of an unknown, newly emerging source is recovered in real time, frame by frame. A two-stage framework then computes the Wiener filter $H_{\mathrm{SA}}(t)$ that detects and extracts new sources — moving sources, sporadic sound events (glass breaking, dog barking), and sources under count uncertainty — without any prior information about them.

## Problem Formulation

In the STFT domain, an $M$-sensor array observes $N$ sources plus background noise. With a *new, a-priori-unknown* source $\boldsymbol{\xi}(t)$ present, the observation vector and its covariance matrix are

$$
\mathbf{y}(t) = \boldsymbol{\xi}(t) + \sum_{n=1}^{N+1} \mathbf{x}_n(t), \qquad
\Phi_{\mathbf{y}}(t) = \phi_{\xi}(t)\,\Gamma_{\xi} + \sum_{n=1}^{N+1} \phi_{X,n}(t)\,\Gamma_{\mathbf{x},n},
$$

where each component's covariance is factored as a time-varying variance $\phi$ times a time-invariant coherence matrix $\Gamma$ (source images modeled via impulse responses in (3)). The covariance matrix is estimated with the first-order recursion

$$
\Phi_{\mathbf{y}}(t) = \alpha\,\Phi_{\mathbf{y}}(t-1) + (1-\alpha)\,\mathbf{y}(t)\mathbf{y}^{H}(t), \qquad \alpha \in (0,1)
$$

(typically $\alpha = 0.9$–$0.98$). Extracting the new source with the multichannel [[concepts/wiener-filter|Wiener filter]]

$$
H_{\xi}(t) = \frac{\phi_{\xi}(t)}{\phi_{\xi}(t) + \sum_{n=1}^{N+1} \phi_{X,n}(t)}
$$

requires $\phi_{\xi}(t)$, which in turn requires the unknown $\Gamma_{\xi}$. The paper's objective is to *model the residual* $\phi_{\xi}(t)\Gamma_{\xi} = \Phi_{\mathbf{y}}(t) - \sum_{n=1}^{N+1}\phi_{X,n}(t)\Gamma_{\mathbf{x},n}$ so that $\Gamma_{\xi}$ emerges automatically from the observations — giving the array "self-awareness" of sources it has never seen. The motivating question, inspired by echo cancellation and spectral subtraction: *can we extract source signals by defining the interferences and background noise?*

## Methodology

### Residual Model of the Covariance Matrix

Consider first the special case with no known sources, where only the background-noise coherence matrix $\Gamma_{\mathbf{x}}$ is known a priori (typically diffuse noise, with sinc elements $\sin(\omega d_{i,j}/c)/(\omega d_{i,j}/c)$, $c = 340$ m/s). With the eigendecomposition $\Gamma_{\mathbf{x}} = \mathbf{Q}\boldsymbol{\Lambda}\mathbf{Q}^{H}$, the paper models the transformed coherence matrix of the new source by **separating amplitude and phase**:

$$
\mathbf{Q}^{H}\Gamma_{\xi}\mathbf{Q} = \left(\mathbf{a}\mathbf{a}^{T}\right) \odot e^{\mathcal{J}\mathbf{P}},
$$

where $\mathbf{a} = [A_1 \cdots A_M]^{T}$ with $A_m > 0$, $\mathcal{J}$ is the imaginary unit, and $\mathbf{P}$ is a symmetric phase matrix with elements in $[0, 2\pi]$.

- **Phase**: since $\boldsymbol{\Lambda}$ is diagonal with nonnegative real entries, the phase of $\mathbf{Q}^{H}\Gamma_{\xi}\mathbf{Q}$ equals that of the observable $\mathbf{Q}^{H}\Phi_{\mathbf{y}}(t)\mathbf{Q}$, giving $\mathbf{P} = \angle[\mathbf{Q}^{H}\Phi_{\mathbf{y}}(t)\mathbf{Q}]$ in closed form.
- **Amplitude**: the off-diagonal magnitudes satisfy $A_i A_j \propto |\mathbf{q}_i^{H}\Phi_{\mathbf{y}}(t)\mathbf{q}_j|$. The optimal $A_i$'s minimize Csiszár's I-divergence

$$
\mathcal{I}(\mathbf{a}) = -\sum_{i=1}^{M}\sum_{j\neq i}\left[\left|\mathbf{q}_i^{H}\Phi_{\mathbf{y}}(t)\mathbf{q}_j\right|\ln(A_iA_j) - A_iA_j\right],
$$

which has no closed-form solution but yields the fixed-point update

$$
A_i \leftarrow \frac{B_i}{\sum_{j\neq i} A_j}, \qquad B_i \triangleq \sum_{j\neq i}\left|\mathbf{q}_i^{H}\Phi_{\mathbf{y}}(t)\mathbf{q}_j\right|,
$$

initialized at $A_i = \sqrt{B_i/(M-1)}$. The iteration converges rapidly (1000 random-init simulations all reach the ground truth; max 20 iterations in practice). Finally, $\Gamma_{\xi}$ is repaired by removing negative eigenvalues and rescaling so its trace equals $M$. See [[concepts/covariance-matrix-residual-model|Covariance Matrix Residual Model]].

![[raw/papers/pan-2026-array-self-awareness/figures/1c6525d3a593c66e79c53bdfc037aaf46ad92e673a834bee2729dff760f01a9e.jpg|Illustration of the matrix decomposition and residual model]]
*Figure 1: The matrix decomposition and residual model — $\Phi_{\mathbf{y}}(t)$ is split into the modeled noise term $\phi_X(t)\Gamma_{\mathbf{x}}$ (diagonalized by the eigenvectors $\mathbf{Q}$ of $\Gamma_{\mathbf{x}}$) and the residual $\phi_{\xi}(t)\Gamma_{\xi}$ of the new source.*

### General Case with N Known Sources

With $N$ known sources, the total interference-plus-noise contribution is compressed into a single equivalent term: rough variances $\phi_{X,n}(t)$ are first estimated from the known coherence matrices (maximum-likelihood variance function $f_{\mathrm{V}}[\cdot]$ of the authors' previous work), the Wiener filters $H_n(t) = \phi_{X,n}(t)/\sum_i \phi_{X,i}(t)$ are formed, and the **total coherence matrix**

$$
\Gamma_{\mathbf{x}} = \sum_{n=1}^{N+1} H_n(t)\,\Gamma_{\mathbf{x},n}, \qquad \phi_X(t) = \sum_{n=1}^{N+1}\phi_{X,n}(t)
$$

substitutes into the same residual-model machinery, reducing the general case to the special case.

### Two-Stage Array Self-Awareness Framework

The full framework (Figure 2) runs two stages per frame:

1. **Stage 1** — estimate the variances of the known interferences and background noise from $\Phi_{\mathbf{y}}(t)$ and the known $\Gamma_{\mathbf{x},n}$'s; build the total coherence matrix $\Gamma_{\mathbf{x}}$.
2. **Stage 2** — compute the residual model to obtain $\Gamma_{\xi}$, then re-estimate *all* variances (including $\phi_{\xi}(t)$) with $\Gamma_{\xi}$ appended, yielding the new-source Wiener filter $H_{\xi}(t)$.

Because the residual model "overfits" at onsets — the direct path and very early reflections of a known source are not yet well described by its full-reflection coherence matrix, so some known-source energy leaks into $\Gamma_{\xi}$ — the final **self-awareness Wiener filter** multiplies in an a priori gate from Stage 1:

$$
H_{\mathrm{SA}}(t) = H_{\xi}(t) \times H_{\mathrm{a priori}}(t), \qquad H_{\mathrm{a priori}}(t) = 1 - \max_{n\in\{1,\ldots,N\}} H_n(t).
$$

$H_{\mathrm{SA}}(t) \in [0,1]$ behaves as a detection probability: it approaches 1 when a new source dominates the current time-frequency bin and 0 otherwise. A fundamental limitation is stated explicitly: a new source whose coherence matrix is very close to that of a known source cannot (and, from the self-awareness standpoint, should not) be detected. See [[concepts/array-self-awareness|Array Self-Awareness]].

![[raw/papers/pan-2026-array-self-awareness/figures/a0c286096e960e588d3b495ce2b83668844075b499df512d3b3e1cfd3741ebd2.jpg|Framework of the array self-awareness]]
*Figure 2: Framework of the array self-awareness — inputs are $\Phi_{\mathbf{y}}(t)$ and the known coherence matrices $\Gamma_{\mathbf{x},n}$; $f_{\mathrm{V}}[\cdot]$ calculates source variances and $f_{\mathrm{MR}}[\cdot]$ the residual model; the output is the Wiener filter of the new emerging source.*

## Experimental Setup

| Item | Setting |
|------|---------|
| Room | 6 m × 4 m × 3 m; image-method RIRs; wall reflection coefficients 0.9, ceiling/floor 0.45 |
| Array | 6-sensor uniform linear array at room center (first sensor at (3, 2, 1)), 2 cm spacing |
| Sources | New source at (4, 2, 1); interferences at (2, 2, 1) and (2.5, 2.8, 1); moving-source path from (4, 2, 1) right-to-left (RIRs interpolated between nearest sampled positions) |
| Background noise | Diffuse + white, 20 dB below interference level |
| Conditions | INR 20 dB; input SIR ≈ 0 dB (feasibility study: 3.1 dB) |
| BSS experiment | Measured RIRs (Northwestern Polytechnical University); sources at 0° (constant interference), 90° (0–10 s), 180° (10–30 s), 1 m from array; sensor offsets 1.3–9.1 cm from reference; diffuse noise at 20 dB SNR |
| Baselines | Recursive AuxIVA and recursive ILRMA (2 s offline initialization, then recursive updates), both at window length $L_w = 2048$; proposed method uses $L_w = 256$ |
| Complexity reference | $Q = 4$ iterations, $f_s = 16$ kHz, $L_w = 256$, $L_s = 64$ |

![[raw/papers/pan-2026-array-self-awareness/figures/7060606ef9615231420b0523b0e81ebe52327f3f77125cd62a1e102513f5893d.jpg|Positions of the source and interferences in the room]]
*Figure 3: Room geometry — gray circles mark the candidate source positions used for the position-dependent evaluation of Figure 7.*

## Results

### Two-Stage Behavior and False-Alarm Suppression

Figure 4 walks through the two stages: Stage-1 Wiener filters for the interference and noise (panel a), Stage-2 filters (panels d–f), and the final extraction. The a priori gate $H_{\mathrm{a priori}}(t)$ eliminates the false alarms caused by direct paths and early reflections of the interference in the first frames after silence (visible when comparing the self-awareness output with the raw Stage-2 filter). Applying $H_{\mathrm{SA}}$ to the observations extracts the new source at **13.9 dB output SIR from a 3.1 dB input SIR**, with no information about the new source used at any point.

![[raw/papers/pan-2026-array-self-awareness/figures/25d3fc485990078e919850fbfd0f61756720c1769b5f407ccb6c3b6cd982973f.jpg|Stage-1 Wiener filter of the interference]]
(a) Stage-1 Wiener filter of the interference.

![[raw/papers/pan-2026-array-self-awareness/figures/03ae5583e889dd46e693c360f921cc67756d6a4cfa2aa262dc69740bc791958b.jpg|Stage-2 Wiener filter of the new source]]
(f) Stage-2 Wiener filter of the new source $H_{\xi}(t)$.

![[raw/papers/pan-2026-array-self-awareness/figures/4375b326b8c75680204d18082209d2f7ee27640db272a2f91255cc5a2cf2a990.jpg|Array observation]]
(g) Array observation.

![[raw/papers/pan-2026-array-self-awareness/figures/9437c08f740f7ee534a1ee1ffa1ff1cc438fb531b1af06e5d546974364a71e55.jpg|Ground truth of the new source]]
(h) Ground truth of the new source.

![[raw/papers/pan-2026-array-self-awareness/figures/532f06f82cf0f67933786602a08dbcb6f33aa7848728cd13fd4312e28f43782d.jpg|Extracted new source]]
(i) Extracted new source through the proposed approach.

*Figure 4: Results of the array self-awareness at different stages (selected panels). Full relationships: (a)+(b)=1, (d)+(e)+(f)=1, (c)=(f)×(b) is the self-awareness filter, and (i)=(g)×(c).*

### Moving Sources and Sporadic Sound Events

Precisely the sources that are hardest for coherence-based methods — moving sources (time-varying impulse responses, so the coherence matrix never has enough stationary frames to be estimated) and sporadic events (glass breaking, dog barking — too short to estimate a coherence matrix) — are handled automatically, because the method never needs *their* coherence matrix as input:

| Scenario | Input SIR | Output SIR |
|----------|-----------|------------|
| Moving source | 0 dB | **11.4 dB** |
| Glass breaking | 6.6 dB | **28.2 dB** |
| Dog barking (woofing) | 1.7 dB | **16.6 dB** |

![[raw/papers/pan-2026-array-self-awareness/figures/868c655e1235bdd1143fd89908f26fd54ec754972321df13adcd0a1df4088e27.jpg|Spectrogram of the array observations with the moving source]]
(a) Spectrogram of the array observations with the moving source.

![[raw/papers/pan-2026-array-self-awareness/figures/2d0d73e2229a0f19cf902628f163a0a55e5471826c09fba14ccdf2899b6f4f02.jpg|Array self-awareness with the moving source]]
(b) The corresponding array self-awareness $H_{\mathrm{SA}}(t)$.

![[raw/papers/pan-2026-array-self-awareness/figures/846c77e1e45581ea1ce2666149bc5ebdd72b3e448cb9563b3f81a0928573c465.jpg|Extracted moving source]]
(c) The extracted moving source, $(\mathrm{a}) \times (\mathrm{b})$.

*Figure 5 (selected panels): Array self-awareness in the presence of a moving source. The same pattern holds for the glass-breaking and dog-woofing sporadic events.*

### Robustness to Source-Count Uncertainty

With three sources present in segments where the algorithm assumes a different active count (all three active; one assumed-extra interference; no interference but two assumed; one interference and no new source), the method keeps extracting the new source correctly, and $H_{\mathrm{SA}}$ stays low when no new source is present — the array output naturally falls silent rather than hallucinating a source.

![[raw/papers/pan-2026-array-self-awareness/figures/4d331452679c5a639409a917879dd3e0dba07f5dc57186aa63b2801cfabeb87a.jpg|Results in the presence of uncertainty in the number of sources]]
*Figure 6: Self-awareness under source-count uncertainty — #1 is the new source, #2/#3 are interferences; the waveform of the new source is superimposed on the output spectrum as reference.*

### Position-Dependent Performance: Reverberation Helps

Sweeping the source over the candidate positions (Figure 7), the output SIR exceeds 15 dB for many positions in the reverberant environment. Failure occurs only when the source is very close to an interference (whose coherence matrix then becomes similar), with a symmetric failure region around the array axis (linear-array manifold symmetry). Crucially, **the failure region is significantly smaller and the maximum SIR improvement larger in the reverberant room than in the anechoic one** — reflections enrich the coherence matrices and make sources easier to distinguish, inverting the usual "reverberation degrades beamforming" intuition.

![[raw/papers/pan-2026-array-self-awareness/figures/a55dddae3b57ae5b8bfbd10573f73ad1123c914c30374ec50ca689eae663d84a.jpg|Output SIR as a function of source positions, reverberant environment]]
(a) Reverberant environment.

![[raw/papers/pan-2026-array-self-awareness/figures/c34cc2003a46b3c452f3b313232ae06604952b182ae207924ab24921ae155ef1.jpg|Output SIR as a function of source positions, anechoic environment]]
(b) Anechoic environment.

*Figure 7: Output SIR as a function of source positions (input SIR 0 dB; red star = interference; red circle = array, no evaluation inside). Reverberation shrinks the failure region.*

### Combination with BSS

The required interference coherence matrices can be estimated blindly: offline ILRMA on past observations yields a demixing matrix from which the impulse responses (and hence coherence matrices) are extracted. In a source-switching experiment (desired source changes at 10 s), recursive AuxIVA and ILRMA (window $L_w = 2048$) perform well initially but need **more than 5 seconds** to re-converge after the switch, while the proposed method adapts almost immediately — and with an 8× smaller window ($L_w = 256$), dramatically reducing system delay. BSS output SIR degrades rapidly for shorter windows, explaining the 2048-sample choice for the baselines.

![[raw/papers/pan-2026-array-self-awareness/figures/982f99f17bca535dfc84e2e75e3668db702c159773bd14328b9c0fb61edf5d80.jpg|Output SIRs of recursive AuxIVA and ILRMA as a function of window length]]
*Figure 8(b): Output SIRs of recursive AuxIVA and ILRMA as a function of window length — short windows cripple the BSS baselines.*

![[raw/papers/pan-2026-array-self-awareness/figures/0f43c434bc1caa62c69ad7c03b602493096b1b54cc7affb0afe6af12c042e82e.jpg|SIR of the proposed approach compared with recursive AuxIVA]]
(b) SIR vs. recursive AuxIVA.

![[raw/papers/pan-2026-array-self-awareness/figures/f2996307d6fc42bda7f05aa4ec44d4b0ee3f52bf4f66844e48c9f7205a5b9d8e.jpg|SIR of the proposed approach compared with recursive ILRMA]]
(c) SIR vs. recursive ILRMA.

*Figure 9 (selected panels): After the desired source switches at 10 s, the BSS baselines need >5 s to re-converge; the proposed approach tracks the new source immediately.*

### Complexity

Per-iteration cost of the variance update is $c(M,N) = M^2[M + 2N + 1 + N(N+1)/2 + N^3/M^2]$ multiplications; with both stages, $Q = 4$ iterations, $f_s = 16$ kHz, $L_w = 256$, $L_s = 64$, the total stays **below 200 MMacs/s for six sensors** — real-time friendly.

![[raw/papers/pan-2026-array-self-awareness/figures/7c3a7995c0a40301a9ca8928c41aa2eb59932397a5fd877c67cbe540625db2a4.jpg|Computational cost as a function of M]]
*Figure 11: Computational cost of the array self-awareness as a function of the number of sensors under different numbers of interferences.*

## Key Contributions

1. **Paradigm inversion for source extraction**: defines the *unwanted* components (interferences + background noise via a priori coherence matrices) rather than the desired source, inspired by echo cancellation / spectral subtraction — any signal deviating from the known model is extracted as "new".
2. **Residual model of the covariance matrix**: a parametric model of $\mathbf{Q}^{H}\Gamma_{\xi}\mathbf{Q}$ with amplitude ($\mathbf{a}\mathbf{a}^{T}$ rank-1 magnitude structure) and phase (symmetric matrix $\mathbf{P}$) separated, recovering an unknown source's coherence matrix from a single frame's covariance estimate.
3. **Fixed-point amplitude estimation**: Csiszár-I-divergence minimization with a rapidly converging multiplicative update for the amplitude vector (verified over 1000 random initializations).
4. **Two-stage self-awareness framework with a priori gating**: $H_{\mathrm{SA}} = H_{\xi} \times (1 - \max_n H_n)$ suppresses onset false alarms caused by direct-path/early-reflection leakage of known sources into the residual model.
5. **Demonstrated robustness**: automatic extraction of moving sources, sporadic events, and sources under count uncertainty; the counterintuitive finding that **reverberation improves** new-source detectability (richer coherence matrices); and a BSS combination (offline ILRMA for blind a priori estimation) with 8× smaller window and instant re-convergence where recursive BSS needs seconds.

## Related Concepts

- [[concepts/array-self-awareness|Array Self-Awareness]]
- [[concepts/covariance-matrix-residual-model|Covariance Matrix Residual Model]]
- [[concepts/spatial-covariance-matrix|Spatial Covariance Matrix]]
- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/wiener-filter|Wiener Filter]]
- [[concepts/blind-source-separation|Blind Source Separation]]
- [[concepts/blind-source-extraction|Blind Source Extraction]]
- [[concepts/independent-low-rank-matrix-analysis|Independent Low-Rank Matrix Analysis]]
- [[concepts/image-source-method|Image-Source Method]]

## Related Synthesis

- [[synthesis/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]
