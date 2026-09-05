11th Convention of the European Acoustics Association
Málaga, Spain • 23rd – 26th June 2025 •
STEERABLE NEURAL DIRECTIONAL FILTERING
Weilong Huang
Mhd Modar Halimeh
Srikanth Raj Chetupalli
Oliver Thiergart
Emanuël Habets
International Audio Laboratories Erlangen†, Am Wolfsmantel 33, 91058 Erlangen, Germany
†A joint institution of the Friedrich-Alexander-Universität Erlangen-Nürnberg (FAU)
and Fraunhofer Institute for Integrated Circuits (IIS)
ABSTRACT
Sound capture with specific directivity patterns is es-
sential in many far-field speech communication systems.
Traditionally, fixed beamformers provide this capability
through predefined directivity patterns.
However, the
fixed beamformers’ characteristics, such as the white
noise gain and directivity factor, highly depend on the
number of microphones, and their directivity and ro-
bustness at low frequencies are often inadequate.
Re-
cent works have employed deep neural network-based
approaches, such as neural directional filtering, to over-
come the limitations of conventional fixed beamformers
and demonstrate superior performance.
This paper ex-
pands on the concept of neural directional filtering by in-
corporating steerable capabilities, termed steerable neural
directional filtering. We propose a training strategy that
uses the steering direction of the directivity pattern as a
conditioning input for the neural network, allowing for
the generation of directivity patterns aimed at any desired
direction during inference. Additionally, we analyze the
performance of the directivity patterns for various steering
directions, revealing that the performance across different
directions remains consistent.
Keywords: Steerable spatial filtering, directivity pattern,
microphone array
*Corresponding author: weilong.huang@fau.de.
Copyright: ©2025 Huang et al. This is an open-access article
distributed under the terms of the Creative Commons Attribution
3.0 Unported License, which permits unrestricted use, distribu-
tion, and reproduction in any medium, provided the original au-
thor and source are credited.
1. INTRODUCTION
Far-field sound capture is indispensable in many speech
communication systems, such as televisions, video con-
ferencing devices, and smart speakers.
One prevalent
technique is to capture sound from a specific speaker that
forms the task of speaker extraction [1, 2].
This tech-
nique requires information describing the target speaker.
Alternatively, leveraging spatial information rather than
speaker information, deep neural network (DNN)-based
approaches [3, 4] focus on extracting speeches from pre-
defined spatial directions/regions.
As a result, moving
speakers close to a region’s border often results in dis-
continuous directional filtering. Consequently, achieving
sound capture with a controllable and smooth directivity
pattern is critical.
Traditionally, fixed beamformers realize such patterns
by filtering and then superimposing microphone signals.
As one of the fixed beamformers, differential beamform-
ers can achieve a frequency-invariant pattern as the de-
sired pattern using the Jacobi-Anger expansion [5, 6] or
define the null positions to control the shape of the direc-
tivity pattern through the null-constrained method [7, 8].
However, differential beamformers often suffer from low
white noise gain (WNG) at low frequencies, leading to
white noise amplification issues. Moreover, differential
beamformers’ directivity depends on the number of mi-
crophones. For example, the highest order of a directivity
pattern for a uniform circular array (UCA) (which leads
to the highest directivity) is upper-bounded by ⌊Q
2 ⌋, where
the Q is the number of microphones [9]. These limitations
persist despite improvements made via exploiting direc-
tional microphones [10–12].
Recently, a neural directional filtering (NDF) method
[13] is proposed, which overcomes the limitations of the
fixed beamformer. As an example, a 3rd-order differen-


