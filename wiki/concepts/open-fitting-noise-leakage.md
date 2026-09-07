---
type: concept
created: 2026-09-07
updated: 2026-09-07
sources:
  - raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/full-text.md
tags:
  - hearing-aids
  - noise-reduction
  - active-noise-control
  - speech-enhancement
---

# Open-Fitting Noise Leakage

**Open-fitting noise leakage** is the ambient noise that enters the ear canal directly through an open hearing-aid fitting (no earmold), bypassing all hearing-aid processing. Because no direct processing can be applied to this signal, its SNR is generally lower than that of the signal provided by the hearing aid, and it can override the action of the noise reduction (NR) performed in the device.

## Context: Why Open Fittings

Open fittings remove the earmold, which reduces the [[concepts/ear-canal-occlusion-effect|occlusion effect]] and improves physical comfort. Their viability grew with more efficient feedback control schemes and fast signal processing units. The price is that the leakage contribution can no longer be neglected, while conventional NR algorithms (GSC, [[concepts/multi-channel-wiener-filter|MWF]]) ignore it entirely.

## Effect on Noise Reduction Performance

The signal reaching the tympanic membrane combines:

- the NR output, amplified by gain $g$ and *attenuated* by the secondary path $S$ (loudspeaker → tympanic membrane, with dc gain < 1), and
- the unprocessed leakage, with its own speech and noise components.

For small amplification gains — precisely the regime where open fittings are used — the leakage can dominate the output SNR, partly canceling the NR improvement. [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel et al. 2010]] quantified this on manikin measurements: with leakage only, MWF-NR degradation remains small down to gains of 10 dB, but with *both* leakage and secondary path the degradation is significant for gains up to at least 20 dB.

![[raw/papers/serizel-2010-integrated-anc-nr-hearing-aids/figures/crop-p08-006.png|Performance comparison for a Multichannel Wiener Filter noise reduction scheme depending on leakage and secondary path]]

*Figure 7 from Serizel et al. 2010: MWF NR performance versus amplification gain, for leakage only and leakage + secondary path.*

## Remedy: Active Noise Control at the Tympanic Membrane

Since the leakage cannot be processed, its *noise component* can instead be canceled physically by feedforward [[concepts/active-noise-control|ANC]], generating a zone of quiet at the tympanic membrane based on an error signal from an ear-canal microphone. The leakage *speech* component is deliberately preserved — it carries localization cues. Combination topologies range from cascaded NR+ANC (whose NR delay consumes the ANC [[concepts/causality|causality margin]]) to the integrated [[concepts/filtered-x-mwf|Filtered-x MWF]], which cancels the leakage noise while compensating the secondary path, without an NR/ANC performance trade-off.

## Related Concepts

- [[concepts/filtered-x-mwf|Filtered-x MWF (FxMWF)]]
- [[concepts/active-noise-control|Active Noise Control]]
- [[concepts/multi-channel-wiener-filter|Multi-Channel Wiener Filter]]
- [[concepts/secondary-path-modeling|Secondary Path Modeling]]
- [[concepts/ear-canal-occlusion-effect|Ear-Canal Occlusion Effect]]
- [[concepts/causality|Causality in ANC]]
- [[concepts/hearing-aid-feedback-cancellation|Hearing-Aid Feedback Cancellation]] — the enabling technology behind open fittings

## Related Sources

- [[sources/serizel-2010-integrated-anc-nr-hearing-aids|Serizel, Moonen, Wouters & Jensen 2010: Integrated Active Noise Control and Noise Reduction in Hearing Aids]]
