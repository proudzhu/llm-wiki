Robin Scheibler    Nobutaka Ono Thanks: This research was supported by JSPS KAKENHI Grant Numbers 17F17049, 16H01735 and JST CREST Grant Number JPMJCR19A3. Thanks: Code and data to reproduce the results of this paper are available at [https://github.com/onolab-tmu/code\_2020ICASSP\_five](https://github.com/onolab-tmu/code_2020ICASSP_five).

###### Abstract

We propose fast independent vector extraction (FIVE), a new algorithm that blindly extracts a single non-Gaussian source from a Gaussian background. The algorithm iteratively computes beamforming weights maximizing the signal-to-interference-and-noise ratio for an approximate noise covariance matrix. We demonstrate that this procedure minimizes the negative log-likelihood of the input data according to a well-defined probabilistic model. The minimization is carried out via the auxiliary function technique whereas, unlike related methods, the auxiliary function is globally minimized at every iteration. Numerical experiments are carried out to assess the performance of FIVE. We find that it is vastly superior to competing methods in terms of convergence speed, and has high potential for real-time applications.

<sup>†</sup>

## 1 Introduction

Blind source extraction (BSE) aims at separating a single target signal from background noise without any prior information [^1] [^2]. While BSE predates independent component analysis (ICA) [^3], the two problems are tightly related [^4] [^5] [^6]. It can be seen as a blind source separation (BSS) problem where only one source is retrieved. BSE most often relies on the independence of a non-Gaussian source contrasted to a Gaussian [^7], or non-Gaussian [^8], background.

Our focus is on audio applications where the mixture is typically convolutive. In this case, the frequency domain BSS framework [^9] can be leveraged to transform the convolution into point-wise multiplication in the time-frequency domain. Then, BSE can be applied in parallel to all the narrowband channels. Done directly, however, this may lead to a problem whereas different sources are extracted at different frequencies. This is known as the permutation ambiguity problem in ICA [^10]. An elegant solution is to consider multivariate probability distributions over frequencies, giving rise to the independent vector analysis (IVA) [^11] [^12] and extraction (IVE) [^7] paradigms in BSS and BSE, respectively. For BSE, OGIVE, a gradient-ascent algorithm, was proposed and shown to be effective [^7]. However, the speed and convergence guarantees of gradient methods are limited. Recently, we introduced OverIVA, an algorithm for overdetermined BSS with fast and guaranteed convergence. OverIVA assumes a super-Gaussian model for sources and a Gaussian background. The algorithm is obtained by applying the auxiliary function optimization method, similarly to AuxIVA [^13], with the addition of orthogonality constraints between the target and background signals [^14]. This algorithm is applicable to IVE.

In this paper, we introduce a new algorithm for fast IVE (FIVE). FIVE iteratively applies maximum signal-to-interference-and-noise ratio ($\mathsf{SINR}$) beamforming [^15] to improve upon an initial estimate of the target signal. We show that this deceptively simple algorithm can be rigorously derived by minimizing the same cost function as OverIVA. Whereas OverIVA relied on orthogonal constraints for the separation of the background, FIVE solves the minimization of the auxiliary function to its global minimum. Interestingly, this is done by solving exactly a special case of the hybrid exact-approximate diagonalization (HEAD) problem [^16]. Experiments reveal that FIVE is blazingly fast and only requires a few iterations to achieve over $4\text{\,}\mathrm{dB}$ signal-to-distortion ratio (SDR) improvement. Further investigation reveals that FIVE behaves similarly to OverIVA and OGIVE in the presence of a mismatched background.

The reminder of this paper is organized as follows. Section 2 introduces notation, signal model and maximum $\mathsf{SINR}$ beamforming. FIVE is described informally in Section 3 and analyzed in Section 4. The experiments are discussed in Section 5. Section 6 concludes.

## 2 Background

### 2.1 Signal Model and Notation

We consider the mixture of a single source with an arbitrary background noise recorded by $M$ microphones. In the time-frequency domain, our signal model is

$$
x_{mfn}=s_{mfn}+b_{mfn},
$$

where $x_{mfn}$, $s_{mfn}$, and $b_{mfn}$ are the short-time Fourier transforms (STFT) [^17] of the microphone, target, and background signals, respectively. The indices $f=1,\ldots,F$ and $n=1,\ldots,N$ are the discrete frequency bins and frames, respectively. For convenience, we can group all microphone signals in the complex-valued vectors

$$
\boldsymbol{x}_{fn}=\begin{bmatrix}x_{1fn}&\cdots&x_{Mfn}\end{bmatrix}\in\mathbb{C}^{M}.
$$

In the rest of the manuscript, we use lower and upper case bold letters for vectors and matrices, respectively. Furthermore, $\boldsymbol{A}^{\top}$, $\boldsymbol{A}^{\mathsf{H}}$, $\det(\boldsymbol{A})$ and $\operatorname{tr}(\boldsymbol{A})$ denote the transpose, conjugate transpose, determinant and trace of matrix $\boldsymbol{A}$, respectively. Unless specified otherwise, indices $m$, $f$, and $n$ always take the ranges defined here.

### 2.2 Maximum SINR Beamforming

Beamforming addresses the problem of finding the optimal weight vectors $\boldsymbol{w}_{f}$ to combine the microphone signals such that $\boldsymbol{w}_{f}^{\mathsf{H}}\boldsymbol{x}_{fn}$ is close to the target signals. This is generally achieved by optimizing a well-chosen cost function. One can define the signal-to-interference-and-noise ratio ($\mathsf{SINR}$)

$$
\mathsf{SINR}_{f}[\boldsymbol{w}]=\frac{\boldsymbol{w}^{\mathsf{H}}\boldsymbol{\Sigma}^{(s)}_{f}\boldsymbol{w}}{\boldsymbol{w}^{\mathsf{H}}\boldsymbol{\Sigma}^{(b)}_{f}\boldsymbol{w}}
$$

where $\boldsymbol{\Sigma}^{(s)}_{f}$ and $\boldsymbol{\Sigma}^{(b)}_{f}$ are the covariance matrices of target and background signals, respectively. The Maximum $\mathsf{SINR}$ beamformer is the one maximizing (3) [^15]. Note that, if the target and background are uncorrelated, replacing $\boldsymbol{\Sigma}^{(s)}_{f}$ by $\boldsymbol{\Sigma}^{(x)}_{f}$, the covariance matrix of the microphone signals, in (3) only changes the ratio by a constant additive factor.

In practice, we must approximate the covariance matrices from the available data, e.g. the estimate of $\boldsymbol{\Sigma}^{(x)}_{f}$ is the sample covariance matrix of the input data

$$
\boldsymbol{C}_{f}=\frac{1}{N}\sum_{n}\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}.
$$

