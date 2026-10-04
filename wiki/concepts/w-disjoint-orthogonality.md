---
type: concept
created: 2026-10-04
updated: 2026-10-04
sources:
  - raw/papers/yamaoka-2021-bin-wise-beamformer-combination/full-text.md
tags:
  - sparsity
  - time-frequency-masking
  - underdetermined
  - blind-source-separation
---

# W-Disjoint Orthogonality

**W-disjoint orthogonality (W-DO)** is the sparsity assumption that at most one source is active in each time-frequency bin of a mixture: for signals $z_p$ and $z_q$,

$$
z_p(f,t)\, z_q(f,t) = 0 \quad \forall f, t, \quad p \neq q.
$$

W-DO underlies binary TF masking and classic underdetermined separation methods (DUET, MENUET). It does not strictly hold for speech — only approximately, which motivated work on approximate W-DO (Rickard & Yılmaz 2002).

## P-DO Generalization

[[sources/yamaoka-2021-bin-wise-beamformer-combination|Yamaoka et al. 2021]] relax W-DO from pairs to $P$ signals, requiring only

$$
\prod_{p=1}^{P} z_p(f,t) = 0 \quad \forall f, t,
$$

i.e., **at most $P-1$ of the $P$ sources are active per TF bin**. P-DO with $P = 2$ recovers pairwise W-DO. The [[concepts/tflc-beamformer|TFLC beamforming]] framework assumes every $M$-combination of the $N-1$ interferers satisfies M-DO — at most $M-1$ interferers per TF bin — which is exactly the condition under which $K = C(N-1, M-1)$ beamformers (each nulling a different $M-1$ interferer subset) are sufficient to suppress whatever is dominant in each bin. Even when M-DO holds only approximately, the framework suppresses at least the $M-1$ dominant interferers per bin.

## Related Concepts

- [[concepts/tflc-beamformer|TFLC Beamforming]] — uses M-DO as its sparsity condition
- [[concepts/ideal-binary-mask|Ideal Binary Mask]] — binary masking built on the same sparsity intuition
- [[concepts/blind-source-separation|Blind Source Separation]] — underdetermined separation methods built on W-DO

## Related Sources

- [[sources/yamaoka-2021-bin-wise-beamformer-combination|Yamaoka, Ono & Makino 2021: TF-Bin-Wise Linear Combination of Beamformers]] — defines and applies the P-DO generalization
