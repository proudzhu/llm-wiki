# A Brief History of Visual Object Detection — Kaiming He (NeurIPS 2025)

**Source**: Bilibili video BV1nckaBcEra, uploaded by 京口先生 (2026-01-19), with original Chinese-English subtitles.
**Original talk**: "A Brief History of Visual Object Detection", Test of Time Award Presentation, NeurIPS 2025.
**Speaker**: Kaiming He (何恺明), Associate Professor, MIT EECS; Distinguished Scientist, Google DeepMind.
**Slides**: https://people.csail.mit.edu/kaiming/neurips2025talk/neurips2025_fasterrcnn_kaiming.pdf
**Context**: Faster R-CNN (Ren, He, Girshick, Sun, 2015) won the NeurIPS 2025 Test of Time Award. This talk was Kaiming He's award presentation summarizing 30 years of visual object detection. Each work highlighted in the talk has won a Test of Time Award at a top venue.

> Note: This summary is reconstructed from the Bilibili metadata and a verified reporting article (机器之心 / JiQizhixin, 2025-12-11) covering the talk. The video transcript was not directly accessible (Bilibili subtitle API requires authentication). Direct quotes are attributed to the reporting article.

## Talk Structure: 30 Years of Object Detection

### Era 1 — Primitive: Hand-crafted "Magnifying Glasses" (1990s–2008)

Before deep learning, computer vision scientists were "craftsmen" designing features by hand.

**Early face detection attempts**:
- **1996 — Rowley et al., "Neural Network-Based Face Detection"**: The first CV paper Kaiming He ever read. Used early neural networks to search for faces in image pyramids.
- **1997 — Osuna et al., "SVM for Face Detection"**: Introduced support vector machines to draw a classification boundary for face detection.
- **2001 — Viola-Jones Framework**: Achieved extremely fast face detection through simple feature combinations (Haar-like features + cascade classifier). Still used in many old cameras' autofocus today.

**Golden age of feature engineering** (find "key points" and "textures" rather than whole objects):
- **1999 — Lowe, SIFT (Scale-Invariant Feature Transform)**: Recognized objects under rotation and scaling; the "absolute king" of its era.
- **2003 — Sivic & Zisserman, "Bag of Visual Words"**: Borrowed from text search; treated images as collections of "visual words."
- **2005 — Dalal & Triggs, HOG (Histogram of Oriented Gradients)**: Described pedestrian contours. Same year: Grauman & Darrell, "Pyramid Match Kernel" for comparing feature-set similarity.
- **2006 — Lazebnik et al., "Spatial Pyramid Matching"**: Solved the bag-of-words model's loss of spatial location information.
- **2008 — DPM (Deformable Part Model)**: The culmination of feature engineering. Modeled objects as deformable parts (head, hands, feet) connected like springs. The peak of traditional methods.

**Pain point**: Features were hand-crafted; classifiers (e.g., SVM) could only work with this limited information. Slow and hard to adapt to complex scenes.

### Era 2 — Dawn: AlexNet and R-CNN's "Brute-Force Aesthetics" (2012–2014)

- **2012 — AlexNet (Krizhevsky et al.)**: Won ImageNet by a landslide. Proved deep CNNs extract features far better than hand-crafted methods.
- **2014 — R-CNN (Girshick et al.)**: The groundbreaking bridge from classification to detection:
  1. Use Selective Search to cut ~2000 candidate regions (region proposals) from the image
  2. Run each region through a CNN to extract features
  3. Classify with an SVM

### Era 3 — Peak: Faster R-CNN's "Speed Evolution" (2014–2015)

R-CNN ran each candidate box through the CNN separately — huge computation. Researchers sought to reuse computation.

- **2014 — SPP-Net (He et al.), Spatial Pyramid Pooling**: Introduced a spatial pyramid pooling layer allowing the network to handle arbitrary image sizes and compute full-image features only once, greatly accelerating detection.
- **2015 — Fast R-CNN (Girshick)**: End-to-end training of the detector; shared convolutional features.
- **2015 — Faster R-CNN (Ren, He, Girshick, Sun)**: Introduced the Region Proposal Network (RPN), making region proposal generation nearly cost-free by sharing full-image convolutional features with the detection network. This unified, end-to-end framework became the core paradigm of modern object detection and a "lighthouse" guiding a decade of visual model development. Won the NeurIPS 2025 Test of Time Award.

### Later developments (referenced in the talk's broader arc)

- **2017 — Mask R-CNN (He et al.)**: Extended Faster R-CNN to instance segmentation by adding a mask prediction branch. Won ICCV 2017 Best Paper.
- The talk frames each milestone as a Test-of-Time-Award-winning contribution that played a decisive role in visual intelligence.

## Key Takeaways

1. **Object detection evolved through three paradigms**: hand-crafted features + classifiers → CNN-based region classification → end-to-end region proposal + detection networks.
2. **Faster R-CNN's RPN was the unifying breakthrough**: sharing convolutional features between proposal generation and detection made the framework both fast and end-to-end trainable, defining the modern paradigm.
3. **Feature learning replaced feature engineering**: the central lesson of 30 years — learned representations (AlexNet onward) decisively outperformed hand-crafted descriptors (SIFT/HOG/DPM).
4. **Each milestone built on shared computation**: SPP-Net (share features across regions) → Fast R-CNN (share features across head) → Faster R-CNN (share features with RPN) — a consistent thread of computational reuse driving speed gains.

## References

- Talk slides (PDF): https://people.csail.mit.edu/kaiming/neurips2025talk/neurips2025_fasterrcnn_kaiming.pdf
- Faster R-CNN paper: https://arxiv.org/pdf/1506.01497 (Ren, He, Girshick, Sun, 2015)
- Reporting article: 机器之心 (JiQizhixin), "何恺明NeurIPS 2025演讲盘点：视觉目标检测三十年", 2025-12-11
- Kaiming He homepage: http://people.csail.mit.edu/kaiming/
