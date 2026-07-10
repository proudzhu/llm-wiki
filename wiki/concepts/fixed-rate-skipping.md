---
type: concept
created: 2026-07-10
updated: 2026-07-10
tags:
  - efficiency
  - real-time
  - speech-enhancement
  - inference
---

# Fixed-Rate Skipping (FRS)

**Fixed-Rate Skipping (FRS)** is a temporal sparsification strategy for real-time streaming inference in which a neural mask estimator is executed only at a predefined interval, and the previously estimated mask is reused on the skipped frames in between. FRS reduces the mask update frequency — and thus the overall computational cost during streaming — by exploiting temporal redundancy in the input signal.

## Mechanism

With an update rate of $1/N$, the mask estimator runs once every $N$ frames; the remaining $N-1$ frames reuse the last estimated mask. This yields a predictable, fixed computational saving of approximately $(N-1)/N$ of the mask-estimation cost, independent of input statistics.

## Comparison with Learned Skipping

Learned skip gates (e.g., Skip RNN, TinyLSTM) use a gating mechanism that dynamically decides at each frame whether to update the recurrent state. While these can achieve high effective skip ratios (~80%), they introduce additional MACs for the gating decision and are less predictable. In [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|RT-Tango]] experiments, learned skipping caused larger quality degradation — especially for the Multi-Node DNN, where SI-SDR dropped from 4.5 dB to 3.3–3.8 dB — whereas FRS preserved performance within 0.2 dB of the baseline for both stages.

## Application in RT-Tango

RT-Tango adopts FRS with update rates of:

- **SN-DNN**: $1/4$ — one inference every four frames (75% frame skipping)
- **MN-DNN**: $1/2$ — one inference every two frames (50% frame skipping)

At a 4 ms hop rate, this reduces the DNN cost from 67.5 MMACs/s (no sparsification) to 28.08 MMACs/s, while maintaining SE quality close to the non-sparsified baseline.

## Related Concepts

- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/asymmetric-stft|Asymmetric STFT]]

## Related Sources

- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
