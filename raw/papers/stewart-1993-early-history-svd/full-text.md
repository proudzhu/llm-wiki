G. W. Stewart

SIAM Review, Volume 35, Issue 4 (Dec., 1993), 551-566.

Stable URL:

http://links.jstor.org/sici?sici=0036-1445%28199312%2935%3A4%3C551%3AOTEHOT%3E2.0.CO%3B2-C

Your use of the JSTOR archive indicates your acceptance of JSTOR's Terms and Conditions of Use, available at http://www.jstor.org/about/terms.html. JSTOR's Terms and Conditions of Use provides, in part, that unless you have obtained prior permission, you may not download an entire issue of a journal or multiple copies of articles, and you may use content in the JSTOR archive only for your personal, non-commercial use.

Each copy of any part of a JSTOR transmission must contain the same copyright notice that appears on the screen or printed page of such transmission

SIAM Review is published by Society for Industrial and Applied Mathematics. Please contact the publisher for further permissions regarding the use of this work. Publisher contact information may be obtained at http://www.jstor.org/journals/siam.html

SIAM Review ©1993 Society for Industrial and Applied Mathematics

JSTOR and the JSTOR logo are trademarks of JSTOR, and are Registered in the U.S. Patent and Trademark Office.   
For more information on JSTOR contact jstor-info@umich.edu.

©2002 JSTOR

# ON THE EARLY HISTORY OF THE SINGULAR VALUE DECOMPOSITION\*

G. W. STEWART†

For Gene Golub on his 15th birthday.

Abstract. This paper surveys the contributions of five mathematicians—Eugenio Beltrami (1835-1899), Camille Jordan (1838–1921), James Joseph Sylvester (1814–1897), Erhard Schmidt (1876–1959), and Hermann Weyl (1885– 1955)—who were responsible for establishing the existence of the singular value decomposition and developing its theory.

Key words. singular value decomposition, history

AMS subject classifications. 01A, 15-03, 15A18

1. Introduction. One of the most fruitful ideas in the theory of matrices is that of a matrix decomposition or canonical form. The theoretical utility of matrix decompositions has long been appreciated. More recently, they have become the mainstay of numerical linear algebra, where they serve as computational platforms from which a variety of problems can be solved.

Of the many useful decompositions, the singular value decomposition —that is, the factorization of a matrix A into the product $\mathbf { U } \pmb { \Sigma } \mathbf { V } ^ { \mathbf { H } }$ of a unitary matrix U, a diagonal matrix Σ, and another unitary matrix $\mathbf { V } ^ { \mathbf { H } }$ — has assumed a special role. There are several reasons. In the first place, the fact that the decomposition is achieved by unitary matrices makes it an ideal vehicle for discussing the geometry of n-space. Second, it is stable; small perturbations in A correspond to small perturbations in Σ, and conversely. Third, the diagonality of Σ makes it easy to determine when A is near to a rank-degenerate matrix; and when it is, the decomposition provides optimal low rank approximations to A. Finally, thanks to the pioneering efforts of Gene Golub, there exist efficient, stable algorithms to compute the singular value decomposition.

The purpose of this paper is to survey the contributions of five mathematicians — Eugenio Beltrami (1835–1899), Camille Jordan (1838–1921), James Joseph Sylvester (1814–1897), Erhard Schmidt (1876–1959), and Hermann Weyl (1885–1955) — who were responsible for establishing the existence of the singular value decomposition and developing its theory. Beltrami, Jordan, and Sylvester came to the decomposition through what we should now call linear algebra; Schmidt and Weyl approached it from integral equations. To give this survey context, we will begin with with a brief description of the historical background.

It is an intriguing observation that most of the classical matrix decompositions predated the widespread use of matrices: they were cast in terms of determinants, linear systems of equations, and especially bilinear and quadratic forms. Gauss is the father of this development. Writing in 1823 [20, §31], he describes his famous elimination algorithm (first sketched in [19, 1809]) as follows:

Specifically, the function Ω [a quadratic function of x, y, z, etc.] can be reduced to the form

$$
\begin{array} { r } { \frac { u ^ { 0 } u ^ { 0 } } { A ^ { 0 } } + \frac { u ^ { \prime } u ^ { \prime } } { B ^ { \prime } } + \frac { u ^ { \prime \prime } u ^ { \prime \prime } } { C ^ { \prime \prime } } + \frac { u ^ { \prime \prime \prime } u ^ { \prime \prime \prime } } { D ^ { \prime \prime \prime } } + \mathrm { e t c . } + M , } \end{array}
$$

in which the divisors $\pmb { A } ^ { 0 } , \pmb { B } ^ { \prime } , \pmb { C } ^ { \prime \prime } , \pmb { C } ^ { \prime \prime \prime } ,$ etc. are constants and $\pmb { u } ^ { 0 } , \pmb { u } ^ { \prime } , \pmb { u } ^ { \prime \prime } , \pmb { u } ^ { \prime \prime \prime }$ , etc. are linear functions of $x , y , z , \in \mathrm { t c }$ However, the second function, $\pmb { u } ^ { \prime } ,$ is independent of x; the third, $\pmb { u } ^ { \prime \prime }$ is independent of x and $y ;$ the fourth, $\pmb { u } ^ { \prime \prime \prime }$ , is independent of $x , y ,$ and z, and so on. The last function, $\pmb { u } ^ { ( \pi - 1 ) }$ , depends only on the the last of the unknowns $x , y , z , \in \mathrm { t c } .$ Moreover, the coefficients $\pmb { A } ^ { 0 } , \pmb { B } ^ { \prime } , \bar { \pmb { C } } ^ { \prime \prime }$ , etc. multiply $x , y , z ,$ etc. in $\pmb { u } ^ { 0 } , \pmb { u } ^ { \prime } , \pmb { u } ^ { \prime \prime } ,$ , etc., respectively.

From this we easily see that Gauss's algorithm factors the matrix of the quadratic form $\mathbf { x } ^ { \mathrm { { T } } } \mathbf { A x }$ into the product $\mathbf { R } \mathbf { \dot { D } } ^ { - 1 } \mathbf { R }$ , where D is diagonal and R is upper triangular with the diagonals of D on its diagonal. Gauss's functions $\pmb { u } ^ { 0 } , \pmb { u } ^ { \prime } , \pmb { u } ^ { \prime \prime }$ , etc. are the components of the vector $\mathbf { u } = \mathbf { R } \mathbf { x }$

Gauss was also able to effectively obtain the inverse of a matrix by a process of eliminatio indefinita, in which the system of equations $\mathbf { y } = \mathbf { A } \mathbf { x }$ is transformed into the inverse system $\mathbf { x } = \mathbf { B } \mathbf { y }$ . Gauss's skill in manipulating quadratic forms and systems of equations made possible his very general treatment of the theory and practice of least squares.

Other developments followed. Cauchy [7, 1829] established the properties of the eigenvalues and eigenvectors of a symmetric system (including the interlacing property) by considering the corresponding homogeneous system of equations. In 1846, Jacobi [30] gave his famous algorithm for diagonalizing a symmetric matrix, and in a posthumous paper [31, 1857] he obtained the LU decomposition by decomposing a bilinear form in the style of Gauss. Weierstrass [63, 1868] established canonical forms for pairs of bilinear functions — what we should today call the generalized eigenvalue problem. Thus the advent of the singular value decomposition in 1873 is seen as one of a long line of results on canonical forms.

We will use modern matrix notation to describe the early work on the singular value decomposition. Most of it slips as easily into matrix terminology as Gauss's description of his decomposition; and we shall be in no danger of anachronism, provided we take care to use matrix notation only as an expository device, and otherwise stick close to the writer's argument. The greatest danger is that the use of modern notation will trivialize the writer's accomplishments by making them obvious to our eyes. On the other hand, presenting derivations in the original scalar form would probably exaggerate the obstacles these people had to overcome, since they were accustomed, as we are not, to grasping sets of equations as a whole.

With a single author, it is usually possible to modernize notation in such a way that it corresponds naturally to what he actually wrote. Here we are dealing with several authors, and uniformity is more important than correspondence with the original. Consequently, throughout paper we will be concerned with the singular value decomposition

$$
\mathbf { A } = \mathbf { U } \pmb { \Sigma } \mathbf { V } ^ { \mathbf { T } } ,
$$

where A is a real matrix of order $\pmb { n } .$

$$
\pmb { \Sigma } = \mathrm { d i a g } ( \sigma _ { 1 } , \sigma _ { 2 } , \ldots , \sigma _ { n } )
$$

has nonnegative diagonal elements arranged in descending order of magnitude, and

$$
\mathbf { U } = ( \mathbf { u } _ { 1 } \ \mathbf { u } _ { 2 } \ \cdots \ \mathbf { u } _ { n } ) \quad { \mathrm { a n d } } \quad \mathbf { V } = ( \mathbf { v } _ { 1 } \ \mathbf { v } _ { 2 } \ \cdots \ \mathbf { v } _ { n } )
$$

