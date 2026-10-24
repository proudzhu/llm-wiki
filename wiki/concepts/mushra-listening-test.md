---
type: concept
created: 2026-10-24
updated: 2026-10-24
sources:
  - raw/papers/mezza-2024-hybrid-plc/full-text.md
tags:
  - evaluation-metric
  - listening-test
  - audio-quality
  - subjective-evaluation
---

# MUSHRA Listening Test

**MUltiple Stimuli with Hidden Reference and Anchor (MUSHRA)** is the ITU-R BS.1534 standard subjective test for intermediate-quality audio systems. Listeners rate several test items against a *hidden reference* (scored 100 by construction) and one or more *anchors* (e.g. a 3.5 kHz low-pass, or in PLC studies zero-filling), on a 0–100 scale, in a single session with free switching between stimuli.

## Protocol Essentials (ITU-R BS.1534-3)

- **Hidden reference** — the untampered signal is included among the stimuli; listeners are instructed to identify it and score it 100.
- **Anchor(s)** — a known-bad condition fixes the bottom of the scale; listeners must give it the lowest score.
- **Post-screening** — an assessor who rates the hidden reference below 90 for more than 15% of the test items is excluded from the aggregate.
- Both mean scores (with standard deviation) and box-and-whisker distributions are reported; **spread** is itself informative — a method with low inter-listener variance shows stronger agreement about its quality.

## Use in PLC Research for Music

Speech PLC papers normally use CMOS/MOS ACR crowdsourcing ([[concepts/pesq|P.808]]). Music-oriented work switches to MUSHRA because the impairments (clicks at packet seams, timbral splintering, loss of harmonic continuity) are intermediate-quality artifacts, and because trained listeners are required to resolve them. [[sources/mezza-2024-hybrid-plc|Mezza et al. 2024]] use a MUSHRA test with 15 musically trained assessors (one excluded by post-screening), 5 × 10-s piano excerpts, 8 PLC methods, and losses of 10 ms every 100 ms; the hidden reference and the zero-filling anchor are both present. In that study MUSHRA is the arbiter that separates the objective proxies: PEAQ ($r=0.957$) and PLCMOS ($r=0.899$) track the mean opinion scores, NMSE correlates significantly ($r=-0.725$), while mel-spectral convergence does not ($r=0.437$, not significant).

## Related Concepts

- [[concepts/peaq|PEAQ]] — objective perceptual audio quality metric validated against such tests
- [[concepts/plcmos|PLCMOS]] — speech-trained objective proxy for MOS
- [[concepts/pesq|PESQ]] — speech-specific objective metric (ITU-T P.862)
- [[concepts/networked-music-performance|Networked Music Performance]] — the domain where MUSHRA replaces CMOS
- [[concepts/packet-loss-concealment|Packet Loss Concealment]]

## Related Sources

- [[sources/mezza-2024-hybrid-plc|Mezza, Amerena, Bernardini & Sarti 2024]] — music-PLC MUSHRA protocol with hidden reference and zero-fill anchor; PARCnet leads by 21.7 points over AR(128) with the smallest spread
