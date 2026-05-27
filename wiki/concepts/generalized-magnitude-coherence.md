---
type: concept
created: 2026-05-27
updated: 2026-05-27
tags:
  - signal-processing
  - multichannel
  - coherence
  - spatial-audio
---

# Generalized Magnitude Coherence (GMC)

**Generalized Magnitude Coherence (GMC)** extends the concept of magnitude-squared coherence between two signals to an arbitrary number of channels. It is defined via the largest eigenvalue of the spectral coherence matrix and provides a single scalar measure of overall coherence across a multi-microphone array.

## Definition

For $N$ microphone signals, the spectral coherence matrix $\boldsymbol{C}_x(l,f)$ is constructed from pairwise complex coherence estimates:

$$[\boldsymbol{C}_x(l,f)]_{ij} = \Gamma_{x_i,x_j}(l,f)$$

where $\Gamma_{x_i,x_j}$ is the complex spatial coherence between microphones $i$ and $j$. The GMC is then defined as:

$$\gamma_x(l,f) = \frac{\lambda_x^{(\max)}(l,f) - 1}{N - 1}$$

where $\lambda_x^{(\max)}(l,f)$ is the largest eigenvalue of $\boldsymbol{C}_x(l,f)$. The GMC satisfies $0 \leq \gamma_x(l,f) \leq 1$, with $\gamma_x = 1$ when all signals are fully coherent.

### Relation to Standard Coherence

For $N = 2$ microphones, the GMC reduces to the magnitude of the standard complex coherence:

$$\gamma_x(l,f) = |\Gamma_{x_1,x_2}(l,f)|$$

## Applications

| Application | How GMC Is Used |
|-------------|-----------------|
| **CDR estimation** | GMC-based CDR estimator: $\widehat{\Lambda}_{\text{gen}} = (\gamma_n - \gamma_x)/(\gamma_x - 1)$ |
| **Microphone selection** | Principal eigenvector coefficients indicate which microphone has the highest signal quality |
| **Multi-microphone signal enhancement** | Inherently exploits all available microphones without pairwise averaging |

## Advantages Over Pairwise Coherence

- **All-channel integration**: Simultaneously uses information from $N$ microphones rather than averaging pairwise estimates
- **No DOA required**: The eigenvalue decomposition implicitly captures the spatial structure without explicit direction estimation
- **Inherent microphone selection**: The principal eigenvector provides a natural ranking of microphone signal quality

## Related Concepts

- [[concepts/spatial-coherence|Spatial Coherence]]
- [[concepts/coherent-to-diffuse-power-ratio|Coherent-to-Diffuse Power Ratio (CDR)]]
- [[concepts/dereverberation|Dereverberation]]
- [[concepts/multi-channel-speech-enhancement|Multi-Channel Speech Enhancement]]

## Key Sources

- [[sources/lollmann-2020-generalized-coherence-based-signal-enhancement|Löllmann, Brendel & Kellermann 2020: Generalized Coherence-Based Signal Enhancement]]
