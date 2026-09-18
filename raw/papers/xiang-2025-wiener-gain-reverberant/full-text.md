# Design of the Wiener Gain in Noisy and Reverberant Environments

Qian Xiang<sup>a</sup>, Jingdong Chen<sup>b,∗</sup>, Jacob Benesty<sup>c</sup>, Tao Lei<sup>d</sup>, Chao Pan<sup>b</sup>

<sup>a</sup>School of Electrical and Control Engineering, Shaanxi University of Science and Technology, Xi’an, Shaanxi 710021, China <sup>b</sup>Center of Intelligent Acoustics and Immersive Communications, Northwestern Polytechnical University, Xi’an, Shaanxi 710072, China

<sup>c</sup>INRS-EMT, University of Quebec, Montreal, QC H5A 1K6, Canada <sup>d</sup>School of Electronic Information and Artificial Intelligence, Shaanxi University of Science and Technology, Xi’an, Shaanxi 710021, China

## Abstract

The Wiener gain or filter plays an important role in both single-channel and multichannel speech enhancement. Tradi tional Wiener gain formulations are typically based solely on either the signal-to-noise ratio (SNR) or the coherent-to difuse ratio (CDR), rendering them suboptimal in noisy and reverberant environments. In this paper, we present an approach to the design of the Wiener gain by incorporating estimates of both SNR and CDR. Additionally, we introduce two hyperparameters to govern the extent of noise reduction and reverberation suppression. Through simulations, we demonstrate that the proposed approach surpasses widely used methods in terms of SNR gain, log-spectral-distortion (LSD), direct-to-reverberant energy ratio (DRR), and Kurtosis ratio (KR).

Keywords: Dereverberation, noise suppression, signal-to-noise ratio, coherence-to-difuse ratio, Wiener gain.

## 1. Introduction

The Wiener beamformer represents a fundamental spatio-temporal filtering technique extensively employed in the field of acoustic signal processing to extract an acoustic source signal from observations tainted by both noise and reverberation. It has been shown in the literature that this beamformer can be decomposed as the combination of a minimum-variance-distortionless-response (MVDR) beamformer and a Wiener gain [1, 2]. Hence, both the MVDR beamformer and Wiener gain necessitate careful design to ensure optimal performance of the Wiener beamformer.

Numerous studies in the literature have been dedicated to the design of MVDR beamformers. These eforts aim to achieve high signal-to-noise-ratio (SNR) gain while ensuring robustness for practical applications [3–5]. Various techniques have been proposed for this purpose, including the diagonal-loading MVDR beamformer [6, 7], worst-case MVDR beamformer [8–10], and simplified MVDR beamformer, where the noise field is modeled as either spatially white [11, 12] or difuse noise [13–15]. Similarly, various endeavors have been undertaken to devise optimal Wiener gains. These approaches can be broadly categorized into two main groups: SNR based methods and coherent-todifuse-ratio (CDR) based techniques.

SNR-based methods primarily target at the suppression of background additive noise [16, 17]. The key lies in obtaining an accurate estimate of the SNR, as more accurate SNR estimation leads to enhanced speech with reduced distortion. Classical algorithms for SNR estimation can be found in the literature [18–21]. In contrast, CDRbased approaches center on reverberation suppression [22– 24]. The crux lies in obtaining an accurate estimate of the CDR. To estimate CDR, it is generally assumed that the noise coherence matrix induced by reverberation mirrors that of difuse noise. Specifically, coherence coeficients corresponding to the distance between sensors and the fre quency of interest are calculated. By leveraging the covariance matrix model of array observations and a priori information on the noise coherence matrix, CDR estimators can be derived [25–27]. Initially, CDR estimators were developed for two-element arrays [28–31], and later extended to arrays with more than two sensors [34]. However, existing CDR estimators do not account for both noise and reverberation simultaneously, rendering them less efective in practical environments, where background noise and re verberation coexist.

In this study, we aim to design the Wiener gain by jointly considering both noise and reverberation. We devise an estimator that incorporates both SNR and CDR as parameters. Additionally, we introduce two hyperparameters to regulate the trade-of between noise reduction and reverberation suppression. Using SNR gain, log spectral-distortion (LSD), direct-to-reverberant energy ratio (DRR) [45, 46], and Kurtosis ratio (KR) [48, 49] as performance metrics, we demonstrate, through simula tions, the superior performance of our proposed method for Wiener gain design.

The organization of the rest of the paper is as follows. In Section 2, we introduce the signal model, discuss the parameters, and describe the objective of this study. Section 3 focuses on deriving the optimal Wiener gain for both reverberation and additive noise suppression. Simulation results are presented and analyzed in Section 4. Finally, we draw conclusions in Section 5.

## 2. Signal model and problem formulation

Consider to use an array with M microphones to pick up sound signals in a noisy and reverberant environment. The observation signals at the sensors can be modeled as [16]

$$
\begin{array}{c} y _ {m} (t) = g _ {m} (t) * s (t) + v _ {m} (t) \\ = g _ {m, \text {early}} (t) * s (t) + g _ {m, \text {late}} (t) * s (t) + v _ {m} (t), \end{array}\tag{1}
$$

where t is the discrete-time index, ∗ stands for the linear convolution, $s ( t )$ is the speech source signal of interest, $v _ { m } ( t )$ is the additive noise at the mth sensor, $g _ { m } ( t )$ is the impulse response from the source to the mth sensor, $g _ { m , \mathrm { e a r l y } } ( t )$ represents the direct and early reflection paths in the impulse response, and $g _ { m , \mathrm { l a t e } } ( t )$ signifies the late reflection paths, which leads to reverberation, with $g ( t ) = g _ { m , \mathrm { e a r l y } } ( t ) + g _ { m , \mathrm { l a t e } } ( t )$ . It is commonly assumed that the source signal, reverberation, and noise are mutually uncorrelated and they all are of zero mean.

In the short-time-Fourier-transform (STFT) domain, the signal model presented in (1) can be rewritten as

$$
Y _ {m} (n, k) = X _ {m} (n, k) + R _ {m} (n, k) + V _ {m} (n, k),\tag{2}
$$

where k is the frequency-bin index, n is the time-frame index, and $Y _ { m } ( n , k ) , X _ { m } ( n , k ) , R _ { m } ( n , k ) , { \mathrm { a n d } } V _ { m } ( n , k )$ are the STFTs of $y _ { m } ( t ) , g _ { m , \mathrm { e a r l y } } ( t ) * s ( t ) , g _ { m , \mathrm { l a t e } } ( t ) * s ( t )$ , and $v _ { m } ( t )$ , respectively. Putting all the signals in (2) into a vector form gives

$$
\begin{array}{l} \mathbf {y} (n, k) \triangleq \left[ \begin{array}{c c c c} Y _ {0} (n, k) & Y _ {1} (n, k) & \dots & Y _ {M - 1} (n, k) \end{array} \right] ^ {T} \\ = \mathbf {d} (k) S (n, k) + \mathbf {r} (n, k) + \mathbf {v} (n, k), \end{array}\tag{3}
$$

