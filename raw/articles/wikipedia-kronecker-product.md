# Kronecker product

> Source: https://en.wikipedia.org/wiki/Kronecker_product
> Retrieved: 2026-09-18
> License: CC BY-SA 4.0 (Wikipedia contributors)

In **mathematics**, the **Kronecker product**, sometimes denoted by $\otimes$, is an operation on two matrices of arbitrary size resulting in a **block matrix**. It is a specialization of the tensor product (which is denoted by the same symbol) from vectors to matrices and gives the matrix of the tensor product linear map with respect to a standard choice of basis. The Kronecker product is to be distinguished from the usual matrix multiplication, which is an entirely different operation. The Kronecker product is also sometimes called **matrix direct product**.

The Kronecker product is named after the German mathematician Leopold Kronecker (1823–1891), even though there is little evidence that he was the first to define and use it. The Kronecker product has also been called the *Zehfuss matrix*, and the *Zehfuss product*, after Johann Georg Zehfuss, who in 1858 described this matrix operation, but *Kronecker product* is currently the most widely used term. The misattribution to Kronecker rather than Zehfuss was due to Kurt Hensel.

## Definition

If **A** is an $m \times n$ matrix and **B** is a $p \times q$ matrix, then the Kronecker product $\mathbf{A} \otimes \mathbf{B}$ is the $pm \times qn$ block matrix:

$$\mathbf{A}\otimes\mathbf{B} = \begin{bmatrix}
  a_{11} \mathbf{B} & \cdots & a_{1n}\mathbf{B} \\
             \vdots & \ddots &           \vdots \\
  a_{m1} \mathbf{B} & \cdots & a_{mn} \mathbf{B}
\end{bmatrix}$$

more explicitly:

$$\mathbf{A}\otimes\mathbf{B} = \begin{bmatrix}
   a_{11} b_{11} & a_{11} b_{12} & \cdots & a_{11} b_{1q} &
                   \cdots & \cdots & a_{1n} b_{11} & a_{1n} b_{12} & \cdots & a_{1n} b_{1q} \\
   a_{11} b_{21} & a_{11} b_{22} & \cdots & a_{11} b_{2q} &
                   \cdots & \cdots & a_{1n} b_{21} & a_{1n} b_{22} & \cdots & a_{1n} b_{2q} \\
   \vdots & \vdots & \ddots & \vdots & & & \vdots & \vdots & \ddots & \vdots \\
   a_{11} b_{p1} & a_{11} b_{p2} & \cdots & a_{11} b_{pq} &
                   \cdots & \cdots & a_{1n} b_{p1} & a_{1n} b_{p2} & \cdots & a_{1n} b_{pq} \\
   \vdots & \vdots & & \vdots & \ddots & & \vdots & \vdots & & \vdots \\
   \vdots & \vdots & & \vdots & & \ddots & \vdots & \vdots & & \vdots \\
   a_{m1} b_{11} & a_{m1} b_{12} & \cdots & a_{m1} b_{1q} &
                   \cdots & \cdots & a_{mn} b_{11} & a_{mn} b_{12} & \cdots & a_{mn} b_{1q} \\
   a_{m1} b_{21} & a_{m1} b_{22} & \cdots & a_{m1} b_{2q} &
                   \cdots & \cdots & a_{mn} b_{21} & a_{mn} b_{22} & \cdots & a_{mn} b_{2q} \\
   \vdots & \vdots & \ddots & \vdots & & & \vdots & \vdots & \ddots & \vdots \\
   a_{m1} b_{p1} & a_{m1} b_{p2} & \cdots & a_{m1} b_{pq} &
                   \cdots & \cdots & a_{mn} b_{p1} & a_{mn} b_{p2} & \cdots & a_{mn} b_{pq}
\end{bmatrix}$$

Using $/\!/$ and $\%$ to denote truncating integer division and remainder, respectively, and numbering the matrix elements starting from 0, one obtains

$$(A\otimes B)_{pr+v, qs+w} = a_{rs} b_{vw}$$
$$(A\otimes B)_{i, j} = a_{i /\!/ p, j /\!/ q} \, b_{i \% p, j \% q}$$

For the usual numbering starting from 1, one obtains

$$(A\otimes B)_{p(r-1)+v, q(s-1)+w} = a_{rs} b_{vw}$$
$$(A\otimes B)_{i, j} = a_{\lceil i/p \rceil,\lceil j/q \rceil} \, b_{((i-1)\%p) +1, ((j-1)\%q) + 1}$$