Now, provided a (possibly scaled) estimate $\boldsymbol{V}_{f}\sim\boldsymbol{\Sigma}_{f}^{(b)}$, we can obtain $\boldsymbol{w}_{f}$ as the result of the following optimization,

$$
\boldsymbol{w}_{f}=\underset{\boldsymbol{w}\in\mathbb{C}^{M}}{\arg\max}\ \frac{\boldsymbol{w}^{\mathsf{H}}\boldsymbol{C}_{f}\boldsymbol{w}}{\boldsymbol{w}^{\mathsf{H}}\boldsymbol{V}_{f}\boldsymbol{w}}\approx\underset{\boldsymbol{w}\in\mathbb{C}^{M}}{\arg\max}\ C_{1}\mathsf{SINR}_{f}[\boldsymbol{w}]+C_{2},
$$

where $C_{1}>0$ and $C_{2}$ are arbitrary constants. The optimizer of (5) is the generalized eigenvector corresponding to the largest generalized eigenvalue for the problem $\boldsymbol{C}_{f}\boldsymbol{w}=\lambda\boldsymbol{V}_{f}\boldsymbol{w}$. However, finding a good estimate $\boldsymbol{V}_{f}$ turns out to be a challenging problem, and the Maximum $\mathsf{SINR}$ beamformer is difficult to use in practice.

## 3 Algorithm

Suppose we are given an initial guess $\hat{s}_{fn}$ of the target signal, typically one of the microphone signals. Then an (unscaled) estimate of the background covariance matrix is

$$
\boldsymbol{V}_{f}=\frac{1}{N}\sum_{n}\varphi_{n}(r_{n})\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}},\quad\forall f,
$$

