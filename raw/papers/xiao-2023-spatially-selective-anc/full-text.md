
View
Online 
Export
Citation
MAY 03 2023
Spatially selective active noise control systems
Tong Xiao 
 ; Buye Xu 
 ; Chuming Zhao 
J. Acoust. Soc. Am. 153, 2733 (2023)
https://doi.org/10.1121/10.0019336
Articles You May Be Interested In
Enhancing binaural rendering of head-worn microphone arrays through the use of adaptive spatial
covariance matching
J. Acoust. Soc. Am. (April 2022)
Mechanical Shocks Produced on Hearing‐Aid Transducers
J. Acoust. Soc. Am. (December 1962)
A stacked self-attention network for two-dimensional direction-of-arrival estimation in hands-free speech
communication
J. Acoust. Soc. Am. (December 2022)
 08 September 2026 00:09:31
Spatially selective active noise control systems
Tong Xiao,1,a)
Buye Xu,2
and Chuming Zhao2
1Centre for Audio, Acoustics and Vibration, University of Technology Sydney, New South Wales 2007, Australia
2Meta Reality Labs Research, Redmond, Washington 98052, USA
ABSTRACT:
Active noise control (ANC) systems are commonly designed to achieve maximal sound reduction regardless of the
incident direction of the sound. When desired sound is present, the state-of-the-art methods add a separate system to
reconstruct it. This can result in distortion and latency. In this work, we propose a multi-channel ANC system that only
reduces sound from undesired directions, and the system truly preserves the desired sound instead of reproducing it. The
proposed algorithm imposes a spatial constraint on the hybrid ANC cost function to achieve spatial selectivity. Based on
a six-channel microphone array on a pair of augmented eyeglasses, results show that the system minimized only noise
coming from undesired directions. The control performance could be maintained even when the array was heavily per-
turbed. The proposed algorithm was also compared with the existing methods in the literature. Not only did the proposed
system provide better noise reduction, but it also required much less effort. The binaural localization cues did not need to
be reconstructed since the system preserved the physical sound wave from the desired source.
V
C 2023 Author(s). All article content, except where otherwise noted, is licensed under a Creative Commons
Attribution (CC BY) license (http://creativecommons.org/licenses/by/4.0/). https://doi.org/10.1121/10.0019336
(Received 2 December 2022; revised 14 March 2023; accepted 17 April 2023; published online 3 May 2023)
[Editor: Efren Fernandez-Grande]
Pages: 2733–2744
I. INTRODUCTION
Active noise control (ANC) systems have seen many
signiﬁcant
advancements
over
the
past
few
decades.
Notably, many personal ANC headphones, aiming to elimi-
nate the unwanted noise for users, have emerged and gained
much success in the market due to their excellent perfor-
mance and robustness (Chang et al., 2016). Other ANC sys-
tems, such as ANC headrests (Elliott et al., 2018; Xiao
et al., 2020) and ANC windows (Lam et al., 2020; Wang
et al., 2017), have also seen signiﬁcant improvements over
the years. These ANC systems have been designed to attenu-
ate all the sound in the environment. One emerging applica-
tion is using ANC to enhance face-to-face conversations in
a noisy environment, e.g., a cocktail-party scenario, where
one hopes to minimize the surrounding noises while still
maintaining the conversations in front of the user. An intelli-
gent ANC system should separate and categorize sounds
coming from various directions. The desired sound should
be maintained for the user while noises coming from other
directions are minimized.
The goal of this work is to develop a spatially selective
ANC system that preserves sound coming from the desired
directions while reducing noise from other directions. The
ﬁltered reference least-mean square (FxLMS) algorithm is
commonly used in these systems for adaptive control due to
its simplicity and robustness (Elliott, 2000; Hansen et al.,
2012; Kuo and Morgan, 1996). Any signals observed by the
reference
microphones
(or
error
microphones
in
the
feedback systems) will be fully controlled regardless of the
residual noise spectrum at the error microphones. So far,
most effort in the ANC systems has been devoted to improv-
ing the noise reduction (NR) level throughout the spectrum
as much as possible.
In recent years, some studies have considered the spatial
aspect of personal ANC systems. Studies (Cheer et al., 2019;
Liebich et al., 2018; Rafaely and Jones, 2002; Zhang and Qiu,
2014) have shown that the performance in ANC headphones
and earphones was affected by the time advance between the
reference and the error microphones in the feedforward conﬁg-
urations. The ANC performance was the best when the time
advance was the most signiﬁcant. However, these systems
were studied to further improve the control performance when
dealing with direction- and/or time-varying noises. They were
not designed for spatial noise selection.
There
are
systems,
which
were
not intentionally
designed, that can be modiﬁed to achieve spatial selection
functionality. For example, the coherence-based selection
method (Shen et al., 2021) can potentially be used to deter-
mine the direction of arrival (DOA) of the noise, which can
then be isolated. The selective ﬁxed-ﬁlter method (Shi et al.,
2020; Shi et al., 2022) and the deep ANC method (Zhang
and Wang, 2021) can be extended to selecting spatial ﬁlters
to control noise coming from certain DOAs. However, these
systems still have issues. The coherence-based selection
method requires the input signals to be distinguished enough
to offer differences in the coherence functions. Thus, it may
be limited to certain spread-out array conﬁgurations, e.g., an
array distributed in a room. The selective ﬁxed-ﬁlter method
and the deep ANC method require the system to be pre-
a)Electronic mail: Tong.Xiao@uts.edu.au
J. Acoust. Soc. Am. 153 (5), May 2023
V
C Author(s) 2023.
2733
0001-4966/2023/153(5)/2733/12/$30.00
ARTICLE
...................................
 08 September 2026 00:09:31