If **A** and **B** represent linear transformations $\mathbf{V}_1 \to \mathbf{W}_1$ and $\mathbf{V}_2 \to \mathbf{W}_2$, respectively, then the tensor product of the two maps is a map $\mathbf{V}_1 \otimes \mathbf{V}_2 \to \mathbf{W}_1 \otimes \mathbf{W}_2$ represented by $\mathbf{A} \otimes \mathbf{B}$.

### Examples

$$\begin{bmatrix}
    1 & 2 \\
    3 & 4 \\
  \end{bmatrix} \otimes
  \begin{bmatrix}
    0 & 5 \\
    6 & 7 \\
  \end{bmatrix} =
  \begin{bmatrix}
    1 \begin{bmatrix} 0 & 5 \\ 6 & 7 \end{bmatrix} &
    2 \begin{bmatrix} 0 & 5 \\ 6 & 7 \end{bmatrix} \\
    3 \begin{bmatrix} 0 & 5 \\ 6 & 7 \end{bmatrix} &
    4 \begin{bmatrix} 0 & 5 \\ 6 & 7 \end{bmatrix}
  \end{bmatrix} =
  \left[\begin{array}{cc|cc}
     0 &  5 &  0 & 10 \\
     6 &  7 & 12 & 14 \\ \hline
     0 & 15 &  0 & 20 \\
    18 & 21 & 24 & 28
  \end{array}\right]$$

Similarly:

$$\begin{bmatrix}
1 & -4 & 7 \\
-2 & 3 & 3
\end{bmatrix} \otimes
\begin{bmatrix}
8 & -9 & -6 & 5 \\
1 & -3 & -4 & 7 \\
2 & 8 & -8 & -3 \\
1 & 2 & -5 & -1
\end{bmatrix} =
\left[\begin{array}{cccc|cccc|cccc}
8 & -9 & -6 & 5 & -32 & 36 & 24 & -20 & 56 & -63 & -42 & 35 \\
1 & -3 & -4 & 7 & -4 & 12 & 16 & -28 & 7 & -21 & -28 & 49 \\
2 & 8 & -8 & -3 & -8 & -32 & 32 & 12 & 14 & 56 & -56 & -21 \\
1 & 2 & -5 & -1 & -4 & -8 & 20 & 4 & 7 & 14 & -35 & -7 \\ \hline
-16 & 18 & 12 & -10 & 24 & -27 & -18 & 15 & 24 & -27 & -18 & 15 \\
-2 & 6 & 8 & -14 & 3 & -9 & -12 & 21 & 3 & -9 & -12 & 21 \\
-4 & -16 & 16 & 6 & 6 & 24 & -24 & -9 & 6 & 24 & -24 & -9 \\
-2 & -4 & 10 & 2 & 3 & 6 & -15 & -3 & 3 & 6 & -15 & -3
\end{array}\right]$$

## Properties

### Relations to other matrix operations

**1. Bilinearity and associativity.** The Kronecker product is a special case of the tensor product, so it is bilinear and associative:

$$\begin{aligned}
        \mathbf{A} \otimes (\mathbf{B} + \mathbf{C}) &= \mathbf{A} \otimes \mathbf{B} + \mathbf{A} \otimes \mathbf{C}, \\
        (\mathbf{B} + \mathbf{C}) \otimes \mathbf{A} &= \mathbf{B} \otimes \mathbf{A} + \mathbf{C} \otimes \mathbf{A}, \\
                    (k\mathbf{A}) \otimes \mathbf{B} &= \mathbf{A} \otimes (k\mathbf{B}) = k(\mathbf{A} \otimes \mathbf{B}), \\
  (\mathbf{A} \otimes \mathbf{B}) \otimes \mathbf{C} &= \mathbf{A} \otimes (\mathbf{B} \otimes \mathbf{C}), \\
  \mathbf{A} \otimes \mathbf{0} &= \mathbf{0} \otimes \mathbf{A} = \mathbf{0},
\end{aligned}$$

where **A**, **B** and **C** are matrices, **0** is a zero matrix, and $k$ is a scalar.

**2. Non-commutative.** In general, $\mathbf{A} \otimes \mathbf{B}$ and $\mathbf{B} \otimes \mathbf{A}$ are different matrices. However, $\mathbf{A} \otimes \mathbf{B}$ and $\mathbf{B} \otimes \mathbf{A}$ are permutation equivalent, meaning that there exist permutation matrices **P** and **Q** such that

