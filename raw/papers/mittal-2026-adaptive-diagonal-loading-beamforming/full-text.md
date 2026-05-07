###### Abstract

Reliable adaptive beamforming is critical for large microphone arrays operating in highly dynamic acoustic environments. In scenarios characterized by fast-moving talkers and interferers, the available sample support for estimating the spatial correlation matrix is often snapshot-deficient. This deficiency, coupled with array imperfections, degrades the White Noise Gain (WNG), leading to severe target signal cancellation. To ensure stable and robust beamforming, we propose a novel adaptive diagonal loading method that guarantees the WNG remains strictly within specified bounds. By leveraging the Kantorovich inequality, we map the desired WNG to a strict upper bound on the condition number of the correlation matrix. Furthermore, we present three estimation techniques for the adaptive loading level, ranging from trace-based bounding to exact eigenvalue decomposition, offering scalable computational complexities of $\mathcal{O}(M)$, $\mathcal{O}(M^{2})$, and $\mathcal{O}(M^{3})$. Our approach demonstrates highly stable beamforming under fast-changing interference.

## I Introduction

Adaptive beamforming techniques, such as the Minimum Power Distortionless Response (MPDR) and the Minimum Variance Distortionless Response (MVDR) [^2], are cornerstone algorithms in real time audio signal processing for noise reduction, dereverberation, and speech enhancement. These techniques achieve high spatial resolution by adapting their spatial filter weights to the second-order statistics of the received acoustic data. However, ensuring the robustness of these adaptive beamformers remains a significant challenge, particularly when deploying large microphone arrays in dynamic, real-world environments characterized by fast-moving interferers and talkers.

The fundamental vulnerability of optimal adaptive beamforming lies in its reliance on the sample Spatial Correlation Matrix (SCM) [^6]. To accurately track a fast-moving acoustic scene, the observation window used to estimate the SCM must be kept exceedingly short. When the number of available snapshots (frames) is less than or comparable to the number of microphone elements, the SCM becomes poorly conditioned or mathematically rank-deficient. Sample matrix inversion under this snapshot deficiency causes the spatial weights to become highly erratic. This phenomenon is exacerbated by inevitable array imperfections, such as sensor positioning errors, gain mismatches, and phase perturbations [^10]. Consequently, the adaptive beamformer exhibits extreme sensitivity to spatially uncorrelated noise, which manifests as a dramatic collapse in the White Noise Gain (WNG) and severe cancellation of the target signal [^3] [^11].

The classical remedy to mitigate SCM ill-conditioning and control the weight vector norm is Diagonal Loading (DL) [^15] [^4] [^13]. By adding a scaled identity matrix to the SCM prior to inversion, DL artificially inflates the spatial noise floor, effectively bounding the maximum condition number of the matrix. While standard DL is ubiquitous, selecting the optimal loading parameter $\mu$ is historically an ad-hoc process. Applying a fixed $\mu$ that is too large over-penalizes the adaptive degrees of freedom, transforming the MPDR beamformer back into a suboptimal delay-and-sum beamformer that fails to null strong interferers. Conversely, a $\mu$ that is too small fails to stabilize the matrix during severe snapshot deficiency, leading to signal distortion. Literature has proposed several robust beamforming techniques over the years to improve the beamformers response to mismatch [^1] [^5] [^14] [^16] [^9] [^7] [^12]. In this paper, we propose a dynamic, closed-form adaptive diagonal loading method that deterministically guarantees the WNG stays within specified bounds. By exploiting the strict mathematical relationship between the array’s WNG, the array gain, and the condition number of the SCM via the Kantorovich inequality, we derive an exact analytical requirement for the loading parameter at every frame.

Because computing the exact eigenvalues of the SCM to determine the necessary DL at every time step is computationally expensive for large arrays, we introduce three progressive bounding techniques for estimating the loading level. These techniques utilize trace-based bounding, the Gershgorin circle theorem, and exact eigenvalue decomposition, offering scalable computational complexities from $\mathcal{O}(M)$ to $\mathcal{O}(M^{3})$.

## II Signal Model