where $\mathbf { d } ( k )$ is called the array manifold vector, $S ( \boldsymbol n , \boldsymbol k )$ is the source signal, and $\mathbf { r } ( n , k )$ and $\mathbf { v } ( n , k )$ , which are defined in the same way as $\mathbf { y } ( n , k )$ , are the reverberation and noise vectors, respectively.

Applying a beamformer $\mathbf { h } ( k )$ of length M to the ob servation vector, $\mathbf { y } ( n , k )$ , we obtain

$$
\begin{array}{l} Z (n, k) = \mathbf {h} ^ {H} (k) \mathbf {y} (n, k) \\ \qquad = \mathbf {h} ^ {H} (k) \mathbf {d} (k) S (n, k) + \mathbf {h} ^ {H} (k) \mathbf {r} (n, k) \\ \qquad + \mathbf {h} ^ {H} (k) \mathbf {v} (n, k), \end{array}\tag{4}
$$

where $\mathbf { h } ^ { H } ( k ) \mathbf { d } ( k ) S ( n , k )$ is the recovered signal after beamforming, and $\mathbf { h } ( k ) \mathbf { r } ( n , k )$ and $\mathbf { h } ( k ) \mathbf { v } ( n , k )$ correspond, respectively, to the residual reverberation and residual noise after beamforming.

Based on the assumption that the source, reverberation, and noise are mutually uncorrelated, we can derive the variance of $Z ( n , k )$ as

$$
\begin{array}{l} \phi_ {Z} (n, k) \triangleq \mathbb {E} \left[ | Z (n, k) | ^ {2} \right] \\ = \left| \mathbf {h} ^ {H} (k) \mathbf {d} (k) \right| ^ {2} \phi_ {S} (n, k) \\ + \mathbf {h} ^ {H} (k) \boldsymbol {\Phi} _ {R} (n, k) \mathbf {h} (k) + \mathbf {h} ^ {H} (k) \boldsymbol {\Phi} _ {V} (n, k) \mathbf {h} (k), \end{array} \tag {5}
$$

where $\mathbb { E } ( \cdot )$ denotes the mathematical expectation, $\phi _ { S } ( n , k )$ is the variance of the source signal, and $\Phi _ { R } ( { \boldsymbol { n } } , { \boldsymbol { k } } )$ and $\Phi _ { V } ( \boldsymbol { n } , \boldsymbol { k } )$ are the covariance matrices of the reverberation and additive noise, respectively. For small-spacing microphone arrays, as assumed in this study, $\Phi _ { R } ( { \boldsymbol { n } } , { \boldsymbol { k } } )$ and $\Phi _ { V } ( \boldsymbol { n } , \boldsymbol { k } )$ can be modeled as [35]

$$
\boldsymbol {\Phi} _ {R} (n, k) = \boldsymbol {\Gamma} _ {R} (k) \phi_ {R} (n, k),\tag{6}
$$

$$
\boldsymbol {\Phi} _ {V} (n, k) = \boldsymbol {\Gamma} _ {V} (k) \phi_ {V} (n, k),\tag{7}
$$

where $\Gamma _ { R } ( k )$ and $\Gamma _ { V } ( k )$ are the coherence matrices of the reverberation and additive noise, respectively, with tr $[ \Gamma _ { R } ( k ) ] = \mathrm { t r } \left[ \Gamma _ { V } ( k ) \right] = M$ , and $\phi _ { R } ( n , k )$ and $\phi _ { V } ( n , k )$ are the variances of the reverberation and additive noise, respectively. With (6) and (7), the variance of $Z ( n , k )$ can be further simplified to

$$
\begin{array}{c} \phi_ {Z} (n, k) = \alpha_ {S} (k) \phi_ {S} (n, k) + \alpha_ {R} (k) \phi_ {R} (n, k) \\ + \alpha_ {V} (k) \phi_ {V} (n, k), \end{array}\tag{8}
$$

where

$$
\alpha_ {S} (k) \triangleq \left| \mathbf {h} ^ {H} (k) \mathbf {d} (k) \right| ^ {2},\tag{9}
$$

$$
\alpha_ {R} (k) \triangleq \mathbf {h} ^ {H} (k) \pmb {\Gamma} _ {R} (k) \mathbf {h} (k),
$$

$$
\alpha_ {V} (k) \triangleq \mathbf {h} ^ {H} (k) \boldsymbol {\Gamma} _ {V} (k) \mathbf {h} (k).\tag{10}
$$

(11)

To enhance the source signal from noisy observations, it is often desired that both $\alpha _ { R } ( k )$ and $\alpha _ { V } ( k )$ are small and, at the same time, $\alpha _ { S } ( k )$ is above some level. However, the performance of a fixed beamformer, $\mathbf { h } ( k )$ , may not meet the requirement and, consequently, a post-filter $G ( n , k ) \in [ 0 , 1 ]$ is often applied to $Z ( n , k ) ~ [ 1 , ~ 2 ]$ . Under this framework, the final estimate of the source signal can be expressed as

$$
\begin{array}{r l} & {\hat {S} (n, k) = G (n, k) Z (n, k)} \\ & {\qquad = G (n, k) \mathbf {h} ^ {H} (k) \mathbf {y} (n, k)} \\ & {\qquad = S _ {\mathrm{fd}} (n, k) + R _ {\mathrm{rr}} (n, k) + V _ {\mathrm{rn}} (n, k),} \end{array}\tag{12}
$$

where $S _ { \mathrm { f d } } ( n , k ) \ \stackrel { \triangle } { = } \ { \cal G } ( n , k ) { \bf h } ^ { H } ( k ) { \bf d } ( k ) S ( n , k )$ is the filtered desired signal, $R _ { \mathrm { r r } } ( n , k ) \ \stackrel { \triangle } { = } \ { \cal G } ( n , k ) { \bf h } ^ { H } ( k ) { \bf r } ( n , k )$ is the residual reverberant signal, and $\begin{array} { r l r l } { V _ { \mathrm { r n } } } & { { } } & { \triangleq } & { } \end{array}$ $G ( n , k ) \mathbf { h } ^ { H } ( k ) \mathbf { v } ( n , k )$ is the residual noise.

Clearly, the optimal gain, i.e., the optimal value of $G ( n , k )$ , is a function of the variances of the desired source, reverberation, and additive noise. In the extreme case where reverberation is absent, the gain degenerates to the following form [18–20]:

$$
G (n, k) = \frac {\mathrm{SNR} (n , k)}{1 + \mathrm{SNR} (n , k)},\tag{13}
$$

where $\mathrm { S N R } \triangleq \phi _ { S } ( n , k ) / \phi _ { V } ( n , k )$ is the SNR. In an another extreme case where the additive noise is absent, the gain degenerates to a function of CDR [22–29], i.e.,

$$
G (n, k) = \frac {\mathrm{CDR} (n , k)}{1 + \mathrm{CDR} (n , k)},\tag{14}
$$