trained to obtain the optimal ﬁlters in advance. These two
methods also require the spatial information to be acquired
elsewhere, thus, resulting in additional computations. These
systems are not yet the best solutions for a spatially selective
ANC system.
To achieve spatial selectivity, it is common to use the
beamforming technique. Beamforming is a well-established
method of designing spatiotemporal ﬁlters for array process-
ing (Doclo et al., 2015; Van Trees, 2002; Van Veen and
Buckley, 1988). For personal devices, a certain number of
microphones can be used to differentiate sound from differ-
ent directions. Hearing aids typically employ beamforming
to improve speech intelligibility for the hearing impaired.
Studies have incorporated the ANC functionality to control
the leakage sound in open-ﬁtting systems, which improves
the insertion signal-to-noise ratio (SNR) gain of the multi-
channel Wiener ﬁlter (MWF) (Dalga and Doclo, 2011;
Serizel et al., 2010). Serizel et al. (2010) used the feedfor-
ward ANC to control the leakage noise, while Dalga and
Doclo (2011) further improved the result by using the hybrid
control due to its better ANC performance. However, the
desired sound in the leakage is canceled (together with the
noise) and then added back to the error signal with a delay.
Recent work by Patel et al. (2020) proposed a structure for a
pair of hear-through ANC headphones. The microphones
were grouped for different purposes independently, i.e.,
ANC and beamforming, and the desired sound from the
beamformer was injected into the secondary sources.
The studies from above can be improved regarding the
following three aspects:
(1) Control effort: Current studies require canceling both
noise and the desired sound ﬁrst and then reproducing
this desired sound again. Thus, the control effort can be
signiﬁcant.
(2) ANC performance: When an adaptive ANC system
needs to reduce both noise and the desired sound, the
attenuation of the noise may be degraded because the
desired sounds, e.g., speech and music, are often non-
stationary, which can drive the adaptive system to sub-
optimal states.
(3) Distortion to the desired sound: When the desired sound
needs to be reconstructed and reproduced acoustically, it
introduces latency and is prone to different types of dis-
tortions, e.g., undesired frequency shaping or binaural
cue distortion for ear-level devices.
These aspects lead to the question, “Instead of minimiz-
ing the noise plus the desired sound and then adding the
desired sound once again, can the system control only the
noise but not the desired sound?”
This article, based on the previous work (Xu and
Miller, 2019), proposes a spatially selective ANC system
that only controls the unwanted noise while leaving the
desired physical sound unaltered. The proposed algorithm is
derived based on the hybrid ANC architecture when both
the reference and the error signals can be used as inputs for
both ANC and the spatial constraint at the same time to
optimize the performance. The constraint vector describing
the frequency response of the signal from the desired DOA
at the error microphone will make sure the desired signal
component is physically preserved rather than reconstructed
to avoid the three aforementioned issues.
II. PROPOSED SPATIALLY SELECTIVE ANC SYSTEMS
A. Signal definition and cost function
Without losing generality, we assume there is one
desired sound source and multiple noise sources in the
scene (see Fig. 1). The ANC system contains a total of K
microphones, one of which serves as an error microphone.
One error microphone with one secondary source is used
in the derivation hereinafter for notation brevity, but it
can be easily extended to cases with multiple sources and/
or microphones. The disturbance signal, d(n), at the error
microphone
with
ANC
disabled
includes
two
components,
dðnÞ ¼ sðnÞ þ vðnÞ;
(1)
where s(n) and v(n) are the desired signal and the noise sig-
nal, respectively, and n denotes the time index. We assume
that the two signals come from different locations and there
is one desired source for now.
We write the error signal e(n) of the hybrid ANC sys-
tem in matrix multiplication form as (Hansen et al., 2012)
eðnÞ ¼ dðnÞ þ wTGTxðnÞ
(2a)
¼ ~d
TxðnÞ þ wTGTxðnÞ
(2b)
¼ uTxðnÞ;
(2c)
where
w 2 RKL ¼ wT
1 wT
2    wT
K

T;
(3a)
FIG. 1. (Color online) Concept diagram of a spatially selective ANC system
preserving the desired sound from one direction and using a secondary
source to control noise from other directions at the error microphone (one
shown here for demonstration).
2734
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
wk 2 RL ¼ wk0 wk1    wk L1
ð
Þ
½

T;
(3b)
G 2 RKLKL ¼ diag ^G ^G    ^G
ð
Þ;
(3c)
^G 2 RLL ¼
^g0
0
0
  
0
^g1
^g0
0
  
0
^g2
^g1
^g0
  
0
...
...
...
..
.
...
^gL1
^gL2
^gL3
  
^g0
2
66666664
3
77777775
;
(3d)
x n
ð Þ 2 RKL ¼ xT
1 n
ð Þ    xT
K1 n
ð Þ ^d
T n
ð Þ
h
iT
;
(3e)
xk n
ð Þ 2 RL ¼ xk n
ð Þ xk n1
ð
Þ  xk nLþ1
ð
Þ

T;
(3f)
^d n
ð Þ 2 RL ¼
^d n
ð Þ ^d n  1
ð
Þ  ^d n  L þ 1
ð
Þ
h
iT
;
(3g)
~d 2 RKL ¼
0T
  
0T
dT

T;
(3h)
u 2 RKL ¼ ~d þ Gw;
(3i)
where wk is the control ﬁlter with L length for the kth chan-
nel ðk ¼ 1; 2; …; KÞ. Superscript ðÞT denotes the transpose,
and hat accent ^ represents the estimated value. ^G is the
Toeplitz matrix of ^g, which is the estimation of the second-
ary path impulse response. We assume that it agrees well
with the actual one, i.e., ^g ¼ ½^g0 ^g1 … ^gL1T  g. This
assumption holds in many situations and will be made here-
inafter. d ¼ ½1 0 … 0T is the Dirac delta function. ^dðnÞ is
the vector of the estimated past values of the disturbance
signal dðnÞ. At the time n þ 1, and after when the ANC is
enabled, it is recovered from the error signal e(n) as
^dðn þ 1Þ ¼ eðnÞ  ^gTyðnÞ;
(4)
where y(n) is the secondary source signal (Kuo and Morgan,
1996).
The spatial selection functionality is achieved by apply-
ing a spatial constraint on the cost function of a traditional
ANC system. From Eq. (2), the spatial constraint for a single
desired source can be expressed as
HTu ¼ f;
(5)
from the Frost algorithm (Frost, 1972). Matrix H consists of
the relative impulse responses (ReIRs) of the array, i.e.,
H 2 RKLL ¼ H1 H2    HK
½
T;
(6)
where Hk is the Toeplitz matrix from hk ¼ ½hk0 hk1 hk2
   hkðL1ÞT, which is the ReIR between the kth microphone
and a chosen reference microphone (the one closest to the
desired source). Vector f 2 RL is a constraint vector that
describes the frequency response of the signal from the
desired direction at the error microphone. It is deﬁned as
f ¼ hK ¼ hK0 hK1    hKðL1Þ

T:
(7)
With ANC enabled, compared with the disturbance sig-
nal in Eq. (1), the error signal will also contain two
components,
eðnÞ ¼ esðnÞ þ vANCðnÞ;
(8)
where esðnÞ is the residual desired signal and vANCðnÞ is the
residual noise. By choosing the appropriate reference chan-
nel for H and the vector f that corresponds to the direction
of interest, the proposed system will reduce only the noise,
v(n), to vANCðnÞ. The constraint vector f in Eq. (7) can
enable the system to preserve the original desired sound
component at the error microphone, i.e., esðnÞ ¼ sðnÞ,
instead of reconstructing it as in Dalga and Doclo (2011),
Patel et al. (2020), and Serizel et al. (2010).
Finally, the cost function of the proposed system can be
written as
min
w
E e2 n
ð Þ


¼ min
w
E uTUxxu


¼ min
w
E
~d þ Gw

TUxx ~d þ Gw


n
o
such that HT ~d þ Gw


¼ f;
(9)
where Uxx 2 RKLKL ¼ E xðnÞxTðnÞ


is the autocorrela-
tion matrix of the tap-stacked input vector, and operator
Efg denotes mathematical expectation.
B. Optimal solution
The optimal solution can be found by setting the gradi-
ent of the cost function to zero and solving the Lagrange
multipliers k 2 RL (Haykin, 2002). The derivation of such
an optimal solution can be found in Appendix A, where the
solution is provided in Eq. (A4). It can be re-written in the
following form for interpretation:
wopt ¼ U1
rr /rd
þU1
rr GTH HTGU1
rr GTH þ qI

