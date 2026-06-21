---
type: concept
created: 2026-06-21
updated: 2026-06-21
sources:
  - wiki/sources/kaiming-he-2025-neurips-object-detection-history.md
  - https://arxiv.org/pdf/1506.01497
tags:
  - computer-vision
  - object-detection
  - deep-learning
  - region-proposal-network
---

# Faster R-CNN

**Faster R-CNN** (Ren, He, Girshick, Sun, 2015) is an end-to-end [[concepts/object-detection|object detection]] framework that introduced the **Region Proposal Network (RPN)**, unifying region proposal generation and object detection into a single, jointly-trainable network that shares full-image convolutional features. It became the core paradigm of modern object detection and won the **NeurIPS 2025 Test of Time Award**.

## Paper

- **Title**: "Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks"
- **Authors**: Shaoqing Ren, [[entities/kaiming-he|Kaiming He]], Ross Girshick, Jian Sun
- **Year**: 2015 (NeurIPS)
- **arXiv**: [1506.01497](https://arxiv.org/pdf/1506.01497)

## Problem Addressed

Prior detectors relied on external region proposal algorithms (e.g., Selective Search in R-CNN / Fast R-CNN), which were:
- **Slow**: Selective Search took ~2 seconds per image, dominating runtime
- **Decoupled**: proposals were computed externally and not jointly optimized with the detector

## Key Innovation: Region Proposal Network (RPN)

The RPN is a small fully-convolutional network that:
1. Takes the shared convolutional feature map of the full image as input
2. Slides a small network over each spatial location, predicting **k** region proposals (objectness score + box coordinates) at multiple scales/aspect ratios (anchors)
3. Shares the full-image convolutional features with the detection network (Fast R-CNN head)

This makes proposal generation **nearly cost-free** (the expensive convolutions are computed once and shared) and **end-to-end trainable** (proposals and detections are jointly optimized).

## Architecture (Two-Stage)

1. **Shared backbone** (e.g., VGG-16 / ResNet): extracts a convolutional feature map from the full image.
2. **RPN stage**: generates region proposals from the shared feature map via anchors.
3. **Detection stage** (Fast R-CNN head): RoI pooling on the shared features for each proposal → fully-connected layers → class label + refined bounding box.

The two stages alternate during training (alternating optimization / approximate joint training).

## Significance

- **Unified, end-to-end**: eliminated the external proposal algorithm; the whole system became jointly trainable.
- **Speed**: ~5–17 fps depending on backbone, approaching real-time — a dramatic speedup over R-CNN's ~47s/image.
- **Paradigm-defining**: established the two-stage detector paradigm (shared features → RPN → RoI head) that guided a decade of detection research.
- **Test of Time Award**: NeurIPS 2025, recognizing its decade-long impact as "a lighthouse profoundly influencing and guiding the development direction of visual models."

## Evolutionary Context

Faster R-CNN was the culmination of a speed-evolution thread built on **shared computation**:

| Method | Year | Shared Computation |
|--------|------|--------------------|
| R-CNN | 2014 | None (each region through CNN separately) |
| SPP-Net | 2014 | Full-image features computed once, shared across regions |
| Fast R-CNN | 2015 | Shared features + end-to-end detector training |
| **Faster R-CNN** | **2015** | **Shared features with RPN (proposal generation too)** |

## Related Concepts

- [[concepts/object-detection|Object Detection]]

## Related Sources

- [[sources/kaiming-he-2025-neurips-object-detection-history|He 2025: A Brief History of Visual Object Detection (NeurIPS 2025 Talk)]]
