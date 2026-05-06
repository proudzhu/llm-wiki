# US20260073929A1: Bone Conducted Signal Guided Speech Enhancement for Voice Assistant on Earbuds

**Patent Number**: US20260073929A1
**Assignee**: Google LLC
**Filing Date**: 2025-07-25
**Publication Date**: 2026-03-12
**Application Number**: US19281540
**Priority**: U.S. Provisional Application 63/694,101 (filed Sep. 12, 2024)

**Inventors**: Jens Heitkaemper, Joseph Peter Caroselli Jr., Max McKinnon, Arun Narayanan, Nathan David Howard

## Cross Reference to Related Applications

[0001] This U.S. patent application claims priority under 35 U.S.C. § 119(e) to U.S. Provisional Application 63/694,101, filed on Sep. 12, 2024.

## Technical Field

[0002] This disclosure relates to bone conducted signal guided speech enhancement for a voice assistant on earbuds.

## Background

[0003] The widespread adoption of voice assistants has made automatic speech recognition (ASR) systems increasingly prevalent. ASR systems transcribe spoken language into text, enabling users to interact with devices using voice commands. While ASR technology has improved significantly, achieving robust performance in real-world scenarios remains a critical challenge. In particular, performance degradation occurs in environments characterized by low signal-to-noise ratios (SNR), where the desired speech signal is weak relative to background noise. Further complications arise from overlapping speech, where multiple speakers are talking simultaneously. Sources of interfering sounds may include anything from ambient noises like traffic or appliance sounds, to music, or the voices of other people. These adverse acoustic conditions obscure or distort the voice of the target speaker, leading to significant errors in transcription and frustrating user experience, ultimately limiting the usability and reliability of voice-controlled devices.

## Summary

[0004] One aspect of the disclosure provides a bone conducted signal-guided speech enhancement model for speech recognition. The speech enhancement model includes a stack of self-attention blocks each having a multi-head self attention mechanism. The stack of self-attention blocks is configured to: receive as input, at an initial block of the stack of self-attention blocks, an input concatenating short-time Fourier transform (STFT) coefficients for a single channel noisy input signal and upscaled STFT coefficients of a bone conducted signal (BCS) recorded by an accelerometer, and generate, as output from a final block of the stack of self-attention blocks, an un-masked output. The enhancement model includes a masking layer configured to receive, as input, the un-masked output generated as output from the final block of the stack of self-attention blocks and generate, as output, a masked single channel noisy input signal. The speech enhancement model includes an inverse STFT layer configured to receive, as input, the STFT coefficients for the single channel noisy input signal and the masked single-channel noisy input signal and generate, as output, enhanced input speech features corresponding to a target utterance.

[0005] Implementations of the disclosure may include one or more of the following optional features. In some implementations, the speech enhancement model includes a feed forward upscaling projection layer configured to receive band-limited STFT coefficients of the BCS as input and generate the upscaled STFT coefficients of the BCS as output. In these implementations, the speech enhancement model may include a down sampling block configured to receive, as input, STFT coefficients of the BCS recorded by the accelerometer and a maximum frequency bin value for sampling the BCS and generate, as output, the band-limited STFT coefficients of the BCS. Here, the down sampling block may generate the band-limited STFT coefficients of the BCS by multiplying the maximum frequency bin value by a factor of two to reduce a sampling rate of the STFT coefficients of the BCS. The feed forward upscaling projection layer, the stack of self-attention blocks, and the masking layer of the speech enhancement model are fine-tuned using a spectral loss based on an L1 loss function and L2 loss function distance between an estimated ratio mask and an ideal ratio mask and an automatic speech recognition (ASR) loss. The ASR loss is computed by generating, using an ASR encoder configured to receive enhanced speech features predicted by the speech enhancement model for a training utterance as input, predicted outputs of the ASR encoder for the enhanced speech features, generating, using the ASR encoder configured to receive target speech features for the training utterance as input, target outputs of the ASR encoder for the target speech features, and computing the ASR loss based on the predicted outputs of the ASR encoder for the enhanced speech features and the target outputs of the ASR encoder for the target speech features.

[0006] In some examples, the stack of self-attention blocks and the masking layer of the speech enhancement model are pretrained using a spectral loss based on an L1 loss function and L2 loss function distance between an estimated ratio mask and an ideal ratio mask and an ASR loss. The ideal ratio mask is computed using reverberant speech and reverberant noise. The ASR loss is computed by generating, using an ASR encoder configured to receive enhanced speech features predicted by the speech enhancement model for a training utterance as input, predicted outputs of the ASR encoder for the enhanced speech features, generating, using the ASR encoder configured to receive target speech features for the training utterance as input, target outputs of the ASR encoder for the target speech features, and computing the ASR loss based on the predicted outputs of the ASR encoder for the enhanced speech features and the target outputs of the ASR encoder for the target speech features. The stack of self-attention blocks may include a stack of Conformer blocks.

