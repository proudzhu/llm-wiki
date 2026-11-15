---
type: concept
created: 2026-11-15
updated: 2026-11-15
sources:
  - raw/papers/ronneberger-2015-u-net/full-text.md
tags:
  - data-augmentation
  - biomedical-imaging
  - segmentation
  - u-net
---

# Elastic Deformation Augmentation

**Elastic deformation augmentation** is a training-time data augmentation that warps each sample by a smooth, random, non-rigid deformation field. Ronneberger et al. (2015) identify it as the key ingredient that lets a segmentation network train on 20–30 annotated images: in biomedical tissue, deformation *is* the dominant nuisance variation, so simulating realistic deformations teaches the invariance without needing to collect examples of it.

## Procedure

1. Sample random displacement vectors on a **coarse grid** — the U-Net paper uses a 3×3 grid — from a Gaussian with standard deviation **10 pixels**.
2. Interpolate the displacement field to per-pixel resolution by **bicubic interpolation**, yielding a smooth (low-frequency) warp.
3. Warp the image and the label map with the same field.

The coarse grid is what makes the deformation *smooth and anatomically plausible*: per-pixel independent displacements would produce high-frequency noise that no tissue exhibits. The same warp applied to image and mask keeps supervision consistent.

## Why it matters

| Augmentation | Teaches | Cost |
|:---|:---|:---|
| Shift / rotation | Global pose invariance | Cheap, but already nearly satisfied by pooling and convolution |
| Elastic deformation | Invariance to the **shape variation** of real tissue | A resampling per sample; no extra annotation |
| Dropout (end of contracting path) | Further implicit regularization | Free |

The U-Net paper pairs elastic warping with dropout at the end of the contracting path, describing dropout as *implicit* augmentation.

## Related Concepts

- [[concepts/u-net|U-Net]]
- [[concepts/boundary-weighted-loss|Boundary-Weighted Loss]]

## Related Sources

- [[sources/ronneberger-2015-u-net|Ronneberger, Fischer & Brox 2015: U-Net]]
