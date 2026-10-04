Robin Scheibler

###### Abstract

We propose a new algorithm for blind source separation of convolutive mixtures using independent vector analysis. This is an improvement over the popular auxiliary function based independent vector analysis (AuxIVA) with iterative projection (IP) or iterative source steering (ISS). We introduce iterative projection with adjustment (IPA), whereas we update one demixing filter and jointly adjust all the other sources along its current direction. We implement this scheme as multiplicative updates by a rank-2 perturbation of the identity matrix. Each update involves solving a non-convex minimization problem that we term log-quadratically penalized quadratic minimization (LQPQM), that we think is of interest beyond this work. We find that the global minimum of an LQPQM can be efficiently computed. In the general case, we show that all its stationary points can be characterized as zeros of a kind of secular equation, reminiscent of modified eigenvalue problems. We further prove that the global minimum corresponds to the largest of these zeros. We propose a simple procedure based on Newton-Raphson seeded with a good initial point to efficiently compute it. We validate the performance of the proposed method for blind acoustic source separation via numerical experiments with reverberant speech mixtures. We show that not only is the convergence speed faster in terms of iterations, but each update is also computationally cheaper. Notably, for four and five sources, AuxIVA with IPA converges more than twice as fast as competing methods.

## I Introduction

Blind source separation (BSS) deals with decomposing a mixture of signals into its constitutive components without any prior information [^1]. It has found prominent application in multichannel audio processing [^2], e.g., for the separation of speech [^3] and music [^4], but also in biomedical signal processing for electrocardiogram [^5] and electroencephalogram [^6], and in digital communications [^7]. For multichannel signals, independent component analysis (ICA) allows to do BSS, only requiring statistical independence of the sources [^8]. For convolutional mixtures such as those found in audio processing, the separation can be done in the frequency domain where convolution becomes pointwise multiplication [^9]. In this case, we need to perform the joint separation at all the frequency sub-bands in parallel. Without further considerations, this introduces a permutation ambiguity whereas the order of extracted sources may be different at each frequency. Independent vector analysis (IVA) solves this problem by assuming a multivariate distribution of the sources over the frequency sub-bands and doing the separation jointly [^10] [^11] [^12]. The source model is used to express the likelihood of the input data which is then maximized to estimate the source signals. This optimization problem is non-convex, and, without a known closed form solution. Auxiliary function based IVA (AuxIVA) was proposed as a fast and stable optimization method to solve IVA [^13]. It relies on the majorization-minimization technique [^14] and is applicable to super-Gaussian source models. AuxIVA majorizes the IVA cost function with a quadratic surrogate, leading to the so-called hybrid exact-approximate diagonalization problem (HEAD) [^15] [^16]. Solving the HEAD for more than two sources is still an open problem and instead AuxIVA performs alternating minimization of the surrogate with respect to the demixing filters of the sources [^13]. This approach has been coined iterative projection (IP). A similar solution was also proposed in the context of Gaussian sources [^17]. Alternatives to the MM approach have been proposed. For example, proximal splitting allows for a versatile algorithm with a heuristic extension based on masking [^18] [^19]. Another approach, specialized for two sources, is based on expectation-maximization and a Gaussian mixture model [^20].

This paper focuses on the MM approach which underpins many algorithms with more sophisticated source models. These include non-negative low-rank [^21], based on a variational auto-encoder [^22], a deep network [^23], or using inter-clique dependence [^24]. In addition, algorithms for overdetermined IVA (OverIVA), i.e., when there are more channels than sources, also rely on IP for estimating the demixing matrix [^25]. As such, any improvement to the optimization of the surrogate function in AuxIVA directly translates to improvements for all of these algorithms. For two sources, the HEAD problem can be solved by a generalized eigenvalue decomposition [^26] and thus globally optimal updates of the surrogate are possible. A similar situation arises for blind extraction of a single source with the fast independent vector extraction algorithm [^27] [^28]. For three and more sources, iterative projection 2 (IP2) does pairwise updates of two sources at a time, leading to faster convergence [^29] [^30]. Finally, iterative source steering (ISS) performs a series of rank-1 updates of the demixing matrix which correspond in fact to alternating updates of the steering vectors [^31]. While the convergence of ISS is similar to that of IP, it does not require matrix inversion, unlike IP, and has an overall lower computational complexity. Thus, when separating three and more sources, all of IP, IP2, and ISS, fix all the other sources when doing one of the updates. This means that further correction can only happen at the next iteration.

In this work, we propose iterative projection with adjustment (IPA), a joint update of one demixing filter with an extra rank-1 modification of the rest of the demixing matrix. As opposed to IP, IP2, and ISS, when updating the demixing filter of one source, we simultaneously correct the demixing filters of all other sources accordingly. Intuitively, this allows the algorithm to make progress in the demixing of all sources at every update. Concretely, we adopt a multiplicative update form whereas the current demixing matrix is multiplied by a rank-2 perturbation of the identity matrix. We show that the minimization of the IVA surrogate function with respect to the multiplicative update leads to an optimization problem that we believe is of independent interest. We term this problem log-quadratically penalized quadratic minimization (LQPQM).

###### Problem 1 (LQPQM).

Let $\boldsymbol{A},\boldsymbol{C}\in\mathbb{C}^{d\times d}$ be Hermitian positive definite and semi-definite, respectively, and $\boldsymbol{b},\boldsymbol{d}\in\mathbb{C}^{d}$, and $z\in\mathbb{R}$, $z\geq 0$. Then, the LQPQM problem is,

$$
\underset{\boldsymbol{x}\in\mathbb{C}^{d}}{\min}\ (\boldsymbol{x}-\boldsymbol{b})^{\mathsf{H}}\boldsymbol{A}(\boldsymbol{x}-\boldsymbol{b})-\log\left((\boldsymbol{x}-\boldsymbol{d})^{\mathsf{H}}\boldsymbol{C}(\boldsymbol{x}-\boldsymbol{d})+z\right).
$$

For a sneak peek of what the objective function looks like in two dimensions, skip to Fig. 1. One of the main contributions of this paper is to show that, despite being non-convex, the global minimum of (P1) can be computed efficiently. In the general case, we show that all the stationary points of the objective of (P1) can be characterized as the zeros of a secular equation. Then, we prove that the value of the objective function decreases for increasing values of the zeros, and the global minimum thus corresponds to the largest zero. Furthermore, we find that its location is the only zero of the secular equation larger than the largest generalized eigenvalue for the problem $\boldsymbol{A}\boldsymbol{x}=\varphi\boldsymbol{B}\boldsymbol{x}$. Thus, we propose to use the Newton-Raphson root finding algorithm in this interval. We find that a good initial point for the root finding is given by the largest real root of a third order polynomial, with which the procedure converges in just a few iterations. The procedure we propose is reminiscent of other algorithms for problems involving pairs of quadratic forms such as modified eigenvalue problems [^32] [^33] [^34], generalized trust region subproblems [^35], or some applications in robust beamforming [^36], multi-lateration [^37], or direction of arrival [^38].

We validate the performance of the proposed method via numerical experiments for the separation of speech mixtures with two to five sources. Compared to competing methods, the proposed algorithm not only converges in fewer iterations, but also faster overall. For up to three sources, IPA and IP2 are similar, with a slight advantage for the former. For four sources and more, IPA converges more than twice as fast.

The rest of this paper is organized as follows. We cover the background on IVA, MM optimization, and AuxIVA in Section II. Section III describes IPA, the proposed AuxIVA updates, and proves that they are given by the solution to an LQPQM. The procedure to find the global minimum of an LQPQM is stated and proved in Section IV. We evaluate the performance of AuxIVA with IPA updates and compare to IP, ISS, and IP2 in Section V. Section VI concludes this paper.

## II Background

We consider the problem of separating $F$ mixtures of $K$ sources, recorded by $M$ sensors,

$$
\boldsymbol{x}_{fn}=\boldsymbol{A}_{f}\boldsymbol{s}_{fn},\quad n=1,\ldots,N,
$$

where $\boldsymbol{x}_{fn}\in\mathbb{C}^{M}$ and $\boldsymbol{s}_{fn}$ are the measurement and source vectors, respectively, in mixture $f$ and at frame $n$. Here, $\boldsymbol{A}_{f}\in\mathbb{C}^{M\times K}$ is the mixing matrix whose entry $(\boldsymbol{A}_{f})_{mk}$ is the transfer function from source $k$ to sensor $m$. Such parallel mixtures most frequently appear as the result of time-frequency domain processing for the separation of convolutional mixtures, e.g., of audio sources [^9]. From here on, we assume that we operate in the determined regime where $M=K$, i.e. the number of sources and sensors is the same. In this case, the separation may be done by finding the $M\times M$ demixing matrices,

$$
\boldsymbol{W}_{f}=\begin{bmatrix}\boldsymbol{w}_{1f}&\cdots&\boldsymbol{w}_{Mf}\end{bmatrix}^{\mathsf{H}},\quad f=1,\ldots,F,
$$

such that an estimate of the sources is,

$$
\boldsymbol{y}_{fn}=\boldsymbol{W}_{f}\boldsymbol{x}_{fn}.
$$

Thus, row $k$ of $\boldsymbol{W}_{f}$ contains the demixing filter $\boldsymbol{w}_{kf}^{\mathsf{H}}$ for source $k$, and $\boldsymbol{y}_{fn}$ is the estimated source vector. Finding matrices

$$
\mathcal{W}=\{\boldsymbol{W}_{f}\,:\,f=1,\ldots,F\}
$$

is the object of IVA.

In the rest of the manuscript, we use lower and upper case bold letters for vectors and matrices, respectively. Furthermore, $\boldsymbol{A}^{\top}$, $\boldsymbol{A}^{\mathsf{H}}$, and $\det(\boldsymbol{A})$ denote the transpose, conjugate transpose, and determinant of matrix $\boldsymbol{A}$, respectively. The conjugate of complex scalar $z\in\mathbb{C}$ is denoted $z^{*}$. Let $\boldsymbol{v}\in\mathbb{C}^{d}$, a complex $d$ -dimensional vector. The vector $\boldsymbol{v}^{*}$ contains the conjugated coefficients of $\boldsymbol{v}$. The Euclidean norm of $\boldsymbol{v}$ is $\|\boldsymbol{v}\|=(\boldsymbol{v}^{\mathsf{H}}\boldsymbol{v})^{\nicefrac{{1}}{{2}}}$. Unless specified otherwise, indices $f$, $k$, $m$, and $n$ always take the ranges defined in this section.

### II-A Independent Vector Analysis

IVA estimates the demixing matrices by maximum likelihood. The observed data are the time-frequency vectors $\boldsymbol{x}_{fn}$, and the parameters to estimate are the demixing matrices $\boldsymbol{W}_{f}$. For convenience, we also define the vector of source $k$ over frequencies, at frame $n$, as

$$
\displaystyle\check{\boldsymbol{s}}_{kn}=\begin{bmatrix}s_{k1n}&\cdots&s_{kFn}\end{bmatrix}^{\top}.
$$

The likelihood function is derived on the basis of the two following hypotheses.

###### Hypothesis 1 (Independence of Sources).

The sources are statistically independent, i.e.,