[0007] In some implementations, the speech enhancement model executes on data processing hardware residing on a user device in communication with an earbud device. The earbud device is configured to capture the target utterance via an array of microphones of the earbud device. In these implementations, the speech enhancement model may be agnostic to number of microphones in the array of microphones. In some examples, an ASR model is configured to process the enhanced input speech features corresponding to the target utterance. In these examples, a pre-trained voice activity detector (VAD) is configured to receive, as input, the BCS recorded by the accelerometer and generate, as output, an estimated speech detection value. Here, the ASR model may be configured to not process the enhanced input speech features and instead process the single channel noisy input signal when the estimated speech detection value generated as output from the VAD does not satisfy the threshold value.

## Description of Drawings

[0013] FIG. 1 is a schematic view of an example system executing a speech recognition system that performs speech enhancement.
[0014] FIGS. 2A and 2B are schematic views of an example speech recognition model.
[0015] FIG. 3 is a schematic view of an example speech enhancement model.
[0016] FIG. 4 is a schematic view of an example training process for training the speech enhancement model.
[0017] FIG. 5 is a flowchart of an example arrangement of operations for a computer-implemented method of performing speech enhancement.
[0018] FIG. 6 is a schematic view of an example computing device that may be used to implement the systems and methods described herein.

## Detailed Description

[0020] The increasing popularity of digital assistants has led to a surge in the use of automatic speech recognition (ASR) systems, which convert spoken language into text. This technology enables users to interact with various devices via voice commands, with earbuds emerging as a prevalent interface for digital assistants. However, the performance of ASR systems degrades significantly in the presence of noise. Environments with low signal-to-noise ratios (SNR), where background noise is substantial relative to the speech signal, cause a drop in ASR performance. Overlapping speech, instances where multiple individuals speak concurrently, also presents challenges.

[0021] These challenging acoustic environments, characterized by low SNR and/or overlapping speech, may severely degrade ASR performance. The presence of noise causes the acoustic signal of the voice of the target speaker to be obscured, distorted, or masked. This interference results in significant errors during the transcription process.

[0022] Accordingly, implementations herein are directed towards a bone conducted signal-guided speech enhancement model that includes a stack of self-attention blocks. The stack of self-attention blocks is configured to receive, as input, an input concatenating short-form Fourier transform (STFT) coefficients for a single channel noisy input signal (i.e., air conducted signal) and upscaled STFT coefficients of a bone conducted (BCS) recorded by an accelerometer and generate an un-masked output. The STFT coefficients of the single channel noisy input signal represent the time-frequency representation of the audio signal captured by a microphone, which includes both the target speech and any background noise. The STFT coefficients of the BCS signal similarly represent the time-frequency representation of the vibrations sensed by the accelerometer, which are primarily caused by the speech spoken by the user. The speech enhancement model includes a masking layer configured to receive, as input, the un-masked output and generate a masked single channel noisy input signal. The speech enhancement model includes an inverse STFT layer configured to generate enhanced input speech features corresponding to a target utterance.

### System Architecture (FIG. 1)

[0023] A system 100 includes a remote computing system 140 in communication with one or more user devices 110 each associated with a respective user 10 via a network 130. The remote computing system 140 may be a distributed system (e.g., a cloud environment) having computing resources 142 and storage resources 144.

[0025] The user device 110 may be in communication with an earbud device 120, which may include earbuds, headphones, or any other listening device designed to be worn in or around the user's ear. The earbud device 120 includes an array of microphones 122 configured to capture a target utterance 106 spoken by the user 10. The earbud device 120 may convert the target utterance 106 into a single channel noisy input signal 104 (air-conducted signal).

[0026] The earbud device 120 includes one or more accelerometers 124 configured to measure bone conduction signals (BCS) 102. Each accelerometer 124 may be positioned to detect vibrations of the user's skull caused by vocal chord activity. This configuration allows the accelerometer 124 to directly capture the target utterance 106, resulting in a signal that is less susceptible to interference from environmental sounds.

### Speech Enhancement Model (FIG. 3)

[0032] The speech enhancement model 300 includes a down-sampling block 310, a feed-forward upscaling projection layer 320, a stack of self-attention blocks 330 (Conformer blocks), a masking layer 340, and an inverse STFT layer 350.

[0033] The down-sampling block 310 receives STFT coefficients of the BCS 102 and a maximum frequency bin value for sampling the BCS. The down-sampling block 310 generates band-limited STFT coefficients of the BCS by multiplying the maximum frequency bin value by a factor of two to reduce the sampling rate.

