# Coherent-to-Diffuse Power Ratio Estimation for Dereverberation

Andreas Schwarz\*, Walter Kellermann, Fellow, IEEE

Abstract—The estimation of the time- and frequencydependent coherent-to-diffuse power ratio (CDR) from the measured spatial coherence between two omnidirectional microphones is investigated. Known CDR estimators are formulated in a common framework, illustrated using a geometric interpretation in the complex plane, and investigated with respect to bias and robustness towards model errors. Several novel unbiased CDR estimators are proposed, and it is shown that knowledge of either the direction of arrival (DOA) of the target source or the coherence of the noise field is sufficient for unbiased CDR estimation. The validity of the model for the application of CDR estimates to dereverberation is investigated using measured and simulated impulse responses. A CDR-based dereverberation system is presented and evaluated using signal-based quality measures as well as automatic speech recognition accuracy. The results show that the proposed unbiased estimators have a practical advantage over existing estimators, and that the proposed DOA-independent estimator can be used for effective blind dereverberation.

Index Terms—Spatial Coherence, Diffuse Noise Suppression, Diffuseness, Dereverberation, Reverberation Suppression

# I. INTRODUCTION

T has been observed as early as 1969 that the measured I spatial coherence between two microphones allows the discrimination between direct sound and reverberation [1]. A first signal enhancement algorithm based on this observation was proposed by Allen et al. in 1977 [2], where the magnitude of the coherence is estimated in the Short-Time Fourier Transform (STFT) domain and used as a gain for reverberation suppression. Other heuristic methods for noise reduction and dereverberation using coherence estimates have since been proposed [3]–[7]. Related methods have also been investigated for noise suppression in connection with beamforming, and postfilters which are statistically optimal under certain conditions have been proposed for the suppression of uncorrelated [8] and diffuse [9] noise.

More recently, explicit estimators for the ratio between direct and diffuse signal components, termed the coherentto-diffuse power ratio (CDR), from short-time coherence estimates have been formulated [10], [11], based on the same assumptions as the earlier optimum postfilter derivations [9]. Also, results have since been generalized from omnidirectional microphones to other microphone directivities [12], [13] and spherical microphone arrays [14]. While these estimates can be

A. Schwarz and W. Kellermann are with the Chair of Multimedia Communications and Signal Processing, Friedrich-Alexander-Universitat¨ Erlangen-Nurnberg, 91058 Erlangen, Germany (e-mail: schwarz@LNT.de; ¨ wk@LNT.de).

The authors would like to thank Opticom GmbH for providing PESQ evaluation software.

EDICS: AUD-SIRR, AUD-MAAE, AUD-SEN, AUD-ASAP

used for the formulation of postfilters for signal enhancement [15], which is the main application considered in this contribution, short-time CDR estimates (or the equivalent “diffuseness” measure) also have applications in parametric coding of spatial audio signals [16] and the extraction of spatial features for automatic speech recognition (ASR) [17].

In this contribution, the estimation of the CDR from the measured coherence between two omnidirectional microphones, and the application of the CDR estimates to dereverberation, is investigated. First, the signal model for the recording of a noisy or reverberant signal with two omnidirectional microphones is described, the relationship between signal and noise coherence models and the coherence of the mixed signal is given, and coherence models for the application to dereverberation are discussed. Then, several known CDR estimators are formulated in a common framework, illustrated using a geometric interpretation in the complex plane, and improved unbiased estimators are proposed. It is shown that knowledge of either the target signal direction or the noise coherence is sufficient for an unbiased CDR estimation, and estimators are proposed for the cases of unknown target signal direction and unknown noise coherence. Finally, the CDR estimators are applied in a postfilter for reverberation suppression and evaluated by processing reverberant speech and comparing ASR recognition accuracy as well as various signal quality measures. This paper builds on results published in a recent conference paper by the same authors, in which the novel estimators were initially proposed [15].

# II. SIGNAL MODEL

We consider the recording of a reverberant or noisy speech signal by two omnidirectional microphones with a spacing $d ,$ located in the same horizontal plane. The signal $x _ { i } ( t )$ of the i-th microphone is composed of a desired signal component $s _ { i } ( t )$ and an undesired component $n _ { i } ( t )$ consisting of noise and/or late reverberation, i.e.,

$$
x _ {i} (t) = s _ {i} (t) + n _ {i} (t), i = 1, 2. \tag {1}
$$

The microphone, desired and noise signals are represented in the time-frequency (STFT) domain by the corresponding uppercase letters, i.e., $X _ { i } ( l , f ) , S _ { i } ( l , f )$ and $N _ { i } ( l , f )$ , respectively, with the discrete-time frame index l and continuous frequency $f ,$ and are assumed to be short-time stationary. Using the representation in the STFT domain, the short-time auto- and cross-power spectra between two signals $u ( t )$ and v(t) are defined as

$$
\Phi_ {u v} (l, f) = \mathcal {E} \{U (l, f) V ^ {*} (l, f) \}, \tag {2}
$$

where E is the expectation operator. It is assumed that the auto-power spectra of the signal components are the same at both microphones, i.e.,

$$
\Phi_ {s _ {1} s _ {1}} (l, f) = \Phi_ {s _ {2} s _ {2}} (l, f) = \Phi_ {s} (l, f), \tag {3}
$$

$$
\Phi_ {n _ {1} n _ {1}} (l, f) = \Phi_ {n _ {2} n _ {2}} (l, f) = \Phi_ {n} (l, f). \tag {4}
$$

Note that this assumption is generally appropriate for a plane wave as desired signal as well as for noise and late reverberation, but may in practice be impacted by the presence of early reflections causing destructive or constructive interference. The time- and frequency-dependent signal-to-noise ratio (SNR) of the microphone signals can be defined as

$$
S N R (l, f) = \frac {\Phi_ {s} (l , f)}{\Phi_ {n} (l , f)}. \tag {5}
$$

The complex spatial coherence functions of the desired signal and noise components are given by

$$
\Gamma_ {s} (f) = \frac {\Phi_ {s _ {1} s _ {2}} (l , f)}{\Phi_ {s} (l , f)}, \Gamma_ {n} (f) = \frac {\Phi_ {n _ {1} n _ {2}} (l , f)}{\Phi_ {n} (l , f)}, \tag {6}
$$

respectively, and are assumed to be time-invariant, i.e., dependent only on the spatial characteristics of the signal components. It is furthermore assumed that signal and noise are mutually orthogonal, such that

$$
\Phi_ {x} (l, f) = \Phi_ {s} (l, f) + \Phi_ {n} (l, f). \tag {7}
$$

The complex spatial coherence of the mixed sound field can then be written as a function of the SNR and the signal and noise coherence functions:

$$
\Gamma_ {x} (l, f) = \frac {S N R (l , f) \Gamma_ {s} (f) + \Gamma_ {n} (f)}{S N R (l , f) + 1}. \tag {8}
$$

This relationship is valid for any signal and noise coherence function. For the special case of a fully coherent desired signal component and diffuse noise, the term CDR or directto-diffuse ratio (DDR) is often used for the SNR. We will adopt the term CDR in the following. (8) can be rewritten as a parametric line equation in the complex plane, highlighting that $\Gamma _ { x }$ lies on a straight line connecting $\Gamma _ { n }$ and $\Gamma _ { s } \mathbf { : }$

$$
\Gamma_ {x} (l, f) = \Gamma_ {s} (f) + \frac {1}{C D R (l , f) + 1} (\Gamma_ {n} (f) - \Gamma_ {s} (f)). \tag {9}
$$

Note that the line parameter $D ( l , f ) = [ C D R ( l , f ) + 1 ] ^ { - 1 }$ is equivalent to the diffuseness defined in [18].

# III. COHERENCE MODELS FOR DEREVERBERATION

The desired and noise or reverberation components of the microphone signals are characterized by time-invariant coherence functions $\Gamma _ { s } ( f )$ and $\Gamma _ { n } ( f )$ , respectively. In the following, suitable models for these spatial coherence functions are discussed for the application to dereverberation.

# A. Desired Signal

The desired signal component is modeled as a plane wave with the direction of arrival (DOA) θ with respect to the microphone axis, where $\theta = 0 ^ { \circ }$ corresponds to broadside direction. The corresponding time-invariant coherence function is given by

$$
\Gamma_ {s} (f) = \frac {\Phi_ {s _ {1} s _ {2}} (l , f)}{\Phi_ {s} (l , f)} = e ^ {j k d \sin (\theta)} = e ^ {j 2 \pi f \Delta t}, \tag {10}
$$

with the time difference of arrival (TDOA) $\Delta t = d \sin ( \theta ) / c ,$ the wavenumber $k = 2 \pi f / c$ and the speed of sound c. This coherence function always has a magnitude of one, and is equal to one for $\Delta t = 0$ .

# B. Reverberation as Isotropic Sound Field

In array signal processing, environmental noise is often modeled by the superposition of an infinite number of uncorrelated, spatially distributed noise sources. In applications like underwater acoustics or radio communication, this model is motivated by the presence of many independent noise and interfering sources around the receiver [19]. The most common assumption for the spatial distribution is a sphere centered around the receiver, which corresponds to what is known as a diffuse or spherically isotropic noise field. The spatial coherence function between two omnidirectional sensors in a diffuse noise field is real-valued and given by

$$
\Gamma_ {\text { diffuse }} (f) = \frac {\sin (k d)}{k d} = \frac {\sin (2 \pi f d / c)}{2 \pi f d / c}. \tag {11}
$$

While diffusivity of the noise field is easily motivated in the aforementioned scenarios, a few more considerations are necessary for the modeling of a reverberation component originating from a single excitation signal. Since acoustic transmission within a room is generally assumed to be linear and time-invariant, a reverberant signal can be modeled by the convolution of a source signal with a time-invariant room impulse response (RIR) [20]. The reverberant signals recorded at two points in space, i.e., by two microphones, are therefore linearly related, and the theoretical coherence function between these two signals is equal to one. However, when limited observation windows are considered, and the excitation signal has a limited temporal correlation, reflections with different delays can be approximated as uncorrelated sources. This uncorrelated scattering assumption is widely used in mobile radio communications [21] and underwater acoustics [22], and is useful in room acoustics as well, where it has been observed that the sound field in a reverberant room appears as an approximately diffuse sound field [23], [24]. The plausibility of the diffuseness assumption for reverberation can be visualized using the image source model [25]: for higher reflection orders, the angular distribution of the image sources becomes increasingly isotropic. Furthermore, given a limited observation window length, the delayed reflected versions of the source signal are increasingly decorrelated with increasing reflection orders. Based on this idea, we can predict a number of factors which contribute to how well the model of diffuseness is fulfilled: a large room contributes to the uncorrelatedness of the image sources, due to larger relative delays between reflections; highly reflective surfaces contribute to the presence of many image sources with similar power, since the power contributed by reflections decays more slowly with the reflection order; and low temporal correlation of the source signal contributes to low correlation between the delayed reflections. Some of these effects are illustrated in Section VI-B using measured and simulated RIRs.

In real rooms, effects like diffraction, diffuse reflection [20], and potentially time-variant effects [26] may further contribute to the randomization of delays and incidence angles of reflections and therefore increase the diffuseness of the reverberation sound field. However, as shown later, the image source model is sufficient to explain a wide range of practical effects which affect the reverberation coherence.

While the diffuse sound field model is the most common in room acoustics and signal enhancement, it has been observed that reverberant noise in rooms with highly absorbing floors and ceilings can be modeled more accurately by noise sources distributed in the horizontal plane, i.e., by a 2D isotropic (cylindrically isotropic) noise field, as opposed to a diffuse (spherically isotropic) noise field [27]. This noise field model consists of uncorrelated noise sources located on a circle around and in the same plane as the microphones (typically the horizontal plane), and is motivated by the rapid decay of all vertically propagating sound components due to the strong absorption at the floor and/or ceiling. The corresponding spatial coherence function for two omnidirectional microphones located in the same plane as the noise sources is the zerothorder Bessel function of the first kind [23], [28]:

$$
\Gamma_ {2 \mathrm{D} - \mathrm{iso}} (f) = J _ {0} (k d) = J _ {0} (2 \pi f d / c). \tag {12}
$$

Note that, both in the case of diffuse and 2D-isotropic noise fields, the coherence function is real-valued, since the spatial distribution of the sources is symmetric with respect to the microphone array axis.

In Section VI-B, the effects of room geometry and surface reflectivity on the coherence of the reverberation component are evaluated using RIRs generated with the image source method, and RIRs that were measured in different rooms.

# IV. COHERENT-TO-DIFFUSE POWER RATIO ESTIMATION

For most proposed postfilters, the gain function has been formulated directly as a function of auto- and cross-power spectral estimates [8], [9], which are typically obtained from the microphone signals by recursive averaging:

$$
\hat {\Phi} _ {x _ {i} x _ {j}} (l, f) = \lambda \hat {\Phi} _ {x _ {i} x _ {j}} (l - 1, f) + (1 - \lambda) X _ {i} (l, f) X _ {j} ^ {*} (l, f), \tag {13}
$$

where λ is a constant between 0 and 1. We follow a different approach where we first derive an SNR estimate, which can then be used to apply any suppression technique such as the Wiener filter or spectral subtraction [29]. Furthermore, we write the estimate not as a function of auto- and cross-power spectral estimates, but as a function of the estimated shorttime spatial coherence, which allows additional insight into the behavior of the estimator. The short-time coherence is estimated by

$$
\hat {\Gamma} _ {x} (l, f) = \frac {\hat {\Phi} _ {x _ {1} x _ {2}} (l , f)}{\sqrt {\hat {\Phi} _ {x _ {1} x _ {1}} (l , f) \hat {\Phi} _ {x _ {2} x _ {2}} (l , f)}}. \tag {14}
$$

Since the focus is on estimating the SNR for a mixture of a fully coherent signal with $| \Gamma _ { s } ( f ) | = 1$ and isotropic noise with $\Gamma _ { n } \in \mathbb { R }$ , where typically $\Gamma _ { n } ( f ) = \Gamma _ { \mathrm { d i f f u s e } } ( f )$ , we use the term CDR instead of SNR for the quantity to be estimated in the following. For the application to dereverberation, the CDR is equivalent to the direct-to-reverberation power ratio (DRR), under the assumption that reverberant sound can be modeled as a mixture of a direct component and a perfectly diffuse reverberation component which are mutually uncorrelated, thus neglecting early reflections.

The aim is now to estimate the CDR from an estimate of the short-time spatial coherence ${ \hat { \Gamma } } _ { x } ( l , f )$ , exploiting the known coherence functions of the signal and/or noise component, and the relationship of these coherence models and the mixed sound field coherence to the CDR given by (9). Solving (9) for the CDR yields (for brevity, the time- and frequencydependency is omitted in the following)

$$
C D R = \frac {\Gamma_ {n} - \Gamma_ {x}}{\Gamma_ {x} - \Gamma_ {s}}, \tag {15}
$$

or, reformulated as the diffuseness D,

$$
D = \frac {1}{C D R + 1} = \frac {\Gamma_ {x} - \Gamma_ {s}}{\Gamma_ {n} - \Gamma_ {s}}. \tag {16}
$$

Although $\Gamma _ { x }$ and $\Gamma _ { s }$ may be complex, the CDR and diffuseness are real-valued quantities; however, when inserting a coherence estimate $\hat { \Gamma } _ { x }$ for $\Gamma _ { x }$ in (15), the resulting values are in general complex-valued, due to mismatch between the coherence models and the actual acoustic conditions, and the variance of the coherence estimate. Estimating the CDR by direct application of (15) is therefore not feasible, which is why a number of different estimator implementations, which yield a positive, real-valued CDR estimate for all possible values of $\hat { \Gamma } _ { x } , | \hat { \Gamma } _ { x } | \leq 1$ , have been proposed.

In the following, first, the interpretation of the estimator behavior in the complex plane is discussed. Then, existing and novel approaches to CDR estimation are analyzed. For an easier comparison, the estimators are reformulated as a function of only the coherence estimate $\hat { \Gamma } _ { x }$ and the assumed coherence models $\tilde { \Gamma } _ { s }$ and $\tilde { \Gamma } _ { n }$ , where $\tilde { \Gamma } _ { s }$ is the direct signal coherence computed according to (10) from an a-priori known or estimated TDOA $\widehat { \Delta t } .$ , and $\tilde { \Gamma } _ { n }$ is assumed to match the diffuse coherence model (11). We start with methods which make use of both $\tilde { \Gamma } _ { s }$ and ${ \tilde { \Gamma } } _ { n } ,$ i.e., exploit information on the DOA and the noise coherence, continue with DOAindependent estimators which exploit only the knowledge of ${ \tilde { \Gamma } } _ { n } .$ , and finally propose a CDR estimator for the case of available signal coherence $\tilde { \Gamma } _ { s } ,$ , but unknown noise coherence. Table I summarizes the presented estimators and their main properties. Finally, estimator bias and robustness are evaluated.

# A. Interpretation of Estimator Behavior in the Complex Plane

Fig. 1 shows the output of the estimators which are described in the following sections in the complex plane of possible coherence values ${ \hat { \Gamma } } _ { x } .$ Results for a direct signal TDOA $\Delta t = 0$ (broadside) are shown in the first row, while in the second row, results are shown for $\begin{array} { r } { \Delta t { } = \frac { 1 } { 5 f } } \end{array}$ . For all estimators, $\tilde { \Gamma } _ { s } ~ = ~ \Gamma _ { s } , ~ \tilde { \Gamma } _ { n } ~ = ~ \Gamma _ { n }$ is assumed. The symbol ◦ marks the coherence of a fully coherent signal with the respective TDOA according to (10), while the symbol × marks the coherence of an ideal diffuse signal given by (11). The straight white line between these points marks the theoretical coherence values which would occur under ideal conditions for different CDR values, according to (9). The bias of a CDR estimator is henceforth defined as the deviation of the estimator from (15) for coherence values along this line; i.e., an unbiased estimator should exactly match (15) for these values. This can be verified by inserting $\Gamma _ { x }$ according to (9) for $\hat { \Gamma } _ { x }$ into the estimator equation, which yields ${ \widehat { C D R } } = { \widehat { C D R } }$ for an unbiased estimator. Furthermore, since the coherence estimates ${ \hat { \Gamma } } _ { x } ,$ which are observed in practice, will not lie exactly on the line, a good estimator should also be robust in the sense that some deviations of the coherence estimate from the assumed model, e.g., caused by an imperfect DOA estimate, do not lead to large deviations of the CDR estimate. In Fig. 1, robustness can be seen in the change of the CDR estimate for coherence values slightly deviating from the line; if these changes are abrupt, as in Fig. 1b for coherence values close to the unit circle, this indicates non-robust behavior. While we do not derive a measure for the overall robustness of an estimator, which would require establishing a statistical model for the errors, we evaluate the behavior of the different estimators with coherence model errors in Section IV-E.

# B. CDR Estimation for Known DOA and Noise Coherence

Using the same model as described in Section II, McCowan and Bourlard [9] derived the Wiener postfilter for a coherent signal in diffuse noise. Jeub et al. [30] evaluated this postfilter for the suppression of reverberation, and formulated a CDR estimate based on the same model [10]. Both McCowan and Jeub rely on the assumption that the direct signal is time-aligned in both microphones, which can be achieved by applying a delay corresponding to the TDOA estimate ∆t to one of the channels [30]. In the STFT domain, this delay is equivalent to a phase rotation of the cross-power spectrum (assuming that the delay is significantly shorter than the transform length), and can therefore be represented in the CDR estimator equation by multiplying the complex rotation factor $e ^ { - j 2 \pi f \widehat { \Delta t } } = \tilde { \Gamma } _ { s } ^ { * }$ with the coherence estimate ${ \hat { \Gamma } } _ { x } .$ . This allows the formulation of the CDR estimator including time alignment as a function of only $\hat { \Gamma } _ { x } , \tilde { \Gamma } _ { s }$ s and ${ \tilde { \Gamma } } _ { n } \colon$

Table I OVERVIEW OF INVESTIGATED CDR ESTIMATORS, REQUIRED PRIOR INFORMATION (NOISE AND/OR SIGNAL COHERENCE) AND UNBIASEDNESS. 

<table><tr><td>Estimator</td><td>Definition</td><td>Required</td><td>Unbiased</td></tr><tr><td>Jeub</td><td> $\frac{\tilde{\Gamma}_{n}-\text{Re}\{\tilde{\Gamma}_{s}^{*}\hat{\Gamma}_{x}\}}{\text{Re}\{\tilde{\Gamma}_{s}^{*}\hat{\Gamma}_{x}\}-1}$ </td><td> $\tilde{\Gamma}_{n}, \tilde{\Gamma}_{s}$ </td><td>no</td></tr><tr><td>Thiergart 1</td><td> $\text{Re}\left\{\frac{\tilde{\Gamma}_{n}-\hat{\Gamma}_{x}}{\tilde{\Gamma}_{x}-\tilde{\Gamma}_{s}}\right\}$ </td><td> $\tilde{\Gamma}_{n}, \tilde{\Gamma}_{s}$ </td><td>yes</td></tr><tr><td>Proposed 1</td><td> $\frac{\text{Re}\{\tilde{\Gamma}_{s}^{*}(\tilde{\Gamma}_{n}-\hat{\Gamma}_{x})\}}{\text{Re}\{\tilde{\Gamma}_{s}^{*}\hat{\Gamma}_{x}\}-1}$ </td><td> $\tilde{\Gamma}_{n}, \tilde{\Gamma}_{s}$ </td><td>yes</td></tr><tr><td>Proposed 2</td><td> $\frac{1-\tilde{\Gamma}_{n}\cos(\arg(\tilde{\Gamma}_{s}))}{|\tilde{\Gamma}_{n}-\tilde{\Gamma}_{s}|} \left| \frac{\tilde{\Gamma}_{s}^{*}(\tilde{\Gamma}_{n}-\hat{\Gamma}_{x})}{\text{Re}\{\tilde{\Gamma}_{s}^{*}\hat{\Gamma}_{x}\}-1} \right|$ </td><td> $\tilde{\Gamma}_{n}, \tilde{\Gamma}_{s}$ </td><td>yes</td></tr><tr><td>Thiergart 2</td><td> $\text{Re}\left\{\frac{\tilde{\Gamma}_{n}-\hat{\Gamma}_{x}}{\hat{\Gamma}_{x}-e^{j\arg\hat{\Gamma}_{x}}}\right\}$ </td><td> $\tilde{\Gamma}_{n}$ </td><td>no</td></tr><tr><td>Proposed 3</td><td>(25)</td><td> $\tilde{\Gamma}_{n}$ </td><td>yes</td></tr><tr><td>Proposed 4</td><td>(27)</td><td> $\tilde{\Gamma}_{s}$ </td><td>yes</td></tr></table>

$$
\begin{array}{l} \widehat {C D R} _ {\mathrm{Jeub}} (l, f) = \max \left(0, \frac {\tilde {\Gamma} _ {n} - \operatorname{Re} \{e ^ {- j 2 \pi f \widehat {\Delta t}} \hat {\Gamma} _ {x} \}}{\operatorname{Re} \{e ^ {- j 2 \pi f \widehat {\Delta t}} \hat {\Gamma} _ {x} \} - 1}\right) \\ = \max \left(0, \frac {\tilde {\Gamma} _ {n} - \operatorname{Re} \{\tilde {\Gamma} _ {s} ^ {*} \hat {\Gamma} _ {x} \}}{\operatorname{Re} \{\tilde {\Gamma} _ {s} ^ {*} \hat {\Gamma} _ {x} \} - 1}\right). \tag {17} \\ \end{array}
$$

The maximum operation is required to prevent negative results for the CDR estimate. This estimator is unbiased for $\tilde { \Gamma } _ { s } = 1$ , i.e., $\widehat { \Delta t } = 0$ . However, for non-zero TDOAs, the phase rotation of the coherence estimate $\hat { \Gamma } _ { x }$ does not only affect the direct signal component, but also the coherence of the diffuse signal component. Since this is not accounted for by this estimator, the estimate is biased for non-zero TDOAs. The estimator is illustrated in Fig. 1a.

![](figures/618c60abfeaea3540c76a48f89046c8ad891d109388c0c238c03967f6036ec55.jpg)

<details>
<summary>heatmap</summary>

| Method | Δt=0 (1j) | Δt=0 (0j) | Δt=0 (-1j) | Δt=1/5f (0j) | Δt=1/5f (-1j) |
|--------|-----------|-----------|------------|--------------|---------------|
| Jeub   | High      | Low       | Medium     | High         | Low           |
| Thiergart 1 unbiased | Medium    | Low       | Medium     | Medium       | Low           |
| Proposed 1 unbiased | Medium    | Low       | Medium     | Medium       | Low           |
| Proposed 2 unbiased | High      | Low       | Medium     | High         | Low           |
| Thiergart 2 DOA-indep. | High     | Medium    | Medium     | High         | Low           |
| Proposed 3 unbiased DOA-indep. | High    | Medium    | Medium     | High         | Low           |
| Proposed 4 unbiased noise-indep. | High    | Medium    | Medium     | High         | Low           |
</details>

Figure 1. Coherent-to-diffuse power ratio estimates obtained from different estimators (columns) as a function of the complex spatial coherence estimate ${ \hat { \Gamma } } _ { x } .$ The theoretical coherence of fully coherent (Γs) and fully diffuse (Γn) signals is marked by ◦ and ×, respectively, while the theoretical coherence of mixed signals lies on the connecting line. Estimators are computed using $\tilde { \Gamma _ { s } } = \mathbf { \bar { \Gamma } } _ { s } , \tilde { \Gamma } _ { n } = \Gamma _ { n } .$ . Parameters d = 8 cm, f = 1 kHz, different TDOAs (rows).

