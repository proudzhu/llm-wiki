

===== [page 1] =====

IEEE TRANSACTIONS ON AUDIO, SPEECH, AND LANGUAGE PROCESSING, VOL. 18, NO. 6, AUGUST 2010
1137
Integrated Active Noise Control and
Noise Reduction in Hearing Aids
Romain Serizel, Marc Moonen, Fellow, IEEE, Jan Wouters, and Søren Holdt Jensen, Senior Member, IEEE
Abstract—This paper presents combined active noise control
and noise reduction schemes for hearing aids to tackle secondary
path effects and effects of noise leakage through an open ﬁtting.
While such leakage contributions and the secondary acoustic
path from the loudspeaker to the tympanic membrane are usually
not taken into account in standard noise reduction systems, they
appear to have a non-negligible impact on the ﬁnal signal-to-noise
ratio. Using a noise-reduction algorithm and an active noise
control system in cascade may be efﬁcient as long as the causality
margin of the system is large enough. Putting the two functional
blocks in parallel and then integrating them is found to lead
to a more robust algorithm. A Filtered-x Multichannel Wiener
Filter is presented and applied to integrate noise reduction and
active noise control. The cascaded scheme and the integrated
scheme are compared experimentally with a Multichannel Wiener
Filter in a classic noise reduction framework without active noise
control, where the integrated scheme is found to provide the best
performance.
Index Terms—Active noise control (ANC), hearing aids, multi-
channel Wiener ﬁlter, noise reduction (NR).
I. INTRODUCTION
T
HE usage of hearing aids with an open ﬁtting has become
more common over the past years mainly owing to the
availability of more efﬁcient feedback control schemes and fast
signal processing units. Whereas removing the earmold reduces
the occlusion effect and improves the physical comfort [1], one
major drawback is that the noise leakage through the ﬁtting
cannot be neglected anymore. Conventional noise reduction
(NR) systems such as the Generalized Sidelobe Canceller
(GSC) [2] or techniques based on the Multichannel Wiener
Filter (MWF) [3] do not take this contribution into account.
Combined with the attenuation in the acoustic path between
the sound source (hearing aid loudspeaker) and the tympanic
Manuscript received March 30, 2009; revised July 29, 2009. First published
September 25, 2009; current version published July 14, 2010. This work was
carried out at the ESAT Laboratory of Katholieke Universiteit Leuven, in the
frame of the Marie-Curie Fellowship EST-SIGNAL Program (http://est-signal.
i3s.unice.fr) under Contract MEST-CT-2005-021175, and the Concerted Re-
search Action GOA-AMBioRICS. The scientiﬁc responsibility is assumed by
the authors. The associate editor coordinating the review of this manuscript and
approving it for publication was Prof. Michael L. Seltzer.
R. Serizel and M. Moonen are with the Department of Electrical Engineering,
Katholieke Universiteit Leuven, ESAT-SCD, B-3001 Leuven, Belgium.
J. Wouters is with the Division of Experimental Otorhinolaryngology,
Katholieke Universiteit Leuven, ExpORL, B-3000 Leuven, Belgium.
S. H. Jensen is with the Department of Electronic Systems, Aalborg Univer-
sity, DK-9220 Aalborg, Denmark.
Color versions of one or more of the ﬁgures in this paper are available online
at http://ieeexplore.ieee.org.
Digital Object Identiﬁer 10.1109/TASL.2009.2030948
membrane (the so-called secondary path), the noise leaking
through the ﬁtting can override the action of the processing
done in the hearing aid.
One efﬁcient way to cancel this undesired noise leakage is to
use active noise control (ANC) [4], [5]. The principle of ANC
is to generate a zone of quiet, in this case at the tympanic mem-
brane, canceling the effect of noise leakage. To acheive feed-
forward ANC at the tympanic membrane, it is assumed that, in
all the subsequent systems, a microphone is present in the ear
canal to provide an error signal. In the hearing aids framework,
ANC then has to be performed together with a NR algorithm.
There are different ways of combining ANC and NR. Here, the
cascading of both functional blocks will be considered ﬁrst and
then the integration of ANC and NR into one ﬁlter set will be
described, based on an initial parallel combination of the func-
tional blocks and a Filtered-x version of the MWF algorithm
(FxMWF) [6].
In a cascaded implementation of the standard NR scheme
with a single-channel ANC algorithm, the output of the NR,
which is supposed to have a low power noise component, is
used as the input of the ANC to produce the so-called anti-noise.
The two functional blocks have opposite targets. Therefore cas-
cading NR and single-channel ANC is found to be inefﬁcient.
Using a multichannel ANC instead of a single-channel
ANC allows to have input signals with higher power noise
components which improve the performance. However, the
delay needed to achieve a high NR performance is still added to
the system latency. In ANC algorithms, this delay is a critical
parameter and can reduce drastically the noise cancellation ca-
pabilities [4]. Therefore, ANC used in cascade with a standard
NR scheme can only compensate for noise leakage as long as
causality margins are sufﬁcient to include the NR delay and still
allow the ANC processing to be causal. When the NR delay
grows, the ANC beneﬁts decrease and vanish quickly.
In an integrated use of ANC and NR based on FxMWF, the
delay from the NR algorithm does not interfere with the leakage
cancellation part. The system is more robust to latency and can
almost provide a constant signal-to-noise ratio (SNR) at the
tympanic membrane up to the causality bound. Also, the use of
a ﬁltered-x algorithm [7]–[9] in the integrated approach allows
to include the secondary path effect in the NR computation. The
error signal that has to be minimized is the difference between
the desired signal and the signal reaching the tympanic mem-
brane rather than the signal fed into the loudspeaker. Therefore,
even with higher system latencies, integrating ANC and NR can
lead to performance improvements compared to a classic NR
scheme where the noise leakage and the secondary path effect
are not taken into account.
1558-7916/$26.00 © 2010 IEEE