11th Convention of the European Acoustics Association
Málaga, Spain • 23rd – 26th June 2025 •
tial microphone array (DMA) pattern was realized using a
three-microphone UCA with an additional center micro-
phone, which is unfeasible for a differential beamformer.
Moreover, the NDF significantly outperforms conven-
tional algorithms, such as [14,15]. However, trained NDF
models in [13] are limited to static pre-defined patterns.
This paper extends the NDF to a steerable neural direc-
tional filtering (SNDF), which achieves flexible steering
with a single trained model. We propose a training strat-
egy to steer the directivity pattern using a conditioning
input such that the trained model can steer the learned
pattern to any desired direction during inference. Exper-
imental results demonstrate the enhanced steerability of
the proposed SNDF.
2. PROBLEM FORMULATION
We consider a compact microphone array of Q omnidi-
rectional sensors that capture an anechoic acoustic scene
with N sound sources located in the far field of the ar-
ray.
Let Xq,n[f, t] represent the signal from the n-th
source as captured by the q-th microphone in the short-
time Fourier transform (STFT) domain, where f and t
denote the frequency-bin and time-frame indices, respec-
tively.
The signal at the q-th microphone, denoted as
Yq[f, t], is expressed as
Yq[f, t] =
N
X
n=1
Xq,n[f, t] + Vq[f, t],
(1)
where Vq[f, t] represents the sensor noise, which is as-
sumed to be spatially uncorrelated across the micro-
phones, and q ∈1, 2, . . . , Q.
Furthermore, we have
Xq,n[f, t] = Hpq,pn[f] Xn[f, t], where Hpq,pn[f] mod-
els the acoustic transfer function (ATF) between the n-th
source Xn[f, t] at position pn and the q-th microphone
located at position pq.
The objective of the steerable neural directional fil-
tering task is to capture the acoustic scene with N sources
at a position pVDM with a steerable directivity pattern
Ψθs[θ], where θ denotes the direction-of-arrival (DOA) of
a source in the far field and θs is the steering direction
of this pattern. In this paper, we assume that all sound
sources and microphones are positioned in the x-y plane,
thereby simplifying our formulation to a two-dimensional
pattern-learning scenario. For simplicity, we also assume
that pVDM is the origin of the coordinate system, the inci-
dent angle for the n-th source θn = arctan2(ypn, xpn),
where ypn and xpn represent the coordinates of the posi-
tion pn on the y-axis and x-axis, respectively. One pos-
STFT
iSTFT
Microphone Array signals
Steering Direction
Input [B, T, F, 2Q]
F-BiLSTM [256]
T-UniLSTM [128]
Linear + Tanh
Mask [B, T, F, 2]
Linear
One Hot Vector Encoding 
FT-JNF Architecture
Steering Mechanism 
Symbols and variables:
B: The batch size
T: The number of time frames
F: The number of frequency bins
Q: The number of microphones
Figure 1. FT-JNF based neural directional filtering
with the steering mechanism.
sible realization of this task is to mimic a virtual direc-
tional microphone (VDM) located at reference position
pVDM with the required directivity pattern steered towards
the specified direction θs. Therefore, the output Zθs[f, t]
of the VDM represents the target signal for our task. In
an anechoic room, there is only one direct-path impulse
response (DPIR) HpVDM,pn[f] between the n-th source
and an omnidirectional microphone at the position of the
VDM; then the VDM signal is expressed as
Zθs[f, t] =
N
X
n=1
Ψθs[θn] HpVDM,pn[f] Xn[f, t].
(2)
In this work, we propose a data-driven approach
wherein a neural network utilizes microphone signals
along with the desired steering direction to estimate the
target signal.
3. PROPOSED METHOD
3.1 Neural Network Architecture
In this work, we employ the spatially selective filter based
on JNF neural network architecture (JNF-SSF) [4], shown
in Fig. 1.
In this architecture, the real and imaginary
parts of the Q microphone signals in the STFT domain
are stacked along the channel dimension, resulting in an
input with dimensions of [B, T, F, 2Q], where T repre-
sents the number of time frames, F denotes the number
of frequency bins, and B indicates the batch size during
training. Firstly, the input is reshaped into an input with
dimensions of [B × T, F, 2Q] and then fed into a bidi-
rectional long short-term memory (LSTM) layer, referred