are orthogonal. The function $\| \cdot \|$ will denote the Frobenius norm defined by

$$
\left\| \mathbf { A } \right\| ^ { 2 } = \sum _ { i , j } a _ { i j } ^ { 2 } = \sum _ { i } \sigma _ { i } ^ { 2 } .
$$

In summarizing the contributions I have followed the principle that if you try to say everything you end up saying nothing. Most of the works treated here are richer than the following sketches would indicate, and the reader is advised to go to the sources for the full story.

2. Beltrami [5, 1873]. Together, Beltrami and Jordan are the progenitors of the singular value decomposition, Beltrami by virtue of first publication and Jordan by the completeness and elegance of his treatment. Beltrami's contribution appeared in the Journal of Mathematics for the Use of the Students of the Italian Universities, and its purpose was to encourage students to become familiar with bilinear forms.

The derivation. Beltrami begins with a bilinear form

$$
f ( \mathbf { x } , \mathbf { y } ) = \mathbf { x } ^ { \mathrm { T } } \mathbf { A } \mathbf { y } ,
$$

where A is real and of order n. If one makes the substitutions

$$
\mathbf { x } = \mathbf { U } \pmb { \xi } \quad \mathrm { a n d } \quad \mathbf { y } = \mathbf { V } \pmb { \eta } ,
$$

then

$$
f ( \mathbf { x } , \mathbf { y } ) = \pmb { \xi } ^ { \mathrm { T } } \mathbf { S } \pmb { \eta } ,
$$

where

$$
\begin{array} { r } { \mathbf { S } = \mathbf { U } ^ { \mathbf { T } } \mathbf { A } \mathbf { V } . } \end{array}\tag{2.1}
$$

Beltrami now observes that if U and V are required to be orthogonal, then there are ${ \pmb n } ^ { 2 } - { \pmb n }$ degrees of freedom in their choice, and he proposes to use these degrees of freedom to annihilate the off diagonal element of S.

Assume that S is diagonal, i.e., $\mathbf { S } = \pmb { \Sigma } = \mathrm { d i a g } ( \sigma _ { 1 } , \dots , \sigma _ { n } )$ . Then it follows from (2.1) and the orthogonality of V that

$$
\mathbf { U ^ { \mathrm { T } } A } = \pmb { \Sigma } \mathbf { V ^ { \mathrm { T } } } .\tag{2.2}
$$

Similarly,

$$
\mathbf { A } \mathbf { V } = \mathbf { U } \mathbf { \Sigma } .\tag{2.3}
$$

Substituting the value of U obtained from (2.3) into (2.2), Beltrami obtains the equation

$$
\begin{array} { r } { \mathbf { U } ^ { \mathrm { T } } ( \mathbf { A } \mathbf { A } ^ { \mathrm { T } } ) = \Sigma ^ { 2 } \mathbf { U } ^ { \mathrm { T } } , } \end{array}\tag{2.4}
$$

and similarly he obtains

$$
( \mathbf { A } ^ { \mathbf { T } } \mathbf { A } ) \mathbf { V } = \mathbf { V } \mathbf { \Sigma } ^ { 2 } .
$$

Thus the $\pmb { \sigma _ { i } }$ are the roots of the equations

$$
\mathbf { d e t } ( \mathbf { A A } ^ { \mathbf { T } } - \sigma ^ { 2 } I ) = 0\tag{2.5}
$$

and

$$
\operatorname* { d e t } ( \mathbf { A } ^ { \mathbf { T } } \mathbf { A } - \sigma ^ { 2 } I ) = 0 .\tag{2.6}
$$

Note that the derivation, as presented by Beltrami, assumes that ∑, and hence A, is nonsingular. Beltrami now argues that the two functions (2.5) and (2.6) are identical because they are polynomials of degree n that assume the same values at $\sigma = \sigma _ { i } ( i = 1 , . . . , n )$ and the

common value $\operatorname* { d e t } ^ { 2 } ( A )$ at $\sigma = 0$ , an argument that presupposes that the singular values are distinct and nonzero.

Beltrami next states that by a well-known theorem, the roots of (2.5) are real. Moreover, they are positive. To show this he notes that

$$
0 < \| \mathbf { x } ^ { \mathrm { T } } \mathbf { A } \| ^ { 2 } = \mathbf { x } ^ { \mathrm { T } } ( \mathbf { A } \mathbf { A } ^ { \mathrm { T } } ) \mathbf { x } = \pmb { \xi } ^ { \mathrm { T } } \pmb { \Sigma } ^ { 2 } \pmb { \xi } ,\tag{2.7}
$$

the last equation following from the theory of quadratic forms. This inequality immediately implies that the $\pmb { \sigma } _ { i } ^ { 2 }$ are positive.

There is some confusion here. Beltrami appears to be assuming the existence of the vector $\pmb { \xi } ,$ whose very existence he is trying to establish. The vector required by his argument is an eigenvector of $\mathbf { A A ^ { T } }$ corresponding to $\pmb { \sigma }$ . The fact that the two vectors turn out to be the same apparently caused Beltrami to leap ahead of himself and use $\pmb { \xi }$ in (2.7).

Beltrami is now ready to give an algorithm to determine the diagonalizing transformation.

1. Find the roots of (2.5).

2. Determine U from (2.4). Here Beltrami notes that the columns of U are determined up to factors of $\pm 1$ , which is true only if the $\sigma _ { i }$ are distinct. He also tacitly assumes that the resulting U will be orthogonal, which also requires that the $\sigma _ { i }$ be distinct.

3. Determine V from (2.2). This step requires that Σ be nonsingular.

Discussion. From the foregoing it is clear that Beltrami derived the singular value decomposition for a real, square, nonsingular matrix having distinct singular values. His derivation is the one given in most textbooks, but it lacks the extras needed to handle degeneracies. It may be that in omitting these extras Beltrami was simplifying things for his student audience, but a certain slackness in the exposition suggests that he had not thought the problem through.

3. Jordan [32], [33]. Camille Jordan can rightly be called the codiscoverer of the singular value decomposition. Although he published his derivation a year after Beltrami, it is clear that the work is independent. In fact, the “Mémoire sur les formes bilinéaires" treats three problems, of which the the reduction of a bilinear form to a diagonal form by orthogonal substitutions is the simplest.²

The derivation. Jordan starts with the form

$$
P = \mathbf { x } ^ { \mathrm { { T } } } \mathbf { A } \mathbf { y }
$$

and seeks the maximum and minimum of P subject to

$$
\left\| \mathbf { x } \right\| ^ { 2 } = \left\| \mathbf { y } \right\| ^ { 2 } = 1 .\tag{3.1}
$$

The maximum is determined by the equation

$$
0 = d P = d \mathbf { x } ^ { \mathrm { { T } } } \mathbf { A } \mathbf { y } + \mathbf { x } ^ { \mathrm { { T } } } \mathbf { A } d \mathbf { y } ,\tag{3.2}
$$

which must be satisfied for all dx and $\pmb { d } \mathbf { y }$ that satisfy

$$
d \mathbf { x } ^ { \mathrm { { T } } } \mathbf { x } = 0 \quad { \mathrm { a n d } } \quad d \mathbf { y } ^ { \mathrm { { T } } } \mathbf { y } = 0 .\tag{3.3}
$$

Jordan then asserts that “equation (3.2) will therefore be a combination of the equations (3.3)," from which one obtains³

$$
\mathbf { A } \mathbf { y } = \sigma \mathbf { x }\tag{3.4}
$$

and

$$
\mathbf { x } ^ { \mathsf { T } } \mathbf { A } = \tau \mathbf { y } ^ { \mathsf { T } } .\tag{3.5}
$$

From (3.4) it follows that the maximum is

$$
\mathbf { x } ^ { \mathrm { { T } } } ( \mathbf { A } \mathbf { y } ) = { \boldsymbol { \sigma } } \mathbf { x } ^ { \mathrm { { T } } } \mathbf { x } = { \boldsymbol { \sigma } } .
$$

Similarly the maximum is also τ, so that $\sigma = \tau$

Jordan now observes that $\pmb { \sigma }$ is determined by the vanishing of the determinant

$$
D = \left| \begin{array} { c c } { - \sigma \mathbf { I } } & { \mathbf { A } } \\ { \mathbf { A } ^ { \mathrm { T } } } & { - \sigma \mathbf { I } } \end{array} \right|
$$

of the system (3.4)—(3.5). He shows that this determinant contains only even powers of $\pmb { \sigma }$

Now let $\sigma _ { 1 }$ be a root of the equation ${ \pmb { D } } = { \bf 0 } .$ , and let (3.4) and (3.5) be satisfied by $\mathbf { x } = \mathbf { u }$ and $\mathbf { y } = \mathbf { v }$ , where $\| \mathbf { u } \| ^ { 2 } = \| \mathbf { v } \| ^ { 2 } = 1$ . (Jordan notes that one can find such a solution, even when it is not unique.) Let