where CDR $\stackrel { \triangle } { = } \phi _ { S } ( n , k ) / \phi _ { R } ( n , k )$ , which is the ratio between the variance of the coherent source signal and that of the late reverberation. To have an estimate of the CDR, one way is to first estimate $\phi _ { \mathrm { S } }$ and $\phi _ { \mathrm { R } }$ using such methods as in [32, 33] and the variance of the source using methods such as the one in [44]. However, these approaches require to know the a priori source coherence matrix, which is dificult to estimate in complex acoustic environments.

While considerable attention has been dedicated in literature to estimating the gain in the form of either (13) or (14), i.e., either considering the case with only noise or the case with only reverberation, few eforts have focused on estimating the gain $G ( n , k )$ while considering both reverberation and additive noise. This is precisely the objective of this work.

## 3. Proposed approach

Consider both the reverberation and additive noise, the optimal Wiener gain can be expressed according to (8) as

$$
\begin{array}{l} G (n, k) \\ = \frac {\alpha_ {S} (k) \phi_ {S} (n , k)}{\alpha_ {S} (k) \phi_ {S} (n , k) + \alpha_ {R} (k) \phi_ {R} (n , k) + \alpha_ {V} (k) \phi_ {V} (n , k)}. \end{array}\tag{15}
$$

Note that the distortionless constraint, $\mathrm { i . e . , } \ \mathbf { h } ^ { H } ( k ) \mathbf { d } ( k ) =$ 1, is often required in array processing to prevent the desired source signal from distortion. It is reasonable to assume that $\alpha _ { S } ( k ) \approx 1 . \mathrm { \ A s }$ a result, one can simplify the Wiener gain as

$$
\begin{array}{c} G (n, k) = \frac {\phi_ {S} (n , k)}{\phi_ {S} (n , k) + \alpha_ {R} (k) \phi_ {R} (n , k) + \alpha_ {V} (k) \phi_ {V} (n , k)} \\ = \frac {1}{1 + \alpha_ {R} (k) \frac {1}{\mathrm{CDR} (n , k)} + \alpha_ {V} (k) \frac {1}{\mathrm{SNR} (n , k)}}. \end{array}\tag{16}
$$

In practical applications, eliminating noise and reverberation simultaneously without distorting the source signal is often challenging, if not impossible. Thus, a strategic approach becomes necessary to strike a reasonable balance between speech distortion, noise reduction, and reverberation suppression. Recognizing that the importance of noise reduction or reverberation suppression may vary depending on the application, we generalize the Wiener gain as follows:

![](figures/61cdb0bee2d924258ebddab3377cd82de8dd35b6a0c95d9d33e8283a04b112b8.jpg)  
Figure 1: Illustration of the elements of $\mathbf { { T } } _ { R }$ as a function of distance and frequency.

$$
G (n, k) = \frac {1}{1 + \beta_ {1} \frac {\alpha_ {R} (k)}{\mathrm{CDR} (n , k)} + \beta_ {2} \frac {\alpha_ {V} (k)}{\mathrm{SNR} (n , k)}},\tag{17}
$$

where $\beta _ { 1 } \geq 0$ and $\beta _ { 2 } \geq 0$ are two hyper-parameters, which control the tradeof between noise reduction and reverberation suppression.

It is widely acknowledged that the filtering process introduces speech distortion, notably the phenomenon known as musical noise [21]. Indeed, research has shown that increased noise reduction tends to correlate with greater speech distortion [36]. To address this, the applied gain to the signal is frequently adjusted to mitigate the impact of speech distortion by

$$
G (n, k) \leftarrow \max \{G (n, k), G _ {\min} \},\tag{18}
$$

where $G _ { \mathrm { m i n } } ~ \in ~ ( 0 , 1 )$ is a small positive number, $\mathrm { e . g . }$ $G _ { \mathrm { m i n } } = 0 . 0 1$ . As musical noise stems from isolated peaks in the STFT domain, raising $G _ { \mathrm { m i n } }$ aids in diminishing these peaks, albeit at the expense of reduced noise reduction.

## 3.1. Implementation

## 3.1.1. Covariance and coherence matrices estimation

The covariance matrix of the observation is estimated according to

$$
\boldsymbol {\Phi} _ {Y} (n, k) = \lambda \boldsymbol {\Phi} _ {Y} (n - 1, k) + (1 - \lambda) \mathbf {y} (n, k) \mathbf {y} ^ {H} (n, k),\tag{19}
$$

where $\lambda \in ( 0 , 1 )$ is a forgetting factor. The corresponding coherence matrix is then calculated by

$$
\boldsymbol {\Gamma} _ {Y} (n, k) = \boldsymbol {\Phi} _ {Y} (n, k) / \phi_ {Y} (n, k),\tag{20}
$$

where $\phi _ { Y } ( n , k ) \overset { \triangle } { = } \mathrm { t r } \left[ \Phi _ { Y } ( n , k ) \right] / M$ is the variance of the observation signals. The covariance matrix of the additive noise is estimated in a similar way when the desired signal is absent. The coherence matrix $\mathbf { \boldsymbol { \Gamma } } _ { V } ( \boldsymbol { k } )$ is then calculated according to (7), i.e., ${ \Gamma _ { V } ( n , k ) = \Phi _ { V } ( n , k ) / \phi _ { V } ( n , k ) }$ . The coherence matrix of the reverberation is modeled by that of the difuse noise, i.e.,

$$
\left[ \boldsymbol {\Gamma} _ {R} (k) \right] _ {i, j} = \frac {\sin (\omega \Delta_ {i , j} / c)}{\omega \Delta_ {i , j} / c},\tag{21}
$$

where $[ \cdot ] _ { i , j }$ stands for the $( i , j )$ th element of a matrix, c represents the speed of sound in air, typically around 340 $\mathrm { m } / \mathrm { s }$ and $\Delta _ { i , j }$ is the distance between the ith and jth sensors. Apparently, the (i, j)th element of $\Gamma _ { R } ( k )$ is a function of $\Delta _ { i , j }$ and ω $, \ ( \omega = 2 \pi k )$ ), as illustrated in Fig. 1.

## 3.1.2. Estimation of the beamformer, $\alpha _ { R } ( k )$ , and $\alpha _ { V } ( k )$

Numerous attempts have been made to design both fixed and adaptive beamformers. For simplification, we adopt the robust superdirective beamformer in this work, which is of the following form:

$$
\mathbf {h} (k) = \frac {\mathbf {\Gamma} _ {R , \epsilon} ^ {- 1} (k) \mathbf {d} _ {0} (k)}{\mathbf {d} _ {0} ^ {H} \mathbf {\Gamma} _ {R , \epsilon} ^ {- 1} (k) \mathbf {d} _ {0} (k)},\tag{22}
$$

where $\boldsymbol { \Gamma } _ { R , \epsilon } ( k ) = \boldsymbol { \Gamma } _ { R } ( k ) + \epsilon \mathbf { I }$ , with $\epsilon = 1 0 ^ { - 3 }$ , and $\mathbf { d } _ { 0 } ( k )$ is the array phase-delay vector corresponding to the desired source direction. For a uniform linear array, the phasedelay vector can be expressed as

