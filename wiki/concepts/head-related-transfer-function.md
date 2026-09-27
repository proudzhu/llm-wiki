---
type: concept
created: 2026-09-27
updated: 2026-09-27
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
tags:
  - acoustics
  - spatial-audio
  - hrtf
---

# Head-Related Transfer Function (HRTF)

The **head-related transfer function** is the frequency-domain transfer function describing how a sound from a given direction is filtered by the listener's head, torso, and pinnae before reaching each eardrum. Its time-domain counterpart is the head-related impulse response (HRIR). Direction-dependent differences between the two ears' HRTFs give rise to the [[concepts/interaural-time-difference|interaural time difference]] and [[concepts/interaural-level-difference|interaural level difference]] cues used for spatial perception. HRTFs vary substantially across individuals (anthropometry) and are modified by devices worn on the head (see [[concepts/device-specific-hrtf|device-specific HRTF]]).

## HRTFs in Training-Data Synthesis

Because binaural ground truth is unobtainable in natural recordings, HRTF datasets are used to synthesize binaural training data: a mono source $x_k$ is convolved with the left- and right-ear impulse responses $h_{k,L}, h_{k,R}$ to produce the ear signals $s_L = \sum_k x_k * h_{k,L}$, $s_R = \sum_k x_k * h_{k,R}$. Veluri et al. (2023) use the CIPIC HRTF dataset (non-reverberant, per-subject) augmented with measured (SBSBRIR, RRBRIR) and simulated (CATT RIR) binaural room impulse responses to also capture reverberation and multipath; splitting datasets across subjects and rooms lets the network generalize to unseen listeners and environments. Related per-device transfer functions are studied in [[concepts/device-specific-hrtf|device-specific HRTF]] for ANC design.

## Related Concepts

- [[concepts/interaural-time-difference|Interaural Time Difference (ITD)]]
- [[concepts/interaural-level-difference|Interaural Level Difference (ILD)]]
- [[concepts/device-specific-hrtf|Device-Specific HRTF]]
- [[concepts/binaural-target-sound-extraction|Binaural Target Sound Extraction]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