where $\varphi_{n}(r)\,:\,\mathbb{R}_{+}\to\mathbb{R}$ is a, yet-to-be-defined, strictly decreasing function, and $r_{n}$ is the magnitude of the target signal estimate,

$$
r_{n}=\sqrt{\sum\nolimits_{f}|\hat{s}_{fn}|^{2}},\quad\forall n.
$$

Due to $\varphi_{n}(r_{n})$, the importance of target dominated frames, i.e. where $r_{n}$ is large, is reduced, while background dominated frames are emphasized. We can now compute $\boldsymbol{w}_{f}$ as in (5) by solving a generalized eigenvalue problem. Now, using the newly obtained demixing filter $\boldsymbol{w}_{f}$, we update the target signal estimate

$$
\hat{s}_{fn}\leftarrow\boldsymbol{w}_{f}^{\mathsf{H}}\boldsymbol{x}_{fn},\quad\forall f,n.
$$

The procedure is then repeated until convergence, or for a fixed number of iterations. Note that a normalization step is needed to keep the extracted signal scale under control.

A simple improvement to this algorithm is to pre-whiten the input signal so that $\boldsymbol{C}_{f}=\boldsymbol{I}$. Then, solving (5) only requires the computation of the smallest eigenvalue and corresponding eigenvector of $\boldsymbol{V}_{f}$. Pseudo-code for the final form of the algorithm is provided in Algorithm 1. While the procedure just presented might seem ad-hoc, we show in the following section that it can be rigorously derived from the minimization of a well-chosen cost function, and that its convergence is, in fact, guaranteed.

Input: Input signals $\{\boldsymbol{x}_{fn}\}$, Initial estimate $\{\hat{s}_{fn}\}$

Output: Extracted signal $\{s_{fn}\}$

\# Input pre-whitening

$\tilde{\boldsymbol{x}}_{fn}=\boldsymbol{Q}^{-\mathsf{H}}_{f}\boldsymbol{x}_{fn}$, with $\frac{1}{N}\sum_{n}\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}=\boldsymbol{Q}_{f}^{\mathsf{H}}\boldsymbol{Q}_{f}$, $\forall f$

for *loop $\leftarrow 1$ to max. iterations* do

 $r_{n}\leftarrow\sqrt{\sum_{f}|\hat{s}_{fn}|^{2}},\ \forall n$

    for *$f\leftarrow 1$ to $F$* do

    $\widetilde{\boldsymbol{V}}_{f}\leftarrow\frac{1}{N}\sum_{n}\varphi_{n}(r_{n})\tilde{\boldsymbol{x}}_{fn}\tilde{\boldsymbol{x}}_{fn}^{\mathsf{H}}$

       Let $\lambda_{M}$ and $\boldsymbol{r}_{M}$ be the smallest eigenvalue of $\widetilde{\boldsymbol{V}}_{f}$ and corresponding eigenvector, respectively

       $\boldsymbol{w}_{f}\leftarrow\lambda_{M}^{-\frac{1}{2}}\boldsymbol{r}_{M}$        $\hat{s}_{fn}\leftarrow\boldsymbol{w}_{f}^{\mathsf{H}}\tilde{\boldsymbol{x}}_{fn},\ \forall n$

       end for

    end for

Algorithm 1 FIVE: Fast Independent Vector Extraction

## 4 Derivation

We turn now to the analysis of the derivation of Algorithm 1. We prove that it extracts the maximum likelihood source estimate under a well-defined probabilistic model. We consider the source extraction problem as a special case of determined blind source separation. More specifically, we want to find the $M\times M$ demixing matrix

$$
\boldsymbol{W}_{f}=\begin{bmatrix}\boldsymbol{w}_{f}&\boldsymbol{J}_{f}\end{bmatrix}^{\mathsf{H}},
$$

where $\boldsymbol{J}_{f}\in\mathbb{C}^{M\times M-1}$ is such that $s_{fn}=\boldsymbol{w}_{f}^{\mathsf{H}}\boldsymbol{x}_{fn}$ is independent from $\boldsymbol{z}_{fn}=\boldsymbol{J}_{f}^{\mathsf{H}}\boldsymbol{x}_{fn}$.

###### Theorem 1.

Let the three following assumptions hold.