We consider a room acoustic environment capturing a group of $J$ active sound sources (target talkers and interferers) using an array of $M$ microphones. Following the narrowband multiplicative assumption in the Short-Time Fourier Transform (STFT) domain, the signal received at the $m$ -th microphone can be expressed as:

$$
y_{m}[i,k]=\sum_{j=1}^{J}h_{m,j}[k]s_{j}[i,k]+v_{m}[i,k]
$$

where $i$ is the time frame index, $k$ is the frequency bin index, $s_{j}[i,k]$ is the STFT of the $j$ -th source signal, $h_{m,j}[k]$ is the Acoustic Transfer Function (ATF) from source $j$ to microphone $m$, and $v_{m}[i,k]$ represents spatially uncorrelated additive sensor noise.

For brevity, we omit the frequency index $k$ in the subsequent vector formulation. Vectorizing across the $M$ microphones, the array signal model at frame $i$ is written as:

$$
\mathbf{y}[i]=\mathbf{H}\mathbf{s}[i]+\mathbf{v}[i]
$$

where $\mathbf{y}[i]\in\mathbb{C}^{M\times 1}$, $\mathbf{s}[i]\in\mathbb{C}^{J\times 1}$, and $\mathbf{H}\in\mathbb{C}^{M\times J}$ is the matrix of stacked acoustic transfer functions. For a target source of interest, we define the Relative Transfer Function (RTF) or steering vector as $\mathbf{d}\in\mathbb{C}^{M\times 1}$, normalized such that $\mathbf{d}^{H}\mathbf{d}=M$.

The MPDR beamformer seeks a weight vector $\mathbf{w}[i]\in\mathbb{C}^{M\times 1}$ that minimizes the output power while maintaining a distortionless response in the target direction:

$$
\min_{\mathbf{w}}\mathbf{w}^{H}\mathbf{R}_{y}\mathbf{w}\quad\text{s.t.}\quad\mathbf{w}^{H}\mathbf{d}=1
$$

where $\mathbf{R}_{y}=\mathbb{E}[\mathbf{y}\mathbf{y}^{H}]$ is the theoretical SCM. The well-known optimal solution is given by $\mathbf{w}_{opt}=\frac{\mathbf{R}_{y}^{-1}\mathbf{d}}{\mathbf{d}^{H}\mathbf{R}_{y}^{-1}\mathbf{d}}$.

In practice, the true SCM is unknown and must be approximated via a short sliding window to track moving sources:

$$
\hat{\mathbf{R}}_{y}[i]=\frac{1}{L}\sum_{l=0}^{L-1}\mathbf{y}[i-l]\mathbf{y}^{H}[i-l]
$$

When the window length $L$ is small ($L<M$), $\hat{\mathbf{R}}_{y}[i]$ is rank-deficient. Its minimum eigenvalues approach zero, causing the condition number to approach infinity and the inverse $\hat{\mathbf{R}}_{y}^{-1}$ to heavily amplify minor estimation errors and uncorrelated noise.

## III Proposed Method

### III-A WNG Bounds via Kantorovich Limits

The robustness of a beamformer to uncorrelated noise is quantified by its White Noise Gain (WNG), defined as the ratio of the output SNR to the input SNR in a spatially white noise field,

$$
W=\frac{\lvert\mathbf{w}^{H}\mathbf{d}\rvert}{\lvert\mathbf{w}^{H}\mathbf{w}\rvert}=\frac{1}{\lvert\mathbf{w}^{H}\mathbf{w}\rvert}
$$

where the second equality holds due to the distortionless constraint $\mathbf{w}^{H}\mathbf{d}=1$. In a snapshot-deficient MPDR beamformer, the norm of the weight vector $\|\mathbf{w}\|^{2}$ spikes dramatically, causing $W$ to plummet. To guarantee stable beamforming, we must enforce a strict lower bound, $W\geq W_{\min}$.

The weight norm for the MPDR beamformer can be rewritten in terms of the SCM:

$$
\mathbf{w}^{H}\mathbf{w}=\frac{\mathbf{d}^{H}\mathbf{R}_{y}^{-2}\mathbf{d}}{(\mathbf{d}^{H}\mathbf{R}_{y}^{-1}\mathbf{d})^{2}}
$$