$$
\mathbf {d} _ {0} (k) = \left[ \begin{array}{l l l l} 1 & e ^ {- \jmath \varpi_ {k} \delta_ {0} \cos \theta_ {0}} & \dots & e ^ {- \jmath (M - 1) \varpi_ {k} \delta_ {0} \cos \theta_ {0}} \end{array} \right.\tag{23}
$$

where $\delta _ { 0 }$ is the array inter-element spacing and $\theta _ { 0 }$ is the desired source direction. Parameters $\alpha _ { R } ( k )$ and $\alpha _ { V } ( k )$ are then calculated according to (10) and (11), respectively.

## 3.1.3. SNR estimation

The SNR is estimated by the so-called decision-direct approach [18], i.e.,

$$
\mathrm{SNR} (n, k) = \lambda_ {S} \xi (n, k - 1) + (1 - \lambda_ {S}) \zeta (n, k),\tag{24}
$$

where $\lambda _ { S } \in ( 0 , 1 )$ is a hyper-parameter and

$$
\xi (n, k) = \frac {| G ^ {\prime} (n , k) Z (n , k) | ^ {2}}{\phi_ {V} (n , k)},\tag{25}
$$

$$
\zeta (n, k) = \max \left[ \frac {| Z (n , k) | ^ {2}}{\phi_ {V} (n , k)} - 1, 0 \right],\tag{26}
$$

with $G ^ { \prime } ( n , k ) \in [ 0 , 1 ]$ being a gain function. The variance of the noise is calculated by minimum tracking [18], the gain function $G ^ { \prime } ( n , k )$ is calculated according to [37]. In the case that $G ^ { \prime } ( n , k ) = \sqrt { | Z ( n , k ) | ^ { 2 } / \phi _ { V } ( n , k ) - 1 }$ , one can verify that $\xi ( n , k ) = \zeta ( n , \dot { k } )$ . Recall that $\zeta ( n , k )$ can be viewed as an instantaneous estimate of SNR, the decisiondirect approach improves the results by smoothing the instantaneous values.

![](figures/b39b405f81481d285309fb6fb4349143226b10f764eaa311ef8ec340b4446c49.jpg)  
Figure 2: Signal processing diagram of the proposed approach.

## 3.1.4. CDR estimation

According to (2), we can express the covariance matrix of the observation as

$$
\begin{array}{l} \boldsymbol {\Phi} _ {Y} (n, k) \\ = \phi_ {S} (n, k) \mathbf {d d} ^ {H} + \phi_ {R} (n, k) \boldsymbol {\Gamma} _ {R} (k) + \phi_ {V} (n, k) \boldsymbol {\Gamma} _ {V} (k) \\ = \phi_ {S} (n, k) \boldsymbol {\Gamma} _ {S} (k) + \phi_ {R} (n, k) \boldsymbol {\Gamma} _ {R} (k) + \phi_ {V} (n, k) \boldsymbol {\Gamma} _ {V} (k), \end{array}\tag{27}
$$

where φ is the variance of the coherent source signal and $\mathbf { r } _ { S } ( k ) = \mathbf { d } \mathbf { d } ^ { H }$ is the coherence matrix of the source.

Since the coherent source signal, late reverberation, and noise signal are mutually uncorrelated, the variance of the observation follows that $\phi _ { Y } = \phi _ { S } + \phi _ { R } + \phi _ { V }$ . The coherence matrix $\boldsymbol { \Gamma } _ { \boldsymbol { Y } } ( \boldsymbol { k } )$ is then calculated according to (20), i.e.,

$$
\boldsymbol {\Gamma} _ {Y} (k) = \frac {\boldsymbol {\Phi} _ {Y} (n , k)}{\phi_ {S} (n , k) + \phi_ {R} (n , k) + \phi_ {V} (n , k)}.\tag{28}
$$

Substituting (27) into (28) gives

$$
\boldsymbol {\Gamma} _ {S} (k) = \frac {\boldsymbol {\Gamma} _ {Y} (k) - \boldsymbol {\Gamma} _ {R} (k))}{\operatorname{CDR} (k)} + \boldsymbol {\Gamma} _ {Y} (k) + \frac {\boldsymbol {\Gamma} _ {Y} (k) - \boldsymbol {\Gamma} _ {V} (k)}{\operatorname{SNR} (k)}.\tag{29}
$$

Using the constraint that all the diagonal elements of $\Gamma _ { S } ( k )$ matrix should be 1, one can estimate the CDR on a pair-by-pair basis using the method developed in [25]. According to (24), if SNR is given, a new DOA-independent CDR estimator for the $( i , j ) t h$ pair of sensors is given as

$$
\begin{array}{l} \mathrm{CDR} _ {i, j} (k) \\ = \frac {- g _ {i , j} (k) - \sqrt {g _ {i , j} ^ {2} (k) - (| e _ {i , j} (k) | ^ {2} - 1) | f _ {i , j} (k) | ^ {2}}}{| e _ {i , j} (k) | ^ {2} - 1}, \end{array}\tag{30}
$$

where

$$
e _ {i, j} (k) \triangleq [ \boldsymbol {\Gamma} _ {Y} (k) ] _ {i, j} + \frac {[ \boldsymbol {\Gamma} _ {Y} (k) ] _ {i , j} - [ \boldsymbol {\Gamma} _ {V} (k) ] _ {i , j}}{\mathrm{SNR} (k)},\tag{31}
$$

$$
f _ {i, j} (k) \triangleq [ \mathbf {\Gamma} _ {Y} (k) ] _ {i, j} - [ \mathbf {\Gamma} _ {R} (k) ] _ {i, j},\tag{32}
$$

$$
g _ {i, j} (k) \triangleq \Re \left\{e (k) _ {i, j} f _ {i, j} ^ {*} (k) \right\}.\tag{33}
$$

The CDR for the array is then calculated as

$$
\mathrm{CDR} (k) = \frac {2}{M (M - 1)} \sum_ {i = 1} ^ {M - 1} \sum_ {j = 0} ^ {i - 1} \mathrm{CDR} _ {i, j} (k),\tag{34}
$$

which represents the mean of CDR estimates across various pairs.

Given the SNR and CDR estimates, one can then compute the gain $G ( n , k )$ , the block diagram of which is illustrated in Fig. 2.

## 4. Evaluation

## 4.1. Setup

In our simulation, we employ the renowned image model method [38, 39] to simulate room impulse responses between the source and sensors within a room dimensions of 6 m×4 m×3 m. A 4-element uniform linear microphone array is utilized with an interelement spacing of 2 cm. The source signal, arbitrarily selected from the TIMIT database, consists of clean speech lasting $^ { 1 7 \ \mathrm { s } , }$ sampled at 16 kHz. Reverberation times $( T _ { 6 0 } )$ vary from 140 ms to 1000 ms across diferent simulation conditions. By convolving the source signal with the impulse response corresponding to the mth sensor, we obtain the signal captured by that sensor.

