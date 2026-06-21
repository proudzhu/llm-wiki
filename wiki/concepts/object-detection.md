---
type: concept
created: 2026-06-21
updated: 2026-06-21
sources:
  - wiki/sources/kaiming-he-2025-neurips-object-detection-history.md
tags:
  - computer-vision
  - object-detection
  - deep-learning
---

# Object Detection

**Object detection** is the computer vision task of localizing and classifying objects in images or video — producing both bounding boxes (where) and category labels (what) for each object instance. It is distinguished from image classification (which assigns a single label to the whole image) and instance segmentation (which produces pixel-level masks).

## Overview

Object detection evolved over ~30 years through three paradigms, as surveyed in Kaiming He's NeurIPS 2025 talk "A Brief History of Visual Object Detection":

### Era 1 — Hand-crafted Features + Classifiers (1990s–2008)

Detection relied on manually designed feature descriptors fed into classifiers (e.g., SVM):

| Year | Method | Contribution |
|------|--------|--------------|
| 1996 | Rowley et al. | Neural network-based face detection on image pyramids |
| 1997 | Osuna et al. | SVM for face detection |
| 2001 | Viola-Jones | Haar-like features + cascade classifier; real-time face detection |
| 1999 | SIFT (Lowe) | Scale-invariant feature transform |
| 2003 | Bag of Visual Words | Text-search-inspired image representation |
| 2005 | HOG (Dalal & Triggs) | Histogram of oriented gradients for pedestrians |
| 2006 | Spatial Pyramid Matching | Restored spatial info in bag-of-words |
| 2008 | DPM | Deformable part model — peak of traditional methods |

**Limitation**: Hand-crafted features were slow and hard to adapt to complex scenes.

### Era 2 — CNN-Based Region Classification (2012–2014)

- **2012 — AlexNet**: Deep CNNs proved to extract features far better than hand-crafted methods.
- **2014 — R-CNN (Girshick et al.)**: Selective Search → ~2000 region proposals → each through a CNN → SVM classification. Bridged classification to detection but was computationally expensive (each region processed separately).

### Era 3 — End-to-End Proposal + Detection Networks (2014–2017)

A consistent thread of **shared computation** drove the speed evolution:

- **2014 — SPP-Net (He et al.)**: Spatial pyramid pooling allowed arbitrary image sizes and computed full-image features once (shared across regions).
- **2015 — Fast R-CNN (Girshick)**: End-to-end detector training with shared convolutional features.
- **2015 — [[concepts/faster-r-cnn|Faster R-CNN]] (Ren, He, Girshick, Sun)**: Region Proposal Network (RPN) sharing features with the detection head — unified, end-to-end, fast. Became the modern paradigm; won NeurIPS 2025 Test of Time Award.
- **2017 — Mask R-CNN (He et al.)**: Extended to instance segmentation with a mask branch; ICCV 2017 Best Paper.

## Key Lessons

1. **Feature learning replaced feature engineering**: learned representations (AlexNet onward) decisively outperformed hand-crafted descriptors.
2. **Shared computation drives speed**: reusing convolutional features across regions, the detection head, and proposal generation was the central architectural insight.
3. **End-to-end training unifies the pipeline**: Faster R-CNN's RPN eliminated the external proposal algorithm, making the whole system jointly trainable.

## Related Concepts

- [[concepts/faster-r-cnn|Faster R-CNN]]

## Related Sources

- [[sources/kaiming-he-2025-neurips-object-detection-history|He 2025: A Brief History of Visual Object Detection (NeurIPS 2025 Talk)]]
