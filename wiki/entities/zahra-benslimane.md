---
type: entity
created: 2026-07-10
updated: 2026-07-16
tags:
  - researcher
  - speech-enhancement
  - binaural
  - hearing-aid
  - distributed
  - quantization
  - model-compression
---

# Zahra Benslimane

**Zahra Benslimane** is a researcher at CEA, List (Université Paris-Saclay), France, affiliated also with Université de Lorraine, CNRS, Inria, LORIA. She is the lead author of the [[concepts/tango-framework|Tango]]-family compression line ([[concepts/mn-tango|MN-TANGO]], RT-Tango) for resource-constrained binaural hearing-aid deployment.

## Research Areas

- Distributed binaural speech enhancement
- Real-time and low-latency speech enhancement for hearing aids
- Efficient neural network architectures for resource-constrained devices
- Neural-network quantization (QAT, DPTQ) for hybrid neural-spatial SE
- Model compression (ERB, grouped RNN, INT8)

## Notable Contributions

- RT-Tango: real-time distributed binaural speech enhancement for low-power hearing aid devices (arXiv 2026, lead author)
- Quantized TANGO / MN-TANGO: low-precision inference for a hybrid distributed binaural SE system; simplifies Tango into MN-TANGO and combines W8A8 QAT with ERB and grouped LSTM to reach 4.65 MMAC/s and 0.177 MB (arXiv 2026, lead author)
- Multichannel Speech Enhancement Under Low-Latency Constraints: Balancing Quality And Computational Cost (EEAI 2025)

## Affiliations

- Université Paris-Saclay, CEA, List, F-91120 Palaiseau, France
- Université de Lorraine, CNRS, Inria, LORIA, F-54000 Nancy, France

## Related Concepts

- [[concepts/distributed-binaural-speech-enhancement|Distributed Binaural Speech Enhancement]]
- [[concepts/tango-framework|Tango Framework]]
- [[concepts/mn-tango|MN-TANGO]]
- [[concepts/grouped-recurrent-neural-network|Grouped Recurrent Neural Network]]
- [[concepts/quantization-aware-training|Quantization-Aware Training (QAT)]]
- [[concepts/post-training-quantization|Post-Training Quantization (DPTQ)]]
- [[concepts/gevd-spatial-filtering|GEVD-Based Spatial Filtering]]
- [[concepts/asymmetric-stft|Asymmetric STFT]]
- [[concepts/erb-scale|ERB Scale]]

## Related Sources

- [[sources/benslimane-2026-rt-tango-binaural-speech-enhancement|Benslimane et al. 2026: RT-Tango]]
- [[sources/benslimane-2026-tango-quantized-distributed|Benslimane et al. 2026: Quantized TANGO / MN-TANGO]]
