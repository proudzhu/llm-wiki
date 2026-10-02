# Steered-response power

> Source: https://en.wikipedia.org/wiki/Steered-response_power
> Retrieved: 2026-10-02
> License: CC BY-SA 4.0 (Wikipedia contributors)

**Steered-response power** (SRP) is a family of acoustic source localization algorithms that can be interpreted as a beamforming-based approach that searches for the candidate position or direction that maximizes the output of a steered delay-and-sum beamformer.[1]

**Steered-response power with phase transform** (SRP-PHAT) is a variant using a "phase transform" to make it more robust in adverse acoustic environments.[2][3]

## Steered-response power

Consider a system of $M$ microphones, where each microphone is denoted by a subindex $m\in\{1,\dots,M\}$. The discrete-time output signal from a microphone is $s_{m}(n)$. The (unweighted) steered-response power (SRP) at a spatial point $\mathbf{x}=[x,y,z]^{\mathsf{T}}$ can be expressed as

$$P_{0}(\mathbf{x})\triangleq \sum _{n\in \mathbb{Z} }\left|\sum _{m=1}^{M}s_{m}{\big (}n-\tau _{m}(\mathbf{x} ){\big )}\right|^{2},$$

where $\mathbb{Z}$ denotes the set of integer numbers, and $\tau _{m}(\mathbf{x} )$ would be the time-lag due to the propagation from a source located at $\mathbf{x}$ to the $m$-th microphone.

The (weighted) SRP can be rewritten as

$$P(\mathbf{x})={\frac {1}{2\pi }}\sum _{m_{1}=1}^{M}\sum _{m_{2}=1}^{M}\int _{-\pi }^{\pi }\Phi _{m_{1},m_{2}}(e^{j\omega })S_{m_{1}}(e^{j\omega })S_{m_{2}}^{*}(e^{j\omega })e^{j\omega \tau _{m_{1},m_{2}}(\mathbf{x} )}\,d\omega,$$

where $()^{*}$ denotes complex conjugation, $S_{m}(e^{j\omega })$ represents the discrete-time Fourier transform of $s_{m}(n)$, and $\Phi _{m_{1},m_{2}}(e^{j\omega })$ is a weighting function in the frequency domain (discussed later). The term $\tau _{m_{1},m_{2}}(\mathbf{x} )$ is the discrete time-difference of arrival (TDOA) of a signal emitted at position $\mathbf{x}$ to microphones $m_{1}$ and $m_{2}$, given by

$$\tau _{m_{1},m_{2}}(\mathbf{x} )\triangleq \left\lfloor f_{s}{\frac {\|\mathbf{x} -\mathbf{x} _{m_{1}}\|-\|\mathbf{x} -\mathbf{x} _{m_{2}}\|}{c}}\right\rceil,$$

where $f_{s}$ is the sampling frequency of the system, $c$ is the sound propagation speed, $\mathbf{x} _{m}$ is the position of the $m$-th microphone, $\|\cdot \|$ is the 2-norm, and $\lfloor \cdot \rceil$ denotes the rounding operator.

## Generalized cross-correlation

The above SRP objective function can be expressed as a sum of generalized cross-correlations (GCCs) for the different microphone pairs at the time-lag corresponding to their TDOA

$$P(\mathbf{x})=\sum _{m_{1}=1}^{M}\sum _{m_{2}=1}^{M}R_{m_{1},m_{2}}(\tau _{m_{1},m_{2}}(\mathbf{x} )),$$

where the GCC for a microphone pair $(m_{1},m_{2})$ is defined as

$$R_{m_{1},m_{2}}(\tau )\triangleq {\frac {1}{2\pi }}\int _{-\pi }^{\pi }\Phi _{m_{1},m_{2}}(e^{j\omega })S_{m_{1}}(e^{j\omega })S_{m_{2}}^{*}(e^{j\omega })e^{j\omega \tau }\,d\omega.$$

The phase transform (PHAT) is an effective GCC weighting for time delay estimation in reverberant environments, that forces the GCC to consider only the phase information of the involved signals:

$$\Phi _{m_{1},m_{2}}(e^{j\omega })\triangleq {\frac {1}{|S_{m_{1}}(e^{j\omega })S_{m_{2}}^{*}(e^{j\omega })|}}.$$

## Estimation of source location

The SRP-PHAT algorithm consists in a grid-search procedure that evaluates the objective function $P(\mathbf{x})$ on a grid of candidate source locations $\mathcal{G}$ to estimate the spatial location $\textbf{x}_{s}$ of the sound source as the point of the grid that provides the maximum SRP:

$${\hat {\mathbf{x} }}_{s}=\arg \max _{\mathbf{x} \in {\mathcal {G}}}P(\mathbf{x} ).$$