===== [page 2] =====

1138
IEEE TRANSACTIONS ON AUDIO, SPEECH, AND LANGUAGE PROCESSING, VOL. 18, NO. 6, AUGUST 2010
Fig. 1. Multichannel noise reduction system in the hearing aids context.
This paper will present a performance comparison between a
standard MWF-based NR without ANC, a cascaded version of
NR and ANC, and an integrated ANC and NR using FxMWF;
all applied in hearing aids with an open ﬁtting. The effects of the
noise leakage and the secondary path on the output of MWF-
based NR are commented on in Section II. Section III intro-
duces different schemes combining ANC and NR. The causality
problem is described in Section IV. The experimental results are
presented in Section V, and ﬁnally Section VI presents the con-
clusions of this paper.
II. PROBLEM STATEMENT
Speech enhancement in hearing aids is based on standard
NR techniques ignoring the possible effects of noise leakage
through the ﬁtting and the secondary path between the loud-
speaker and the tympanic membrane. This section describes an
NR algorithm based on MWF [3] and how the noise leaking
through the ﬁtting and the attenuation in the secondary path can
affect its performance.
A. Signal Model and Multichannel Wiener Filter Basics
Let
be the ﬁlter length and
the number of microphones
(channels). The signal
for microphone
has a desired
speech part
and an additive noise part
, i.e.,
(1)
where
is the time index.
In the sequel, superscripts
and
will also be used for other
signals and vectors, to denote their speech and noise component,
respectively. Signal model (1) holds for so-called “speech plus
noise periods.” There are also “noise-only periods” (i.e., speech
pauses), during which only a noise component is observed.
The column vector
contains the
last samples of the
channel
(2)
The compound vector gathering all channels is
(3)
In the NR context (Fig. 1), the output of the system is
(4)
with
the optimal Wiener ﬁlter
which minimizes the mean squared error (MSE)
(5)
and which is given by
(6)
Here,
is the correlation matrix of the input
and
is the cross-correlation vector between the input
and the desired signal
, which is chosen to be equal to
the (unknown) speech component in the ﬁrst microphone, up to
a delay
(7)
(8)
(9)
Note that by assuming that the speech and noise components
of the input signals are uncorrelated, the cross-correlation vector
can be estimated using
(10)
(11)
(12)
While
and
are
estimated
during
the
speech-plus-noise periods,
can be estimated during
the noise-only periods.
B. Multichannel Wiener Filter-Based Noise Reduction With
Leakage and Secondary Path Effects
The NR scheme based on MWF, as applied in the hearing aids
context, is presented in Fig. 1. The gain
is the ampliﬁcation
that compensates for the hearing losses. It is considered here to
be a broadband gain.
Classic NR schemes ignore the so-called secondary path, i.e.,
the propagation from the loudspeaker to the tympanic mem-
brane (including the loudspeaker response itself). Assuming that
the loudspeaker characteristic is approximately linear, the sec-
ondary path can be represented by the transfer function
.
As explained in [6], the dc gain of
is lower than 1, so the
power of the output is decreased when taking the secondary path
into account.
The hearing aid with an open ﬁtting has no earmold to prevent
ambient sound from leaking into the ear canal, which results in
additional leakage signal
reaching the tympanic membrane
[10]. No direct processing can be done on this signal; therefore,
its SNR is generally lower than for the signal provided by the
hearing aid.
Taking both, the leakage signal and the secondary path effect
into account, leads to the following output signal model
(13)


===== [page 3] =====