To strictly bound this ratio, we leverage the Kantorovich inequality [^8]. For any Hermitian positive-definite matrix $\mathbf{R}$ with condition number $\kappa=\lambda_{\max}/\lambda_{\min}$, and for any non-zero vector $\mathbf{x}$, the general inequality states:

$$
\frac{(\mathbf{x}^{H}\mathbf{x})^{2}}{(\mathbf{x}^{H}\mathbf{R}\mathbf{x})(\mathbf{x}^{H}\mathbf{R}^{-1}\mathbf{x})}\geq\frac{4\kappa}{(\kappa+1)^{2}}
$$

To apply this to our beamforming problem, let $\mathbf{R}=\mathbf{R}_{y}$ and define the vector $\mathbf{x}=\mathbf{R}_{y}^{-1/2}\mathbf{d}$. Substituting these into the component terms of the inequality yields:

$$
\mathbf{x}^{H}\mathbf{x}=\mathbf{d}^{H}\mathbf{R}_{y}^{-1}\mathbf{d}
$$
 
$$
\mathbf{x}^{H}\mathbf{R}_{y}\mathbf{x}=\mathbf{d}^{H}\mathbf{R}_{y}^{-1/2}\mathbf{R}_{y}\mathbf{R}_{y}^{-1/2}\mathbf{d}=\mathbf{d}^{H}\mathbf{d}=M
$$
 
$$
\mathbf{x}^{H}\mathbf{R}_{y}^{-1}\mathbf{x}=\mathbf{d}^{H}\mathbf{R}_{y}^{-2}\mathbf{d}
$$

Plugging these expanded terms back into the Kantorovich inequality gives:

$$
\frac{(\mathbf{d}^{H}\mathbf{R}_{y}^{-1}\mathbf{d})^{2}}{M(\mathbf{d}^{H}\mathbf{R}_{y}^{-2}\mathbf{d})}\geq\frac{4\kappa}{(\kappa+1)^{2}}
$$

Recognizing from our earlier definitions that $W=\frac{(\mathbf{d}^{H}\mathbf{R}_{y}^{-1}\mathbf{d})^{2}}{\mathbf{d}^{H}\mathbf{R}_{y}^{-2}\mathbf{d}}$, we obtain the relationship:

$$
\frac{W}{M}\geq\frac{4\kappa}{(\kappa+1)^{2}}
$$

Let $A_{G}=M/W_{\min}$ represent the strict array gain limit (i.e., the maximum allowable degradation relative to the optimal delay-and-sum Array Gain). To guarantee $W\geq W_{\min}$, we set $M/W=A_{G}$ and solve the inequality for the maximum allowable condition number $\kappa_{\max}$:

$$
\kappa_{\max}=(2A_{G}-1)+2\sqrt{A_{G}(A_{G}-1)}
$$

This is a powerful deterministic result: by actively limiting the condition number of the estimated SCM, we implicitly and strictly control the WNG of the resulting adaptive beamformer.

### III-B Adaptive Diagonal Loading Estimation

To actively constrain the SCM’s condition number to $\kappa_{\max}$, we apply a dynamic diagonal loading factor $\mu[i]$ at every frame:

$$
\mathbf{Q}[i]=\hat{\mathbf{R}}_{y}[i]+\mu[i]\mathbf{I}
$$

Let $\lambda_{\max}$ and $\lambda_{\min}$ be the maximum and minimum eigenvalues of the unloaded sample matrix $\hat{\mathbf{R}}_{y}[i]$. The eigenvalues of the loaded matrix $\mathbf{Q}[i]$ are shifted by $\mu[i]$, yielding a new condition number:

$$
\kappa_{loaded}=\frac{\lambda_{\max}+\mu[i]}{\lambda_{\min}+\mu[i]}
$$

To satisfy $\kappa_{loaded}\leq\kappa_{\max}$, we solve for the exact required loading multiplier:

$$
\mu[i]=\max\left(0,\frac{\lambda_{\max}-\kappa_{\max}\lambda_{\min}}{\kappa_{\max}-1}\right)
$$

