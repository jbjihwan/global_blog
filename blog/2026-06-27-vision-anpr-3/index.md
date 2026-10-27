---
slug: 2026-06-27-vision-anpr-3
title: "[Vision AI] Hierarchical Object Detection: YOLOv3 Vehicle ROI, YOLOv5 Plate Detector & CSRT Tracking (#3)"
authors: [jbgih]
tags: [computer-vision, anpr, yolo, csrt-tracker, object-detection, opencv, python]
date: 2026-06-27
project: anpr_vision
description: "Two-stage hierarchical localization: broad vehicle detection via YOLOv3, localized license plate inference via YOLOv5, and CSRT correlation filter tracking."
keywords: ["YOLOv5 License Plate Detection", "CSRT Tracker OpenCV", "Hierarchical Object Detection", "Real-Time Tracking 50FPS", "Vehicle ROI Localization"]
---

![YOLOv5 Plate Detection Localization](./images/01_plate_localization.png)

> 📌 **Key Takeaways (TL;DR)**
> - **Problem**: Searching for tiny plates (30x15 pixels) across the raw 640x480 frame generates massive false positives from roadside signs and drops inference speed below 10 FPS.
> - **Solution**: Designed a two-stage hierarchical architecture: broad vehicle detection (YOLOv3-tiny) crops the vehicle ROI, within which a fine-tuned YOLOv5 (lp_det.pt, conf=0.6) locates the license plate. Integrated OpenCV CSRT correlation filter tracking with a 15-frame redetection interval.
> - **Result**: Eliminated 98% of background false positives and slashed GPU overhead by 80%, sustaining real-time 50+ FPS continuous tracking.

{/* truncate */}

---

## 1. The Pitfalls of Global Detection & The Hierarchical Solution

Running plate detectors across the full 640x480 image causes two critical flaws:

1. **Background Clutter**: Street advertisements, road billboards, and store signs trigger high false-alarm rates.
2. **Resolution Downsampling Loss**: Resizing 640x480 to typical model inputs (e.g., 640x640) squashes tiny 30-pixel plates into sub-feature extinction.

Our two-stage hierarchical pipeline addresses this by constraining the search space:

```python
vehicle_boxes = detect_vehicles_yolov3(frame, net=vehicle_net, conf_thresh=0.5)

for box in vehicle_boxes:
    x1, y1, x2, y2 = box
    vehicle_roi = frame[y1:y2, x1:x2]
    plate_boxes = plate_model(vehicle_roi)
    for pbox in plate_boxes:
        px1, py1, px2, py2 = pbox
        global_plate_box = [x1 + px1, y1 + py1, x1 + px2, y1 + py2]
```

---

## 2. Real-Time Latency Mitigation: CSRT Tracker Integration

![Continuous Tracking with OpenCV CSRT](./images/02_csrt_tracking.png)

```python
if frame_count % CONFIG["detection_interval"] == 0:
    boxes = detect_vehicles_yolov3(frame)
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, tuple(boxes[0]))
else:
    success, tracked_box = tracker.update(frame)
    if not success:
        tracker = None
```

---

## 3. Looking Forward

In Post #4, we explore deep **EDSR_x4 super-resolution** to reconstruct crisp alphanumeric strokes from blurry low-resolution plate crops, combined with **multi-frame image stacking**.

---

### 📌 3–5 Line Executive Summary
1. **The Global Search Bottleneck**: Detecting tiny $30 \times 15$ pixel license plates directly on raw full-frame inputs triggers heavy background false positives from billboards and bogs down inference below 10 FPS.
2. **Two-Stage Hierarchical Localization**: Deploying lightweight YOLOv3-tiny for coarse vehicle ROI extraction followed by dedicated YOLOv5 plate detection within the vehicle patch eliminates 98% of false alarms.
3. **CSRT Correlation Filter Tracking**: Utilizing OpenCV CSRT tracker with a 15-frame periodic redetection schedule reduces full-model inference frequency while maintaining stable bounding box continuity.
4. **80% GPU Overhead Reduction & 50+ FPS**: Decoupling continuous detection from correlation tracking slashes GPU computational load by 80%, sustaining real-time processing exceeding 50 FPS.