$$
\hat { \mathbf { U } } = ( \mathbf { u _ { \alpha } } \mathbf { U _ { * } } ) \quad \mathrm { a n d } \quad \hat { \mathbf { V } } = ( \mathbf { v _ { \alpha } } \mathbf { V _ { * } } )
$$

be orthogonal, and let

$$
\begin{array} { r } { \mathbf { x } = \hat { \mathbf { U } } \hat { \mathbf { x } } \quad \mathrm { a n d } \quad \mathbf { y } = \hat { \mathbf { V } } \hat { \mathbf { y } } . } \end{array}
$$

With these substitutions, let

$$
\begin{array} { r } { P = \hat { \mathbf { x } } ^ { \mathrm { T } } \hat { \mathbf { A } } \hat { \mathbf { y } } . } \end{array}
$$

In this system, P attains its maximum⁴ for $\hat { \mathbf { x } } = \hat { \mathbf { y } } = \mathbf { e } _ { 1 }$ , where $\mathbf { e } _ { 1 } = ( 1 , 0 , \ldots , 0 ) ^ { \mathrm { T } }$ . Moreover, at the maximum we have

$$
\hat { \bf A } \hat { \bf y } = \sigma _ { 1 } \hat { \bf x } \quad \mathrm { a n d } \quad \hat { \bf x } ^ { \mathrm { T } } \hat { \bf A } = \sigma _ { 1 } \hat { \bf y } ^ { \mathrm { T } } ,
$$

which implies that

$$
\hat { \bf A } = \left( \begin{array} { c c } { \sigma } & { \mathbf { 0 } } \\ { \mathbf { 0 } } & { \mathbf { A } _ { 1 } } \end{array} \right) .
$$

Thus with $\pmb { \xi } _ { 1 } = \hat { x } _ { 1 }$ and $\eta _ { 1 } = { \hat { y } } _ { 1 } , P$ assumes the form

$$
\sigma _ { 1 } \xi _ { 1 } \eta _ { 1 } + P _ { 1 } ,
$$

where $P _ { 1 }$ is independent of $\pmb { \xi } _ { 1 }$ and $\pmb { \eta _ { 1 } }$ . Jordan now applies the reduction inductively to $P _ { 1 }$ to arrive at the canonical form

$$
P = \pmb { \xi } ^ { \mathrm { T } } \pmb { \Sigma } \pmb { \eta } .
$$

Finally, Jordan notes that when the roots of the characteristic equation $\pmb { D } = \pmb { 0 }$ are simple, the columns of U and $\mathbf { v }$ can be calculated directly from (3.1), (3.4), and (3.5).

Discussion. In this paper we see the sure hand of a skilled professional. Jordan proceeds from problem to solution with economy and elegance. His approach of using a partial solution of the problem to reduce it to one of smaller size—deflation is the modern term — avoids the degeneracies that complicate Beltrami's approach. Incidentally, the technique of deflation apparently lay fallow until Schur [52, 1917] used it to establish his triangular form of a general matrix. It is now a widely used theoretical and algorithmic tool.

The matrix

$$
\left( \begin{array} { c c } { { { \bf 0 } } } & { { { \bf A } } } \\ { { { \bf A } ^ { \mathrm { T } } } } & { { { \bf 0 } } } \end{array} \right) ,
$$

from which the determinant D was formed, is also widely used. Its present day popularity is due to Wielandt (see [18, p.113]) and Lanczos [38, 1958]. The latter apparently rediscovered the singular value decomposition independently.

Yet another consequence of Jordan's approach is the variational characterization of the largest singular value as the maximum of a function. This and related characterizations have played an important role in perturbation and localization theorems for singular values (for more, see [55, §4.4]).

4. Sylvester [57, 1889], [59, 1889], [58, 1889]. Sylvester wrote a footnote and two papers on the subject of the singular value decomposition. The footnote appears at the end of a paper in The Messenger of Mathematics [57] entitled “A new proof that a general quadric may be reduced to its canonical form (that is, a linear function of squares) by means of a real orthoganal substitution." In the paper Sylvester describes an iterative algorithm for reducing a quadratic form to diagonal form. In the footnote he points out that an analogous iteration can be used to diagonalize a bilinear form and says that he has “sent for insertion in the C. R. of the Institute, a Note in which I give the rule for effecting this reduction." The rule turns out to be Beltrami's algorithm. In a final paper [58, 1889], Sylvester presents both the iterative algorithm and the rule.

The rule. Here we follow [59, 1899]. Sylvester begins with the bilinear form

$$
\pmb { { \cal B } } = \mathbf { x } ^ { \mathrm { T } } \mathbf { A } \mathbf { y }
$$

and considers the quadratic form

$$
M = \sum _ { i } \left( { \frac { d B } { d y _ { i } } } \right) ^ { 2 }
$$

(which is $\mathbf { x } ^ { \mathrm { { T } } } \mathbf { A } \mathbf { A } ^ { \mathrm { { T } } } \mathbf { x } ,$ a fact tacitly assumed by Sylvester). Let $M = \sum \lambda _ { i } \pmb { \xi } _ { i } ^ { 2 }$ be the canonical form of M. If B has the canonical form $\begin{array} { r } { B = \sum \sigma _ { i } \pmb { \xi } _ { i } \pmb { \eta } _ { i } } \end{array}$ , then $\textstyle \sum [ \sigma _ { i } \pmb { \xi } ] ^ { 2 }$ is orthogonally equivalent to $M = \sum { \lambda _ { i } \pmb { \xi } _ { i } ^ { 2 } }$ , which implies that $\lambda _ { i } = \sigma _ { i } ^ { 2 }$ in some order.

To find the substitutions, Sylvester introduces the matrices $\mathbf { M } = \mathbf { A } \mathbf { A } ^ { \mathrm { T } }$ and $\mathbf { N } = \mathbf { A } ^ { \mathrm { T } } \mathbf { A }$ and asserts that the substitution for x is the substitution that diagonalizes M and substitution for y is the one that diagonalizes N. In general, this is true only if the singular values of A are distinct.

In his Comptes Rendus note, Sylvester gives the following rule for finding the coefficients of the x-substitution corresponding to a singular value σ. Strike a row of the matrix $\mathbf { M } - \sigma ^ { 2 } \mathbf { I }$ Then the vector of coefficients is the vector of minors of order $n - 1$ of the reduced matrix normalized so that their sum of squares is one. Coefficients of the y-substitution may be obtained analogously from $ { \mathbf { N } } - \sigma ^ { 2 }  { \mathbf { I } }$ . This only works if the singular value σ is simple.

Infinitesimal iteration. Sylvester first proposed this method as a technique for showing that a quadratic form could be diagonalized, and he later extended it to bilinear forms. It is already intricate enough for quadratic forms, and we will confine ourselves to a sketch of that case.

Sylvester proceeds inductively, assuming that he can solve a problem of order n — 1. Thus for ${ \pmb n } = 3$ he can assume the matrix is of the form

$$
\mathbf { A } = { \left( \begin{array} { l l l } { a } & { 0 } & { f } \\ { 0 } & { b } & { g } \\ { f } & { g } & { c } \end{array} \right) } ,
$$

the zeros being introduced by the induction step. His problem is then to get rid of f and g without destroying the zeros previously introduced.

Sylvester proposes to make an “infinitesimal orthogonal substitution" of the form

$$
\left( \begin{array} { l } { x _ { 1 } } \\ { x _ { 2 } } \\ { x _ { 3 } } \end{array} \right) = \left( \begin{array} { c c c } { 1 } & { \epsilon } & { \eta } \\ { - \epsilon } & { 1 } & { \theta } \\ { - \eta } & { - \theta } & { 1 } \end{array} \right) \left( \begin{array} { l } { \xi _ { 1 } } \\ { \xi _ { 2 } } \\ { \xi _ { 3 } } \end{array} \right) ,
$$

where the off-diagonal quantities are so small that powers higher than the first can be neglected. Then the the (2, 1)- and (1, 2)-elements of the transformed matrix are

$$
( a - b ) \epsilon - f \theta - g \eta ,\tag{4.1}
$$

while the change in $f ^ { 2 } + g ^ { 2 }$ is given by

$$
{ \textstyle \frac { 1 } { 2 } } \delta ( f ^ { 2 } + g ^ { 2 } ) = ( a - c ) f \eta + ( b - c ) g \theta .
$$

If either $( a - c ) f$ or $( b - c ) g$ is nonzero, η and θ can be chosen to decrease $f ^ { 2 } + g ^ { 2 }$ . If $( a - b )$ is nonzero, € may then be chosen so that (4.1) is zero, i.e., so that the zero previously introduced is preserved. Sylvester shows how special cases like ${ a = b }$ can be handled by explicitly deflating the problem.