$$\mathbf{B} \otimes \mathbf{A} = \mathbf{P} \, \left(\mathbf{A} \otimes \mathbf{B}\right) \, \mathbf{Q}.$$

If **A** and **B** are square, then $\mathbf{A} \otimes \mathbf{B}$ and $\mathbf{B} \otimes \mathbf{A}$ are even permutation similar, meaning that we can take $\mathbf{P} = \mathbf{Q}^\textsf{T}$.

The matrices **P** and **Q** are perfect shuffle matrices, called the "commutation" matrix. The commutation matrix $\mathbf{S}_{p,q}$ can be constructed by taking slices of the $\mathbf{I}_r$ identity matrix, where $r = pq$:

$$\mathbf{S}_{p,q} = \begin{bmatrix}
  \mathbf{I}_r(1:q:r,:) \\
  \mathbf{I}_r(2:q:r,:) \\
  \vdots \\
  \mathbf{I}_r(q:q:r,:)
\end{bmatrix}$$

MATLAB colon notation is used here to indicate submatrices, and $\mathbf{I}_r$ is the $r \times r$ identity matrix. If $\mathbf{A} \in \mathbb{R}^{m_1 \times n_1}$ and $\mathbf{B} \in \mathbb{R}^{m_2 \times n_2}$, then

$$\mathbf{B} \otimes \mathbf{A} = \mathbf{S}_{m_1,m_2} (\mathbf{A} \otimes \mathbf{B}) \mathbf{S}^\textsf{T}_{n_1,n_2}$$

**3. The mixed-product property.** If **A**, **B**, **C** and **D** are matrices of such size that one can form the matrix products **AC** and **BD**, then

$$(\mathbf{A} \otimes \mathbf{B})(\mathbf{C} \otimes \mathbf{D}) = (\mathbf{AC}) \otimes (\mathbf{BD}).$$

This is called the *mixed-product property*, because it mixes the ordinary matrix product and the Kronecker product.

As an immediate consequence (again, taking $\mathbf{A} \in \mathbb{R}^{m_1 \times n_1}$ and $\mathbf{B} \in \mathbb{R}^{m_2 \times n_2}$),

$$\mathbf{A} \otimes \mathbf{B} = (\mathbf{I}_{m_1} \otimes \mathbf{B} )(\mathbf{A} \otimes \mathbf{I}_{n_2}) = (\mathbf{A} \otimes \mathbf{I}_{m_2} )(\mathbf{I}_{n_1} \otimes \mathbf{B}).$$

In particular, using the *transpose* property from below, this means that if $\mathbf{A} = \mathbf{Q} \otimes \mathbf{U}$ and **Q** and **U** are orthogonal (or unitary), then **A** is also orthogonal (resp., unitary).

The mixed Kronecker matrix-vector product can be written as:

$$\left( \mathbf{A} \otimes \mathbf{B} \right) \operatorname{vec} \left( \mathbf{V} \right) = \operatorname{vec} (\mathbf{B} \mathbf{V} \mathbf{A}^T)$$

where $\operatorname{vec}(\mathbf{V})$ is the vectorization operator applied on $\mathbf{V}$ (formed by reshaping the matrix).

**4. Commutator property.** If $\mathbf{A}$ and $\mathbf{C}$ are square matrices of the dimension $m$, and $\mathbf{B}$ and $\mathbf{D}$ are square matrices of the dimension $n$, then the commutator

$$[\mathbf{A} \otimes \mathbf{B},\mathbf{C} \otimes \mathbf{D}]=[\mathbf{A},\mathbf{C}]\otimes (\mathbf{B}\mathbf{D}) +  (\mathbf{C}\mathbf{A}) \otimes [\mathbf{B},\mathbf{D}],$$

or

$$[\mathbf{A} \otimes \mathbf{B},\mathbf{C} \otimes \mathbf{D}]=[\mathbf{A},\mathbf{C}]\otimes (\mathbf{D}\mathbf{B}) +  (\mathbf{A}\mathbf{C}) \otimes [\mathbf{B},\mathbf{D}].$$

**5. Hadamard product (element-wise multiplication).** The mixed-product property also works for the element-wise product. If **A** and **C** are matrices of the same size, **B** and **D** are matrices of the same size, then

$$(\mathbf{A} \otimes \mathbf{B}) \circ (\mathbf{C} \otimes \mathbf{D}) = (\mathbf{A} \circ \mathbf{C}) \otimes (\mathbf{B} \circ \mathbf{D}).$$