In our simulations, the noise signal $v _ { m } ( t )$ is a composite of interference noise, difuse noise [40], and white noise, with interference and difusion noise ratios to white noise approximately 6.5 dB each. Interference is generated akin to the source signal. Adjusting the input SNR involves scaling the noise signal $v _ { m } ( t )$ appropriately. As our method operates in the STFT domain, observations are segmented into frames of 512 samples with a hop size of 128 samples, followed by application of a Hanning window to each frame before Fourier transformation.

We explore four baseline approaches alongside our proposed method for comparative analysis: the traditional SNR-based Wiener approach [36], the CDR-based approach [25], TSNR [20], HRNR [20], and the adaptive weighted prediction estimation (AWPE) approach [41, 42].

## 4.2. Performance measures

To assess the proposed approaches comprehensively, we compute four performance metrics under varying simula tion conditions: fullband SNR Gain [36], LSD [43, 44], DRR [45, 46], speech-to-reverberation modulation energy ratio (SRMR) [47], and KR [48, 49].

The fullband SNR gain is the ratio between the fullband output SNR and the fullband input SNR, i.e.,

$$
\mathrm{SNRGain} = \frac {\mathrm{oSNR}}{\mathrm{iSNR}}.\tag{35}
$$

With out loss of generality, we choose the first sensor in the microphone array as the reference for evaluation. Then, the fullband output and input SNRs are written, respectively, as

$$
\mathrm{iSNR} = \frac {\mathbb {E} [ | s _ {\mathrm{d}} (t) | ] ^ {2}}{\mathbb {E} [ | v (t) | ] ^ {2}},\tag{36}
$$

$$
\mathrm{oSNR} = \frac {\mathbb {E} [ | s _ {\mathrm{fd}} (t) | ] ^ {2}}{\mathbb {E} [ | v _ {\mathrm{rn}} (t) | ] ^ {2}},\tag{37}
$$

where $s _ { \mathrm { d } } ( t ) = g _ { \mathrm { 1 , e a r l y } } ( t ) * s ( t )$ is the desired signal, $v ( t ) =$ $v _ { 1 } ( t )$ is the additive noise, and $s _ { \mathrm { f d } } ( t )$ and $v _ { \mathrm { r n } } ( t )$ are, respectively, the time-domain counterparts of $S _ { \mathrm { f d } } ( n , k )$ and $V _ { \mathrm { r n } } ( n , k )$ in (12).

The DRR of the array output can be expressed as

$$
\mathrm{DRR} = \frac {\mathbb {E} [ | s _ {\mathrm{fd}} (t) | ] ^ {2}}{\mathbb {E} [ | r _ {\mathrm{rr}} (t) | ] ^ {2}},\tag{38}
$$

where $r _ { \mathrm { r r } } ( t )$ is the time-domain counterpart of $R _ { \mathrm { r r } } ( n , k )$ in (12).

The LSD quantifies the distance between the desired signal and the array output, which is defined as

LSD

$$
\frac {1}{N} \sum_ {n = 0} ^ {N - 1} \sqrt {\frac {1}{K} \sum_ {k = 0} ^ {K - 1} \left| 1 0 \log_ {1 0} \frac {\hat {S} (n , k)}{S _ {\mathrm{d}} (n , k)} \right| ^ {2}},\tag{39}
$$

where $\hat { S } ( n , k )$ is the array output given in (12) and $S _ { \mathrm { d } } ( n , k ) = S ( n , k )$

Finally, the KR is applied to measure the amount of the musical noise in the array output. The KR is defined as

$$
\mathrm{KR} = \frac {\mathrm{kurt} _ {\mathrm{out}}}{\mathrm{kurt} _ {\mathrm{in}}},\tag{40}
$$

where $\mathrm { k u r t _ { o u t } }$ and ${ \mathrm { k u r t } } _ { \mathrm { i n } }$ are the Kurtosis of the array output and observed signals, respectively. The Kurtosis of a random process X is defined as $\mu _ { 4 } / \mu _ { 2 } ^ { 2 }$ , where $\mu _ { n }$ is nth order moment given by $\begin{array} { r } { \mu _ { n } = \int _ { 0 } ^ { \infty } x ^ { n } p _ { X } \overline { { ( x ) } } d x } \end{array}$ , and $p _ { X } ( x )$ Ris the probability density function.

It is worth to mention that all the SNR Gain, LSD, DRR, and KR are calculated in the logarithmic scale, i.e., $1 0 \mathrm { l o g } _ { 1 0 }$ (SNR Gain), $1 0 \mathrm { l o g } _ { 1 0 } ( \mathrm { L S D } )$ ， $1 0 \log _ { 1 0 } ( \mathrm { { D R R } ) }$ , and $\log _ { 1 0 } ( \mathrm { K R } )$

## 4.3. Performance comparison

To ensure a fair comparison of performance across different approaches, except for AWPE, all gains are applied to the output of the superdirective (SD) beamformer. These resulting approaches are denoted as SD-SNR, SD-CDR, SD-TSNR, and SD-HRNR, respectively.

In first set of simulations, we evaluate the CDR esti mator given in (30) and compare it with the one developed in [25]. The reverberation time $T _ { 6 0 }$ is set to 500 ms, the input SNR is set to $\mathrm { S N R } = 2 0 ~ \mathrm { d B }$ , the number of sensors is $M = 4 ,$ and the distance between adjacent sensors is 2 cm. It is worth noting that early reflections and noise signals are excluded when calculating the ground truth of the CDRs. The results are shown in Fig. 3. As seen, the proposed approach demonstrates lower estimation errors compared to the SD-CDR approach.

![](figures/16b1a83038aa4fc135866c4861c49680fe6b90ce717baf73cb81fb455f68f9fd.jpg)  
Figure 3: The error between groundtruth and estimated CDRs.

Table 1: The values of the SNR Gains, LSDs, and DRRs of the diferent approaches.

<table><tr><td>Approaches</td><td>SNR Gain</td><td>LSD</td><td>DRR</td></tr><tr><td>SD-SNR</td><td>9.8</td><td>7.2</td><td>8.3</td></tr><tr><td>SD-CDR</td><td>8.6</td><td>8.1</td><td>9.2</td></tr><tr><td>SD-TSNR</td><td>10.2</td><td>7.4</td><td>8.5</td></tr><tr><td>SD-HRNR</td><td>10.1</td><td>8.0</td><td>8.7</td></tr><tr><td>AWPE</td><td>-</td><td>11.1</td><td>-</td></tr><tr><td>Proposed</td><td>11.4</td><td>7.2</td><td>9.3</td></tr></table>

Referring to (17), we have two hyper-parameters, $\mathrm { i . e . , }$ $\beta _ { 1 }$ and $\beta _ { 2 }$ , to determine. Figure 4(a) illustrates the tradeof between SNR Gain and DRR for the proposed approach, varying with $\beta _ { 1 }$ and $\beta _ { 2 }$ . Here, the input SNR is 5 dB, the reverberation time $T _ { 6 0 }$ is approximately 500 ms, and $\beta _ { 1 }$ and $\beta _ { 2 }$ vary from 1 to 10 incrementally, with each curve corresponding to the same $\beta _ { 2 }$ . One can see from the plot that DRR increases with as the value of $\beta _ { 1 }$ increases, while SNR Gain rises with increasing $\beta _ { 2 }$ . Notably, when $\beta _ { 2 }$ surpasses a certain threshold, $\mathrm { e . g . , } \beta _ { 2 } \geq 5$ , further increments do not significantly enhance SNR Gain. Conversely, enhancing DRR appears to be more eficiently achieved by elevating $\beta _ { 1 }$ . Compared to traditional approaches, our method surpasses them in terms of both DRR and SNR Gain by selecting suitable values of $\beta _ { 1 }$ and $\beta _ { 2 }$