11th Convention of the European Acoustics Association
Málaga, Spain • 23rd – 26th June 2025 •
to as F-BiLSTM, which models the spectro-spatial rela-
tionships in the data. In addition to the microphone array
signals, we input an angle θs through the steering mech-
anism. This angle represents the steering direction of the
directivity pattern. Within the steering mechanism, the
input angle is encoded into a one-hot vector, the dimen-
sion of which is determined by the defined angular reso-
lution. Subsequently, a linear layer processes the one-hot
encoded vector, ensuring that its outputs are compatible
with the input dimensions of the F-BiLSTM layer. We
employ the steering direction-based information from the
linear layer to initialize the forward and backward initial
states of the F-BiLSTM layer for each time frame, as in
[4]. The output from the F-BiLSTM layer is then reshaped
into [B × F, T, 512] which is processed by a second uni-
directional LSTM layer, denoted as T-UniLSTM, which
can model the temporal relationships in the data. This
study focuses on a frame-level causal scenario; therefore,
the T-UniLSTM is configured to be unidirectional. The
first F-BiLSTM layer contains 256 hidden units, while
the second T-UniLSTM layer contains 128. Finally, the
output of the second LSTM is reshaped to [B, F, T, 256]
and then passed through a linear layer with a hyperbolic
tangent activation function, which computes a complex-
valued single-channel mask, denoted Mθs[f, t]. The de-
sired VDM signal is then estimated by applying this mask
to the reference microphone signal (here chosen to be the
first microphone positioned at the center of the array) as
follows
bZθs[f, t] = Mθs[f, t]Y1[f, t].
(3)
3.2 Loss Function
In this work, we utilize a batch-aggregated normalized L1
loss function to measure mean absolute error (MAE), for-
mulated as:
LMAE =
PB
b=1
zb
VDM −bzb
VDM

1
PB
b=1
zb
VDM

1 + ϵ
,
(4)
where ϵ is a small constant value, and the signals zVDM
and bzVDM are the time-domain signals of the STFT repre-
sentations Zθs[f, t] and bZθs[f, t], respectively.
3.3 Training Strategy
Our earlier research, as detailed in [13], has shown that
the DNN models trained with two or more concurrently
active speakers can effectively generalize to scenarios in-
volving up to six speakers. Simultaneously, training with
more than three speakers does not significantly enhance
the model’s performance.
Therefore, in this study, we
train our model using mixtures of up to three speakers.
We perform a discrete uniform sampling of the az-
imuth angle along a circle with a radius of d. This uni-
form sampling generates a number of P discrete admis-
sible speaker positions, each position corresponding to a
DOA having equal angular distances. Then, we locate our
array in the circle’s center and make the array coplanar
and concentric with the circle, such that the radius d is
equivalent to the source-array distance.
We define a specific speaker-array setup as one acous-
tic scene. In each acoustic scene, we randomly select N
positions from the P discrete admissible speaker positions
for N speech sources, where N ∈{1, 2, 3}. Then we sim-
ulate Hpq,pn[f] for all N sources and Q microphones us-
ing the room impulse response (RIR) generator [16] with
a reflection order of zero. Following this, we compute Q
microphone signals for this acoustic scene using (1). For
each acoustic scene, we simulate M target VDM signals
for steering directions uniformly spanning 0◦to 360◦de-
grees, where M = 360◦
ϑ
and ϑ denotes the angular resolu-
tion of the steerable network. The m-th VDM target sig-
nal Zθm
s [f, t] corresponding to the steering direction θm
s
is obtained using (2). During training, we consider micro-
phone signals from each acoustic scene paired with one
VDM target signal Zθm
s [f, t] as a training sample. This
process is then repeated for M target signals. Thus, the
repeated utilization of the same microphone signals for
training helps to emphasize the steerability function.
In addition, we introduce an enhanced mini-batch
sampling approach. More specifically, for a mini-batch
of B samples, at least one sample must contain a speaker
from the target direction or its vicinity. This prevents the
denominator calculation for L1-based loss functions from
becoming excessively small. Therefore, the loss returned
in each iteration is more stable, thereby enhancing the ro-
bustness of our model training process.
4. EXPERIMENTAL SETUP
4.1 Target directivity pattern
The frequency-independent directivity pattern of an Rth-
order DMA for the target direction θs is defined as [17]
Ψθs[θ] =
R
X
r=0
ar cosr(θ −θs),
(5)
where ar, r ∈{0, 1, · · · , R} are real coefficients and de-
termine the shape of DMA patterns. At the target direc-