$$
\check{\boldsymbol{s}}_{kn}\perp\check{\boldsymbol{s}}_{k^{\prime}n^{\prime}},\ \forall k\neq k^{\prime},n,n^{\prime}.
$$

###### Hypothesis 2 (Source Model).

The sources follow a multivariate distribution, i.e.,

$$
p(\check{\boldsymbol{s}}_{kn})=\frac{1}{Z}e^{-F(\check{\boldsymbol{s}}_{kn})},\quad\forall k
$$

where $F(\boldsymbol{s})$ is called the contrast function and $Z$ is a normalizing constant that does not depend on the source.

Let us apply the change of variable $y_{kfn}=\boldsymbol{w}^{\mathsf{H}}\boldsymbol{x}_{fn}$ and define $\check{\boldsymbol{y}}_{kn}$ similarly to (5),

$$
\check{\boldsymbol{y}}_{kn}=\begin{bmatrix}y_{k1n}&\cdots&y_{kFn}\end{bmatrix}^{\top}.
$$

By further using independence, the joint distribution of the sources is just their product. Thus, the likelihood of the observation is

$$
\mathcal{L}(\mathcal{W})=\prod_{kn}p(\check{\boldsymbol{y}}_{kn})\prod_{f}|\det\boldsymbol{W}_{f}|^{2N}.
$$

Finally, IVA estimates $\boldsymbol{W}_{f}$ by minimizing the negative log-likelihood function, shown here with constant terms omitted,

$$
\ell(\mathcal{W})=\sum\nolimits_{kn}F(\check{\boldsymbol{y}}_{kn})-2\sum\nolimits_{f}\log|\det\boldsymbol{W}_{f}|.
$$

The choice of the contrast function and the minimization of the negative log-likelihood have been the object of considerable work [^10] [^11] [^12] [^26] [^13] [^29] [^30]. Source models based on spherical super-Gaussian distributions [^26] [^13] [^30] underpin AuxIVA, described in Section II-C. They allow to apply the MM optimization technique that we describe next.

### II-B Majorization-Minimization Optimization

MM optimization is an iterative technique that makes use of a surrogate function that is both tangent to, and majorizes the cost function everywhere. Repeatedly minimizing the surrogate also minimizes the original cost function.

###### Proposition 1.

Let $Q({\boldsymbol{\theta}},\hat{{\boldsymbol{\theta}}})$ be a surrogate function such that

$$
\displaystyle Q(\hat{{\boldsymbol{\theta}}},\hat{{\boldsymbol{\theta}}})=f(\hat{{\boldsymbol{\theta}}}),\quad\text{and},\quad Q({\boldsymbol{\theta}},\hat{{\boldsymbol{\theta}}})\geq f({\boldsymbol{\theta}}),\quad\forall{\boldsymbol{\theta}},\hat{{\boldsymbol{\theta}}}.
$$

Given an initial point ${\boldsymbol{\theta}}_{0}$, consider the sequence of iterates

$$
\displaystyle{\boldsymbol{\theta}}_{t}=\underset{{\boldsymbol{\theta}}}{\arg\min}\ Q({\boldsymbol{\theta}},{\boldsymbol{\theta}}_{t-1}),\quad t=1,\ldots,T.
$$

Then, the cost function is monotonically decreasing on the sequence, ${\boldsymbol{\theta}}_{0},{\boldsymbol{\theta}}_{1},...,{\boldsymbol{\theta}}_{T}$, i.e.,

$$
\displaystyle f({\boldsymbol{\theta}}_{0})\geq f({\boldsymbol{\theta}}_{1})\geq\ldots\geq f({\boldsymbol{\theta}}_{T}).
$$

###### Proof.

Applying the properties of the surrogate,

$$
f({\boldsymbol{\theta}}_{t-1})=Q({\boldsymbol{\theta}}_{t-1},{\boldsymbol{\theta}}_{t-1})\\
\geq\underset{{\boldsymbol{\theta}}}{\min}\ Q({\boldsymbol{\theta}},{\boldsymbol{\theta}}_{t-1})=Q({\boldsymbol{\theta}}_{t},{\boldsymbol{\theta}}_{t-1})\geq f({\boldsymbol{\theta}}_{t}),
$$

where we used in order, (11) (left), (12), and (11) (right). ∎

Note that the proposition still holds even if the minimization in (12) is replaced by any operation that merely reduces the value of $Q({\boldsymbol{\theta}},{\boldsymbol{\theta}}_{t-1})$. MM optimization has many desirable properties. It allows to tackle non-convex and/or non-smooth objective. Unlike gradient descent, it does not require tuning of a step size. Finally, the derived updates often have an intuitive interpretation. It has been applied to multi-dimensional scaling [^39], sparse norm minimization as the popular iteratively reweighted least-squares algorithm [^40], sub-sample time delay estimation [^41], and direction-of-arrival estimation [^38]. For in-depth theory, a general introduction, or more applications in signal processing, see [^14] [^42] [^43].

Input: Microphone signals $\boldsymbol{x}_{fn}\in\mathbb{C}^{M}$, $\forall f,n$

Output: Separated signals $\boldsymbol{y}_{fn}\in\mathbb{C}^{M}$, $\forall f,n$

 $\boldsymbol{W}_{f}\leftarrow\boldsymbol{I}_{K},\ \forall f$ $\boldsymbol{y}_{fn}\leftarrow\boldsymbol{x}_{fn},\ \forall f,n$

for *loop $\leftarrow 1$ to max. iterations* do

    $r_{kn}\leftarrow\sqrt{\sum_{f}|y_{kfn}|^{2}},\ \forall k,n$     $\boldsymbol{V}_{kf}\leftarrow\frac{1}{N}\sum_{n}\frac{G^{\prime}(r_{kn})}{2r_{kn}}\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}},\ \forall k,f$

   for *$f\leftarrow 1$ to $F$* do

       $\boldsymbol{W}_{f}\leftarrow\operatorname{Update}(\boldsymbol{W}_{f},\boldsymbol{V}_{1f},\ldots,\boldsymbol{V}_{Mf})$        $\boldsymbol{y}_{fn}\leftarrow\boldsymbol{W}_{f}\boldsymbol{x}_{fn},\ \forall n$

Algorithm 1 AuxIVA. The sub-routine Update performs one of IP, IP2, ISS, or IPA.

### II-C Auxiliary function based IVA

AuxIVA applies the MM technique to the IVA cost function (10) [^13]. This is done by restricting the contrast function to the class of spherical super-Gaussian source models.

###### Definition 1 (Spherical super-Gaussian contrast function ).

A spherical super-Gaussian contrast function depends only on the magnitude of the source vector, i.e.,

$$
F(\check{\boldsymbol{s}}_{kn})=G(\|\check{\boldsymbol{s}}_{kn}\|)
$$

and, in addition, $G\,:\,\mathbb{R}_{+}\to\mathbb{R}$ is a real, continuous, and differentiable function such that $G^{\prime}(r)/r$ is continuous everywhere and monotonically decreasing for $r>0$. Function $G^{\prime}(r)$ is the derivative of $G(r)$.

These contrast functions include Laplace, time-varying Gauss, Cauchy, and other popular source models [^26] [^30]. Conveniently, they can be majorized by a quadratic function.

###### Lemma 1 (Theorem 1 in ).

Let $G$ be as in Definition 1. Then,

$$
G(r)\leq G^{\prime}(r_{0})\frac{r^{2}}{2r_{0}}+\left(G(r_{0})-\frac{r_{0}}{2}G^{\prime}(r_{0})\right),
$$

with equality for $r=r_{0}$.

Equipped with this inequality, we can form $\ell_{2}$, a surrogate of (10) such that $\ell(\mathcal{W})\leq N\ell_{2}(\mathcal{W})+\text{constant}$,

$$
\ell_{2}(\mathcal{W})=\sum\nolimits_{kf}\boldsymbol{w}_{kf}^{\mathsf{H}}\boldsymbol{V}_{kf}\boldsymbol{w}_{kf}-2\sum\nolimits_{f}\log|\det\boldsymbol{W}_{f}|,
$$

where

$$
\boldsymbol{V}_{kf}=\frac{1}{N}\sum\nolimits_{n}\frac{G^{\prime}(r_{kn})}{2r_{kn}}\boldsymbol{x}_{fn}\boldsymbol{x}_{fn}^{\mathsf{H}},
$$

and $r_{kn}$ is an auxiliary variable. Conveniently, the surrogate is separable for $f$. In AuxIVA, described in Algorithm 1, the optimization at different frequencies is tied together by $r_{kn}$. Taking $r_{kn}=\|\check{\boldsymbol{y}}_{kn}\|$, with $\check{\boldsymbol{y}}_{kn}$ from (8), ensures that the surrogate is tangent to the objective, i.e. (11) (left). Interestingly, $r_{kn}$ is the magnitude of the source estimate from the previous iteration. Closed-form minimization is possible for two sources via the generalized eigenvalue decomposition. However, for more than two sources, it is still an open problem. Instead, a number of strategies updating the parameters alternatingly in a block-coordinate descent fashion have been proposed.

One of them is IP [^13] [^17]. It considers minimization of (17) with respect to only one demixing filter, e.g., $\boldsymbol{w}_{kf}$, keeping everything else fixed. In this case, the following closed-form solution exists,

$$
\displaystyle\boldsymbol{w}_{kf}\leftarrow\frac{(\boldsymbol{W}_{f}\boldsymbol{V}_{kf})^{-1}\boldsymbol{e}_{k}}{\boldsymbol{e}_{k}^{\top}\boldsymbol{W}^{-\mathsf{H}}\boldsymbol{V}_{kf}^{-1}\boldsymbol{W}^{-1}\boldsymbol{e}_{k}}.
$$

The update is applied for $k=1,\ldots,M$, in order.

IP2 is an improvement over IP whereas (17) is minimized with respect to two demixing filter, e.g. $\boldsymbol{w}_{kf},\boldsymbol{w}_{mf}$, keeping everything else fixed [^29] [^30]. First, form $\boldsymbol{P}_{uf}=(\boldsymbol{W}_{f}\boldsymbol{V}_{uf})^{-1}[\boldsymbol{e}_{k}\,\boldsymbol{e}_{m}]$, and let $\widetilde{\boldsymbol{V}}_{uf}=\boldsymbol{P}_{uf}^{\mathsf{H}}\boldsymbol{V}_{uf}\boldsymbol{P}_{uf}$, for $u=k,m$. Then, the new demixing filters are given by the generalized eigenvectors of the generalized eigenvalue problem $\widetilde{\boldsymbol{V}}_{kf}\boldsymbol{x}=\varphi\widetilde{\boldsymbol{V}}_{mf}\boldsymbol{x}$. The update is applied to pairs of sources, e.g., for three sources: $(1,2),(3,1),(2,3),$ etc.

Finally, ISS updates the whole demixing matrix [^31],

$$
\boldsymbol{W}_{f}\leftarrow\boldsymbol{W}_{f}-\boldsymbol{v}_{kf}\boldsymbol{w}_{kf}^{\mathsf{H}},
$$

where the $m$ th coefficient of $\boldsymbol{v}_{kf}$ is given by