**6. The inverse of a Kronecker product.** It follows that $\mathbf{A} \otimes \mathbf{B}$ is invertible if and only if both **A** and **B** are invertible, in which case the inverse is given by

$$(\mathbf{A} \otimes \mathbf{B})^{-1} = \mathbf{A}^{-1} \otimes \mathbf{B}^{-1}.$$

The invertible product property holds for the Moore–Penrose pseudoinverse as well, that is

$$(\mathbf{A} \otimes \mathbf{B})^{+} = \mathbf{A}^{+} \otimes \mathbf{B}^{+}.$$

In the language of category theory, the mixed-product property of the Kronecker product (and more general tensor product) shows that the category **Mat**$_F$ of matrices over a field $F$ is in fact a monoidal category, with objects natural numbers $n$, morphisms $n \to m$ are $n \times m$ matrices with entries in $F$, composition is given by matrix multiplication, identity arrows are simply $n \times n$ identity matrices $I_n$, and the tensor product is given by the Kronecker product.

**Mat**$_F$ is a concrete skeleton category for the equivalent category **FinVect**$_F$ of finite dimensional vector spaces over $F$, whose objects are such finite dimensional vector spaces $V$, arrows are $F$-linear maps $L : V \to W$, and identity arrows are the identity maps of the spaces. The equivalence of categories amounts to simultaneously choosing a basis in every finite-dimensional vector space $V$ over $F$; matrices' elements represent these mappings with respect to the chosen bases; and likewise the Kronecker product is the representation of the tensor product in the chosen bases.

**7. Transpose.** Transposition and conjugate transposition are distributive over the Kronecker product:

$$(\mathbf{A}\otimes \mathbf{B})^\textsf{T} = \mathbf{A}^\textsf{T} \otimes \mathbf{B}^\textsf{T} \quad\text{and}\quad (\mathbf{A}\otimes \mathbf{B})^* = \mathbf{A}^* \otimes \mathbf{B}^*.$$

**8. Determinant.** Let **A** be an $n \times n$ matrix and let **B** be an $m \times m$ matrix. Then

$$\left| \mathbf{A} \otimes \mathbf{B} \right| = \left| \mathbf{A} \right| ^m \left| \mathbf{B} \right| ^n .$$

The exponent in $|\mathbf{A}|$ is the order of **B** and the exponent in $|\mathbf{B}|$ is the order of **A**.

**9. Kronecker sum and exponentiation.** If **A** is $n \times n$, **B** is $m \times m$, and $\mathbf{I}_k$ denotes the $k \times k$ identity matrix then we can define what is sometimes called the **Kronecker sum**, $\overline{\oplus}$, by

$$\mathbf{A}\,\overline{\oplus}\,\mathbf{B} = \mathbf{A} \otimes \mathbf{I}_m + \mathbf{I}_n \otimes \mathbf{B} .$$

This is *different* from the direct sum of two matrices. This operation is related to the tensor product on Lie algebras, as detailed in "Relation to the abstract tensor product" below.

We have the following formula for the matrix exponential, which is useful in some numerical evaluations:

$$\exp({\mathbf{N}\,\overline{\oplus}\,\mathbf{M}}) = \exp(\mathbf{N}) \otimes \exp(\mathbf{M})$$

Kronecker sums appear naturally in physics when considering ensembles of non-interacting systems. If $H^r$ is the Hamiltonian of the $r$th such system, then the total Hamiltonian of the ensemble is

$$H_{\operatorname{Tot}}=\overline{\bigoplus_r} H^r .$$

**10. Vectorization of a Kronecker product.** Let $A$ be an $m\times n$ matrix and $B$ a $p \times q$ matrix. When the order of the Kronecker product and vectorization is interchanged, the two operations can be linked linearly through a function that involves the commutation matrix, $K_{qm}$. That is, $\operatorname{vec}(\operatorname{Kron}(A, B))$ and $\operatorname{Kron}(\operatorname{vec}A,\operatorname{vec}B)$ have the following relationship:

$$\operatorname{vec}(A\otimes B) = (I_n \otimes K_{qm}\otimes I_p)(\operatorname{vec}A \otimes \operatorname{vec}B).$$

Furthermore, the above relation can be rearranged in terms of either $\operatorname{vec}A$ or $\operatorname{vec}B$ as follows:

$$\operatorname{vec}(A\otimes B)= (I_n \otimes G)\operatorname{vec}A = (H\otimes I_p)\operatorname{vec}B,$$

where

$$G = (K_{qm}\otimes I_p)(I_m \otimes \operatorname{vec}B) \quad \text{and} \quad H=(I_n\otimes K_{qm})(\operatorname{vec}A \otimes I_q).$$

**11. Outer product.** If $x \in \mathbb{R}^n$ and $y \in \mathbb{R}^m$ are arbitrary vectors, then the outer product between $x$ and $y$ is defined as $xy^T$. The Kronecker product is related to the outer product by: $y\otimes x = \operatorname{vec}(xy^T)$.

### Abstract properties

**1. Spectrum.** Suppose that **A** and **B** are square matrices of size $n$ and $m$ respectively. Let $\lambda_1, \ldots, \lambda_n$ be the eigenvalues of **A** and $\mu_1, \ldots, \mu_m$ be those of **B** (listed according to multiplicity). Then the eigenvalues of $\mathbf{A} \otimes \mathbf{B}$ are

$$\lambda_i \mu_j, \qquad i=1,\ldots,n ,\, j=1,\ldots,m.$$

It follows that the trace and determinant of a Kronecker product are given by

$$\operatorname{tr}(\mathbf{A} \otimes \mathbf{B}) = \operatorname{tr} \mathbf{A} \, \operatorname{tr} \mathbf{B} \quad\text{and}\quad \det(\mathbf{A} \otimes \mathbf{B}) = (\det \mathbf{A})^m (\det \mathbf{B})^n.$$

**2. Singular values.** If **A** and **B** are rectangular matrices, then one can consider their singular values. Suppose that **A** has $r_\mathbf{A}$ nonzero singular values, namely $\sigma_{\mathbf{A},i}$ for $i = 1, \ldots, r_\mathbf{A}$. Similarly, denote the nonzero singular values of **B** by $\sigma_{\mathbf{B},i}$ for $i = 1, \ldots, r_\mathbf{B}$. Then the Kronecker product $\mathbf{A} \otimes \mathbf{B}$ has $r_\mathbf{A} r_\mathbf{B}$ nonzero singular values, namely

$$\sigma_{\mathbf{A},i} \sigma_{\mathbf{B},j}, \qquad i=1,\ldots,r_\mathbf{A} ,\, j=1,\ldots,r_\mathbf{B}.$$

Since the rank of a matrix equals the number of nonzero singular values, we find that

$$\operatorname{rank}(\mathbf{A} \otimes \mathbf{B}) = \operatorname{rank} \mathbf{A} \, \operatorname{rank} \mathbf{B}.$$

**3. Relation to the abstract tensor product.** The Kronecker product of matrices corresponds to the abstract tensor product of linear maps. Specifically, if the vector spaces $V$, $W$, $X$, and $Y$ have bases $\{v_1, \ldots, v_m\}$, $\{w_1, \ldots, w_n\}$, $\{x_1, \ldots, x_d\}$, and $\{y_1, \ldots, y_e\}$, respectively, and if the matrices $A$ and $B$ represent the linear transformations $S : V \to X$ and $T : W \to Y$, respectively in the appropriate bases, then the matrix $A \otimes B$ represents the tensor product of the two maps, $S \otimes T : V \otimes W \to X \otimes Y$, with respect to the basis $\{v_1 \otimes w_1, v_1 \otimes w_2, \ldots, v_2 \otimes w_1, \ldots, v_m \otimes w_n\}$ of $V \otimes W$ (and the similarly defined basis of $X \otimes Y$) with the property that $A \otimes B(v_i \otimes w_j) = (Av_i) \otimes (Bw_j)$, where $i$ and $j$ are integers in the proper range.

When $V$ and $W$ are Lie algebras, and $S : V \to V$ and $T : W \to W$ are Lie algebra homomorphisms, the Kronecker sum of $A$ and $B$ represents the induced Lie algebra homomorphisms $V \otimes W \to V \otimes W$.

**4. Relation to products of graphs.** The Kronecker product of the adjacency matrices of two graphs is the adjacency matrix of the tensor product graph. The Kronecker sum of the adjacency matrices of two graphs is the adjacency matrix of the Cartesian product graph.

## Matrix equations

The Kronecker product can be used to get a convenient representation for some matrix equations. Consider for instance the equation $\mathbf{AXB} = \mathbf{C}$, where **A**, **B** and **C** are given matrices and the matrix **X** is the unknown. We can use the "vec trick" to rewrite this equation as

