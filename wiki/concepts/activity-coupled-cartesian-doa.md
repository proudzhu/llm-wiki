---
type: concept
created: 2026-09-09
updated: 2026-09-19
sources:
  - raw/papers/grumiaux-2022-ssl-deep-learning-survey/full-text.txt
  - raw/papers/pan-2025-data-driven-acoustics/full-text.md
tags:
  - accdoa
  - doa-estimation
  - sel-d
  - deep-learning
---

# ACCDOA (Activity-Coupled Cartesian Direction of Arrival)

ACCDOA is an output representation for neural [[concepts/sound-source-localization|sound source localization]] / [[concepts/sel-d|SELD]] systems in which sound event activity and direction of arrival are coupled in a single Cartesian output vector: for each event class, the network regresses a 3D unit (or scaled) Cartesian direction vector whose magnitude encodes event activity. Introduced by Shimada et al. 2020, it was adopted by many DCASE 2021 SELD systems (e.g. Shimada et al. 2021, Naranjo-Alcazar et al. 2021, Huang & Perez 2021, Emmanuel et al. 2021).

## Significance

- **Joint SED+SSL up to the last layer**: unlike two-branch (SED head + SSL head) architectures, ACCDOA performs multi-task learning implicitly in a single output — no separate detection branch needed.
- **Regression, not classification**: avoids discretizing the DoA space into grid classes; continuous Cartesian coordinates sidestep grid-resolution limits and front/back ambiguity of azimuth-only outputs.
- As a multi-source representation, outputting one vector per event class handles simultaneous overlapping sources with (implicit) source counting via activity thresholds.

## Formulation (Pan 2025)

[[sources/pan-2025-data-driven-acoustics|Pan 2025]] presents ACCDOA as a **joint cost function for simultaneous source detection and localization**: with $L$ known source categories, the frame label $\bm{y}(t)$ is a $3 \times L$ matrix in which the magnitude of the $\ell$-th column encodes the probability of the $\ell$-th source's occurrence and the normalized column gives its direction,

$$
\bm{\varphi}_n(t) \leftarrow \frac{[\bm{y}(t)]_{:,\ell}}{\|[\bm{y}(t)]_{:,\ell}\|}, \qquad P[C_\ell | \bm{x}_n(t)] \leftarrow \|[\bm{y}(t)]_{:,\ell}\|,
$$

trained with the usual MSE regression loss between the network's $3 \times L \times T$ output and this label tensor. A full-sample label is a $3 \times L \times T$ matrix.

## Related Concepts

- [[concepts/sound-source-localization|Sound Source Localization]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/sel-d|SELD]]

## Related Sources

- [[sources/grumiaux-2022-ssl-deep-learning-survey|Grumiaux et al. 2022: A Survey of SSL with Deep Learning Methods]]
- [[sources/pan-2025-data-driven-acoustics|Pan 2025: Fundamentals of Data-Driven Approaches to Acoustic Signal Detection, Filtering, and Transformation]] — presents the $3 \times L$ label-matrix formulation of the joint detection+localization cost