Sylvester now claims that an infinite sequence of these infinitesimal transformations will reduce one of f or g to zero, or will reduce the problem to one of the special cases.

Discussion. These are not easy papers to read. The style is opaque, and Sylvester pontificates without proving, leaving too many details to the reader. The mathematical reasoning harks back to an earlier, less rigorous era.

The fact that Sylvester sent a note to Comptes Rendus, the very organ where Jordan announced his results a decade and a half earlier, makes it clear that he was working in ignorance of his predecessors. It also suggests the importance he attached to his discovery, since a note in Comptes Rendus was tantamount to laying claim to a new result.

Sylvester was also working in ignorance of the iterative algorithm of Jacobi [30, 1846] for diagonalizing a quadratic form. The generalization of this algorithm to the singular value decomposition is due to Kogbetliantz [36].

It is not clear whether Sylvester intended to ignore second-order terms in his iteration or whether he regards the diagonalization as being composed of an (uncountably) infinite number of infinitesimal transformation. Though the preponderance of his statements favor the latter, neither interpretation truly squares with everything he writes. In the first, small, but finite, terms.replace the zeros previously introduced, so that a true diagonalization is not achieved. The second has the flavor of some recent algorithms in which discrete transformations are replaced by continuous transformations defined by differential equations (for applications of this approach to the singular value decomposition see [8] and [11]). But Sylvester does not give enough detail to write down such equations.

5. Schmidt [50, 1907]. Our story now moves from the domain of linear algebra to integral equations, one of the hot topics of the first decades of our century. In his treatment of integral equations with unsymmetric kernels, Erhard Schmidt (of Gram-Schmidt fame and a student of Hilbert) introduced the infinite-dimensional analogue of the singular value decomposition. But he went beyond the mere existence of the decomposition by showing how it can be used to obtain optimal, low-rank approximations to an operator. In doing so he transformed the singular value decomposition from a mathematical curiosity to an important theoretical and computational tool.

Symmetric kernels. Schmidt's approach is essentially the same as Beltrami's; however, because he worked in infinite-dimensional spaces of functions he could not appeal to previous results on quadratic forms. Consequently, the first part of his paper is devoted to symmetric kernels.

Schmidt begins with a kernel $A ( s , t )$ that is continuous and symmetric on $[ a , b ] \times [ a , b ]$ A continuous, nonvanishing function $\varphi ( s )$ satisfying

$$
\varphi ( s ) = \lambda \int _ { a } ^ { b } A ( s , t ) \varphi ( t ) d t
$$

is said to be an eigenfunction of A corresponding to the eigenvalue λ. Note that Schmidt's eigenvalues are the reciprocals of ours.

Schmidt then establishes the following facts.

1. The kernel A has at least one eigenfunction.

2. The eigenvalues and their eigenfunctions are real.

3. Each eigenvalue of A has at most a finite number of linearly independent eigenfunctions.

4. The kernel A has a complete, orthonormal system of eigenfunctions; that is, a sequence $\varphi _ { 1 } ( s ) , \varphi _ { 2 } ( s ) , . . .$ . of orthonormal eigenfunctions such that every eigenfunction can be expressed as a linear combination of a finite number of the $\varphi _ { j } ( s )$ 5

5. The eigenvalues satisfy

$$
\int _ { a } ^ { b } \int _ { a } ^ { b } \left( A ( s , t ) \right) ^ { 2 } d s d t \geq \sum _ { i } { \frac { 1 } { \lambda _ { i } ^ { 2 } } } ,
$$

which implies that the sequence of eigenvalues is unbounded.

Unsymmetric kernels. Schmidt now allows $A ( s , t )$ to be unsymmetric and calls any nonzero pair $\pmb { u } ( \pmb { s } )$ and $v ( s )$ satisfying

$$
u ( s ) = \lambda \int _ { a } ^ { b } A ( s , t ) v ( t ) d t
$$

and

$$
v ( t ) = \lambda \int _ { a } ^ { b } A ( s , t ) u ( s ) d s ,
$$

a pair of adjoint eigenfunctions corresponding to the eigenvalue $\lambda . ^ { 6 }$ He then introduces the symmetric kernels

$$
\bar { A ( s , t ) } = \int _ { a } ^ { b } A ( s , r ) A ( t , r ) d r
$$

and

$$
\underline { { { A } } } ( s , t ) = \int _ { a } ^ { b } A ( r , s ) A ( r , t ) d r
$$

and shows that if ${ \pmb u } _ { 1 } ( s ) , { \pmb u } _ { 2 } ( s ) , . . .$ . is a complete orthonormal system for $\bar { A } ( s , t )$ corresponding to the eigenvalues $\lambda _ { 1 } ^ { 2 } , \lambda _ { 2 } ^ { 2 } , \ldots$ , then the sequence defined by

$$
v _ { i } ( t ) = \lambda _ { i } \int _ { a } ^ { b } A ( s , t ) u ( s ) d s , \qquad i = 1 , 2 , \ldots
$$

is a complete orthonormal system for $\underline { { \boldsymbol { A } } } ( s , t )$ . Moreover, for $i = 1 , 2 , \dots$ . the functions $\pmb { u } _ { i } ( s )$ and $v _ { i } ( s )$ form an adjoint pair for $A ( s , t )$

Schmidt then goes on to consider the expansion of functions in series of eigenfunctions. Specifically, if

$$
g ( s ) = \int _ { a } ^ { b } A ( s , t ) h ( t ) d t ,
$$

then

$$
g ( s ) = \sum _ { i } { \frac { u _ { i } ( s ) } { \lambda _ { i } } } \int _ { a } ^ { b } h ( t ) v _ { i } ( t ) d t ,
$$

and the convergence is absolute and uniform. Finally, he shows that if g and h are continuous, then

$$
\int _ { a } ^ { b } \int _ { a } ^ { b } A ( s , t ) g ( s ) h ( t ) d s d t = \sum _ { i } { \frac { 1 } { \lambda _ { i } } } \int _ { a } ^ { b } g ( s ) u _ { i } ( s ) d s \int _ { a } ^ { b } h ( t ) v _ { i } ( t ) d t ,\tag{5.1}
$$

an expression which Schmidt says “corresponds to the canonical decomposition of a bilinear form."

The approximation theorem. Up to now, our exposition has been cast in the language of integral equations, principally to keep issues of analysis in the foreground. These issues are not as important in what follows, and we will therefore return to matrix notation, taking care, as always, to follow Schmidt's development closely.

The problem Schmidt sets out to solve is that of finding the best approximation to A of the form

$$
\mathbf { A } \cong \sum _ { i = 1 } ^ { k } \mathbf { x } _ { i } \mathbf { y } _ { i } ^ { \operatorname { T } }
$$

in the sense that

$$
\left\| \mathbf { A } - \sum _ { i = 1 } ^ { k } \mathbf { x } _ { i } \mathbf { y } _ { i } ^ { \mathrm { T } } \right\| = \operatorname* { m i n } .
$$

In other words, he is looking for the best approximation of rank not greater than k.

Schmidt begins by noting that if

$$
\mathbf { A } _ { k } = \sum _ { i = 1 } ^ { k } \sigma _ { i } \mathbf { u } _ { i } \mathbf { v } _ { i } ^ { \mathsf { T } } ,\tag{5.2}
$$

then

$$
\| \mathbf { A } - \mathbf { A } _ { k } \| ^ { 2 } = \| \mathbf { A } \| ^ { 2 } - \sum _ { i = 1 } ^ { k } \sigma _ { i } ^ { 2 } .
$$

Consequently, if it can be shown that for arbitrary $\mathbf { x } _ { i }$ and $\mathbf { y } _ { i }$

$$
\left\| \mathbf { A } - \sum _ { i = 1 } ^ { k } \mathbf { x } _ { i } \mathbf { y } _ { i } ^ { \operatorname { T } } \right\| \geq \| \mathbf { A } \| ^ { 2 } - \sum _ { i = 1 } ^ { k } \sigma _ { i } ^ { 2 } ,\tag{5.3}
$$

then $\mathbf { A } _ { k }$ will be the desired approximation.

Without loss of generality we may assume that the vectors $\mathbf { x } _ { 1 } , \ldots , \mathbf { x } _ { k }$ are orthonormal. For if they are not, we can use Gram-Schmidt orthogonalization to express them as linear combinations of orthonormal vectors, substitute these expressions in $\textstyle \sum _ { i = 1 } ^ { k } \mathbf { x } _ { i } \mathbf { y } _ { i } ^ { \mathsf { T } }$ , and collect terms in the new vectors.

Now