$$
v_{mkf}=\begin{cases}\frac{\boldsymbol{w}_{mf}^{\mathsf{H}}\boldsymbol{V}_{mf}\boldsymbol{w}_{kf}}{\boldsymbol{w}_{kf}^{\mathsf{H}}\boldsymbol{V}_{mf}\boldsymbol{w}_{kf}}&\text{if $m\neq k$,}\\
1-(\boldsymbol{w}_{kf}^{\mathsf{H}}\boldsymbol{V}_{kf}\boldsymbol{w}_{kf})^{-\nicefrac{{1}}{{2}}}&\text{if $m=k$}.\end{cases}
$$

This corresponds in fact to an update of the $k$ th steering vector. This is performed for $k=1,\ldots,M$, in order, once per iteration.

## III Iterative Projection with Adjustment

We propose to perform an update that blends IP and ISS. We completely replace the $k$ th demixing filter, and, jointly, we adjust the values of all other filter by taking a step aligned with the current estimate of source $k$. This is implemented as the following multiplicative update of the demixing matrix,

$$
\boldsymbol{W}\leftarrow\boldsymbol{T}_{k}(\boldsymbol{u},\boldsymbol{q})\boldsymbol{W},
$$

where $\boldsymbol{u}\in\mathbb{C}^{M}$, $\boldsymbol{q}\in\mathbb{C}^{M-1}$, and,

$$
\boldsymbol{T}_{k}(\boldsymbol{u},\boldsymbol{q})=\boldsymbol{I}+\boldsymbol{e}_{k}(\boldsymbol{u}-\boldsymbol{e}_{k})^{\mathsf{H}}+\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\boldsymbol{e}_{k}^{\top},
$$

with $\bar{\boldsymbol{E}}_{k}$ being the $M\times(M-1)$ matrix containing all canonical basis vectors but the $k$ th,

$$
\displaystyle\bar{\boldsymbol{E}}_{k}
$$
 
$$
\displaystyle=\begin{bmatrix}\boldsymbol{e}_{1}&\cdots&\boldsymbol{e}_{k-1}&\boldsymbol{e}_{k+1}&\cdots&\boldsymbol{e}_{M}\end{bmatrix}.
$$

Without loss of generality, we can assume $\boldsymbol{W}=\boldsymbol{I}$, since in (17) it can be absorbed into the weighted covariance matrices $\boldsymbol{V}_{kf}$ and some constant factors. Note that we removed the index $f$ to lighten the notation, and because optimization of $(\ref{eqn:cost_auxiva})$ can be carried out separately for different $f$.

Plugging (22) into the IVA surrogate (17), we obtain

$$
\ell_{2}(\boldsymbol{u},\boldsymbol{q})=\sum_{m\neq k}(\boldsymbol{e}_{m}+q_{m}\boldsymbol{e}_{k})^{\mathsf{H}}\boldsymbol{V}_{m}(\boldsymbol{e}_{m}+q_{m}\boldsymbol{e}_{k})\\
+\boldsymbol{u}^{\mathsf{H}}\boldsymbol{V}_{k}\boldsymbol{u}-2\log|\det\boldsymbol{T}_{k}(\boldsymbol{u},\boldsymbol{q})|,
$$

and we want to find the optimal values of $\boldsymbol{u}$ and $\boldsymbol{q}$, i.e.,

$$
\boldsymbol{u}^{\star},\boldsymbol{q}^{\star}=\underset{\boldsymbol{u}\in\mathbb{C}^{M},\boldsymbol{q}\in\mathbb{C}^{M-1}}{\arg\min}\ \ell_{2}(\boldsymbol{u},\boldsymbol{q}).\\
$$

Albeit not convex, it turns out that the solution of this optimization problem can be found efficiently. First, we show that a closed-form solution for $\boldsymbol{u}$ as a function of $\boldsymbol{q}$ exists. Then, plugging the expression for $\boldsymbol{u}$ back in the cost function, we find that the optimal $\boldsymbol{q}$ is given by the solution of Problem 1. This is formalized in Theorem 1. An efficient algorithm to solve Problem 1 is described in the following section and the final procedure is given in Algorithm 2.

###### Theorem 1.

Let $\boldsymbol{V}_{1},\ldots,\boldsymbol{V}_{M}$ be $M$ Hermitian positive definite matrices. Then, the solution of (26) is as follows.

1. The optimal vector $\boldsymbol{u}^{\star}$ is given by
	$$
	\displaystyle\boldsymbol{u}^{\star}=\frac{\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}}{\sqrt{\tilde{\boldsymbol{q}}_{k}^{\mathsf{H}}\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}}}e^{j\theta}.
	$$
	where we defined $\tilde{\boldsymbol{q}}$ for convenience as
	$$
	\tilde{\boldsymbol{q}}_{k}=\boldsymbol{e}_{k}-\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*},
	$$
	and $\theta\in[0,2\pi]$ is an arbitrary phase.
2. The optimal $\boldsymbol{q}^{\star}$ is the solution to the following instance of Problem 1,
	$$
	\underset{\boldsymbol{q}\in\mathbb{C}^{M-1}}{\min}\ (\boldsymbol{q}+\boldsymbol{A}^{-1}\boldsymbol{b})^{\mathsf{H}}\boldsymbol{A}(\boldsymbol{q}+\boldsymbol{A}^{-1}\boldsymbol{b})\\
	-\log\left((\boldsymbol{q}-\boldsymbol{C}^{-1}\boldsymbol{g})^{\mathsf{H}}\boldsymbol{C}(\boldsymbol{q}-\boldsymbol{C}^{-1}\boldsymbol{g})+z\right)
	$$
	with
	$$
	\displaystyle\boldsymbol{A}
	$$
	 
	$$
	\displaystyle=\operatorname{diag}(\ldots,\,\boldsymbol{e}_{k}^{\top}\boldsymbol{V}_{m}\boldsymbol{e}_{k},\,\ldots),\quad m\neq k,
	$$
	$$
	\displaystyle\boldsymbol{b}
	$$
	 
	$$
	\displaystyle=\begin{bmatrix}\,\cdots&\boldsymbol{e}_{k}^{\top}\boldsymbol{V}_{m}\boldsymbol{e}_{m}&\cdots\,\end{bmatrix}^{\top},\quad m\neq k
	$$
	 
	$$
	\displaystyle\boldsymbol{C}
	$$
	 
	$$
	\displaystyle=\bar{\boldsymbol{E}}_{k}^{\top}(\boldsymbol{V}_{k}^{-1})^{*}\bar{\boldsymbol{E}}_{k},
	$$
	$$
	\displaystyle\boldsymbol{g}
	$$
	 
	$$
	\displaystyle=\bar{\boldsymbol{E}}_{k}^{\top}(\boldsymbol{V}_{k}^{-1})^{*}\boldsymbol{e}_{k},
	$$
	$$
	\displaystyle z
	$$
	 
	$$
	\displaystyle=\boldsymbol{e}_{k}^{\top}(\boldsymbol{V}_{k}^{-1})^{*}\boldsymbol{e}_{k}-\boldsymbol{g}^{\mathsf{H}}\boldsymbol{C}^{-1}\boldsymbol{g}.
	$$

Input: $\boldsymbol{W}$, $\boldsymbol{V}_{1}$, $\ldots$, $\boldsymbol{V}_{M}$

Output: Updated matrix $\boldsymbol{W}$

for *$k\leftarrow 1$ to $M$* do

    $\boldsymbol{A}\leftarrow\operatorname{diag}(\ldots,\,\boldsymbol{w}_{k}^{\mathsf{H}}\boldsymbol{V}_{m}\boldsymbol{w}_{k},\,\ldots),\quad m\neq k$     $\boldsymbol{b}\leftarrow\begin{bmatrix}\,\cdots&\boldsymbol{w}_{k}^{\mathsf{H}}\boldsymbol{V}_{m}\boldsymbol{w}_{m}&\cdots\,\end{bmatrix}^{\top},\quad m\neq k$     $\widetilde{\boldsymbol{V}}\leftarrow((\boldsymbol{W}\boldsymbol{V}_{k}\boldsymbol{W}^{\mathsf{H}})^{-1})^{*}$     $\boldsymbol{C}\leftarrow\bar{\boldsymbol{E}}_{k}^{\top}\widetilde{\boldsymbol{V}}\bar{\boldsymbol{E}}_{k}$     $\boldsymbol{g}\leftarrow\bar{\boldsymbol{E}}_{k}^{\top}\widetilde{\boldsymbol{V}}\boldsymbol{e}_{k}$     $z\leftarrow\boldsymbol{e}_{k}^{\top}\widetilde{\boldsymbol{V}}\boldsymbol{e}_{k}-\boldsymbol{g}^{\mathsf{H}}\boldsymbol{C}^{-1}\boldsymbol{g}$     $\boldsymbol{q},\lambda\leftarrow\operatorname{LQPQM}(\boldsymbol{A},-\boldsymbol{A}^{-1}\boldsymbol{b},\boldsymbol{C},\boldsymbol{C}^{-1}\boldsymbol{g},z)$     $\boldsymbol{u}\leftarrow\frac{1}{\sqrt{\lambda}}\widetilde{\boldsymbol{V}}(\boldsymbol{e}_{k}-\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*})$     $\boldsymbol{W}\leftarrow(\boldsymbol{I}+\boldsymbol{e}_{k}(\boldsymbol{u}^{\mathsf{H}}-\boldsymbol{e}_{k}^{\top})+\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\boldsymbol{e}_{k}^{\top})\boldsymbol{W}$

Algorithm 2 UpdateIPA: Update sub-routine of AuxIVA implementing IPA.

###### Proof.

We prove the two parts of the theorem in order.

1. Let us take the derivative of (25) with respect to $\boldsymbol{u}^{*}$, and
	$$
	\displaystyle\nabla_{\boldsymbol{u}^{*}}\mathcal{L}
	$$
	 
	$$
	\displaystyle=\boldsymbol{V}_{k}\boldsymbol{u}-\boldsymbol{T}_{k}^{-1}(\boldsymbol{u},\boldsymbol{q})\boldsymbol{e}_{k}.
	$$
	Equating to zero and multiplying by $\boldsymbol{T}_{k}^{-1}(\boldsymbol{u},\boldsymbol{q})$ from the left, we obtain the following equations,
	$$
	\displaystyle\boldsymbol{u}^{\mathsf{H}}\boldsymbol{V}_{k}\boldsymbol{u}
	$$
	 
	$$
	\displaystyle=1,
	$$
	$$
	\displaystyle(\bar{\boldsymbol{E}}_{k}^{\top}+\boldsymbol{q}^{*}\boldsymbol{e}_{k}^{\top})\boldsymbol{V}_{k}\boldsymbol{u}
	$$
	 
	$$
	\displaystyle=0.
	$$
	We can find an equation for $\boldsymbol{u}$ by seeing (37) as a null space constraint. Adding the extra equation $\boldsymbol{e}_{k}\boldsymbol{V}_{k}\boldsymbol{u}=\eta$, we have
	$$
	\displaystyle(\boldsymbol{I}+\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\boldsymbol{e}_{k}^{\top})\boldsymbol{V}_{k}\boldsymbol{u}=\eta\boldsymbol{e}_{k},
	$$
	where $\eta\in\mathbb{C}$ is an extra variable. We can use the matrix inverse lemma to give a closed form solution of $\boldsymbol{u}$ as a function of $\boldsymbol{q}$ and $\eta$,
	$$
	\displaystyle\boldsymbol{u}
	$$
	 
	$$
	\displaystyle=\eta\boldsymbol{V}_{k}^{-1}(\boldsymbol{I}+\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\boldsymbol{e}_{k}^{\top})^{-1}\boldsymbol{e}_{k}
	$$
	 
	$$
	\displaystyle=\eta\boldsymbol{V}_{k}^{-1}\left(\boldsymbol{I}-\frac{\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\boldsymbol{e}_{k}^{\top}}{1+\boldsymbol{e}_{k}^{\top}\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}}\right)\boldsymbol{e}_{k}
	$$
	 
	$$
	\displaystyle=\eta\boldsymbol{V}_{k}^{-1}\left(\boldsymbol{e}_{k}-\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\right)=\eta\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k},
	$$
	where we used the fact that $\boldsymbol{e}_{k}^{\top}\bar{\boldsymbol{E}}_{k}\boldsymbol{q}=0$. Now, we can compute $\eta$ from (36)
	$$
	\displaystyle\boldsymbol{u}^{\mathsf{H}}\boldsymbol{V}_{k}\boldsymbol{u}
	$$
	 
	$$
	\displaystyle=|\eta|^{2}\tilde{\boldsymbol{q}}_{k}^{\mathsf{H}}\boldsymbol{V}_{k}^{-1}\boldsymbol{V}_{k}\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}=1,
	$$
	and thus
	$$
	\displaystyle\eta=e^{j\theta}\left(\tilde{\boldsymbol{q}}^{\mathsf{H}}\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}\right)^{-\nicefrac{{1}}{{2}}}.
	$$
	Together with (41), this gives (27).