- Target signal and background are statistically independent.
- The source signal distribution is spherical super-Gaussian
	$$
	p_{S_{n}}(s_{1n},\ldots,s_{Fn})\sim e^{-G_{n}\left(\sqrt{\sum_{f}s_{fn}}\right)},
	$$
	with $G_{n}\>:\>\mathbb{R}_{+}\to\mathbb{R}$, strictly increasing, differentiable, and such that $G_{n}^{\prime}(r)/r$ is strictly decreasing (see [^13] [^18] for details).
- The background is Gaussian with arbitrary covariance structure across channels, but uncorrelated over frequencies.

Then, Algorithm 1 with

$$
\varphi_{n}(r)=\frac{G^{\prime}_{n}(r)}{2r}
$$

is guaranteed to converge to a stationary point of the negative log-likelihood of the observed signal.

The rest of this section proves the theorem. Based on the probabilistic model enounced in Theorem 1, we can write explicitly the negative log-likelihood of the observed signal,

$$
\begin{aligned}
\mathcal{L}=-2N\sum_{f}\log|\det(\boldsymbol{W}_{f})|+\sum_{n}G_{n}\left(\sqrt{\sum\nolimits_{f}|\boldsymbol{w}_{f}^{\mathsf{H}}\boldsymbol{x}_{fn}|^{2}}\right)\\
+\sum_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}}\boldsymbol{J}_{f}\boldsymbol{B}^{-1}_{f}\boldsymbol{J}_{f}^{\mathsf{H}}\boldsymbol{x}_{fn},
\end{aligned}
$$

where $\boldsymbol{B}=\mathbb{E}\left[\boldsymbol{z}_{fn}\boldsymbol{z}_{fn}^{\mathsf{H}}\right]$ is the covariance matrix of the background after demixing. At this point, we will assume that $\boldsymbol{B}$ is known or can be estimated. As we will find out, it is in fact irrelevant. The maximum likelihood estimate of the target signal is provided by minimizing (12) with respect to $\boldsymbol{w}_{f}$ and $\boldsymbol{J}_{f}$. While direct minimization of $\mathcal{L}$ is hard due to the non-quadratic term in $\boldsymbol{w}_{f}$, it can be done via the auxiliary function approach [^18] [^13]. We make use of an inequality for super-Gaussian sources to create a majorizing function of (12).

###### Lemma 1 (from ).

Let $G_{n}(r)$ be as defined in Theorem 1. Then,

$$
G_{n}(r)\leq G_{n}^{\prime}(r_{0})\frac{r^{2}}{2r_{0}}+\left(G_{n}(r_{0})-\frac{r_{0}}{2}G_{n}^{\prime}(r_{0})\right),
$$

with equality for $r=r_{0}$.

Then, the majorizing function $\mathcal{L}_{2}$ is as follows

$$
\begin{aligned}
\mathcal{L}\leq\mathcal{L}_{2}=-2N\sum_{f}\log|\det(\boldsymbol{W}_{f})|+N\sum_{f}\boldsymbol{w}_{f}^{\mathsf{H}}\boldsymbol{V}_{f}\boldsymbol{w}_{f}\\
+N\sum_{f}\operatorname{tr}\left(\boldsymbol{J}_{f}^{\mathsf{H}}\boldsymbol{C}_{f}\boldsymbol{J}_{f}\boldsymbol{B}^{-1}_{f}\right)+\text{constant},
\end{aligned}
$$

with $\boldsymbol{V}_{f}$, $\boldsymbol{C}_{f}$, and $r_{n}$ defined in (6), (4), and (7), respectively. Then, the auxiliary function method (also known as majorization-minimization) consists in iteratively minimizing (14) and recomputing $r_{n}$ based on the new demixing filter. This method is guaranteed to converge to a stationary point of (12) [^19]. Equating the gradient of $\mathcal{L}_{2}$ to zero leads to the following quadratic system of equations

$$
\begin{bmatrix}\boldsymbol{w}_{f}^{\mathsf{H}}\\
\boldsymbol{J}_{f}^{\mathsf{H}}\end{bmatrix}\begin{bmatrix}\boldsymbol{V}_{f}\boldsymbol{w}_{f}&\boldsymbol{C}_{f}\boldsymbol{J}_{f}\end{bmatrix}=\begin{bmatrix}1&\boldsymbol{0}^{\top}\\
\boldsymbol{0}&\boldsymbol{B}_{f}\end{bmatrix},\quad\forall f.
$$