$$
\begin{array} { l } { \displaystyle \left\| \mathbf { A } - \sum _ { i = 1 } ^ { k } \mathbf { x } _ { i } \mathbf { y } _ { i } ^ { \mathsf { T } } \right\| = \mathrm { t r a c e } \left( \left( \mathbf { A } - \sum _ { i = 1 } ^ { k } \mathbf { x } _ { i } \mathbf { y } _ { i } ^ { \mathsf { T } } \right) ^ { \mathrm { T } } \left( \mathbf { A } - \sum _ { i = 1 } ^ { k } \mathbf { x } _ { i } \mathbf { y } _ { i } ^ { \mathsf { T } } \right) \right) } \\ { \displaystyle \qquad = \mathrm { t r a c e } \left( \mathbf { A } ^ { \mathsf { T } } \mathbf { A } + \sum _ { i = 1 } ^ { k } ( \mathbf { y } _ { i } - \mathbf { A } ^ { \mathsf { T } } \mathbf { x } _ { i } ) ( \mathbf { y } _ { i } - \mathbf { A } ^ { \mathsf { T } } \mathbf { x } _ { i } ) ^ { \mathrm { T } } - \sum _ { i = 1 } ^ { k } \mathbf { A } ^ { \mathsf { T } } \mathbf { x } _ { i } \mathbf { x } _ { i } ^ { \mathsf { T } } \mathbf { A } \right) . } \end{array}
$$

Since trace $\left( ( \mathbf { y } _ { i } - \mathbf { A } ^ { \mathrm { T } } \mathbf { x } _ { i } ) ( \mathbf { y } _ { i } - \mathbf { A } ^ { \mathrm { T } } \mathbf { x } _ { i } ) ^ { \mathrm { T } } \right) \geq 0$ and trace $( \mathbf { A } \mathbf { x } _ { i } \mathbf { x } _ { i } ^ { \mathsf { T } } \mathbf { A } ^ { \mathsf { T } } ) = \| \mathbf { A } \mathbf { x } _ { i } \| ^ { 2 }$ , the result will be established if it can be shown that

$$
\sum _ { i = 1 } ^ { k } \| \mathbf { A x } _ { i } \| ^ { 2 } \leq \sum _ { i = 1 } ^ { k } \sigma _ { i } ^ { 2 } .
$$

Let $\begin{array} { r } { { \bf V } = ( { \bf V } _ { 1 } \ { \bf V } _ { 2 } ) } \end{array}$ , where $\mathbf { v } _ { 1 }$ has $\pmb { k }$ columns, and let $\pmb { \Sigma } = \mathbf { d i a g } ( \pmb { \Sigma } _ { 1 } , \pmb { \Sigma } _ { 2 } )$ be a conformal partition of $\pmb { \Sigma } .$ Then

$$
\begin{array} { r l } & { \| \mathbf { A x } _ { i } \| ^ { 2 } = \sigma _ { k } ^ { 2 } + \big ( \| \Sigma _ { 1 } \mathbf { V } _ { 1 } ^ { \mathrm { T } } \mathbf { x } _ { i } \| ^ { 2 } - \sigma _ { k } ^ { 2 } \| \mathbf { V } _ { 1 } ^ { \mathrm { T } } \mathbf { x } _ { i } \| ^ { 2 } \big ) } \\ & { \quad \quad \quad - \big ( \sigma _ { k } ^ { 2 } \| \mathbf { V } _ { 2 } ^ { \mathrm { T } } \mathbf { x } _ { i } \| ^ { 2 } - \| \Sigma _ { 2 } \mathbf { V } _ { 2 } ^ { \mathrm { T } } \mathbf { x } _ { i } \| ^ { 2 } \big ) } \\ & { \quad \quad \quad - \sigma _ { k } ^ { 2 } \big ( 1 - \| \mathbf { V } ^ { \mathrm { T } } \mathbf { x } _ { i } \| \big ) . } \end{array}\tag{5.4}
$$

Now the last two terms in (5.4) are clearly nonnegative. Hence

$$
\begin{array} { r l } { \displaystyle \sum _ { i = 1 } ^ { k } \| \mathbf { A } \mathbf { x } _ { i } \| ^ { 2 } \leq k \sigma _ { k } ^ { 2 } + \displaystyle \sum _ { i = 1 } ^ { k } ( \| \Sigma _ { 1 } \mathbf { V } _ { 1 } ^ { \mathsf { T } } \mathbf { x } _ { i } \| ^ { 2 } - \sigma _ { k } ^ { 2 } \| \nabla _ { 1 } ^ { \mathsf { T } } \mathbf { x } _ { i } \| ^ { 2 } ) } & { } \\ & { \quad = k \sigma _ { k } ^ { 2 } + \displaystyle \sum _ { i = 1 } ^ { k } \displaystyle \sum _ { j = 1 } ^ { k } ( \sigma _ { j } ^ { 2 } - \sigma _ { k } ^ { 2 } ) | \mathbf { V } _ { j } ^ { \mathsf { T } } \mathbf { x } _ { i } | ^ { 2 } } \\ & { \quad = \displaystyle \sum _ { j = 1 } ^ { k } \left( \sigma _ { k } ^ { 2 } + ( \sigma _ { j } ^ { 2 } - \sigma _ { k } ^ { 2 } ) \displaystyle \sum _ { i = 1 } ^ { k } | \mathbf { v } _ { j } ^ { \mathsf { T } } \mathbf { x } _ { i } | ^ { 2 } \right) } \\ & { \quad \leq \displaystyle \sum _ { j = 1 } ^ { k } ( \sigma _ { k } ^ { 2 } + ( \sigma _ { j } ^ { 2 } - \sigma _ { k } ^ { 2 } ) ) } \\ & { \quad = \displaystyle \sum _ { j = 1 } ^ { k } \sigma _ { j } ^ { 2 } , } \end{array}
$$

which establishes the result.

Discussion. Schmidt's two contributions to the singular value decomposition are its generalization to function spaces and his approximation theorem. Although Schmidt did not refer to earlier work on the decomposition in finite-dimensional spaces, the quote following (5.1) suggests that he knew of its existence. Nonetheless, his contribution here is substantial, especially since he had to deal with many of the problems of functional analysis without modern tools.

An important difference in Schmidt's version of the decomposition is the treatment of nullvectors of $\mathbf { A } .$ In his predecessors'treatments they are part of the substitution that reduces the bilinear form $\mathbf { x } ^ { \mathrm { { T } } } \mathbf { A } \mathbf { y }$ to its canonical form. For Schmidt they are not part of the decomposition. The effect of this can be seen in the third term of (5.4), which in the usual approach is zero but in Schmidt's approach can be nonzero.

The crowning glory of Schmidt's work is his approximation theorem, which is nontrivial to conjecture and hard to prove from scratch. Schmidt's proof is certainly not pretty—we will examine the more elegant approach of Weyl in the next section—but it does establish what can properly be termed the fundamental theorem of the singular value decomposition.

6. Weyl [64, 1912]. An important application of the approximation theorem is the determination of the rank of a matrix in the presence of error. If A is of rank k and $\tilde { \mathbf { A } } = \mathbf { A } + \mathbf { E }$ then the last $\pmb { n } - \pmb { k }$ singular values of $\tilde { \bf A }$ satisfy

$$
\tilde { \sigma } _ { k + 1 } ^ { 2 } + \cdots + \tilde { \sigma } _ { n } ^ { 2 } \leq \| E \| ^ { 2 } ,\tag{6.1}
$$

so that the defect in rank of A will be manifest in the size of its trailing singular values.

The inequality (6.1) is actually a perturbation theorem for the zero singular values of a matrix. Weyl's contribution to the theory of the singular value decomposition was to develop a general perturbation theory and use it to give an elegant proof of the approximation theorem. Although Weyl treated integral equations with symmetric kernels, in a footnote on Schmidt's contribution he states, “E. Schmidt's theorem, by the way, treats arbitrary (unsymmetric) kernels; however, our proof can also be applied directly to this more general case."Since here we are concerned with the more general case, we will paraphrase Weyl's development as he might have written it for unsymmetric matrices.

The location of singular values. The heart of Weyl's development is a lemma concerning the singular values of a perturbed matrix. Specifically, if $\mathbf { B } _ { k } = \mathbf { \bar { X } Y ^ { T } }$ , where X and Y have k columns (i.e., rank $( \pmb { \mathrm { \pmb { \mathrm { B } } } } _ { k } ) \leq k )$ , then

$$
\sigma _ { 1 } ( \mathbf { A } - \mathbf { B } _ { k } ) \geq \sigma _ { k + 1 } ( \mathbf { A } ) ,\tag{6.2}
$$

where $\sigma _ { i } ( \cdot )$ denotes the ith singular value of its argument.

The proof is simple. Since Y has k columns, there is a linear combination

$$
\mathbf { v } = \gamma _ { 1 } \mathbf { v } _ { 1 } + \gamma _ { 2 } \mathbf { v } _ { 2 } + \cdot \cdot \cdot + \gamma _ { k + 1 } \mathbf { v } _ { k + 1 }
$$