Figure 4(b) depicts the tradeof between SNR Gain and LSD concerning $\beta _ { 1 }$ and $\beta _ { 2 }$ , both ranging from 1 to 10 incrementally. Initially, LSD experiences a rapid decline with increasing the value of $\beta _ { 2 }$ . Since SNR Gain escalates with the value of $\beta _ { 2 }$ , this decrease in LSD correlates with SNR Gain augmentation. However, with further increments in the value of $\beta _ { 2 }$ , LSD increases alongside SNR Gain, implying that greater SNR enhancement leads to more significant signal distortion. Consequently, strategically increasing the value of $\beta _ { 2 }$ could be beneficial in practical scenarios. When $\beta _ { 2 }$ is fixed, say $\beta _ { 2 } > 3$ , a slight decrease in SNR Gain and a substantial increase in DRR occur with increasing the value of $\beta _ { 1 }$ , indicating enhanced reverberation suppression. However, the value of LSD rises with $\beta _ { 1 }$ , suggesting amplified signal distortion. Hence, a tradeof becomes necessary when determining the value of $\beta _ { 1 }$ in practical contexts.

![](figures/6726c4a492ac9fdd3dcd74cbd802bc9d02dac38c0526259d0d2d3642f64f2099.jpg)

(a)  
![](figures/fba169fbbd6112001f2f5348df6f5874c5f3c2c71bca7eeea4e5ec02a1dadd66.jpg)  
(b)  
Figure 4: (a) The DRR v.s. the SNR Gain, (b) the LSD v.s. the SNR Gain of baseline approaches and proposed one as a function of $\beta _ { 1 } ,$ , β2 (input SNR = 5 dB, $T _ { 6 0 } = 5 0 0$ ms).

Finally, we present the spectrograms of the clean, noisy and reverberant, and array output signals of the proposed method in Fig. 5, with $\beta _ { 1 } = 5$ and $\beta _ { 2 } = 3$ . Additionally, the corresponding CDR, SNR, and filter gain are plotted in Fig. 6. It is evident from these figures that the proposed approach efectively attenuates noise in the observations. Furthermore, Table 1 presents the SNR Gains, LSDs, and DRRs of various approaches, clearly demonstrating the superiority of our proposed method over traditional ones in terms of SNR Gain, LSD, and DRR.

## 4.4. Performance as a function of the input SNR

In this subsection, we assess the performance of the proposed approach under various input SNR conditions with the noise signal consisting of interference, difuse noise, and white noise. The reverberation time $T _ { 6 0 }$ is maintained to be approximately 500 ms. Figure 7 plots the SNR Gain, DRR, and LSD of diferent approaches. It is seen that the proposed approach surpasses traditional methods in both SNR Gain and LSD, with the DRR slightly exceeding that of the SD-CDR approach, consistent with the earlier evaluation of CDR estimation accuracy. Particularly noteworthy is the highest DRR achieved by our proposed approach, indicating superior reverberation suppression. This achievement primarily stems from our approach’s consideration of the noise signal during CDR estimation. Furthermore, the SNR Gain of the SD beam former remains nearly constant across input SNRs. This constancy arises because the SNR Gain relies on the coherence matrix of the noisy environment, rather than the covariance matrix, which depends on noise variance.

![](figures/67de3b426ee802b4f5015fc7d1106b7b96e10ed6ff05588a32af1c5631b90292.jpg)

(a)  
![](figures/355dbf1af139ad445cfb09f07cfc68c12483299d85395326091a8f2e92ffb401.jpg)  
(b)

![](figures/8d4ac3083fa78e0964786bb58034cbc6ba30363d448c925e5bd602d977334722.jpg)  
(c)  
Figure 5: The spectrograms of: (a) the clean speech, (b) the noisy observation (input $\mathrm { S N R } = 5$ dB and $T _ { 6 0 } = 5 0 0 ~ \mathrm { m s } )$ , and (c) the filter output (SNR Gain= 11.4 dB ).

Interestingly, the variation in DRR is minimal for both the SD-CDR approach and our proposed method across varying input SNRs. This stability stems from the fact that the Wiener gain of both approaches depends on the CDR, which reflects the level of reverberation. Moreover, CDR estimation is not significantly influenced by changes in background noise level.

![](figures/80c0d0e097efb94c3ef34c6908eeb0d2c0eb356fd6452aab53c27939f6827858.jpg)  
(a)

![](figures/e0395b8e242ee3d39f8edffc935157d3a06387baf3cec391870ed51088a1e059.jpg)  
(b)

![](figures/de32a4c3b4bb320e952f61889017103a237853622627d5a5ac15ea3cdde47a42.jpg)  
(c)  
Figure 6: CDR, SNR, and the filter gain.

## 4.5. Performance versus reverberation time

The proposed Wiener gain is determined by both the SNR and CDR. Given that the CDR reflects the degree of reverberation, it is interesting to evaluate the performance of our approach under varying reverberation conditions. These results are plotted in Fig. 8 where the input SNR is 5 dB. Interestingly, the level of reverberation has minimal impact on LSD, with only slight reduction observed under high reverberation conditions. This phenomenon can be attributed to the fact that signal distortion primarily arises from noise suppression. Furthermore, the DRR of all methods exhibits a rapid decline with increasing reverberation time. However, the DRR of the proposed approach surpasses that of traditional methods, as demonstrated in the local enlarged view, particularly when $T _ { 6 0 }$ is 200 ms and 500 ms.

![](figures/9a7d2a69e33aa41d6769926fb3a7a87ed248582018ee2c64e0ae45d7cffad915.jpg)  
(a)

![](figures/2ebe07d85b391d60564a9926d0df79847b7bbeaf3aa3df2d04bdc6b68b306b3e.jpg)  
(b)

![](figures/ddf11c9634518a553a2738a5ebd6fbc9ecddc6d489892a14c639079526f6db8f.jpg)  
(c)  
Figure 7: The SNR Gain, LSD, and DRR of the compared methods as a function of the input SNR.

In addition to the CDR-based approaches, the AWPE [41, 42] method is also widely used for dereverberation.

![](figures/7a956830c37c4b4d33283feca0c3fa37fe65d9791e2a937e155e2d25dc8b5063.jpg)

(a)  
![](figures/9b38902da7179d8fa35a5f4a171f8fce39e2f8bccfee36cc4d399b629e8163d9.jpg)

(b)  
![](figures/e431841f122a612113e60a3b05e57d81ec3a8071c2e5c908ce8c567d98e98a33.jpg)  
(c)  
Figure 8: The SNR Gain, LSD and DRR of the compared methods versus reverberation time.