11th Convention of the European Acoustics Association
Málaga, Spain • 23rd – 26th June 2025 •
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-30 -20 -10
0
1st-order Pattern
3rd-order Pattern
6th-order Pattern
Figure 2. Three target DMA patterns for training our
DNN models.
tion θs, the response must be equal to 1, i.e., Ψθs[θs] = 1.
Therefore, we have PR
r=0 ar = 1.
In this paper, we choose three DMA directivity pat-
terns as target patterns for the DNN model to learn. The
first pattern is the first-order cardioid pattern with coef-
ficients a0 =
1
2 and a1 =
1
2; The second pattern is the
third-order pattern with coefficients a0 = 0, a1 =
1
6,
a2 = 1
2, and a3 = 1
3; The third pattern is the sixth-order
pattern with coefficients a0 =
1
49, a1 =
8
49, a2 =
8
49,
a3 = −48
49, a4 = −48
49, a5 = 64
49, and a6 = 64
49. Polar plots
of the respective patterns steered towards 0◦are shown
in Fig. 2. In the training and testing, we use these target
DMA patterns to generate the target VDM signals via (2).
Additionally, throughout this paper, we set the maximum
suppression at −40 dB (linear scale: 0.01) for all target di-
rectivity patterns in training and testing when generating
target VDM signals.
4.2 Performance Evaluation
We consider a test dataset with K test samples. For each
test sample, we have N concurrent active sound sources
from different directions. For the k-th sample, we use θk
to represent these directions
θk = θk
1, . . . , θk
n, . . . , θk
N.
(6)
where θk
n represents the incident angle of the n-th speaker
for the k-th test sample.
The STFT representation
Xk
1,n[f, t] stands for n-th speaker of the k-th sample as
received by the reference microphone q = 1.
4.2.1 Estimated directivity patterns
For the k-th test sample, we apply the estimated mask
Mθs[f, t] separately to the direct-path part of each indi-
vidual source, such as the n-th speaker Xk
1,n[f, t] at the
reference microphone.
The corresponding narrowband
power ratio ζk
θs,n[f] of the masked source signals to the
unmasked source signals is then calculated as
ζk
θs,n[f] =
PT
t=1
Mθs[f, t] Xk
1,n[f, t]
2
PT
t=1
Xk
1,n[f, t]
2
,
(7)
and the wideband power ratio ξk
θs,n for the n-th source of
the k-th sample is given as:
ξk
θs,n =
PF
f=1
PT
t=1
Mθs[f, t] Xk
1,n[f, t]
2
PF
f=1
PT
t=1
Xk
1,n[f, t]
2
.
(8)
After we obtain the power ratios, we can obtain the
learned patterns for the entire test dataset. The narrow-
band directivity pattern bBθs[θ, f] is given by:
bBθs[θ, f] =
v
u
u
t 1
|Hθ|
X
(k,n)∈Hθ
ζk
θs,n[f],
(9)
where Hθ is a set of indices (k, n) that include all sources
in the test dataset which are located in the direction θ and
|Hθ| represents the cardinality of the set Hθ. We define
Hθ as follows
Hθ =

(k, n) | θk
n = θ
	
.
(10)
The wideband directivity pattern bPθs[θ] is then given by:
bPθs[θ] =
v
u
u
t 1
|Hθ|
X
(k,n)∈Hθ
ξk
θs,n.
(11)
4.2.2 Signal-to-distortion ratio
We use the averaged signal-to-distortion ratio (SDR) [18,
19] to measure the distance between the estimated and tar-
get signal
SDR = 10
K
K
X
k=1
log10
 
