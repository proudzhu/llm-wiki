

----- [Page 1] -----

      17th European Signal Processing Conference (EUSIPCO 2009)                        Glasgow, Scotland, August 24-28, 2009





   DIRECTION ESTIMATION BASED ON SOUND INTENSITY VECTORS

                                        Sakari Tervo

                                        Helsinki University of Technology
                                  Department of Media Technology
                                P.O.Box 5400, FI-02015 TKK, Finland
                                              sakari.tervo@tkk.ﬁ



           ABSTRACT                     be used to obtain the mixtures.
The direction of a sound source in an enclosure can be       Generally, sound intensity vectors are obtained ei-
estimated with a microphone array and some proper    ther with microphone pair measurements or from B-
signal processing.  Earlier, in applications and in re-   format signals [4].  In practice both of these measure-
search the use of time delay estimation methods, such   ment techniques introduce a bias to the direction of
as the cross correlation, has been popular.  Recently,    the intensity vector.  For example, in Soundﬁeld mi-
techniques for direction estimation that involve sound    crophones, the bias is caused by the non-idealities in
intensity vectors have been developed and used in ap-    the directivity patterns of the microphones [4]. In mi-
plications, e.g. in teleconferencing. Unlike in time de-   crophone pair measurements the direction estimation is
lay estimation, these methods have not been compared    biased, since the gradient of the sound pressure is not
widely. In this article, ﬁve methods for direction estima-    constant within the sensor array [6]. In the case of mi-
tion in the concept of sound intensity vectors are com-   crophone pair measurement, also the non-idealities of
pared with real data from a concert hall. The results    the pressure microphones aﬀect the measurement.
of the comparison indicate that the methods that are      The article is organized as follows.  In Sec.  2 the
based on convolutive mixture models perform slightly    calculation of sound intensity vectors as well the bias
better than some of the simple averaging methods. The   compensation of the vectors are formulated. Section 3
convolutive mixture model based methods are also more    introduces the direction estimation methods. In Sec. 4
robust against additive noise.                            the experimental setup is described and in Sec. 5 the re-
                                                                sults from the experiments are presented and discussed.
              1. INTRODUCTION                  In Sec. 6 the ﬁnal conclusions of this study are given.

Direction or location of a sound source is of interest in                       2. THEORY
several applications that aim to capture or to reproduce
the sound [1, 2, 3].  This is of interest for example in    In a room environment the sound s(t) traveling from
teleconferencing [3]. Moreover, when exploring concert    the sound source to the receiver n is aﬀected by the
hall impulse responses it is of interest from where and   path hn(t):
when the direct sound and the so-called early reﬂections
arrive [4].                                                                pn(t) = hn(t) ∗s(t) + w(t),            (1)
   Direction estimation with traditional methods, such
                                                  where           convolution and w(t) is measurementas the cross correlation, has been researched widely over                                                       ∗denotes                                                               noise, independent and identically distributed for eachseveral decades (see e.g.   [5] and references within).
                                                                receiver.Nowadays, sound intensity vectors are used for direction
estimation in increasingly many applications [1, 2, 3, 6].
                                                     2.1 Sound IntensityNot much research, if any, has been published in com-
paring the diﬀerent methods used in direction estima-   On a certain axis a, the sound intensity is given in the
tion from sound intensity vectors.  In this article, ﬁve    frequency domain as
direction estimation methods are compared in a real
                                                                                                                  (2)concert hall environment.                                             Ia(ω) = Re{P ∗(ω)Ua(ω)},  A sound intensity vector has a length and a direction