2. The proof of the second part follows from substituting $\boldsymbol{u}^{\star}$ from (27) into the objective function (25).
	1. By (36), the quadratic term in $\boldsymbol{u}$ equals one.
	2. Now, we handle the log-determinant part. In Appendix A, we show that
		$$
		\det(\boldsymbol{T}_{k})=\boldsymbol{u}^{\mathsf{H}}\tilde{\boldsymbol{q}}_{k}.
		$$
		Substituting $\boldsymbol{u}^{\star}$, we further have
		$$
		\displaystyle|(\boldsymbol{u}^{\star})^{\mathsf{H}}\tilde{\boldsymbol{q}}_{k}|=\left|\frac{\tilde{\boldsymbol{q}}_{k}^{\mathsf{H}}\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}}{\sqrt{\tilde{\boldsymbol{q}}_{k}^{\mathsf{H}}\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}}}\right|=\sqrt{\tilde{\boldsymbol{q}}_{k}^{\mathsf{H}}\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}}.
		$$
		Finally, with a little algebra, one can check that
		$$
		\tilde{\boldsymbol{q}}_{k}^{\mathsf{H}}\boldsymbol{V}_{k}^{-1}\tilde{\boldsymbol{q}}_{k}=(\boldsymbol{q}-\boldsymbol{C}^{-1}\boldsymbol{g})^{\mathsf{H}}\boldsymbol{C}(\boldsymbol{q}-\boldsymbol{C}^{-1}\boldsymbol{g})+z.
		$$
	3. As shown in Appendix B, the remaining quadratic terms can be transformed into a standard quadratic form as follows
		$$
		\sum_{m\neq k}(\boldsymbol{e}_{m}+q_{m}\boldsymbol{e}_{k})^{\mathsf{H}}\boldsymbol{V}_{m}(\boldsymbol{e}_{m}+q_{m}\boldsymbol{e}_{k})\\
		=(\boldsymbol{q}+\boldsymbol{A}^{-1}\boldsymbol{b})^{\mathsf{H}}\boldsymbol{A}(\boldsymbol{q}+\boldsymbol{A}^{-1}\boldsymbol{b})-\boldsymbol{b}^{\mathsf{H}}\boldsymbol{A}^{-1}\boldsymbol{b}+\boldsymbol{1}^{\top}\boldsymbol{c},
		$$
		where $c_{m}=\boldsymbol{e}_{m}^{\top}\boldsymbol{V}_{m}\boldsymbol{e}_{m}$, and $\boldsymbol{1}$ is the all one vector.
	Removing the constant terms yields the proof.

∎

## IV Log-quadratically Penalized Quadratic Minimization

We will now provide an efficient algorithm to compute the solution of Problem 1. It is interesting to take a look at the landscape of one instance of the 2D problem as shown in Fig. 1. Let us first try to give an intuitive and informal description of the problem. The quadratic term of the objective forms the familiar bowl shape, and the log-quadratic term appears like someone pinched and pulled up the "fabric" of the cost function in one point. The location of the "pinch", described by offset vectors $\boldsymbol{b}$ and $\boldsymbol{d}$, as well as the offset $z$ in the log, may create different patterns of stationary points. In the 2D case of Fig. 1, we observe two "bowls", separated by a kind of ridge, which is due to the log-quadratic term. There are in fact only a finite number of stationary points, five in Fig. 1, to be precise. In the rest of this section, we will make precise this intuitive description, and give a procedure to find the global minimum.

Since $\boldsymbol{A}$ (in Problem 1) is Hermitian positive definite, it has a Cholesky decomposition, which can be inverted. This allows to consider the following alternative form of LQPQM instead.

###### Problem 2 (LQPQM alternative form).

Let $\boldsymbol{U}\in\mathbb{C}^{d\times d}$ be Hermitian positive semi-definite, and $\boldsymbol{v}\in\mathbb{C}^{d}$.

$$
\underset{\boldsymbol{y}\in\mathbb{C}^{d}}{\min}\ \boldsymbol{y}^{\mathsf{H}}\boldsymbol{y}-\log\left((\boldsymbol{y}+\boldsymbol{v})^{\mathsf{H}}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})+z\right)
$$

The two problems are equivalent, as we explain now.

###### Proposition 2.

Let $\boldsymbol{G}$ be such that $\boldsymbol{A}=\boldsymbol{G}^{\mathsf{H}}\boldsymbol{G}$. Further, let $\boldsymbol{y}^{\star}$ be the optimum of (P2) with

$$
\displaystyle\boldsymbol{U}=\boldsymbol{G}^{-\mathsf{H}}\boldsymbol{C}\boldsymbol{G}^{-1},\quad\text{and}\quad\boldsymbol{v}=\boldsymbol{G}(\boldsymbol{b}-\boldsymbol{d}).
$$

Then, the optimum of Problem 1 is

$$
\boldsymbol{x}^{\star}=\boldsymbol{G}^{-1}\boldsymbol{y}+\boldsymbol{b}.
$$

###### Proof.

Let $\boldsymbol{y}=\boldsymbol{G}(\boldsymbol{x}-\boldsymbol{b})$, and substitute in (P1). ∎

###### Proposition 3.

The objective function of (P2) is bounded from below and takes its minimum at a finite value.

###### Proof.

See Appendix C. ∎

The next two theorems fully characterize the solution of Problem 1 and 2. Theorem 2 handles the case when the offset vector $\boldsymbol{v}$ is zero (or $\boldsymbol{b}=\boldsymbol{d}$ in Problem 1). There, the solution can be obtained from the eigendecomposition of $\boldsymbol{U}$. Note that the eigendecomposition of $\boldsymbol{U}$ is equivalent to the generalized eigendecomposition of $\boldsymbol{A}$ and $\boldsymbol{B}$. When $\boldsymbol{v}\neq\boldsymbol{0}$, the solution can be computed by solving a secular equation as explained in Theorem 3. An algorithmic instantiation of these two theorems is provided by Algorithm 3.

###### Theorem 2 (Special Case, 𝒗=𝟎\\boldsymbol{v}=\\boldsymbol{0}).

The global minimum of (P2) is characterized as follows. Let $\varphi_{1}\leq\ldots\leq\varphi_{d}$ be the eigenvalues of $\boldsymbol{U}$, and ${\boldsymbol{\sigma}}_{1},\ldots,{\boldsymbol{\sigma}}_{d}$, the corresponding eigenvectors.

1. If $z\geq\varphi_{d}$, the unique global minimum of (P2) is $\boldsymbol{y}^{\star}=\boldsymbol{0}$.
2. If $z<\varphi_{d}$, the minimum of (P2) is given by
	$$
	\boldsymbol{y}^{\star}=e^{j\theta}\sqrt{\frac{\varphi_{d}-z}{\tilde{{\boldsymbol{\sigma}}}^{\mathsf{H}}\boldsymbol{U}\tilde{{\boldsymbol{\sigma}}}}}\tilde{{\boldsymbol{\sigma}}},
	$$
	where $\theta\in[0,2\pi]$ is an arbitrary phase. If $\varphi_{d}>\varphi_{d-1}$, the global minimum is unique (up to the phase $\theta$) and given by $\tilde{{\boldsymbol{\sigma}}}={\boldsymbol{\sigma}}_{d}$. If the largest eigenvalue has multiplicity $k$, then any linear combination $\tilde{{\boldsymbol{\sigma}}}$ of ${\boldsymbol{\sigma}}_{d-k},\ldots,{\boldsymbol{\sigma}}_{d}$ is a global minimum.

###### Theorem 3 (General Case, 𝒗≠𝟎\\boldsymbol{v}\\neq\\boldsymbol{0}).

Let $\boldsymbol{U}=\boldsymbol{\Sigma}{\boldsymbol{\Phi}}\boldsymbol{\Sigma}^{\mathsf{H}}$ be the eigendecomposition of $\boldsymbol{U}$, with ${\boldsymbol{\Phi}}=\operatorname{diag}(\varphi_{1},\ldots,\varphi_{d})$, where $\varphi_{1}\leq\ldots\leq\varphi_{d}$ are the eigenvalues of $\boldsymbol{U}$. Then, the unique global minimum of (P2) is

$$
\boldsymbol{y}^{\star}=(\lambda^{\star}\boldsymbol{I}-\boldsymbol{U})^{-1}\boldsymbol{U}\boldsymbol{v}
$$

where $\lambda^{\star}$ is the largest root of the function $f\,:\,\mathbb{R}_{+}\to\mathbb{R}$,

$$
f(\lambda)=\lambda^{2}\sum_{m\in\mathcal{S}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})^{2}}-\lambda+z,
$$

where $\tilde{v}_{m}$ are the coefficients of the vector $\tilde{\boldsymbol{v}}=\boldsymbol{\Sigma}^{\mathsf{H}}\boldsymbol{v}$, and $\mathcal{S}$ is the common support of $\tilde{v}$ and the eigenvalues,

$$
\mathcal{S}=\{m\,:\,\varphi_{m}|\tilde{v}_{m}|^{2}\neq 0\}.
$$

Furthermore, the largest root is the unique root located in the interval $(\max(\varphi_{\max},z),+\infty)$, where $\varphi_{\max}=\max_{m\in\mathcal{S}}\ \varphi_{m}$. In this interval, $f(\lambda)$ is strictly decreasing.

Because the optimal $\lambda$ is restricted to an interval where $f(\lambda)$ is strictly decreasing, we may use a root finding algorithm such as Newton-Raphson to compute it efficiently, Initialization and stability aspects of the root finding are covered in Section IV-C. The complete procedure for LQPQM is described in Algorithm 3. Algorithm 4 is the sub-routine that solves the secular equation.