We omit the index $f$ from here on for convenience. This is a special case of the HEAD problem [^16] where $M-1$ columns share the same matrix. Although a general closed form solution of HEAD is unknown for $M>2$, we show that (15) can be solved exactly. This is a generalization of the case $M=2$, presented in [^20].

###### Proposition 1.

Let $\boldsymbol{C}$ and $\boldsymbol{B}$, both Hermitian matrices, have decompositions $\boldsymbol{C}=\boldsymbol{Q}^{\mathsf{H}}\boldsymbol{Q}$ and $\boldsymbol{B}=\boldsymbol{U}^{\mathsf{H}}\boldsymbol{U}$, and let $\lambda_{1}\geq\ldots\geq\lambda_{M}$ and $\boldsymbol{r}_{1},\ldots,\boldsymbol{r}_{M}$ be the eigenvalues and eigenvectors, respectively, of $\widetilde{\boldsymbol{V}}=\boldsymbol{Q}^{-\mathsf{H}}\boldsymbol{V}\boldsymbol{Q}^{-1}$. In addition, let $\boldsymbol{\macc@depth\char 1\relax\macc@set@skewchar\macc@nested@a 111{R}}_{k}$ be the $M\times M-1$ matrix whose columns are $\boldsymbol{r}_{\ell}$, $\forall\ell\neq k$. Then,

$$
\boldsymbol{w}=\frac{1}{\sqrt{\lambda_{k}}}\boldsymbol{Q}^{-1}\boldsymbol{r}_{k},\quad\boldsymbol{J}=\boldsymbol{Q}^{-1}\boldsymbol{\macc@depth\char 1\relax\macc@set@skewchar\macc@nested@a 111{R}}_{k}\boldsymbol{U},
$$

is a solution to (15) for every $k=1,\ldots,M$.

###### Proof.

The proof follows by substituting (16) into (15), applying the properties of the eigenvectors, and the decompositions. ∎

As we have just shown, there are $M$, possibly distinct, solutions to (15), corresponding to $M$ stationary points of (14).

###### Proposition 2.

The global minimum of (14) is given by the minimum eigenvalue, i.e. $k=M$.

###### Proof.

Under the choice (16), the only non-constant term in (14) is the log-determinant. All we need to show is that the determinant is maximized. Because $\boldsymbol{Q}$ and $\boldsymbol{U}$ are independent of $k$, and

$$
\boldsymbol{W}^{\mathsf{H}}=\boldsymbol{Q}^{-1}\begin{bmatrix}\frac{1}{\sqrt{\lambda_{M}}}\boldsymbol{r}_{M}&\boldsymbol{\macc@depth\char 1\relax\macc@set@skewchar\macc@nested@a 111{R}}_{M}\end{bmatrix}\begin{bmatrix}1&\boldsymbol{0}^{\top}\\
\boldsymbol{0}&\boldsymbol{U}\end{bmatrix},
$$

we only need to focus on the determinant of the middle term. There,

$$
\displaystyle\left|\det\begin{bmatrix}\frac{1}{\sqrt{\lambda_{M}}}\boldsymbol{r}_{M}&\boldsymbol{\macc@depth\char 1\relax\macc@set@skewchar\macc@nested@a 111{R}}_{M}\end{bmatrix}\right|=\sqrt{\frac{\lambda_{k}}{\lambda_{M}}}\left|\det\begin{bmatrix}\frac{1}{\sqrt{\lambda_{k}}}\boldsymbol{r}_{k}&\boldsymbol{\macc@depth\char 1\relax\macc@set@skewchar\macc@nested@a 111{R}}_{k}\end{bmatrix}\right|,\ \forall k,
$$

and the proof follows because $\lambda_{k}/\lambda_{M}\geq 1$ for any $k$. ∎

There are two points left to obtain the final algorithm. First, $\boldsymbol{Q}$ never changes throughout the algorithm and corresponds to a whitening of the input data. It can by applied once and for all at the beginning of the algorithm. Further multiplications are thus avoided. Finally, we are only interested in $\boldsymbol{w}$. Being never needed, computation of $\boldsymbol{J}$ is omitted, which makes knowledge or estimation of $\boldsymbol{B}$ moot.