This formulation ensures that we apply the absolute minimum amount of diagonal loading necessary to preserve the requested WNG, thereby preserving the beamformer’s ability to place deep nulls on interferers.

### III-C Complexity Scalable Estimation Modes

Calculating $\mu[i]$ requires knowledge of the SCM’s extreme eigenvalues at every frame. Because Exact Eigenvalue Decomposition (EVD) is computationally prohibitive ($\mathcal{O}(M^{3})$) for arrays with many elements operating at high sampling rates, we propose three scalable estimation techniques:

1. Trace Mode ($\mathcal{O}(M)$): The sum of the eigenvalues equals the trace of the matrix. Since SCMs are positive semi-definite, we can formulate a rapid, strictly conservative upper bound: $\lambda_{\max}\leq\text{Tr}(\hat{\mathbf{R}}_{y})$. We assume worst-case snapshot deficiency where $\lambda_{\min}\approx 0$. This mode is extremely fast but results in slightly heavier diagonal loading than strictly necessary.
2. Gershgorin Mode ($\mathcal{O}(M^{2})$): This mode utilizes the Gershgorin Circle Theorem to place tighter bounds on the eigenspectrum without performing a full decomposition. Every eigenvalue of $\hat{\mathbf{R}}_{y}$ lies within at least one Gershgorin disc $D(\hat{R}_{m,m},R_{m})$, where the radius is the sum of the absolute off-diagonal elements in that row: $R_{m}=\sum_{j\neq m}\lvert\hat{R}_{m,j}\rvert$. We estimate the bounds as:
	$$
	\displaystyle\lambda_{\max}
	$$
	 
	$$
	\displaystyle\leq\max_{m}\left(\hat{R}_{m,m}+R_{m}\right)
	$$
	 
	$$
	\displaystyle\lambda_{\min}
	$$
	 
	$$
	\displaystyle\geq\max\left(0,\min_{m}\left(\hat{R}_{m,m}-R_{m}\right)\right)
	$$
	This provides an excellent trade-off, offering tighter loading limits at moderate complexity.
3. Exact EVD ($\mathcal{O}(M^{3})$): For smaller arrays or systems with high computational budgets, exact eigenvalues are extracted. This guarantees the theoretically optimal $\mu[i]$, providing the highest possible interference suppression while exactly adhering to the WNG limit.

### III-D WNG Bounds in the GSC Framework

In the direct MPDR formulation, the target distortionless constraint and the adaptive degrees of freedom are entangled within the same weight vector. Alternatively, the Generalized Sidelobe Canceller (GSC) architecture orthogonalizes these components. The overall weight vector in the GSC is defined as:

$$
\mathbf{w}_{gsc}=\mathbf{w}_{q}-\mathbf{B}\mathbf{w}_{a}
$$

where $\mathbf{w}_{q}=\mathbf{d}/M$ is the fixed quiescent weight vector satisfying the target constraint, $\mathbf{B}\in\mathbb{C}^{M\times(M-1)}$ is the blocking matrix such that $\mathbf{B}^{H}\mathbf{d}=\mathbf{0}$ and $\mathbf{B}^{H}\mathbf{B}=\mathbf{I}$, and $\mathbf{w}_{a}\in\mathbb{C}^{(M-1)\times 1}$ is the adaptive noise cancellation weight vector.

The adaptive noise cancellation weight vector is traditionally computed as $\mathbf{w}_{a}=\mathbf{R}_{n}^{-1}\mathbf{r}_{qn}$, where $\mathbf{R}_{n}=\mathbf{B}^{H}\hat{\mathbf{R}}_{y}\mathbf{B}$ is the noise correlation matrix and $\mathbf{r}_{qn}=\mathbf{B}^{H}\hat{\mathbf{R}}_{y}\mathbf{w}_{q}$ is the cross-correlation vector. Let $p_{q}=\mathbf{w}_{q}^{H}\hat{\mathbf{R}}_{y}\mathbf{w}_{q}$ denote the quiescent output power tracked over the sliding window.