Fig. 1: The loss landscape of an instance of the 2D LQPQM shown with in a 3D (left) and 2D (right) contour plots. The global minimum is indicated by an $\times$ on the right figure.

Input: $\boldsymbol{A}$, $\boldsymbol{b}$, $\boldsymbol{C}$, $\boldsymbol{d}$, $z$

Output: $\boldsymbol{x}$, $\lambda$, solution to Problem 1

 $\boldsymbol{G}\leftarrow\operatorname{Cholesky}(\boldsymbol{A})$ $\boldsymbol{U}\leftarrow\boldsymbol{G}^{-\mathsf{H}}\boldsymbol{C}\boldsymbol{G}^{-1}$ ${\boldsymbol{\Phi}},\boldsymbol{\Sigma}\leftarrow\operatorname{EigenValueDecomposition}(\boldsymbol{U})$

if *$\boldsymbol{b}=\boldsymbol{d}$* then

   if *$z\geq\varphi_{d}$* then

       $\lambda\leftarrow z$        $\boldsymbol{y}\leftarrow\boldsymbol{0}$

   else

       $\lambda\leftarrow\varphi_{d}$        $\boldsymbol{y}\leftarrow\sqrt{\frac{\varphi_{d}-z}{{\boldsymbol{\sigma}}_{d}^{\mathsf{H}}\boldsymbol{U}{\boldsymbol{\sigma}}_{d}}}{\boldsymbol{\sigma}}_{d}$

else

    $\tilde{\boldsymbol{v}}\leftarrow\boldsymbol{\Sigma}^{\mathsf{H}}\boldsymbol{G}(\boldsymbol{b}-\boldsymbol{d})$     $\mu\leftarrow\operatorname{SolveSecularEquation}\left(\frac{{\boldsymbol{\Phi}}}{\varphi_{\max}},\frac{\tilde{\boldsymbol{v}}}{\varphi_{\max}},\frac{z}{\varphi_{\max}}\right)$     $\lambda\leftarrow\mu\,\varphi_{\max}$     $\boldsymbol{y}\leftarrow\boldsymbol{\Sigma}(\lambda\boldsymbol{I}-{\boldsymbol{\Phi}})^{-1}{\boldsymbol{\Phi}}\tilde{\boldsymbol{v}}$ $\boldsymbol{x}\leftarrow\boldsymbol{G}^{-1}\boldsymbol{y}+\boldsymbol{b}$

Algorithm 3 LQPQM

### IV-A

The special case, $\boldsymbol{v}=\boldsymbol{0}$, leads to the simpler problem,

$$
\underset{\boldsymbol{x}\in\boldsymbol{C}^{d}}{\min}\ \boldsymbol{y}^{\mathsf{H}}\boldsymbol{y}-\log(\boldsymbol{y}^{\mathsf{H}}\boldsymbol{U}\boldsymbol{y}+z).
$$

Equating the gradient to zero, and adding an extra non-negative variable $\lambda\geq 0$, we can obtain the following first order necessary optimality conditions,

$$
\left\{\begin{array}[]{rl}\boldsymbol{U}\boldsymbol{y}&=\lambda\boldsymbol{y},\\
\lambda&=\boldsymbol{y}^{\mathsf{H}}\boldsymbol{U}\boldsymbol{y}+z.\end{array}\right.
$$

Solutions to this system of equations are stationary points.

- The trivial solution to (54): $\lambda=z$, $\boldsymbol{y}=\boldsymbol{0}$.
- The eigenvalue/vectors of $\boldsymbol{U}$ also provide the solutions,
	$$
	\lambda=\varphi_{i},\quad\boldsymbol{y}=e^{j\theta}\sqrt{\frac{\varphi_{i}-z}{{\boldsymbol{\sigma}}_{i}^{\mathsf{H}}\boldsymbol{U}{\boldsymbol{\sigma}}_{i}}}{\boldsymbol{\sigma}}_{i},
	$$
	where $\theta\in[0,2\pi]$ is an arbitrary phase, for all $\varphi_{i}\geq z$.

From (54), we can obtain $\boldsymbol{y}^{\mathsf{H}}\boldsymbol{y}=(\lambda-z)/\lambda$. Together with the second equation in (54), we can rewrite the objective as a function of $\lambda$,

$$
g(\lambda)=-\log\lambda+\frac{\lambda-z}{\lambda}.
$$

The derivative is

$$
g^{\prime}(\lambda)=\frac{z-\lambda}{\lambda^{2}},
$$

and $g(\lambda)$ is thus decreasing for $\lambda>z$. Thus, if $\varphi_{d}\geq z$, the solution is given by the largest eigenvector (or eigenvectors if the multiplicity of the largest eigenvalue is more than one). Otherwise, the optimum is zero. $\square$

### IV-B

Equating the gradient of the objective of (P2) with respect to $\boldsymbol{y}^{*}$ to zero, we obtain the following equation,

$$
\boldsymbol{y}-\frac{\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})}{(\boldsymbol{y}+\boldsymbol{v})^{\mathsf{H}}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})+z}=\boldsymbol{0}.
$$

As in the previous section, we isolate the quadratic term in a second equation by adding the non-negative variable $\lambda\geq 0$, and obtain the following first order optimality conditions,

$$
\left\{\begin{array}[]{rl}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})&=\lambda\boldsymbol{y},\\
\lambda&=(\boldsymbol{y}+\boldsymbol{v})^{\mathsf{H}}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})+z.\end{array}\right.
$$

Solving for $\boldsymbol{y}$, we obtain a solution as a function of $\lambda$,

$$
\boldsymbol{y}(\lambda)=(\lambda\boldsymbol{I}-\boldsymbol{U})^{-1}\boldsymbol{U}\boldsymbol{v}.
$$

Switching to the eigenbasis of $\boldsymbol{U}$ and substituting into the second equation leads to

$$
\displaystyle\lambda
$$
 
$$
\displaystyle=\|{\boldsymbol{\Phi}}^{\nicefrac{{1}}{{2}}}((\lambda\boldsymbol{I}-{\boldsymbol{\Phi}})^{-1}{\boldsymbol{\Phi}}+\boldsymbol{I})\tilde{\boldsymbol{v}}\|^{2}+z
$$
 
$$
\displaystyle=\lambda^{2}\sum_{m\in\mathcal{S}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})^{2}}+z.
$$

This gives us the necessary condition that $f(\lambda)=0$ for any stationary point of (P2). Now this equation may have multiple roots, so we need to find the one with the lowest value of the objective. It turns out that the value of the objective can also be written as a function of $\lambda$ only. First, we expand the left-most factor of the second equation in (59) to obtain,

$$
\displaystyle\lambda
$$
 
$$
\displaystyle=\boldsymbol{y}^{\mathsf{H}}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})+\boldsymbol{v}^{H}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})+z.
$$

From the first equation in (59), we have

$$
\displaystyle\boldsymbol{y}^{\mathsf{H}}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})
$$
 
$$
\displaystyle=\lambda\boldsymbol{y}^{\mathsf{H}}\boldsymbol{y}.
$$

Then, by (60), we find the second term

$$
\displaystyle\boldsymbol{v}^{\mathsf{H}}\boldsymbol{U}(\boldsymbol{y}+\boldsymbol{v})
$$
 
$$
\displaystyle=\boldsymbol{v}^{\mathsf{H}}(\boldsymbol{U}(\lambda\boldsymbol{I}-\boldsymbol{U})^{-1}\boldsymbol{U}+\boldsymbol{U})\boldsymbol{v}.
$$

Substituting into the second condition in (63) gives us

$$
\displaystyle\lambda
$$
 
$$
\displaystyle=\lambda\boldsymbol{y}^{\mathsf{H}}\boldsymbol{y}+\boldsymbol{v}^{\mathsf{H}}(\boldsymbol{U}(\lambda\boldsymbol{I}-\boldsymbol{U})^{-1}\boldsymbol{U}+\boldsymbol{U})\boldsymbol{v}+z.
$$

Using the eigendecomposition of $\boldsymbol{U}$ and rearranging terms,

$$
\boldsymbol{y}^{\mathsf{H}}\boldsymbol{y}=1-\sum_{m\in\mathcal{S}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})}-\frac{z}{\lambda}.
$$

Finally, replacing into the objective, we obtain

$$
g(\lambda)=1-\sum_{m\in\mathcal{S}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})}-\frac{z}{\lambda}-\log\lambda.
$$

Thus, the optimal $\lambda$ is the solution to the following optimization problem,

$$
\underset{\lambda\in\mathbb{R}_{+}}{\min}\ g(\lambda),\quad\text{subject to}\ f(\lambda)=0.
$$

where $f(\lambda)$ is defined in (51). In Fig. 2, we show the functions $g(\lambda)$ and $f(\lambda)$ for the instance of LQPQM of Fig. 1. This new problem is highly non-linear and the objective is not even continuous. However, we can show that $f(\lambda)$ only has a finite number of roots and that the largest, $\lambda^{\star}$, has the minimum value of the objective among them. In the next series of lemmas, we characterize all the roots of $f(\lambda)$. We show that the value of the cost function decreases for increasing roots. As a consequence, the largest root is the global minimum of the cost function. In the following, to lighten the notation, we assume, without loss of generality, that $\mathcal{S}=\{1,\ldots,d\}$.

###### Lemma 2.

The function $f(\lambda)$ has

1. no roots smaller or equal to $z$,
2. zero, one, or two roots in $(z,\varphi_{k})$, with $\varphi_{k}$ being the smallest eigenvalue larger than $z$, if such a root exists,
3. zero, one, or two roots in $(\varphi_{L-1},\varphi_{L})$ for $L=k+1,\ldots,d$,
4. a unique root in the interval $(\max(\varphi_{\max},z),+\infty)$.

###### Proof.

The proof proceeds by inspection of the first and second derivatives of $f(\lambda)$,

$$
\displaystyle f^{\prime}(\lambda)
$$
 
$$
\displaystyle=-2\lambda\sum_{m\in\mathcal{S}}\frac{\varphi_{m}^{2}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})^{3}}-1,
$$
$$
\displaystyle f^{\prime\prime}(\lambda)
$$
 
$$
\displaystyle=2\sum_{m\in\mathcal{S}}\varphi_{m}^{2}|\tilde{v}_{m}|^{2}\frac{2\lambda+\varphi_{m}}{(\lambda-\varphi_{m})^{4}}.
$$
1. Follows from $z-\lambda\geq 0$ in $(0,z)$, and
	$$
	\lambda^{2}\sum_{m\in\mathcal{S}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})^{2}}>0,\quad\text{if $\lambda>0$}.
	$$
2. In $(z,\varphi_{k})$, we have
	$$
	\displaystyle f(z)>0,\quad f(\varphi_{k}-\epsilon)\underset{\epsilon\to 0}{\longrightarrow}+\infty,
	$$
	and because $f^{\prime\prime}(\lambda)>0$ in this interval, the function there is strictly convex with a unique minimum. If the minimum is larger than zero, there is no root. If the minimum is zero, there is one root. If the minimum is less than zero, there are two roots.