SERIZEL et al.: INTEGRATED ACTIVE NOISE CONTROL AND NOISE REDUCTION IN HEARING AIDS
1139
Fig. 2. Multichannel noise reduction and single-channel active noise control systems in cascade.
It clearly appears that, for small ampliﬁcation gains
, the at-
tenuation caused by the secondary path and the additive leakage
contribution do matter. The leakage SNR may affect the output
SNR thus partly canceling the improvement achieved with the
NR in the hearing aid. In conclusion, whereas the secondary
path and the leakage are not taken into account in convetional
NR algorithms, they may degrade their performance signiﬁ-
cantly (see also Section V for an evaluation of the system shown
on Fig. 1).
III. COMBINED NOISE REDUCTION AND
ACTIVE NOISE CONTROL
The leakage signal is not processed in the hearing aid there-
fore it is not possible to improve its SNR using standard NR al-
gorithms. It is possible however to attenuate the leakage signal’s
noise component using ANC. In all the subsequent systems, it is
assumed that a microphone is present in the ear canal to provide
an error signal. Commercial hearing aids currently do not have
an ear canal microphone, but it is technically possible to include
a microphone on the eartip. This section describes different ap-
proaches to combine the NR scheme (as presented in Section II)
and the ANC algorithm. Two of these schemes (shaded Figs. 3
and 5) will then be used for further evaluation in the next sec-
tions (and compared against the scheme shown Fig. 1).
A. Noise Reduction and Single-Channel Active Noise Control
in Cascade
A straightforward way to combine ANC and NR is to cascade
both functional blocks, using the output of the noise canceller
as the input to the ANC system (Fig. 2).
In an ANC system, the controller output is designed to cancel
a noise signal and generate a zone of quiet based on destructive
interference. In a hearing aid, the noise is to be canceled at the
tympanic membrane and, as in any ANC system, the secondary
path plays an important part in the algorithm. Introducing this
extra path may lead to instabilities. Therefore, it is necessary
to use so-called ﬁltered-x algorithms [4], [7]–[9] based on an
estimate of the secondary path:
(14)
(15)
and the ﬁltered reference signal
(16)
where
.
The secondary path can be estimated ofﬂine using classic
identiﬁcation methods based for example on Least Mean Square
(LMS) algorithms, or online by adding random noise to the
signal exciting the secondary path, as introduced by Eriksson
et al. in [11] and later reﬁned by Kuo et al. [12] and Zhang et
al. [13].
The ANC output signal is
, where the ﬁlter
is
designed to minimize the MSE
(17)
Here,
is an error signal, constructed from the ear canal
microphone signal
, as will be described next.
The lower branch with
in Fig. 2 (and also in subsequent
ﬁgures), represents the adaptation (gradient estimation) of
a standard ﬁltered-x adaptive ﬁlter algorithm.
The goal here is to cancel the noise component of the leakage
signal while preserving the speech signal estimate provided by
the NR. In the hearing aids context, the speech component of
the leakage signal can provide cues which, e.g., are helpful to
localize the speaker. Therefore, it was chosen here to cancel
only the noise component of the leakage signal and preserve the
speech component. All the schemes presented here, however,
can straightforwardly be modiﬁed for the case where the full
leakage signal is to be canceled. Cancelling only the noise com-
ponent of the leakage signal effectively corresponds to removing
the unknown speech component of the leakage
from the
ANC error signal
as indicated in Fig. 2. Note however
that, as
is unknown, this subtraction is not done explicitly.
The noise component of the leakage
can be canceled by
adapting the ﬁlter
in noise only periods. During speech plus
noise periods, the remaining leakage signal could then be con-
sidered as an estimate of the speech component of the leakage:
(18)
The ANC itself would also tend to remove the desired speech
component (NR output signal
) so this signal, multiplied
by the ampliﬁcation gain
, has to be added back to the ANC
output signal (loudspeaker input signal) and then the same


===== [page 4] =====

1140
IEEE TRANSACTIONS ON AUDIO, SPEECH, AND LANGUAGE PROCESSING, VOL. 18, NO. 6, AUGUST 2010
Fig. 3. Multichannel noise reduction and active noise control systems in cascade.
signal ﬁltered by the estimated secondary path
(corre-
sponding to an estimate of the NR output as delivered at the
tympanic membrane) is subtracted from the ANC error signal
, as explained in [14] and [15], leading to:
(19)
Assuming that the secondary path identiﬁcation error is small
(
), the upper branches with
and
do not con-
tribute to
. Furthermore, by also assuming that the ﬁlter
is adapting slowly, the error reduces to:
(20)
where
.
The output of the combined system (at the tympanic mem-
brane) is given by
(21)
(22)
This is the sum of the minimized error signal, the enhanced
speech signal as delivered at the tympanic membrane and the
speech component of the leakage signal.
Assuming that the speech and the noise components in (20)
are uncorrelated, the MSE criterion (17) can be rewritten as fol-
lows:
(23)
A simple ANC scheme is then obtained when the MSE crite-
rion is modiﬁed to:
(24)
resulting in a standard ﬁltered-x adaptive ﬁltering operated in
noise only periods.
In the case of a perfect NR the noise component of the input
signal of the ANC is zero. This is problematic as the feedforward
ANC is designed to produce so-called anti-noise based on the
noise component of its input. In practice, the NR is never perfect
and so the noise component of its output, i.e., the input of the
ANC, is nonzero and can be used in the ANC to produce the
anti-noise. Still, this noise component may be small and then
the ANC may exhibit a poor performance.
B. Noise Reduction and Multichannel Active Noise Control
in Cascade
The NR output signal
is the sum of ﬁltered microphone
signals. These ﬁltered microphone signals themselves gener-
ally have a signiﬁcant noise component, typically larger than
the noise component in the sum signal. These signals therefore
provide more suitable input signals for the ANC than the NR
output
itself. A cascaded scheme with a multichannel ANC
can then be derived from the initial cascade of MWF-based NR
and single channel ANC as indicated in Fig. 3, which will ex-
hibit improved performance.
The NR algorithm is the same as described in Section II. The
multichannel input of the ANC is the output of the NR before
the summation. Let
denote the
th ﬁltered microphone
signal
(25)
Let
denote the column vector containing the last
sam-
ples of
(
being the length of the ANC ﬁlter) and let
denote the compound vector gathering all the channels
(26)
The ﬁltered reference signals in the ANC are deﬁned as
(27)
Let
denote the column vector containing the last
sam-
ples of
and let
denote the compound vector gathering
all the channels:
(28)
The ANC output signal is equal to
, where
is a multichannel adaptive ﬁlter of length
,
which minimizes the MSE
(29)


===== [page 5] =====