![[raw/papers/scheibler-2020-fast-independent-vector-extraction/figures/fig1.png|Refer to caption]]

Figure 1: Right, the room setup for simulation. Left, the histogram of simulated reverberation times.

Figure 2: Mean convergence curves: SDR improvement as a function of the runtime for $1\text{\,}\mathrm{s}$ of input signal. From left to right, 2, 3, 5, and 8 microphones are used.

## 5 Experiments

The performance of FIVE is assessed via simulations. We study the convergence speed, the separation level after a few iterations, and the effect of mismatch in the background model.

### 5.1 Experimental Setup

We use the pyroomacoustics toolbox [^21] to simulate 100 random rectangular rooms with walls between $6\text{\,}\mathrm{m}$ and $10\text{\,}\mathrm{m}$ and ceiling from $2.8\text{\,}\mathrm{m}$ to $4.5\text{\,}\mathrm{m}$ high. Simulated reverberation times ($T_{60}$) range from $60\text{\,}\mathrm{ms}$ to $540\text{\,}\mathrm{ms}$. Sources and microphone array are placed at random at least $50\text{\,}\mathrm{cm}$ away from the walls and between $1\text{\,}\mathrm{m}$ and $2\text{\,}\mathrm{m}$ high. The array is circular and regular with 2, 3, 5, or 8 microphones, and radius such that neighboring elements are $2\text{\,}\mathrm{cm}$ apart. The distance from target source to array center is in $[d_{\text{crit}},d_{\text{crit}}+1]$, where the critical distance $d_{\text{crit}}=0.057\sqrt{V/T_{60}}$, with $V$ the volume of the room [^22]. The $Q=10$ interferers are at least $d_{\text{crit}}+1$ from the array. We define $\mathsf{SINR}=\sigma_{T}^{2}/(Q\sigma_{I}^{2}+\sigma_{w}^{2})$, where $\sigma_{T}^{2}$ and $\sigma_{I}^{2}$ are the variance of target and interferers at the first microphone. We fix $\mathsf{SINR}=$ $5\text{\,}\mathrm{dB}$. The uncorrelated noise variance $\sigma_{w}^{2}$ is set to be $1\text{\,}\mathrm{\%}$ of the total noise-and-interference. An illustration of the room setup and a histogram of the reverberation times are provided in Fig. 1. We use a 4096 points STFT with half-overlap and a Hamming window.

We compare FIVE to OverIVA [^23], full AuxIVA [^13] with selection of the strongest output channel, and the gradient ascent based algorithm, OGIVE [^7]. The first three are run for 50 iterations, while the last one is run for 4000 iterations with step size 0.1, as specified in [^7]. We compare two source models: time-invariant Laplace and time-varying Gaussian. Without going into details due to lack of space, these models lead to the weighting functions

$$
\varphi^{\text{Lap}}_{n}(r)=(2r)^{-1},\quad\text{and}\quad\varphi^{\text{Gau}}_{n}(r)=(r^{2}/F)^{-1},
$$

respectively. The scale of the separated signals is restored by projection back onto the first microphone [^24]. The separation performance is evaluated in terms of signal-to-distortion ratio (SDR) and signal-to-interference ratio (SIR) [^25] using a popular toolbox [^26].

Figure 3: Box-plots of the SDR improvement after just three iterations.

### 5.2 Convergence Speed

Fig. 2 shows the mean evolution of SDR improvement ($\Delta$ SDR) as a function of runtime. The runtime is normalized per one second of input signal to gauge potential for real-time applications. FIVE (Laplace) is the fastest and reaches peak $\Delta$ SDR in one to three iterations. We observe however that the $\Delta$ SDR subsequently decreases before reaching convergences. Note that this is not a contradiction since the cost function (12) is not the SDR. We conjecture this to be due to a mismatch with the signal model. In terms of speed, FIVE (Gauss) is close behind but stably attains a larger $\Delta$ SDR value. OverIVA behaves similarly in terms of $\Delta$ SDR, which is expected because it also minimizes (12). Its convergence speed is about five times slower. Doing full separation with AuxIVA improves $\Delta$ SDR performance, likely due to a better modelling of the background as extra independent sound sources. However, convergence is at least one order of magnitude slower, which hits particularly hard when using more microphones. The gradient-based OGIVE converges at a much slower pace, but eventually reaches similar $\Delta$ SDR values, although outside the limits of Fig. 2. We do admit, however, that its runtime might improve with a more careful implementation.