[0034] The feed-forward upscaling projection layer 320 receives the band-limited STFT coefficients of the BCS and generates upscaled STFT coefficients of the BCS. The upscaling projection layer projects the band-limited BCS features into a higher-dimensional space to match the dimensionality of the air-conducted signal features.

[0035] The stack of self-attention blocks 330 receives as input a concatenation of the STFT coefficients for the single channel noisy input signal 104 and the upscaled STFT coefficients of the BCS 102. The stack of self-attention blocks 330 processes this concatenated input through multiple Conformer blocks, each having a multi-head self-attention mechanism, to generate an un-masked output.

[0036] The masking layer 340 receives the un-masked output and generates a masked single channel noisy input signal (i.e., an estimated ratio mask). The masking layer applies the estimated ratio mask to the original STFT coefficients.

[0037] The inverse STFT layer 350 receives the STFT coefficients for the single channel noisy input signal and the masked single channel noisy input signal, and generates enhanced input speech features corresponding to a target utterance by applying the inverse STFT.

### Training Process (FIG. 4)

[0040] The speech enhancement model is trained in two stages: pre-training and fine-tuning.

**Pre-training**: The stack of self-attention blocks 330 and the masking layer 340 are pretrained using:
- A spectral loss based on L1 and L2 loss function distance between an estimated ratio mask and an ideal ratio mask
- The ideal ratio mask is computed using reverberant speech and reverberant noise
- An ASR loss computed by comparing ASR encoder outputs for enhanced speech features vs. target speech features

**Fine-tuning**: The feed-forward upscaling projection layer 320, the stack of self-attention blocks 330, and the masking layer 340 are fine-tuned using:
- The same spectral loss (L1 + L2 on ratio masks)
- The same ASR loss
- This stage additionally trains the BCS upscaling pathway

### VAD-Gated Processing

[0050] A pre-trained voice activity detector (VAD) receives the BCS recorded by the accelerometer and generates an estimated speech detection value. The ASR model processes the enhanced input speech features when the VAD output satisfies a threshold value. When the VAD does not detect speech, the ASR model instead processes the single channel noisy input signal directly (bypassing enhancement).

### Key Design Features

1. **Single-channel air + BCS fusion**: Concatenates STFT of single-channel noisy mic signal with upscaled BCS STFT in a Conformer-based architecture
2. **BCS upscaling pathway**: Down-sampling block reduces BCS bandwidth; feed-forward projection upscales to match air-conducted signal dimensionality
3. **Mic-agnostic**: Model is agnostic to the number of microphones in the earbud array
4. **Two-stage training**: Pre-train on spectral + ASR loss; fine-tune with BCS upscaling pathway included
5. **VAD gating**: BCS-based VAD determines whether to use enhanced or raw signal for ASR
6. **Ratio mask estimation**: Model estimates an ideal ratio mask applied to the original STFT, then uses iSTFT for waveform reconstruction

## Claims

### Claim 1
A speech enhancement model comprising: a stack of self-attention blocks each having a multi-head self attention mechanism, the stack of self-attention blocks configured to receive as input, at an initial block, an input concatenating STFT coefficients for a single channel noisy input signal and upscaled STFT coefficients of a bone conducted signal (BCS) recorded by an accelerometer, and generate, as output from a final block, an un-masked output; a masking layer configured to receive the un-masked output and generate a masked single channel noisy input signal; and an inverse STFT layer configured to receive the STFT coefficients for the single channel noisy input signal and the masked single-channel noisy input signal and generate enhanced input speech features corresponding to a target utterance.

### Claim 9
A computer-implemented method executed on data processing hardware that causes the data processing hardware to perform operations for speech enhancement, the operations comprising: receiving, as input to an initial block of a stack of self-attention blocks of a speech enhancement model, an input concatenating STFT coefficients for a single channel noisy input signal and upscaled STFT coefficients of a BCS recorded by an accelerometer; generating, using a final block, an un-masked output; generating, using a masking layer, a masked single channel noisy input signal; and generating, using an inverse STFT layer, enhanced input speech features corresponding to a target utterance.

### Claim 17
A speech enhancement model comprising: a feed forward upscaling projection layer configured to receive band-limited STFT coefficients of a BCS and generate upscaled STFT coefficients of the BCS; a down sampling block configured to receive STFT coefficients of the BCS and a maximum frequency bin value and generate band-limited STFT coefficients of the BCS; a stack of Conformer blocks configured to receive a concatenation of STFT coefficients for a single channel noisy input signal and the upscaled STFT coefficients of the BCS and generate an un-masked output; a masking layer configured to generate a masked single channel noisy input signal; and an inverse STFT layer configured to generate enhanced input speech features.

## Source

- URL: https://patents.google.com/patent/US20260073929A1/en
- Zotero: Q833LYDX