3. In $(\varphi_{L-1},\varphi_{L})$, we have
	$$
	\displaystyle f(\varphi_{L-1}+\epsilon)\underset{\epsilon\to 0}{\longrightarrow}+\infty,\quad f(\varphi_{L}-\epsilon)\underset{\epsilon\to 0}{\longrightarrow}+\infty,
	$$
	and $f^{\prime\prime}(\lambda)>0$, thus, $f(\lambda)$ is strictly convex with a unique minimum, as in 2.
4. In $(\max(\varphi_{\max},z),+\infty)$, $f^{\prime}(\lambda)<0$ because $\varphi_{m}>0$ for all $m$, and $\lambda>\max(\varphi_{\max},z)$. In addition, we have
	$$
	\displaystyle f(\varphi_{\max}+\epsilon)\underset{\epsilon\to 0}{\longrightarrow}+\infty,\quad\text{and}\quad f(\lambda)\underset{\lambda\to+\infty}{\longrightarrow}-\infty,
	$$
	and thus there is exactly one root in this interval. By 1), the root is in $(z,+\infty)$ if $z>\varphi_{\max}$.

∎

###### Corollary 1.

The roots of $f(\lambda)$ are strictly larger than 0.

###### Proof.

By Lemma 2, 1), if $f(\lambda)=0$, then $\lambda>z\geq 0$. ∎

###### Fact 1.

The derivative of $g(\lambda)$ is $g^{\prime}(\lambda)=\frac{1}{\lambda^{2}}f(\lambda)$.

###### Lemma 3.

If $f(\lambda)$ has roots $0<\lambda_{1}\leq\lambda_{2}$ in $(\varphi_{L-1},\varphi_{L})$, then, $f(\lambda_{1})\geq f(\lambda_{2})$.

###### Proof.

From Fact 1, we know that the roots of $f(\lambda)$ are stationary points of $g(\lambda)$. Moreover, because $f(\lambda)$ is convex with a unique minimum in the interval, $f(\lambda)<0$ for $\lambda\in(\lambda_{1},\lambda_{2})$. Thus, $g^{\prime}(\lambda)=\frac{1}{\lambda^{2}}f(\lambda)<0$ for $\lambda\in(\lambda_{1},\lambda_{2})$, and the proof follows. ∎

Fig. 2: The secular equation $f(\lambda)$ corresponding to the 2D LQPQM in Fig. 1, its objective $g(\lambda)$, and the cubic polynomial used for the initialization of the root finding. The optimal $\lambda^{\star}$ is the largest root of $f(\lambda)$.

###### Lemma 4.

Let $\lambda_{1}\in(\varphi_{L-1},\varphi_{L})$ and $\lambda_{2}\in(\varphi_{L+K},\varphi_{L+K+1})$ such that $f(\lambda_{1})=f(\lambda_{2})=0$, for some $L\in\{1,\ldots,d\}$ and $K\in\{0,\ldots,d-L\}$. For convenience, we defined $\varphi_{0}=z$ and $\varphi_{d+1}=+\infty$. Then $g(\lambda_{1})\geq g(\lambda_{2})$.

###### Proof.

First, we define two functions $\bar{f}_{\mathcal{A}}(\lambda)$ and $\bar{g}_{\mathcal{A}}(\lambda)$, that are similar to $f(\lambda)$ and $g(\lambda)$, respectively, but with all the discontinuous terms between $\lambda_{1}$ and $\lambda_{2}$ removed. Then, we show that $\bar{g}_{\mathcal{A}}(\lambda)$ is decreasing in $(\lambda_{1},\lambda_{2})$ with $g(\lambda_{1})$ and $g(\lambda_{2})$ strictly above and below $\bar{g}_{\mathcal{A}}(\lambda)$, respectively.

Let $\mathcal{A}=\{L,\ldots,L+K\}$ and define

$$
\displaystyle f_{\mathcal{A}}(\lambda)
$$
 
$$
\displaystyle=\lambda^{2}\sum_{m\in\mathcal{A}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})^{2}}\geq 0
$$
 
$$
\displaystyle g_{\mathcal{A}}(\lambda)
$$
 
$$
\displaystyle=-\sum_{m\in\mathcal{A}}\frac{\varphi_{m}|\tilde{v}_{m}|^{2}}{(\lambda-\varphi_{m})}\ \begin{cases}>0&\text{if $\lambda<\varphi_{L}$}\\
<0&\text{if $\lambda>\varphi_{L+K}$}\\
\end{cases}
$$

Then, let $\bar{f}_{\mathcal{A}}(\lambda)=f(\lambda)-f_{\mathcal{A}}(\lambda)$, and $\bar{g}_{\mathcal{A}}(\lambda)=g(\lambda)-g_{\mathcal{A}}(\lambda)$. Note that these two functions are continuous in $(\lambda_{1},\lambda_{2})$. Since $f_{\mathcal{A}}(\lambda)\geq 0$, we have

$$
\displaystyle\bar{f}_{\mathcal{A}}(\lambda_{p})\leq f(\lambda_{p})=0,\quad\text{for $p=1,2$.}
$$

Together with Lemma 2, this means that $\bar{f}_{\mathcal{A}}(\lambda)$ has two roots in $(\varphi_{L-1},\varphi_{L+K+1})$, or just one if $\varphi_{L+K+1}=+\infty$. As a consequence, $\bar{g}^{\prime}_{\mathcal{A}}(\lambda)=\frac{1}{\lambda^{2}}\bar{f}_{\mathcal{A}}(\lambda)<0$ for $\lambda\in(\lambda_{1},\lambda_{2})$. And, thus, $\bar{g}_{\mathcal{A}}(\lambda)$ is strictly decreasing on this interval.

Then, because $g_{\mathcal{A}}(\lambda_{1})>0$ and $g_{\mathcal{A}}(\lambda_{2})<0$, we have

$$
\displaystyle g(\lambda_{1})>\bar{g}_{\mathcal{A}}(\lambda_{1}),\quad\text{and,}\quad g(\lambda_{2})<\bar{g}_{\mathcal{A}}(\lambda_{1}),
$$

respectively. Finally, because $\bar{g}_{\mathcal{A}}(\lambda)$ is strictly decreasing in the interval,

$$
g(\lambda_{1})>\bar{g}_{\mathcal{A}}(\lambda_{1})>\bar{g}_{\mathcal{A}}(\lambda_{2})>g(\lambda_{2}),
$$

which concludes the proof. ∎

Input: ${\boldsymbol{\Phi}}$, $\tilde{\boldsymbol{v}}$, $z$

Output: Largest zero of $f(\lambda)$

 $\lambda\leftarrow\operatorname{InitCubicPoly}(\varphi_{\max},\tilde{v}_{\max},z)$ $\lambda\leftarrow\max(\lambda,z)$

while *$|f(\lambda)|>\epsilon$* do

    $\mu\leftarrow\lambda-\frac{f(\lambda)}{f^{\prime}(\lambda)}$

   if *$\mu>\varphi_{\max}$* then

       $\lambda\leftarrow\mu$

   else

       $\lambda\leftarrow\frac{\varphi_{\max}+\lambda}{2}$

Algorithm 4 SolveSecularEquation. The sub-routine InitCubicPoly returns the largest real root of the cubic polynomial (81).

### IV-C Root finding

The solution to the general problem (P2) is given by the largest root of $f(\lambda)$, from (51). We have shown that the root is in $(\max(\varphi_{\max},z),+\infty)$, and we can thus use a root finding algorithm to find it. Several methods are possible, but we opt for Newton-Raphson,

$$
\lambda_{t}\leftarrow\lambda_{t-1}-\frac{f(\lambda_{t-1})}{f^{\prime}(\lambda_{t-1})},\quad t=1,\ldots,T,
$$

where $f^{\prime}(\lambda)$ is given in (70). With a good enough starting point $\lambda_{0}$, this method converges in just a few iterations.

#### IV-C1 Initialization

Because the inverse square terms in $f(\lambda)$ decay quickly, when $\lambda>\varphi_{\max}$, we can approximate

$$
f(\lambda)\approx\lambda^{2}\frac{\varphi_{\max}|v_{\max}|^{2}}{(\lambda-\varphi_{\max})^{2}}-\lambda+z
$$

where $\varphi_{d}$ is the largest eigenvalue. Note that this approximation is guaranteed to have its largest zero in the same interval as $f(\lambda)$, which is important for Newton-Raphson. Equating to zero and multiplying by $(\lambda-\varphi_{\max})^{2}$ on both sides leads to a cubic equation in $\lambda$ (see also Fig. 2),

$$
-\lambda^{3}+(\varphi_{\max}|\tilde{v}_{\max}|^{2}+2\varphi_{\max}+z)\lambda^{2}\\
-(\varphi_{\max}+2z)\varphi_{\max}\lambda+\varphi_{\max}^{2}z=0.
$$

Cubic equation have three solutions including at least one real, and two possibly complex. We will thus use the largest real solution as a starting point for the root finding.

#### IV-C2 Numerical Stability

When the eigenvalues are large, computation of $(\lambda-\varphi_{m})^{-2}$ may lead to an overflow, jeopardizing the algorithm. Instead, we consider

$$
\hat{f}(\mu)=\frac{1}{\varphi_{\max}}f(\varphi_{\max}\mu)=\mu^{2}\sum\nolimits_{m}\frac{\hat{\varphi}_{m}|\hat{v}_{m}|^{2}}{(\mu-\hat{\varphi}_{m})^{2}}-\mu+\hat{z},
$$

with $\hat{\varphi}_{m}=\varphi_{m}/\varphi_{\max}$, $\hat{v}_{m}=\tilde{v}_{m}/\varphi_{\max}$, and $\hat{z}=z/\varphi_{\max}$. We can find the largest root of $\hat{f}(\mu)=0$, $\mu^{*}$, according to Lemma 2. Then, the largest root of $f(\lambda)$ is $\lambda^{*}=\varphi_{\max}\,\mu^{*}$.

## V Numerical Experiments

The effectiveness of the proposed IPA updates for AuxIVA is compared to that of competing methods: IP [^13], ISS [^25], and IP2 [^29] [^30]. The experiments are done on simulated reverberant speech mixtures and the performance is evaluated in terms of scale-invariant signal-to-distortion and signal-to-interference ratios (SI-SDR and SI-SIR, respectively) [^44]. We evaluate different numbers of sources/microphones and signal-to-noise ratios (SNR).

### V-A Setup

Fig. 3: Box-plots of the final SI-SDR (left) and SI-SIR (right) values after a hundred iterations. From top to bottom, the SNR is $5\text{\,}\mathrm{dB}$, $15\text{\,}\mathrm{dB}$, and $25\text{\,}\mathrm{dB}$. In subplots, from left to right, the number of sources goes from two to five.

Fig. 4: Evolution of the average SI-SIR over number of iterations or runtime in the top and bottom row, respectively. The number of sources increases from two to five from left to right. The SNR is $25\text{\,}\mathrm{dB}$.