$$\left(\mathbf{B}^\textsf{T} \otimes \mathbf{A}\right) \, \operatorname{vec}(\mathbf{X}) = \operatorname{vec}(\mathbf{AXB}) = \operatorname{vec}(\mathbf{C}).$$

Here, $\operatorname{vec}(\mathbf{X})$ denotes the vectorization of the matrix **X**, formed by stacking the columns of **X** into a single column vector.

It now follows from the properties of the Kronecker product that the equation $\mathbf{AXB} = \mathbf{C}$ has a unique solution, if and only if **A** and **B** are invertible (Horn & Johnson 1991, Lemma 4.3.1).

If **X** and **C** are row-ordered into the column vectors **u** and **v**, respectively, then (Jain 1989, 2.8 Block Matrices and Kronecker Products)

$$\mathbf{v} = \left(\mathbf{A} \otimes \mathbf{B}^\textsf{T}\right)\mathbf{u}.$$

The reason is that

$$\mathbf{v} = \operatorname{vec}\left((\mathbf{AXB})^\textsf{T}\right) = \operatorname{vec}\left(\mathbf{B}^\textsf{T}\mathbf{X}^\textsf{T}\mathbf{A}^\textsf{T}\right) = \left(\mathbf{A} \otimes \mathbf{B}^\textsf{T}\right)\operatorname{vec}\left(\mathbf{X}^\textsf{T}\right) = \left(\mathbf{A} \otimes \mathbf{B}^\textsf{T}\right)\mathbf{u}.$$

### Applications

For an example of the application of this formula, see the article on the Lyapunov equation. This formula also comes in handy in showing that the matrix normal distribution is a special case of the multivariate normal distribution. This formula is also useful for representing 2D image processing operations in matrix-vector form.

Another example is when a matrix can be factored as a Kronecker product, then matrix multiplication can be performed faster by using the above formula. This can be applied recursively, as done in the radix-2 FFT and the Fast Walsh–Hadamard transform. Splitting a known matrix into the Kronecker product of two smaller matrices is known as the "nearest Kronecker product" problem, and can be solved exactly by using the SVD (Van Loan & Pitsianis 1992). To split a matrix into the Kronecker product of more than two matrices, in an optimal fashion, is a difficult problem and the subject of ongoing research; some authors cast it as a tensor decomposition problem.

In conjunction with the least squares method, the Kronecker product can be used as an accurate solution to the hand–eye calibration problem.

## Related matrix operations

Two related matrix operations are the **Tracy–Singh** and **Khatri–Rao products**, which operate on partitioned matrices. Let the $m \times n$ matrix **A** be partitioned into the $m_i \times n_j$ blocks $\mathbf{A}_{ij}$ and $p \times q$ matrix **B** into the $p_k \times q_\ell$ blocks $\mathbf{B}_{kl}$, with of course $\sum_i m_i = m$, $\sum_j n_j = n$, $\sum_k p_k = p$ and $\sum_\ell q_\ell = q$.

### Tracy–Singh product

The **Tracy–Singh product** is defined as

$$\mathbf{A} \circ \mathbf{B} = \left(\mathbf{A}_{ij} \circ \mathbf{B}\right)_{ij} = \left(\left(\mathbf{A}_{ij} \otimes \mathbf{B}_{kl}\right)_{kl}\right)_{ij}$$

which means that the $(ij)$-th subblock of the $mp \times nq$ product $\mathbf{A} \circ \mathbf{B}$ is the $m_i p \times n_j q$ matrix $\mathbf{A}_{ij} \circ \mathbf{B}$, of which the $(k\ell)$-th subblock equals the $m_i p_k \times n_j q_\ell$ matrix $\mathbf{A}_{ij} \otimes \mathbf{B}_{k\ell}$. Essentially the Tracy–Singh product is the pairwise Kronecker product for each pair of partitions in the two matrices.

For example, if **A** and **B** both are $2 \times 2$ partitioned matrices e.g.:

$$\mathbf{A} = \left[\begin{array}{c | c} \mathbf{A}_{11} & \mathbf{A}_{12} \\ \hline \mathbf{A}_{21} & \mathbf{A}_{22} \end{array}\right] = \left[\begin{array}{c c | c} 1 & 2 & 3 \\ 4 & 5 & 6 \\ \hline 7 & 8 & 9 \end{array}\right], \quad \mathbf{B} = \left[\begin{array}{c | c} \mathbf{B}_{11} & \mathbf{B}_{12} \\ \hline \mathbf{B}_{21} & \mathbf{B}_{22} \end{array}\right] = \left[\begin{array}{c | c c} 1 & 4 & 7 \\ \hline 2 & 5 & 8 \\ 3 & 6 & 9 \end{array}\right],$$

we get:

$$\mathbf{A} \circ \mathbf{B} = \left[\begin{array}{c | c} \mathbf{A}_{11} \circ \mathbf{B} & \mathbf{A}_{12} \circ \mathbf{B} \\ \hline \mathbf{A}_{21} \circ \mathbf{B} & \mathbf{A}_{22} \circ \mathbf{B} \end{array}\right] = \left[\begin{array}{c | c | c | c}
 \mathbf{A}_{11} \otimes \mathbf{B}_{11} & \mathbf{A}_{11} \otimes \mathbf{B}_{12} & \mathbf{A}_{12} \otimes \mathbf{B}_{11} & \mathbf{A}_{12} \otimes \mathbf{B}_{12} \\
 \hline
 \mathbf{A}_{11} \otimes \mathbf{B}_{21} & \mathbf{A}_{11} \otimes \mathbf{B}_{22} & \mathbf{A}_{12} \otimes \mathbf{B}_{21} & \mathbf{A}_{12} \otimes \mathbf{B}_{22} \\
 \hline
 \mathbf{A}_{21} \otimes \mathbf{B}_{11} & \mathbf{A}_{21} \otimes \mathbf{B}_{12} & \mathbf{A}_{22} \otimes \mathbf{B}_{11} & \mathbf{A}_{22} \otimes \mathbf{B}_{12} \\
 \hline
 \mathbf{A}_{21} \otimes \mathbf{B}_{21} & \mathbf{A}_{21} \otimes \mathbf{B}_{22} & \mathbf{A}_{22} \otimes \mathbf{B}_{21} & \mathbf{A}_{22} \otimes \mathbf{B}_{22}
\end{array}\right] = \left[\begin{array}{c c | c c c c | c | c c}
 1 &  2 &  4 &  7 &  8 & 14 &  3 & 12 & 21 \\
 4 &  5 & 16 & 28 & 20 & 35 &  6 & 24 & 42 \\
 \hline
 2 &  4 &  5 &  8 & 10 & 16 &  6 & 15 & 24 \\
 3 &  6 &  6 &  9 & 12 & 18 &  9 & 18 & 27 \\
 8 & 10 & 20 & 32 & 25 & 40 & 12 & 30 & 48 \\
 12 & 15 & 24 & 36 & 30 & 45 & 18 & 36 & 54 \\
 \hline
 7 &  8 & 28 & 49 & 32 & 56 &  9 & 36 & 63 \\
 \hline
 14 & 16 & 35 & 56 & 40 & 64 & 18 & 45 & 72 \\
 21 & 24 & 42 & 63 & 48 & 72 & 27 & 54 & 81
\end{array}\right].$$

### Khatri–Rao product

- Block Kronecker product
- Column-wise Khatri–Rao product

### Face-splitting product

Mixed-products properties (Slyusar 1998):

$$\mathbf{A} \otimes (\mathbf{B}\bull \mathbf{C}) = (\mathbf{A}\otimes \mathbf{B}) \bull \mathbf{C} ,$$

where $\bull$ denotes the Face-splitting product.

$$(\mathbf{A} \bull \mathbf{B})(\mathbf{C} \otimes \mathbf{D}) = (\mathbf{A}\mathbf{C}) \bull (\mathbf{B} \mathbf{D}) ,$$

Similarly:

$$(\mathbf{A} \bull \mathbf{L})(\mathbf{B} \otimes \mathbf{M}) \cdots (\mathbf{C} \otimes \mathbf{S}) = (\mathbf{A}\mathbf{B} \cdots \mathbf{C}) \bull (\mathbf{L}\mathbf{M} \cdots \mathbf{S}) ,$$

$$\mathbf{c}^\textsf{T} \bull \mathbf{d}^\textsf{T} = \mathbf{c}^\textsf{T} \otimes \mathbf{d}^\textsf{T} ,$$

where $\mathbf{c}$ and $\mathbf{d}$ are vectors,

