---
type: concept
created: 2026-05-18
updated: 2026-05-18
sources:
aliases:
- Spline ANC
- Spline LMS
tags:
- nonlinear-systems
- adaptive-filtering
- interpolation
---

# Spline Adaptive Filter

## Overview

A **Spline Adaptive Filter** models a nonlinear system as a cascade of a linear dynamic block and an **adaptive look-up table (LUT)** whose values are interpolated by a low-order polynomial spline curve. Originally proposed by Scarpiniti et al. (2013) for system identification, it was subsequently extended to [[nonlinear-active-noise-control|NLANC]]. Its principal advantage is much lower computational complexity than [[volterra-filter|Volterra]] or [[flann-filter|FLANN]] structures, while retaining strong nonlinear modelling capability.

## Structure

Two cascaded stages:

1. **Linear filter** (FIR or IIR) produces an intermediate signal $y_s(n)$.
2. **Spline interpolator** maps $y_s(n)$ through a control-point LUT.

The local span index $i$ and parameter $u$ are computed from the linear filter output:

$$
i = \left\lfloor \frac{y_s(n)}{\Delta x} \right\rfloor + \frac{C-1}{2}, \qquad
u(n) = \frac{y_s(n)}{\Delta x} - \left\lfloor \frac{y_s(n)}{\Delta x} \right\rfloor,
$$

where $\Delta x$ is the spacing between control points and $C$ is the total number of control points. The output is

$$ y(n) = \mathbf{u}^T(n)\,\mathbf{C}\,\mathbf{q}_i, $$

with $\mathbf{u}(n) = [u^3(n), u^2(n), u(n), 1]^T$, $\mathbf{C}$ the pre-computed spline basis matrix (e.g. Catmull–Rom, B-spline), and $\mathbf{q}_i$ the four neighbouring control points.

## Variants for ANC

- **FIR-spline ANC** (initial proposal): linear stage is FIR.
- **IIR-spline ANC** (2016): uses FuLMS-style feedback in the linear stage; better implementation efficiency.
- **Multi-channel spline ANC**: Extends to multi-channel scenarios; outperforms multi-channel VFxLMS and FsLMS in MSE and computational complexity.
- **Sparse-modeling EMFN+spline**: Reduces computational load with sparse secondary-path modeling without sacrificing performance.

## Advantages

- **Low complexity**: only the LUT and the linear filter are adapted; spline basis $\mathbf{C}$ is pre-computed.
- **Smooth nonlinearity**: the spline interpolation is differentiable, making gradient updates straightforward.
- **Locality**: each input updates only the four neighbouring control points.
- **Lower steady-state MSE** than [[volterra-filter|VFxLMS]] and [[flann-filter|FsLMS]] in NLANC benchmarks.

## Related Concepts

- [[nonlinear-active-noise-control|Nonlinear ANC]]
- [[volterra-filter|Volterra Filter]]
- [[flann-filter|FLANN Filter]]
- [[lagrange-interpolation|Lagrange Interpolation]] — alternative interpolation scheme
- [[adaptive-filtering|Adaptive Filtering]]

## Related Sources

- [[../sources/lu-2021-anc-survey-nonlinear|Lu et al. 2021: Survey on ANC — Part II (Nonlinear)]]
