---
type: concept
created: 2026-04-12
updated: 2026-04-17
sources:
tags:
  - active-noise-control
  - headphone
  - audio-processing
---

# Transparency Mode

**Transparency Mode** (also known as HearThrough or Awareness Mode) is a headphone feature that allows external ambient sounds to pass through to the user's ears, effectively bypassing the physical and electronic isolation of ANC.

## Overview

Transparency mode is the inverse of ANC. Instead of generating anti-noise to cancel external sound, the headphone uses its microphones to capture external sound, processes it, and plays it back through the speakers. This allows users to stay aware of their surroundings or have conversations without removing their headphones.

## Key Technologies

### 1. Automatic Conversation Detection
Advanced systems can automatically toggle between ANC and Transparency Mode when a conversation is detected. This involves:
- **[[voice-activity-detection|Voice Activity Detection]] (VAD)**: Identifying when the wearer (OVAD) or a target person (TVAD) is speaking.
- **Adaptive Thresholds**: Learning a user's speaking patterns to prevent premature termination of transparency during pauses in a conversation (Masilamani 2024).
- **Mis-trigger Rejection**: Using machine learning and sensor fusion (accelerometers, bone conduction) to ignore non-speech sounds like coughing, chewing, or humming.

### 2. Directional Awareness
Using **[[beamforming|Beamforming]]** with multiple microphones to focus on the person speaking in front of the user while still suppressing background noise from other directions.

### 3. Spatialization
Processing the external sound so it feels natural and originates from its actual location in space (head-externalization), rather than sounding like it's inside the user's head.

### 4. Media Handling
During transparency mode, background media (music, podcasts) may be lowered in volume (**ducking**) or processed to remove vocals to improve conversation clarity.

## Implementation Challenges

- **Latency**: The path from microphone to speaker must be extremely fast (typically < 100 $\mu$s) to avoid comb-filtering effects with sound that leaks through the headphones naturally.
- **Naturalness**: Replicating the natural frequency response of the open ear, compensating for the **[[ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]**.
- **Wind Noise**: External microphones are highly sensitive to wind, which can cause unpleasant artifacts in transparency mode.

## Related Concepts

- [[active-noise-control|Active Noise Control]]
- [[voice-activity-detection|Voice Activity Detection]]
- [[beamforming|Beamforming]]
- [[ear-canal-occlusion-effect|Ear Canal Occlusion Effect]]
- [[../sources/fukumoto-2025-whisphone-paper-reading-note|Whisphone]]

## Related Sources

- [[../sources/masilamani-2024-headphone-conversation-detect-paper-reading-note|Masilamani 2024: Headphone Conversation Detect]]
- [[../sources/fukumoto-2025-whisphone-paper-reading-note|Fukumoto 2025: Whisphone Paper Reading Note]]
- [[../sources/benois-2020-hybrid-pseudo-cascaded-anc-headphones|Benois 2020: Hybrid and Pseudo-Cascaded ANC for Headphones]]
- [[../sources/lu-2024-headphone-speech-listening-ambient-noise|Lu 2024: Headphone Speech Listening]]