of the first $k + 1$ columns of V (from the singular value decomposition of A) such that $\mathbf { Y ^ { \mathrm { T } } v } = 0$ . Without loss of generality we may assume that $\| \mathbf { v } \| = 1$ , or equivalently that $\gamma _ { 1 } ^ { 2 } + \cdots + \gamma _ { k + 1 } ^ { 2 } = 1$ . It follows that

$$
\begin{array} { r l } & { \sigma _ { 1 } ^ { 2 } ( \mathbf { A } - \mathbf { B } ) \geq \mathbf { v } ^ { \mathrm { T } } ( \mathbf { A } - \mathbf { B } ) ^ { \mathrm { T } } ( \mathbf { A } - \mathbf { B } ) \mathbf { v } } \\ & { \qquad = \mathbf { v } ^ { \mathrm { T } } ( \mathbf { A } ^ { \mathrm { T } } \mathbf { A } ) \mathbf { v } } \\ & { \qquad = \gamma _ { 1 } ^ { 2 } \sigma _ { 1 } ^ { 2 } + \gamma _ { 2 } ^ { 2 } \sigma _ { 2 } ^ { 2 } + \cdots + \gamma _ { k + 1 } ^ { 2 } \sigma _ { k + 1 } ^ { 2 } } \\ & { \qquad \geq \sigma _ { k + 1 } ^ { 2 } . } \end{array}
$$

Weyl then proves two theorems. The first states that if $\mathbf { A } = \mathbf { A } ^ { \prime } + \mathbf { A } ^ { \prime \prime }$ , then

$$
\sigma _ { i + j - 1 } \leq \sigma _ { i } ^ { \prime } + \sigma _ { j } ^ { \prime \prime } ,\tag{6.3}
$$

where the ${ \bf { \sigma } } _ { \pmb { \sigma } _ { i } ^ { \prime } }$ and ${ \pmb { \sigma } } _ { i } ^ { \prime \prime }$ are the singular values of $\mathbf { A } ^ { \prime }$ and $\mathbf { A } ^ { \prime \prime }$ arranged in descending order of magnitude. Weyl begins by establishing (6.3) for $i = j = 1$

$$
\begin{array} { r } { \sigma _ { 1 } = \mathbf { u } _ { 1 } ^ { \mathrm { T } } \mathbf { A } \mathbf { v } _ { 1 } = \mathbf { u } _ { 1 } ^ { \mathrm { T } } \mathbf { A } ^ { \prime } \mathbf { v } _ { 1 } + \mathbf { u } _ { 1 } ^ { \mathrm { T } } \mathbf { A } ^ { \prime \prime } \mathbf { v } _ { 1 } \leq \sigma _ { 1 } ^ { \prime } + \sigma _ { 1 } ^ { \prime \prime } . } \end{array}
$$

To establish the result in general, let $\mathbf { A } _ { i - 1 } ^ { \prime }$ and $\mathbf { A } _ { j - 1 } ^ { \prime \prime }$ be formed in analogy with (5.2). Then $\sigma _ { 1 } ( \mathbf { A } ^ { \prime } { - } \mathbf { A } _ { i - 1 } ^ { \prime } ) = \sigma _ { i } ( \mathbf { A } ^ { \prime } )$ and $\sigma _ { 1 } ( \mathbf { A } ^ { \prime \prime } { - } \mathbf { A } _ { i - 1 } ^ { \prime \prime } ) = \sigma _ { j } ( \mathbf { \bar { A } } ^ { \prime \prime } )$ . Moreoverrank $( \mathbf { A } _ { i - 1 } ^ { \prime } + \mathbf { A } _ { j - 1 } ^ { \prime \prime } ) \leq i + j - 2$ From these facts and from (6.2) it follows that

$$
\begin{array} { r l } & { \sigma _ { i } ^ { \prime } + \sigma _ { j } ^ { \prime \prime } = \sigma _ { 1 } ( \mathbf { A } ^ { \prime } - \mathbf { A } _ { i - 1 } ^ { \prime } ) + \sigma _ { 1 } ( \mathbf { A } ^ { \prime \prime } - \mathbf { A } _ { j - 1 } ^ { \prime \prime } ) } \\ & { \qquad \geq \sigma _ { 1 } ( \mathbf { A } - \mathbf { A } _ { i - 1 } ^ { \prime } - \mathbf { A } _ { j - 1 } ^ { \prime \prime } ) } \\ & { \qquad \geq \sigma _ { i + j - 1 } , } \end{array}
$$

which proves the theorem.

The second theorem is really a corollary of the first. Set $\mathbf { A } ^ { \prime } = \mathbf { A } - \mathbf { B } _ { k }$ and $\mathbf { A } ^ { \prime \prime } = \mathbf { B } _ { k }$ where, as above, $\mathbf { B } _ { k }$ has rank k. Since $\sigma _ { k + 1 } ( \mathbf { B } _ { k } ) = 0$ , we have on setting $j = k + 1$ in (6.3),

$$
\sigma _ { i } ( \mathbf { A } - \mathbf { B } _ { k } ) \geq \sigma _ { k + i } , \qquad i = 1 , 2 , \ldots .
$$

As a corollary to this result we obtain

$$
\| \mathbf { A } - \mathbf { B } _ { k } \| ^ { 2 } \geq \sigma _ { k + 1 } ^ { 2 } + \cdot \cdot \cdot + \sigma _ { n } ^ { 2 } .
$$

This inequality is equivalent to (5.3) and thus establishes the approximation theorem.

Discussion. Weyl did not actually write down the development for unsymmetric kernels, and we remind the reader once again of the advisability of consulting original sources. In particular, since symmetric kernels can have negative eigenvalues as well as positive ones, Weyl wrote down three sequences of inèqualities: one for positive eigenvalues, one for negative, and one—corresponding to the inequalities presented here—for the absolute values of the eigenvalues.

Returning to the perturbation problem that opened this section, if in (6.3) we make the identification $\mathbf { A } \gets \tilde { \mathbf { A } } , \mathbf { A } ^ { \prime } \gets \mathbf { A }$ , and ${ \bf A } ^ { \prime \prime }  \bf E$ , then with j = 1 we get

$$
\tilde { \sigma } _ { i } \leq \sigma _ { i } + \| \mathbf { E } \| _ { 2 } ,
$$

where $\| E \| _ { 2 } = \sigma _ { 1 } ( E )$ . On the other hand, if we make the identifications $\mathbf { A } ^ { \prime }  \tilde { \mathbf { A } }$ and ${ \bf A } ^ { \prime \prime }  - { \bf E }$ , then we get

$$
\tilde { \sigma } _ { i } \leq \sigma _ { i } - \| \mathbf { E } \| _ { 2 } .
$$

It follows that

$$
| \tilde { \sigma } _ { i } - \sigma _ { i } | \leq \| \mathbf { E } \| _ { 2 } , \qquad i = 1 , 2 , \ldots , n .
$$

The number $\| \mathbf E \| _ { 2 }$ is called the spectral norm of E. Thus Weyl's result implies that if the singular values of A and $\tilde { \bf A }$ are associated in their natural order, they cannot differ by more than the spectral norm of the perturbation.

7. Envoi. With Weyl's contribution, the theory of the singular value decomposition can be said to have matured. The subsequent history is one of extensions, new discoveries, and applications. What follows is a brief, selective sketch of these developments yet to come.

Extensions. Autonne [2, 1913] extended the decomposition to complex matrices. Eckart and Young [16, 1936], [17, 1939] extended it to rectangular matrices and rediscovered Schmidt's approximation theorem, which is often (and incorrectly) called the Eckart-Young theorem.

8. Nomenclature.7 The term "singular value" seems to have come from the literature on integral equations. A little after the appearance of Schmidt's paper, Bateman [4, 1908] refers to numbers that are essentially the reciprocals of the eigenvalues of the kernel as singular values. Picard [45, 1909] combined Schmidt's results with Riesz's theorem on the strong convergence of generalized Fourier series [48, 1907] to establish a necessary and sufficient condition for the existence of solutions of integral equations. In a later paper on the same subject [46, 1910], he notes that for symmetric kernels Schmidt's eigenvalues are real and in this case (but not in general) he calls them singular values. By 1937, Smithies [53] was referring to singular values of an integral equation in our modern sense of the word. Even at this point, usage had not stabilized. In 1949, Weyl [65] speaks of the "two kinds of eigenvalues of a linear transformation," and in a 1969 translation of a 1965 Russian treatise on nonselfadjoint operators Gohberg and Krein [21] refer to the “s-numbers" of an operator. For the term "principal component," see below.

Related decompositions. Beltrami's proof of the existence of the singular value decomposition shows that it is closely related to the spectral decompositions of ATA and AAT. It can $\mathbf { A A ^ { \mathrm { T } } }$ also be used to derive the polar decomposition of Autonne [1, 1902], [3, 1915], in which is a matrix is factored into the product of a Hermitian matrix and a unitary matrix.