SERIZEL et al.: INTEGRATED ACTIVE NOISE CONTROL AND NOISE REDUCTION IN HEARING AIDS
1141
Assuming that the secondary path identiﬁcation error is small
(
) and that the ﬁlter
is adapting slowly, the error
signal reduces to
(30)
The output of the combined system (at the tympanic membrane)
is given by
(31)
(32)
This is the sum of the minimized error signal, the enhanced
speech signal as delivered at the tympanic membrane and the
speech component of the leakage signal. Cascading a standard
NR scheme and the ANC algorithm thus allows to improve the
SNR of the signal, while reducing the impact of noise leakage
on the ﬁnal output.
Assuming that the speech and the noise components in (30)
are uncorrelated, the MSE criterion (29) can be rewritten as fol-
lows:
(33)
A simple ANC scheme is then again obtained when the MSE
criterion is modiﬁed to
(34)
resulting in a standard ﬁltered-x adaptive ﬁltering operated in
noise only periods. One consequence of such adaptation during
noise only periods is that the effect of the ﬁlter
on the speech
component of the signal is unknown and cannot be controlled.
Also, as long as
in the upper branch (Fig. 3), the ﬁlter
does not compensate for the secondary path effects.
An attempt to compensate for this extra path can be to replace
in the upper branch (Fig. 3) by
, which is the identity
ﬁlter of length
such that, for any signal
,
.
The MSE criterion (29) is then modiﬁed into
(35)
Introducing
as the compound vector gathering all the
such that
(36)
(37)
the ANC error signal can be written as follows:
(38)
where
is the optimization vector.
Assuming that the secondary path identiﬁcation error is small
(
) and that the ﬁlter
is adapting slowly, the error
reduces to
(39)
Assuming that the speech and noise components in (35) are
uncorrelated, the MSE criterion (35) can be written as
(40)
Here, the coefﬁcients of the ﬁlter have to be updated during
both noise only periods and speech plus noise periods. This
makes the use of standard ANC algorithms based on gradient
estimation inconvenient. Therefore, here and in the subsequent
schemes, the adaptive ﬁlters are computed based on the estima-
tion of second order statistics of the speech signals and the noise
signals, as in the MWF approach of Section II.
From (40), it can be seen that the desired signal to be used
here is
(41)
The optimal ﬁlter
is then given by
(42)
Here,
is the correlation matrix of the ﬁltered reference
signal
and
is the cross-correlation vector be-
tween the ﬁltered reference signal
and the target signal
(43)
(44)
Note that by assuming that the speech and noise components
of the input signals are uncorrelated the cross-correlation vector
can be estimated using
(45)
(46)
(47)
with
(48)
(49)
(50)
While
and
are estimated during speech plus noise
periods,
and
can be estimated during noise
only periods, where based on (39)
(51)
(52)
The ﬁrst term on the right-hand side in (40) corresponds to the
difference between the ampliﬁed desired speech signal and the
speech component of the signal reaching the tympanic mem-
brane, where the secondary path effect has been canceled ef-
fectively. The second term is the difference between the noise
component in the ampliﬁed
and the noise component of


===== [page 6] =====

1142
IEEE TRANSACTIONS ON AUDIO, SPEECH, AND LANGUAGE PROCESSING, VOL. 18, NO. 6, AUGUST 2010
Fig. 4. Active noise control and noise reduction system in parallel.
the signal (loudspeaker + leakage) reaching the tympanic mem-
brane. Therefore, minimizing (40) corresponds to compensating
for the secondary path effect on the reference signal while can-
celing the effect of the noise leakage. The output signal (at the
tympanic membrane) is
(53)
which is the sum of the minimized error, the enhanced speech
signal as delivered at the tympanic membrane and the speech
component of the leakage signal.
In the cascaded implementation, the input of the ANC is
related to the output of the NR which is then also the reference
signal for the secondary path cancellation (upper branch on
Fig. 3). This is problematic, the ANC needs an input with a
strong noise component, while the secondary path cancellation
ideally has to be applied to the desired speech signal. To
design a performant algorithm for ANC and secondary path
cancellation, the input signal of the ANC and the secondary
path cancellation reference signal have to be different signals.
Therefore, cascading does not seem to be the most efﬁcient
approach (see also Section V for an evaluation of the system in
Fig. 3).
C. Noise Reduction and Multichannel Active Noise Control
in Parallel
As an alternative to cascading the NR with the ANC, the two
functional blocks can also be put in parallel (Fig. 4). Here,
is an MWF applied in the context of NR and
is a multi-
channel ANC ﬁlter, also compensating for the secondary path
effects.
Assuming that the speech and noise components are uncorre-
lated, the MSE to be minimized by
is
(54)
The ﬁlter
thus minimizes the noise sound pressure at the
tympanic membrane as well as the inﬂuence of the secondary
Fig. 5. Integrated multichannel active noise control and noise reduction system.
path on the output signal. The output of the system is the sum of
this minimized error, the ampliﬁed enhanced speech signal and
the speech component of the leakage signal:
(55)
The parallel system is thus combining the NR, the ANC and
the compensation of the secondary path effect. In this approach
the reference signal for the secondary path compensation is an
estimate of the speech signal (
) ampliﬁed by
. To further simplify the system, this signal can implicitly be
replaced by the desired signal of the NR (
). This is pur-
sued in the next section.
D. Integrated Active Noise Control and Noise Reduction
This section introduces an algorithm integrating both the NR
and the ANC in a single set of adaptive ﬁlters (Fig. 5).
The algorithm relies on a ﬁltered-x version of the MWF
(FxMWF) based on an estimate of the secondary path
.
The ﬁltered reference signals are now
(56)
(57)
(58)
The aim of the integrated scheme is to improve the speech-to-
noise ratio, and so the desired signal (at the tympanic mem-
brane) to be used is
(59)
The MSE criterion to be minimized is then
(60)
Assuming that the secondary path identiﬁcation error is small
(
) and that the ﬁlter
is adapting slowly, the error
signal can be rewritten as follows:
(61)