To further compare the dereverberation performance of AWPE with other approaches, we calculate the speech-toreverberation modulation ratio (SRMR) for all methods (note that AWPE does not use DRR). These results are illustrated in Fig. 9, where the reverberation time $T _ { 6 0 }$ is approximately 500 ms. Observing the figure, we note that the SRMR of the AWPE approach is slightly lower than that of SD-CDR and our proposed approach when the input SNR is high (i.e., 20 dB). However, as the input SNR decreases, the SRMR of AWPE declines rapidly compared to other methods, indicating its high sensitivity to additive noise. In contrast, it is evident that the proposed approach outperforms AWPE in environments with both noise and reverberation.

![](figures/ead83db9ebb19870e9d8f673177c043e4a17df23930648a825079c693c296c4c.jpg)

Figure 9: The SRMR of the compared methods as a function of the input SNR.  
![](figures/05a1fe9eed228c8acac1c423c801043b710add73ff633fdc8055915a9fa47750.jpg)  
Figure 10: The log Kurtosis ratio of the diferent approaches as a function of $G _ { \mathrm { m i n } } .$

## 4.6. Impact of $G _ { \mathrm { m i n } }$ on performance

The minimum value of the Wiener gain, i.e., $G _ { \mathrm { m i n } } .$ serves as a crucial hyperparameter in filter implementation. Smaller values of $G _ { \mathrm { m i n } }$ typically yield larger SNR Gain. However, the occurrence of musical noise becomes a concern if $G _ { \mathrm { m i n } }$ falls below a certain threshold. To assess the presence of musical noise, the Kurtosis ratio is introduced in [48, 49]. A higher Kurtosis ratio indicates a greater risk of musical noise generation. Figure 10 plots the Kurtosis ratio of our proposed approach as a function of $G _ { \mathrm { m i n } }$ where the input SNR is 5 dB and the reverberation time $T _ { 6 0 }$ is approximately 500 ms.

As seen, the Kurtosis ratio increases as the value of $G _ { \mathrm { m i n } }$ decreases, indicating a higher risk of musical noise. Opting for $G _ { \mathrm { m i n } } = 0 . 1$ appears prudent, as the Kurtosis ratio remains relatively stable for $G _ { \mathrm { m i n } } \geq 0 . 1$ . Additionally, it is noteworthy that the Kurtosis ratio of our proposed approach is lower than that of the SD-SNR, SD-TSNR, and SD-HRNR methods. Since SD is a fixed beamformer, it does not introduce musical noise, thus maintaining a consistently low Kurtosis ratio, as depicted in Fig. 10. Sur prisingly, the Kurtosis ratio of the SD-CDR approach also remains minimal across changes in $G _ { \mathrm { m i n } }$ . However, despite this, given the inferior SNR Gain of both SD and SD-CDR approaches, our proposed method still outperforms them.

## 5. Conclusions

In this paper, we proposed an approach to the design of the Wiener gain for microphone array beamforming. The resultant Wiener gain is a function of both SNR and CDR, featuring two hyperparameters to suppress background noise and reverberation. By employing the SD beamformer as the spatial filter and integrating our proposed Wiener gain as the post-filter, we evaluated our approach and also compared it with some widely used methods in terms of SNR improvement, LSD, DRR, SRMR, and Kurtosis ratio. The results demonstrate the superiority of our proposed method over the compared ones.

## Acknowledgements

## References

[1] K. U. Simmer, J. Bitzer and C. Marro, Post-filtering techniques, Microphone Arrays. Springer, New York, 2001, pp. 36-60.

[2] I. McCowan and H. Bourlard, Microphone array post-filter based on noise field coherence, IEEE Trans. Speech Audio Process. 11 (6) (2003) 709-716.

[3] J. Capon, High resolution frequency-wavenumber spectrum analysis, Proc. IEEE, 57 (1969) 1408-1418.

[4] J. Benesty, J. Chen, and Y. Huang, A generalized MVDR spec trum, IEEE Signal Process. Lett. 12 (2005) 827-830.

[5] C. Pan, J. Chen, and J. Benesty, On the noise reduction performance of the MVDR beamformer in noisy and reverberant environments, in: Proc. IEEE ICASSP, Florence, Italy, May, 2014, pp. 815-819.

[6] H. Cox, R. M. Zeskind, T. Kooij, Practical Supergain, IEEE Trans. Acoust.,Speech, Signal Process. 34 (3) (1986) 393–398.

[7] J. Li, P. Stoica and Zhisong Wang, On robust Capon beamforming and diagonal loading, IEEE Trans. Signal Process. 51 (7) (2003) 1702-1715.

[8] S. A. Vorobyov, A. B. Gershman and Z. Luo, Robust adaptive beamforming using worst-case performance optimization: a solution to the signal mismatch problem, IEEE Trans. Signal Process. 51 (2) (2003) 313-324.

[9] S. Shahbazpanahi, A. B. Gershman, Z. Luo and K. Wong, Robust adaptive beamforming for general-rank signal models, IEEE Trans. Signal Process. 51 (9) (2003) 2257-2269.

[10] S. A. Vorobyov, A. B. Gershman and Y. Rong, On the Relationship between the Worst-Case Optimization-Based and Probability-Constrained Approaches to Robust Adaptive Beam forming, in: Proc. IEEE ICASSP, Honolulu, USA, Apr., 2007, pp. 977-980.

[11] J. L. Flanagan, J. D. Johnson, R. Zahn, and G. W. Elko, Computer-steered microphone arrays for sound transduction in large rooms, J. Acoust. Soc. Amer. 78 (5) (1985) 1508–1518.

[12] B. Rafaely, Phase-Mode Versus Delay-and-Sum Spherical Microphone Array Processing, IEEE Signal Process. Lett. 12 (10) (2005) 713–716.

[13] J. M. Kates, Superdirective Arrays for Hearing Aids, J. Acoust. Soc. Amer. 94 (4) (1993) 1930-1933.

[14] S. Doclo, M. Moonen, Superdirective Beamforming Robust Against Microphone Mismatch, IEEE Trans. Acoust., Speech, Signal Process. 15 (2) (2007) 617-631.

[15] C. Pan, J. Chen, and J. Benesty, Reduced-order robust superdirective beamforming with uniform linear microphone arrays IEEE/ACM Trans. Audio, Speech, Lang. Process. 24 (9) (2016) 1548-1560.

[16] J. Benesty, J. Chen, E. A. P. Habets. Speech Enhancement in the STFT Domain, Springer Briefs in Electrical and Computer Engineering, Berlin, 2011.

[17] J. Benesty, J. Chen, Optimal Time-Domain Noise Reduction Filters-A Theoretical Study, Springer Briefs in Electrical and Computer Engineering, Berlin, 2011.

[18] Y. Ephraim and D. Malah, Speech enhancement using a mini mum mean-square error log-spectral amplitude estimator, IEEE Trans. Acoust., Speech, Signal Process. 33 (2) (1985) 443-445.

[19] I. Cohen, Noise Spectrum Estimation in Adverse Environment: Improved Minima Controlled Recursive Averaging, IEEE Trans. Acoust., Speech, Signal Process. 11 (5) (2003) 466-475.