zk
VDM
2
2
zk
VDM −bzk
VDM
2
2 + ϵ)
!
, (12)
where zk
VDM and bzk
VDM are the time-domain signals cor-
responding to the STFT representations Zk
θs[f, t] and
bZk
θs[f, t] at the k-th sample in the test set, respectively.
4.3 Datasets
We followed the dataset preparation scheme in [13] for
the microphone array signals. All speech sources were
taken from the LibriSpeech database [20]. We used the
subsets ‘train-clean-360’, ‘dev-clean’, and ‘test-clean’ for
training, validation, and testing. We truncated each speech


11th Convention of the European Acoustics Association
Málaga, Spain • 23rd – 26th June 2025 •
source signal into a 4-second sample prior to convolution
by the acoustic impulse response (AIR). If any sources
from LibriSpeech were shorter than 4 seconds, we ex-
tended them by zero-padding.
The number of admissible speaker positions for
the training set and validation set were restricted to
Ptrain
=
72
with
θ
∈
{0◦, 5◦, · · · , 355◦}
and
Pvalidate = 72 with θ ∈{2.5◦, 7.5◦, · · · , 357.5◦}.
The
training and validation sets consisted of 11520 and
2880 acoustic scenes, respectively. Each acoustic scene
corresponded to M
=
72 VDM target signal with
θs ∈{0◦, 5◦, · · · , 355◦}. Therefore, the number of sam-
ples for the training set was 11520 × 72, and the number
for the validation set was 2880 × 72.
The number of admissible speaker positions for
the
test
set
was
restricted
to
Ptest
=
144
with
θ ∈{1.25◦, 3.75◦, · · · , 358.75◦}. During testing, each
acoustic scene contained two concurrent speakers. The
test set consisted of 3240 acoustic scenes. For each acous-
tic scene, we generated five target VDM signals with
θs ∈{0◦, 30◦, 60◦, 90◦, 120◦}. Therefore, the number of
samples in the test set was 3240 × 5.
Similar to [13], we normalized all signals after con-
volution with the RIR to achieve a loudness within
[−33, −25] dBFS. Additionally, we added white Gaus-
sian noise for the array’s microphones as microphone self-
noise at a signal-to-noise ratio of 30 dB with respect to the
mixture of all speakers.
4.4 Configuration details
We employed a four-microphone configuration (Q = 4),
consisting of a microphone at the center of the array
(q = 1) and three microphones (q = 2, 3, 4) arranged in
a UCA. The VDM was placed at the center microphone
position, i.e., pVDM = p1. The diameter of the UCA was
3 cm.
For each directivity pattern, a DNN model was trained
to a maximum of 100 epochs. We configure all models
with a batch size of 10 and a learning rate of 0.001. The
final model was selected based on the lowest validation
loss observed throughout the training epochs. All trained
DNNs have a total of 873K parameters. The STFT was
computed on signal frames of 32 ms duration, using a
square-root Hann window with a 50 % overlap at a sam-
pling frequency of 16 kHz. We set ϵ = 1.2 · 10−7.
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-15-10-5 0
Estimate
Target
(a) Target at 0◦( bP)
0°
60° 120°180°240°300°360°
DOA (angles)
0
1
2
3
4
5
6
7
8
Frequency (kHz)
30
25
20
15
10
5
0
(b) Target at 0◦( bB)
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-15-10-5 0
Estimate
Target
(c) Target at 60◦( bP)
0°
60° 120°180°240°300°360°
DOA (angles)
0
1
2
3
4
5
6
7
8
Frequency (kHz)
30
25
20
15
10
5
0
(d) Target at 60◦( bB)
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-15-10-5 0
Estimate
Target
(e) Target at 120◦( bP)
0°
60° 120°180°240°300°360°
DOA (angles)
0
1
2
3
4
5
6
7
8
Frequency (kHz)
30
25
20
15
10
5
0
(f) Target at 120◦( bB)
Figure 3. DNN estimated wideband pattern (marked
as bP) and narrowband pattern (marked as bB) for the
target cardioid pattern
5. EXPERIMENTAL RESULTS
We study the performance of the proposed steerable neu-
ral directional filtering in terms of estimated directivity
patterns, SDR, and audio spectrograms.
5.1 Steerable patterns
Figures 3, 4 and 5 show the estimated wideband direc-
tivity patterns bPθs[θ] and narrowband directivity patterns