In his investigation of the geometry of n-space, Jordan [34, 1875] introduced canonical bases for pairs of subspaces. This line of development lead to the CS (cosine-sine) decomposition of a partitioned orthogonal matrix introduced implicitly by Davis and Kahan [9, 1970], and explicitly in [54, 1977]. The CS decomposition can in turn be used to derive the generalized singular value decomposition of a matrix, either in the original form introduced by Van Loan [60] or in the revised version of Paige and Saunders [43, 1981]. Recently even broader generalizations of the singular value decomposition have been proposed, e.g., see [10].

Although it is not, strictly speaking, a matrix decomposition, the Moore-Penrose pseudoinverse [41, 1920], [44, 1955] can be calculated from the singular value decomposition of a matrix as follows. Suppose that the first k singular values of A are nonzero while the last $\pmb { n } - \pmb { k }$ are zero, and set $\bar { \Sigma ^ { \dag } } = \mathrm { d i a g } ( \sigma _ { 1 } ^ { - 1 } , \ldots , \sigma _ { k } ^ { - 1 } , 0 , \ldots , 0 )$ . Then the pseudoinverse of A is given by $\mathbf { A } ^ { \dagger } = \mathbf { U } \pmb { \Sigma } ^ { \dagger } \mathbf { V } ^ { \mathbf { T } }$

Unitarily invariant norms. A matrix norm $\| \cdot \| _ { \mathbf { u } }$ is unitarily invariant if $\| \mathbf { U } ^ { \mathbf { H } } \mathbf { A } \mathbf { V } \| _ { \mathbf { u } } =$ $\| \mathbf { A } \| _ { \mathbf { u } }$ for all unitary matrices U and V. A vector norm $\| \cdot \| _ { \ 8 }$ is a symmetric gauge function if $\| \mathbf { P x } \| _ { \mathbf { g } } = \| \mathbf { x } \| _ { \mathbf { g } }$ for any permutation matrix and $\| | \mathbf { x } | \| _ { \mathbf { g } } = \| \mathbf { x } \| _ { \mathbf { g } }$ Von Neumann [61, 1937] showed that to any unitarily invariant norm $\Vert \cdot \Vert _ { \mathbf { u } }$ there corresponds a symmetric gauge function $\| \cdot \| _ { g }$ such that $\| \mathbf { A } \| _ { \mathbf { u } } = \| ( \sigma _ { 1 } , \ldots , \sigma _ { n } ) ^ { \mathrm { T } } \| _ { \mathbf { g } } , \mathrm { i . e . }$ , a unitarily invariant norm is a symmetric gauge function of the singular values of its argument.

Approximation theorems. Schmidt's approximation theorem has been generalized in a number of directions. Mirsky [40, 1960] showed that Ak of (5.2) is a minimizing matrix in any $\mathbf { A } _ { k }$ unitarily invariant norm. The case where further restrictions are imposed on the minimizing matrix are treated in [12], [22], and [47].

Given matrices A and B, the Procrustes problem, which arises in the statistical method of factor analysis, is that of determining a unitary matrix Q such that $\| \mathbf { A } - \mathbf { B } \mathbf { Q } \|$ is minimized (see [29, 1962]). Green [25, 1952] and Schöneman [51, 1966] showed that if $\mathbf { U } ^ { \mathbf { T } } \mathbf { A } ^ { \mathbf { T } } \mathbf { B } \mathbf { V } = \pmb { \Sigma }$ is the singular value decomposition of ATB, then the minimizing matrix is $\mathbf { A } ^ { \mathbf { T } } \mathbf { B } .$ $\mathbf { Q } = \mathbf { V U } ^ { \mathbf { T } }$ . Rao [47, 1980] considers the more general problem of minimizing $\| \mathbf { P A } - \mathbf { B Q } \|$ , where P and Q are orthogonal.

Principal components. An alternative to factor analysis is the principal component analysis of Hotelling [27, 1933]. Specifically, if xT is a multivariate random variable with mean $\mathbf { x ^ { \mathrm { { T } } } }$ zero and common dispersion matrix D, and $\mathbf { D } = \mathbf { V } \pmb { \Sigma } \mathbf { V } ^ { \mathbf { T } }$ is the eigenvalue-eigenvector decomposition of D, then the components of $\mathbf { x } ^ { \mathrm { { T } } } \mathbf { V }$ are uncorrelated with variances $\sigma _ { i }$ . Hotelling called the transformed variables "the principal components of variance" of xT. If the rows of X $\mathbf { x ^ { \mathrm { { T } } } }$ consist of independent samples of xT, then the expectation of $\mathbf { x } ^ { \hat { \mathbf { T } } }$ $\mathbf { X } ^ { \mathbf { T } } \mathbf { X }$ is proportional to Σ. It follows that the matrix  obtained from the singular value decomposition of X is an estimate V.

Hotelling [28, 1936] also introduced canonical correlations between two sets of random variables that bear the same relation to the generalized singular value decomposition as his principal components bear to the singular value decomposition.

Inequalities involving singular values. Just as Schmidt did not have the last word on approximation theorems, Weyl was not the last to work on inequalities involving singular values. The subject is too voluminous to treat here, and we refer the reader to the excellent survey with references in [26, Chap. 3]. However, mention should be made of a line of research initiated by Weyl [65, 1949] relating the singular values and eigenvalues of a matrix.

Computational methods. The singular value decomposition was introduced into numerical analysis by Golub and Kahan [23, 1965], who proposed a computational algorithm. However, it was Golub [24, 1970] who gave the algorithm that has been the workhorse of the past two decades. Recently, Demmel and Kahan [13, 1990] have proposed an interesting alternative.

Sources. For short bibliographies of the principles see the Dictionary of Scientific Biography [6], and particularly the articles [6], [14], [15], [42], and [56]. The nearest thing to a systematic survey of the devèlopment of matrix decompositions is the chapter on determinants and matrices in Kline's Mathematical Thought from Ancient to Modern Times [35, Chap. 33]. Mac Duffee's book, The Theory of Matrices [39], is a gold mine of references to the older literature.

Acknowledgments. I would like to thank Anne Greenbaum, Nick Higham, David Wood, and Hongyuan Zha for reading and commenting on the manuscript.

## REFERENCES

[1] L. AuToNNE, Sur les groupes linéaires, réels et orthogonaux, Bull. Soc. Math. France, 30 (1902), pp. 121–134.

[2] —, Sur les matrices hypohermitiennes et les unitairs, Comptes Rendus de l’Academie Sciences, Paris, 156 (1913), pp. 858–860.

[3] —, Sur les matrices hypohermitiennes et sur les matrices unitaires, Ann. Univ. Lyons, Nouvelle Sér. I, 38 (1915), pp. 1–77.

[4] H. BATEMAN, A formula for the solving function of a certain integral equation of the second kind, Trans. Cambridge Philos. Soc., 20 (1908), pp. 179–187.

[5] E. BELTRAMI, Sulle funzioni bilineari, Giornale di Matematiche ad Uso degli Studenti Delle Universita, 11 (1873), pp. 98–106. An English translation by D. Boley is available as University of Minnesota, Department of Computer Science, Minneapolis, MN, Technical Report 90–37, 1990.

[6] M. BERNKoPF, Schmidt, Erhard, in Dictionary of Scientific Biography XII, C. C. Gillispe, ed., Charles Scribner's Sons, New York, 1975.

[7] A. L. CAuCHY, Sur l'équation á l'aide de laquelle on détermine les inégalités séculaires des mouvements des planètes, in Oeuvres Complétes (IIe Série), Vol. 9, 1829.

[8] M. CHU, A differential equation approach to the singular value decomposition of bidiagonal matrices, Linear Algebra Appl., 80 (1986), pp. 71–79.

[9]C. DAvIs AND W. KAHAN, The rotation of eigenvectors by a perturbation. III, SIAM J. Numer. Anal., 7 (1970), pp. 1-46.

[10] B. DE MooR, A tree of generalizations of the ordinary singular value decomposition, Linear Algebra Appl. 147 (1991), pp. 469–500.

[11] P. DEIFT, J. DENMEL, L.-C. LI, AND C. ToMEI, The bidiagonal singular value decomposition and Hamiltonian mechanics, SIAM J. Numer. Anal., 28 (1991), pp. 1463–1516.

[12] · J. DEMMEL, The smallest perturbation of a submatrix which lowers the rank and constrained total least squares problems, SIAM J. Numer. Anal., 24 (1987), pp. 199–206.

[13] J. DEMMEL AND W. KAHAN, Accurate singular values of bidiagonal matrices, SIAM J. Sci. Statist. Comput., 11 (1989), pp. 873–912.