$$(\mathbf{A} \bull \mathbf{B})(\mathbf{c} \otimes \mathbf{d}) = (\mathbf{A}\mathbf{c}) \circ (\mathbf{B}\mathbf{d}) ,$$

where $\mathbf{c}$ and $\mathbf{d}$ are vectors, and $\circ$ denotes the Hadamard product.

Similarly:

$$(\mathbf{A} \bull \mathbf{B})(\mathbf{M}\mathbf{N}\mathbf{c} \otimes \mathbf{Q}\mathbf{P}\mathbf{d}) = (\mathbf{A}\mathbf{M}\mathbf{N}\mathbf{c}) \circ (\mathbf{B}\mathbf{Q}\mathbf{P}\mathbf{d}),$$

$$\mathcal{F}(C^{(1)}x \star C^{(2)}y) = (\mathcal{F} C^{(1)} \bull \mathcal{F} C^{(2)})(x \otimes y)= \mathcal{F} C^{(1)}x \circ \mathcal{F} C^{(2)}y,$$

where $\star$ is vector convolution and $\mathcal{F}$ is the Fourier transform matrix (this result is an evolving of count sketch properties),

$$(\mathbf{A} \bull \mathbf{L})(\mathbf{B} \otimes \mathbf{M}) \cdots (\mathbf{C} \otimes \mathbf{S})(\mathbf{K} \ast \mathbf{T}) = (\mathbf{A}\mathbf{B} \cdots \mathbf{C}\mathbf{K}) \circ (\mathbf{L}\mathbf{M} \cdots \mathbf{S}\mathbf{T}) ,$$

where $\ast$ denotes the column-wise Khatri–Rao product.

Similarly:

$$(\mathbf{A} \bull \mathbf{L})(\mathbf{B} \otimes \mathbf{M}) \cdots (\mathbf{C} \otimes \mathbf{S})(c \otimes d ) = (\mathbf{A}\mathbf{B} \cdots \mathbf{C}\mathbf{c}) \circ (\mathbf{L}\mathbf{M} \cdots \mathbf{S}\mathbf{d}) ,$$

$$(\mathbf{A} \bull \mathbf{L})(\mathbf{B} \otimes \mathbf{M}) \cdots (\mathbf{C} \otimes \mathbf{S})(\mathbf{P}\mathbf{c} \otimes \mathbf{Q}\mathbf{d} ) = (\mathbf{A}\mathbf{B} \cdots \mathbf{C}\mathbf{P}\mathbf{c}) \circ (\mathbf{L}\mathbf{M} \cdots \mathbf{S}\mathbf{Q}\mathbf{d}) ,$$

where $\mathbf{c}$ and $\mathbf{d}$ are vectors.

## See also

- Generalized linear array model
- Hadamard product (matrices)
- Kronecker coefficient

## References

- Horn, Roger A.; Johnson, Charles R. (1991). *Topics in Matrix Analysis*. Cambridge University Press. ISBN 978-0-521-46713-1.
- Jain, Anil K. (1989). *Fundamentals of Digital Image Processing*. Prentice Hall. ISBN 978-0-13-336165-0.
- Steeb, Willi-Hans (1997). *Matrix Calculus and Kronecker Product with Applications and C++ Programs*. World Scientific Publishing. ISBN 978-981-02-3241-2.
- Steeb, Willi-Hans (2006). *Problems and Solutions in Introductory and Advanced Matrix Calculus*. World Scientific Publishing. ISBN 978-981-256-916-5.
- Liu, Shuangzhe; Trenkler, Götz (2008). "Hadamard, Khatri-Rao, Kronecker and other matrix products". *International Journal of Information and Systems Sciences*. 4: 160–177.
- Van Loan, Charles F. (2000). "The ubiquitous Kronecker product". *Journal of Computational and Applied Mathematics*. 123 (1–2): 85–100.
- Zehfuss, G. (1858). "Ueber eine gewisse Determinante". *Zeitschrift für Mathematik und Physik*. 3: 298–301.
- Henderson, Harold V.; Pukelsheim, Friedrich; Searle, Shayle R. (1983). "On the history of the Kronecker product". *Linear and Multilinear Algebra*. 14 (2): 113–120.
- Tracy, D.S.; Singh, R.P. (1972). "A new matrix product and its applications in matrix differentiation". *Statistica Neerlandica*. 26 (4): 143–157.

## External links

- MathWorld: [Kronecker product](https://mathworld.wolfram.com/KroneckerProduct.html)
- Springer Encyclopedia of Mathematics: Tensor product