To enforce the Kantorovich-derived WNG bounds without explicitly reconstructing the full spatial correlation matrix $\hat{\mathbf{R}}_{y}$, we define a unitary transformation matrix $\mathbf{T}=[\sqrt{M}\mathbf{w}_{q},\mathbf{B}]$. Because $\mathbf{T}^{H}\mathbf{T}=\mathbf{I}$, the transformed matrix $\tilde{\mathbf{R}}=\mathbf{T}^{H}\hat{\mathbf{R}}_{y}\mathbf{T}$ inherently shares the exact same eigenvalues as $\hat{\mathbf{R}}_{y}$. By leveraging the orthogonal properties of the GSC, we can construct $\tilde{\mathbf{R}}$ directly from the continuously tracked components:

$$
\tilde{\mathbf{R}}=\begin{bmatrix}Mp_{q}&\sqrt{M}\mathbf{r}_{qn}^{H}\\
\sqrt{M}\mathbf{r}_{qn}&\mathbf{R}_{n}\end{bmatrix}
$$

Because the eigenspectrum is perfectly preserved, the extreme eigenvalues $\lambda_{\max}$ and $\lambda_{\min}$ can be estimated from $\tilde{\mathbf{R}}$ using the previously defined scalable modes (Trace, Gershgorin, or Exact EVD). Consequently, the requisite adaptive diagonal loading factor $\mu[i]$ is identical to that of the direct MPDR formulation for the Trace and EVD modes. Note, the Gershgorin estimates depend on the choice of basis functions, and will generally result in different diagonal loading estimates. This is shown in the simulations.

The WNG-constrained beamformer is then realized by applying this condition-bounding load solely to the noise correlation matrix prior to inversion:

$$
\mathbf{w}_{a}=(\mathbf{R}_{n}+\mu[i]\mathbf{I})^{-1}\mathbf{r}_{qn}
$$

This formulation demonstrates that the proposed dynamic loading technique is structurally agnostic, providing the exact same deterministic WNG guarantees and stability whether applied directly to the sample matrix inversion or within the partitioned GSC framework.

## IV Simulations

### IV-A Simulation Setup

We evaluate the proposed adaptive diagonal loading strategies using a simulated uniform linear array (ULA) consisting of $M=15$ microphones with half-wavelength spacing at a center frequency of $f_{0}=1000$ Hz. To rigorously test the tracking capabilities and robustness of the algorithms, we simulate a highly dynamic “birth-death” spatial interference scenario over $T=20000$ snapshots. In this scenario, up to two statistically independent interferers randomly appear, remain active for a duration, and disappear.

To prevent trivial interference scenarios or impossible target separation, the interferers are strictly confined to an angular grid where the target’s normalized quiescent beampattern response falls between $-13$ dB and $-3$ dB. This may be typical in cocktail party scenario where multiple closely spaced talkers may need to be separated. The dynamic interferers are generated with an Interference-to-Noise Ratio (INR) of $7$ dB. The target signal is fixed at broadside ($90^{\circ}$) with a Signal-to-Noise Ratio (SNR) of $-5$ dB. To induce severe snapshot deficiency, the sample Spatial Correlation Matrix (SCM) is tracked using a sliding rectangular window of $L=37$ snapshots ($L\approx 2.5M$). For an array of $M=15$, the maximum theoretical WNG is $10\log_{10}(15)\approx 11.76$ dB. To allow for adaptive interference nulling while preventing target cancellation, we define a strict WNG lower bound of $W_{\min}=10\log_{10}(M)-3\approx 8.76$ dB.

We compare the three proposed complexity modes—Trace, Gershgorin, and Exact Eigenvalue Decomposition (EVD)—against the classical post-hoc weight scaling method proposed by Cox et al. [^3], and an Omniscient Capon beamformer. The Omniscient Capon utilizes the exact, theoretical underlying ECM at every snapshot and serves as the absolute upper bound for achievable performance.

### IV-B Results and Discussion

The ground truth scanned spatial response over a single trial is shown in 1. The beamformers successfully place and dynamically update deep nulls as the birth-death interferers transition, without suppressing the broadside target.

![Refer to caption](figures/ground_truth_trial_1.png)

