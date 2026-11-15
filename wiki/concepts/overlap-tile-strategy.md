---
type: concept
created: 2026-11-15
updated: 2026-11-15
sources:
  - raw/papers/ronneberger-2015-u-net/full-text.md
tags:
  - segmentation
  - image-processing
  - inference-strategy
  - u-net
---

# Overlap-Tile Strategy

The **overlap-tile strategy** is an inference scheme for segmenting images larger than the network's input tile. Each output tile is predicted from an input tile that is **larger on every side** than the region being predicted; the extra margin supplies the context the valid convolutions would otherwise consume, and only the interior ("valid") region of each prediction is kept. Missing image data outside the true image boundary is **extrapolated by mirroring**.

## Mechanics

For a network with $L$ pooling levels and valid convolutions, a tile of side $S$ produces an output of side $S - 4L$ (each 3×3 valid conv eats 2 pixels per side; two convs per level plus pooling alignment). To predict an interior block $B$ and lose nothing, feed a tile of side $B + 4L$ centred on $B$, with the surrounding pixels taken from the image where available and from a **mirror reflection** of the image edge where not.

Consequence: the segmentation map can be stitched **seamlessly** — adjacent output tiles agree on their shared border because each saw real (or mirrored) context rather than padding zeros. This removes the tile-boundary artifacts that zero-padding produces.

A second, structural constraint: the input tile size must be chosen so that every 2×2 max-pool operates on a layer with **even** x- and y-size; otherwise the pooling grid shifts relative to the output grid and tiles cannot be aligned.

## Comparison

| Approach | Boundary handling | Artifact |
|:---|:---|:---|
| Zero-pad to tile size | Zeros are out-of-distribution context | Darkened / mis-segmented frame |
| Mirror extrapolation (this) | Reflect the edge | None visible; the network sees plausible continuation |
| Predict whole image | Requires image ≤ tile | Not scale-free |

## Related Concepts

- [[concepts/u-net|U-Net]] — the architecture the strategy was introduced with, in the context of EM stacks and arbitrary-size microscopy images

## Related Sources

- [[sources/ronneberger-2015-u-net|Ronneberger, Fischer & Brox 2015: U-Net]]