11th Convention of the European Acoustics Association
Málaga, Spain • 23rd – 26th June 2025 •
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-20-15-10-5 0
Estimate
Target
(a) Target at 0◦( bP)
0°
60° 120°180°240°300°360°
DOA (angles)
0
1
2
3
4
5
6
7
8
Frequency (kHz)
30
25
20
15
10
5
0
(b) Target at 0◦( bB)
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-20-15-10-5 0
Estimate
Target
(c) Target at 60◦( bP)
0°
60° 120°180°240°300°360°
DOA (angles)
0
1
2
3
4
5
6
7
8
Frequency (kHz)
30
25
20
15
10
5
0
(d) Target at 60◦( bB)
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-20-15-10-5 0
Estimate
Target
(e) Target at 120◦( bP)
0°
60° 120°180°240°300°360°
DOA (angles)
0
1
2
3
4
5
6
7
8
Frequency (kHz)
30
25
20
15
10
5
0
(f) Target at 120◦( bB)
Figure 4. DNN estimated Wideband pattern (marked
as bP) and Narrowband pattern (marked as bB) for the
target 3rd-order pattern
bBθs[θ, f] for the first-order cardioid, third-order, and sixth-
order target patterns, respectively. The left-hand side (a,
c, e) of each figure shows the estimated wideband direc-
tivity patterns and compares them with the correspond-
ing target pattern in different steering directions θs =
{0◦, 60◦, 120◦}. Meanwhile, each figure’s right-hand side
(b, e, f) shows the estimated narrowband directivity pat-
terns in different steering directions θs = {0◦, 60◦, 120◦}.
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-20-15-10-5 0
Estimate
Target
(a) Target at 0◦( bP)
0°
60° 120°180°240°300°360°
DOA (angles)
0
1
2
3
4
5
6
7
8
Frequency (kHz)
30
25
20
15
10
5
0
(b) Target at 0◦( bB)
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-20-15-10-5 0
Estimate
Target
(c) Target at 60◦( bP)
0°
60° 120°180°240°300°360°
DOA (angles)
0
1
2
3
4
5
6
7
8
Frequency (kHz)
30
25
20
15
10
5
0
(d) Target at 60◦( bB)
0°
30°
60°
90°
120°
150°
180°
210°
240°
270°
300°
330°
-20-15-10-5 0
Estimate
Target
(e) Target at 120◦( bP)
0°
60° 120°180°240°300°360°
DOA (angles)
0
1
2
3
4
5
6
7
8
Frequency (kHz)
30
25
20
15
10
5
0
(f) Target at 120◦( bB)
Figure 5. DNN estimated Wideband pattern (marked
as bP) and Narrowband pattern (marked as bB) for the
target 6th-order pattern
Firstly, we can see that SNDF can learn similar patterns
for different steering directions. The shape of the esti-
mated patterns is steering invariant. Secondly, the main-
lobe of the target pattern is well approximated, while the
null direction has a limited attenuation. Lastly, we can
also see that the estimated patterns are frequency invari-
ant as desired.