Fig. 1: Ground Truth Spatial spectrum over time for a single trial, demonstrating the dynamic birth-death interferers and the broadside target.

The primary objective of the proposed Kantorovich-bounded loading is to guarantee WNG stability. Fig. 2 plots the ensemble WNG over time. Under tight snapshot deficiency, standard sample matrix inversion causes the weight vector norm to explode, resulting in dramatic target cancellation. As designed, the Trace, Gershgorin, and EVD modes strictly and actively constrain the WNG above the $8.76$ dB threshold at every frame.

![Refer to caption](figures/wng.png)

Fig. 2: Ensemble White Noise Gain (WNG). All proposed pre-inversion conditioning methods actively bound the WNG above the specified 8.76 dB limit.

The ensemble cumulative Mean Squared Error (MSE) and output Signal-to-Interference-plus-Noise Ratio (SINR) are presented in Fig. 3 and Fig. 4, respectively. Among the realizable methods, a clear performance hierarchy emerges: Exact EVD $>$ Gershgorin $>$ Trace $>$ Cox.

The Exact EVD mode achieves the highest output SINR. By extracting the true extreme eigenvalues, it applies the exact minimal diagonal loading necessary, preserving the maximum possible degrees of freedom for deep interference nulling. The Gershgorin mode performs nearly identically to the EVD mode, successfully suppressing the dynamic interferers while drastically reducing the computational burden to $\mathcal{O}(M^{2})$. The Trace mode ($\mathcal{O}(M)$) serves as a rapid, strictly conservative bound; because it slightly overestimates the required loading, it behaves closer to a delay-and-sum beamformer, resulting in a marginally lower SINR but absolute WNG stability.

In contrast, while the Cox method attempts to restore WNG via post-hoc scaling of the weight vector’s null-space projection, this ad-hoc geometric adjustment disrupts the optimality of the spatial filter. This results in significantly worse cumulative MSE and slower convergence during interferer transitions compared to our proposed pre-inversion conditioning.

![Refer to caption](figures/mse.png)

Fig. 3: Ensemble cumulative Mean Squared Error (MSE) for the MPDR formulation.

![Refer to caption](figures/sinr.png)

Fig. 4: Ensemble output SINR. The Exact EVD and Gershgorin modes track closely to the Omniscient baseline.

### IV-C Architecture Equivalence: MPDR vs. GSC

We also evaluated the algorithms within the Generalized Sidelobe Canceller (GSC) architecture. Mathematically, the EVD, Trace, and Cox modes are perfectly invariant under the unitary transformation mapping the direct MPDR to the GSC framework. Therefore, they yield identical beamforming weights and performance in both architectures.

However, as illustrated in Fig. 5, the Gershgorin mode exhibits divergent behavior between the MPDR and GSC formulations. This discrepancy arises because the Gershgorin circle bounds are inherently basis-dependent. The unitary blocking matrix $\mathbf{B}$ applied in the GSC alters the distribution of matrix energy between the diagonal and off-diagonal elements of the partitioned correlation matrix. Because the Gershgorin radii are defined by the sum of the absolute off-diagonal elements, this transformation tightens or loosens the estimated eigenvalue bounds depending on the instantaneous snapshot data, resulting in slight variations in the applied loading parameter $\mu$ compared to the direct MPDR domain.

![Refer to caption](figures/gershgorin.png)

Fig. 5: Performance comparison of the Gershgorin mode between the direct MPDR and GSC architectures, highlighting the basis-dependent nature of the eigenvalue bounds.

## V Conclusion

In this paper, we proposed a novel WNG-constrained adaptive diagonal loading approach tailored for snapshot-deficient scenarios and highly dynamic acoustic environments. By establishing an analytic bound using the Kantorovich inequality, our method actively and deterministically constrains the condition number of the spatial correlation matrix. This mathematically guarantees that the beamformer’s White Noise Gain remains strictly within specified bounds, preventing the severe target signal cancellation commonly observed in standard MPDR and MVDR beamformers. Furthermore, we introduced three progressive eigenvalue bound estimation techniques—Trace, Gershgorin, and Exact EVD—that provide flexible trade-offs between computational complexity and strict WNG adherence. Our simulations demonstrate that this approach yields highly stable, robust beamforming that outperforms classical post-hoc scaling methods, making it highly suitable for large microphone arrays operating in real-world, low-latency audio applications. It also provides a principled approach to diagonal loading for neural estimated covariance matrices which have become a standard estimation technique.