===== [page 7] =====

SERIZEL et al.: INTEGRATED ACTIVE NOISE CONTROL AND NOISE REDUCTION IN HEARING AIDS
1143
Fig. 6. Delays in hearing aid system environment.
Assuming that, the noise and speech components in (61) are
uncorrelated, the criterion (60) can be rewritten as follows:
(62)
The ﬁrst term of the right-hand side corresponds to the
secondary path compensation on the speech component of the
output signal while the second term speciﬁes the noise sound
pressure at the tympanic membrane and thus corresponds to
the ANC. The ﬁlter described in (63) is thus performing a NR,
which takes the secondary path into account, combined with a
ANC.
The optimal ﬁlter (FxMWF) minimizing (62) is
(63)
Here,
is the correlation matrix of the ﬁltered reference
signal
and
is the cross-correlation vector between
the ﬁltered reference signal
and the desired signal
(64)
(65)
Note that by assuming that the speech and noise components
of the input signals are uncorrelated the cross-correlation vector
can be estimated using
(66)
(67)
with
(68)
(69)
(70)
While
and
are estimated during speech plus
noise periods,
and
can be estimated during
noise only periods with
(71)
IV. ROBUSTNESS TO CAUSALITY
As explained in [4], the main condition to get the (feedfor-
ward) ANC system working is that a causality criterion is sat-
isﬁed. That is (Fig. 6) the acoustic delay from the noise source
to the ear canal microphone
is longer than: the sum of the
delay from the source to one of the reference microphones
,
the delay associated with the processing within the hearing aid
, the algorithmic delay
and the acoustic delay of the
secondary path
.
The bandwidth on which it is possible to achieve good ANC
performance reduces with the “degree of causality” (i.e., the
delay margin speciﬁed in (73)). When (72) is not satisﬁed, the
ANC efﬁciency vanishes quickly [16]. Delay is thus a critical
problem in ANC and many approaches have been developed to
try to deal with it [17], [18]
(72)
(73)
In case of hearing aids, the delay available for processing is
linked to the distance between the microphones and the loud-
speaker which is not more than a few centimeters. This corre-
sponds to a few tens of microseconds, i.e., only a few samples
for standard sampling frequencies.
A. Noise Reduction and Active Noise Control in Cascade
In the cascaded schemes presented in Sections III-A and
III-B, the input of the ANC is the output of a standard multi-
channel NR, which itself introduces a delay
(Fig. 1).
Usually, this delay is set to half of the NR ﬁlter length (
)
and will already exceed the few taps available for processing.
Therefore, the causality criterion speciﬁed in (72) cannot be
fullﬁlled and so the ANC may not be able to yield good perfor-
mance. Reducing the NR delay increases the causality of the
system, but this also has an impact on the NR performance.
Cascading NR and ANC therefore requires a tradeoff be-
tween the performance of the two functional blocks. Besides,
knowing that the ANC’s performance quickly decreases as the
non-causality increases, the NR delay
has to be decreased
drastically in order to improve the ANC efﬁciency. In realistic
scenarios, ﬁnding a satisfying tradeoff may be impossible,
which may make the ANC useless.
B. Integrated Noise Reduction and Active Noise Control
In the integrated approach (Section III-D), the ﬁlter mini-
mizing the MSE (62) can be split into a sum of two ﬁlters
(74)
where
(75)
(76)
The ﬁlter
describes a NR which also compensates for
the secondary path effects while the ﬁlter
is an ANC
system canceling the noise leakage. So, under the assumption
that speech and noise components are uncorrelated, the set of
ﬁlters integrating NR and ANC can be seen as the sum of two
sets of ﬁlters, one for NR and the other for the ANC. Therefore,
the output of the ANC does not depend on the delay introduced
in the NR part (i.e.,
) and so it is possible to design a
causal active noise controller to be integrated with the NR as
long as
(77)
That is, there is no performance tradeoff to be done between the
NR and the ANC.


===== [page 8] =====