11th Convention of the European Acoustics Association
Málaga, Spain • 23rd – 26th June 2025 •
Table 1. SDR [dB] over various steering directions.
0◦
30◦
60◦
90◦
120◦
1st-order pattern
25.81
25.90
25.89
25.96
25.95
3rd-order pattern
20.16
20.22
20.21
20.20
20.29
6th-order pattern
17.21
17.06
16.89
16.73
17.51
5.2 SDR results
We show the averaged SDR for different steering direc-
tions θs ∈{0◦, 30◦, 60◦, 90◦, 120◦} in Table 1. It is clear
that the SNDF achieves similar performance over differ-
ent steering directions in terms of SDR. Since the input
microphone array signals in the test set remain the same
for different steering directions, this implicitly suggests
that the target speakers differ for each direction, lead-
ing to minor differences in the SDRs over steering direc-
tions. Moreover, higher-order target patterns are increas-
ingly difficult for DNN to learn. The target VDM signals
for the sidelobes around the null positions are low-power
signals, resulting in poor SDR, as observed also in [13].
5.3 Spectrogram Example
To illustrate the SNDF performance, we designed an
acoustic scene of duration 20 seconds involving two sound
sources, a speech source located at an angle of 60◦and a
music source located at an angle of 230◦with respect to
the center of the array. Both sources were active simul-
taneously, producing a fully overlapping mixture signal
in the reference microphone, which is illustrated in Fig-
ure 6(a). During the first 10 seconds, we set the steer-
ing direction to 60◦using the steering mechanism in our
method. We adjust the steering direction for the subse-
quent 10 seconds to 230◦. We processed this mixture us-
ing the SNDF model trained with a first-order pattern as
the target pattern. The expected output (target VDM sig-
nal) and the output of our proposed method for this infer-
ence scenario are shown in Figure 6(b) and Figure 6(c), re-
spectively. During the first 10 seconds, the music source is
used as interference, which arrives from an angle close to
the null direction and is consequently suppressed. A simi-
lar phenomenon is observed for the last 10 seconds where
the speech source as interference is suppressed. There is
no evident signal distortion comparing the spectrogram
of the output signal by the proposed SNDF to the spec-
trogram of the VDM signal. It is worth noting that the
SNDF works well for music even though it is trained us-
ing speech only.
0
5
10
15
20
Time (s)
0.0
0.5
1.0
2.0
4.0
Frequency (kHz)
(a) Reference microphone signal
0
5
10
15
20
Time (s)
0.0
0.5
1.0
2.0
4.0
Frequency (kHz)
(b) Target VDM signal
0
5
10
15
20
Time (s)
0.0
0.5
1.0
2.0
4.0
Frequency (kHz)
(c) Output signal by the proposed SNDF
Figure 6. Spectrograms comparison for a scenario
with different steering direction of the SNDF.
6. CONCLUSIONS
In this paper, we have proposed a DNN-based steerable
directional filtering method named SNDF. We propose a
training strategy that considers the directivity pattern and
steering direction. The steering direction is also used as
an additional input to the model, which allows the model
to form a directivity pattern steered in any desired direc-
tion during inference. The experimental results demon-
strate the SNDF’s steerability by comparing the learned
and target patterns. Meanwhile, the SNDF achieves simi-
lar SDRs over different steering directions. Furthermore,
SNDF can learn high-order patterns, even when the order
exceeds the number of microphones.


