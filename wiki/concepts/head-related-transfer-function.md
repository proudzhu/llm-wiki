---
type: concept
created: 2026-09-27
updated: 2026-10-31
sources:
  - raw/papers/veluri-2023-semantic-hearing/full-text.md
  - raw/papers/kuo-2006-anc-headphones/full-text.txt
tags:
  - acoustics
  - spatial-audio
  - hrtf
---

# Head-Related Transfer Function (HRTF)

The **head-related transfer function** is the frequency-domain transfer function describing how a sound from a given direction is filtered by the listener's head, torso, and pinnae before reaching each eardrum. Its time-domain counterpart is the head-related impulse response (HRIR). Direction-dependent differences between the two ears' HRTFs give rise to the [[concepts/interaural-time-difference|interaural time difference]] and [[concepts/interaural-level-difference|interaural level difference]] cues used for spatial perception. HRTFs vary substantially across individuals (anthropometry) and are modified by devices worn on the head (see [[concepts/device-specific-hrtf|device-specific HRTF]]).

## HRTFs in Training-Data Synthesis

Because binaural ground truth is unobtainable in natural recordings, HRTF datasets are used to synthesize binaural training data: a mono source $x_k$ is convolved with the left- and right-ear impulse responses $h_{k,L}, h_{k,R}$ to produce the ear signals $s_L = \sum_k x_k * h_{k,L}$, $s_R = \sum_k x_k * h_{k,R}$. Veluri et al. (2023) use the CIPIC HRTF dataset (non-reverberant, per-subject) augmented with measured (SBSBRIR, RRBRIR) and simulated (CATT RIR) binaural room impulse responses to also capture reverberation and multipath; splitting datasets across subjects and rooms lets the network generalize to unseen listeners and environments. Related per-device transfer functions are studied in [[concepts/device-specific-hrtf|device-specific HRTF]] for ANC design.

## Pinna Spectral Filtering for Error-Microphone Placement

The pinna's contribution to the HRTF also shapes the **secondary path** of a feedback-ANC headphone — the loudspeaker-to-error-microphone transfer function inside the ear-cup. [[sources/kuo-2006-anc-headphones|Kuo, Mitra & Gan 2006]] measured $S(z)$ at eight error-microphone positions around the ear-pad and found responses grouped by ear anatomy: positions over the posterior folded rim of skin/cartilage (#1–#4) differed markedly from those over the anterior multi-fold hollow (#5–#8, similar among themselves), with the flattest $|S(z)|$ near the external auditory meatus (#8). Because the feedback-optimal controller is $W^{opt}(z) = P(z)/S(z)$, dips in $|S(z)|$ translate directly into instability — making pinna-induced spectral filtering a design variable for error-sensor placement, not just a spatial-hearing phenomenon. The #8 response also matched the KEMAR ear-canal microphone, i.e. the perceptual target.

## Related Concepts

- [[concepts/interaural-time-difference|Interaural Time Difference (ITD)]]
- [[concepts/interaural-level-difference|Interaural Level Difference (ILD)]]
- [[concepts/device-specific-hrtf|Device-Specific HRTF]]
- [[concepts/binaural-target-sound-extraction|Binaural Target Sound Extraction]]

## Related Sources

- [[sources/veluri-2023-semantic-hearing|Veluri et al. 2023: Semantic Hearing]]
- [[sources/kuo-2006-anc-headphones|Kuo, Mitra & Gan 2006: Active Noise Control System for Headphone Applications]] — pinna spectral filtering as the mechanism guiding error-microphone placement in feedback-ANC headphones