### 5.3 Separation Performance after Three Iterations

Figure 4: Success rate at $\mathsf{SINR}=$ $0\text{\,}\mathrm{dB}$ and for different number of interferers.

Fig. 3 displays box-plots of the $\Delta$ SDR and $\Delta$ SIR of FIVE, OverIVA, and AuxIVA after three iterations. We leave out OGIVE of the comparison because it was difficult to include it in a meaningful manner. In all cases FIVE dominates, with OverIVA behind, and AuxIVA last. Also recall that three iterations of AuxIVA is about ten times longer than the other two. In general, time-varying Gauss model achieves higher $\Delta$ SDR and Laplace model higher $\Delta$ SIR.

### 5.4 Effect of Background Model Mismatch

In our experiments so far, the background has been composed of ten interference sources which is close to the Gaussian background assumption. We now rerun the experiment with the conditions modified as follows. The SINR is decreased to $0\text{\,}\mathrm{dB}$ and the number of microphones set to three. Then, we run the experiment with one, two, five, and ten interferers and measure the success rate of each algorithm. The success is defined as $\Delta$ SIR $\geq$ $1\text{\,}\mathrm{dB}$. The experiment result is shown in Fig. 4 When there is only one interferer, we expect all algorithms to fail because it is not possible to tell which source is the target without prior information. Indeed, even AuxIVA is slightly lower than 0.5, meaning that it probably separates the sources, but picks the wrong one half of the time. Other algorithms fail more often, which implies that separation itself fails. As we increase the number of interferers and the background approach Gaussianity, the success rate of all algorithms increases, with the exception of OGIVE (Gauss). There is not much difference between FIVE and OverIVA, but AuxIVA, which does not assume a specific background model, performs markedly better.

## 6 Conclusion

We presented a deceptively simple algorithm for BSE which can be described as iterative maximization of the SINR. The algorithm can be rigorously derived and its convergence is guaranteed. In experiments we showed that the proposed algorithm is blazingly fast, only needing a few iterations, even for up to eight microphones. In contrast, full IVA takes an order of magnitude longer, or more, to obtain the same SDR improvement. However, our method assumes a Gaussian distributed background and its performance degrades, sometimes significantly, when this is not fulfilled. Because BSE relies exclusively on the cost function for the extraction, a crucial next step is to identify a more suitable background model. It should be flexible enough to accommodate a wide variety of conditions, yet offer good contrast between target and background, for example as in [^8].

[^1]: P. J. Huber, “Projection pursuit,” *Ann. Stat.*, vol. 13, no. 2, pp. 435–475, Jun. 1985.

[^2]: J. F. Cardoso and A. Souloumiac, “Blind beamforming for non-Gaussian signals,” *IET*, vol. 140, no. 6, p. 362, 1993.

[^3]: P. Comon and C. Jutten, *Handbook of blind source separation: independent component analysis and applications*, 1st ed. Oxford, UK: Academic Press/Elsevier, 2010.

[^4]: S. Amari and A. Cichocki, “Adaptive blind signal processing-neural network approaches,” *Proc. IEEE*, vol. 86, no. 10, pp. 2026–2048, 1998.

[^5]: S. A. Cruces-Alvarez, A. Cichocki, and S. Amari, “From blind signal extraction to blind instantaneous signal separation: Criteria, algorithms, and stability,” *IEEE Trans. Neural Netw.*, vol. 15, no. 4, pp. 859–873, Jul. 2004.

[^6]: S. Javidi, D. P. Mandic, and A. Cichocki, “Complex blind source extraction from noisy mixtures using second-order statistics,” *IEEE Trans. Circuits Syst. I*, vol. 57, no. 7, pp. 1404–1416, Jul. 2010.

[^7]: Z. Koldovský and P. Tichavský, “Gradient algorithms for complex non-Gaussian independent component/vector extraction, question of convergence,” *IEEE Trans. Signal Process.*, vol. 67, no. 4, pp. 1050–1064, Dec. 2018.