Thiergart et al. [11], [13] proposed to estimate the CDR by directly inserting the target signal coherence estimate $\tilde { \Gamma } _ { s }$ into (15), and taking the real part:

$$
\widehat {C D R} _ {\text { Thiergart1 }} (l, f) = \max \left(0, \operatorname{Re} \left\{\frac {\tilde {\Gamma} _ {n} - \hat {\Gamma} _ {x}}{\hat {\Gamma} _ {x} - \tilde {\Gamma} _ {s}} \right\}\right). \tag {18}
$$

While this estimator is unbiased, it was found to be very sensitive towards phase deviations of the coherence estimate from the ideal model [13]. For a measured coherence with a magnitude close to one, even a small phase difference between $\hat { \Gamma } _ { x }$ and $\Gamma _ { s }$ can have a large effect on the CDR estimate. This can be seen in Fig. 1b, where, unlike in Fig. 1a, the CDR for coherence values close to the unit circle sharply drops to zero, and is shown in more detail later.

Based on (17), an unbiased CDR estimator can be formulated [15]. The diffuse coherence model is first corrected to account for the phase rotation of the coherence estimate by multiplying the diffuse noise coherence $\tilde { \Gamma } _ { n }$ with the phase term $e ^ { - j 2 \pi f \widehat { \Delta t } }$ as well, which removes the bias of the estimator, while preserving the robust properties of (17) against phase errors (see Fig. 1c):

$$
\begin{array}{l} \widehat {C D R} _ {\mathrm{prop1}} (l, f) = \max \left(0, \frac {\operatorname{Re} \{e ^ {- j 2 \pi f \widehat {\Delta t}} \tilde {\Gamma} _ {n} - e ^ {- j 2 \pi f \widehat {\Delta t}} \hat {\Gamma} _ {x} \}}{\operatorname{Re} \{e ^ {- j 2 \pi f \widehat {\Delta t}} \hat {\Gamma} _ {x} \} - 1}\right) \\ = \max \left(0, \frac {\operatorname{Re} \{\tilde {\Gamma} _ {s} ^ {*} (\tilde {\Gamma} _ {n} - \hat {\Gamma} _ {x}) \}}{\operatorname{Re} \{\tilde {\Gamma} _ {s} ^ {*} \hat {\Gamma} _ {x} \} - 1}\right). \tag {19} \\ \end{array}
$$

This estimator is identical to (17) for $\widetilde { \Gamma } _ { s } = 1 , \mathrm { i . e . , } \widehat { \Delta t } = 0$ . Note that an equivalent CDR estimate can be derived from the maximum likelihood noise variance estimator which was proposed in [31] and applied to noise reduction in [32].

For a second, heuristically motivated variant of an unbiased estimator, the real part in the numerator of (19) and the max operator are first replaced by the magnitude of the entire term. The resulting estimator was found to lead to an increased performance for the application to dereverberation [33]:

$$
\widehat {C D R} _ {\text {prop2}} ^ {\prime} (l, f) = \left| \frac {\tilde {\Gamma} _ {s} ^ {*} (\tilde {\Gamma} _ {n} - \hat {\Gamma} _ {x})}{\operatorname{Re} \{\tilde {\Gamma} _ {s} ^ {*} \hat {\Gamma} _ {x} \} - 1} \right|. \tag {20}
$$