[^1]: K. L. Bell, Y. Ephraim, and H. L. Van Trees (2002) A bayesian approach to robust adaptive beamforming. IEEE Transactions on Signal Processing 48 (2), pp. 386–398. Cited by: §I.

[^2]: J. Capon (1969) High-resolution frequency-wavenumber spectrum analysis. Proceedings of the IEEE 57 (8), pp. 1408–1418. External Links: [Document](https://dx.doi.org/10.1109/PROC.1969.7278) Cited by: §I.

[^3]: H. Cox, R. Zeskind, and M. Owen (1987) Robust adaptive beamforming. IEEE Transactions on Acoustics, Speech, and Signal Processing 35 (10), pp. 1365–1376. Cited by: §I, §IV-A.

[^4]: A. Elnashar, S. M. Elnoubi, and H. A. El-Mikati (2006) Further study on robust adaptive beamforming with optimum diagonal loading. IEEE Transactions on Antennas and Propagation 54 (12), pp. 3647–3658. Cited by: §I.

[^5]: D. D. Feldman and L. J. Griffiths (2002) A projection approach for robust adaptive beamforming. IEEE Transactions on signal processing 42 (4), pp. 867–876. Cited by: §I.

[^6]: S. Gannot, E. Vincent, S. Markovich-Golan, and A. Ozerov (2017) A consolidated perspective on multimicrophone speech enhancement and source separation. IEEE/ACM Transactions on Audio, Speech, and Language Processing 25 (4), pp. 692–730. Cited by: §I.

[^7]: G. Itzhak and I. Cohen (2024) Robust beamforming for multispeaker audio conferencing under doa uncertainty. IEEE Transactions on Audio, Speech and Language Processing 33, pp. 139–151. Cited by: §I.

[^8]: L. V. Kantorovich (1948) Functional analysis and applied mathematics (in russian). Uspekhi Mat Nauk 3, pp. 89. Cited by: §III-A.

[^9]: C.J. Lam and A.C. Singer (2006) Bayesian beamforming for doa uncertainty: theory and implementation. IEEE Transactions on Signal Processing 54 (11), pp. 4435–4445. External Links: [Document](https://dx.doi.org/10.1109/TSP.2006.880257) Cited by: §I.

[^10]: D. Levin, E. A. Habets, and S. Gannot (2013) Robust beamforming using sensors with nonidentical directivity patterns. In 2013 IEEE International Conference on Acoustics, Speech and Signal Processing, pp. 91–95. Cited by: §I.

[^11]: J. Li and P. Stoica (2006) Robust adaptive beamforming. Wiley Online Library. Cited by: §I.

[^12]: E. Mabande, A. Schad, and W. Kellerman (2009) Robust superdirectional beamforming for hands-free speech capture in cars. NAG/DAGA 2009, pp. 23–26. Cited by: §I.

[^13]: X. Mestre and M. A. Lagunas (2005) Diagonal loading for finite sample size beamforming: an asymptotic approach. Robust adaptive beamforming, pp. 200–266. Cited by: §I.

[^14]: S. Shahbazpanahi, A. B. Gershman, Z. Luo, and K. M. Wong (2003) Robust adaptive beamforming for general-rank signal models. IEEE Transactions on Signal Processing 51 (9), pp. 2257–2269. Cited by: §I.

[^15]: H. L. Van Trees (2002) Optimum array processing: part iv of detection, estimation, and modulation theory. John Wiley & Sons. Cited by: §I.

[^16]: S. A. Vorobyov, A. B. Gershman, and Z. Luo (2003) Robust adaptive beamforming using worst-case performance optimization: a solution to the signal mismatch problem. IEEE transactions on signal processing 51 (2), pp. 313–324. Cited by: §I.
