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
| [[concepts/coherent-to-diffuse-power-ratio\|Coherent-to-Diffuse Power Ratio (CDR)]] | Power ratio between directional and diffuse components; estimated from spatial coherence for dereverberation | 2026-05-27 |
| [[concepts/dereverberation\|Dereverberation]] | Processing to reduce late reverberation in speech; CDR-based, MCLP, and deep learning approaches | 2026-05-27 |
| [[concepts/generalized-magnitude-coherence\|Generalized Magnitude Coherence (GMC)]] | Multi-microphone coherence via eigenvalue decomposition; inherently integrates N channels | 2026-05-27 |
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
| [[concepts/deep-marginal-feedback-cancellation\|Deep Marginal Feedback Cancellation]] | DNN-based interference suppression for hearing aid feedback via complex spectrum mapping; L3C-DeepMFC extension | 2026-07-01 |
| [[concepts/closed-loop-fine-tuning\|Closed-Loop Fine Tuning]] | Training strategy addressing open-loop training vs. closed-loop estimation mismatch | 2026-07-01 |
| [[concepts/densely-gated-convolutional-attention-network\|DenGCAN]] | Lightweight encoder-decoder with dense blocks, gated conv, sConformer bottleneck, AG skip-connections | 2026-05-16 |
| [[concepts/iterative-attentional-feature-fusion\|Iterative Attentional Feature Fusion (iAFF)]] | Coarse-then-refined multi-modal fusion using channel attention modules | 2026-05-16 |
| [[concepts/attention-gate\|Attention Gate (AG)]] | Selective skip-connection mechanism using local + global feature attention | 2026-05-16 |
| [[concepts/adaptive-time-frequency-attention\|Adaptive Temporal-Frequency Attention (ATFA)]] | Dual-axis MHSA over time and frequency with adaptive hierarchical fusion (AHA) for speech enhancement | 2026-05-16 |
| [[concepts/sensor-failure-robust-fusion\|Sensor-Failure Robust Multi-Modal Fusion]] | Random modality dropout training + dual-mask architecture for graceful degradation when one sensor is invalid | 2026-05-16 |
| [[concepts/frequency-shift-feedback-cancellation\|Frequency Shift Feedback Cancellation]] | De-correlation via small frequency offset; limited for HA but effective when combined with PEM | 2026-05-15 |
| [[concepts/maximum-stable-gain\|Maximum Stable Gain]] | Maximum amplification before feedback instability; key metric for hearing aid performance | 2026-05-15 |
| [[concepts/complex-spectral-mapping\|Complex Spectral Mapping]] | Predicting RI components of clean speech STFT directly; preserves phase for superior enhancement | 2026-05-16 |
| [[concepts/online-secondary-path-estimation\|Online Secondary Path Estimation]] | Continuous adaptation of the secondary path model during ANC operation | 2026-05-17 |
| [[concepts/distributed-anc\|Distributed ANC]] | Cooperative ANC over wireless acoustic sensor networks; incremental and diffusion strategies | 2026-05-17 |
| [[concepts/psychoacoustic-anc\|Psychoacoustic ANC]] | ANC weighted by human hearing perception; loudness-based optimization | 2026-05-17 |
| [[concepts/selective-anc\|Selective ANC]] | Pre-tuned filter selection based on audio features instead of real-time adaptation | 2026-05-17 |
| [[concepts/active-structural-acoustic-control\|Active Structural Acoustic Control (ASAC)]] | Vibration control of casings/panels to reduce radiated noise at the source | 2026-05-17 |
| [[concepts/convex-combination-anc\|Convex Combination ANC]] | Two filters (fast+slow) blended via mixing parameter to avoid convergence/residue tradeoff | 2026-05-17 |
| [[concepts/sparse-anc\|Sparse ANC]] | Exploiting path or source sparsity via proportionate NLMS and zero-attracting strategies | 2026-05-17 |
| [[concepts/subband-adaptive-filter\|Subband Adaptive Filter]] | Per-subband adaptive filtering for fast convergence with long channel responses | 2026-05-17 |
| [[concepts/neural-observation-filter\|Neural Observation Filter]] | Neural network estimation of RMT observation filter coefficients online; CNN (367k params) or Conv-TasNet; GCC-PHAT + position inputs; async dual-loop | 2026-05-17 |
| [[concepts/fastmnmf\|FastMNMF]] | Fast multichannel NMF with joint diagonalizable SCMs for BSS; block-diagonal variant for distributed arrays reduces cost from O(M^4) to O(sum M_l^4) | 2026-05-20 |
| [[concepts/cross-talk-reduction\|Cross-Talk Reduction]] | Isolates wearer's close-talk speech from cross-talk+noise via blind deconvolution; CTRnet + PuLSS framework for far-field separation | 2026-05-20 |
| [[concepts/acoustic-scene-classification\|Acoustic Scene Classification]] | Classifying environmental audio recordings into location-based classes | 2026-05-20 |
| [[concepts/effective-receptive-field\|Effective Receptive Field]] | The actual input region contributing significantly to a deep network unit's response | 2026-05-20 |
| [[concepts/time-frequency-separate-convolutions\|Time-Frequency Separate Convolutions]] | Parallel 1D temporal and frequential convolutions with split channels for efficient audio networks | 2026-05-20 |
| [[concepts/adaptive-residual-normalization\|Adaptive Residual Normalization]] | Trainable residual normalization balancing raw features with Frequency Instance Normalization | 2026-05-20 |
| [[concepts/bc-resnet\|BC-ResNet]] | CNN architecture using broadcasted residual blocks for efficient keyword spotting and audio classification | 2026-05-20 |
| [[concepts/keyword-spotting\|Keyword Spotting]] | Detecting predefined spoken commands in audio streams under strict latency, memory, and compute constraints | 2026-05-21 |
| [[concepts/broadcasted-residual-learning\|Broadcasted Residual Learning]] | Residual design that averages 2D spectrogram features over frequency, applies temporal convolution, and broadcasts back to 2D | 2026-05-21 |
| [[concepts/subspectral-normalization\|SubSpectral Normalization]] | Frequency-subband normalization for spectrogram neural networks, used in BC-ResNet blocks | 2026-05-21 |
| [[concepts/all-pass-filter\|All Pass Filter]] | Signal processing filter with unity magnitude response at all frequencies, used to modify phase or delay without affecting amplitude | 2026-05-20 |
| [[concepts/bone-conduction-function\|Bone Conduction Function (BCF)]] | Transfer function from audio to bone-conducted vibration; enables synthetic vibration data augmentation | 2026-05-16 |
| [[concepts/complex-ratio-mask\|Complex Ratio Mask]] | Masking target in STFT domain estimating both magnitude and phase of clean speech, providing superior enhancement compared to magnitude-only masks | 2026-05-20 |
| [[concepts/depthwise-separable-convolution\|Depthwise Separable Convolution]] | Efficient convolution block splitting standard convolution into spatial depthwise and channel-wise pointwise convolutions | 2026-05-20 |
| [[concepts/dprnn\|Dual-Path RNN (DPRNN)]] | Lightweight sequence modeling with intra/inter-block RNNs for speech separation | 2026-05-16 |
| [[concepts/robust-control\|Robust Control]] | Branch of control theory dealing with system uncertainty; designs controllers like H-infinity or LQG that maintain stability under acoustic variations | 2026-05-20 |
| [[concepts/waterbed-effect\|Waterbed Effect]] | Fundamental constraint in feedback control (Bode sensitivity integral) where noise reduction in one band inevitably increases noise in others | 2026-05-20 |
| [[concepts/nonlinear-active-noise-control\|Nonlinear Active Noise Control (NLANC)]] | Extends ANC to scenarios with nonlinear primary/secondary paths using Volterra, FLANN, spline, kernel filters | 2026-05-18 |
| [[concepts/volterra-filter\|Volterra Filter]] | Polynomial expansion for modeling nonlinear systems with fading memory; used in NLANC as functional link | 2026-05-18 |
| [[concepts/flann-filter\|Functional Link ANN (FLANN)]] | Single-layer nonlinear expansion via fixed basis functions; low-complexity alternative to Volterra filters | 2026-05-18 |
| [[concepts/spline-adaptive-filter\|Spline Adaptive Filter]] | Cascades linear block with adaptive LUT (look-up table) for efficient nonlinear system modeling | 2026-05-18 |
| [[concepts/kernel-adaptive-filter\|Kernel Adaptive Filter (KAF)]] | Uses kernel trick to project into high-dimensional feature space; KLMS, KAPA, KRLS variants | 2026-05-18 |
| [[concepts/bilinear-filter\|Bilinear Filter]] | Recursive nonlinear filter combining past inputs and outputs via cross-product terms; simple NLANC baseline | 2026-05-18 |
| [[concepts/independent-vector-analysis\|Independent Vector Analysis]] | Multivariate extension of ICA for frequency-domain blind source separation; exploits inter-frequency dependencies to avoid permutation ambiguity | 2026-05-21 |
| [[concepts/blind-source-separation\|Blind Source Separation]] | Recovering individual source signals from observed mixtures without knowledge of mixing process; core audio BSS methods include IVA, ILRMA, FastMNMF | 2026-05-21 |
| [[concepts/heuristic-anc-algorithms\|Heuristic ANC Algorithms]] | Population-based global optimizers (PSO, DE, GA) applied to ANC for non-convex or constrained problems | 2026-05-18 |
| [[concepts/spatially-selective-anc\|Spatially Selective ANC]] | ANC variant for hearables that suppresses noise from undesired directions while preserving sound from a chosen target direction at the eardrum, using ReIRs in a soft-constrained cost | 2026-05-23 |
| [[concepts/soft-constrained-anc\|Soft-Constrained ANC]] | ANC controller design that adds a weighted penalty for a secondary objective (speech preservation, distortion) rather than imposing it as a hard constraint, governed by trade-off scalar $\beta$ | 2026-05-23 |
| [[concepts/spatially-selective-nonlinear-filter\|Spatially Selective Non-Linear Filter (SSF)]] | Deep-learning-based spatial filter for target speaker extraction using LSTM layers and DOA conditioning; geometry-dependent performance | 2026-05-23 |
| [[concepts/geometry-conditioned-ssf\|Geometry-Conditioned SSF (GC-SSF)]] | SSF extension with FiLM-based geometry conditioning via DOA-MPE; generalises across array geometries without retraining | 2026-05-23 |
| [[concepts/doa-microphone-positional-encoding\|DOA-Microphone Positional Encoding (DOA-MPE)]] | Joint encoding of microphone positions and target DOA via sinusoidal features; enables geometry-aware spatial filtering | 2026-05-23 |
| [[concepts/film-layer\|FiLM Layer]] | Feature-wise Linear Modulation for conditioning neural networks via learned scaling and bias parameters | 2026-05-23 |
| [[concepts/target-speaker-extraction\|Target Speaker Extraction]] | Isolating a specific speaker's speech from a mixture using spatial, enrolment, visual, or textual cues | 2026-05-23 |
| [[concepts/time-domain-speech-enhancement\|Time-Domain Speech Enhancement]] | Neural network approaches operating directly on raw waveform samples; avoids invalid STFT and phase reconstruction problems | 2026-05-23 |
| [[concepts/frequency-domain-loss\|Frequency Domain Loss for Time-Domain Networks]] | Training paradigm using spectral loss (STFT magnitude MAE) to optimise time-domain networks; better perceptual quality than waveform loss | 2026-05-23 |
| [[concepts/invalid-stft-problem\|Invalid STFT Problem]] | Modified magnitude + noisy phase may not correspond to valid time-domain signal; causes artefacts in frequency-domain enhancement | 2026-05-23 |
| [[concepts/auxiliary-filter\|Auxiliary Filter]] | Filter identifying the overall path from noise control filter input to error microphone output; used in simultaneous equations method to avoid explicit secondary path modeling | 2026-05-23 |
| [[concepts/simultaneous-equations-method\|Simultaneous Equations Method]] | ANC method that estimates the optimal noise control filter without a secondary path model by solving two independent equations from an auxiliary filter | 2006 |
| [[concepts/gtcrn\|GTCRN (Grouped Temporal CRN)]] | Grouped temporal CRN for ultralightweight speech enhancement; 23.7K params, SFE, TRA | 2026-05-24 |
| [[concepts/nlcmv-beamforming\|NLCMV Beamforming]] | Non-Linearly Constrained Minimum Variance beamforming with WNG and null constraints | 2026-05-24 |
| [[concepts/neural-beamforming\|Neural Beamforming]] | Learning beamformer weights via backprop; integrated with separation/ASR; NLCMV-weight initialization + fine-tuning | 2026-05-20 |
| [[concepts/lcmv-beamformer\|LCMV Beamformer]] | Generalizes MVDR to multiple linear constraints; enables simultaneous target preservation and null steering | 2026-05-26 |
| [[concepts/relative-transfer-function\|Relative Transfer Function (RTF)]] | Acoustic propagation relative to reference microphone; estimated via covariance whitening for beamforming | 2026-05-26 |
| [[concepts/minimum-statistics\|Minimum Statistics]] | VAD-free noise PSD estimation via optimal smoothing and spectral minima tracking; bias compensation for correlated PSD estimates | 2026-05-26 |
| [[concepts/relative-path-virtual-sensing\|Relative Path Virtual Sensing]] | VS method estimating disturbance + anti-noise via relative primary/secondary path models; unifies AF-VS and RM-VS | 2026-05-27 |
| [[concepts/ideal-binary-mask\|Ideal Binary Mask (IBM)]] | Binary T-F mask training target for supervised speech separation; labels T-F units as speech- or noise-dominated | 2026-06-01 |
| [[concepts/ideal-ratio-mask\|Ideal Ratio Mask (IRM)]] | Soft T-F mask training target representing speech energy proportion per unit; preferred target for separation quality | 2026-06-01 |
| [[concepts/permutation-invariant-training\|Permutation Invariant Training (PIT)]] | Training strategy resolving output-speaker ambiguity by minimizing over all output permutations; enables speaker-independent separation | 2026-06-01 |
| [[concepts/deep-clustering-speech-separation\|Deep Clustering for Speech Separation]] | DNN-based embedding learning + K-means clustering of T-F units for speaker-independent multi-talker separation | 2026-06-01 |
| [[concepts/switching-independent-vector-analysis\|Switching Independent Vector Analysis]] | IVA extension using multiple demixing matrices with switching mechanism for time-varying acoustic conditions | 2026-06-04 |
| [[concepts/iterative-source-steering\|Iterative Source Steering]] | Rank-one update for IVA without matrix inversions; 5–7× faster than IP updates | 2026-06-04 |
| [[concepts/spatial-regularization\|Spatial Regularization]] | DOA-based regularization for BSS to resolve permutation ambiguity and improve convergence | 2026-06-04 |
| [[concepts/acoustic-echo-cancellation\|Acoustic Echo Cancellation]] | Removing acoustic echo from microphone signals using adaptive filtering or deep learning | 2026-06-06 |
| [[concepts/cross-attention-alignment\|Cross-Attention Alignment]] | Soft-aligning microphone and far-end signals in feature space for AEC | 2026-06-06 |
| [[concepts/complex-convolving-mask\|Complex Convolving Mask]] | Time-frequency varying complex filter for speech enhancement using 120° weight components | 2026-06-06 |
| [[concepts/sub-pixel-convolution\|Sub-Pixel Convolution]] | Learnable upsampling method for decoder architectures; factor-2 frequency-axis upsampling | 2026-06-06 |
| [[concepts/deep-filtering\|Deep Filtering]] | Complex-valued linear filtering in STFT domain along time axis; outperforms CRMs at low latency | 2026-06-07 |
| [[concepts/erb-scale|ERB Scale]] | Psychoacoustic frequency scale modeling human auditory filter bandwidths; compresses to 32 bands for efficient SE | 2026-06-07 |
| [[concepts/deep-feedback-cancellation|Deep Feedback Cancellation]] | Compact DNN (856K params) for direct feedback-path IR estimation in hearing aids; 30x faster convergence than FD-AFC | 2026-06-10 |
| [[concepts/normalized-euclidean-system-distance|Normalized Euclidean System Distance]] | NESD: normalized squared error between true and estimated feedback-path IRs; used as loss and metric in AFC | 2026-06-10 |
| [[concepts/dynamic-convolution|Dynamic Convolution]] | Input-dependent convolution kernel mixing via lightweight gating; used in HALO adaptive frame-rate operators | 2026-06-18 |
| [[concepts/speech-enhancement\|Speech Enhancement]] | Foundational concept of improving quality and intelligibility of noisy speech | 2026-06-19 |
| [[concepts/gaussian-mixture-model\|Gaussian Mixture Model (GMM)]] | Probabilistic model of weighted Gaussian components; used for clean-speech embedding priors | 2026-06-19 |
| [[concepts/speaker-embedding\|Speaker Embedding]] | Fixed-dimensional vector capturing speaker characteristics for conditioning | 2026-06-19 |
| [[concepts/prior-matching\|Prior Matching]] | Refining noisy embeddings by matching against a clean GMM prior | 2026-06-19 |
| [[concepts/ecapa-tdnn\|ECAPA-TDNN]] | Speaker embedding extractor with channel attention and multi-layer aggregation | 2026-06-19 |
| [[concepts/mp-senet\|MP-SENet]] | TF-domain speech enhancement backbone with magnitude-phase estimation | 2026-06-19 |
| [[concepts/personalized-speech-enhancement\|Personalized Speech Enhancement]] | Speaker-conditioned enhancement using enrollment embeddings | 2026-06-19 |
| [[concepts/voicebank-demand\|VoiceBank+DEMAND (VBD)]] | Standard SE benchmark dataset | 2026-06-19 |
| [[concepts/dns-challenge\|DNS Challenge]] | Deep Noise Suppression challenge dataset | 2026-06-19 |
| [[concepts/pesq\|PESQ]] | ITU-T P.862 perceptual speech quality metric | 2026-06-19 |
| [[concepts/ear-canal-deformation\|Ear Canal Deformation (ECD)]] | Articulatory-gesture-induced ear canal shape change causing air pressure imbalance in sealed ear canal; degrades in-ear speech quality | 2026-06-21 |
| [[concepts/quality-aware-speech-enhancement\|Quality-Aware Speech Enhancement]] | Multi-modal fusion paradigm dynamically weighting auxiliary modality by self-assessed quality; mitigates modality imbalance (QuaSE) | 2026-06-21 |
| [[concepts/object-detection\|Object Detection]] | CV task of localizing + classifying objects; 30-year history from hand-crafted features (Viola-Jones/SIFT/HOG/DPM) to deep learning (R-CNN→Faster R-CNN) | 2026-06-21 |
| [[concepts/faster-r-cnn\|Faster R-CNN]] | End-to-end object detection with Region Proposal Network sharing conv features; modern detection paradigm; NeurIPS 2025 Test of Time Award | 2026-06-21 |
| [[concepts/robust-minimum-variance-beamforming\|Robust Minimum Variance Beamforming (RMVB)]] | Extension of Capon's MVDR enforcing unity-gain over an ellipsoidal array-response uncertainty set; formulated as SOCP, solved by Lagrange multipliers | 2026-06-21 |
| [[concepts/ellipsoidal-uncertainty-modeling\|Ellipsoidal Uncertainty Modeling]] | Representing array-manifold uncertainty as an ellipsoid and propagating it via ellipsoidal calculus (Minkowski sum, Hadamard product) for robust optimization | 2026-06-21 |
| [[concepts/hadamard-product-ellipsoids\|Hadamard Product of Ellipsoids]] | Outer-ellipsoidal approximation of element-wise product of two ellipsoid-valued vectors; propagates multiplicative gain/phase uncertainty in robust beamforming | 2026-06-21 |
| [[concepts/physics-informed-neural-network\|Physics-Informed Neural Network (PINN)]] | Neural network trained with PDE residual loss to respect physical laws; used for soundfield interpolation, HRTF upsampling | 2026-06-25 |
| [[concepts/soundfield-interpolation\|Soundfield Interpolation]] | Estimating acoustic pressure at unmeasured positions from limited sensor measurements; SH, PINN, and RMT methods | 2026-06-25 |
| [[concepts/input-shaping\|Input Shaping]] | Feedforward control technique that convolves command input with impulse sequences to cancel residual vibrations at natural frequencies | 2026-06-28 |
| [[concepts/reinforcement-learning-for-control\|Reinforcement Learning for Control]] | Applies RL paradigm to dynamic system control, enabling adaptive model-free strategies for nonlinear and time-varying systems | 2026-06-28 |
| [[concepts/safe-reinforcement-learning\|Safe Reinforcement Learning]] | Extends RL with hard constraints, risk metrics, and formal safety guarantees for safety-critical engineering applications | 2026-06-28 |
| [[concepts/denoiser-network\|Denoiser Network (DEMUCS)]] | Real-time waveform-domain speech enhancement network from DEMUCS; pretrained baseline fine-tuned for AHS by mixing howling samples with noise-reduction data | 2026-07-03 |
| [[concepts/block-size-adaptation\|Block Size Adaptation (Reblocking)]] | Buffering between host/plugin block sizes in realtime audio; minimum delay Δ = b_plugin − gcd(b_host, b_plugin) | 2026-07-07 |
| [[concepts/ring-buffer\|Ring Buffer (Circular Buffer)]] | Fixed-size FIFO data structure using contiguous memory with wrap-around; standard for realtime audio buffering | 2026-07-07 |
| [[concepts/greatest-common-divisor\|Greatest Common Divisor (GCD)]] | Largest integer dividing two inputs; Euclidean algorithm computes it in O(log n); key to audio block delay formula | 2026-07-07 |
| [[concepts/bezouts-identity\|Bézout's Identity]] | Number theory result: gcd(a,b) = c₁a + c₂b for integers c₁,c₂; foundation for proving tightness of block delay bound | 2026-07-07 |
| [[concepts/audio-latency\|Audio Latency]] | Time delay between input and output in audio systems; sources include block size, reblocking, AD/DA, resampling | 2026-07-07 |
| [[concepts/fifo-queue\|FIFO Queue (First-In-First-Out)]] | Order-preserving queue data structure; implemented as ring buffers for audio stream buffering | 2026-07-07 |
| [[concepts/distributed-binaural-speech-enhancement\|Distributed Binaural Speech Enhancement]] | Two-device (left/right ear) SE exchanging only a compressed representation; enables hearing-aid deployment under bandwidth/latency constraints | 2026-07-10 |
| [[concepts/tango-framework\|Tango Framework]] | Two-stage distributed binaural SE (SN-DNN → SDW-MWF → exchange → MN-DNN → SDW-MWF); baseline for RT-Tango | 2026-07-10 |
| [[concepts/grouped-recurrent-neural-network\|Grouped Recurrent Neural Network (GRNN)]] | Partitions RNN hidden state into G groups for O(H²/G) complexity; cross-band info via rearrangement; used in RT-Tango | 2026-07-10 |
| [[concepts/asymmetric-stft\|Asymmetric STFT]] | Long analysis window + shorter synthesis window to decouple spectral resolution from algorithmic latency | 2026-07-10 |
| [[concepts/fixed-rate-skipping\|Fixed-Rate Skipping (FRS)]] | Temporal sparsification: run DNN at fixed interval, reuse mask in between; exploits temporal redundancy for inference cost reduction | 2026-07-10 |
| [[concepts/td-speakerbeam\|TD-SpeakerBeam]] | Time-domain SpeakerBeam; enrollment-conditioned TSE/OVC baseline | 2026-07-10 |
| [[concepts/own-voice-cancellation\|Own-Voice Cancellation (OVC)]] | Removing enrolled speaker from noisy mixture; complement of TSE | 2026-07-10 |
| [[concepts/mamba-mingru\|Mamba-MinGRU]] | Compute-efficient linear RNN architecture; Mamba blocks + MinGRU temporal mixing; 2 ms latency | 2026-07-10 |
| [[concepts/mingru\|MinGRU]] | Minimal gated RNN; linear recurrence via parallel associative scan | 2026-07-10 |
| [[concepts/singular-value-decomposition\|Singular Value Decomposition]] | Factorization $\mathbf{A}=\mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^{\mathrm{T}}$; discovered independently by Beltrami (1873), Jordan (1874), Sylvester (1889), Schmidt (1907); fundamental tool in numerical linear algebra | 2026-07-12 |
| [[concepts/eckart-young-theorem\|Eckart–Young Theorem]] | Best rank-$k$ approximation in Frobenius/spectral norm is truncated SVD; first proved by Schmidt (1907), rediscovered by Eckart & Young (1936), generalized to all unitarily invariant norms by Mirsky (1960) | 2026-07-12 |
| [[concepts/spectral-norm\|Spectral Norm]] | Matrix 2-norm $\|\mathbf{A}\|_2=\sigma_1(\mathbf{A})$; governs singular-value perturbation bound $|\tilde{\sigma}_i-\sigma_i|\leq\|\mathbf{E}\|_2$ (Weyl 1912) | 2026-07-12 |
| [[concepts/speculative-decoding\|Speculative Decoding]] | Draft-then-verify LLM inference acceleration; rejection sampling guarantees lossless distribution equivalence; speedup $S=\frac{1+c\gamma\alpha}{1+c\gamma}$ governed by acceptance rate $\alpha$, cost ratio $c$, draft length $\gamma$ | 2026-07-12 |
| [[concepts/dspark\|DSpark]] | DeepSeek's speculative decoding framework (2026); semi-autoregressive generation (parallel backbone + lightweight serial head) + confidence-scheduled verification with hardware-aware prefix scheduler; deployed on DeepSeek-V4 with 60–85% speedup | 2026-07-12 |
| [[concepts/dflash\|DFlash]] | Parallel block-diffusion drafting (2025); $O(1)$ drafting latency via bidirectional backbone + KV injection of target hidden states; direct predecessor of DSpark | 2026-07-12 |
| [[concepts/eagle-speculative-decoding\|EAGLE (Speculative Decoding)]] | Feature-layer autoregressive drafting family (EAGLE-1/2/3, 2024–2025); dynamic draft trees, training-time test; principal autoregressive baseline for DSpark | 2026-07-12 |
| [[concepts/medusa\|Medusa]] | Multi-head self-speculation (2024); K extra prediction heads on target LLM + tree attention + typical acceptance; spawned the self-speculation research line | 2026-07-12 |
| [[concepts/multi-token-prediction\|Multi-Token Prediction (MTP)]] | Training-integrated multi-head forecasting (Meta MTP 2024, DeepSeek-V3 MTP 2024); shifts drafting from post-training add-on to pretraining-builtin feature | 2026-07-12 |
| [[concepts/tree-attention\|Tree Attention]] | Attention-mask trick for single-pass parallel verification of branched draft candidates; $O(b^d)$ paths verified in $O(b\cdot d)$ operations; foundation for SpecInfer, Medusa, EAGLE-2, DDTree, DSpark | 2026-07-12 |
| [[concepts/specinfer\|SpecInfer]] | First tree-based speculative decoding (2023); token-tree verification + restorative (generalized rejection) sampling; introduced tree attention to the field | 2026-07-12 |
| [[concepts/ddtree\|DDTree]] | Best-first tree search over DFlash's marginal logits (2026); restores prefix-dependency in parallel drafting without serial heads; sibling approach to DSpark | 2026-07-12 |
| [[concepts/online-feedback-path-modeling\|Online Feedback-Path Modeling (OFBPM)]] | Adaptive estimation of the feedback path F(z) during ANC operation; couples with OSPM when both active. | 2026-07-15 |
| [[concepts/supporting-filter-anc\|Supporting Filter in ANC]] | Auxiliary adaptive filter (e.g., H1/H2) used to decouple OSPM/OFBPM from the FFANC controller and drive AWGN scaling. | 2026-07-15 |
| [[concepts/auxiliary-noise-scaling\|Auxiliary Noise Scaling]] | Dynamic AWGN gain scheduling for OSPM/OFBPM: local (error-driven) vs global (residual- or SF-driven) strategies. | 2026-07-15 |
| [[concepts/mn-tango\|MN-TANGO]] | Simplified single-stage Tango variant; removes SN-DNN; W8A8 + ERB + grouped LSTM reaches 4.65 MMAC/s, 0.177 MB | 2026-07-16 |
| [[concepts/quantization-aware-training\|Quantization-Aware Training (QAT)]] | Quantization strategy simulating INT8 inference during training via fake-quantization + straight-through estimator; preserves FP32 quality for LSTM-based SE | 2026-07-16 |
| [[concepts/post-training-quantization\|Post-Training Quantization (DPTQ)]] | Quantize a trained FP32 model without retraining; INT8 weights + dynamic activation quantization; fails for LSTM due to heterogeneous activation ranges | 2026-07-16 |
| [[concepts/gevd-spatial-filtering\|GEVD-Based Spatial Filtering]] | Rank-constrained SDW-MWF via generalized eigendecomposition of speech/noise SCMs; inference-time spatial filter in TANGO family; robust to mask errors | 2026-07-16 |
| [[concepts/ulcnet\|ULCNet]] | Ultra-low complexity DNN for noise suppression and joint AENR | 2026-07-16 |
| [[concepts/channel-wise-feature-reorientation\|Channel-Wise Feature Reorientation]] | Sub-band feature processing technique for low-complexity speech enhancement | 2026-07-16 |
| [[concepts/power-law-compression\|Power-Law Compression]] | Nonlinear magnitude compression for spectral dynamic range reduction | 2026-07-16 |
| [[concepts/bark-scale-spectral-features\|Bark-Scale Spectral Features]] | Perceptually motivated low-dimensional STFT magnitude projection onto Bark critical bands; enables ~2.5x compression for lightweight AEC post filters (PercepNet, Bark-AEC, EchoFree) | 2026-07-17 |
| [[concepts/u-net-post-filter\|U-Net Post Filter]] | Encoder-decoder neural network with skip connections used as the neural stage of a hybrid AEC/SE pipeline; EchoFree instance: 278K params / 30 MMACs/s on Bark-scale features | 2026-07-17 |
| [[concepts/percepnet-style-neural-post-filter\|PercepNet-Style Neural Post Filter]] | Hybrid AEC/SE design pattern: linear adaptive filter + lightweight neural Bark-scale gain masker; lineage: PercepNet (2021) -> Bark-AEC (2024) -> EchoFree (2025) | 2026-07-17 |
| [[concepts/nsnet2\|NSNet2]] | Lightweight FC+GRU neural network for real-time noise suppression; backbone of Seidel 2024 Bark-AEC postfilter | 2026-07-17 |
| [[concepts/complex-compressed-mse\|Complex Compressed MSE (CCMSE)]] | Speech-enhancement loss combining magnitude-only and phase-aware compressed MSE; used in Seidel 2024 with c=0.3 | 2026-07-17 |
| [[concepts/stft-consistency\|STFT Consistency]] | Re-transforming estimated time-domain signal back to STFT before loss; ensures loss is on a physically realizable spectrum (Wisdom et al. 2019) | 2026-07-17 |
| [[concepts/oversampled-filterbank\|Oversampled Filterbank]] | Multi-rate filterbank with total output rate > input rate; reduces aliasing for subband adaptive filtering (Harteneck-Weiss-Stewart 1999) | 2026-07-17 |
| [[concepts/dtln\|DTLN (Dual-Signal Transformation LSTM Network)]] | Fully data-driven AEC baseline; 4 LSTM(256) + FC sigmoid; 3.16M params, 408 MMACs/s (Westhausen & Meyer 2021) | 2026-07-17 |
| [[concepts/percepnet\|PercepNet]] | Perceptually-motivated low-complexity hybrid DSP/DNN speech enhancement & AEC (ERB + pitch coherence + comb filter) | 2026-07-17 |
| [[concepts/pitch-coherence\|Pitch Coherence]] | Perceptual feature quantifying speech periodicity at pitch; used in PercepNet for double-talk preservation | 2026-07-17 |
| [[concepts/multidelay-block-frequency-domain-adaptive-filter\|Multidelay Block Frequency-Domain Adaptive Filter (MDF)]] | Frequency-domain adaptive filter for AEC; partitions impulse response into blocks for FFT-based convolution (Soo & Pang 1990) | 2026-07-17 |
| [[concepts/structured-sparsity\|Structured Sparsity]] | Neural network compression with whole sub-blocks zeroed; preserves SIMD vectorization (16x4 blocks in PercepNet) | 2026-07-17 |
| [[concepts/recurrent-neural-network\|Recurrent Neural Network]] | Neural network designed for sequential data; maintains hidden state across time steps. Parent concept for LSTM, GRU, BiLSTM, ESN, IndRNN | 2026-07-18 |
| [[concepts/long-short-term-memory\|Long Short-Term Memory (LSTM)]] | Gated RNN variant with input/forget/output gates regulating cell state; addresses vanishing gradient problem (Hochreiter & Schmidhuber 1997) | 2026-07-18 |
| [[concepts/gated-recurrent-unit\|Gated Recurrent Unit (GRU)]] | Simplified LSTM with update/reset gates and merged cell/hidden state (Cho et al. 2014); fewer parameters, comparable performance | 2026-07-18 |
| [[concepts/bidirectional-lstm\|Bidirectional LSTM (BiLSTM)]] | LSTM processing sequence in both forward and backward directions; captures past and future context. 2x cost, best for sentiment, bioinformatics, anomaly detection | 2026-07-18 |
| [[concepts/peephole-lstm\|Peephole LSTM]] | LSTM variant with peephole connections letting gates access cell state directly (Gers & Schmidhuber 2000); improves timing decisions | 2026-07-18 |
| [[concepts/echo-state-network\|Echo State Network (ESN)]] | RNN with fixed random reservoir; only output layer trained (Jaeger 2001). Variants: Deep ESN, Ensemble Deep ESN, ESN+EWT. Fast training, no BPTT | 2026-07-18 |
| [[concepts/independently-recurrent-neural-network\|Independently Recurrent Neural Network (IndRNN)]] | RNN with element-wise recurrent weights decoupling neurons (Li et al. 2018); enables very deep recurrent stacks with stable gradients | 2026-07-18 |
| [[concepts/vanishing-gradient-problem\|Vanishing/Exploding Gradient Problem]] | Central RNN training difficulty: gradients shrink or explode exponentially during BPTT. Mitigated by LSTM/GRU gating, gradient clipping, linear recurrences | 2026-07-18 |
| [[concepts/activation-functions\|Activation Functions]] | Nonlinear functions (tanh, ReLU, Leaky ReLU, ELU, sigmoid, softmax) introducing non-linearity into neural networks | 2026-07-18 |
| [[concepts/attention-mechanism\|Attention Mechanism]] | Allows networks to focus on relevant parts of input sequence; context vector = weighted sum of hidden states. Foundation of transformers | 2026-07-18 |
| [[concepts/adam-optimizer\|Adam Optimizer]] | Adaptive moment estimation optimizer (Kingma & Ba 2015); per-parameter learning rates via first/second moment estimates with bias correction | 2026-07-18 |
| [[concepts/neural-architecture-search\|Neural Architecture Search (NAS)]] | Automates neural network design via optimization over architecture space (Zoph & Le 2016); RL, evolutionary, or gradient-based search | 2026-07-18 |
| [[concepts/gradient-clipping\|Gradient Clipping]] | Rescales gradient norm to threshold tau to prevent exploding gradients during BPTT; standard for RNN training | 2026-07-18 |
| [[concepts/mobilevqe\|MobileVQE]] | Stage-1 depthwise-separable-conv variant of DeepVQE-s for NXP embedded deployment (635k params, 1.34 MMACs) | 2026-07-18 |
| [[concepts/tinyvqe\|TinyVQE]] | Final selected embedded-deployment variant of DeepVQE-s (114k params, 0.48 MMACs/frame, 2.32 ms / 16 ms on HiFi4 DSP @ 600 MHz) | 2026-07-18 |
| [[concepts/fastgrnn\|FastGRNN]] | Lightweight gated RNN reusing weight matrices for gate and candidate; 2-4x fewer params than GRU; exhibits inference-time state drift on long sequences | 2026-07-19 |
| [[concepts/comfi-fastgrnn\|Comfi-FastGRNN]] | Complementary-filter extension of FastGRNN (2 scalars) that mitigates inference-time state drift on long streaming sequences | 2026-07-19 |
| [[concepts/fast-ulcnet\|Fast-ULCNet]] | ULCNet variant using FastGRNN/Comfi-FastGRNN; 0.338M params, ~34% RTF reduction vs. ULCNet at matched NS quality | 2026-07-19 |
| [[concepts/cofi-lite\|CoFi-Lite]] | Ultra-lightweight SE model (Yang et al. 2026) decoupling spectral modeling into parallel coarse (full-band envelope) and fine (low-frequency detail) paths; 12.87M MACs/s, outperforms GTCRN | 2026-07-21 |
| [[concepts/cross-path-fusion\|Cross-Path Fusion (CPF)]] | Lightweight bottleneck fusion module bridging CoFi-Lite's parallel coarse/fine paths via concat–FC–GRU–FC; +0.14 PESQ in ablation | 2026-07-21 |
| [[concepts/output-based-speech-enhancement\|Output-based Speech Enhancement]] | Paradigm configuring an SE system by evaluating SI/SQ of candidate outputs rather than extracting input features. | 2026-07-21 |
| [[concepts/glimpse-proportion\|Glimpse Proportion]] | SI-inspired measure: fraction of T-F tiles where estimated audibility exceeds a threshold (Cooke 2006). | 2026-07-21 |
| [[concepts/dpt-fsnet\|DPT-FSNet]] | Dual-Path Transformer-based Full-Subband Network; 2D-conv encoder + dual-path transformer + 2D-conv decoder on T-F feature map | 2026-07-20 |
| [[concepts/dual-path-compression\|Dual-Path Compression]] | Grid-searched T x F compression combining frame-skip prediction + trainable Mel filters; outperforms single-path at 8x-16x | 2026-07-20 |
| [[concepts/trainable-frequency-compression\|Trainable Frequency Compression]] | Learnable linear transform per band replacing fixed ERB/Mel triangle filters; >0.1 WB-PESQ gain at 8x-16x | 2026-07-20 |
| [[concepts/frame-skip-prediction\|Frame-Skip Prediction]] | Run mask estimator once every r frames, copy mask to skipped frames; PostNet recovers +0.33 WB-PESQ at 8x | 2026-07-20 |
| [[concepts/post-processing-network\|Post-Processing Network (PostNet)]] | Lightweight 67K-param 1-layer GRU + convs refinement module for frame-skip prediction; 15M MACs/s | 2026-07-20 |
| [[concepts/pi-nlms\|PI-NLMS (Physics-Informed NLMS)]] | Adaptive filtering algorithm incorporating RIR structural priors for AEC | 2026-07-17 |
| [[concepts/fast-filter-bank\|Fast Filter Bank (FFB)]] | High-selectivity linear-phase FFT tree with FRM-designed kernels; ~56 dB sidelobe rejection at ~2x FFT cost. | 2026-07-23 |
| [[concepts/constant-q-transform\|Constant-Q Transform (CQT)]] | Spectral transform with constant Q=f_k/Df_k, geometric channel spacing matching the musical equal-tempered scale. | 2026-07-23 |
| [[concepts/bounded-q-transform\|Bounded-Q Transform (BQT)]] | CQT approximation with geometric octave spacing and linear intra-octave channel spacing; medium cost. | 2026-07-23 |
| [[concepts/constant-q-fast-filter-bank\|Constant-Q Fast Filter Bank (CQFFB)]] | High-selectivity geometric-spacing filter bank combining FFB selectivity with CQT distribution; high cost. | 2026-07-23 |
| [[concepts/bounded-q-fast-filter-bank\|Bounded-Q Fast Filter Bank (BQFFB)]] | High-selectivity piecewise-linear filter bank; CQFFB octave separation + FFB intra-octave; ~5 orders lower cost than CQFFB. | 2026-07-23 |
| [[concepts/frequency-response-masking\|Frequency Response Masking (FRM)]] | Digital filter design technique for sharp-transition-band linear-phase FIR filters; underlies the FFB. | 2026-07-23 |
| [[concepts/adaptive-convolution\|Adaptive Convolution]] | Frame-wise causal dynamic convolution for streaming SE; per-frame kernel aggregation via frequency-pooled temporal (GRU) attention; CV→SE transfer failures documented | 2026-07-22 |
| [[concepts/adaptcrn\|AdaptCRN]] | Ultra-lightweight SE model pairing adaptive convolution with ConvNeXt/StarNet block, grouped DPRNN, ERB spectral compression — 135K params, 41 MMACs/s, PESQ 2.98 on VCTK-DEMAND | 2026-07-22 |
| [[concepts/warped-iir-filter\|Warped IIR Filter]] | IIR filters with all-pass warping; modified structures eliminate delay-free recursive loops | 2026-07-23 |
| [[concepts/warped-linear-prediction\|Warped Linear Prediction]] | LPC with all-pass chain — Bark-scale spectral matching, ~6dB SNR savings over conventional LPC at wideband rates | 2026-07-23 |
| [[concepts/agi-roadmap-staircase\|AGI Roadmap Staircase]] | Liang Wenfeng's staircase narrative of intelligence: GPT → CoT → Agent → Continuous learning → Self-iterating singularity → Embodied AI; each step non-disposable; world models and video gen excluded from main line | 2026-07-24 |
| [[concepts/continuous-learning\|Continuous Learning (LLM)]] | Next AI bottleneck per Liang Wenfeng — a problem (not one technique); currently unsolved globally; low-resource 'lottery' research mode at DeepSeek | 2026-07-24 |
| [[concepts/restraint-as-strategy\|Restraint as Strategy]] | Liang Wenfeng's commercial argument: in a market as large as AI, the player willing to take less profit wins; expressed in open-source, 10-month payback pricing, no-KPI organization | 2026-07-24 |
| [[concepts/noise-agnostic-enrollment-guidance\|Noise-agnostic Enrollment Guidance]] | Denoise mixture before context interaction with enrollment so guidance is free of noise contamination (LGTSE) | 2026-07-25 |
| [[concepts/distortion-aware-training\|Distortion-aware Training]] | Use denoiser's mildly distorted output as additional training input to expose model to distortion (D-LGTSE) | 2026-07-25 |
| [[concepts/sef-pnet\|SEF-PNet]] | Speaker encoder-free personalized TSE backbone (ICASSP 2025); baseline for LGTSE/D-LGTSE | 2026-07-25 |
| [[concepts/cie-mdptnet\|CIE-mDPTNet]] | SOTA embedding-free TSE backbone (Interspeech 2024); stronger baseline for D-LGTSE generalization | 2026-07-25 |
| [[concepts/geometry-aware-dynamic-convolution\|Geometry-Aware Dynamic Convolution (Geo-DConv)]] | Dynamic conv whose basis-kernel mixture weights are produced from microphone coordinates by TACT; universal adapter converting fixed-array SE backbones into array-invariant systems with permutation equivariance. | 2026-07-27 |
| [[concepts/topology-aware-coordinate-transformer\|Topology-Aware Coordinate Transformer (TACT)]] | Transformer-Encoder over Fourier-encoded microphone coordinates; produces the transformation matrix used by Geo-DConv; permutation-equivariant by construction. | 2026-07-27 |
| [[concepts/array-invariant-speech-enhancement\|Array-Invariant Speech Enhancement]] | Subfield of MCSE building models that generalize across mic counts and geometries without retraining; spans array-agnostic (TAC, USES2, FOA, UniArray) and geometry-aware (Geo-DConv, GC-SSF) approaches. | 2026-07-27 |
| [[concepts/trunet\|Tiny Recurrent U-Net (TRU-Net)]] | Lightweight frequency-axis U-Net with FGRU/TGRU recurrent mixing for real-time speech enhancement (0.38 M params, 0 ms lookahead) | 2026-07-31 |
| [[concepts/phase-aware-beta-sigmoid-mask\|Phase-aware β-sigmoid Mask (PHM)]] | Complex-valued mask with learnable β magnitude range and law-of-cosines phase reconstruction; quadrilateral extension enables joint denoising + dereverberation | 2026-07-31 |
| [[concepts/per-channel-energy-normalization\|Per-Channel Energy Normalization (PCEN)]] | Spectral-normalization technique that divides each band's energy by its time-averaged level; used as a training-time threshold oracle and VAD | 2026-08-01 |
| [[concepts/iccrn\|ICCRN]] | Inplace Cepstral CRN — Liu & Zhang 2023; CFB + U-Net, no frequency downsampling, CSM loss. | 2026-08-01 |
| [[concepts/cepstral-frequency-block\|Cepstral Frequency Block (CFB)]] | Core novel ICCRN block — FFT-based cepstral-space branch + TF residual branch with task-split gate. | 2026-08-01 |
| [[concepts/cepstral-space-speech-enhancement\|Cepstral-Space Speech Enhancement]] | SE paradigm processing TF features in a cepstral space reached via real-valued FFT; exploits harmonic sparsity. | 2026-08-01 |
| [[concepts/igcrn\|IGCRN]] | Inplace Gated CRN for dual-channel SE — inplace convolutions + channel-wise LSTM reused across frequency bins; the inplace-CRN family founder and predecessor of ICCRN. | 2026-08-01 |
| [[concepts/inplace-convolution\|Inplace Convolution]] | Stride-1 convolution on the frequency dimension that preserves per-bin spatial cues for multi-channel SE; the core architectural choice of IGCRN/ICCRN. | 2026-08-01 |
| [[concepts/channel-wise-lstm\|Channel-wise LSTM with Model Reuse]] | Per-frequency-bin LSTM with weights shared across all bins (one 64-hidden LSTM vs. 1024 in conventional CRN); the compact recurrent bottleneck of the inplace-CRN family. | 2026-08-01 |
| [[concepts/mask-mapping-amplitude-prediction\|Mask + Mapping + Phase Target]] | Multi-output training target combining amplitude mask, amplitude mapping, and normalized phase in a single decoder; complementary strengths at high/low SNR; introduced by IGCRN. | 2026-08-01 |
| [[concepts/sicrn\|SICRN]] | State-space + Inplace-Conv CRN; first S4ND + inplace conv combination for monaural SE. | 2026-08-01 |
| [[concepts/sic-block\|SIC Block]] | Channel-bifurcated S4ND + 2D inplace conv module fused via sigmoid attention; SICRN's core contribution. | 2026-08-01 |
| [[concepts/s4nd\|S4ND]] | Multidimensional state space model (PDE extension of S4) with infinite receptive field along every axis; SICRN's global branch. | 2026-08-01 |
| [[concepts/sse-net\|SSE-Net]] | Spike-native SNN-SE architecture (SFEB/ITB, LIF encoder-decoder) — SOTA SNN-SE, 19.70 M Ops/s power proxy | 2026-08-01 |
| [[concepts/spiking-feature-extraction-block\|Spiking Feature Extraction Block]] | Three-branch residual spiking block (LIF + continuous path) mitigating binary-activation information loss | 2026-08-01 |
| [[concepts/information-transformation-block\|Information Transformation Block]] | Two-branch gated refinement converting spike features back to continuous signals | 2026-08-01 |
| [[concepts/intel-neuromorphic-dns-challenge\|Intel Neuromorphic DNS Challenge]] | SNN-SE benchmark defining power-proxy metrics (SynOPs + 10×NeuronOPs, PDP) on Intel Loihi energy accounting | 2026-08-01 |
| [[concepts/mamba\|Mamba]] | Selective state-space model with input-dependent parameters and linear-time scan | 2026-08-03 |
| [[concepts/semamba\|SEMamba]] | First Mamba-based speech enhancement system; SOTA PESQ 3.69 on VoiceBank-DEMAND with PCS | 2026-08-03 |
| [[concepts/perceptual-contrast-stretching\|Perceptual Contrast Stretching (PCS)]] | Post-enhancement spectral stretching by perceptual importance; lifts SEMamba PESQ to 3.69 | 2026-08-03 |
| [[concepts/lights4\|lightS4]] | Diagonal-constrained S4 variant for lightweight SE; element-wise ZOH discretization + FFT global convolution | 2026-08-03 |
| [[concepts/auditory-inspired-spectral-compressor\|Auditory-Inspired Spectral Compressor (AISC)]] | Parameter-free ERB-based dimensionality reduction; 1.5kHz perceptual split, 2.6x MACs reduction | 2026-08-03 |
| [[concepts/classifier-loss\|Classifier Loss]] | Auxiliary speaker-classification cross-entropy loss for vocal-interference suppression; +0.16 PESQ under competing voices | 2026-08-03 |

