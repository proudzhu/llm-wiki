---
type: concept
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/mohapatra-2026-localizing-conversation-partners-head-motion/full-text.md
  - raw/papers/miran-2026-imu-feedback-cancellation/full-text.txt
tags:
  - sensors
  - wearables
  - imu
---

# Inertial Measurement Unit

An **Inertial Measurement Unit (IMU)** is a sensor module that measures specific force, angular velocity, and sometimes magnetic field orientation of a body, commonly used in wearable devices for motion tracking.

## Overview

A typical IMU consists of:
- **3-axis gyroscope**: Measures angular velocity (rad/s) — used for rotational tracking
- **3-axis accelerometer**: Measures linear acceleration (m/s²) — used for gravitational reference and translational motion
- **Optional 3-axis magnetometer**: Measures magnetic field — provides absolute heading reference (9-axis IMU)

## IMU in Wearable Audio Devices

In smartglasses and hearing aids, IMUs serve as non-intrusive behavioral sensors:

| Device | IMU Location | Sampling Rate | Application |
|--------|-------------|---------------|-------------|
| Aria smartglasses | Right leg | 1000 Hz | Head orientation for conversation localization (Mohapatra et al. 2026) |
| BTE hearing aid | Behind-the-ear | — | Head movement detection for AFC step-size control (Miran et al. 2026) |

## IMU for Bone-Conduction Vibration Sensing

Beyond head motion tracking, IMU accelerometers in earables can capture subtle bone-conducted vibrations from the user's vocal tract (He et al. 2025). At typical IMU sampling rates (~1.6 kHz), the ~800 Hz bandwidth overlaps with the lower frequency range of human speech. This enables multi-modal speech enhancement where:

- The accelerometer provides noise-immune vibration signals dominated by the user's own voice.
- The microphone captures full-band but noisy audio.
- A fusion network combines both modalities for robust speech enhancement.

VibOmni (He et al. 2025) demonstrates this approach, achieving 21% PESQ improvement and 40% WER reduction across 32 volunteers. The system also models the transfer function from audio to vibration as a [[concepts/bone-conduction-function|Bone Conduction Function (BCF)]] for synthetic data augmentation.

## Advantages for Audio Applications

1. **Non-intrusive**: Does not require cameras or external tracking systems
2. **Low power**: Significantly less power consumption than visual modalities
3. **Privacy-preserving**: No visual data captured, suitable for social settings
4. **Always available**: Works in all lighting conditions and environments

## Limitations

1. **Drift**: Integration of gyroscope data accumulates error over time
2. **No absolute reference**: Without magnetometer, heading drifts; with magnetometer, magnetic interference can corrupt readings
3. **Limited translational accuracy**: Double integration of accelerometer data for position is unreliable
4. **Device-specific calibration**: Requires correction for bias, scale factor, and temperature effects

## Related Concepts

- [[concepts/head-orientation-from-imu|Head Orientation from IMUs]]
- [[concepts/acoustic-zones-of-interest|Acoustic Zones of Interest]]

## Related Sources

- [[sources/mohapatra-2026-localizing-conversation-partners-head-motion|Mohapatra et al. 2026: Localizing Conversation Partners Using Head Motion]]
- [[sources/miran-2026-imu-feedback-cancellation|Miran 2026: IMU-Based Acoustic Feedback Cancellation]]
