---
type: concept
created: 2026-05-03
updated: 2026-05-03
sources:
  - raw/papers/mohapatra-2026-localizing-conversation-partners-head-motion/full-text.md
  - raw/papers/miran-2026-imu-feedback-cancellation/full-text.txt
tags:
  - imu
  - sensors
  - head-orientation
  - wearables
---

# Head Orientation from IMUs

**Head orientation from IMUs** refers to the estimation of a wearer's head pose (azimuth and elevation angles) using inertial measurement units integrated into wearable devices such as smartglasses or hearing aids.

## Overview

Inertial Measurement Units (IMUs) typically contain a 3-axis gyroscope and a 3-axis accelerometer. For head orientation estimation, the gyroscope provides angular velocity measurements that can be integrated over time to track rotational changes. The accelerometer provides gravitational reference but is less commonly used for orientation in this context due to sensitivity to linear acceleration.

## Quaternion-Based Attitude Propagation

The standard approach integrates angular velocity using quaternion representation. Given angular velocity $\boldsymbol{\omega} = [\omega_x, \omega_y, \omega_z]^T$ sampled at intervals $\Delta t$, the quaternion update is:

$$\mathbf{q}_{t+1} = \left[\cos\left(\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\mathbf{I}_4 + \frac{1}{\|\boldsymbol{\omega}\|}\sin\left(\frac{\|\boldsymbol{\omega}\|\Delta t}{2}\right)\boldsymbol{\Omega}(\boldsymbol{\omega})\right]\mathbf{q}_t$$

where $\boldsymbol{\Omega}(\boldsymbol{\omega})$ is the skew-symmetric operator:

$$\boldsymbol{\Omega}(\boldsymbol{\omega}) = \begin{bmatrix} 0 & -\boldsymbol{\omega}^T \\ \boldsymbol{\omega} & -[\boldsymbol{\omega}]_\times \end{bmatrix}$$

The resulting rotation matrix is then transformed to spherical coordinates (azimuth, elevation) with the front-facing direction as origin.

## Key Challenges

1. **Sensor drift**: Gyroscope integration accumulates error over time. For short observation windows (e.g., 30 seconds), drift remains acceptable. Bland-Altman analysis shows 95% of IMU measurements fall within ±1.96 SD of OptiTrack ground truth (Mohapatra et al. 2026).
2. **No translational motion**: Double integration of accelerometer data for position estimation is error-prone. For seated conversations, translational motion offers limited value.
3. **Device-dependent calibration**: Bias instability, scale factor errors, and temperature coefficients require device-specific correction. Short observation windows mitigate this.
4. **Clock drift**: Between devices, corrected via cross-correlation of short-term audio signals.

## Applications in Audio Systems

| Application | Paper | Use |
|-------------|-------|-----|
| Acoustic zone localization | Mohapatra et al. 2026 | Infer conversation partner locations from head-orienting patterns |
| Acoustic feedback cancellation | Miran et al. 2026 | Control AFC step size based on head movement acceleration |

## Related Concepts

- [[concepts/acoustic-zones-of-interest|Acoustic Zones of Interest]]
- [[concepts/inertial-measurement-unit|Inertial Measurement Unit]]
- [[concepts/voice-activity-detection|Voice Activity Detection]]
- [[concepts/beamforming|Beamforming]]

- [[concepts/direction-dependent-acoustic-parameters|Direction-Dependent Acoustic Parameters]]

## Related Sources

- [[sources/mohapatra-2026-localizing-conversation-partners-head-motion|Mohapatra et al. 2026: Localizing Conversation Partners Using Head Motion]]
- [[sources/miran-2026-imu-feedback-cancellation|Miran 2026: IMU-Based Acoustic Feedback Cancellation]]
- [[sources/goetz-2026-blind-direction-dependent-acoustic-parameter-estimation|Görtz et al. 2026: Blind DDAP Estimation Using Smart Glasses]]
