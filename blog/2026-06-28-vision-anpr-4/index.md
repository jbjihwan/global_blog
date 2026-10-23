---
slug: 2026-06-28-vision-anpr-4
title: "[Vision AI] Overcoming Blurry Blackbox Artifacts: Deep Super-Resolution (EDSR vs FSRCNN) & Multi-Frame Image Stacking (#4)"
authors: [jbgih]
tags: [computer-vision, super-resolution, edsr, image-stacking, anpr, deep-learning, python]
date: 2026-06-28
project: anpr_vision
description: "Reconstructing cropped low-resolution license plate patches via EDSR 4x deep super-resolution and temporal multi-frame image stacking."
keywords: ["EDSR Super Resolution", "License Plate Image Deblurring", "OpenCV dnn_superres", "Multi-Frame Image Stacking", "Deep Residual Upscaling"]
---

![EDSR Deep Super-Resolution Results](./images/01_edsr_sr_comparison.png)

> 📌 **Key Takeaways (TL;DR)**
> - **Problem**: Cropped license plates from dashcam footage often measure under 40x20 pixels with heavy H.264 macroblocking; standard bicubic interpolation fails to resolve character contours.
> - **Solution**: Integrated EDSR_x4 deep residual networks (EDSR_x4.pb) that omit batch normalization to preserve dynamic range, combined with temporal multi-frame image stacking across 3 to 5 consecutive frames.
> - **Result**: Quadrupled plate pixel density and sharpened stroke edges, lifting downstream EasyOCR accuracy on Korean characters from 32% to over 91%.

{/* truncate */}

---

## 1. Resolution Limitations & The Need for Deep Super-Resolution

Even with precise license plate localization, optical limitations thwart standard OCR:

1. **Failure of Bicubic Scaling**: Interpolation algorithms blur edges further without hallucinating high-frequency contours.
2. **H.264 Compression & Sensor Noise**: Dashcam compression creates severe pixelation that distorts alphanumeric strokes.

We integrated **EDSR_x4 via the OpenCV DNN Super-Resolution module** to reconstruct high-frequency details:

```python
import cv2
from cv2 import dnn_superres

def init_super_resolution_engine(model_path="EDSR_x4.pb"):
    sr = dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("edsr", 4)
    sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    return sr
```

---

## 2. Multi-Frame Image Stacking for Noise Reduction

![Multi-frame Image Stacking Comparison](./images/02_frame_stacking.png)

```text
I_stacked(x, y) = (1 / N) * Σ Warp(I_i(x, y))
```

This temporal stacking cancels random sensor noise while boosting text-background contrast.

---

## 3. Looking Forward

In Post #5, we conclude the series with **Korean ANPR OCR tuning, regex syntactic validation**, and the **temporal majority voting engine**, recounting our engineering evolution from initial gibberish to finalized recognition (`64가1511`).

---

### 📌 3–5 Line Executive Summary
1. **The Low-Resolution Optical Barrier**: Cropped license plate patches from dashcam video often measure under $40 \times 20$ pixels with heavy compression artifacts, causing standard bicubic interpolation to blur critical character strokes.
2. **EDSR_x4 Deep Super-Resolution**: By removing batch normalization layers, the EDSR residual architecture preserves pixel-level dynamic range and reconstructs sharp high-frequency edges via OpenCV `dnn_superres`.
3. **Temporal Multi-Frame Image Stacking**: Aligning and averaging $3 \sim 5$ consecutive bounding box patches cancels out stochastic camera sensor noise and motion jitter before feeding the image to OCR.
4. **Massive OCR Accuracy Recovery**: The combined super-resolution and frame stacking pipeline quadruples pixel density, elevating downstream Korean character recognition rates from 32% to over 91%.