11th Convention of the European Acoustics Association
Málaga, Spain • 23rd – 26th June 2025 •
7. REFERENCES
[1] M. Delcroix, K. Zmolikova, K. Kinoshita, A. Ogawa,
and T. Nakatani, “Single channel target speaker ex-
traction and recognition with speaker beam,” in IEEE
Int. Conf. Acoust. Speech Signal Process. (ICASSP),
pp. 5554–5558, IEEE, 2018.
[2] K. Žmolíková, M. Delcroix, K. Kinoshita, T. Ochiai,
T. Nakatani, L. Burget, and J. ˇCernock`y, “Speaker-
beam:
Speaker aware neural network for target
speaker extraction in speech mixtures,” IEEE Journal
of Selected Topics in Signal Processing, pp. 800–814,
2019.
[3] K. Tesch and T. Gerkmann, “Nonlinear spatial filter-
ing in multichannel speech enhancement,” IEEE/ACM
Trans. on Audio, Speech, and Language Processing,
vol. 29, pp. 1795–1805, 2021.
[4] K. Tesch and T. Gerkmann, “Multi-channel speech
separation using spatially selective deep non-linear fil-
ters,” IEEE/ACM Trans. on Audio, Speech, and Lan-
guage Processing, vol. 32, pp. 542–553, 2023.
[5] G. Huang, J. Benesty, and J. Chen, “On the design of
frequency-invariant beampatterns with uniform circu-
lar microphone arrays,” IEEE/ACM Trans. on Audio,
Speech, and Language Processing, pp. 1140–1153,
2017.
[6] G. Huang, J. Chen, and J. Benesty, “Insights into
frequency-invariant beamforming with concentric cir-
cular microphone arrays,” IEEE/ACM Trans. on Au-
dio, Speech, and Language Processing, pp. 2305–
2318, 2018.
[7] J. Benesty and C. Jingdong, Study and design of dif-
ferential microphone arrays, vol. 6. Springer Science
& Business Media, 2012.
[8] G. Huang, I. Cohen, J. Chen, and J. Benesty, “Con-
tinuously steerable differential beamformers with null
constraints for circular microphone arrays,” The Jour-
nal of the Acoustical Society of America, pp. 1248–
1258, 2020.
[9] J. Benesty, J. Chen, and I. Cohen, Design of circular
differential microphone arrays. Springer, 2015.
[10] W. Huang and J. Feng, “Differential beamforming for
uniform circular array with directional microphones,”
in Interspeech 2020, pp. 71–75, 2020.
[11] W. Huang and J. Feng, “Minimum-norm differential
beamforming for linear array with directional micro-
phones,” in Interspeech 2021, pp. 701–705, 2021.
[12] W. Huang and J. Feng, “Robust steerable differential
beamformer for concentric circular array with direc-
tional microphones,” in Asia-Pacific Signal and In-
formation Processing Association Annual Summit and
Conference (APSIPA ASC), pp. 319–323, 2022.
[13] J. Wechsler, S. R. Chetupalli, M. M. Halimeh,
O. Thiergart, and E. A. Habets, “Neural directional fil-
tering: Far-field directivity control with a small micro-
phone array,” in International Workshop on Acoustic
Signal Enhancement (IWAENC), pp. 459–463, IEEE,
2024.
[14] E. Rasumow, M. Hansen, S. van de Par, D. Püschel,
V. Mellert, S. Doclo, and M. Blau, “Regularization
approaches for synthesizing hrtf directivity patterns,”
IEEE/ACM Trans. on Audio, Speech, and Language
Processing, vol. 24, no. 2, pp. 215–225, 2016.
[15] K.
Kowalczyk,
O.
Thiergart,
M.
Taseska,
G. Del Galdo, V. Pulkki, and E. A. P. Habets,
“Parametric spatial sound processing:
A flexible
and efficient solution to sound scene acquisition,
modification, and reproduction,” IEEE Sig. Proc.
Magazine, pp. 31–42, 2015.
[16] E. A. Habets, “Room impulse response generator,”
Technische Universiteit Eindhoven, Tech. Rep, vol. 2,
no. 2.4, p. 1, 2006.
[17] G. W. Elko, “Superdirectional microphone arrays,”
Acoustic signal processing for telecommunication,
pp. 181–237, 2000.
[18] Y. Luo and N. Mesgarani, “Tasnet: time-domain au-
dio separation network for real-time, single-channel
speech separation,” in IEEE Int. Conf. Acoust. Speech
Signal Process. (ICASSP), pp. 696–700, IEEE, 2018.
[19] Y. Luo, Z. Chen, and T. Yoshioka, “Dual-path rnn:
efficient long sequence modeling for time-domain
single-channel speech separation,” in IEEE Int. Conf.
Acoust. Speech Signal Process. (ICASSP), pp. 46–50,
IEEE, 2020.
[20] V. Panayotov, G. Chen, D. Povey, and S. Khudanpur,
“Librispeech: An asr corpus based on public domain
audio books,” in IEEE Int. Conf. Acoust. Speech Sig-
nal Process. (ICASSP), pp. 5206–5210, 2015.
View publication stats