Modifications of the classical SRP-PHAT algorithm have been proposed to reduce the computational cost of the grid-search step of the algorithm and to increase the robustness of the method. In the classical SRP-PHAT, for each microphone pair and for each point of the grid, a unique integer TDOA value is selected to be the acoustic delay corresponding to that grid point. This procedure does not guarantee that all TDOAs are associated to points on the grid, nor that the spatial grid is consistent, since some of the points may not correspond to an intersection of hyperboloids. This issue becomes more problematic with coarse grids since, when the number of points is reduced, part of the TDOA information gets lost because most delays are not anymore associated to any point in the grid.

The modified SRP-PHAT[4] collects and uses the TDOA information related to the volume surrounding each spatial point of the search grid by considering a modified objective function:

$$P'(\mathbf{x} )=\sum _{m_{1}=1}^{M}\sum _{m_{2}=1}^{M}\sum _{\tau =L_{m_{1},m_{2}}^{l}(\mathbf{x} )}^{L_{m_{1},m_{2}}^{u}(\mathbf{x} )}R_{m_{1},m_{2}}(\tau ),$$

where $L_{m_{1},m_{2}}^{l}(\mathbf{x} )$ and $L_{m_{1},m_{2}}^{u}(\mathbf{x} )$ are the lower and upper accumulation limits of GCC delays, which depend on the spatial location $\mathbf{x}$.

## Accumulation limits

The accumulation limits can be calculated beforehand in an exact way by exploring the boundaries separating the regions corresponding to the points of the grid. Alternatively, they can be selected by considering the spatial gradient of the TDOA $\nabla _{\tau _{m_{1},m_{2}}}(\mathbf{x} )=[\nabla _{x\tau _{m_{1},m_{2}}}(\mathbf{x} ),\nabla _{y\tau _{m_{1},m_{2}}}(\mathbf{x} ),\nabla _{z\tau _{m_{1},m_{2}}}(\mathbf{x} )]^{\mathsf{T}}$, where each component $\gamma \in \{x,y,z\}$ of the gradient is

$$\nabla _{\gamma \tau _{m_{1},m_{2}}}(\mathbf{x} )={\frac {1}{c}}\left({\frac {\gamma -\gamma _{m_{1}}}{\|\mathbf{x} -\mathbf{x} _{m_{1}}\|}}-{\frac {\gamma -\gamma _{m_{2}}}{\|\mathbf{x} -\mathbf{x} _{m_{2}}\|}}\right).$$

For a rectangular grid where neighboring points are separated a distance $r$, the lower and upper accumulation limits are given by

$$L_{m_{1},m_{2}}^{l}(\mathbf{x} )=\tau _{m_{1},m_{2}}(\mathbf{x} )-\|\nabla _{\tau _{m_{1},m_{2}}}(\mathbf{x} )\|\cdot d,$$

$$L_{m_{1},m_{2}}^{u}(\mathbf{x} )=\tau _{m_{1},m_{2}}(\mathbf{x} )+\|\nabla _{\tau _{m_{1},m_{2}}}(\mathbf{x} )\|\cdot d,$$

where

$$d={\frac {r}{2}}\min \left({\frac {1}{|\sin(\theta )\cos(\phi )|}},{\frac {1}{|\sin(\theta )\sin(\phi )|}},{\frac {1}{|\cos(\theta )|}}\right),$$

and the gradient direction angles are given by

$$\theta =\cos ^{-1}\left({\frac {\nabla _{z\tau _{m_{1},m_{2}}}(\mathbf{x} )}{\|\nabla _{\tau _{m_{1},m_{2}}}(\mathbf{x} )\|}}\right),$$

$$\phi =\arctan _{2}\left(\nabla _{y\tau _{m_{1},m_{2}}}(\mathbf{x} ),\nabla _{x\tau _{m_{1},m_{2}}}(\mathbf{x} )\right).$$

## See also

- Acoustic source localization
- Multilateration
- Audio signal processing

## References

1. Don H. Johnson; Dan E. Dudgeon (1993). *Array Signal Processing: Concepts and Techniques*. Prentice Hall. ISBN 978-0-13-048513-7.
2. DiBiase, J. H. (2000). *A High Accuracy, Low-Latency Technique for Talker Localization in Reverberant Environments using Microphone Arrays* (PDF) (Ph.D.). Brown Univ.
3. Silverman, H. F.; Yu, Y.; Sachar, J. M.; Patterson III, W. R. (2005). "Performance of real-time source-location estimators for a large-aperture microphone array". *IEEE Transactions on Speech and Audio Processing*. **13** (4). IEEE: 593–606. doi:10.1109/TSA.2005.848875.
4. Cobos, M.; Marti, A.; Lopez, J. J. (2011). "A Modified SRP-PHAT Functional for Robust Real-Time Sound Source Localization With Scalable Spatial Sampling". *IEEE Signal Processing Letters*. **18** (1). IEEE: 71–74. doi:10.1109/LSP.2010.2091502.