[20] C. Plapous, C. Marro and P. Scalart, Improved Signal-to-Noise Ratio Estimation for Speech Enhancement, IEEE Trans. Audio, Speech, Lang. Process. 14 (6) (2006) 2098-2108.

[21] O. Cappe, Elimination of the musical noise phenomenon with Ephraim and Malah noise suppressor, IEEE Trans. Speech Audio Process. 2 (2) (1994) 345-349.

[22] M. Jeub, C. M. Nelke, C. Beaugeant, and P. Vary, Blind estimation of the coherent-to-difuse energy ratio from noisy speech signals, in: Proc. EUSIPCO, Barcelona, Spain, Aug., 2011, pp. 1347-1351.

[23] O. Thiergart, G. DelGaldo, and E. A. P. Habets, Signal-toreverberant ratio estimation based on the complex spatial coherence between omnidirectional microphones, in: Proc. IEEE ICASSP, Kyoto, Japan, Mar., 2012, pp. 309-312.

[24] O. Thiergart, G. DelGaldo, and E. A. P. Habets, On the spatial coherence in mixed sound fields and its application to signal-todifuse ratio estimation, J. Acoust. Soc. Amer. 132 (4) (2012) 2337-2346.

[25] A. Schwarz and W. Kellermann, Coherent-to-difuse power ratio estimation for dereverberation, IEEE/ACM Trans. Audio, Speech, Lang. Process. 23 (6) (2015) 1006-1018.

[26] P. Calamia, N. Balsam and P. Robinson Blind estimation of the direct-to-reverberant ratio using a beta distribution fit to binaural coherence, J. Acoust. Soc. Amer. 148 (4) (2020) EL359.

[27] H. W. L¨ollmann, A. Brendel and W. Kellermann, Efective Rank-Based Estimation of the Coherent-to-Difuse Power Ratio, in: Proc. IEEE ICASSP, Toronto, Canada, Jun., 2021, pp. 955-959.

[28] C. Zheng, X. Li, A. Schwarz and W. Kellermann, Statistical analysis and improvement of coherent-to-difuse power ratio estimators for dereverberation, in: Proc. IWAENC, Xi’an, China, Sept., 2016, pp. 1-5.

[29] Y. Fang, H. Feng and Y. Chen. A robust interaural time differences estimation and dereverberation algorithm based on the coherence function, Appl. Acoust. 129 (2018) 126-134.

[30] A. Brendel and W. Kellermann, Learning-based Acoustic Source Localization in Acoustic Sensor Networks using the Coherent-to-Difuse Power Ratio, in: Proc. EUSIPCO, Rome, Italy, Sept., 2018, pp. 1572-1576.

[31] M. Zohourian and R. Martin, Binaural Direct-to-Reverberant Energy Ratio and Speaker Distance Estimation, IEEE/ACM Trans. Audio, Speech, Lang. Process. 28 (2019) 92-104.

[32] S. Braun, A. Kuklasinski, O. Schwartz, O. Thiergart, E. A. P. Habets, S. Gannot, S. Doclo and J. Jensen, Evaluation and

Comparison of Late Reverberation Power Spectral Density Estimators, IEEE/ACM Trans. Audio, Speech, Lang. Process. 26 (6) (2018) 1056-1071.

[33] I. Kodrasi and S. Doclo, Analysis of Eigenvalue Decomposition-Based Late Reverberation Power Spectral Density Estimation, IEEE/ACM Trans. Audio, Speech, Lang. Process. 26 (6) (2018) 1106-1118.

[34] H. W. L¨ollmann, A. Brendel, and W. Kellermann, Generalized Coherence-based Signal Enhancement, in: Proc. IEEE ICASSP, Barcelona, Spain, May, 2020, pp. 201-205.

[35] J. Benesty, I. Cohen, J. Chen, Array Beamforming with Linear Diference Equations, Springer-Verlag, Berlin, 2021.

[36] J. Benesty, J. Chen, Y. Huang, and I. Cohen, Noise Reduction in Speech Processing, Springer-Verlag, Berlin, 2009.

[37] R. J. McAulay and M. L. Malpass, Speech enhancement using a soft-decision noise suppression filter, IEEE Trans. Acoust., Speech, Signal Process. 28 (2) (1980) 137-145.

[38] J. Allen, D. Berkley, and J. Blauert, Multimicrophone signalprocessing technique to remove room reverberation from speech signals, J. Acoust. Soc. Amer. 62 (4) (1977) 912-915.

[39] C. Pan, L. Zhang, Y. Lu, J. Jin, L. Qiu, J. Chen, J. Benesty, An Anchor-Point Based Image-Model for Room Impulse Response Simulation with Directional Source Radiation and Sensor Directivity Patterns, ArXiv abs/2308.10543 (2023) 1–19.

[40] E. A. P. Habets and S. Gannot, Generating sensor signals in isotropic noise fields,J. Acoust. Soc. Amer. 122 (6) (2007) 3464- 3470.

[41] T. Yoshioka, T. Nakatani, and M. Miyoshi, Integrated speech enhancement method using noise suppression and dereverberation, IEEE Trans. Audio, Speech, Lang. Process. 17 (2) (2009) 231-246.

[42] T. Yoshioka, Speech enhancement in reverberant environments, PhD thesis, Tyoto Univ., Tyoto, Japan, 2010.

[43] I. Cohen and S. Gannot, Springer Handbook of Speech Processing, Springer-Verlag, Berlin, 2008, pp. 873-901.

[44] C. Pan, J. Chen and G. Shi, On Estimation of Time-Varying Variances of Source and Noise for Sensor Array Processing, IEEE/ACM Trans. Audio, Speech, Lang. Process. 28 (2020) 2865-2879.

[45] J. Jo and M. Koyasu, Measurement of reverberation time based on the direct-reverberant sound energy ratio in steady state, in: Proc. of Inter-noise 75, 1975, pp. 579-582.

[46] Y. Hioka, K. Niwa, S. Sakauchi, K. Furuya and Y. Haneda, Estimating direct-to-reverberant energy ratio based on spatial correlation model segregating direct sound and reverberation, in: Proc. IEEE ICASSP, Dallas, USA, Mar., 2010, pp. 149-152.

[47] T. H. Falk, C. Zheng, and W. Chan, A non-intrusive quality and intelligibility measure of reverberant and dereverberated speech, IEEE Trans. Audio, Speech, Lang. Process. 18 (7) (2010) 1766- 1774.

[48] Y. Uemura, Y. Takahashi, H. Saruwatari, K. Shikano, K. Kondo, Automatic optimization scheme of spectral subtraction based on musical noise assessment via higher-order statistics, in: Proc. IWAENC, Seattle, USA, Sept., 2008.

[49] R. Miyazaki, H. Saruwatari, S. Nakamura, K. Shikano, K. Kondo, J. Blanchette, M. Bouchard, Musical-noise-free blind speech extraction integrating microphone array and iterative spectral subtraction, Signal Process. 102 (2014) 226-239.