---
type: source
created: 2026-06-21
updated: 2026-06-21
sources:
  - raw/articles/kaiming-he-2025-neurips-object-detection/bilibili-metadata.json
  - raw/articles/kaiming-he-2025-neurips-object-detection/talk-summary.md
  - https://www.bilibili.com/video/BV1nckaBcEra/
  - https://people.csail.mit.edu/kaiming/neurips2025talk/neurips2025_fasterrcnn_kaiming.pdf
  - https://arxiv.org/pdf/1506.01497
tags:
  - computer-vision
  - object-detection
  - deep-learning
  - history
  - talk
  - neurips-2025
  - test-of-time-award
---

# He 2025: A Brief History of Visual Object Detection (NeurIPS 2025 Talk)

**Speaker**: [[entities/kaiming-he|Kaiming He (何恺明)]] — Associate Professor, MIT EECS; Distinguished Scientist, Google DeepMind
**Venue**: NeurIPS 2025, Test of Time Award Presentation
**Talk title**: "A Brief History of Visual Object Detection" (视觉目标检测简史)
**Award context**: Faster R-CNN (Ren, He, Girshick, Sun, 2015) won the NeurIPS 2025 Test of Time Award
**Type**: Conference talk (video recording)
**Slides**: [neurips2025_fasterrcnn_kaiming.pdf](https://people.csail.mit.edu/kaiming/neurips2025talk/neurips2025_fasterrcnn_kaiming.pdf)
**Video**: [Bilibili BV1nckaBcEra](https://www.bilibili.com/video/BV1nckaBcEra/) (uploaded by 京口先生, 2026-01-19, ~26:26, Chinese-English subtitles)

## Summary

A historical review talk by Kaiming He summarizing 30 years of visual [[concepts/object-detection|object detection]], delivered upon Faster R-CNN winning the NeurIPS 2025 Test of Time Award. The talk traces the field through three eras — hand-crafted features, the AlexNet/R-CNN dawn of deep learning, and the Faster R-CNN peak — and highlights that each milestone work it covers has itself won a Test of Time Award at a top venue. The central narrative: feature *learning* decisively replaced feature *engineering*, and a consistent thread of *shared computation* (SPP-Net → Fast R-CNN → Faster R-CNN) drove the speed evolution that made modern real-time detection possible.

> **Note on sourcing**: The video transcript was not directly accessible (Bilibili's subtitle API requires authentication). This page is reconstructed from the Bilibili metadata and a verified reporting article (机器之心 / JiQizhixin, 2025-12-11) covering the talk, cross-checked against Kaiming He's official slides and homepage. Specific attributions below cite the reporting article.

## Talk Content: Three Eras of Object Detection

### Era 1 — Hand-crafted "Magnifying Glasses" (1990s–2008)

Before deep learning, CV scientists were "craftsmen" designing features by hand.

**Early face detection**:
- **1996 — Rowley et al., "Neural Network-Based Face Detection"**: The first CV paper Kaiming He ever read; early neural networks searching image pyramids for faces.
- **1997 — Osuna et al., "SVM for Face Detection"**: Introduced SVMs to draw a face/non-face classification boundary.
- **2001 — Viola-Jones Framework**: Extremely fast face detection via simple Haar-like features + cascade classifier; still powers autofocus in many older cameras.

**Golden age of feature engineering**:
- **1999 — Lowe, SIFT**: Scale-invariant feature transform; recognized objects under rotation and scaling.
- **2003 — Sivic & Zisserman, Bag of Visual Words**: Borrowed from text search; images as collections of "visual words."
- **2005 — Dalal & Triggs, HOG**: Histogram of oriented gradients for pedestrian contours. (Same year: Grauman & Darrell, Pyramid Match Kernel.)
- **2006 — Lazebnik et al., Spatial Pyramid Matching**: Restored spatial location info lost in bag-of-words.
- **2008 — DPM (Deformable Part Model)**: The culmination of feature engineering — objects as spring-connected deformable parts. The peak of traditional methods.

**Pain point**: Hand-crafted features + classifiers (e.g., SVM) were slow and hard to adapt to complex scenes.

### Era 2 — Dawn: AlexNet and R-CNN (2012–2014)

- **2012 — AlexNet (Krizhevsky et al.)**: Landslide ImageNet win; proved deep CNNs extract features far better than hand-crafted methods.
- **2014 — R-CNN (Girshick et al.)**: The bridge from classification to detection — Selective Search cuts ~2000 region proposals, each run through a CNN, then classified by an SVM.

### Era 3 — Peak: Faster R-CNN's Speed Evolution (2014–2015)

R-CNN ran each candidate box through the CNN separately — huge computation. The drive to reuse computation defined this era:

- **2014 — SPP-Net (He et al.)**: Spatial pyramid pooling layer allowed arbitrary image sizes and computed full-image features only once.
- **2015 — Fast R-CNN (Girshick)**: End-to-end detector training with shared convolutional features.
- **2015 — [[concepts/faster-r-cnn|Faster R-CNN]] (Ren, He, Girshick, Sun)**: Introduced the **Region Proposal Network (RPN)**, making proposal generation nearly cost-free by sharing full-image convolutional features with the detection network. This unified, end-to-end framework became the core paradigm of modern object detection — a "lighthouse" guiding a decade of visual model development. Won the NeurIPS 2025 Test of Time Award.

### Later Arc

- **2017 — Mask R-CNN (He et al.)**: Extended Faster R-CNN to instance segmentation with a mask prediction branch; ICCV 2017 Best Paper.

## Key Takeaways

1. **Three paradigms**: hand-crafted features + classifiers → CNN-based region classification → end-to-end proposal + detection networks.
2. **Faster R-CNN's RPN was the unifying breakthrough**: sharing convolutional features between proposal generation and detection made the framework fast and end-to-end trainable, defining the modern paradigm.
3. **Feature learning replaced feature engineering**: the central lesson of 30 years — learned representations (AlexNet onward) decisively outperformed hand-crafted descriptors (SIFT/HOG/DPM).
4. **Shared computation as the speed thread**: SPP-Net (share features across regions) → Fast R-CNN (share across head) → Faster R-CNN (share with RPN) — consistent computational reuse driving speed gains.

## Related Concepts

- [[concepts/object-detection|Object Detection]]
- [[concepts/faster-r-cnn|Faster R-CNN]]

## Related Entities

- [[entities/kaiming-he|Kaiming He]]