1144
IEEE TRANSACTIONS ON AUDIO, SPEECH, AND LANGUAGE PROCESSING, VOL. 18, NO. 6, AUGUST 2010
V. EXPERIMENTAL RESULTS
The algorithms introduced in Section II (Fig. 1) and
Section III-B (Fig. 3) and Section III-D (Fig. 5) have been
tested experimentally and their performance has been com-
pared.
A. Experimental Setup
The simulations were run on acoustic path measurements
with a manikin head and torso equipped with artiﬁcial ears
and a two-microphone behind-the-ear (BTE) hearing aid. The
speech source was located at 0 and a noise source at 270 . The
BTE was worn on left ear, facing the noise source. Commercial
hearing aids currently do not have an ear canal microphone,
therefore the artiﬁcial ear eardrum microphone is used here
to generate the error signal. The tests were run on 22-s-long
signals. The speech was composed of three sentences from the
HINT database [19] concatenated with silence periods. The
noise was the multitalker babble from Auditec [20]. All the
signals were sampled at 16 kHz.
The (BTE microphone) input SNR is often used as a reference
measure in standard NR schemes. In our case, as two algorithms
also perfom ANC, the leakage SNR, which can also be consid-
ered as the SNR when the hearing aid is turned off, is taken
as a reference. The intelligibility-weighted signal-to-noise ratio
(SNR) improvement [21] is used here as a performance mea-
sure, which is deﬁned as
SNR
SNR
SNR
(78)
where
is the band importance function deﬁned in [22] and
and
represent the output SNR and the
leakage SNR (in dB) of the th band, respectively.
The ﬁlter lengths are set to
and
, and the
NR delay is set to half of the NR ﬁlter length (
). The
secondary path
is estimated ofﬂine using an identiﬁcation
technique based on the Normalized Least Mean Square (NLMS)
algorithm. The length of the estimated path
is set to
.
The ﬁrst experiment shows the effect of leakage on the NR
performance and the improvement achieved by ANC. For an
ampliﬁcation gain
varying from 0 dB to 20 dB the inputs are
ﬁltered using the three algorithms previously described and the
SNR
is evaluated. The system is calibrated so that for
dB, for a source at 0 , the leakage and the signal fed in
the loudspeaker have equal power.
The second test aimed to demonstrate the impact of delay
on the ANC performance with the different algorithms. With
a ﬁxed ampliﬁcation gain
, for a varying degree of causality
(73), the system performances are compared.
B. Leakage and Secondary Path Effects, Improvements With
Active Noise Control
To evaluate the effect of the leakage and the secondary path,
the input signals are ﬁrst ﬁltered by an MWF-based NR scheme
(Fig. 1). Depending on which disturbance is being tested, the
signal produced can then be ﬁltered by the secondary path model
and/or the leakage can be added, as described in Section II.
Fig. 7. Performance comparison for a Multichannel Wiener Filer noise reduc-
tion scheme depending on leakage and secondary path.
Fig. 8. Performance comparison for noise reduction scheme with or without
active noise control,  = 48.
The reference SNR (leakage signal), is equal to
1.3 dB. This
value depends on the noise and speech angles as well as the input
SNR (source signals), which is 5 dB here.
When the leakage is the only disturbance considered, the
degradations induced by the leakage remain small even for
reasonably low gain
[down to 10 dB (Fig. 7)]. However,
introducing both the leakage and the secondary path the degra-
dations are signiﬁcant for gains up to at least 20 dB. This shows
that for small ampliﬁcation gains, as usually used with open
ﬁttings, there is a need for leakage cancellation.
Fig. 8 shows the performance of the combinations of NR and
ANC [cascaded (Fig. 3) and integrated (Fig. 5)] compared to a
classic NR, for gain
dB. The degree of causality is
here kept high enough (
, i.e., for
the criterion
(72) is fullﬁlled) so that no performance tradeoff has to be made
between the NR and the ANC. For gains up to 15 dB, cascading
NR and ANC allows to maintain a constant SNR improvement
of around 4 dB, which is already signiﬁcantly better then the
performance of the NR alone. When the gain is increasing above
15 dB, the performance converges to the performance of the NR
alone. The integrated approach gives an almost constant SNR
improvement around 12 dB for all values of the gain. This is
better than NR alone or the cascaded NR and ANC.
All these results are given for a system where the degree of
causality is sufﬁcient for any processing, which is not the case
in a realistic system.


===== [page 9] =====

SERIZEL et al.: INTEGRATED ACTIVE NOISE CONTROL AND NOISE REDUCTION IN HEARING AIDS
1145
Fig. 9. Performance depending on the degree of non-causality.
C. Causality Study
In hearing aids, the causality margins are much smaller
than what was used for the previous simulations. Based on the
transfer functions which are used here, the degree of causality
for a signal coming from an angle of 270 (the noise direction
of arrival) is seen to be about two samples (rather than the 48
samples used previously).
To see how the delays in the system can affect performance,
for each algorithm the ampliﬁcation is set to
dB, and a
delay is added to the input signals (BTE microphones), to allow
the degree of causality to vary between
16 and 48. Fig. 9 shows
the SNR improvement for each algorithm as a function of the
degree of causality .
When the degree of causality is high, the obtained perfor-
mance for the cascade is close to what was obtained in Fig. 8.
When the degree of causality decreases and becomes lower than
the NR delay (
), the SNR improvement starts to de-
crease and eventually converges to the improvement obtained
with the classic NR. This is due to the fact that for a degree
of causality lower than 32, the ANC has to be designed as a
non-causal system, therefore its performance is reduced. The in-
tegrated approach gives an almost constant SNR improvement
as long as the overall system is causal.
Fig. 10 shows the SNR improvement given by the three al-
gorithms for a realistic degree of causality equal to 2, which
corresponds to what has been measured on the transfer func-
tions used for the simulations. For lower gains,
dB,
the cascade approach gives only minor improvement (around 1
dB) compared to the standard scheme, then their performances
tend to converge as ampliﬁcation is increased. The integrated
approach on the other hand maintains an SNR improvement of
more than 10 dB. Therefore, this integrated approach seems to
offer a practical way to introduce ANC in hearing aids.
Finally, Fig. 11 shows the SNR improvement for
for the integrated approach and the NR only approach. Here,
the performance improvement achieved with the integrated
approach is mainly due to the secondary path compensation.
Fig. 11 also shows the SNR improvement obtained with a ﬁl-
tered-x MWF algorithm that does not include the ANC, which
is indeed found to achieve a similar performance improvement.
Fig. 10. Performance comparison for noise reduction scheme with or without
active noise control,  = 2.
Fig. 11. Performance for a non-causal system,  =  16.
VI. CONCLUSION
Standard NR techniques used in hearing aids ignore leakage
and secondary path effects. When open ﬁttings are used these
aspects cannot be neglected and are in fact found to seriously
degrade the NR performance. ANC can then be used to reduce
the impact of the leakage, it has shown to provide SNR improve-
ments between 4 dB and 12 dB depending on the approach used.
The ANC performance is conditioned by the system causality
which differs for the two algorithms evaluated here. A cascaded
approach can give good results (SNR improvement around
4 dB) as long as the system causality is high enough to support
the NR latency (
). This is not a realistic assumption for
hearing aids where the latency margin is in fact close to zero.
An alternative integrated approach of ANC with NR has
shown to improve the SNR by about 12 dB for low hearing
aid gains (between 0 dB and 20 dB), as long as the system is
causal. When the system becomes non-causal, the integrated
approach can still outperform standard NR algorithms by taking
the secondary path into account in the speech enhancement
and ampliﬁcation process, thereby reducing the impact of
the leakage on the output signal. All the previous schemes,
however, rely on the presence of an ear canal microphone.
Commercial hearing aids currently do not have an ear canal
microphone. Adding this extra microphone might induce some
problems such as bone conduction to the ear canal microphone
when the user talks. These problems would have to be investi-
gated before practical tests.