and it is a function of time and frequency. In this work,   where P(ω) and Ua(ω) are the frequency presentations
the focus is on the direction estimation over some set    of the sound pressure and of the particle velocity with
of frequencies during a certain time frame.  Direction    angular frequency ω. In addition, Re{·} and is the realestimation methods can be broadly classiﬁed into two    part of a complex number and ∗denotes the complex
classes: 1) direct 2) and mixture estimation. The ﬁrst    conjugate [4]. Here, Cartesian coordinate system with x
class includes methods such as averaging. The second   -and y coordinate axis, shown in Fig. 1, is used. Corre-
class contains convolutive mixture models where the di-   sponding polar coordinate presentation of the Cartesian
rection of the sound source is found by ﬁtting two or    coordinates is denoted with azimuth angle θ and radius
more probability distribution of a certain shape to the     r. The procedure for obtaining the sound intensity pro-
directional data, as for example in [2] and [7]. Naturally,    ceeds as follows and is similar for both axes.
the methods in the second class are much more complex      The sound pressure at the center point between four
than in the ﬁrst, since some optimization method has to    microphones, shown in Fig. 1, can be approximated as

   © EURASIP, 2009                          700

----- [Page 2] -----

the average pressure of the microphones [6]:                                      3

                                4
              P(ω)        Pn(ω).               (3)                                                                         d            ≈14                        n=1X
For x-axis, in frequency domain the particle velocity is                  2            d    1
estimated as
                                                               y
          Ux(ω)   −j                            (4)           ≈ ωρ0d[P1(ω) −P2(ω)],
                                                                    x
                                                                             4
where d is the distance between the two receivers and
ρ0 = 1.2 kg/m3 is the median density of the air and j is
the imaginary unit.                                     Figure 1: The square grid with four microphones and
   Now, the sound intensity in (2) can be estimated    the coordinate system.
with the approximations in (3) and (4). For obtaining
the y-component of the sound intensity, the microphones
1 and 2 are replaced in (4) with microphones 3 and 4.
                                                  where arg{·} is the argument of a complex number, and
2.2  Bias Compensation for the Square Grid       wi = 1/N  is the weighting function.  In principle, the
                                                        weighting function can be chosen freely. If the weighting
Since the pressure signals are subtracted from each other                                                          function is chosen as wi = ri, with     ri = 1, where ri
in the approximation made in (4), the azimuth angle θ of                                                                             is the corresponding radial componentP  of an intensitythe intensity suﬀers from a systematic bias [6]. This bias                                                             vector, then CME is equal to the mean of the Cartesian
can be formulated for a four-microphone square grid as                                                          presentation (MCA) of the sound intensity, i.e.:
[6]

                                                N                        sin(ω 2cd sin(θ))
                 θbiased =                                                          arg        riejθi = arctan  E{Iy}  := ˆθMCA,   (7)                        sin(ω 2cd cos(θ)),            (5)                     Xi=1                E{Ix}
where c = 343 m/s is the speed of sound. The bias can
be   compensated              by                 ﬁnding                          the                                inverse                                          of                                               (5). However,                                                  where                                                                                             is                                                                      the                                                                       expected                                                                                           value,                                                                                                 Ix = [x1,                                                                                                         x2, ..., xN],                                                           E{·}this    equation does                  not                     have                         any                                  closed                                   form                                                 solution.                                                                                                                        ...,                                                                                   the Cartesian                                                                                                    presentation                                                and Iy                                      = [y1,                                                                               y2,                                                                    yN] are
Kallinger et al.  [6] estimate the inverse function with    of the vectors.
linear interpolation. In addition, the inverse function is       Here, the circular median (CMD) is deﬁned analo-
known [6] to have an upper limit at fmax = c/(d√ 2),    gously to CME:
where ω = 2πf, i.e.

                                                   + jMe                                                                                                                                                                                  ,                      d
                 0 < ω                <                         π                        ˆθCMD = arg Me n Re{wiejθi} o                                                                nIm{wiejθi} o                        2c  √2.                                                                              (8)