We simulate 100 random rectangular rooms with the pyroomacoustics Python package [^45]. The walls are between $6\text{\,}\mathrm{m}$ and $10\text{\,}\mathrm{m}$ long, and the ceiling from $2.8\text{\,}\mathrm{m}$ to $4.5\text{\,}\mathrm{m}$ high. Simulated reverberation times ($T_{60}$) are approximately uniformly sampled between $60\text{\,}\mathrm{ms}$ and $450\text{\,}\mathrm{ms}$. Sources and microphone array are placed at random at least $50\text{\,}\mathrm{cm}$ away from the walls and between $1\text{\,}\mathrm{m}$ and $2\text{\,}\mathrm{m}$ high. The array is circular and regular with 2, 3, 4, or 5 microphones, and radius such that neighboring elements are $10\text{\,}\mathrm{cm}$ apart. All sources are placed further from the array than the critical distance of the room — the distance where direct sound and reverberation have equal energy. It is computed as $d_{\text{crit}}=0.057\sqrt{V/T_{60}}\,$\mathrm{m}$$, with $V$ the volume of the room [^46]. Uncorrelated Gaussian noise with variance $\sigma_{n}^{2}$ is added to the microphone inputs. The source signals are normalized to have equal variance $\sigma_{s}^{2}$ at the first microphone, and $\sigma_{n}^{2}$ chosen so that the SNR, defined as $\operatorname{SNR}=M\sigma_{s}^{2}/\sigma_{n}^{2}$, where $M$ is the number of sources, is $5\text{\,}\mathrm{dB}$, $15\text{\,}\mathrm{dB}$, or $25\text{\,}\mathrm{dB}$.

The simulation is conducted at 16 kHz with concatenated utterances from the CMU Arctic corpus [^47] [^48]. We use an STFT with a 4096-points Hamming analysis window and $\nicefrac{{3}}{{4}}$ -overlap. Reconstruction uses the optimal synthesis window [^49]. All algorithms are run for 100 iterations and with the microphone signals as initial source estimates. Because IP2 and IPA update twice as many parameters per iteration than IP and ISS, each of their iteration is counted twice, so that the total number of parameter updates are about the same for all algorithms. The scale of the output is restored by minimizing distortion with respect to the first microphone [^50] [^51].

### V-B Results

First, we compare the final value of the SI-SDR and SI-SIR after 100 iterations. Fig. 3 shows box-plots for different numbers of sources and SNR. In all cases, the proposed IPA updates attain the same or a higher final performance. For larger number of sources and lower SNR, especially, we observe that IPA performs clearly better, even compared to IP2. For two sources, IP and ISS have slightly higher final SI-SIR values. This is due to IP and ISS converging slower, but also overshooting in terms of SI-SIR, as seen in Fig. 4.

Next, we look at the convergence of the SI-SIR as a function of the number of iterations and runtime. Fig. 4 shows the results for SNR $25\text{\,}\mathrm{dB}$. This is where IPA really shines as it outperforms all other methods for all number of sources. In terms of number of iterations, IPA is closely tied to IP2 for 2 and 3 Microphones. But when the x-axis is scaled according to the runtime of one iteration (for $1\text{\,}\mathrm{s}$ of input signal, the so-called real-time factor), then IPA converges faster overall. In the two source cases, IP2 performs globally optimal minimization of the surrogate function (17), and it is thus surprising that IPA seems to converge faster. This might suggest some subtle effects in the minimization of the underlying objective function (10) that we believe deserve further study. For four and five sources, IPA converges more than twice faster than IP2, which makes it a good candidate for high performance implementations.

## VI Conclusion

We proposed a new algorithm for the MM-based independent vector analysis algorithm AuxIVA. Unlike previous methods that only update parts of the demixing matrix at a time, we introduced iterative projection with adjustment (IPA) that updates the whole demixing matrix with a multiplicative update. In the derivation of the IPA update, we stumbled upon a generic optimization problem that we call log-quadratically penalized quadratic minimization (LQPQM). Despite being non-convex, its global minimum can be computed efficiently. To the best of our knowledge, this problem had not been solved before. We assessed the performance of AuxIVA with the IPA updates in numerical experiments with simulated reverberant speech mixtures. We found IPA to outperform all other methods in terms of convergence speed, both for iteration count and runtime, significantly so for four sources and more.

In future work, we hope to evaluate the impact of IPA updates on more source models, e.g. in ILRMA [^21], and in the overdetermined [^25] [^30] and underdetermined [^52] regimes. Another interesting question is whether LQPQM is applicable in other contexts. The log-penalty suggests it might be useful for barrier-based interior point methods. Another possibility is the maximization of the information theoretic capacity subject to a quadratic penalty or constraint [^53].

## Acknowledgment

We would like to acknowledge the work of the open source scientific Python community, on which the code for this paper relies. In particular numpy for the computations [^54] [^55], pandas for the statistical analysis of the results [^56], and matplotlib and seaborn for the figures [^57] [^58].

## References

## Appendix A Determinant of 𝑻k\\boldsymbol{T}\_{k}

The proof uses the matrix determinant lemma, and the fact that $\boldsymbol{e}_{k}^{\top}\bar{\boldsymbol{E}}_{k}\boldsymbol{q}=0$ several times,

$$
\displaystyle\det(\boldsymbol{T}_{k})
$$
 
$$
\displaystyle=\det(\boldsymbol{I}+\boldsymbol{e}_{k}(\boldsymbol{u}-\boldsymbol{e}_{k})^{\mathsf{H}}+\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\boldsymbol{e}_{k}^{\top})
$$
 
$$
\displaystyle=\det\left(\boldsymbol{I}_{2}+\begin{bmatrix}\boldsymbol{u}^{\mathsf{H}}-\boldsymbol{e}_{k}^{\top}\\
\boldsymbol{e}_{k}^{\top}\end{bmatrix}\begin{bmatrix}\boldsymbol{e}_{k}&\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\end{bmatrix}\right)
$$
 
$$
\displaystyle=\det\left(\begin{bmatrix}u_{k}^{*}&\boldsymbol{u}^{\mathsf{H}}\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}\\
1&1\end{bmatrix}\right)=\boldsymbol{u}^{\mathsf{H}}(\boldsymbol{e}_{k}-\bar{\boldsymbol{E}}_{k}\boldsymbol{q}^{*}).
$$

## Appendix B Quadratic form

Let $a_{m}=\boldsymbol{e}_{k}\boldsymbol{V}_{m}\boldsymbol{e}_{k}$, $b_{m}=\boldsymbol{e}_{m}\boldsymbol{V}_{m}\boldsymbol{e}_{k}$, $c_{m}=\boldsymbol{e}_{m}^{\top}\boldsymbol{V}_{m}\boldsymbol{e}_{m}$, and $\boldsymbol{1}$ be the all one vector. Further let $\boldsymbol{A}=\operatorname{diag}(\ldots,\,a_{m},\,\ldots)$, $m\neq k$. Then,

$$
\displaystyle\sum_{m\neq k}
$$
 
$$
\displaystyle(\boldsymbol{e}_{m}+q_{m}\boldsymbol{e}_{k})^{\mathsf{H}}\boldsymbol{V}_{m}(\boldsymbol{e}_{m}+q_{m}\boldsymbol{e}_{k})
$$
 
$$
\displaystyle=\sum_{m\neq k}a_{m}|q_{m}|^{2}+(b_{m}^{*}q_{m}+b_{m}q_{m}^{*})+c_{m}
$$
 
$$
\displaystyle=\boldsymbol{q}^{\mathsf{H}}\boldsymbol{A}\boldsymbol{q}+(\boldsymbol{b}^{\mathsf{H}}\boldsymbol{q}+\boldsymbol{q}^{\mathsf{H}}\boldsymbol{b})+\boldsymbol{1}^{\top}\boldsymbol{c}
$$
 
$$
\displaystyle=(\boldsymbol{q}+\boldsymbol{A}^{-1}\boldsymbol{b})^{\mathsf{H}}\boldsymbol{A}(\boldsymbol{q}+\boldsymbol{A}^{-1}\boldsymbol{b})-\boldsymbol{b}^{\mathsf{H}}\boldsymbol{A}^{-1}\boldsymbol{b}+\boldsymbol{1}^{\top}\boldsymbol{c}.
$$

## Appendix C Proof of Proposition

We can lower bound the objective in (P2) as follows

$$
\boldsymbol{y}^{\mathsf{H}}\boldsymbol{y}-\log\left(\boldsymbol{y}^{\mathsf{H}}\boldsymbol{U}\boldsymbol{y}+2\operatorname{\mathsf{Re}}\left\{\boldsymbol{y}^{\mathsf{H}}\boldsymbol{U}\boldsymbol{v}\right\}+\boldsymbol{v}^{\mathsf{H}}\boldsymbol{U}\boldsymbol{v}+z\right)\\
\geq\|\boldsymbol{y}\|^{2}-\log(a\|\boldsymbol{y}\|^{2}+b\|\boldsymbol{y}\|+c),
$$

where $a=\lambda_{\max}(\boldsymbol{U})$ is the largest eigenvalue of $\boldsymbol{U}$, $b=2\|\boldsymbol{U}\boldsymbol{v}\|$, and $c=\boldsymbol{v}^{\mathsf{H}}\boldsymbol{U}\boldsymbol{v}+z$. We used the spectral norm of $\boldsymbol{U}$ to bound the quadratic term, and Cauchy-Schwarz for the linear term. Thus, we can equivalently study the real function $f(x)=x^{2}-\log(ax^{2}+bx+c)$, of $x\geq 0$, with $a>0$, $b,c\geq 0$. One can show that the stationary points of this function are the zeros of a third order polynomial. Thus, by the properties of cubic polynomials, $f(x)$ has either one or three stationary points. Furthermore $f(x)\to+\infty$, when $x\to+\infty$, since the quadratic term grows faster than the log decreases. Thus, with a single stationary point, $f(x)$ is strictly decreasing to a minimum, and then increasing. With three stationary points, it must be strictly decreasing, increasing, decreasing, and increasing, with two minima and one maximum. By continuity, in both cases, $f$ is bounded from below. $\square$

![[raw/papers/scheibler-2021-log-quadratically-penalized-iva/figures/fig1.png]]

Robin Scheibler

[^1]: P. Comon and C. Jutten, *Handbook of blind source separation: independent component analysis and applications*. Oxford, UK: Academic Press/Elsevier, 2010.

[^2]: S. Makino, Ed., *Audio Source Separation*, ser. Signals and Communication Technology. Cham, CH: Springer International Publishing, 2018.

[^3]: S. Makino, H. Sawada, and T.-W. Lee, Eds., *Blind Speech Separation*, ser. Signals and Communication Technology. Cham, CH: Springer, 2007.

[^4]: E. Cano, D. FitzGerald, A. Liutkus, M. D. Plumbley, and F.-R. Stöter, “Musical source separation: An introduction,” *IEEE Signal Process. Mag.*, vol. 36, no. 1, pp. 31–40, Jan. 2019.

[^5]: V. Zarzoso, A. K. Nandi, and E. Bacharakis, “Maternal and foetal ECG separation using blind source separation methods,” *IMA J Math Appl Med Biol*, vol. 14, no. 3, pp. 207–225, Sep. 1997.

[^6]: F. Cong, “Blind source separation,” in *EEG Signal Processing and Feature Extraction*, L. Hu and Z. Zhang, Eds. Singapore: Springer, 2019, ch. 7, pp. 117–140.

[^7]: H. Yang, H. Zhang, J. Li, L. Yang, and W. Ding, “Baseband communication signal blind separation algorithm based on complex nonparametric probability density estimation,” *IEEE Access*, vol. 6, pp. 22 434–22 440, Apr. 2018.