===== [page 10] =====

1146
IEEE TRANSACTIONS ON AUDIO, SPEECH, AND LANGUAGE PROCESSING, VOL. 18, NO. 6, AUGUST 2010
REFERENCES
[1] J. Kiessling, “Sounds towards the tympanic membrane,” in Proc. 8th
EFAS Congr., Heidelberg, Germany, Jun. 2007.
[2] L. J. Grifﬁths and C. W. Jim, “An alternative approach to linearly con-
strained adaptive beamforming,” IEEE Trans. Antennas Propagat., vol.
AP-30, no. 1, pp. 27–34, Jan. 1982.
[3] S. Doclo, A. Spriet, J. Wouters, and M. Moonen, “Frequency-domain
criterion for the speech distortion weighted multichannel wiener ﬁlter
for robust noise reduction,” Speech Commun., vol. 49, no. 7-8, pp.
636–656, 2007.
[4] S. J. Elliott and P. A. Nelson, Active Control of Sound.
Cambridge,
MA: Academic, 1993.
[5] S. M. Kuo and D. R. Morgan, “Active noise control: a tutorial review,”
Proc. IEEE, vol. 87, no. 6, pp. 943–973, Jun. 1999.
[6] R. Serizel, M. Moonen, J. Wouters, and S. H. Jensen, “Combined active
noise control and noise reduction in hearing aids,” in Proc. 11th Int.
Workshop Acoust. Echo Noise Control (IWAENC), Sep. 2008.
[7] J. C. Burgess, “Active adaptive sound control in a duct: a computer
simulation,” J. Acoust. Soc. Amer., vol. 70, no. 3, pp. 715–726, Sep.
1981.
[8] B. Widrow and S. D. Stearns, Adaptive Signal Processing.
Engle-
wood Cliffs, NJ: Prentice-Hall, 1985.
[9] E. Bjarnason, “Analysis of the ﬁltered-x LMS algorithm,” IEEE Trans.
Speech Audio Process., vol. 3, no. 6, pp. 504–514, Nov. 1995.
[10] H. Dillon, Hearing Aids.
New York: Thieme, 2001.
[11] L. J. Eriksson and M. C. Allie, “Use of random noise for on-line trans-
ducer modeling in an adaptive active attenuation system,” J. Acoust.
Soc. Amer., vol. 85, no. 2, pp. 797–802, Feb. 1989.
[12] S. M. Kuo and D. Vijayan, “A secondary path modeling technique for
active noise controlsystems,” IEEE Trans. Speech Audio Process., vol.
5, no. 4, pp. 374–377, Jul. 1997.
[13] M. Zhang, H. Lan, and W. Ser, “Cross-updated active noise control
system with online secondary path modeling,” IEEE Trans. Speech
Audio Process., vol. 9, no. 5, pp. 598–602, Jul. 2001.
[14] W. S. Gan and S. M. Kuo, “An integrated audio and active noise control
headset,” IEEE Trans. Consumer Electron., vol. 48, no. 2, pp. 242–247,
May 2002.
[15] S. M. Kuo and B. M. Finn, “An integrated audio and active noise con-
trol system,” in Proc. IEEE Int. Symp. Circuits Syst. ISCAS’93, 1993,
pp. 2529–2532.
[16] X. Kong and S. M. Kuo, “Study of causality constraint on feedforward
active noise control systems,” IEEE Trans. Circuits Systems II: Analog
Digital Signal Process., vol. 46, no. 2, pp. 183–186, Feb. 1999.
[17] D. R. Morgan and J. C. Thi, “A delayless subband adaptive ﬁlter archi-
tecture,” IEEE Trans. Signal Process., vol. 43, no. 8, pp. 1819–1830,
Aug. 1995.
[18] B. Rafaely and M. Furst, “Audiometric ear canal probe with active am-
bient noise control,” IEEE Trans. Speech Audio Process., vol. 4, no. 3,
pp. 224–230, May 1996.
[19] M. Nilsson, S. D. Soli, and A. Sullivan, “Development of the Hearing in
Noise Test for the measurement of speech reception thresholds in quiet
and in noise,” J. Acoust. Soc. Amer., vol. 95, no. 2, pp. 1085–1099, Feb.
1994.
[20] “Auditory Tests (Revised), Compact Disc, Auditec,”.
St. Louis, MO,
Auditec, 1997.
[21] J. E. Greenberg, P. M. Peterson, and P. M. Zurek, “Intelligi-
bility-weighted measures of speech-to-interference ratio and speech
system performance,” J. Acoust. Soc. Amer., vol. 94, no. 5, pp.
3009–3010, Nov. 1993.
[22] American National Standard Methods for Calculation of the Speech
Intelligibility Index, ANSI S3.5–1997, Acoust. Soc. Amer., 1997.
Romain Serizel received the M.Eng. degree in
automatic system engineering from ENSEM, Nancy,
France, in 2005 and the M.Sc. degree in signal pro-
cessing from Université Rennes 1, Rennes, France,
in 2006. He is currently pursuing the Ph.D. degree
under the supervision of Prof. M. Moonen in the
Electrical Engineering Department (ESAT-SCD),
Katholieke Universiteit Leuven, Leuven, Belgium.
His research interests include hearing aids systems
and digital signal processing for audio.
Marc Moonen (M’94–SM’06–F’07) received the
electrical engineering degree and the Ph.D. degree
in applied sciences from Katholieke Universiteit
Leuven, Leuven, Belgium, in 1986 and 1990, re-
spectively.
Since 2004, he has been a Full Professor in the
Electrical
Engineering
Department,
Katholieke
Universiteit Leuven, where he is heading a research
team working in the area of numerical algorithms
and signal processing for digital communications,
wireless communications, DSL, and audio signal
processing.
Prof. Moonen received the 1994 K.U.Leuven Research Council Award, the
1997 Alcatel Bell (Belgium) Award (with P. Vandaele), the 2004 Alcatel Bell
(Belgium) Award (with R. Cendrillon), and was a 1997 “Laureate of the Belgium
Royal Academy of Science.” He received a journal best paper award from the
IEEE TRANSACTIONS ON SIGNAL PROCESSING (with G. Leus) and from Elsevier
Signal Processing (with S. Doclo). He was chairman of the IEEE Benelux Signal
Processing Chapter (1998–2002), and is currently Past-President of EURASIP
(European Association for Signal Processing) and a member of the IEEE Signal
Processing Society Technical Committee on Signal Processing for Communi-
cations. He has served as Editor-in-Chief for the EURASIP Journal on Applied
Signal Processing (2003–2005), and has been a member of the editorial board
of IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS II (2002–2003), and IEEE
Signal Processing Magazine (2003–2005) and Integration, the VLSI Journal.
He is currently a member of the editorial board of EURASIP Journal on Ap-
plied Signal Processing, EURASIP Journal on Wireless Communications and
Networking, and Signal Processing.
Jan Wouters was born in Leuven, Belgium, in 1960. He received the physics
degree and the Ph.D. degree in sciences/physics from the Katholieke Univer-
siteit Leuven, Leuven, Belgium, in 1982 and 1989, respectively.
From 1989 until 1992, he was a Research Fellow with the Belgian National
Fund for Scientiﬁc Research (FWO) at the Institute of Nuclear Physics (UCL
Louvain-la-Neuve and K.U. Leuven) and at NASA Goddard Space Flight
Center. Since 1993, he has been a Professor at the Neurosciences Department
of the K.U. Leuven (Full Professor since 2001). His research activities center
around audiology and the auditory system, signal processing for cochlear
implants, and hearing aids. He is author of about 145 articles in international
peer-reviewed journals and is a reviewer for several international journals.
Dr. Wouters received an Award of the Flemish Ministry in 1989, a Fullbright
Award and a NATO Research Fellowship in 1992, and the Flemish VVL Speech
Therapy–Audiology Award in 1996. He is member of the International Col-
legium for ORL (CORLAS), a Board Member of the International Collegium
for Rehabilitative Audiology (ICRA), and is responsible for the Laboratory for
Experimental ORL and the audiology program at K.U. Leuven.
Søren Holdt Jensen (S’87–M’88–SM’00) received
the M.Sc. degree in electrical engineering from Aal-
borg University, Aalborg, Denmark, in 1988, and the
Ph.D. degree in signal processing from the Technical
University of Denmark, Lyngby, in 1995.
He is a Full Professor at Aalborg University and
is currently heading a research team working in the
area of numerical algorithms and signal processing
for speech and audio processing, image and video
processing, multimedia technologies, and digital
communications. Before joining the Department of
Electronic Systems at Aalborg University, he was with the Telecommunications
Laboratory of Telecom Denmark, Ltd., Copenhagen, Denmark, the Electronics
Institute of the Technical University of Denmark, the Scientiﬁc Computing
Group of Danish Computing Center for Research and Education (UNI•C),
Lyngby, Denmark, the Electrical Engineering Department of Katholieke Uni-
versiteit Leuven, Leuven, Belgium, and the Center for PersonKommunikation
(CPK) of Aalborg University.
Prof. Jensen was an Associate Editor for the IEEE TRANSACTIONS ON SIGNAL
PROCESSING, and is currently Member of the Editorial Board of Elsevier Signal
Processing and the EURASIP Journal on Advances in Signal Processing. He is a
recipient of an European Community Marie Curie Fellowship, former Chairman
of the IEEE Denmark Section, and Founder and Chairman of the IEEE Denmark
Section’s Signal Processing Chapter.
