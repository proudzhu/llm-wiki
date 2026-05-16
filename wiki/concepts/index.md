# Concepts

> Pages about ideas, theories, methods, and abstract topics.

| Page | Summary | Created |
|------|---------|---------|
| [[concepts/signal-processing\|Signal Processing]] | Mathematical foundation for acoustic signal analysis | 2026-04-22 |
| [[concepts/mclp\|MCLP]] | Multi-Channel Linear Prediction for dereverberation | 2026-04-22 |
| [[concepts/llm-wiki-pattern\|LLM Wiki Pattern]] | The core idea of using LLMs to incrementally build and maintain a persistent wiki knowledge base | 2026-04-10 |
| [[concepts/branch-cuts\|Branch Cuts]] | How multi-valued complex functions are made single-valued by removing a curve from the domain | 2026-04-10 |
| [[concepts/symbolic-computation\|Symbolic Computation]] | Algorithms for exact manipulation of mathematical expressions; CAS simplification challenges | 2026-04-10 |
| [[concepts/virtual-sensing\|Virtual Sensing]] | Estimating noise at a location without a physical sensor using state-space observers | 2026-04-17 |
| [[concepts/ai-skill-formation\|AI Skill Formation]] | How AI assistance affects new skill acquisition; RCT shows 17% mastery decrease with cognitive offloading | 2026-04-11 |
| [[concepts/active-noise-control\|Active Noise Control]] | Cancelling noise by generating anti-noise of equal amplitude and opposite phase | 2026-04-10 |
| [[concepts/filtered-x-lms-algorithm\|Filtered-x LMS Algorithm]] | The standard adaptive algorithm for ANC, accounting for the secondary path | 2026-04-10 |
| [[concepts/leaky-fxlms-algorithm\|Leaky FxLMS Algorithm]] | FxLMS variant with leakage coefficient to limit filter gain and improve stability | 2026-04-10 |
| [[concepts/adjoint-lms-algorithm\|Adjoint LMS Algorithm]] | Filters error signal instead of reference; 10× computational savings in multichannel ANC | 2026-04-28 |
| [[concepts/internal-model-control\|Internal Model Control]] | Control structure used in adaptive feedback ANC to regenerate a reference signal | 2026-04-10 |
| [[concepts/simplified-adaptive-feedback-anc\|Simplified Adaptive Feedback ANC]] | Uses error signal directly as reference, eliminating IMC's convolution operation | 2026-04-10 |
| [[concepts/broad-band-feedforward-anc\|Broad-Band Feedforward ANC]] | Standard ANC architecture using upstream reference microphone with FXLMS algorithm | 2026-04-10 |
| [[concepts/narrow-band-feedforward-anc\|Narrow-Band Feedforward ANC]] | Uses internally generated sinusoidal references (tachometer), no feedback problem | 2026-04-10 |
| [[concepts/multi-channel-anc\|Multi-Channel ANC]] | Extends ANC to multiple sensors/sources using multichannel FxLMS, O(M·L·N) complexity | 2026-04-10 |
| [[concepts/acoustic-feedback\|Acoustic Feedback]] | Anti-noise radiating upstream to reference microphone; solutions include neutralization and IIR filters | 2026-04-10 |
| [[concepts/adaptive-feedback-control\|Adaptive Feedback Control]] | Feedback ANC systems that adapt automatically — IMC-based and simplified architectures | 2026-04-10 |
| [[concepts/online-secondary-path-modeling\|Online Secondary-Path Modeling]] | Identifying S(z) during ANC operation via auxiliary noise injection | 2026-04-10 |
| [[concepts/deep-learning-for-signal-processing\|Deep Learning for Signal Processing]] | Neural networks replacing or augmenting TSP algorithms for nonlinearity and robustness | 2026-04-17 |
| [[concepts/complex-analysis\|Complex Analysis]] | Mathematical foundation for branch cuts, analytic continuation, and CAS behavior | 2026-04-10 |
| [[concepts/analytic-continuation\|Analytic Continuation]] | Extending analytic functions beyond their original domain via branch cuts | 2026-04-10 |
| [[concepts/offline-secondary-path-modeling\|Offline Secondary-Path Modeling]] | Identifying S(z) during a training phase before ANC operation begins | 2026-04-11 |
| [[concepts/frequency-domain-anc\|Frequency-Domain ANC]] | FFT-based block processing for efficient long-filter ANC | 2026-04-11 |
| [[concepts/subband-anc\|Subband ANC]] | Per-subband adaptive filtering with independent optimization | 2026-04-11 |
| [[concepts/correntropy\|Correntropy]] | Nonlinear local similarity measure in kernel space; robust to outliers via Gaussian kernel | 2026-04-12 |
| [[concepts/generalized-correntropy\|Generalized Correntropy]] | GGD-kernel correntropy with shape parameter α; GMCC algorithm with zero POD | 2026-04-12 |
| [[concepts/maximum-correntropy-criterion\|Maximum Correntropy Criterion]] | Gaussian-kernel correntropy as optimization criterion; exponential outlier suppression | 2026-04-12 |
| [[concepts/generalized-gaussian-distribution\|Generalized Gaussian Distribution]] | Parametric distribution family (Laplace↔Gaussian↔Uniform) via shape parameter α | 2026-04-12 |
| [[concepts/information-theoretic-learning\|Information Theoretic Learning]] | Entropy/correntropy-based optimization; all-order statistics via kernel embedding | 2026-04-12 |
| [[concepts/robust-adaptive-filtering\|Robust Adaptive Filtering]] | Adaptive algorithms for non-Gaussian/impulsive noise; score function comparison | 2026-04-12 |
| [[concepts/feedback-anc\|Feedback ANC]] | ANC using error sensor only (no reference mic); IMC-based or simplified architectures | 2026-04-12 |
| [[concepts/feedforward-anc\|Feedforward ANC]] | ANC using upstream reference microphone; standard FXLMS architecture | 2026-04-12 |
| [[concepts/hybrid-anc\|Hybrid ANC]] | Combining feedforward + feedback ANC structures for improved performance | 2026-04-12 |
| [[concepts/minimum-variance-control\|Minimum Variance Control]] | Optimal control minimizing output variance; foundation for IMC-based ANC | 2026-04-12 |
| [[concepts/wiener-filter\|Wiener Filter]] | Optimal linear filter minimizing MSE; foundation for MWF and optimal control | 2026-04-12 |
| [[concepts/model-predictive-control\|Model Predictive Control]] | Rolling-horizon optimization with explicit constraint handling; applied to ANC | 2026-04-12 |
| [[concepts/state-space-model\|State-Space Model]] | System representation via state variables; used in MPC and modern control | 2026-04-12 |
| [[concepts/system-identification\|System Identification]] | Estimating system models from data; vector fitting for state-space extraction | 2026-04-12 |
| [[concepts/active-vibration-control\|Active Vibration Control]] | ANC applied to structural vibration; similar control architecture | 2026-04-12 |
| [[concepts/quadratic-programming\|Quadratic Programming]] | Optimization with quadratic objective and linear constraints; MPC solver | 2026-04-12 |
| [[concepts/kalman-filter\|Kalman Filter]] | Optimal state estimation for linear systems with Gaussian noise | 2026-04-12 |
| [[concepts/impulsive-noise\|Impulsive Noise]] | Non-Gaussian noise with heavy-tailed distribution; requires robust algorithms | 2026-04-12 |
| [[concepts/kernel-methods\|Kernel Methods]] | Nonlinear mapping to reproducing kernel Hilbert space; basis for correntropy | 2026-04-12 |
| [[concepts/renyi-entropy\|Rényi Entropy]] | Generalized entropy measure parameterized by order; used in ITL | 2026-04-12 |
| [[concepts/generalized-maximum-correntropy-criterion\|Generalized Maximum Correntropy Criterion]] | GGD-kernel MCC with shape parameter p; robust to impulsive noise | 2026-04-12 |
| [[concepts/transparency-mode\|Transparency Mode]] | Headphone mode allowing external sound passthrough for conversation awareness | 2026-04-12 |
| [[concepts/voice-activity-detection\|Voice Activity Detection]] | Detecting speech presence; used for conversation detection in headphones | 2026-04-12 |
| [[concepts/beamforming\|Beamforming]] | Microphone array spatial filtering for directional sound capture | 2026-04-12 |
| [[concepts/bone-conduction\|Bone Conduction]] | Sound transmission through skull bone; used for whisper input detection | 2026-04-12 |
| [[concepts/ear-canal-occlusion-effect\|Ear Canal Occlusion Effect]] | Low-frequency boom when ear canal is blocked; relevant for in-ear ANC | 2026-04-12 |
| [[concepts/whispering-speech-recognition\|Whispering Speech Recognition]] | ASR for whispered speech; input modality for earbud-based interaction | 2026-04-12 |
| [[concepts/backpropagation-through-time\|Backpropagation Through Time]] | Standard RNN training algorithm; unrolls through time for gradient computation | 2026-04-12 |
| [[concepts/real-time-recurrent-learning\|Real-Time Recurrent Learning]] | Online RNN training without unrolling; exact gradients at each step | 2026-04-12 |
| [[concepts/linear-recurrent-unit\|Linear Recurrent Unit]] | Efficient RNN cell with linear recurrence; avoids vanishing/exploding gradients | 2026-04-12 |
| [[concepts/secondary-path-modeling\|Secondary Path Modeling]] | Identifying S(z) transfer function; essential for FXLMS stability | 2026-04-17 |
| [[concepts/socp-optimization\|SOCP Optimization]] | Convex optimization for robust control under norm-bounded uncertainties | 2026-04-19 |
| [[concepts/floating-point-comparison\|Floating-point Comparison]] | When and how to compare floats; pitfalls of universal epsilons | 2026-04-18 |
| [[concepts/ieee-754\|IEEE 754]] | The industry standard for deterministic floating-point arithmetic | 2026-04-18 |
| [[concepts/neural-networks\|Neural Networks]] | Three generations of NNs: perceptrons, ANNs/DNNs, SNNs; rate-based vs spike-based computation | 2026-04-25 |
| [[concepts/spectrogram-analysis\|Spectrogram Analysis]] | Placeholder for spectrogram analysis fundamentals | 2026-04-18 |
| [[concepts/adaptive-filtering\|Adaptive Filtering]] | Placeholder for adaptive filtering fundamentals | 2026-04-18 |
| [[concepts/numerical-stability\|Numerical Stability]] | Placeholder for numerical stability fundamentals | 2026-04-18 |
| [[concepts/spatial-coherence\|Spatial Coherence]] | Multi-channel signal correlation for separating coherent sources from diffuse sound fields | 2026-04-25 |
| [[concepts/spiking-neural-networks\|Spiking Neural Networks]] | Third-generation neural networks using spike-based computation; energy-efficient, temporally coded | 2026-04-25 |
| [[concepts/neuromorphic-computing\|Neuromorphic Computing]] | Brain-inspired hardware (TrueNorth, Loihi, SpiNNaker) for energy-efficient SNN deployment | 2026-04-25 |
| [[concepts/spike-timing-dependent-plasticity\|Spike-Timing-Dependent Plasticity]] | Unsupervised Hebbian learning rule based on pre/post-spike timing; key SNN training mechanism | 2026-04-25 |
| [[concepts/convolutional-recurrent-network\|Convolutional Recurrent Network]] | Encoder-LSTM-decoder architecture combining CNN feature extraction with RNN temporal modeling for real-time audio | 2026-04-25 |
| [[concepts/complex-spectrum-mapping\|Complex Spectrum Mapping]] | Joint estimation of real/imaginary STFT components for precise phase control in ANC | 2026-04-25 |
| [[concepts/speech-preserving-anc\|Speech-Preserving ANC]] | Selective noise cancellation that preserves speech via algebraic cancellation in the loss function | 2026-04-25 |
| [[concepts/image-source-method\|Image Source Method]] | Classical algorithm for simulating room acoustics via virtual mirror sound sources (RIR generation) | 2026-04-25 |
| [[concepts/extended-kalman-filter\|Extended Kalman Filter]] | Nonlinear Kalman filter variant that linearizes via Jacobians at each time step | 2026-04-25 |
| [[concepts/uncertainty-modeling-for-anc\|Uncertainty Modeling for ANC]] | How plant variations are abstracted into mathematical sets for robust controller design | 2026-04-26 |
| [[concepts/convex-hull-uncertainty-model\|Convex Hull Uncertainty Model]] | Minimal-area contiguous uncertainty model using polyhedral geometry; ~60% of disk area | 2026-04-26 |
| [[concepts/elliptic-uncertainty-model\|Elliptic Uncertainty Model]] | Ellipse-shaped uncertainty model capturing elongated variations; ~60-70% of disk area | 2026-04-26 |
| [[concepts/robust-stability-constraint\|Robust Stability Constraint]] | Mathematical condition guaranteeing feedback stability for all plant variations in an uncertainty set | 2026-04-26 |
| [[concepts/causality\|Causality in ANC]] | Anti-noise must arrive at the cancellation point no later than the primary noise; delay limits broadband ANC bandwidth | 2026-04-26 |
| [[concepts/deep-secondary-path-estimation\|Deep Secondary Path Estimation]] | Neural network prediction of secondary path in real time, replacing iterative adaptation with frame-level inference | 2026-04-27 |
| [[concepts/variable-step-size-lms\|Variable Step Size LMS]] | Dynamically adjusting LMS step size; Akhtar's inverse strategy (small→large) exploits decreasing disturbance in online SPM | 2006 |
| [[concepts/roi-beamforming\|Region-of-Interest Beamforming]] | Spatial filtering preserving signals from a region rather than single DOA; time-domain superior for smart glasses | 2026-04-28 |
| [[concepts/multi-channel-speech-enhancement\|Multi-Channel Speech Enhancement]] | Multi-microphone speech enhancement exploiting spatial information; linear, data-driven, and hybrid approaches | 2026-04-29 |
| [[concepts/variable-span-linear-filter\|Variable Span Linear Filter]] | Generalized linear filtering framework with controllable speech distortion vs noise reduction tradeoff; MWF/MVDR as special cases | 2026-04-29 |
| [[concepts/multi-channel-wiener-filter\|Multi-Channel Wiener Filter]] | Optimal linear filter minimizing MSE across multiple channels; VSLF special case with μ=1, Q=M | 2026-04-29 |
| [[concepts/mvdr-beamformer\|MVDR Beamformer]] | Minimum variance distortionless response beamformer; VSLF special case with μ=0, Q=rank(Φ_x) | 2026-04-29 |
| [[concepts/spatial-covariance-matrix\|Spatial Covariance Matrix]] | Second-order statistics of multi-channel signals; core quantity for MWF, MVDR, VSLF weight computation | 2026-04-29 |
| [[concepts/generalized-eigenvalue-decomposition\|Generalized Eigenvalue Decomposition]] | Joint diagonalization of speech and noise SCMs; foundation for VSLF framework | 2026-04-29 |
| [[concepts/remote-microphone-technique\|Remote Microphone Technique]] | Virtual sensing using fixed compensation filter derived from transfer functions between physical and virtual locations | 2026-04-29 |
| [[concepts/variance-ratio-estimation\|Variance Ratio Estimation]] | Decomposing normalized SCM into linear combination of coherence matrices; multiplicative update with KL regularization | 2026-04-30 |
| [[concepts/selective-fixed-filter-anc\|Selective Fixed-Filter ANC]] | Pre-trained filter library with real-time selection; variants include SFANC, D-SFANC, PD-SFANC, DFG-SFANC, GFANC | 2026-04-30 |
| [[concepts/direction-of-arrival-estimation\|Direction-of-Arrival Estimation]] | Determining signal arrival direction at sensor arrays; CRNN-based prediction for ANC | 2026-04-30 |
| [[concepts/moving-source-tracking\|Moving Source Tracking]] | Continuous DoA estimation for non-stationary sources; predictive vs reactive approaches | 2026-04-30 |
| [[concepts/frequency-response-matching\|Frequency Response Matching]] | Non-neural filter selection for SFANC by comparing estimated primary path response against pre-trained profiles | 2026-05-01 |
| [[concepts/lagrange-interpolation\|Lagrange Interpolation]] | Polynomial interpolation via Lagrange basis functions; unique degree-n polynomial through n+1 distinct points | 2026-05-02 |
| [[concepts/vandermonde-matrix\|Vandermonde Matrix]] | Geometric progression matrix with known determinant; arises in polynomial interpolation but is ill-conditioned | 2026-05-02 |
| [[concepts/acoustic-howling-suppression\|Acoustic Howling Suppression]] | Preventing positive feedback loops in audio amplification systems; AFC, deep learning, and NN-augmented Kalman filter approaches | 2026-05-02 |
| [[concepts/frequency-domain-kalman-filter\|Frequency-Domain Kalman Filter]] | Frequency-domain Kalman filter variant for acoustic echo/howling suppression with per-frequency-bin state updates | 2026-05-02 |
| [[concepts/asymptotic-analysis-adaptive-algorithms\|Asymptotic Analysis of Adaptive Algorithms]] | Weak convergence and ODE method for characterizing almost sure behavior and limiting distribution of adaptive filter estimates | 2026-05-03 |
| [[concepts/generative-fixed-filter-anc\|Generative Fixed-Filter ANC]] | Neural co-processor generates custom ANC filters via sub-filter recombination (GFANC) or direct coefficient regression (E2E-CFG) | 2026-05-04 |
| [[concepts/end-to-end-differentiable-anc\|End-to-End Differentiable ANC]] | Training paradigm integrating co-processor and ANC path in one differentiable graph; unsupervised via residual error | 2026-05-04 |
| [[concepts/device-specific-hrtf\|Device-Specific HRTF (DHRTF)]] | HRTF measured through headphone microphones; captures DOA-dependent primary path for ANC | 2026-05-05 |
| [[concepts/primary-path-variability\|Primary Path Variability]] | DOA-induced changes in the primary path P(z) that degrade feedforward ANC performance | 2026-05-05 |
| [[concepts/anc-attenuation-bounds\|ANC Attenuation Bounds]] | Analytical limits on achievable attenuation given magnitude/phase deviation; 20 dB requires <0.83 dB and <5.76° | 2026-05-05 |
| [[concepts/direction-dependent-acoustic-parameters\|Direction-Dependent Acoustic Parameters]] | Acoustic quantities varying with observation direction; essential for realistic AAR rendering | 2026-05-05 |
| [[concepts/spherical-harmonic-transform\|Spherical Harmonic Transform]] | Decomposition of spherical functions into SH coefficients; compact spatial representation for acoustics | 2026-05-05 |
| [[concepts/auditory-augmented-reality\|Auditory Augmented Reality]] | Rendering virtual sound sources in real acoustic environments; requires directional acoustic parameter knowledge | 2026-05-05 |
| [[concepts/dynamic-time-warping\|Dynamic Time Warping]] | Optimal nonlinear alignment of temporal sequences; applied to impulse response interpolation and ANC secondary path alignment | 2026-05-06 |
| [[concepts/secondary-path-interpolation\|Secondary Path Interpolation]] | Estimating secondary paths at unmeasured positions via interpolation; DTW-based method extends stable frequency range for moving listeners | 2026-05-06 |
| [[concepts/bcs-guided-speech-enhancement\|BCS-Guided Speech Enhancement]] | Multi-modal fusion of bone-conducted and air-conducted signals for speech enhancement; Conformer-based architecture with VAD gating | 2026-05-06 |
| [[concepts/diagonal-loading\|Diagonal Loading]] | Regularization for adaptive beamforming: adds μI to SCM before inversion to bound condition number | 2026-05-07 |
| [[concepts/kantorovich-inequality\|Kantorovich Inequality]] | Bounds Rayleigh quotient ratio by condition number; maps WNG to κ_max in beamforming | 2026-05-07 |
| [[concepts/white-noise-gain\|White Noise Gain (WNG)]] | Beamformer robustness metric: W = 1/‖w‖²; collapses under snapshot deficiency | 2026-05-07 |
| [[concepts/mpdr-beamformer\|MPDR Beamformer]] | Minimizes total output power with distortionless constraint; sensitive to snapshot deficiency | 2026-05-07 |
| [[concepts/gsc-beamformer\|Generalized Sidelobe Canceller (GSC)]] | Orthogonalized LCMV beamformer: fixed quiescent path + adaptive noise cancellation path | 2026-05-07 |
| [[concepts/condition-number\|Condition Number]] | Matrix sensitivity metric κ = λ_max/λ_min; controls WNG via Kantorovich inequality | 2026-05-07 |
| [[concepts/gershgorin-circle-theorem\|Gershgorin Circle Theorem]] | Eigenvalue bounds via diagonal dominance; O(M²) alternative to exact EVD for DL | 2026-05-07 |
| [[concepts/virtual-microphone-estimation\|Virtual Microphone Estimation]] | Estimating signals at absent microphone positions from real measurements; decouples spatial from spectral enhancement | 2026-05-12 |
| [[concepts/spatial-audio-representation-learning\|Spatial Audio Representation Learning]] | SARL framework: conditions MC-SE on VM signals (SARL-S) or features (SARL-F) for improved spatial diversity | 2026-05-12 |
| [[concepts/neural-directional-filtering\|Neural Directional Filtering]] | Data-driven VDM reconstruction using DNNs to learn ideal directional microphone behavior on compact arrays | 2026-05-13 |
| [[concepts/virtual-directional-microphone\|Virtual Directional Microphone]] | Computationally synthesized microphone with specified directivity pattern reconstructed from array recordings | 2026-05-13 |
| [[concepts/diffuse-sound-extraction\|Diffuse Sound Extraction]] | Isolating late reverberant diffuse component for spatial audio control and immersive quality | 2026-05-13 |
| [[concepts/directivity-pattern\|Directivity Pattern]] | Directional sensitivity characterization of beamformers/microphones; Cardioid, hypercardioid, etc. | 2026-05-13 |
| [[concepts/fixed-beamformer\|Fixed Beamformer]] | Time-invariant spatial filtering; DMA, superdirective, delay-and-sum | 2026-05-13 |
| [[concepts/differential-microphone-array\|Differential Microphone Array]] | Spatial difference-based beamforming with frequency-invariant patterns; limited by array size | 2026-05-13 |
| [[concepts/room-transfer-function\|Room Transfer Function]] | Acoustic propagation characteristics between source and receiver in enclosed space | 2026-05-13 |
| [[concepts/room-impulse-response\|Room Impulse Response]] | Time-domain characterization of room acoustics; direct path, early reflections, late reverberation | 2026-05-13 |
| [[concepts/joint-nonlinear-filtering\|Joint Nonlinear Filtering]] | Neural architectures jointly processing spatial and temporal-spectral information; FT-JNF framework | 2026-05-13 |
| [[concepts/acoustic-zones-of-interest\|Acoustic Zones of Interest]] | Discretized spatial regions corresponding to conversation partner locations for smartglasses audio | 2026-05-03 |
| [[concepts/diffusion-models-for-speech\|Diffusion Models for Speech]] | Score-based generative modeling applied to speech enhancement via forward noise process | 2026-05-03 |
| [[concepts/drifting-models\|Drifting Models]] | Generative modeling as distributional equilibrium; native one-step generation without distillation | 2026-05-03 |
| [[concepts/head-orientation-from-imu\|Head Orientation from IMU]] | Estimating head pose (azimuth/elevation) using IMU sensors for conversation partner localization | 2026-05-03 |
| [[concepts/inertial-measurement-unit\|Inertial Measurement Unit]] | Sensor measuring specific force, angular velocity, and magnetic field orientation | 2026-05-03 |
| [[concepts/momentum-lms\|Momentum LMS]] | LMS with momentum term for faster convergence without sacrificing steady-state performance | 2026-05-03 |
| [[concepts/one-step-generative-models\|One-Step Generative Models]] | Single-function-evaluation generation eliminating iterative sampling of diffusion models | 2026-05-03 |
| [[concepts/online-learning\|Online Learning]] | Incremental model updates as data arrives; no need to store or revisit past data | 2026-05-03 |
| [[concepts/self-supervised-speech-representation\|Self-Supervised Speech Representation]] | Features learned from unlabeled speech corpora via self-supervised pre-training | 2026-05-03 |
| [[concepts/frequency-warping\|Frequency Warping]] | Non-uniform frequency resolution via all-pass delay substitution; enables low-order WFIR filters | 2026-05-13 |
| [[concepts/warped-fir-filter\|Warped FIR Filter]] | FIR filter in warped frequency domain; 16th order matches 128th FIR at low frequencies | 2026-05-13 |
| [[concepts/q-parameterization\|Q-Parameterization]] | Youla parameterization for stabilizing controller design; optimization over free Q parameter | 2026-05-13 |
| [[concepts/sensitivity-function\|Sensitivity Function]] | Closed-loop transfer function $S = 1/(1+CP)$; characterizes noise attenuation and waterbed effect | 2026-05-13 |
| [[concepts/teacher-forcing\|Teacher Forcing]] | Training strategy that feeds ground-truth previous outputs during recurrent learning; used to reformulate recursive AHS training | 2026-05-15 |
| [[concepts/self-attentive-recurrent-neural-network\|Self-Attentive Recurrent Neural Network]] | Recurrent + self-attention architecture used in Hybrid AHS for recursive speech enhancement | 2026-05-15 |
| [[concepts/prediction-error-method\|Prediction Error Method]] | De-correlation technique using whitening pre-filters to solve bias in closed-loop AFC | 2026-05-15 |
| [[concepts/hearing-aid-feedback-cancellation\|Hearing Aid Feedback Cancellation]] | AFC methods specific to hearing aids: PEM, FS, probe noise, and deep learning approaches | 2026-05-15 |
| [[concepts/densely-gated-convolutional-attention-network\|DenGCAN]] | Lightweight encoder-decoder with dense blocks, gated conv, sConformer bottleneck, AG skip-connections | 2026-05-16 |
| [[concepts/iterative-attentional-feature-fusion\|Iterative Attentional Feature Fusion (iAFF)]] | Coarse-then-refined multi-modal fusion using channel attention modules | 2026-05-16 |
| [[concepts/attention-gate\|Attention Gate (AG)]] | Selective skip-connection mechanism using local + global feature attention | 2026-05-16 |
| [[concepts/adaptive-time-frequency-attention\|Adaptive Temporal-Frequency Attention (ATFA)]] | Dual-axis MHSA over time and frequency with adaptive hierarchical fusion (AHA) for speech enhancement | 2026-05-16 |
| [[concepts/sensor-failure-robust-fusion\|Sensor-Failure Robust Multi-Modal Fusion]] | Random modality dropout training + dual-mask architecture for graceful degradation when one sensor is invalid | 2026-05-16 |
| [[concepts/frequency-shift-feedback-cancellation\|Frequency Shift Feedback Cancellation]] | De-correlation via small frequency offset; limited for HA but effective when combined with PEM | 2026-05-15 |
| [[concepts/maximum-stable-gain\|Maximum Stable Gain]] | Maximum amplification before feedback instability; key metric for hearing aid performance | 2026-05-15 |
