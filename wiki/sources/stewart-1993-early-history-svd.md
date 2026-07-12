---
type: source
created: 2026-07-12
updated: 2026-07-12
sources:
  - raw/papers/stewart-1993-early-history-svd/full-text.md
  - https://doi.org/10.1137/1035134
  - zotero://select/items/0_WKC35DNZ
tags:
  - singular-value-decomposition
  - linear-algebra
  - matrix-decomposition
  - history-of-mathematics
  - bilinear-forms
  - integral-equations
  - approximation-theorem
  - perturbation-theory
---

# Stewart 1993: On the Early History of the Singular Value Decomposition

**Author**: [[entities/g-w-stewart|G. W. Stewart]] (University of Maryland, College Park)
**Venue**: SIAM Review, vol. 35, no. 4, pp. 551–566
**Published**: December 1993
**Type**: Survey / historical article
**DOI**: [10.1137/1035134](https://doi.org/10.1137/1035134)
**Zotero**: [select/items/0_WKC35DNZ](zotero://select/items/0_WKC35DNZ)
**Dedication**: For Gene Golub on his 15th birthday.

## Summary

This paper surveys the contributions of five mathematicians — [[entities/eugenio-beltrami|Eugenio Beltrami]] (1835–1899), [[entities/camille-jordan|Camille Jordan]] (1838–1921), [[entities/james-joseph-sylvester|James Joseph Sylvester]] (1814–1897), [[entities/erhard-schmidt|Erhard Schmidt]] (1876–1959), and [[entities/hermann-weyl|Hermann Weyl]] (1885–1955) — who established the existence of the [[concepts/singular-value-decomposition|singular value decomposition]] and developed its theory. Beltrami, Jordan, and Sylvester arrived at the decomposition through linear algebra (bilinear forms), while Schmidt and Weyl approached it from integral equations. Schmidt's contribution elevated the SVD from a mathematical curiosity to a computational tool via his best rank-$k$ approximation theorem; Weyl provided an elegant perturbation theory and an alternative proof of the approximation theorem.

## Historical Background

Most classical matrix decompositions **predated the widespread use of matrices** — they were cast in terms of determinants, linear systems, and bilinear/quadratic forms. Key precursors to the SVD include:

- **Gauss (1823)**: Elimination algorithm factoring the matrix of a quadratic form $\mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{x}$ into $\mathbf{R}\mathbf{D}^{-1}\mathbf{R}$ (diagonal $\mathbf{D}$, upper triangular $\mathbf{R}$) — effectively the LU decomposition.
- **Cauchy (1829)**: Eigenvalues and eigenvectors of symmetric systems, including the interlacing property.
- **Jacobi (1846)**: Diagonalization algorithm for symmetric matrices.
- **Weierstrass (1868)**: Canonical forms for pairs of bilinear functions (the generalized eigenvalue problem).

The SVD's advent in 1873 is thus one result in a long line of work on canonical forms.

Throughout the paper, the decomposition is written as

$$\mathbf{A} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^{\mathrm{T}},$$

where $\mathbf{A}$ is a real $n \times n$ matrix, $\boldsymbol{\Sigma} = \mathrm{diag}(\sigma_1, \ldots, \sigma_n)$ has nonnegative diagonal elements in descending order, and $\mathbf{U}, \mathbf{V}$ are orthogonal. The norm $\|\cdot\|$ is the Frobenius norm with $\|\mathbf{A}\|^2 = \sum_{i,j} a_{ij}^2 = \sum_i \sigma_i^2$.

## The Five Contributions

### 1. Beltrami (1873)

**Source**: *Sulle funzioni bilineari*, Giornale di Matematiche, 1873.

Beltrami is the first publisher of the SVD. His derivation, aimed at students, begins with a bilinear form $f(\mathbf{x}, \mathbf{y}) = \mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{y}$ and seeks orthogonal substitutions $\mathbf{x} = \mathbf{U}\boldsymbol{\xi}$, $\mathbf{y} = \mathbf{V}\boldsymbol{\eta}$ that diagonalize it:

$$\mathbf{S} = \mathbf{U}^{\mathrm{T}}\mathbf{A}\mathbf{V} = \boldsymbol{\Sigma}.$$

From the orthogonality of $\mathbf{U}$ and $\mathbf{V}$, Beltrami derives:

$$\mathbf{U}^{\mathrm{T}}(\mathbf{A}\mathbf{A}^{\mathrm{T}}) = \boldsymbol{\Sigma}^2 \mathbf{U}^{\mathrm{T}}, \qquad (\mathbf{A}^{\mathrm{T}}\mathbf{A})\mathbf{V} = \mathbf{V}\boldsymbol{\Sigma}^2.$$

Thus the singular values $\sigma_i$ are roots of $\det(\mathbf{A}\mathbf{A}^{\mathrm{T}} - \sigma^2 \mathbf{I}) = 0$.

**Algorithm**: (1) Find roots of the characteristic equation; (2) determine $\mathbf{U}$ from $\mathbf{U}^{\mathrm{T}}(\mathbf{A}\mathbf{A}^{\mathrm{T}}) = \boldsymbol{\Sigma}^2\mathbf{U}^{\mathrm{T}}$; (3) determine $\mathbf{V}$ from $\mathbf{U}^{\mathrm{T}}\mathbf{A} = \boldsymbol{\Sigma}\mathbf{V}^{\mathrm{T}}$.

**Limitations**: The derivation assumes $\mathbf{A}$ is nonsingular with **distinct** singular values. Beltrami's argument for positivity of $\sigma_i^2$ contains a circularity (using $\boldsymbol{\xi}$ whose existence he is trying to establish). Stewart notes "a certain slackness in the exposition suggests that he had not thought the problem through."

### 2. Jordan (1874)

**Source**: *Mémoire sur les formes bilinéaires*, J. Math. Pures Appl., 1874.

Jordan is the **codiscoverer** of the SVD; his treatment is more complete and elegant than Beltrami's. He approaches the problem variationally: maximize $P = \mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{y}$ subject to $\|\mathbf{x}\|^2 = \|\mathbf{y}\|^2 = 1$.

Using Lagrange multipliers, the optimality conditions yield:

$$\mathbf{A}\mathbf{y} = \sigma \mathbf{x}, \qquad \mathbf{x}^{\mathrm{T}}\mathbf{A} = \sigma \mathbf{y}^{\mathrm{T}},$$

and the singular value $\sigma$ is determined by the vanishing of

$$D = \left|\begin{array}{cc} -\sigma \mathbf{I} & \mathbf{A} \\ \mathbf{A}^{\mathrm{T}} & -\sigma \mathbf{I} \end{array}\right|.$$

**Key innovation — deflation**: Jordan uses a partial solution to reduce the problem to one of smaller size. Given a maximizing pair $(\mathbf{u}, \mathbf{v})$, he extends them to orthogonal matrices $\hat{\mathbf{U}} = (\mathbf{u} \; \mathbf{U}_*)$, $\hat{\mathbf{V}} = (\mathbf{v} \; \mathbf{V}_*)$ and shows the transformed matrix has the block-diagonal form

$$\hat{\mathbf{A}} = \left(\begin{array}{cc} \sigma & \mathbf{0} \\ \mathbf{0} & \mathbf{A}_1 \end{array}\right).$$

Applying this inductively yields the full SVD. The **deflation** technique avoids the degeneracy problems of Beltrami's approach. Stewart notes it "apparently lay fallow until Schur (1917) used it to establish his triangular form."

The block matrix $\left(\begin{array}{cc} \mathbf{0} & \mathbf{A} \\ \mathbf{A}^{\mathrm{T}} & \mathbf{0} \end{array}\right)$ is also widely used today, with its popularity due to Wielandt and Lanczos (1958, who apparently rediscovered the SVD independently).

### 3. Sylvester (1889)

**Sources**: A footnote in *Messenger of Mathematics* [57], a *Comptes Rendus* note [59], and a full paper [58].

Sylvester discovered the SVD independently, in ignorance of Beltrami and Jordan. He contributed two methods:

**The rule**: Given the bilinear form $B = \mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{y}$, form the quadratic $M = \sum_i (dB/dy_i)^2 = \mathbf{x}^{\mathrm{T}}\mathbf{A}\mathbf{A}^{\mathrm{T}}\mathbf{x}$. If $M = \sum \lambda_i \xi_i^2$ is the canonical form, then the canonical form of $B$ is $B = \sum \sigma_i \xi_i \eta_i$ with $\lambda_i = \sigma_i^2$. To find the substitution coefficients for a singular value $\sigma$, strike a row of $\mathbf{M} - \sigma^2\mathbf{I}$ and take the vector of order-$(n{-}1)$ minors, normalized. This only works for simple singular values.

**Infinitesimal iteration**: An inductive procedure using "infinitesimal orthogonal substitutions" — infinitesimal rotations that zero out off-diagonal elements while preserving previously introduced zeros. Stewart notes the style is "opaque" and Sylvester "pontificates without proving." This method anticipates modern continuous-transformation algorithms defined by differential equations, though Sylvester does not give enough detail to write down such equations.

Stewart observes that Sylvester was also working in ignorance of Jacobi's (1846) iterative diagonalization algorithm; the generalization to SVD is due to Kogbetliantz (1955).

### 4. Schmidt (1907)

**Source**: *Zur Theorie der linearen und nichtlinearen Integralgleichungen*, Math. Ann., 1907.

Schmidt, a student of Hilbert, **generalized the SVD to infinite-dimensional function spaces** (integral equations with unsymmetric kernels) and — crucially — proved the **approximation theorem** that transforms the SVD from a mathematical curiosity into a powerful tool.

**Symmetric kernels**: Schmidt first establishes the spectral theory for a continuous symmetric kernel $A(s,t)$ on $[a,b]\times[a,b]$: existence of eigenfunctions, reality of eigenvalues, completeness of the orthonormal eigenfunction system, and the unboundedness of the eigenvalue sequence.

**Unsymmetric kernels**: For an unsymmetric kernel, Schmidt defines adjoint eigenfunction pairs $(u_i(s), v_i(t))$ satisfying $u(s) = \lambda \int A(s,t)v(t)\,dt$ and $v(t) = \lambda \int A(s,t)u(s)\,ds$. He constructs them via the symmetric kernels $\bar{A}(s,t) = \int A(s,r)A(t,r)\,dr$ and $\underline{A}(s,t) = \int A(r,s)A(r,t)\,dr$, and shows the bilinear form admits the expansion

$$\int\!\!\int A(s,t)\,g(s)\,h(t)\,ds\,dt = \sum_i \frac{1}{\lambda_i} \int g(s)u_i(s)\,ds \int h(t)v_i(t)\,dt,$$

which he says "corresponds to the canonical decomposition of a bilinear form."

**The approximation theorem** ([[concepts/eckart-young-theorem|Eckart–Young theorem]]): Schmidt's crowning contribution is the proof that the best rank-$k$ approximation to $\mathbf{A}$ in the Frobenius norm is

$$\mathbf{A}_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^{\mathrm{T}},$$

with $\|\mathbf{A} - \mathbf{A}_k\|^2 = \|\mathbf{A}\|^2 - \sum_{i=1}^k \sigma_i^2 = \sum_{i=k+1}^n \sigma_i^2.$

The proof proceeds by showing that for arbitrary rank-$k$ approximations $\sum_{i=1}^k \mathbf{x}_i \mathbf{y}_i^{\mathrm{T}}$ (with $\mathbf{x}_i$ orthonormalized without loss of generality),

$$\sum_{i=1}^k \|\mathbf{A}\mathbf{x}_i\|^2 \leq \sum_{i=1}^k \sigma_i^2,$$

which is established via a clever partition of $\mathbf{V} = (\mathbf{V}_1 \; \mathbf{V}_2)$ and bounding each $\|\mathbf{A}\mathbf{x}_i\|^2$ using the structure of $\boldsymbol{\Sigma}$. Stewart calls this "the fundamental theorem of the singular value decomposition."

**Distinction**: Unlike his predecessors, Schmidt does not include null vectors of $\mathbf{A}$ in the decomposition — they are not part of his substitution. This difference manifests in the proof's third term, which would be zero in the usual finite-dimensional treatment.

### 5. Weyl (1912)

**Source**: *Das asymptotische Verteilungsgesetz der Eigenwerte linearer partieller Differentialgleichungen*, Math. Ann., 1912.

Weyl's contribution is a **general perturbation theory for singular values** and an elegant alternative proof of the approximation theorem. Although his paper treated symmetric kernels, he noted in a footnote that his proof extends to the unsymmetric case.

**Core lemma**: If $\mathbf{B}_k = \mathbf{X}\mathbf{Y}^{\mathrm{T}}$ with $\mathbf{X}, \mathbf{Y}$ having $k$ columns (i.e., $\mathrm{rank}(\mathbf{B}_k) \leq k$), then

$$\sigma_1(\mathbf{A} - \mathbf{B}_k) \geq \sigma_{k+1}(\mathbf{A}).$$

The proof constructs a vector $\mathbf{v}$ in the span of the first $k{+}1$ right singular vectors that is orthogonal to all columns of $\mathbf{Y}$, then uses $\sigma_1^2(\mathbf{A}-\mathbf{B}_k) \geq \mathbf{v}^{\mathrm{T}}(\mathbf{A}-\mathbf{B})^{\mathrm{T}}(\mathbf{A}-\mathbf{B})\mathbf{v} = \mathbf{v}^{\mathrm{T}}\mathbf{A}^{\mathrm{T}}\mathbf{A}\mathbf{v} \geq \sigma_{k+1}^2$.

**Weyl's inequality**: For $\mathbf{A} = \mathbf{A}' + \mathbf{A}''$ with singular values in descending order,

$$\sigma_{i+j-1} \leq \sigma_i' + \sigma_j''. \tag{6.3}$$

The proof first establishes the $i=j=1$ case via the variational characterization $\sigma_1 = \mathbf{u}_1^{\mathrm{T}}\mathbf{A}\mathbf{v}_1 \leq \sigma_1' + \sigma_1''$, then uses the core lemma with best rank-$(i{-}1)$ and rank-$(j{-}1)$ approximations of $\mathbf{A}'$ and $\mathbf{A}''$.

**Approximation theorem (corollary)**: Setting $\mathbf{A}' = \mathbf{A} - \mathbf{B}_k$ and $\mathbf{A}'' = \mathbf{B}_k$ with $\mathrm{rank}(\mathbf{B}_k) = k$ gives $\sigma_i(\mathbf{A} - \mathbf{B}_k) \geq \sigma_{k+i}$, hence

$$\|\mathbf{A} - \mathbf{B}_k\|^2 \geq \sigma_{k+1}^2 + \cdots + \sigma_n^2,$$

which is equivalent to Schmidt's result.

**Perturbation bound**: With $\mathbf{A} \gets \tilde{\mathbf{A}}$, $\mathbf{A}' \gets \mathbf{A}$, $\mathbf{A}'' \gets \mathbf{E}$ in Weyl's inequality,

$$|\tilde{\sigma}_i - \sigma_i| \leq \|\mathbf{E}\|_2, \qquad i = 1, \ldots, n,$$

where $\|\mathbf{E}\|_2 = \sigma_1(\mathbf{E})$ is the [[concepts/spectral-norm|spectral norm]]. This bounds the maximum change in any singular value by the spectral norm of the perturbation.

## Later Developments

The paper's final section (§7, "Envoi") sketches post-Weyl developments:

| Topic | Key contributors | Year |
|-------|------------------|------|
| Extension to complex matrices | Autonne | 1913 |
| Extension to rectangular matrices; rediscovery of approximation theorem | Eckart & Young | 1936, 1939 |
| Principal component analysis | Hotelling | 1933 |
| Canonical correlations | Hotelling | 1936 |
| Unitarily invariant norms ↔ symmetric gauge functions | von Neumann | 1937 |
| Moore–Penrose pseudoinverse | Moore, Penrose | 1920, 1955 |
| Generalization of Eckart–Young to any unitarily invariant norm | Mirsky | 1960 |
| Computational algorithm (Golub–Kahan) | Golub & Kahan | 1965 |
| Practical SVD algorithm (Golub–Reinsch) | Golub & Reinsch | 1970 |
| Accurate SVD of bidiagonal matrices | Demmel & Kahan | 1990 |
| Generalized SVD | Van Loan; Paige & Saunders | 1975; 1981 |
| CS decomposition | Davis & Kahan; Stewart | 1970; 1977 |

**Nomenclature**: The term "singular value" originates from the integral equations literature — Bateman (1908), Picard (1910), and Smithies (1937) used it in the modern sense. Usage was not stabilized even by mid-century: Weyl (1949) spoke of "two kinds of eigenvalues," and Gohberg & Krein (1965) called them "s-numbers."

## Key Contributions

1. **Beltrami (1873)**: First publication of the SVD. Derived via bilinear forms and orthogonal substitutions; gave an algorithm based on the characteristic equation of $\mathbf{A}\mathbf{A}^{\mathrm{T}}$. Limited to nonsingular matrices with distinct singular values.
2. **Jordan (1874)**: Codiscoverer. Variational derivation via maximizing a bilinear form; introduced the **deflation** technique to handle degeneracies; used the block matrix $\left(\begin{smallmatrix} \mathbf{0} & \mathbf{A} \\ \mathbf{A}^{\mathrm{T}} & \mathbf{0} \end{smallmatrix}\right)$.
3. **Sylvester (1889)**: Independent rediscovery. Two methods: a rule using minors of $\mathbf{A}\mathbf{A}^{\mathrm{T}} - \sigma^2\mathbf{I}$, and infinitesimal iteration (anticipating continuous-transformation algorithms).
4. **Schmidt (1907)**: Generalized SVD to function spaces (integral equations); proved the **best rank-$k$ approximation theorem** (often misattributed as the Eckart–Young theorem). Transformed SVD from a curiosity to a fundamental tool.
5. **Weyl (1912)**: General perturbation theory for singular values; **Weyl's inequality** $\sigma_{i+j-1} \leq \sigma_i' + \sigma_j''$; elegant proof of the approximation theorem as a corollary; established the spectral-norm perturbation bound $|\tilde{\sigma}_i - \sigma_i| \leq \|\mathbf{E}\|_2$.

## Related Concepts

- [[concepts/singular-value-decomposition|Singular Value Decomposition]] — the central subject of this historical survey
- [[concepts/eckart-young-theorem|Eckart–Young Theorem]] — Schmidt's best rank-$k$ approximation result, rediscovered by Eckart and Young
- [[concepts/spectral-norm|Spectral Norm]] — the unitarily invariant norm $\|\mathbf{A}\|_2 = \sigma_1(\mathbf{A})$ arising in Weyl's perturbation bound

## Related Synthesis

*(No synthesis pages currently reference this source.)*