In this work the linear interpolation for ﬁnding the so-   where Me{·} is the median. The mode could also belution to the inverse function of (5) is included and used   used instead of the median, but this is not considered
for compensating the azimuth angles. The unbiased es-    in this article.  Again, the weighting function can be
timate, i.e. the compensated angle at i:th frequency bin    selected freely.  Here, wi = 1/N  is selected as earlier
is denoted with θi.                                     with CME.

                                                     3.2  Mixture Models       3. METHODS FOR DIRECTION
           ESTIMATION                When inspecting the distribution of the azimuth angle
                                                                of the intensity vectors, for example in Fig. 2, one canIn a certain time window, sound intensity vectors are
                                                           notice that the azimuth angle is a mixture of two distri-estimated over a set of frequencies. Each intensity vector
                                                        butions rather than one. In the example in Fig. 2 the
at frequency bin i, consists of a radial component ri and
                                                             distribution that has smaller variance (or higher con-
of an angular component θi. In this article, the focus is
                                                           centration) is caused by the sound source. The secondon ﬁnding the direction of a sound source from a set of
                                                             distribution models the noise ﬂoor. The shape of theseradial and angular components. Next, ﬁve methods for
                                                             distributions is deﬁned by the impulse response, i.e. thedirection estimation are formulated.
                                              room and the frequency content of the source signal. A
3.1  Circular Mean and Median                 new sound source in the room always introduces a new
                                                             distribution to the total azimuth distribution [2, 7].