1f
U1
rr GTH HTGU1
rr GTH þ qI

1

HT~d  HTGU1
rr /rd

	
;
(10)
where
rðnÞ ¼ GTxðnÞ;
(11a)
Urr ¼ E rðnÞrTðnÞ


þ bI;
(11b)
/rd ¼ EfrðnÞdðnÞg:
(11c)
This optimal solution has three terms. The ﬁrst term is
the Wiener solution of a hybrid ANC system controlling all
the observable sounds. The second term is due to the spatial
constraint, which is similar to the beamformer solution in
Frost (1972), but the secondary path matrix G is added due
to the physical constraint of the ANC system. The third term
provides the coupling of the two subsystems. All three terms
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
2735
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
contribute to calculating the control ﬁlter w such that only
the noise from the undesired directions is minimized. The
residual desired signal component in the residual error sig-
nal after control is the original desired physical sound left
unaltered by the proposed system. Further details about pre-
serving or reconstructing this desired physical sound will be
emphasized in Sec. IV.
Note that matrix HTGU1
rr GTH is rank-deﬁcient due to
G being rank-deﬁcient. (There are delays in the secondary
paths.) Thus, a Tikhonov regularization factor q has been
applied to the diagonal elements to make it invertible
(Tikhonov and Arsenin, 1977).
Note that Eq. (11b) has also been added with a regulari-
zation factor b compared to Eq. (A4), which is equivalent to
adding a penalty term, the l2 norm of the control ﬁlter jjwjj2
in Eq. (9). This is essentially the leaky version of the algo-
rithm for a more robust ANC system (Cartes et al., 2002;
Elliott et al., 1992). The robustness of the system will be
further discussed in Sec. II E.
C. Adaptive solution
Commonly, adaptive algorithms are used to reduce
computations and handle fast environmental changes. The
derivations of the adaptive solution in the proposed method
can be found in Appendix B. The ﬁnal solution is expressed
as
wð0Þ ¼ q;
(12a)
wðn þ 1Þ ¼ P wðnÞ  lGTxðnÞeðnÞ


þ q;
(12b)
where
P ¼ I  GTH HTGGTH þ cI

1HTG;
(13a)
q ¼ GTH HTGGTH þ cI

