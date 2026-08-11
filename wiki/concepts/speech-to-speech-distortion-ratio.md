---
type: concept
created: 2026-08-11
updated: 2026-08-11
sources:
  - raw/papers/fang-2020-robust-residual-echo-suppression/full-text.md
tags:
  - evaluation-metric
  - residual-echo-suppression
  - double-talk
  - speech-distortion
---

# Speech-to-Speech-Distortion power Ratio (SSDR)

Speech-to-Speech-Distortion power Ratio (SSDR) is an objective metric for evaluating near-end speech distortion during **double talk** in acoustic echo cancellation / residual echo suppression systems. Unlike [[concepts/echo-return-loss-enhancement|ERLE]], which is only meaningful in single talk, SSDR quantifies how much the RES gain distorts the desired near-end speech.

## Key Formulations

$$\mathrm{SSDR} = 10\log_{10}\frac{\sum_{n=0}^{N_{DT}-1}|s[n]|^2}{\sum_{n=0}^{N_{DT}-1}|s[n] - e[n]|^2},$$

where $s[n]$ is the clean reference near-end speech, $e[n]$ is the system output, and $N_{DT}$ is the number of samples in the double-talk (DTD) segment. Higher SSDR (in dB) means less near-end speech distortion.

### Interpretation

- SSDR is computed **only over the double-talk region**, where both near-end speech and echo are active. This is the most demanding condition for an RES system: the gain must suppress echo while preserving the near-end speech overlapped in time and frequency.
- A system that applies an aggressive gain (strong echo suppression) tends to lower SSDR (more near-end distortion); a system that preserves near-end speech tends to leave more residual echo. The trade-off between ERLE and SSDR is the central design tension of RES.
- A method that improves **both** ERLE and SSDR simultaneously — as claimed by [[sources/fang-2020-robust-residual-echo-suppression|Fang 2020]] — is desirable because it breaks the usual trade-off.

### Relationship to ERLE

| Metric | Condition | Captures |
|--------|-----------|----------|
| [[concepts/echo-return-loss-enhancement\|ERLE]] | Single talk (far-end only) | Echo attenuation |
| **SSDR** | Double talk (near-end + echo) | Near-end speech preservation |

A complete RES evaluation reports both, since optimizing one in isolation can degrade the other.

## Related Concepts

- [[concepts/echo-return-loss-enhancement|Echo Return Loss Enhancement (ERLE)]] — the complementary single-talk metric.
- [[concepts/residual-echo-suppression|Residual Echo Suppression]] — the system SSDR evaluates.

## Related Sources

- [[sources/fang-2020-robust-residual-echo-suppression|Fang 2020]] — uses SSDR to show the proposed correlation-based RES introduces less near-end distortion than a slow-attach-fast-decay baseline (4.83 vs 4.68 dB) while also improving ERLE.