In direction estimation one has to take into account the                                                            Since the azimuth angle is circular, wrapped distri-
fact that the data is circular. Therefore, for example the                                                        butions have to be used for the ﬁtting. Here, two dis-
                                                            tributions are tested.  The ﬁrst one is the von Misesmean of a set of angles θ = [θ1, θ2, ..., θN], θi ∈(−π, π]is deﬁned as the circular mean (CME) [8]:                                                           probability distribution (VM) [2, 8]:

                    N
                                                                                  eκ cos(x−µ))
              ˆθCME = arg Xi=1 wiejθi   ,            (6)                 fVM(θ|µ, κ) =        κ)  ,            (9)                                                                                 2πI(0,
                                             701

----- [Page 3] -----

                                                    one of the mixture components models the noise ﬂoor
   .04
                                                 and the other one the sound source. The direction of the
   .03                                                    source is then estimated as the mean parameter µ of the
PDF .02                                                mixtureor highercomponentconcentrationwhich(VMM).has smallerThesevarianceestimated(WGM)direc-
                                                              tions are noted here with ˆθWGMand ˆθVMM according to   .01
                                                         the used model.
    0                                                       In order to ﬁnd the parameters of the mixture model,
                                                 an optimization algorithm has to be used. The search
                                                                   criteria is the same as in maximum-likelihood estima-   .04
                                                                 tion, where the goal is to maximize the likelihood
   .03                                                           N
   .02                                                          L(µ, ρ) =    log p(θi|µ, ρ).          (12)pVMM(θ)                         Xi=1
   .01
                                                         Here,  the parameters  are sought with MATLAB’s
    0                                             fminsearch which uses the Nelder-Mead method [10].
                                                   Other optimization algorithms that are more optimal for
   .04                                                           this problem could be used as well, e.g. the expectation-
                                                     maximization algorithm.  Figure 2 shows examples of
   .03                                                              distributions estimated with both of the models and an
   .02                                              example of the original probability distribution functionpWGM(θ)                                                (PDF), i.e. the normalized histogram of the estimated
   .01                                                          directions.
    0
        -150   -100   -50    0    50   100   150                4. EXPERIMENTAL SETUP
                                θ, [◦]
                                   A microphone array consisting of two four-microphone
 Figure 2:  Examples of the normalized histogram of    grids (see Fig. 1) was used. The four-microphone grids
 the estimated azimuth angles (top, –), the von Mises    share the same center point, having d = 10 mm and
 mixture model (middle, - -), and the wrapped Gaussian   d = 100 mm. The smaller grid is used for the frequen-
 mixture model (bottom, - -), with mixture components    cies from 1 kHz to 5 kHz and the larger for frequencies
                                                   from                                                         100 Hz                                                                        to                                                                   1 kHz.                                                                The bias compensation is done shown        separately                     (–). The vertical                                          lines                                                (–·) illustrate                                                           separately                                                                             for                                                                both                                                                                  arrays. the true                            and                                    estimated                                                source          angle θs =                  −19◦(top),                       The methods were tested with real concert hall data.
 directions ˆθVMM = −23◦(middle), ˆθWGM = −22◦(bot-   The impulse response measurement setup in the concert tom). Source position S3 and receiver position R2 was
                                                                 hall (Pori, located in Finland) is given in Fig. 3. This used (see Sec. 4).
                                                          concert hall has 700 seats and a reverberation time of
                                                      approximately 2.1 seconds. The signals were recorded
                                                           at 48 kHz with three sound source locations (S), and where κ is a measure of concentration, µ is the mean,
                                                    ﬁve receiving (R) locations for the array. Here, the ﬁrst
 and I(0, κ) is the modiﬁed Bessel function of order 0.    three receiver positions are used (R1-R3 in Fig. 3). The The second tested distribution is the wrapped Gaussian
                                                   sound source was an omnidirectional loudspeaker of 26 probability distribution (WG)[9]:
                                         cm diameter, consisting of 12 driver elements.
                    K                      Two source signals, 2 seconds of violin playing a sig-
                     1            −(θ−µ−2πk)2                                                           tone                                                        and                                                                 2 seconds                                                                                           of white                                                                                                    noise,                                                                                        were convolved                                              σ2       ,     (10)    nal
                                                      with                                                              the                                                           measured                                                                         impulse                                                                                       responses.                                                                                     Then,                                                                                                                  signal-to-     fWG(θ|µ, σ) = √2πσ2 k=−KX e
                                                            noise ratio (SNR) was varied by adding white noise (w(t)
 where σ2 is the variance, µ is the mean, and 2K + 1 is    in (1)) to the signals. Next, sound intensity vectors were
 the number of Gaussian to be wrapped, here K = 2.       calculated and compensated as stated in Sec.  2. The
   The mixture model is formulated as the sum of the    direction was estimated from the intensity vectors with
 distributions:                                            the methods introduced in Sec. 3 on a frame by frame
                                                                 basis. Frames with 1024 samples in length and 50 %
               M                                 overlap were used. For each method and test condition,
                                                                 this                                                                 leads                                                                     to                                                                   187                                              = 1683                                                                                           direction                                                                                                   estimates.                                                                                            More-           p(θ|µ, ρ) =                                                                9 ×               mX= 1 amf (m)(θ|µm, ρm),      (11)                                                              over,                                                         8192                                                                      bins                                                              was                                                                        used                                                                                          in the                                                                                                     fast Fourier                                                                                                     transform.
                                                      This implies that the direction was estimated from 837
 where, m indicates the index of a mixture, f = fWG                                                        frequency bins, since the frequency band was from 100
 for the wrapped Gaussian mixture model (WGM), and
                                                           to 5 kHz.
 f = fVM for the von Mises mixture model (VMM). Pa-
 rameters µ = [µ1, µ2, ..., µM] and ρ = [ρ1, ρ2, ..., ρM] de-                                                                  5. RESULTS AND DISCUSSION
 pend also on the model. The weighting factor is here
 selected as am = 1/M and the number of mixtures is    In order to compare the methods, the estimated direc-
M = 2, since there is only a single sound source. Thus,    tions are processed as follows. Firstly, the anomalies are

                                             702

----- [Page 4] -----

                                     CME  MCA  CMD  VMM  WGM
                                                       4

                                                       3
                                                          [◦]
                                                       2
                                                                        µθ,
                                                       1

                                                       0
                                                      20

                                                      15
                                                          [◦]
                                                      10
                                                                        σθ,
Figure 3: Receiver (R) and source (S) positions in the       5
concert hall of Pori. Receiver positions R1, R2, and R3,
and source positions S1, S2, and S3 were used in the       0
experiments.                                                     100
                                                      80
                                                                             [%]removed from the direction estimates. Here, the thresh-      60
old criteria             for an               anomaly                                    is                              30◦,                                               i.e.  if                           >                                                      40                                                                         |ˆθi −θs|                                                    30◦,     PAN,where               true                   angle of                           the                            sound                                        source,                                             the                                                             esti-       θs is the
                                                      20
mate  ˆθi is considered to be an anomaly. The goodness
                                                       0of a method is evaluated with three measures. The ﬁrst                                                            0   5   10  15  20  25  30  35  40
measure is the percentage of anomalies PAN, the sec-                      SNR, [dB]
ond measure is the circular bias of the non-anomalous
estimates ˜θi:                                           Figure 4: Bias (top) and standard deviation (middle) of
                                                        the non-anomalous estimates, as well as the percentage
                   N˜                                 of anomalies (bottom) against SNR. White noise was
                                                     used as the source signal and the reverberation time is             µθ =  arg        ej(˜θi−θs)
                                                   about 2.1 seconds.        Xi=1

and the third is the circular standard deviation:

                   N˜               1/2         VMM is the most robust method against additive
        σθ =  2 1              ej(˜θi−θs)           ,              noise. In Fig. 5, VMM has less than 50 % of anomalies          −1˜N                                                              in all the test conditions. Thus, even with high noise        Xi=1
                                                                  level VMM is able to ﬁnd the distribution caused by
where N˜ is the number of non-anomalous estimates,       the sound source. One reason for this might be that,                                                                                   | · |    although the total energy of the noise is higher thanis the absolute value of a real number and        is the                                                                      || · ||          the energy of the sound source, the distribution causedlength of a complex number.
                                                 by the noise has much smaller concentration than the   The results of the experiments for a white noise
source signal are presented in Fig.  4 and for a violin    distribution caused by the sound source.
source signal in Fig. 5. As expected, since white noise      The bias of all methods is less than 4 ◦in all cases.
has energy in all frequencies it provides more robustness   With noise source the bias increases in general when the
against additive noise and gives more accurate direction  SNR increases.  Thus, the error distribution is biased
estimation results than a violin source signal.           more with high SNR. The reasons behind this unex-
   As one can see from Figs. 4 and 5, the mixture model    pected behaviour are not clear. When the SNR is high
based estimation methods, VMM and WGM, perform    the bias is introduced by the reverberation.  Perhaps,
the best in all conditions, VMM having lowest num-    this is caused by the non-idealities in the microphones.
ber of anomalies in total, and therefore performing the   However, with violin source signal the trend of the bias
best of all the methods. The best estimator from the     is the opposite. The general trend of the standard de-
ﬁrst class (introduced in Sec.  3.1) is CME. However,    viation is that it decreases when the SNR increases, as
the diﬀerences in the performance between the mixture    expected.
model based estimation methods and two simple aver-      As the results indicated, MCA is not a good method
aging methods, CME, and CMD, are not drastical. The    to estimate the direction of arrival from a continuous sig-
worst estimator in all conditions is clearly MCA. Even    nal. MCA gives very often anomalous estimates. This
with the highest SNR the percentage of anomalies is     is caused by the weighting with the radial components,
high (PAN ≈38 %).                                         since when the weighting is not used, as in CME, the
                                             703

----- [Page 5] -----

                                     ACKNOWLEDGEMENTS

                                                 The author wishes to thank Dr.  Tapio Lokki for
     CME  MCA  CMD  VMM WGM
                                                         the supervision of this work. The research leading to
     4
                                                            these results has received funding from the Academy
                                                                 of Finland, project no.  [119092], the European Re-     3
                                                          search Council under the European Community’s Sev-[◦]
     2                                                 enth Framework Programme (FP7/2007-2013) / ERC
 µθ,                                                      grant agreement no.  [203636], and Helsinki Graduate
     1                                                  School in Computer Science and Engineering.

    0                                            References
    20                                                                            [1] J. Merimaa and V. Pulkki,  “Spatial Impulse Re-
                                                            sponse Rendering I: Analysis and Synthesis,”  J.
    15                                                       Audio Eng. Soc., vol. 53, no. 12, pp. 1115–1127,
[◦]                                                              2005.    10
 σθ,                                                                        [2] B. G¨unel, H. Haclhabibo˘glu, and A.M. Kondoz,
     5                                                      “Acoustic Source Separation of Convolutive Mix-
                                                                  tures Based on Intensity Vector Statistics,” IEEE
    0                                                       Trans. Audio, Speech, and Language Processing,
   100                                                                  vol. 16, no. 4, pp. 748–756, 2008.
                                                                            [3] V. Pulkki, “Spatial Sound Reproduction with Di-    80
 [%]                                                                 rectional Audio Coding,” J. Audio Eng. Soc., vol.
    60                                                            55, no. 6, pp. 503–516, 2007.
    40                                                                    [4] J. Merimaa, Analysis, Synthesis and Perception of PAN,                                                                        spatial sound-Binaural Auditory modeling and mul-    20
                                                                 tichannel loudspeaker reproduction,  Ph.D. thesis,
    0
          0   5   10  15  20  25  30  35  40             Helsinki University of Technology, 2006.
                    SNR, [dB]                               [5] J. Chen, J. Benesty, and Y. Huang,  “Time de-
                                                                   lay estimation in room acoustic environments: an
 Figure 5: Bias (top) and standard deviation (middle) of                                                              overview,” EURASIP J. Applied Signal Processing,
 the non-anomalous estimates, as well as the percentage                                                                         vol. 2006, no. 1, pp. 170–170, 2006.
  of anomalies (bottom) against SNR. The source signal
                                                                            [6] M. Kallinger, F. Kuech, R. Schultz-Amling, G. del was violin and the reverberation time is about 2.1 sec-
                                                           Galdo, J. Ahonen, and V. Pulkki, “Enhanced Di- onds.
                                                                  rection Estimation Using Microphone Arrays for
                                                                 Directional Audio Coding,”  in Proc. Hands-Free
                                                             Speech Communication and Microphone Arrays,
 estimation is close to the actual direction. So, at least in        2008, pp. 45–48.
 thecase of circular mean it is not a good idea to use the      [7] N. Madhu and R. Martin, “A Scalable Framework
 radial components as the weighting function. Perhaps,         for Multiple Speaker Localization and Tracking,” in
  if one would select only a certain set of the azimuth        Proc. Int. Workshop on Acoustic Echo and Noise
 and of the radial components one would arrive to bet-         Cancellation, 2008.
  ter result.  Also, one could use a maximum-likelihood      [8] N.I. Fisher,  Statistical Analysis of Circular Data,
 weighting (with respect to the spectrums of the signal      New York: Cambridge University Press, 1993.
 and the noise) for the cross spectral components, as in      [9] Y. Agiomyrgiannakis and Y. Stylianou, “Stochastic
 time delay estimation [5].                                 Modeling and Quantization of Harmonic Phases in
                                                         Speech using Wrapped Gaussian Mixture Models,”
                 6. CONCLUSIONS                          in Proc. Int. Conf. Acoustics, Speech and Signal
                                                                  Processing, 2007, vol. 4, pp. 1121–1124. Five methods for estimating the direction of a sound
                                                                    [10] J.A. Nelder and R. Mead, “A Simplex Method for source from a  set  of sound  intensity  vectors was
                                                           Function Minimization,” The Computer Journal, considered. There were two classes of methods in test.
                                                                         vol. 7, no. 4, pp. 308, 1965. First class includes simple methods such as the circular
 mean, and the second class contains methods that are
 based on convolutive mixture models.  The methods
 were tested in a real concert hall environment.  The
  results indicate that the methods from the second class
 perform better and provide more robustness against
 additive noise than the methods from the ﬁrst class.
 Especially, the von Mises distribution was found to suit
 well for the problem.



                                              704