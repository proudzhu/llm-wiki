---
type: concept
created: 2026-08-19
updated: 2026-08-19
sources:
  - raw/papers/zmolikova-2023-neural-target-speech-extraction-overview/full-text.md
tags:
  - spatial-clue
  - target-speaker-extraction
  - microphone-array
  - direction-of-arrival
  - phase-difference
---

# Angle Feature

The **angle feature (AF)** is a directional feature used in spatial-clue-conditioned [[concepts/target-speaker-extraction|target speech extraction (TSE)]] to encode the direction of arrival (DOA) of a target speaker relative to a microphone array. It measures how well the inter-microphone phase differences in the observed mixture match the phase differences expected for a plane wave arriving from the target direction.

## Formulation

The angle feature is the cosine of the difference between the **target phase difference (TPD)** and the **interaural phase difference (IPD)**, summed over a set $\mathcal{M}$ of microphone pairs:

$$
\mathrm{AF}[n, f] = \sum_{m_{1}, m_{2} \in \mathcal{M}} \cos\left(\mathrm{TPD}(m_{1}, m_{2}, \phi_{s}, f) - \mathrm{IPD}(m_{1}, m_{2}, n, f)\right),
$$

with the two phase quantities defined as

$$
\mathrm{TPD}(m_{1}, m_{2}, \phi_{s}, f) = \frac{2\pi f F_{s}}{F} \frac{\cos\phi_{s}\,\Delta_{m_{1}, m_{2}}}{c},
$$

$$
\mathrm{IPD}(m_{1}, m_{2}, n, f) = \angle Y^{m_{2}}[n, f] - \angle Y^{m_{1}}[n, f],
$$

where $\phi_{s}$ is the target direction (azimuth), $F_{s}$ the sampling rate, $F$ the STFT bin count, $c$ the speed of sound, $\Delta_{m_{1}, m_{2}}$ the distance between microphone $m_{1}$ and $m_{2}$, and $Y^{m}[n, f]$ the complex STFT coefficient of microphone $m$ at time frame $n$ and frequency bin $f$.

## Interpretation

For time-frequency bins dominated by a source arriving from direction $\phi_{s}$, the IPD closely matches the TPD, so $\mathrm{AF} \to +1$ (or $-1$ on antiphase microphone pairs). Time-frequency bins dominated by sources from other directions produce smaller-magnitude AF values. The AF thus forms a soft directional mask that the TSE network can fuse with mixture features to identify the target.

## Relation to Other Directional Features

The angle feature is the most commonly used directional feature in neural spatial TSE [3], [36], but alternatives exist:

- **Directional power ratio** — ratio of the response of a fixed beamformer steered toward $\phi_{s}$ to the total response across a grid of beamformers.
- **Directional SNR** — ratio of the target-direction beamformer response to the strongest off-target beamformer response.
- **IPD vectors from multi-channel enrollment** — when a multi-channel enrollment utterance is available, raw IPDs can be used directly without explicitly estimating DOA.

All such features encode the target direction into a form the speech-extraction network can consume alongside (or fused into) the mixture representation $\mathbf{Z}_{y}$.

## Use in TSE

In the general TSE framework, the angle feature plays the role of the **clue embedding** $\mathbf{E}_{s}$ that conditions the extraction network via a fusion layer (concatenation in Gu et al. [36]). When the spatial clue is used, the speech extraction module must also receive the multi-channel mixture input so it can identify which time-frequency bins belong to the target direction. The target extractor is often implemented as a [[concepts/beamforming|beamformer]] (e.g., MVDR) rather than a mask, because the spatial covariance matrices needed for beamforming can be derived from the TSE-estimated mask.

## Limitations

- **DOA estimation errors** propagate directly into the AF and degrade extraction.
- **Close angular separation** between speakers (< 15° in [36]) collapses the AFs and reduces the spatial clue's discriminability; combining with audio or visual clues is the standard remedy.
- **Fixed source assumption** — most AF-based systems assume the target direction is stationary; moving-source extensions are rare [24].

## Related Concepts

- [[concepts/target-speaker-extraction|Target Speaker Extraction (TSE)]]
- [[concepts/direction-of-arrival-estimation|Direction-of-Arrival Estimation]]
- [[concepts/beamforming|Beamforming]]
- [[concepts/mvdr-beamformer|MVDR Beamformer]]
- [[concepts/film-layer|FiLM Layer]]
- [[concepts/relative-transfer-function|Relative Transfer Function]]

## Related Sources

- [[sources/zmolikova-2023-neural-target-speech-extraction-overview|Zmolikova et al. 2023: Neural Target Speech Extraction: An Overview]]