[14] J. DIEUDoNNÉ, Jordan, Camille, in Dictionary of Scientific Biography VII, C. C. Gillispe, ed., Charles Scribner's Sons, New York, 1973.

[15] —, Weyl, Hermann, in Dictionary of Scientific Biography XIV, C. C. Gillispe, ed., Charles Scribner's Sons, New York, 1976.

[16] C. ECKART AND G. YoUNG, The approximation of one matrix by another of lower rank, Psychometrika, 1 (1936), pp. 211–218.

[17] —, A principal axis transformation for non-Hermitian matrices, Bull. Amer. Math. Soc., 45 (1939), pp. 118–121.

[18] K. FAN AND A. J. HoFFMAN, Some metric inequalities in the space of matrices, Proc. Amer. Math. Soc., 6 (1955), pp. 111–116.

[19] C. F. GAuss, Theoria Motus Corporum Coelestium in Sectionibus Conicis Solem Ambientium, Perthes and Besser, Hamburg, Germany, 1809.

[20] , Theoria combinationis observationum erroribus minimis obnoxiae, pars posterior, in Werke, IV, Königlichen Gesellshaft der Wissenschaften zu Göttingin (1880), 1823, pp. 27–53.

[21] I. C. GoíBERG AND M. G. KREIN, Introduction to the Theory of Linear Nonselfadjoint Operators, American Mathematical Society, Providence, RI, 1969.

[22] G. H. GoLUB, A. HoFFMAN, AND G. W. STEwART, A generalization of the Eckart-Young matrix approximation theorem, Linear Algebra Appl., 88/89 (1987), pp. 317–327.

[23]G. H. GoLUB AND W. KAHAN, Calculating the singular values and pseudo-inverse of a matrix, SIAM J. Numer. Anal., 2 (1965), pp. 205–224.

[24] G. H. GoLUB AND C. REINsCH, Singular value decomposition and least squares solution, Numer. Math., 14 (1970), pp. 403–420; also in [66, pp.134–151].

[25] B. F. GrEEN, The orthogonal approximation of the oblique structure in factor analysis, Psychometrika, 17 (1952), pp, 429–440.

[26] R. A. HoRN AND C. R. JoíNsoN, Topics in Matrix Analysis, Cambridge University Press, Cambridge, UK, 1991.

[27] H. HoτELLING, Analysis of a complex of statistical variables into principal components, J. Ed. Psych., 24 (1933), pp. 417–441 and 498–520.

[28]—, Relation between two sets of variates, Biometrika, 28 (1936), pp. 322–377.

[29] J. R. HuRLEY AND R. B. CArTELL, The Procrustes program: Direct rotation to test a hypothesized factor structure, Behav. Sci., 7 (1962), pp. 258–262.

[30] C. G. J. JACoBı, Über ein leichtes Verfahren die in der Theorie der Säculärstörungen vorkommenden Gleichungen numerisch aufzulösen, J. Reine Angew. Math., 30 (1846), pp. 51–94.

[31] —, Über eine elementare Transformation eines in Buzug jedes von zwei Variablen-Systemen linearen und homogenen Ausdrucks, J. Reine Angew. Math., 53 (1857, posthumous), pp. 265–270.

[32] C. JoRDAN, Mémoire sur les formes bilinéaires, J. Math. Pures Appl., Deuxième Série, 19 (1874), pp. 35–54.

[33] —, Sur la réduction des formes bilinéaires, Comptes Rendus de l'Academie Sciences, Paris, 78 (1874), pp. 614–617.

[34] —, Essai sur la géométrie à n dimensions, Bull. Soc. Math., 3 (1875), pp. 103–174.

[35] M. KLINE, Mathematical Thought from Ancient to Modern Times, Oxford University Press, New York, 1972.

[36] E. G. KoGBETLIANTz, Solution of linear systems by diagonalization of coefficients matrix, Quart. Appl. Math., 13 (1955), pp. 123–132.

[37] L. KRoNECKER, Über bilineare Formen, Sitzungberichte der Königlich Preußischen Akademie der Wissenschaften zu Berlin, (1866), pp. 597–613.

[38] C. LANCzos, Linear systems in self-adjoint form, Amer. Math. Monthly, 65 (1958), pp. 665–679.

[39] C. C. MAc DuFFEE, The Theory of Matrices, Chelsea, New York, 1946.

[40] L. MırsKY, Symmetric gauge functions and unitarily invariant norms, Quart. J. Math., 11 (1960), pp. 50–59.

[41] E. H. MooRE, On the reciprocal of the general algebraic matrix, Bull. Amer. Math. Soc., 26 (1920), pp. 394 395.

[42] J. D. NoRTH, Sylvester, James Joseph, in Dictionary of Scientific Biography XIII, C. C. Gillispe, ed., Charles Scribner's Sons, New York, 1976.

[43]C. C. PAIGE AND M. A. SAUNDERs, Toward a generalized singular value decomposition, SIAM J. Numer. Anal., 18 (1981), pp. 398–405.

[44] R. PENRosE, A generalized inverse for matrices, Proc. Cambridge Philos. Soc., 51 (1955), pp. 406–413.

[45] E. PiCARD, Quelques remarques sur les équations intégrales de première espèce et sur certains problèms de Physique mathématique, Comptes Rendus de 1'Academie Sciences, Paris, 148 (1909), pp. 1563–1568.

[46] —, Sur un théorèm général relatif aux équations intégrales de premièr espèce et sur quelques problèmes de physique mathématique, Rend. Circ. Mat. Palermo, 25 (1910), pp. 79–97.

[47] C. R. RAo, Matrix approximations and reduction of dimensionality in multivariate statistical analysis, in Multivariate Analysis, V, P. R. Krishnaiah, ed., North Holland, Amsterdam, 1980.

[48]F. RiEsz, Über orthogonale Funktionensystem, Götinger Nachr., (1907), pp. 116–122. Cited in [49].

[49] F. Riesz AND B. Sz.-NAGY, L. F. Boron, trans., Functional Analysis, Ungar, New York, 1955.

[50]E. ScHMIDT, Zur Theorie der linearen und nichtlinearen Integralgleichungen. I Teil. Entwicklung willkürlichen Funktionen nach System vorgeschriebener, Math. Ann., 63 (1907), pp. 433–476.

[51] P. H. SchöNEMAN, A generalized solution of the orthogonal Procrustes problem, Psychometrika, 31 (1966), pp. 1–10.

[52] J. SchUR, Über Potenzreihen, die im Innern des Einkeitskreise beschänkt sind, J. Angew. Math., 147 (1917), pp. 205–232.

[53] F. SmrTíIEs, The eigen-values and singular values of integral equations, Proc. London Math. Soc., 43 (1937), pp. 255–279.

[54]G. W. STEwART, On the perturbation of pseudo-inverses, projections, and linear least squares problems, SIAM Rev., 19 (1977), pp. 634–662.

[55] G. W. STEwART AND J.-G. SUN, Matrix Perturbation Theory, Academic Press, Boston, MA, 1990.

[56] D. J. STRUIk, Beltrami, Eugenio, in Dictionary of Scientific Biography I, C. C. Gillispe, ed., Charles Scribner's Sons, New York, 1970.

[57] J. J. SYLvEsTER, A new proof that a general quadric may be reduced to its canonical form (that is, a linear function of squares) by means of a real orthogonal substitution, Messenger of Mathematics, 19 (1889), pp. 1–5.

[58] —, On the reduction of a bilinear quantic of the nth order to the form of a sum of n products by a double orthogonal substitution, Messenger of Mathematics, 19 (1889), pp. 42–46.

[59] —. Sur la réduction biorthogonale d’une forme linéo-linéaire à sa forme cannonique, Comptes Rendus de l'Academie Sciences, Paris, 108 (1889), pp. 651–653.

[60]C. F. VAN LoAN, A general matrix eigenvalue algorithm, SIAM J. Numer. Anal., 12 (1975), pp. 819–834.

[61] J. voN NEuMANN, Some matrix-inequalities and metrization of matrix-space, Tomsk. Univ. Rev., 1 (1937), pp. 286–300.

[62] —, Collected Works, A. H. Taub, ed., Pergamon, New York, 1962.

[63] K. WEIERsTRAss, Zur Theorie der bilinearen und quadratischen Formen, Monatshefte Akademie Wissenschaften Berlin, (1868), pp. 310–338.

[64] H. WEYL, Das asymptotische Verteilungsgesetz der Eigenwert linearer partieller Differentialgleichungen (mit einer Anwendung auf der Theorie der Hohlraumstrahlung), Math. Ann., 71 (1912), pp. 441–479.

[65] —, Inequalities between the two kinds of eigenvalues of a linear transformation, Proc. Nat. Acad. Sci., 35 (1949), pp. 408–411.

[66] J. H. WILKINsoN AND C. REINsCH, Handbook for Automatic Computation, Vol. II Linear Algebra, Springer-Verlag, New York, 1971.