1 f  HT~d
ð
Þ;
(13b)
and l is the step-size. Figure 2 illustrates the block diagram
of the proposed adaptive spatially selective ANC system.
Notice that the solution is coupled by the adaptive algo-
rithm in the ANC subsystem and the adaptive Frost algo-
rithm. The spatial constraint in Eq. (9) resulted in P and q.
Without it, the solution would become wðn þ 1Þ ¼ wðnÞ
lGTxðnÞeðnÞ, which is a traditional adaptive hybrid ANC
solution minimizing the overall error signal (Elliott, 2000;
Hansen et al., 2012).
Notice that a regularization factor c in Eq. (13) has been
added compared to Eq. (B5). Similarly to the optimal solu-
tion, although the matrix HTH is invertible due to the use of
ReIRs, that is, there is always an identity matrix in H,
matrix HTGGTH is rank-deﬁcient. Therefore, c has been
added for inversion.
D. Spectral weighting
In some cases, spatial ﬁltering alone may not be sufﬁ-
cient due to limitations of the array, e.g., ﬁlter length, array
conﬁguration. To deal with this, the proposed method can
be further improved by applying a spectral weighting ﬁlter,
i.e.,
F 2 RL ¼ ShK
(14)
instead of f in Eq. (7). S 2 RLL is the Toeplitz matrix of
the impulse response of the spectral weighting ﬁlter to atten-
uate the frequency range that is not of interest. Note that S is
a digital ﬁlter, which can be designed to be minimum-phase.
A non-minimum-phase ﬁlter is not desired since it leads to
delays in the error signal.
This technique is performed provided that the frequency
range attenuated by the spectral ﬁlter has little overlap with
that of the desired signal. Otherwise, one needs to consider
the trade-off between NR and signal distortion.
E. Robustness
Robustness is an important factor to consider. The
robustness issues in ANC systems can be contributed by
non-stationary inputs, low SNR, and/or secondary path
changes (Cartes et al., 2002; Elliott, 2000). Many beam-
forming systems are subject to numerical and/or spatial
robustness issues arising from signal mismatches, which are
due to mismatches between the presumed and actual relative
transfer functions (Gannot et al., 2017; Vorobyov, 2013).
We will mainly focus on the numerical robustness issue due
to signal mismatches herein.
For the proposed joint optimization problem, the robust-
ness of the system can be from the following aspects:
(1) Robustness of the ANC subsystem
(2) Robustness of the beamforming subsystem
(3) ANC on the beamforming subsystem
(4) Beamforming on the ANC subsystem (due to signal
mismatches).
The former two aspects can be easily understood since
each subsystem can inherently have its own robustness
issues. The solutions to these issues can also be easily found
in many studies. For example, the ANC subsystem can use a
leaky algorithm constraining jjwjj2 in the cost function
(Cartes et al., 2002; Tobias and Seara, 2004). As for a robust
beamformer, the diagonal loading method can be used. This
is achieved by constraining the white noise gain (WNG)
FIG. 2. (Color online) Block diagram of proposed spatially selective ANC
system. The adaptive hybrid ANC algorithm is spatially constrained.
2736
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
jjujj2 in the cost function (Cox et al., 1987; Li et al., 2003;
Vorobyov, 2013).
The latter two issues are due to the joint optimization of
ANC and beamforming. The third issue arises from the sec-
ondary paths in ANC systems, particularly the delays from
the acoustic propagation and the electronics. They can be
coupled with the beamforming constraints, resulting in an
adverse effect, e.g., the rank deﬁciency of G as discussed
previously. Regularization factors q and c have been added
to solve the problem (Hansen, 2010; Tikhonov and Arsenin,
1977).
As for the fourth aspect, the beamforming constraint
can be unstable due to signal mismatches and, thus, affect
the ANC performance. This is similar to designing a robust
beamformer. Constraining the WNG in the cost function can
stabilize the system. The optimal solution presented previ-
ously has been applied with the regularization factor b for
robustness (Cox et al., 1987; Vorobyov, 2013).
III. NUMERICAL SIMULATION ON AUGMENTED
REALITY (AR) GLASSES
In this section, we put the proposed algorithm in a pair
of open-ﬁtting AR glasses.
A. System setup
A six-channel system from the EasyCom dataset
(Donley et al., 2021) is shown in Fig. 3. The four micro-
phones in the frame (labeled as #1 to #4) can be used for the
reference microphones. For each ear, the corresponding bin-
aural microphone (labeled as either #5 or #6) was used as
the error microphone. The single-ear (right side) system is
considered in this article for brevity, but it can be easily
extended to a binaural case. The control performance at
microphone #6 is focused on hereinafter.
It was assumed that the desired speech was at h ¼ 0
and the noise source was at h ¼ 60. The desired signal was
a 20-s male speech (Acclivity, 2006). The noise was a
speech babble noise from the NOISEX-92 database (Varga
and Steeneken, 1993). The noise level was adjusted such
that the original clean speech was not intelligible when
mixed, i.e., the a priori SNR was 13.2 dB. The waveforms
and the spectrograms of the clean speech and the noisy
speech can be seen in Figs. 4(a) and 4(b), respectively.
These signals were inﬂuenced by the KEMAR manikin
(Burkhard and Sachs, 1975) and the glasses. The frequency
response of the acoustic secondary path was acquired from
the COMSOL Multiphysics software, where the secondary
source was simulated as a perfect point sound source and
was located at about 0.05 m above the error microphone #6
as shown in Fig. 3(a). In this article, we assumed that the
sound source was not constrained by transducer characteris-
tics (such as excursion limit and transducer resonance), and
the response of the electrical control system and the trans-
ducers could be modeled with pure delays. The sampling
rate was 48 kHz, and the ﬁlter length was L ¼ 768. The
secondary path delay had ten samples (208.3 ls), which
FIG. 3. (Color online) (a) The isometric view and (b) the top view of a KEMAR manikin with a pair of AR glasses with a six-microphone array. (c)
Microphone setup.
FIG. 4. (Color online) Waveforms and spectrograms of (a) the desired clean
speech and (b) the noisy speech at the error microphone.
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
2737
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
included both the acoustic propagation delay and the elec-
tronics delay in practice.
B. Performance metrics
To quantitatively evaluate the control performance, the
NR level of the ANC system is deﬁned as
NR ¼ 10 log10
E v2ðnÞ


E v2
ANCðnÞ


 
!
;
(15)
where the NR level should be as high as possible.
In addition, the speech distortion index (SDI) (Chen
et al., 2006) is used to monitor any potential distortion in
the residual speech component, and it is calculated as
SDI ¼ 10 log10
E
sðnÞ  esðnÞ
½
2
n
o
E s2ðnÞ


0
@
1
A;
(16)
where esðnÞ should match s(n) as much as possible, and,
thus, the SDI value should be as small as possible.
Signals esðnÞ and vANCðnÞ can be decoupled by record-
ing the history of the control ﬁlter w, which is then used to
re-ﬁlter either the desired speech signal or the noise. For
example, one can nullify the desired speech signal while
maintaining the noise to observe the NR level. Similarly,
one can observe the SDI value by nullifying the noise. This
method is only used to quantitatively evaluate the compo-
nents in the error signal in this article. In reality, the desired
signal and the noise are unknown. It is typical to estimate
them at different time intervals in speech processing and
then estimate the NR levels and the SDI values.
C. Control performance
The step-size l used in the simulation was a variable
step-size (VSS) to ensure the system with a fast convergence
speed and small misadjustment for the desired speech signal
(Aboulnasr and Mayyas, 1997). The parameters chosen for
calculating the VSS were lmax ¼ 0:0001; lmin ¼ 0:0000 08;
aVSS ¼ 0:999 98; cVSS
¼ 0:000 01, and bVSS ¼ 0:999 99.
The regularization factor c in Eq. (13) was chosen to be
0.0001. A minimum-phase high-pass ﬁlter with a cut-off fre-
quency at 140 Hz was applied as the spectral weighting ﬁlter
discussed in Eq. (14).
The waveform and the spectrogram of the residual error
signal are shown in Fig. 5(a). After ANC was enabled using
the proposed method, the noise component was considerably
attenuated within the ﬁrst 2 s, leaving only the desired
speech signal in good agreement with the original clean
speech in Fig. 4(a) overall.
The spectra of the noisy speech, the clean speech, and
the total residual error signal with ANC enabled are shown
in Fig. 5(b). Although the spectrum of the error signal fol-
lowed the majority of the clean speech, there was still some
minor residual noise below 100 Hz. As shown in Fig. 5(c),
decoupling the speech and the noise components as
described in Sec. III B conﬁrms that the system was mainly
bound by the ANC subsystem. From the last 10 s of the sig-
nals, the SNR has been improved from 13.9 to 15.2 dB in
total, which enhanced the unintelligible speech signiﬁcantly.
The NR level was 29.1 dB, and the SDI value was shown to
be 25.1 dB above 100 Hz. The SDI was low enough for the
listener not to notice any undesired distortion.
D. Spectral weighting
As discussed in Sec. II D, the performance of the spatial
constraint may be sub-optimal due to either an insufﬁcient
number of channels or limited ﬁlter lengths. Figure 6 shows
the control performance without the spectral weighting ﬁl-
ter. The error signal cannot be controlled adequately below
100 Hz. The reason can be found by performing the hybrid
ANC and the Frost algorithms separately with the same six
microphones. Although the ANC subsystem can reduce the
noise across the spectrum using the hybrid control, the spa-
tial constraint cannot be below 100 Hz due to the limited
length of the ﬁlters. Therefore, it is necessary to use the
spectral weighting method.
FIG. 5. (Color online) (a) Waveform and the spectrogram of the error signal
with ANC enabled; (b) spectra of the noisy speech, the clean speech, and
the total error signal with ANC enabled; and (c) the decoupled speech and
noise components in the error signal. The spectra are from the last 10 s
period.
2738
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
E. Robustness
This part follows the system robustness discussions in
Sec. II E. We mainly examine how sensor noise (signal mis-
matches) from the beamforming constraint affects the ANC
system and the control performance. To examine the robust-
ness of the system, sensor noise was added to some chan-
nels, e.g., microphones #1, #3, #4, and #5. It is common to
model the sensor noise as Gaussian white noise (Van Trees,
2002) with the power of r2
n. The signal-to-sensor-noise ratio
(SsNR) at microphone #5 was used to represent different
levels of sensor noise. The optimal solution in Eq. (10) was
used to calculate the ANC control ﬁlter. Here, we show the
importance of b and q for the robustness of the system.
Beamforming problems typically follow the rule of 10r2
n
to
choose
the
regularization
factor
(Li
et
al.,
2003;
Shahbazpanahi et al., 2003; Vorobyov et al., 2003). Figure 7
(blue square mark) shows the NR and SDI results of the pro-
posed ANC system using b ¼ q ¼ 10r2
n under different
SsNRs. The problem with this method is that, for example,
when the sensor noise is small, e.g., SsNR¼ 30dB, b and q are
too small to have a regularization effect. Although the noise
can be signiﬁcantly reduced (NR¼ 41.1dB), the desired speech
is also highly distorted (SDI¼ 14.0dB). On the other hand,
when the sensor noise is great, e.g., SsNR¼ 30dB, b and q
are very large and can over-regulate the system. The system
can neither control noise sufﬁciently (NR¼ 6.1dB) nor retain
the original desired speech (SDI¼ 3.1dB).
We show that b and q can be chosen depending on the
largest eigenvalue of the matrix to be inverted. Assume the
largest eigenvalues of E rðnÞrTðnÞ


and HTGU1
rr GTH are
k1
max and k2
max, respectively. Typically, the ratios between
k1
max and b and between k2
max and q depend on different sys-
tems. Here, we found that the ratio between 5000 and
50 000 had good results. The performance under this range
is shown in Fig. 7 with shaded areas, and the result with b ¼
k1
max=10 000 and q ¼ k2
max=10 000 is depicted as an example
(red diamond mark). It is obvious the system performance
has been maintained well across different levels of sensor
noise. Particularly, when the input signals have been disas-
trously perturbed, i.e., SsNR ¼ 30 dB, the system could
still exhibit good behavior. The NR level had 24.3 dB, and
the SDI was maintained at 22.5 dB. Thus, by choosing the
regularization factors based on the largest eigenvalue
instead of the sensor noise power, the proposed system can
achieve a good result even with extreme cases of sensor
noise.
F. Directivity
The direction-dependent NR performance of the dem-
onstrated AR glasses ANC system is shown in Fig. 8(a) for
different frequency bands. In this experiment, the desired
sound source is ﬁxed at the 0 angle, and a pink noise source
is placed at various angles in the horizontal plane. The opti-
mal solutions were calculated.
At the desired direction h ¼ 0, all signals were main-
tained including the noise. The NR performance was the
best at h 2 ð30; 150Þ. The noise could be reduced by at
least 20 dB. Low frequencies, e.g., below 500 Hz, had more
than 30 dB reduction. The system had an unsatisfactory per-
formance at h 2 ð150; 300Þ. This was due to the ANC
capability of the speciﬁc microphone array conﬁguration. In
these directions, the noise reached the error microphone ﬁrst
and then the reference microphones. Thus, the system cau-
sality was violated, and only the feedback subsystem was in
operation, which was only effective below 500 Hz with
about 10 dB reduction. High frequencies were slightly
increased due to the waterbed effect (Skogestad and
Postlethwaite, 2005).
One of the potential solutions is to decrease the delay in
the secondary path, which mainly depends on the electronic
components in the device. Another way is to adjust the array
conﬁguration. As shown in Fig. 8(b), eight reference micro-
phones are in a circular formation with an error microphone
at the center. Although ideal, it demonstrated that it is possi-
ble to cancel noise in every direction except for the desired
FIG. 6. (Color online) Spectra of the error signal from the proposed method,
the error signal from the spatial constraint only, and that from the ANC sys-
tem only after control without using the minimum-phase high-pass ﬁlter
with a cut-off frequency at 140 Hz.
FIG. 7. (Color online) (a) The NR level and (b) the SDI value of the error
signal with respect to different SsNRs. The blue square marks are the results
by choosing b ¼ q ¼ 10r2
n. The red diamond marks are the results by
choosing b ¼ k1
max=10 000 and q ¼ k2
max=10 000. The shaded areas repre-
sent the results with the ratio from 5000 to 50 000.
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
2739
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
direction if the causality of the ANC subsystem can be
maintained. Depending on the speciﬁc application, the array
design will change, and the directivity pattern will change
accordingly.
IV. COMPARISON WITH EXISTING METHODS
One unique feature of the proposed method is to truly
preserve the original desired physical sound rather than
reconstruct it. The results from the proposed method will be
compared with the ones from the previous works (Dalga and
Doclo, 2011; Patel et al., 2020; Serizel et al., 2010).
We would like to highlight the fact that the previous
works had been developed for different systems with differ-
ent ANC and beamforming algorithms. For ANC, Serizel
et al. (2010) and Patel et al. (2020) used the feedforward
conﬁguration, while Dalga and Doclo (2011) used the
hybrid control. For the beamforming, Serizel et al. (2010)
and Dalga and Doclo (2011) used the MWF, while Patel
et al. (2020) used the superdirective beamformer. For con-
sistency in this article, we evaluated all the methods for the
aforementioned open-ﬁtting AR glasses with the ﬁxed six-
array microphones. The monaural setup at microphone #6 is
still generally considered for simplicity of discussion. For a
fair comparison, the hybrid ANC control and the Frost
algorithm were used for all the cases. The optimal solutions
were also computed for most cases, except Sec. IV B. The
main goal for the comparison was to see how the desired
signal was obtained (e.g., reconstructed or preserved) in
these systems and its implications.
The three conﬁgurations were as follows:
(1) For Dalga and Doclo (2011) and Serizel et al. (2010),
the ANC and beamformer modules can be partially cou-
pled. Microphones #1 to #6 were used for ANC, and
two microphones (#2 and #4) were also used as the
beamforming array. The extracted signal from the beam-
former had 1 ms delay, and the gain was 0 dB as pro-
vided by Serizel et al. (2010). The extracted signal was
added to the error signal [see Fig. 5 in Serizel et al.
(2010)].
(2) For the decoupled conﬁguration by Patel et al. (2020),
microphones #1 and #3 were used as the reference
microphones for the ANC subsystem, and microphones
#2 and #4 were used as the beamforming array. The
other error microphone #5 was not available to control
#6. Note that such a decoupled conﬁguration requires
dedicated reference microphones with error micro-
phones for ANC (microphone #1 with #5 for the left
channel ANC, #3 with #6 for the right). Thus, only
microphones #2 and #4 are left for the beamformer. The
extracted signal from the beamformer had 5 ms delay.
The extracted signal was added to the secondary source
[see Fig. 3 in Patel et al. (2020)].
(3) The proposed method, as described in Sec. III.
The aforementioned three aspects—control effort of the
secondary source, control performance for multiple noise
sources, and binaural localization cues and latency of the
desired sound—are discussed below.
A. Control effort
Figure 9(a) shows the secondary source signal y(n) in
the three systems when the desired speech was at 0, the
pink noise was at 60, and the a priori SNR was 0 dB. It is
clear that the secondary source signals in the partially cou-
pled and the decoupled conﬁgurations contained the desired
speech. These systems needed to cancel both the desired
speech and noise ﬁrst and then reconstruct and reproduce
the desired speech. It is even more so for the decoupled con-
ﬁguration since the desired speech needs to be directly
injected into the secondary source signals [see Fig. 3 in
Patel et al. (2020)]. On the contrary, the one from the pro-
posed method was only for the noise, indicating it controlled
the noise only and, thus, preserving the original desired
speech.
Another method of conﬁrmation is to compare the con-
trol effort for various a priori SNRs. We used the secondary
source energy Efy2ðnÞg instead of jjwjj2
2 since the former
provides a clearer physical representation (Elliott, 2000, p.
147). The relative energy consumption E y in percentage was
calculated as
FIG. 8. (Color online) Directivity plot of the residual noise at the error
microphone #6 for a single noise source by (a) the demonstrated AR glasses
conﬁguration and (b) a system with eight reference microphones in a circu-
lar formation with an error microphone #9 at the center for the pink noise.
2740
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
E y ¼ Efy2 n
ð Þg
Efy2
ref n
ð Þg  100%;
(17)
where Efy2
refðnÞg is the mean square of the secondary source
signal in Dalga and Doclo (2011) and Serizel et al. (2010)
for a time period (e.g., 20 s) as the reference.
The energy of the secondary source and the correspond-
ing NR levels are shown in Figs. 9(b) and 9(c), respectively.
When the noise level was high, e.g., SNR ¼ 15 dB, the
energy difference was small since most energy was devoted
to controlling the noise for all cases. The NR levels were
also similar. However, as the desired speech became more
and more prominent, the difference became more and more
apparent. For example, when SNR ¼ 10 dB, the environment
is relatively quiet. The other two conﬁgurations still used a
vast amount of energy. Particularly, the decoupled conﬁgu-
ration used 50% more energy than the partially coupled due
to better control performance. (The reason for this will be
discussed in Sec. IV B.) These systems see the desired
speech as “noise” too and attempt to cancel it ﬁrst and then
try to reconstruct the desired speech once again.
On the other hand, the proposed algorithm barely needed
to change the original desired signal as illustrated in the time
domain in Fig. 9(a). It required only 2% energy while yet
achieving a better NR level than the partially coupled conﬁgu-
ration. These results further conﬁrm that the proposed system
only reduces the noise and truly preserves the desired sound.
B. Noise attenuation for multiple noise sources
The ANC performance comparison of the three conﬁgura-
tions has been partially demonstrated for a single noise in Fig.
9(c). A more practical situation is that the noises are from mul-
tiple directions. In this case, the uncorrelated pink noise was set
coming from ﬁve directions, 60; 90; 120; 300, and 330,
with the same level, while the DOA of the desired speech
remained from 0, and other conﬁgurations were kept the same.
Figure 10(a) shows the overall error signal. The proposed sys-
tem had the closest result to the desired clean speech. The noise
and the speech components in the error signal can be decoupled
for further observations.
The noise components in the error signal are shown in
Fig. 10(b). For the other two conﬁgurations, which tried to
cancel both the desired speech and noise, more microphones
(in the partially coupled conﬁguration) can lead to a worse
performance. The desired speech in the input signal can
result in a greater eigenvalue spread of the correlation
matrix of the input signal, thus, limiting the step-size and
causing a slower adaption speed (Haykin, 2002). The maxi-
mum step-size before making the system diverge for the par-
tially coupled system was 0.000 04, whereas the one for the
FIG. 9. (Color online) (a) Secondary source signals from the three conﬁgu-
rations when the a priori SNR ¼ 0 dB; (b) relative secondary source energy
consumption; and (c) the NR levels for different a priori SNRs.
FIG. 10. (Color online) Spectra of the noisy speech, the clean speech, (a) the overall error signals, (b) the noise components in the error signals, and (c) the
speech component differences compared to the clean speech in the error signals with ANC enabled in the three conﬁgurations. The spectra are from the last
10 s period. (a) Overall; (b) noise component; (c) speech component difference.
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
2741
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
decoupled was 0.000 08. Thus, conﬁguration 2 had a better
ANC performance in both Figs. 9(c) and 10(b). The pro-
posed conﬁguration did not need to cancel the speech. Thus,
it has the best NR performance.
The speech component differences compared to the origi-
nal clean speech are shown in Fig. 10(c). The other two sys-
tems used the same array for signal extraction, thus, having the
same result. The reconstructed desired speech from these sys-
tems had about 610dB difference compared to the clean
speech in general. On the other hand, the proposed system did
not have this issue since it left the original desired physical
sound unaltered. Thus, the difference above 140 Hz was essen-
tially zero. The difference below 140 Hz was due to the spec-
tral weighting ﬁlter as discussed previously. This range did not
cause any noticeable auditory distortion.
C. Binaural localization cues and latency
When the desired sound comes from directions other
than 0, binaural localization cues should be enabled for the
user. The DOA of the desired speech was moved to 60,
whereas the pink noise came from 0 instead.
Figure 11 shows the waveforms of the speech compo-
nents in the decoupled and the proposed systems compared
to the clean speech at two ears. The result in the partially
coupled system was the same as the decoupled but with
1 ms delay instead of 5 ms. The partially coupled and the
decoupled systems had the reconstructed desired signals at
microphone #4. Unless a binaural beamformer was used, the
binaural localization cues were lost. This is also shown in
Fig. 12 in the frequency domain. When the DOA of the
desired source is at 60, the spectral property of the recon-
structed desired signal at microphone #4 may be similar to
that of microphone #6 due to their close proximity, although
only between 100 Hz and 2 kHz as shown in Fig. 12(b). For
the left side, the reconstructed signal is monaural and still at
microphone #4, which is signiﬁcantly different from that of
microphone #5 across the spectrum as shown in Fig. 12(a).
On the other hand, it is apparent that the speech compo-
nent in the error signal from the proposed system agreed
with the original clean speech very well, in both time and
frequency domains. This once again conﬁrms that the pro-
posed system can preserve the natural binaural localization
cues since it left the desired physical sound unaltered.
V. REMARKS AND FUTURE DIRECTIONS
For brevity, it was assumed that there was one desired
source throughout this article. For multiple desired sources
from different directions, multiple spatial constraints can be
added to the cost function in Eq. (9), i.e., HT
s1ð~d þ GwÞ
¼ fs1; HT
s2ð~d þ GwÞ ¼ fs2; …, pointing to the directions of
the desired sources. These constraints can also be combined
into one. More information can be found in the linear con-
straint minimum variance beamforming algorithm (Van
Trees, 2002; Van Veen and Buckley, 1988).
The desired sound and the noise can be from the same
direction. This can happen when either both sources are located
in the same direction, or the noise source is in another direction
but the reverberation of the noise is mixed with the desired
source. This problem requires further investigation. Possible
solutions may be found in the ﬁeld of Blind Source Separation.
Studies such as (Mukai et al., 2006) can separate mixed signals
even when two sources come from the same direction.
The demonstrated system was a pair of open-ﬁtting AR
glasses, which allows the system to be fully coupled, that is, all
the microphones to be used for both ANC and the spatial con-
straint. Another ANC application, for example, a pair of close-
ﬁtting ANC headphones, may not be able to use error micro-
phones in the earcups for the spatial constraint since the distur-
bance signals are highly attenuated. Using all the microphones
may not provide any signiﬁcant improvements. Therefore,
using a partially coupled system can reduce computation.
The secondary sources in such a personal AR glasses
system are miniaturized speakers. The proposed system only
needs to cancel the noise, so the transducer excursion limit
can be relaxed. This is favorable in acoustic transducer
FIG. 11. (Color online) Waveforms of the clean speech at the error micro-
phone and the speech components in the error signals from the decoupled and
the proposed systems at two ears. The desired sound is at 60, and the noise
comes from 0. (a) Left ear (microphone #5); (b) right ear (microphone #6).
FIG. 12. (Color online) Spectra of the clean speech at the error microphone
and the speech components in the error signals from the decoupled and the
proposed systems at two ears. The desired sound is at 60, and the noise
comes from 0. (a) Left ear (microphone #5); (b) right ear (microphone #6).
2742
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
designs. However, the response of miniaturized speakers
can still be sub-optimal at some frequencies, which can
affect the system control performance. Therefore, the sec-
ondary path in this article was from the COMSOL simula-
tion with an ideal sound source to eliminate this factor for
the purpose of brevity. Other applications, such as ANC
headrests or ANC windows, which can also adopt the pro-
posed algorithm, may not have this issue since the loud-
speakers are not necessarily required to be miniaturized.
The acoustic feedback from the secondary sources to
reference microphones can affect the system signiﬁcantly in
practice. It should be considered in the future.
VI. CONCLUSION
In this article, we have presented a spatially selective
ANC system that truly preserves the desired sound rather
than canceling it and then reconstructing it again. The Frost
spatial constraint was imposed on the cost function of a tra-
ditional hybrid ANC system, and both the optimal and the
adaptive solutions were derived. The method was examined
in a pair of AR glasses with six microphones. Overall, the
system exhibited good performance in controlling noise
coming from undesired directions. The SNR was improved
from 13.9 to 15.2 dB while the SDI was kept at 25.1 dB.
The system could also maintain good robustness when it
was disastrously perturbed. Even when the signal mismatch
level was 30 dB higher than that of the desired signal, by
choosing the regularization factor based on the largest
eigenvalue, the noise could still be controlled by 24.3 dB,
and the SDI was maintained at 22.5 dB. However, the
directivity was bound by the causality of the ANC system,
which mainly depended on the array conﬁguration.
Compared to the state-of-the-art systems, the desired
sound in the proposed system was indeed preserved while
noise from other directions was minimized. The proposed
system used much less control effort while still achieving
the best ANC performance since it controlled only the noise
instead of noise plus speech. Furthermore, when the original
desired speech at the error microphone is preserved, there is
no need to reconstruct the natural binaural localization cues
as in other systems. Future work includes considering acous-
tic feedback control and examining the system in a non-
ideal environment, e.g., in a reverberant room.
ACKNOWLEDGMENT
The work was conducted during the ﬁrst author’s
internship
with
the
Facebook
Reality
Labs
Research,
Redmond, WA, USA. The authors wish to thank the
anonymous
reviewers
for
their
helpful
comments
and
suggestions. The authors would also like to thank Jacob
Donley and Sarmad Malik for their assistance with this project.
APPENDIX A: OPTIMAL SOLUTION DERIVATION
By taking the gradient of Eq. (9) and using the chain
rule (Petersen and Pedersen, 2012), it is found that
rwJ ¼ @J
@w ¼ @u
@w
@J
@u ¼ GT Uxxu þ Hk
ð
Þ:
(A1)
Setting the gradient of the cost function to zero, the
optimal solution can be written as
wopt ¼ ðGTUxxGÞ1GTðUxx~d þ HkÞ
¼  U1
rr /rd þ U1
rr GTHk


;
(A2)
where
rðnÞ ¼ GTxðnÞ; Urr ¼ E rðnÞrTðnÞ


and
/rd
¼ EfrðnÞdðnÞg. The Lagrangian k can be found by putting
Eq. (A2) in the spatial constraint HTðGwopt þ ~dÞ ¼ f,
k ¼ HTGU1
rr GTH

† ðHT~d  fÞ  HTGU1
rr /rd
h
i
;
(A3)
where superscript ðÞ† denotes pseudoinverse. Matrix G is
rank-deﬁcient due to the delays in the secondary paths in the
ANC system. Note that the autocorrelation matrix of the ﬁl-
tered reference signals Urr is typically full rank and, thus, is
invertible.
Using Eqs. (A2) and (A3), the optimal solution can be
found as
wopt ¼  I  U1
rr GTH HTGU1
rr GTH

†HTG
h
i
U1
rr /rd
þU1
rr GTH HTGU1
rr GTH

† f  HT~d
ð
Þ
(A4)
written in a compact form. Note that f 6¼ HT~d. Otherwise, it
would imply w ¼ 0 from the cost function in Eq. (9).
APPENDIX B: ADAPTIVE SOLUTION DERIVATION
The adaptive solution of w in the proposed method can
be found using the LMS method as
wðn þ 1Þ ¼ wðnÞ  lrwJ
¼ wðnÞ  lGT Uxxu þ Hk
ð
Þ:
(B1)
Using Eq. (3i), the constraint has
f ¼ HTuðn þ 1Þ
¼ HT Gwðn þ 1Þ þ ~d
h
i
¼ HTGwðnÞ  lHTGGT Uxxu þ HkðnÞ
½
 þ HT~d:
(B2)
Putting kðnÞ from Eq. (B2) in Eq. (B1), it becomes
wðn þ 1Þ ¼ wðnÞ  lGTUxxu
GTHðHTGGTHÞ†HTGwðnÞ
þlGTHðHTGGTHÞ†HTGGTUxxu
þGTHðHTGGTHÞ†ðf  HT~dÞ:
(B3)
Using Eq. (2) and rearranging Eq. (B3), it becomes
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
2743
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
wð0Þ ¼ q;
(B4a)
wðn þ 1Þ ¼ P wðnÞ  lGTxðnÞeðnÞ


þ q;
(B4b)
where
P ¼ I  GTHðHTGGTHÞ†HTG;
(B5a)
q ¼ GTHðHTGGTHÞ†ðf  HT~dÞ:
(B5b)
Aboulnasr, T., and Mayyas, K. (1997). “A robust variable step-size LMS-
type algorithm: Analysis and simulations,” IEEE Trans. Signal Process.
45(3), 631–639.
Acclivity (2006).
“Henry5.mp3,” https://freesound.org/people/acclivity/
sounds/24096/ (Last viewed March 18, 2021).
Burkhard, M. D., and Sachs, R. M. (1975). “Anthropometric manikin for
acoustic research,” J. Acoust. Soc. Am. 58(1), 214–222.
Cartes, D. A., Ray, L. R., and Collier, R. D. (2002). “Experimental evalua-
tion of leaky least-mean-square algorithms for active noise reduction in
communication headsets,” J. Acoust. Soc. Am. 111(4), 1758–1771.
Chang, C.-Y., Siswanto, A., Ho, C.-Y., Yeh, T.-K., Chen, Y.-R., and Kuo,
S. M. (2016). “Listening in a noisy environment: Integration of active
noise control in audio products,” IEEE Consum. Electron. Mag. 5(4),
34–43.
Cheer, J., Patel, V., and Fontana, S. (2019). “The application of a multi-
reference control strategy to noise cancelling headphones,” J. Acoust.
Soc. Am. 145(5), 3095–3103.
Chen, J., Benesty, J., Huang, Y., and Doclo, S. (2006). “New insights into
the noise reduction Wiener ﬁlter,” IEEE Trans. Audio Speech Lang.
Process. 14(4), 1218–1234.
Cox,
H.,
Zeskind,
R.,
and
Owen,
M.
(1987).
“Robust
adaptive
beamforming,” IEEE Trans. Acoust. Speech Signal Process. 35(10),
1365–1376.
Dalga, D., and Doclo, S. (2011). “Combined feedforward-feedback noise
reduction schemes for open-ﬁtting hearing aids,” in Proceedings of the
2011 IEEE Workshop on Applications of Signal Processing to Audio and
Acoustics (WASPAA), October 16–19, New Paltz, NY, pp. 185–188.
Doclo, S., Kellermann, W., Makino, S., and Nordholm, S. E. (2015).
“Multichannel signal enhancement algorithms for assisted listening devi-
ces: Exploiting spatial diversity using multiple microphones,” IEEE
Signal Process. Mag. 32(2), 18–30.
Donley, J., Tourbabin, V., Lee, J.-S., Broyles, M., Jiang, H., Shen, J.,
Pantic, M., Ithapu, V. K., and Mehra, R. (2021). “Easycom: An aug-
mented reality dataset to support algorithms for easy communication in
noisy environments,” arXiv:2107.04174.
Elliott, S. J. (2000). Signal Processing for Active Control (Academic Press,
San Diego, CA), p. 511.
Elliott, S. J., Boucher, C. C., and Nelson, P. A. (1992). “The behavior of a
multiple channel active control system,” IEEE Trans. Signal Process.
40(5), 1041–1052.
Elliott, S. J., Jung, W., and Cheer, J. (2018). “Head tracking extends local
active control of broadband sound to higher frequencies,” Sci. Rep. 8(1),
5403.
Frost, O. L. (1972). “An algorithm for linearly constrained adaptive array
processing,” Proc. IEEE 60(8), 926–935.
Gannot, S., Vincent, E., Markovich-Golan, S., and Ozerov, A. (2017). “A
consolidated perspective on multimicrophone speech enhancement and
source separation,” IEEE/ACM Trans. Audio Speech Lang. Process.
25(4), 692–730.
Hansen, C., Snyder, S., Qiu, X., Brooks, L., and Moreau, D. (2012). Active
Control of Noise and Vibration, 2nd ed. (CRC Press, Boca Raton, FL), p.
1554.
Hansen, P. C. (2010). Discrete Inverse Problems: Insight and Algorithms
(Society for Industrial and Applied Mathematics, Philadelphia, PA).
Haykin, S. (2002). Adaptive Filter Theory, 4th ed. (Prentice Hall, Upper
Saddle River, NJ).
Kuo, S. M., and Morgan, D. R. (1996). Active Noise Control Systems:
Algorithms and DSP Implementations (Wiley, New York), p. 389.
Lam, B., Shi, D., Gan, W.-S., Elliott, S. J., and Nishimura, M. (2020).
“Active control of broadband sound through the open aperture of a full-
sized domestic window,” Sci. Rep. 10(1), 10021.
Li, J., Stoica, P., and Wang, Z. (2003). “On robust capon beamforming and
diagonal loading,” IEEE Trans. Signal Process. 51(7), 1702–1715.
Liebich, S., Richter, J.-G., Fabry, J., Durand, C., Fels, J., and Jax, P. (2018).
“Direction-of-arrival dependency of active noise cancellation head-
phones,” in Proceedings of the ASME 2018 Noise Control and Acoustics
Division Session Presented at INTERNOISE 2018, August 26–29,
Chicago, IL.
Mukai, R., Sawada, H., Araki, S., and Makino, S. (2006). “Frequency-
domain blind source separation of many speech signals using near-ﬁeld
and far-ﬁeld models,” EURASIP J. Adv. Signal Process. 2006, 083683.
Patel, V., Cheer, J., and Fontana, S. (2020). “Design and implementation of
an active noise control headphone with directional hear-through capa-
bility,” IEEE Trans. Consum. Electron. 66(1), 32–40.
Petersen, K. B., and Pedersen, M. S. (2012). “The matrix cookbook,” ver-
sion 20121115, http://www2.compute.dtu.dk/pubdb/pubs/3274-full.html
(Last viewed August 22, 2022).
Rafaely, B., and Jones, M. (2002). “Combined feedback–feedforward active
noise-reducing headset–the effect of the acoustics on broadband perform-
ance,” J. Acoust. Soc. Am. 112(3), 981–989.
Serizel, R., Moonen, M., Wouters, J., and Jensen, S. H. (2010). “Integrated
active noise control and noise reduction in hearing aids,” IEEE Trans.
Audio Speech Lang. Process. 18(6), 1137–1146.
Shahbazpanahi, S., Gershman, A. B., Luo, Z.-Q., and Wong, K. M. (2003).
“Robust adaptive beamforming for general-rank signal models,” IEEE
Trans. Signal Process. 51(9), 2257–2269.
Shen, X., Shi, D., and Gan, W.-S. (2021). “A wireless reference active noise
control headphone using coherence based selection technique,” in
Proceedings of ICASSP 2021—2021 IEEE International Conference on
Acoustics, Speech and Signal Processing (ICASSP), June 6–11, Toronto,
Canada, pp. 7983–7987.
Shi, D., Gan, W.-S., Lam, B., and Wen, S. (2020). “Feedforward selective
ﬁxed-ﬁlter active noise control: Algorithm and implementation,” IEEE/
ACM Trans. Audio Speech Lang. Process. 28, 1479–1492.
Shi, D., Lam, B., Ooi, K., Shen, X., and Gan, W.-S. (2022). “Selective
ﬁxed-ﬁlter active noise control based on convolutional neural network,”
Signal Process. 190, 108317.
Skogestad, S., and Postlethwaite, I. (2005). Multivariable Feedback
Control: Analysis and Design (Wiley, New York).
Tikhonov, A. N., and Arsenin, V. Y. (1977). Solutions of Ill-Posed
Problems (V. H. Winston, New York), p. 30.
Tobias, O. J., and Seara, R. (2004). “Leaky delayed LMS algorithm:
Stochastic analysis for Gaussian data and delay modeling error,” IEEE
Trans. Signal Process. 52(6), 1596–1606.
Van Trees, H. L. (2002). Optimum Array Processing (Wiley, New York).
Van Veen, B., and Buckley, K. (1988). “Beamforming: A versatile
approach to spatial ﬁltering,” IEEE ASSP Mag. 5(2), 4–24.
Varga, A., and Steeneken, H. J. (1993). “Assessment for automatic speech
recognition: II. NOISEX-92: A database and an experiment to study the
effect of additive noise on speech recognition systems,” Speech Commun.
12(3), 247–251.
Vorobyov, S. A. (2013). “Principles of minimum variance robust adaptive
beamforming design,” Signal Process. 93(12), 3264–3277.
Vorobyov, S. A., Gershman, A. B., and Luo, Z.-Q. (2003). “Robust adaptive
beamforming using worst-case performance optimization: A solution to the
signal mismatch problem,” IEEE Trans. Signal Process. 51(2), 313–324.
Wang, S., Tao, J., and Qiu, X. (2017). “Controlling sound radiation through
an opening with secondary loudspeakers along its boundaries,” Sci. Rep.
7(1), 13385.
Xiao, T., Qiu, X., and Halkon, B. (2020). “Ultra-broadband local active
noise control with remote acoustic sensing,” Sci. Rep. 10(1), 20784.
Xu, B., and Miller, T. (2019). “Selective active noise cancellation based
on directional reference signals,” J. Acoust. Soc. Am. 146(4), 2794.
Zhang, H., and Wang, D. (2021). “Deep ANC: A deep learning approach to
active noise control,” Neural Netw. 141, 1–10.
Zhang, L., and Qiu, X. (2014). “Causality study on a feedforward active
noise control headset with different noise coming directions in free ﬁeld,”
Appl. Acoust. 80, 36–44.
2744
J. Acoust. Soc. Am. 153 (5), May 2023
Xiao et al.
https://doi.org/10.1121/10.0019336
 08 September 2026 00:09:31