[^8]: Z. Koldovský, P. Tichavský, and N. Ono, “Orthogonally-constrained extraction of independent non-Gaussian component from non-Gaussian background without ICA,” in *Latent Variable Analysis and Signal Separation*. Cham: Springer, Cham, Jul. 2018, pp. 161–170.

[^9]: P. Smaragdis, “Blind separation of convolved mixtures in the frequency domain,” *Neurocomputing*, vol. 22, no. 1-3, pp. 21–34, Nov. 1998.

[^10]: H. Sawada, S. Araki, and S. Makino, “Measuring dependence of bin-wise separated signals for permutation alignment in frequency-domain BSS,” in *Proc. IEEE ISCAS*, New Orleans, LA, USA, May 2007, pp. 3247–3250.

[^11]: A. Hiroe, “Solution of permutation problem in frequency domain ICA, using multivariate probability density functions,” in *ASIACRYPT 2016*. Berlin, Heidelberg: Springer Berlin Heidelberg, 2006, pp. 601–608.

[^12]: T. Kim, H. T. Attias, S.-Y. Lee, and T.-W. Lee, “Blind source separation exploiting higher-order frequency dependencies,” *IEEE Trans. Audio, Speech, Language Process.*, vol. 15, no. 1, pp. 70–79, Dec. 2006.

[^13]: N. Ono, “Stable and fast update rules for independent vector analysis based on auxiliary function technique,” in *Proc. IEEE WASPAA*, New Paltz, NY, USA, Oct. 2011, pp. 189–192.

[^14]: J. F. Cardoso, “On the performance of orthogonal source separation algorithms,” in *Proc. IEEE EUSIPCO*, Edinburgh, UK, Sep. 1994, pp. 776–779.

[^15]: H. L. Van Trees, *Optimum Array Processing*. New York, USA: John Wiley & Sons, Inc., Mar. 2002.

[^16]: A. Yeredor, “On hybrid exact-approximate joint diagonalization,” in *Proc. IEEE CAMSAP*, Dec. 2009, pp. 312–315.

[^17]: J. Allen, “Short term spectral analysis, synthesis, and modification by discrete Fourier transform,” *IEEE Trans. Acoust., Speech, Signal Process.*, vol. 25, no. 3, pp. 235–238, Jun. 1977.

[^18]: N. Ono and S. Miyabe, “Auxiliary-function-based independent component analysis for super-Gaussian sources,” *Proc. LVA/ICA*, vol. 6365, no. 6, pp. 165–172, Sep. 2010.

[^19]: K. Lange, *MM optimization algorithms*. SIAM, 2016.

[^20]: N. Ono, “Fast stereo independent vector analysis and its implementation on mobile phone,” in *Proc. IWAENC*, Aachen, DE, Sep. 2012.

[^21]: R. Scheibler, E. Bezzam, and I. Dokmanić, “Pyroomacoustics: A Python package for audio room simulations and array processing algorithms,” in *Proc. IEEE ICASSP*, Calgary, CA, Apr. 2018, pp. 351–355.

[^22]: H. Kuttruff, *Room acoustics*. CRC Press, 2009.

[^23]: R. Scheibler and N. Ono, “Independent vector analysis with more microphones than sources,” in *Proc. IEEE WASPAA*, New Paltz, NY, USA, Oct. 2019, accepted.

[^24]: N. Murata, S. Ikeda, and A. Ziehe, “An approach to blind source separation based on temporal structure of speech signals,” *Neurocomputing*, vol. 41, no. 1-4, pp. 1–24, Oct. 2001.

[^25]: E. Vincent, R. Gribonval, and C. Fevotte, “Performance measurement in blind audio source separation,” *IEEE Trans. Audio, Speech, Language Process.*, vol. 14, no. 4, pp. 1462–1469, Jun. 2006.

[^26]: C. Raffel, B. McFee, E. J. Humphrey, J. Salomon, O. Nieto, D. Liang, D. P. W. Ellis, C. C. Raffel, B. Mcfee, and E. J. Humphrey, “mir\_eval: A transparent implementation of common MIR metrics,” in *Proc. ISMIR*, 2014.