This estimator however has a small bias for non-zero TDOAs; a correction term for this bias can be computed by inserting (9) into (20) and solving for $\frac { C D R } { \widehat { C D R } _ { \mathrm { p r o p 2 } } ^ { \prime } }$ CDR [ 0prop2 . The bias-compensated estimator is then given by

$$
\widehat {C D R} _ {\text { prop2 }} (l, f) = \frac {1 - \tilde {\Gamma} _ {n} \cos (\arg (\tilde {\Gamma} _ {s}))}{| \tilde {\Gamma} _ {n} - \tilde {\Gamma} _ {s} |} \widehat {C D R} _ {\text { prop2 }} ^ {\prime} (l, f), \tag {21}
$$

and is illustrated in Fig. 1d. Compensation of this small bias however only has a negligible effect on practical performance. The derivation of these estimators shows that, when both knowledge of the signal and noise coherence are available, several different unbiased CDR estimators can be implemented. The reason for this is that the requirement of unbiasedness only defines the behavior of the estimator for coherence values matching the model given by (9), i.e., the values on the line in Fig. 1, while allowing arbitrary behavior for other coherence values. While the second proposed unbiased variant has significant practical advantages, as shown in the qualitative analysis of the estimator behavior in Section IV-E and the signal-based evaluation in Section VI, it does not seem to be optimal in any sense. A possible direction for future work would therefore be to establish a statistical model for the deviations of $\hat { \Gamma } _ { x }$ from the theoretical model given by (9), and derive a correspondingly optimized unbiased estimator.

# C. CDR Estimation for Unknown DOA

The previously shown methods rely on prior knowledge or an estimate of the target DOA. As an alternative, Thiergart et al. [11], [13] proposed to use the instantaneous phase of the estimated cross-power spectrum $\hat { \Phi } _ { x _ { 1 } x _ { 2 } }$ as a phase estimate for the direct signal model, i.e., $\tilde { \Gamma } _ { s } = e ^ { j \arg \hat { \Phi } _ { x _ { 1 } x _ { 2 } } }$ , thus removing the need for explicit DOA estimation to obtain $\tilde { \Gamma } _ { s }$ . Since, according to (14), arg $\hat { \Gamma } _ { x } = \arg \hat { \Phi } _ { x _ { 1 } x _ { 2 } }$ , this estimator can be formulated as a function of only the coherence estimate $\hat { \Gamma } _ { x }$ and the noise coherence ${ \tilde { \Gamma } } _ { n } \mathrm { : }$

$$
\widehat {C D R} _ {\text { Thiergart2 }} (l, f) = \max \left(0, \operatorname{Re} \left\{\frac {\tilde {\Gamma} _ {n} - \hat {\Gamma} _ {x}}{\hat {\Gamma} _ {x} - e ^ {j \arg \hat {\Gamma} _ {x}}} \right\}\right). \tag {22}
$$

However, the instantaneous phase of the mixture is not an unbiased estimate of the phase of the direct signal component, since, for low CDR values, the coherence of the mixture is dominated by the coherence of the diffuse signal component [13], which is real-valued, i.e., has a phase of zero. For $\theta \neq 0 ^ { \circ }$ , the estimator is therefore biased. The behavior of the estimator is illustrated in Fig. 1e.

As shown in [15], it is possible to derive an unbiased CDR estimator which does not require an estimate of the source DOA, since the knowledge that $| \Gamma _ { s } | = 1$ , i.e., that the direct signal is fully coherent, is sufficient to solve (15). This can be explained using a geometric interpretation: according to $( 9 ) , \Gamma _ { x } , \Gamma _ { i }$ s and $\Gamma _ { n }$ all lie on a straight line in the complex plane, and it is furthermore known that $\Gamma _ { s }$ lies on the unit circle and $\Gamma _ { n }$ on the real axis. $\Gamma _ { s }$ can therefore be obtained by the intersection of the line through $\Gamma _ { n }$ and $\Gamma _ { x }$ with the unit circle, and inserted into (15). An alternative way of obtaining this solution is by solving (9) for $\Gamma _ { s }$ and setting the magnitude to 1:

$$
\left| \Gamma_ {s} \right| = \left| \Gamma_ {x} - \left(\Gamma_ {n} - \Gamma_ {x}\right) C D R ^ {- 1} \right| \stackrel {!} {=} 1, \tag {23}
$$

$$
\widehat {C D R} _ {\text {prop3}} (l, f) = \frac {\tilde {\Gamma} _ {n} \operatorname{Re} \left\{\hat {\Gamma} _ {x} \right\} - \left| \hat {\Gamma} _ {x} \right| ^ {2} - \sqrt {\tilde {\Gamma} _ {n} ^ {2} \operatorname{Re} \left\{\hat {\Gamma} _ {x} \right\} ^ {2} - \tilde {\Gamma} _ {n} ^ {2} \left| \hat {\Gamma} _ {x} \right| ^ {2} + \tilde {\Gamma} _ {n} ^ {2} - 2 \tilde {\Gamma} _ {n} \operatorname{Re} \left\{\hat {\Gamma} _ {x} \right\} + \left| \hat {\Gamma} _ {x} \right| ^ {2}}}{\left| \hat {\Gamma} _ {x} \right| ^ {2} - 1} \tag {25}
$$

which leads to a quadratic equation for the CDR:

$$
\begin{array}{l} \left(\left| \Gamma_ {x} \right| ^ {2} - 1\right) C D R ^ {2} - 2 \operatorname{Re} \left\{\Gamma_ {x} \left(\Gamma_ {n} - \Gamma_ {x}\right) ^ {*} \right\} C D R \\ + \left| \Gamma_ {n} - \Gamma_ {x} \right| ^ {2} = 0. \tag {24} \\ \end{array}
$$

Taking the positive of both possible solutions yields the unbiased DOA-independent CDR estimator which is given by (25) and illustrated in Fig. 1f. In contrast to the DOAdependent estimators, where an infinite number of unbiased estimators exists, the DOA-independent estimator is uniquely determined by the requirement of unbiasedness.

# D. CDR Estimation for Unknown Noise Coherence

From the geometric interpretation of the coherence of mixed sound fields it can be analogously concluded that knowledge of $\Gamma _ { n }$ is not required when $\Gamma _ { s }$ is known, since the noise coherence is assumed to be real and therefore determined by the intersection of the real axis and the line through $\Gamma _ { s }$ and $\Gamma _ { x }$ . Using Im $\{ \Gamma _ { n } \} = 0 , \Gamma _ { n }$ can therefore be eliminated from (15), resulting in

$$
C D R = \frac {\mathrm{Im} \{\Gamma_ {x} \}}{\mathrm{Im} \{\Gamma_ {s} \} - \mathrm{Im} \{\Gamma_ {x} \}}. \tag {26}
$$

When using this formulation with the estimates $\hat { \Gamma } _ { x }$ and $\tilde { \Gamma } _ { s }$ as an estimator for the CDR, practical problems occur in cases where, due to model mismatch and coherence estimation errors, the imaginary part of the coherence estimate Im $\{ \hat { \Gamma } _ { x } \}$ has either values with a larger magnitude than Im $\{ \tilde { \Gamma } _ { s } \}$ , or a different sign, in which case this equation would not yield a meaningful result. For this reason, the CDR estimate is continuously extended into these two problematic regions by returning an infinite CDR in the former case, and a CDR of zero in the latter case. The final proposed estimator is then given by

$$
\widehat {C D R} _ {\text {prop4}} (l, f) = \left\{ \begin{array}{l l} \infty , & \text {for} \frac {\operatorname{Im} \{\hat {\Gamma} _ {x} \}}{\operatorname{Im} \{\tilde {\Gamma} _ {s} \}} \geq 1 \\ \frac {\operatorname{Im} \{\hat {\Gamma} _ {x} \}}{\operatorname{Im} \{\tilde {\Gamma} _ {s} \} - \operatorname{Im} \{\hat {\Gamma} _ {x} \}}, & \text {for} 0 <   \frac {\operatorname{Im} \{\hat {\Gamma} _ {x} \}}{\operatorname{Im} \{\tilde {\Gamma} _ {s} \}} <   1 \\ 0, & \text {for} \frac {\operatorname{Im} \{\hat {\Gamma} _ {x} \}}{\operatorname{Im} \{\tilde {\Gamma} _ {s} \}} \leq 0. \end{array} \right. \tag {27}
$$

An inherent constraint that limits practical applicability of this estimator is that arg $\Gamma _ { s } \neq 0 .$ , since otherwise the imaginary parts disappear; i.e., the estimator is not usable for $\Delta t = 0$ , and increasingly sensitive towards estimation errors for small TDOAs. The estimator is visualized in Fig. 1g. Note that in [34] a noise power spectrum estimate was derived in a similar way from the imaginary part of a cross-power spectrum.

# E. Evaluation of Estimator Bias and Robustness

To illustrate the bias of the estimators $\widehat { C D R } _ { \mathrm { J e u b } }$ , the uncompensated estimator $\widehat { C D R } _ { \mathrm { p r o p 2 } } ^ { \prime }$ and $\widehat { C D R } _ { \mathrm { T h i e r g a r t } , 2 }$ , Fig. 2 compares the true CDR value and the different estimates for mixtures of coherent and ideally diffuse signals for a TDOA $\begin{array} { r } { \Delta t { } = \frac { 1 } { 5 f } } \end{array}$ (corresponding to the values along the white line in Fig. 1, second row). The proposed estimators are all unbiased, as is the DOA-dependent estimator proposed by Thiergart et al. (18). The estimator by Jeub et al. (17) and the DOAindependent estimator by Thiergart et al. (22) both have a significant bias, with the former under- or overestimating the CDR depending on the values of ∆t and $f ,$ and the latter always underestimating the CDR. Also shown is the uncompensated version of the proposed estimator 2 (20), which has a small, TDOA- and frequency-dependent bias (for f = 3 kHz, the difference to the unbiased case is too small to be noticeable in the plot).

![](figures/8b539670df86870dc07e83cd315d3d1049817d263eb47cbd287933beb5743583.jpg)

Figure 2. Comparison of true CDR and estimated CDR. Parameters $d =$ 8 cm, $\widehat { \Delta t } = \Delta t { \dot { = } } \frac { 1 } { 5 f } , f = 1$ kHz (left), 3 kHz (right).   
![](figures/0f965e6e32a182c91548ee198f8e7315af853020ea1fc5d41425d31c1ca000a6.jpg)

![](figures/f158fe9f9b86dd27cd625492963f363c96b478da6786b99c9368f24645fade87.jpg)

<details>
<summary>line</summary>

| Method | CDR = 10 dB (arg Γ̃_s - arg Γ_s [rad]) | CDR = 10 dB (arg Γ̃_n - Γ_n) |
|---|---|---|
| proposed 2 | 0 | 0 |
| proposed 1 | 0 | 0 |
| Thiergart 1 | 0 | 0 |
| proposed 3 | 0 | 0 |
</details>

Figure 3. CDR estimation error for noise and direct signal coherence model errors. Parameters d = 8 cm, ∆ct = 15f , f = 1 kHz.

Fig. 3 shows the CDR estimation error for cases where the actual coherence of the noise $\Gamma _ { n }$ or the direct signal component $\Gamma _ { s }$ deviates from the assumed coherence models $\tilde { \Gamma } _ { n }$ and $\tilde { \Gamma } _ { s } ,$ respectively. Fig. 3a and b show the error for a low CDR of −10 dB, while c and d show results for a high CDR of 10 dB. The DOA-independent estimator $\widehat { C D R } _ { \mathrm { p r o p 3 } }$ is naturally unaffected by the phase error of the direct signal coherence model, as seen in Fig. 3b and d; however, for errors of the noise coherence, the CDR is quickly overestimated by the DOA-independent estimator (see Fig. 3a). The estimator $\widehat { C D R } _ { \mathrm { T h i e r g a r t , 1 } }$ has the problem of reacting strongly to small phase deviations when the CDR is high (see Fig. 3d). Comparing the different unbiased DOA-dependent variants $\widehat { C D R } _ { \mathrm { p r o p l } }$ and $\widehat { C D R } _ { \mathrm { p r o p } 2 }$ , it can be stated that $\widehat { C D R } _ { \mathrm { p r o p } 2 }$ seems slightly more tolerant towards model errors, which could explain the better performance of this estimator for signal enhancement.

![](figures/943f4509d2dea0b2d06b3acc5c072181b1dfa77b2297db8bf635b6c695c807c7.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["X₁(l,f)"] --> B["Preprocessing"]
    C["X₂(l,f)"] --> B
    B --> D["Y(l,f)"]
    D --> E["G(l,f)"]
    E --> F["Z(l,f)"]
    G["TDOA estimation"] --> H["Coherence estimation"]
    H --> I["\hat{\Gamma}_x(k,f)"]
    I --> J["CDR estimation"]
    J --> K["\hat{\Gamma}_s(f)"]
    J --> L["\hat{\Gamma}_n(f)"]
    K --> M["\Delta t"]
    L --> M
    M --> N["\widehat{CDR}(l,f)"]
    N --> E
```
</details>

Figure 4. Coherence-based noise and reverberation suppression system consisting of a preprocessor and a CDR-based postfilter.

# V. APPLICATION TO SPEECH ENHANCEMENT

Fig. 4 shows the structure of the proposed reverberation or diffuse noise suppression system based on short-time CDR estimates. First, the microphone signals are combined by averaging the squared magnitudes and using the phase from one of the microphone signals:

$$
Y (l, f) = \frac {1}{2} \sqrt {\left| X _ {1} (l , f) \right| ^ {2} + \left| X _ {2} (l , f) \right| ^ {2}} \cdot e ^ {j \arg X _ {1} (l, f)}. \tag {28}
$$

Spatial magnitude averaging in the STFT domain is typically used to reduce the variance of spectral estimates for the computation of microphone array postfilters [9], but has also been used as a preprocessor for signal enhancement [35]. It is used here with the purpose of reducing the variations in the transfer function which are caused by constructive and destructive interference of early reflection components with the direct path. For the computation of the coherence-based postfilter gain $G ( l , f )$ , short-time estimates ${ \hat { \Gamma } } _ { x } ( l , f )$ of the spatial coherence are first obtained according to (14) from spectra which have been estimated by recursive averaging. From the coherence, the CDR is estimated based on models for the direct signal and/or reverberation coherence, where the direct signal coherence is derived from a known or estimated TDOA, and the reverberation coherence is assumed to be known. A postfilter gain is then computed using spectral magnitude subtraction [29]:

$$
G (l, f) = \max \left\{G _ {\min}, 1 - \sqrt {\frac {\mu}{\widehat {C D R} (l , f) + 1}} \right\}, \tag {29}
$$

with the oversubtraction factor $\mu$ and the gain floor $G _ { \mathrm { m i n } }$ . The output signal is computed by applying the postfilter gain to the preprocessed signal $Y ( l , f ) , { \mathrm { i . e . , } } Z ( l , f ) = G ( l , f ) Y ( l , f )$ , and transformed back into the time domain. Since the preprocessor does not have any spatial filtering effect, the postfilter gain can be directly applied to the preprocessor output, and does not require a correction to account for spatial filtering, as it would be the case for a beamformer as preprocessor [8].

Note that, when employing a DOA-independent CDR estimator, the proposed signal enhancement system is completely independent of the DOA of the target signal.

# VI. EVALUATION

In the following, the spatial properties of reverberation are first evaluated using simulated and measured RIRs, in order to verify the assumptions made in Sect. III-B. Then, the estimation accuracy of the CDR estimators and the effect of the proposed CDR-based dereverberation system are evaluated.

A MATLAB implementation of the proposed CDR estimators and signal enhancement scheme is provided online1.

# A. Setup and Parameters

For the main evaluation, sets of measured RIRs from three rooms are used:

• Room A: 6 m × 6 m × 3 m, partially closed curtains on walls, $T _ { 6 0 } \approx 0 . 4 \ : \mathrm { s }$   
• Room B: 7 m × 11 m × 3 m (lecture hall), $T _ { 6 0 } \approx 1$ s   
• Room C: 54 m × 7 m × 3 m (large foyer). $T _ { 6 0 } \approx 3 . 5 \mathrm { s }$

The reverberation time $T _ { 6 0 }$ was measured from the energy decay curve of the RIR. In each room, RIRs were measured for 40-70 different source positions in l = 1, 2 and 4 m distance from the microphones, in the angular range $\theta = - 9 0 \ldots 9 0 ^ { \circ }$ . Microphones are spaced d =8 cm apart.

Additionally, the RIRs that were used in the REVERB challenge [36] for the generation of multi-condition training data are evaluated. These RIRs were measured using an 8- channel circular microphone array with a diameter of 20 cm (corresponding to d = 8 cm spacing between neighboring microphones) in 6 different rooms (SR1/2, MR1/2, LR1/2), for two source-microphone distances (≈0.5 m and ≈2 m), and two different angles of the source w.r.t. the microphone array. The rooms have the following properties (note that SR2 and LR2 are the same rooms as A and B, respectively):

• SR1 (“Small Room 1”): variable reverberation room, $4 . 5 \mathrm { m } \times 3 . 5 \mathrm { m } \times 3 \mathrm { m } , T _ { 6 0 } \approx 0 . 2 \mathrm { s }$   
• SR2 (“Small Room 2”): room A, but curtains fully closed, $T _ { 6 0 } \approx 0 . 2 \mathrm { s }$   
• MR1 (“Medium Room 1”): same as SR1, $T _ { 6 0 } \approx 0 . 5 \mathrm { s }$   
• MR2 (“Medium Room 2”): meeting room, 5 m×3.5 m× $3 \mathrm { m } , T _ { 6 0 } \approx 0 . 6 \mathrm { s }$   
• LR1 (“Large Room 1”): same as $\mathrm { S R 1 } , T _ { 6 0 } \approx 0 . 8 \mathrm { s }$   
• LR2 (“Large Room 2”): room B

In the following, all processing takes place at a sampling rate of 16 kHz. For the transformation into the time-frequency domain and short-time spectral estimation, a DFT-based uniform filterbank with window length 1024, FFT size 512, and downsampling factor 128 is employed [37]. The short-time

(a) Reflective room (β = 0.9)   
![](figures/c2ef20874a1846f58b011171df78fd1ef73259e86e2b228a59d5f4692643fc40.jpg)

<details>
<summary>line</summary>

| f[kHz] | Re{Γ} (Red Line) | Re{Γ} (Blue Dashed Line) |
|--------|------------------|--------------------------|
| 0      | 1.0              | 1.0                      |
| 2      | -0.5             | -0.3                     |
| 4      | 0.2              | 0.1                      |
| 6      | -0.1             | -0.2                     |
| 8      | 0.0              | 0.0                      |
</details>

(b) Absorbing floor and ceiling (βWalls = 0.9, βFloor, Ceil = 0.1)   
![](figures/a365132435cc86d9dc7305b1c5279de94b7d8d87f7e45903f4c09869e6cb71c0.jpg)

<details>
<summary>line</summary>

| f [kHz] | Re{Γ} (Solid) | Re{Γ} (Dashed) |
| ------- | ------------- | -------------- |
| 0       | 1.0           | 1.0            |
| 2       | -0.5          | -0.2           |
| 4       | 0.2           | 0.1            |
| 6       | 0.0           | -0.1           |
| 8       | -0.1          | -0.2           |
</details>

(c) Absorbing walls (βWalls = 0.5, βFloor, Ceiling = 0.9)   
![](figures/abd1a038517cac4e206fb480267a7973cf42aaad3f001c691c3e13c830ac4110.jpg)

<details>
<summary>line</summary>

| f [kHz] | Re{Γ} (Red Solid) | Re{Γ} (Blue Dashed) |
| ------- | ----------------- | ------------------- |
| 0       | 1.0               | 1.0                 |
| 2       | ~0.8              | ~0.5                |
| 4       | ~0.6              | ~0.0                |
| 6       | ~0.4              | ~-0.2               |
| 8       | ~0.3              | ~-0.3               |
</details>

3D isotropic 2D isotropic measured

Figure 5. Spatial coherence estimated from the reverberation tail of simulated RIRs, averaged over 7 microphone pairs with spacing $d = 8 \mathrm { c m } .$ , for different reflection coefficients $\beta ,$ compared to coherence of diffuse and 2D isotropic sound fields. Left: small room $( 4 \times 3 \times 2 . 5 \mathrm { m } )$ , right: large room $( 1 5 \times 1 8 \times$ 10 m).

coherence estimates are obtained by recursive averaging of the auto- and cross-power spectra according to (13), with the forgetting factor $\lambda = 0 . 6 8$ .

# B. Spatial Properties of Reverberation in Simulated and Measured Rooms

For the evaluation of the spatial characteristics of reverberation, we use simulated and measured RIRs. The reverberation tail of the RIRs is extracted by removing the initial part containing the direct path and early reflections (see Appendix), using a typical value of $T _ { \mathrm { e } } = 5 0$ ms for the cutoff time between early reflections and reverberation [20]. The late RIRs are convolved with a speech signal, transformed into the STFT domain, and the spatial coherence is estimated from auto- and cross-power spectra estimated by averaging over an interval of 10 s.

First, RIRs are generated using the image method [25], [38]. In the simulations, a uniform linear array (inter-microphone spacing $d = 8 \mathrm { c m } )$ is placed horizontally in the center of rectangular rooms with varying dimensions and reflectivities. The image source order is chosen sufficiently high to include all reflections within 60 dB of the main peak. In order to reduce the variance of the estimate for a better visualization, the

(a) Small room 1   
![](figures/049a5a133f86e727fdd0dbb62a15ae1ab79c4791864691b18b70dab513400624.jpg)

<details>
<summary>line</summary>

| f [kHz] | Re{Γ} (Red Line) | Re{Γ} (Blue Dashed Line) |
| ------- | ---------------- | ------------------------ |
| 0       | 1.0              | 1.0                      |
| 1       | 0.5              | 0.5                      |
| 2       | -0.5             | -0.5                     |
| 3       | 0.0              | 0.0                      |
| 4       | 0.5              | 0.5                      |
| 5       | 0.0              | 0.0                      |
| 6       | -0.5             | -0.5                     |
| 7       | 0.0              | 0.0                      |
| 8       | -0.5             | -0.5                     |
</details>

(b) Small room 2   
![](figures/d6bf3f95aa75a25d330c9b4df62995aee6760c5ac1d2d72cae341667190f949b.jpg)

<details>
<summary>line</summary>

| f[kHz] | Value |
| ------ | ----- |
| 0      | 1.0   |
| 1      | 0.5   |
| 2      | 0.2   |
| 3      | 0.8   |
| 4      | 0.3   |
| 5      | 0.7   |
| 6      | 0.4   |
| 7      | 0.6   |
| 8      | 0.5   |
</details>

(c) Medium room 1   
![](figures/4e3cb1885b8094dbc520bf0b177fd69ff12bf484aa2b2eb4ace134e66e22b841.jpg)

<details>
<summary>line</summary>

| f [kHz] | Re{Γ} (Red Line) | Re{Γ} (Blue Dashed Line) |
| ------- | ---------------- | ------------------------ |
| 0       | 1.0              | 1.0                      |
| 1       | ~0.3             | ~0.2                     |
| 2       | ~-0.2            | ~-0.3                    |
| 3       | ~-0.1            | ~-0.1                    |
| 4       | ~0.2             | ~0.1                     |
| 5       | ~0.3             | ~0.2                     |
| 6       | ~0.1             | ~0.0                     |
| 7       | ~-0.1            | ~-0.1                    |
| 8       | ~-0.2            | ~-0.2                    |
</details>

(d) Medium room 2   
![](figures/ebf2743b0f4c93adf08e8c488a6d5bc0ba9a88f1a085ab29260197f6b3fa0920.jpg)

<details>
<summary>line</summary>

| f[kHz] | Value |
| ------ | ----- |
| 0      | 1.0   |
| 2      | -0.5  |
| 4      | 0.8   |
| 6      | -0.3  |
| 8      | 0.2   |
</details>

(e) Large room 1   
![](figures/0eb80445a10e089bf06d55ffd46993d70067704d3a8ce58d3710b03a3e818f10.jpg)

<details>
<summary>line</summary>

| f [kHz] | Re{Γ} (Red Line) | Re{Γ} (Blue Dashed Line) |
| ------- | ---------------- | ------------------------ |
| 0       | 1.0              | 1.0                      |
| 1       | ~0.5             | ~0.5                     |
| 2       | ~-0.2            | ~-0.3                    |
| 3       | ~-0.1            | ~-0.1                    |
| 4       | ~0.2             | ~0.1                     |
| 5       | ~0.3             | ~0.2                     |
| 6       | ~0.1             | ~0.1                     |
| 7       | ~0.2             | ~0.1                     |
| 8       | ~0.1             | ~0.1                     |
</details>

(f) Large room 2   
![](figures/b4478b32fdf911b9735e8cfe688393fcfb0b570483ba184d8ff14840c6566ca3.jpg)

<details>
<summary>line</summary>

| f [kHz] | Value |
| ------- | ----- |
| 0       | 1.0   |
| 1       | 0.5   |
| 2       | 0.2   |
| 3       | 0.1   |
| 4       | 0.3   |
| 5       | 0.6   |
| 6       | 0.4   |
| 7       | 0.3   |
| 8       | 0.2   |
</details>

3D isotropic 2D isotropic measured

Figure 6. Spatial coherence estimated from the reverberation tail of measured RIRs from the REVERB challenge, averaged over 7 microphone pairs with spacing $d = 8 \mathrm { c m }$ . coherence is also spatially averaged over the estimates from 7 microphone pairs [24]. Fig. 5 shows plots of the real part of the resulting coherence, for a large room $( 1 5 \times 1 8 \times 1 0 \mathrm { m } .$ , left) and a small room $( 4 \times 3 \times 2 . 5 \mathrm { m }$ , right); for both rooms, three configurations for the surface reflectivity $\beta$ are used: equally high reflectivity for all surfaces $( \beta ~ = ~ 0 . 9 )$ , highly absorbing floor and ceiling $( \beta _ { \mathrm { { W a l l s } } } = 0 . 9 , \beta _ { \mathrm { { F l o o r , C e i l } } } = 0 . 1 )$ , and moderately absorbing walls $( \beta _ { \mathrm { W a l l s } } = 0 . 5 , \beta _ { \mathrm { F l o o r , C e i l } } = 0 . 9 )$ . The results in Fig. 5 confirm the assumptions on the coherence properties of reverberation that were made in Section III-B: for equal reflectivity of all surfaces, the coherence closely matches the coherence of the diffuse sound field. If floor and ceiling are highly absorbing, the model of a 2D isotropic sound field is appropriate. If instead the walls are more absorbing than floor and ceiling, the coherence is significantly higher than the diffuse coherence, since the dominating vertically propagating components are strongly correlated between the horizontally spaced microphones. Also, the variance of the coherence estimate is visibly lower in the larger room.

Fig. 6 shows the reverberation coherence estimates obtained from the RIRs of the REVERB challenge database, estimated in the same way as for the simulated RIRs. The coherence estimates are obtained for 7 pairs of neighboring microphones from the circular array and averaged. Most rooms match the

![](figures/7b1954cc58c1a3ccaa3675270633f098c747d70c9677e177d2c96b41c66d2718.jpg)  
3D isotropic 2D isotropic measured

Figure 7. Spatial coherence estimated from the reverberation tail of measured RIRs in rooms A, B, C, one microphone pair with spacing d = 8 cm.

diffuse model quite well, with two exceptions. In SR2, the coherence is higher than expected from the diffuse model, which can be explained by the presence of absorbing curtains on all four walls. In MR2, the coherence however almost perfectly matches the 2D isotropic model, since in this room, walls are more reflective than floor and ceiling. Also, it can again be observed that the variance of the coherence estimate is lower for rooms with a longer reverberation time.

Fig. 7 shows the results for one position in the rooms A, B and C. The coherence estimate is here computed just from one pair of microphones, therefore the variance is significantly higher. The diffuse model is a good fit for rooms B and $\mathrm { C } ,$ where all surfaces are highly reflective. In room A, the coherence is similar to the simulated case of partially absorbing walls, which is due to the presence of partially closed curtains on the walls of the room.

Concluding the analysis of the spatial properties, it can be stated that, for microphones located in the same horizontal plane, the spatial coherence of reverberation in real rooms typically lies between the coherence of diffuse and 2D isotropic noise, with some exceptions where the coherence is increased due to dominant vertical reflections. The diffuse model is a good fit for most rooms, unless there are large differences in the reflectivity of the room surfaces. Finally, it is noteworthy that the image source model with sufficient order can reproduce the spatial characteristics of late reverberation which are observed in real rooms.

# C. CDR Estimation for Reverberant Speech

In Section II, a reverberant speech signal is modeled as consisting of a directional and a diffuse component, which are mutually uncorrelated. In practice, the reverberant sound field consists of the direct path, several spatially distinct early reflections, and the reverberation component, all of which are not perfectly uncorrelated, due to the non-zero length of the observation window and the temporal correlation of speech signals. In the previous section, it was shown that the model of a diffuse sound field is appropriate for the reverberation component. In the following, it is investigated whether the simplified model of a mixture of uncorrelated directional and diffuse sound fields can be applied to real reverberant speech signals, i.e., whether the CDR estimate can be used as a practical measure for the time- and frequency-dependent ratio between desired and undesired signal components, as it is required for speech enhancement. We now consider the desired signal components to be the direct path plus the reflections arriving within $T _ { \mathrm { e } } = 5 0 \mathrm { m s }$ after the direct path, and the undesired components to be the energy caused by the reverberation tail of the RIR. This is motivated by the well-known effect that early reflections are beneficial both for speech intelligibility [39] and ASR accuracy [40], and should therefore be considered part of the desired signal. In other words, the relevant SNR to be estimated for the application to signal enhancement is the early-to-late power ratio $E L R _ { 5 0 \mathrm { m s } } ( l , f )$ (see Appendix).

To exemplarily illustrate the relationship between the (nonstationary) early-to-late power ratio and the short-time coherence estimate, the time-frequency bins of a reverberant speech signal are first classified according to the instantaneous $E L R _ { \mathrm { 5 0 m s } }$ into low-reverberant and highly reverberant, and the corresponding distribution of the short-time estimates of the complex coherence is visualized as a histogram. Fig. 8 shows the two-dimensional histograms of the complex coherence of bins with $E L R > 1 0 \mathrm { d B }$ (left) and $E L R < - 1 0 \mathrm { d B }$ (right) around $f \mathrm { ~ = ~ } 1 \mathrm { k H z }$ . The coherence of the low-reverberant bins matches the coherence of a single plane wave quite well, although the signal contains contributions from early reflections in addition to the direct path. The phase has a slight spread, caused by early reflections; this has to be tolerated by the CDR estimator. The coherence of the highly reverberant bins, which should lie close to the diffuse model coherence, has a considerably higher spread and is not exactly centered around the model. This indicates that, while the simplified model seems to be reasonable, errors are non-negligible, and the differences in the realizations of the unbiased estimators, which affect only the behavior for values deviating from the ideal model, are likely to have a significant impact on estimation performance.

For the comparison of the estimation performance of the different estimators, it is convenient to transform the true and estimated CDR into the true and estimated diffuseness $D = [ C D R + 1 ] ^ { - 1 }$ and $\hat { D } \ = \ [ \widehat { C D R } + 1 ] ^ { - 1 }$ , respectively, due to the diffuseness being bounded between 0 and 1, and to evaluate the mean squared error $\widehat { M S E } = \mathcal { E } \{ | D - \hat { D } | ^ { 2 } \}$ . For this evaluation, the true CDR is again approximated by the ELR $( C D R \approx E L R _ { 5 0 \mathrm { m s } } )$ , and the expectation is approximated by averaging over time and frequency. The coherence models $\tilde { \Gamma } _ { s }$ and $\tilde { \Gamma } _ { n }$ for the estimators are based on the measured TDOA and the diffuse coherence assumption, respectively. Table II shows the MSE for the different estimators, averaged over all source positions in the respective room. The estimator $\widehat { C D R } _ { \mathrm { T h i e r g a r t , 1 } }$ has a relatively high estimation error, due to the high sensitivity of this estimator towards phase variation of the coherence. The estimator $\widehat { C D R } _ { \mathrm { p r o p 1 } }$ shows a slightly reduced estimation error compared to the biased estimator $\hat { C } D \hat { R } _ { \mathrm { J e u b } }$ , while the variant $\hat { C } D \hat { R } _ { \mathrm { p r o p } 2 }$ further reduces the error. Among the DOA-independent estimators, the proposed unbiased version leads to an error reduction as well, while the noise coherence-independent variant $\overline { { C } } \widehat { D R } _ { \mathrm { p r o p 4 } }$ has the overall second-highest error, due to the difficulties in cases where the phase of the coherence is close to zero.

![](figures/3bc0f9164d46be2e0789679adffa094cabf997486d7d6af23a952e4159bc0807.jpg)

<details>
<summary>scatter</summary>

| Re{Γ̂ₓ} | Im{Γ̂ₓ} | Occurrences |
|--------|--------|-------------|
| 0.5    | 0.0    | Yes         |
</details>

Figure 8. Histogram of complex coherence values $\hat { \Gamma } _ { x }$ measured from a reverberant speech signal, for time-frequency bins with $E L R _ { 5 0 \mathrm { m s } } >$ 10 dB (left) and $< - 1 0 \mathrm { d B }$ (right). Room B, $l = 2$ m, $d = 8$ cm, $\theta = 6 0 ^ { \circ } , \ : f =$ 1 kHz). Theoretical signal coherence $\Gamma _ { s }$ computed from measured TDOA and diffuse noise coherence $\Gamma _ { n }$ are marked by ◦ and $\times ,$ respectively.

Table II ESTIMATION ERROR OF DIFFERENT CDR ESTIMATORS. 

<table><tr><td>CDR est.</td><td>Jeub</td><td>Thiergart 1 *</td><td>proposed 1 *</td><td>proposed 2 *</td><td>Thiergart 2</td><td>proposed 3 *</td><td>proposed 4 *</td></tr><tr><td>Prior inform.</td><td>DOA,  $\Gamma_n$ </td><td>DOA,  $\Gamma_n$ </td><td>DOA,  $\Gamma_n$ </td><td>DOA,  $\Gamma_n$ </td><td> $\Gamma_n$ </td><td> $\Gamma_n$ </td><td>DOA</td></tr><tr><td>Room A</td><td>0.182</td><td>0.486</td><td>0.166</td><td>0.095</td><td>0.062</td><td>0.057</td><td>0.243</td></tr><tr><td>Room B</td><td>0.146</td><td>0.301</td><td>0.140</td><td>0.086</td><td>0.090</td><td>0.087</td><td>0.212</td></tr><tr><td>Room C</td><td>0.080</td><td>0.235</td><td>0.080</td><td>0.066</td><td>0.103</td><td>0.104</td><td>0.159</td></tr><tr><td>MR1</td><td>0.131</td><td>0.373</td><td>0.114</td><td>0.069</td><td>0.059</td><td>0.052</td><td>0.171</td></tr><tr><td>MR2</td><td>0.111</td><td>0.287</td><td>0.092</td><td>0.061</td><td>0.073</td><td>0.066</td><td>0.159</td></tr><tr><td>LR1</td><td>0.119</td><td>0.313</td><td>0.109</td><td>0.068</td><td>0.067</td><td>0.063</td><td>0.170</td></tr><tr><td>LR2</td><td>0.073</td><td>0.262</td><td>0.059</td><td>0.047</td><td>0.071</td><td>0.069</td><td>0.134</td></tr><tr><td>Mean</td><td>0.120</td><td>0.322</td><td>0.109</td><td>0.070</td><td>0.075</td><td>0.071</td><td>0.178</td></tr></table>

# D. Dereverberation Performance

In the following, the signal enhancement system described in Section V is evaluated for the application to dereverberation. For all of the following results, two-channel signals are processed by first applying spatial magnitude averaging as described by (28), and then applying a postfilter based on the different CDR estimators, or one of several other dereverberation methods used for comparison.

1) Measures and Evaluation Method: To quantify the amount of reverberation in the unprocessed and processed signals, the time- and frequency-averaged early-to-late power ratio $E L R _ { \mathrm { 5 0 m s } }$ is evaluated (see Appendix). The amount of signal distortion caused by the postfilter is quantified by the frequency-weighted segmental signal-to-distortion ratio (fwSegSDR), which we define as the fwSegSNR [41] computed for the postfiltered early signal component (i.e., the signal convolved with the first 50 ms of the RIR), with the unprocessed early signal component $Y _ { e }$ as the reference:

$$
f w S e g S D R = f w S e g S N R (Y _ {e} (l, f), G (l, f) Y _ {e} (l, f)) \tag {30}
$$

The overall quality of the processed signals, including both the effects of reverberation reduction and undesired speech distortion, is evaluated using the recognition rate of an automatic speech recognizer. The ASR engine PocketSphinx [42] is used with an acoustic model trained on clean speech from the GRID corpus [43], using $\mathbf { M F C C + } \Delta { + } \Delta \Delta$ features. Cepstral mean normalization is used for the equalization of the effect of early reverberation [44]. For the computation of the recognition rate, only the letter and the number in the utterance are evaluated, as in the CHiME challenge [45]. Furthermore, two signal-based measures for the overall speech quality are evaluated, which were shown to be significantly correlated to the perceived amount of reverberation [46]: PESQ [47] and the frequencyweighted segmental signal-to-noise ratio (fwSegSNR) [41]. We use the wideband version of PESQ and give values in the MOS-LQO scale. For both PESQ and the fwSegSNR, the clean speech signal is used as reference.

CDR-based dereverberation is evaluated with all estimators discussed in this paper. In addition to the CDR-based methods, two heuristic coherence-based postfiltering methods are evaluated: a version of Allen’s method [2], where the magnitude of the coherence is used as a spectral gain and applied to the spatially preprocessed signal, and the coherence-to-gainmapping proposed by Westermann et al. [7], which depends on a histogram of the magnitude squared coherence. Also evaluated is the exponential decay model by Lebart et al. [48], using the true reverberation times measured from the RIRs, which in practice would have to be estimated blindly from the reverberant signals [49]. For the method of Lebart and the CDR-based methods, spectral magnitude subtraction according to (29) is applied, with $G _ { \mathrm { m i n } } = 0 . 1$ . The suppression parameter $\mu$ is set to 1.3, which yields close to optimum recognition rates for all except Lebart’s method (see the comment in the following section). Ideal TDOA knowledge is assumed for the CDR estimators which require a TDOA estimate $\widehat { \Delta t } .$ , i.e., $\widehat { \Delta t } \ = \ \Delta t$ . The dereverberation methods are evaluated for the rooms A, B, C, MR1/2 and LR1/2. In SR1/2, the very low amount of reverberation $( T _ { 6 0 } < 0 . 3 \mathrm { s } )$ did not lead to a significantly lower recognition rate compared to clean speech, therefore these rooms are not included in the evaluation. For each room and source position, 500 GRID utterances are convolved with the measured two-channel RIRs (in the case of the REVERB challenge RIRs, two neighboring microphones are selected from the circular array), and then processed by the dereverberation methods.

2) Results: Table III summarizes the resulting performance measurements, averaged over all source positions in each room. The first column shows the results for the unprocessed microphone signals. The spatial magnitude averaging leads to a small but consistent improvement in all performance measures, as seen in the second column.

Postfiltering using the CDR estimator $\widehat { C D R } _ { \mathrm { p r o p } 2 }$ leads to the highest recognition rate among all methods across all evaluated rooms, as well as to the highest average PESQ score. Comparing the CDR-based methods, the following observations can be made: both for the DOA-dependent and DOA-independent estimators, all measures reflect the slight advantage of the respective unbiased variant $( \widehat { C D R } _ { \mathrm { p r o p 1 } }$ and ${ \widehat { C D R } } _ { \mathrm { p r o p } 3 } ,$ , respectively) over the biased estimators. For the DOA-dependent estimator, the variant $\widehat { C D R } _ { \mathrm { p r o p } 2 }$ further improves the result over the first proposed unbiased estimator, due to the different behavior of this estimator for coherence values which deviate from the ideal coherence model. The significant improvement suggests that further improvement may be possible by modeling these deviations statistically and explicitly optimizing the estimator for this model. Remarkable are the results of the DOA-independent estimators: without requiring any knowledge or estimation of source DOA or other parameters of the scenario, the CDR-based postfilter can significantly increase the overall signal quality according to all evaluated measures.

Table III PERFORMANCE MEASURES, AVERAGED OVER ALL SOURCE POSITIONS IN EACH ROOM. FIRST COLUMN: UNPROCESSED MICROPHONE SIGNAL, SECOND COLUMN: SPATIALLY AVERAGED MAGNITUDES WITHOUT POSTFILTERING, REMAINING COLUMNS: DIFFERENT POSTFILTERS. 

<table><tr><td colspan="2">Preprocessor</td><td>-</td><td colspan="11">Squared Magnitude Averaging</td></tr><tr><td rowspan="3" colspan="2">Postfilter</td><td rowspan="3">-</td><td rowspan="3">-</td><td rowspan="3">Lebart</td><td colspan="9">Coherence-based</td></tr><tr><td rowspan="2">Allen</td><td rowspan="2">Westermann</td><td colspan="7">CDR-based</td></tr><tr><td>Jeub</td><td>Thiergart 1*</td><td>proposed 1*</td><td>proposed 2*</td><td>Thiergart 2</td><td>proposed 3*</td><td>proposed 4*</td></tr><tr><td colspan="2">Required</td><td>-</td><td>-</td><td> $T_{60}$ </td><td>-</td><td>Coh. histog.</td><td>DOA,  $\Gamma_n$ </td><td>DOA,  $\Gamma_n$ </td><td>DOA,  $\Gamma_n$ </td><td>DOA,  $\Gamma_n$ </td><td> $\Gamma_n$ </td><td> $\Gamma_n$ </td><td>DOA</td></tr><tr><td colspan="2">Parameter</td><td>-</td><td>-</td><td> $\mu=1.3$ </td><td>-</td><td> $k_p=0.30$ </td><td> $\mu=1.3$ </td><td> $\mu=1.3$ </td><td> $\mu=1.3$ </td><td> $\mu=1.3$ </td><td> $\mu=1.3$ </td><td> $\mu=1.3$ </td><td> $\mu=1.3$ </td></tr><tr><td rowspan="8">Recognition Rate [%]</td><td>Room A</td><td>87.0</td><td>87.1</td><td>87.7</td><td>89.0</td><td>89.9</td><td>89.0</td><td>86.2</td><td>89.4</td><td>90.0</td><td>89.8</td><td>89.9</td><td>88.2</td></tr><tr><td>Room B</td><td>49.2</td><td>49.9</td><td>69.5</td><td>63.5</td><td>67.5</td><td>76.0</td><td>64.7</td><td>76.4</td><td>78.2</td><td>72.4</td><td>73.0</td><td>67.7</td></tr><tr><td>Room C</td><td>36.4</td><td>36.6</td><td>47.8</td><td>48.1</td><td>51.7</td><td>65.7</td><td>53.2</td><td>67.6</td><td>68.6</td><td>55.8</td><td>56.3</td><td>59.5</td></tr><tr><td>MR1</td><td>77.2</td><td>78.2</td><td>84.8</td><td>83.6</td><td>85.0</td><td>85.6</td><td>78.9</td><td>86.6</td><td>87.0</td><td>86.1</td><td>86.3</td><td>84.1</td></tr><tr><td>MR2</td><td>63.9</td><td>65.7</td><td>80.0</td><td>74.5</td><td>76.6</td><td>80.1</td><td>70.8</td><td>80.7</td><td>81.9</td><td>79.8</td><td>80.2</td><td>75.9</td></tr><tr><td>LR1</td><td>64.8</td><td>65.1</td><td>77.3</td><td>72.8</td><td>75.4</td><td>78.9</td><td>70.2</td><td>79.4</td><td>81.1</td><td>77.9</td><td>78.8</td><td>75.7</td></tr><tr><td>LR2</td><td>57.2</td><td>58.8</td><td>75.5</td><td>70.4</td><td>73.8</td><td>82.7</td><td>71.6</td><td>83.3</td><td>83.5</td><td>78.6</td><td>78.9</td><td>79.4</td></tr><tr><td>Mean</td><td>62.2</td><td>63.1</td><td>74.7</td><td>71.7</td><td>74.3</td><td>79.7</td><td>70.8</td><td>80.5</td><td>81.5</td><td>77.2</td><td>77.6</td><td>75.8</td></tr><tr><td rowspan="8">PESQ</td><td>Room A</td><td>1.51</td><td>1.53</td><td>1.72</td><td>1.58</td><td>1.64</td><td>1.67</td><td>1.46</td><td>1.67</td><td>1.76</td><td>1.64</td><td>1.66</td><td>1.65</td></tr><tr><td>Room B</td><td>1.19</td><td>1.19</td><td>1.34</td><td>1.23</td><td>1.25</td><td>1.36</td><td>1.26</td><td>1.34</td><td>1.38</td><td>1.27</td><td>1.28</td><td>1.29</td></tr><tr><td>Room C</td><td>1.13</td><td>1.13</td><td>1.23</td><td>1.14</td><td>1.16</td><td>1.31</td><td>1.21</td><td>1.32</td><td>1.32</td><td>1.17</td><td>1.17</td><td>1.26</td></tr><tr><td>MR1</td><td>1.28</td><td>1.29</td><td>1.46</td><td>1.33</td><td>1.41</td><td>1.37</td><td>1.26</td><td>1.37</td><td>1.45</td><td>1.41</td><td>1.43</td><td>1.38</td></tr><tr><td>MR2</td><td>1.30</td><td>1.33</td><td>1.56</td><td>1.40</td><td>1.48</td><td>1.43</td><td>1.28</td><td>1.45</td><td>1.57</td><td>1.56</td><td>1.56</td><td>1.50</td></tr><tr><td>LR1</td><td>1.18</td><td>1.19</td><td>1.33</td><td>1.21</td><td>1.25</td><td>1.24</td><td>1.18</td><td>1.22</td><td>1.27</td><td>1.24</td><td>1.25</td><td>1.25</td></tr><tr><td>LR2</td><td>1.28</td><td>1.31</td><td>1.57</td><td>1.37</td><td>1.50</td><td>1.54</td><td>1.27</td><td>1.57</td><td>1.61</td><td>1.58</td><td>1.58</td><td>1.54</td></tr><tr><td>Mean</td><td>1.27</td><td>1.28</td><td>1.46</td><td>1.32</td><td>1.38</td><td>1.42</td><td>1.27</td><td>1.42</td><td>1.48</td><td>1.41</td><td>1.42</td><td>1.41</td></tr><tr><td rowspan="8">fwSegSNR</td><td>Room A</td><td>6.15</td><td>6.58</td><td>8.34</td><td>7.94</td><td>8.96</td><td>7.17</td><td>7.14</td><td>8.63</td><td>8.48</td><td>8.71</td><td>8.73</td><td>6.94</td></tr><tr><td>Room B</td><td>2.07</td><td>2.15</td><td>6.13</td><td>4.20</td><td>3.92</td><td>4.46</td><td>4.15</td><td>5.81</td><td>5.45</td><td>5.38</td><td>5.40</td><td>4.04</td></tr><tr><td>Room C</td><td>1.08</td><td>1.31</td><td>4.58</td><td>2.89</td><td>3.20</td><td>2.42</td><td>2.46</td><td>3.79</td><td>3.60</td><td>3.93</td><td>3.93</td><td>2.32</td></tr><tr><td>MR1</td><td>6.97</td><td>7.09</td><td>7.94</td><td>7.58</td><td>8.51</td><td>6.72</td><td>6.21</td><td>7.41</td><td>7.76</td><td>7.86</td><td>7.88</td><td>7.20</td></tr><tr><td>MR2</td><td>5.63</td><td>5.84</td><td>7.28</td><td>6.81</td><td>7.64</td><td>6.68</td><td>5.85</td><td>7.31</td><td>7.52</td><td>7.59</td><td>7.59</td><td>7.15</td></tr><tr><td>LR1</td><td>5.65</td><td>5.66</td><td>6.75</td><td>6.16</td><td>7.07</td><td>6.11</td><td>5.56</td><td>6.44</td><td>6.79</td><td>6.67</td><td>6.67</td><td>6.54</td></tr><tr><td>LR2</td><td>5.12</td><td>5.55</td><td>7.59</td><td>7.24</td><td>8.35</td><td>6.98</td><td>6.87</td><td>8.91</td><td>8.76</td><td>8.65</td><td>8.66</td><td>7.23</td></tr><tr><td>Mean</td><td>4.67</td><td>4.88</td><td>6.94</td><td>6.12</td><td>6.81</td><td>5.79</td><td>5.46</td><td>6.90</td><td>6.91</td><td>6.97</td><td>6.98</td><td>5.92</td></tr><tr><td rowspan="8">ELR50ms</td><td>Room A</td><td>11.21</td><td>11.22</td><td>16.77</td><td>11.54</td><td>13.80</td><td>17.33</td><td>14.16</td><td>15.80</td><td>15.95</td><td>14.77</td><td>14.66</td><td>14.73</td></tr><tr><td>Room B</td><td>4.39</td><td>4.41</td><td>12.10</td><td>4.87</td><td>6.41</td><td>11.66</td><td>8.17</td><td>10.47</td><td>10.43</td><td>8.68</td><td>8.54</td><td>8.69</td></tr><tr><td>Room C</td><td>1.03</td><td>0.99</td><td>8.94</td><td>1.21</td><td>2.52</td><td>8.67</td><td>5.35</td><td>7.60</td><td>7.50</td><td>4.04</td><td>3.94</td><td>6.34</td></tr><tr><td>MR1</td><td>6.37</td><td>6.56</td><td>11.90</td><td>6.71</td><td>8.55</td><td>11.55</td><td>8.60</td><td>9.99</td><td>9.86</td><td>9.42</td><td>9.28</td><td>8.32</td></tr><tr><td>MR2</td><td>8.46</td><td>8.81</td><td>14.87</td><td>9.20</td><td>10.72</td><td>13.49</td><td>10.76</td><td>12.21</td><td>12.29</td><td>11.92</td><td>11.79</td><td>11.06</td></tr><tr><td>LR1</td><td>3.70</td><td>3.86</td><td>10.48</td><td>3.98</td><td>5.62</td><td>8.47</td><td>5.73</td><td>6.79</td><td>6.94</td><td>6.35</td><td>6.24</td><td>6.06</td></tr><tr><td>LR2</td><td>7.37</td><td>7.61</td><td>15.70</td><td>7.97</td><td>9.69</td><td>13.81</td><td>10.60</td><td>12.33</td><td>12.63</td><td>11.26</td><td>11.14</td><td>11.65</td></tr><tr><td>Mean</td><td>6.08</td><td>6.21</td><td>12.97</td><td>6.50</td><td>8.19</td><td>12.14</td><td>9.05</td><td>10.74</td><td>10.80</td><td>9.49</td><td>9.37</td><td>9.55</td></tr><tr><td rowspan="8">fwSegSDR50ms</td><td>Room A</td><td>-</td><td>-</td><td>12.31</td><td>27.47</td><td>17.12</td><td>12.79</td><td>10.58</td><td>13.53</td><td>14.12</td><td>15.82</td><td>15.92</td><td>12.76</td></tr><tr><td>Room B</td><td>-</td><td>-</td><td>8.25</td><td>21.77</td><td>16.44</td><td>8.95</td><td>9.72</td><td>9.30</td><td>9.91</td><td>11.32</td><td>11.45</td><td>10.30</td></tr><tr><td>Room C</td><td>-</td><td>-</td><td>6.60</td><td>24.05</td><td>15.81</td><td>8.83</td><td>9.63</td><td>9.74</td><td>10.20</td><td>12.10</td><td>12.25</td><td>9.74</td></tr><tr><td>MR1</td><td>-</td><td>-</td><td>11.04</td><td>25.55</td><td>16.87</td><td>10.06</td><td>11.13</td><td>11.87</td><td>12.48</td><td>13.65</td><td>13.83</td><td>12.07</td></tr><tr><td>MR2</td><td>-</td><td>-</td><td>10.00</td><td>24.14</td><td>17.06</td><td>10.26</td><td>10.85</td><td>11.58</td><td>12.25</td><td>13.18</td><td>13.35</td><td>11.68</td></tr><tr><td>LR1</td><td>-</td><td>-</td><td>9.10</td><td>24.58</td><td>16.58</td><td>9.56</td><td>10.63</td><td>10.94</td><td>11.46</td><td>12.67</td><td>12.85</td><td>11.18</td></tr><tr><td>LR2</td><td>-</td><td>-</td><td>8.31</td><td>25.58</td><td>16.21</td><td>11.01</td><td>10.49</td><td>12.61</td><td>12.86</td><td>13.88</td><td>14.01</td><td>11.98</td></tr><tr><td>Mean</td><td>-</td><td>-</td><td>9.37</td><td>24.73</td><td>16.58</td><td>10.21</td><td>10.43</td><td>11.37</td><td>11.90</td><td>13.23</td><td>13.38</td><td>11.39</td></tr></table>

\* unbiased

Compared to CDR-based dereverberation, the methods by Allen and Westermann yield a low ELR improvement, and at the same time a higher signal-to-distortion ratio. The overall improvement in recognition rate and PESQ is relatively low for both, while Westermann’s method shows good results for the fwSegSNR. The discrepancies between these measures can be explained by the different tradeoffs between reverberation suppression and signal distortion, which have different effects on the evaluated quality measures. Apparently, Allen’s and Westermann’s methods apply a lower overall amount of suppression, which benefits the fwSegSNR measure, but has a small effect on ASR recognition rate and PESQ.

It is noticeable that Lebart’s method yields the highest ELR, but at the same time the worst signal-to-distortion ratio; this indicates that reverberation is overestimated, and consequently too much suppression is applied, possibly due to mismatch between the exponential decay assumption and the early part of the impulse responses [50]. Reducing the suppression gain to the optimum value $\mu ~ = ~ 0 . 6$ to counter overestimation increases the mean recognition rate to 77.4 %.

The estimator $\widehat { C D R } _ { \mathrm { p r o p } 4 }$ , which makes no assumption on the noise coherence, yields on average comparable results to the other estimators, although it can not obtain usable CDR estimates for some of the source positions where the TDOA is close to zero. To gain further insight into the behavior for different TDOAs, we evaluate the performance for the different source positions individually in the following. Fig. 9 shows the recognition rate for signals processed with the proposed unbiased estimators 2, 3 and 4 for the different source positions in rooms A, B and C. While dereverberation using the heuristic DOA-dependent estimator $\widehat { C D R } _ { \mathrm { p r o p } 2 }$ yields the highest recognition rate in almost all cases, the DOAindependent estimator $\widehat { C D R } _ { \mathrm { p r o p 3 } }$ also achieves a significant improvement over all angles. The estimator $\widehat { C D R } _ { \mathrm { p r o p 4 } } .$ , while not usable for DOA $\theta = 0$ due to the disappearing imaginary part of the coherence, remarkably already achieves a significantly increased recognition rate for DOAs as small as $1 0 ^ { \circ }$ , and similar recognition rates as the DOA-independent estimator for higher DOAs. In Room $\mathbf { A } ,$ where the mismatch between the diffuse assumption and the actual reverberation coherence is significant, the estimator slightly exceeds the performance of the (on average best) estimator $\widehat { C D R } _ { \mathrm { p r o p } 2 }$ for some positions, indicating that in some scenarios it may be of advantage to use an estimator which does not assume an isotropic noise field.

Fig. 10 shows the time-averaged $E L R _ { \mathrm { 5 0 m s } }$ for different frequencies before and after processing for an exemplary scenario (room B, $l = 2 \mathrm { m } , d = 8 \mathrm { c m } )$ , where ${ \widehat { C D R } } _ { \mathrm { p r o p } 2 }$ was used for dereverberation. It can be seen that the dereverberation is most effective at frequencies above 1000 Hz, but is already significant at frequencies as low as 300 Hz.

# VII. CONCLUSION

Several well-known and some novel CDR estimation methods and their application to dereverberation have been investigated. Using simulated and measured RIRs for different environments, it has been confirmed that the commonly used model of a reverberant speech signal as a plane wave in diffuse noise is sufficiently accurate to justify the application of CDRbased signal enhancement to dereverberation. However, the known CDR estimators were found to be either biased or not robust enough for practical application to signal enhancement. It has been shown that several variants of unbiased estimators can be derived which improve robustness towards model errors, and that knowledge of either the signal DOA or the noise coherence is sufficient for estimation of the CDR. Employing the improved estimators for dereverberation has been shown to lead to improved dereverberation performance. Using the DOA-independent estimator, the proposed signal enhancement scheme constitutes a completely blind dereverberation system which requires no knowledge or estimation of the signal DOA.

# APPENDIX: DEFINITION OF THE ELR

Reverberant microphone signals $x _ { i } ( t )$ can be written as a convolution of RIRs $h _ { i } ( t )$ with a clean signal $d ( t )$ , i.e., $x _ { i } ( t ) = h _ { i } ( t ) * d ( t )$ . The RIRs can be split at $t = T _ { \mathrm { e } }$ into an early part containing direct path and early reflections, and a late part containing reverberation. To quantify the amount of reverberation in a signal, the early-to-late power ratio $E L R _ { T _ { \mathrm { e } } }$ can then be defined as the power ratio between the components created by convolution with the early RIR, and

(a) CDR estimator $\widehat { C D R } _ { \mathrm { p r o p } 2 }$   
![](figures/a004172d24575feb2f9793a3ee1bff0d9949a2174fecd07763778e6a60b0cf96.jpg)

![](figures/3273bd90712e437f977696df1ac1c36bbd3ec4d2e7376ea6b309bcc8f0ff08df.jpg)

<details>
<summary>line</summary>

| DOA θ | Recognition rate [%] (Red Circle) | Recognition rate [%] (Blue Cross) | Recognition rate [%] (Black Diamond) |
|-------|----------------------------------|----------------------------------|-------------------------------------|
| -45   | 91                               | 90                               | 88                                  |
| 0     | 90                               | 88                               | 78                                  |
| 45    | 91                               | 90                               | 88                                  |
</details>

![](figures/7f0f18e1b6424c0e96599a018130dfd014ba712d7f70021fc01ce7aaef62be34.jpg)

<details>
<summary>line</summary>

| DOA θ | Red Line | Black Line | Blue Line |
|-------|----------|------------|-----------|
| -45   | 90       | 70         | 60        |
| 0     | 85       | 65         | 55        |
| 45    | 85       | 60         | 50        |
</details>

![](figures/4cbb11f04abb00ec3b0413052d91da0cb6cb497cf79c2b50a9b302cdb1c853cd.jpg)

(c) CDR estimator $\widehat { C D R } _ { \mathrm { p r o p 4 } }$ (no noise coherence model)   
![](figures/35331b1544642eb0dac117ed3b3f7b9472e182a07ec8306a0c9d6f9136c460f6.jpg)

<details>
<summary>line</summary>

| DOA θ | Recognition rate [%] (Red Circles) | Recognition rate [%] (Blue Crosses) | Recognition rate [%] (Black Diamonds) |
|-------|------------------------------------|-------------------------------------|--------------------------------------|
| -45   | ~91                                | ~89                                 | ~88                                  |
| 0     | ~72                                | ~70                                 | ~70                                  |
| 45    | ~91                                | ~89                                 | ~88                                  |
</details>

![](figures/88d37934ec97ca7fcf0b8604509dfc6678e307122988e65156bc7ccf919d8c14.jpg)

<details>
<summary>line</summary>

| DOA θ | Red Line | Blue Line | Black Line |
|-------|----------|-----------|------------|
| -45   | 85       | 75        | 60         |
| 0     | 50       | 30        | 25         |
| 45    | 90       | 75        | 60         |
</details>

![](figures/b5e51e05823f91f4526954aa62e00f365873993294b0df28a552555faf450d82.jpg)

<details>
<summary>line</summary>

| DOA θ | Red Line | Blue Line | Black Line | Purple Line |
|-------|----------|-----------|------------|-------------|
| -45   | 80       | 60        | 40         | 20          |
| 0     | 60       | 20        | 10         | 80          |
| 45    | 80       | 60        | 40         | 20          |
</details>

![](figures/5bcfe18ae7269482b963d6fdb3a6adb1395400972ba90d2f9e44dc6f293d3813.jpg)

<details>
<summary>text_image</summary>

1m, processed
2m, processed
4m, processed
1m, unprocessed
2m, unprocessed
4m, unprocessed
</details>

Figure 9. Average recognition rate for different rooms and source positions $( l { \ ' { = } 1 , 2 , 4 \mathrm { m } , \theta } = \bar { - } 9 0 \dots 9 0 ^ { \circ } )$ , for unprocessed signals and signals processed by spatial magnitude averaging combined with coherence-based postfilters based on different CDR estimators.

![](figures/7bc4c3030b1c5c85df707589476e3a7d42b516fe80458d42b2ca62c2de335248.jpg)

<details>
<summary>line</summary>

| f [Hz] | processed | unprocessed |
| ------ | --------- | ----------- |
| 0      | ~5        | ~3          |
| 1000   | ~15       | ~8          |
| 2000   | ~18       | ~10         |
| 3000   | ~16       | ~12         |
| 4000   | ~20       | ~15         |
| 5000   | ~22       | ~18         |
| 6000   | ~15       | ~12         |
| 7000   | ~12       | ~10         |
| 8000   | ~5        | ~2          |
</details>

Figure 10. Time-averaged $E L R _ { 5 0 \mathrm { m s } }$ as function of frequency (room $\mathbf { B } , l =$ 2 m, $d = 8 \mathrm { c m } ) .$ , for unprocessed reverberant signal, and signal dereverberated using the proposed unbiased estimator 2.

the reverberation components created by convolution with the late RIR, where $T _ { \mathrm { e } }$ is set to an appropriate threshold, $\mathrm { e . g . }$ ., $T _ { \mathrm { e } } = 5 0 \mathrm { m s } \ [ 2 0 ]$ . When $T _ { \mathrm { e } }$ is set to include only the direct path in the early component, the ELR is equivalent to the DRR. For the evaluation in this paper, the $E L R _ { T _ { \mathrm { e } } }$ is computed for the unprocessed microphone signals, and for the signals at the output of the signal enhancement system by processing the early and late signal components separately.

# REFERENCES

[1] L. Danilenko, “Binaurales Horen im nichtstation ¨ aren diffusen ¨ Schallfeld,” Kybernetik, vol. 6, no. 2, pp. 50–57, Jun. 1969.   
[2] J. B. Allen, D. A. Berkley, and J. Blauert, “Multimicrophone signalprocessing technique to remove room reverberation from speech signals,” J. Acoust. Soc. Am., vol. 62, no. 4, pp. 912–915, 1977.   
[3] P. Bloom and G. Cain, “Evaluation of two-input speech dereverberation techniques,” in Proc. ICASSP, 1982.   
[4] R. Zelinski, “A microphone array with adaptive post-filtering for noise reduction in reverberant rooms,” in Proc. ICASSP, 1988.   
[5] R. Le Bouquin and G. Faucon, “Using the coherence function for noise reduction,” Communications, Speech and Vision, IEE Proceedings I, vol. 139, no. 3, pp. 276–280, 1992.   
[6] R. Le Bouquin-Jeannes, A. Azirani, and G. Faucon, “Enhancement of speech degraded by coherent and incoherent noise using a cross-spectral estimator,” IEEE Trans. Speech and Audio Process., vol. 5, no. 5, pp. 484–487, Sep. 1997.   
[7] A. Westermann, J. M. Buchholz, and T. Dau, “Binaural dereverberation based on interaural coherence histograms,” J. Acoust. Soc. Am., vol. 133, no. 5, pp. 2767–2777, 2013.   
[8] K. U. Simmer, J. Bitzer, and C. Marro, “Post-filtering techniques,” in Microphone Arrays, ser. Digital Signal Process., P. M. Brandstein and D. D. Ward, Eds. Springer Berlin Heidelberg, Jan. 2001, pp. 39–60.   
[9] I. McCowan and H. Bourlard, “Microphone array post-filter based on noise field coherence,” IEEE Trans. Speech and Audio Process., vol. 11, no. 6, pp. 709–716, 2003.   
[10] M. Jeub, C. M. Nelke, C. Beaugeant, and P. Vary, “Blind estimation of the coherent-to-diffuse energy ratio from noisy speech signals,” in Proc. EUSIPCO, 2011.   
[11] O. Thiergart, G. Del Galdo, and E. A. P. Habets, “Signal-to-reverberant ratio estimation based on the complex spatial coherence between omnidirectional microphones,” in Proc. ICASSP, 2012.   
[12] ——, “Diffuseness estimation with high temporal resolution via spatial coherence between virtual first-order microphones,” in Proc. WASPAA, 2011.   
[13] ——, “On the spatial coherence in mixed sound fields and its application to signal-to-diffuse ratio estimation,” J. Acoust. Soc. Am., vol. 132, no. 4, p. 2337, 2012.   
[14] D. P. Jarrett, O. Thiergart, E. A. P. Habets, and P. A. Naylor, “Coherencebased diffuseness estimation in the spherical harmonic domain,” in Proc. IEEEI, 2012.   
[15] A. Schwarz and W. Kellermann, “Unbiased coherent-to-diffuse ratio estimation for dereverberation,” in Proc. IWAENC, 2014.   
[16] V. Pulkki, “Spatial sound reproduction with directional audio coding,” J. Audio Eng. Soc., vol. 55, no. 6, pp. 503–516, Jun. 2007.   
[17] A. Schwarz, C. Huemmer, R. Maas, and W. Kellermann, “Spatial diffuseness features for DNN-based speech recognition in noisy and reverberant environments,” in Proc. ICASSP, 2015.   
[18] G. Del Galdo, M. Taseska, O. Thiergart, J. Ahonen, and V. Pulkki, “The diffuse sound field in energetic analysis,” J. Acoust. Soc. Am., vol. 131, no. 3, pp. 2141–2151, 2012.   
[19] B. F. Cron and C. H. Sherman, “Spatial-correlation functions for various noise models,” J. Acoust. Soc. Am., vol. 34, no. 11, pp. 1732–1736, 1962.   
[20] H. Kuttruff, Room Acoustics. London: Taylor & Francis, 2000.   
[21] R. Steele and L. Hanzo, Mobile Radio Communications, 2nd Edition. Wiley-IEEE Press, May 1999.   
[22] D. B. Kilfoyle and A. B. Baggeroer, “The state of the art in underwater acoustic telemetry,” IEEE J. Oceanic Eng., vol. 25, no. 1, pp. 4–27, 2000.   
[23] R. K. Cook, R. V. Waterhouse, R. D. Berendt, S. Edelman, and M. C. T. Jr, “Measurement of correlation coefficients in reverberant sound fields,” J. Acoust. Soc. Am., vol. 27, no. 6, pp. 1072–1077, 1955.   
[24] F. Jacobsen and T. Roisin, “The coherence of reverberant sound fields,” J. Acoust. Soc. Am., vol. 108, no. 1, pp. 204–210, 2000.   
[25] J. B. Allen and D. A. Berkley, “Image method for efficiently simulating small-room acoustics,” J. Acoust. Soc. Am., vol. 65, no. 4, pp. 943–950, 1979.   
[26] G. W. Elko, E. Diethorn, and T. Gansler, “Room impulse response ¨ variation due to thermal fluctuation and its impact on acoustic echo cancellation,” in Proc. IWAENC, 2003.

[27] G. W. Elko, “Superdirectional microphone arrays,” in Acoustic Signal Process. for Telecommunication, S. L. Gay and J. Benesty, Eds. Kluwer Academic Publishers, 2000, pp. 181–237.   
[28] —, “Spatial coherence functions for differential microphones in isotropic noise fields,” in Microphone Arrays. Springer, 2001, pp. 61– 85.   
[29] E. Haensler and G. Schmidt, Acoustic Echo and Noise Control: A Practical Approach. Wiley-Interscience, 2004.   
[30] M. Jeub, M. Schafer, T. Esch, and P. Vary, “Model-based dereverberation preserving binaural cues,” IEEE Trans. Audio, Speech, and Language Process., vol. 18, no. 7, pp. 1732–1745, 2010.   
[31] H. Ye and R. DeGroat, “Maximum likelihood DOA estimation and asymptotic cramer-rao bounds for additive unknown colored noise,” IEEE Trans. Signal Process., vol. 43, no. 4, pp. 938–949, Apr. 1995.   
[32] A. Kuklasinski, S. Doclo, S. H. Jensen, and J. Jensen, “Maximum likelihood based multi-channel isotropic reverberation reduction for hearing aids,” in Proc. EUSIPCO, 2014.   
[33] A. Schwarz, A. Brendel, and W. Kellermann, “Coherence-based dereverberation for automatic speech recognition,” in Proc. DAGA, 2014.   
[34] N. Ito, N. Ono, E. Vincent, and S. Sagayama, “Designing the Wiener post-filter for diffuse noise suppression using imaginary parts of interchannel cross-spectra,” in Proc. ICASSP, 2010.   
[35] E. A. P. Habets, “Single- and multi-microphone speech dereverberation using spectral enhancement,” Ph.D. dissertation, Technische Universiteit Eindhoven, 2007.   
[36] K. Kinoshita, M. Delcroix, T. Yoshioka, T. Nakatani, A. Sehr, W. Kellermann, and R. Maas, “The REVERB challenge: A common evaluation framework for dereverberation and recognition of reverberant speech,” in Proc. WASPAA, 2013.   
[37] M. Harteneck, S. Weiss, and R. Stewart, “Design of near perfect reconstruction oversampled filter banks for subband adaptive filters,” IEEE Trans. Circuits and Systems II: Analog and Digital Signal Process., vol. 46, no. 8, pp. 1081–1085, Aug. 1999.   
[38] P. M. Peterson, “Simulating the response of multiple microphones to a single acoustic source in a reverberant room,” The Journal of the Acoustical Society of America, vol. 80, no. 5, pp. 1527–1529, Nov. 1986.   
[39] J. S. Bradley, H. Sato, and M. Picard, “On the importance of early reflections for speech in rooms,” J. Acoust. Soc. Am., vol. 113, no. 6, pp. 3233–3244, 2003.   
[40] A. Sehr, E. A. P. Habets, R. Maas, and W. Kellermann, “Towards a better understanding of the effect of reverberation on speech recognition performance,” in Proc. IWAENC, 2010.   
[41] Y. Hu and P. C. Loizou, “Evaluation of objective quality measures for speech enhancement,” IEEE Trans. Audio, Speech and Langage Process., vol. 16, no. 1, pp. 229–238, Jan. 2008.   
[42] D. Huggins-Daines, M. Kumar, A. Chan, A. W. Black, M. Ravishankar, and A. I. Rudnicky, “PocketSphinx: A free, real-time continuous speech recognition system for hand-held devices,” in Proc. ICASSP, 2006.   
[43] M. Cooke, J. Barker, S. Cunningham, and X. Shao, “An audio-visual corpus for speech perception and automatic speech recognition,” J. Acoust. Soc. Am., vol. 120, no. 5, pp. 2421–2424, 2006.   
[44] S. Furui, “Cepstral analysis technique for automatic speaker verification,” IEEE Trans. Acoustics, Speech and Signal Process., vol. 29, no. 2, pp. 254–272, 1981.   
[45] H. Christensen, J. Barker, and P. Green, “The CHiME corpus: a resource and a challenge for computational hearing in multisource environments,” in Proc. Interspeech, 2010.   
[46] S. Goetze, A. Warzybok, I. Kodrasi, J. O. Jungmann, B. Cauchi, J. Rennies, E. A. P. Habets, A. Mertins, T. Gerkmann, S. Doclo, and B. Kollmeier, “A study on speech quality and speech intelligibility measures for quality assessment of single-channel dereverberation algorithms,” in Proc. IWAENC, 2014.   
[47] A. W. Rix, J. G. Beerends, M. P. Hollier, and A. P. Hekstra, “Perceptual evaluation of speech quality (PESQ) - a new method for speech quality assessment of telephone networks and codecs,” in Proc. ICASSP, 2001.   
[48] K. Lebart, J.-M. Boucher, and P. N. Denbigh, “A new method based on spectral subtraction for speech dereverberation,” Acta Acustica united with Acustica, vol. 87, no. 3, pp. 359–366, 2001.   
[49] C. Schuldt and P. Handel, “Decay rate estimators and their performance for blind reverberation time estimation,” IEEE/ACM Trans. Audio, Speech, and Language Process., vol. 22, no. 8, pp. 1274–1284, Aug. 2014.   
[50] E. Habets, S. Gannot, and I. Cohen, “Late reverberant spectral variance estimation based on a statistical model,” IEEE Signal Process. Letters, vol. 16, no. 9, pp. 770–773, Sep. 2009.