[^8]: P. Comon, “Independent component analysis, a new concept?” *Signal Processing*, vol. 36, no. 3, pp. 287–314, 1994.

[^9]: P. Smaragdis, “Blind separation of convolved mixtures in the frequency domain,” *Neurocomputing*, vol. 22, no. 1-3, pp. 21–34, Nov. 1998.

[^10]: A. Hiroe, “Solution of permutation problem in frequency domain ICA, using multivariate probability density functions,” in *Advances in Cryptology – ASIACRYPT 2016*. Berlin, Heidelberg: Springer Berlin Heidelberg, 2006, pp. 601–608.

[^11]: T. Kim, H. T. Attias, S.-Y. Lee, and T.-W. Lee, “Blind source separation exploiting higher-order frequency dependencies,” *IEEE Trans. Audio, Speech, Lang. Process.*, vol. 15, no. 1, pp. 70–79, Dec. 2006.

[^12]: I. Lee, T. Kim, and T.-W. Lee, “Independent vector analysis for convolutive blind speech separation,” in *Blind Speech Separation*. Dordrecht: Springer, Dordrecht, 2007, pp. 169–192.

[^13]: N. Ono, “Stable and fast update rules for independent vector analysis based on auxiliary function technique,” in *Proc. IEEE WASPAA*, New Paltz, NY, USA, Oct. 2011, pp. 189–192.

[^14]: K. Lange, *MM optimization algorithms*. SIAM, 2016.

[^15]: A. Yeredor, “On hybrid exact-approximate joint diagonalization,” in *Proc. IEEE CAMSAP*, Dec. 2009, pp. 312–315.

[^16]: A. Weiss, A. Yeredor, S. Cheema, and M. Haardt, “The extended “sequentially drilled” joint congruence transformation and its application in Gaussian independent vector analysis,” *IEEE Trans. Signal Process.*, vol. 65, no. 23, pp. 6332–6344, Dec. 2017.

[^17]: S. Degerine and A. Zaidi, “Separation of an instantaneous mixture of Gaussian autoregressive sources by the exact maximum likelihood approach,” *IEEE Trans. Signal Process.*, vol. 52, no. 6, pp. 1499–1512, Jun. 2004.

[^18]: K. Yatabe and D. Kitamura, “Determined blind source separation via proximal splitting algorithm,” in *Proc. IEEE ICASSP*, Calgary, CA, Apr. 2018, pp. 776–780.

[^19]: ——, “Determined bss based on time-frequency masking and its application to harmonic vector analysis,” *arXiv*, Apr. 2020.

[^20]: Z. Gu, J. Lu, and K. Chen, “Speech separation using independent vector analysis with an amplitude variable Gaussian mixture model,” in *Proc. Interspeech 2019*, Graz, AU, Sep. 2019, pp. 1358–1362.

[^21]: D. Kitamura, N. Ono, H. Sawada, H. Kameoka, and H. Saruwatari, “Determined blind source separation unifying independent vector analysis and nonnegative matrix factorization,” *IEEE/ACM Trans. Audio Speech Lang. Process.*, vol. 24, no. 9, pp. 1626–1641, Sep. 2016.

[^22]: H. Kameoka, L. Li, S. Inoue, and S. Makino, “Supervised determined source separation with multichannel variational autoencoder,” *Neural computation*, vol. 31, no. 9, pp. 1891–1914, Sep. 2019.

[^23]: N. Makishima, S. Mogami, N. Takamune, D. Kitamura, H. Sumino, S. Takamichi, H. Saruwatari, and N. Ono, “Independent deeply learned matrix analysis for determined audio source separation,” *IEEE/ACM Trans. Audio Speech Lang. Process.*, vol. 27, no. 10, pp. 1601–1615, 2019.

[^24]: U.-H. Shin and H.-M. Park, “Auxiliary-function-based independent vector analysis using generalized inter-clique dependence source models with clique variance estimation,” *IEEE Access*, vol. 8, pp. 68 103–68 113, Apr. 2020.

[^25]: R. Scheibler and N. Ono, “Independent vector analysis with more microphones than sources,” in *Proc. IEEE WASPAA*, New Paltz, NY, USA, Oct. 2019, pp. 185–189.

[^26]: N. Ono and S. Miyabe, “Auxiliary-function-based independent component analysis for super-Gaussian sources,” *Proc. LVA/ICA*, vol. 6365, no. 6, pp. 165–172, Sep. 2010.

[^27]: R. Scheibler and N. Ono, “Fast independent vector extraction by iterative SINR maximization,” in *Proc. IEEE ICASSP*, Barcelona, ES, May 2020, accepted.

[^28]: R. Ikeshita, T. Nakatani, and S. Araki, “Overdetermined independent vector analysis,” in *Proc. IEEE ICASSP*, Barcelona, ES, May 2020, accepted.

[^29]: N. Ono, “Fast algorithm for independent component/vector/low-rank matrix analysis with three or more sources,” in *Proc. Acoustical Society of Japan*, Mar. 2018, pp. 437–438.

[^30]: R. Scheibler and N. Ono, “MM algorithms for joint independent subspace analysis with application to blind single and multi-source extraction,” *arXiv*, Apr. 2020.

[^31]: ——, “Fast and stable blind source separation with rank-1 updates,” in *Proc. IEEE ICASSP*, Barcelona, ES, May 2020, pp. 236–240.

[^32]: G. H. Golub, “Some modified matrix eigenvalue problems,” *SIAM Review*, vol. 15, no. 2, pp. 318–334, Apr. 1973.

[^33]: J. R. Bunch, C. P. Nielsen, and D. C. Sorensen, “Rank-one modification of the symmetric eigenproblem,” *Numerische Mathematik*, vol. 31, no. 1, pp. 31–48, Mar. 1978.

[^34]: K.-B. Yu, “Recursive updating the eigenvalue decomposition of a covariance matrix,” *IEEE Trans. Signal Process.*, vol. 39, no. 5, pp. 1136–1145, May 1991.

[^35]: J. J. More, “Generalizations of the trust region problem,” *Optim. Method Softw.*, vol. 2, no. 3-4, pp. 189–209, Jan. 1993.

[^36]: R. G. Lorenz and S. P. Boyd, “Robust minimum variance beamforming,” *IEEE Trans. Signal Process.*, vol. 53, no. 5, pp. 1684–1696, 2005.

[^37]: A. Beck, P. Stoica, and J. Li, “Exact and approximate solutions of source localization problems,” *IEEE Trans. Signal Process.*, vol. 56, no. 5, pp. 1770–1778, Apr. 2008.

[^38]: M. Togami and R. Scheibler, “Sparseness-aware DOA estimation with majorization minimization,” in *Proc. Interspeech*, Oct. 2020, accepted.

[^39]: J. de Leeuw and W. J. Heiser, “Convergence of correction matrix algorithms for multidimensional,” in *Geometric Representations of Relational Data*, J. C. Lingoes, E. Roskam, and I. Borg, Eds. Ann Arbor, MI: Geometric representations of relational data, 1977, pp. 735–752.

[^40]: I. Daubechies, R. DeVore, M. Fornasier, and C. Sinan Güntürk, “Iteratively reweighted least squares minimization for sparse recovery,” *Communications on Pure and Applied Mathematics*, vol. 63, no. 1, pp. 1–38, Jan. 2010.

[^41]: K. Yamaoka, R. Scheibler, N. Ono, and Y. Wakabayashi, “Sub-sample time delay estimation via auxiliary-function-based iterative updates,” in *Proc. IEEE WASPAA*, New Paltz, NY, USA, Oct. 2019, pp. 130–134.

[^42]: D. R. Hunter and K. Lange, “A tutorial on MM algorithms,” *The American Statistician*, vol. 58, no. 1, pp. 30–37, Feb. 2004.

[^43]: Y. Sun, P. Babu, D. P. I. T. o. Signal, and 2016, “Majorization-minimization algorithms in signal processing, communications, and machine learning,” *IEEE Trans. Signal Process.*, vol. 65, no. 3, pp. 794–816, Feb. 2017.

[^44]: J. Le Roux, S. Wisdom, H. Erdogan, and J. R. Hershey, “SDR — half-baked or well done?” in *Proc. IEEE ICASSP*, Brighton, UK, May 2019, pp. 626–630.

[^45]: R. Scheibler, E. Bezzam, and I. Dokmanić, “Pyroomacoustics: A Python package for audio room simulations and array processing algorithms,” in *Proc. IEEE ICASSP*, Calgary, CA, Apr. 2018, pp. 351–355.

[^46]: H. Kuttruff, *Room acoustics*. CRC Press, 2009.

[^47]: J. Kominek and A. W. Black, “CMU ARCTIC databases for speech synthesis,” Language Technologies Institute, School of Computer Science, Carnegie Mellon University, Tech. Rep. CMU-LTI-03-177, 2003.

[^48]: R. Scheibler, “CMU ARCTIC concatenated 15s,” Zenodo. \[Online\]. Available: [http://doi.org/10.5281/zenodo.3066489](http://doi.org/10.5281/zenodo.3066489)

[^49]: D. Griffin and J. Lim, “Signal estimation from modified short-time Fourier transform,” *IEEE Trans. Acoust. Speech Signal Process.*, vol. 32, no. 2, pp. 236–243, 1984.

[^50]: K. Matsuoka and S. Nakashima, “Minimal distortion principle for blind source separation,” in *Proc. ICA*, San Diego, Dec. 2001, pp. 722–727.

[^51]: K. Matsuoka, “Minimal distortion principle for blind source separation,” in *Proc. SICE*, Aug. 2002, pp. 2138–2143.

[^52]: K. Sekiguchi, A. A. Nugraha, Y. Bando, and K. Yoshii, “Fast multichannel source separation based on jointly diagonalizable spatial covariance matrices,” *Proc. EUSIPCO*, Sep. 2019.

[^53]: T. M. Cover and J. A. Thomas, *Elements of Information Theory*. Wiley-Interscience, Jul. 2006.

[^54]: T. E. Oliphant, “Python for scientific computing,” *Computing in Science & Engineering*, vol. 9, no. 3, pp. 10–20, 2007.

[^55]: S. van der Walt, S. C. Colbert, and G. Varoquaux, “The NumPy array: A structure for efficient numerical computation,” *Computing in Science & Engineering*, vol. 13, no. 2, pp. 22–30, Feb. 2011.

[^56]: Wes McKinney, “Data structures for statistical computing in python,” in *Proc. 9th Python Sci. Conf.*, Stéfan van der Walt and Jarrod Millman, Eds., 2010, pp. 56 – 61.

[^57]: J. D. Hunter, “Matplotlib: A 2D graphics environment,” *Computing in Science & Engineering*, vol. 9, no. 3, pp. 90–95, 2007.

[^58]: M. Waskom, O. Botvinnik, J. Ostblom, M. Gelbart, S. Lukauskas, P. Hobson, D. C. Gemperline, T. Augspurger, Y. Halchenko, J. B. Cole, and et al., “mwaskom/seaborn: v0.10.1 (April 2020),” Apr 2020. \[Online\]. Available: [https://github.com/mwaskom/seaborn](https://github.com/mwaskom/seaborn)