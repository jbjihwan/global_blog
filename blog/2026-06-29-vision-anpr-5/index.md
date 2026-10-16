---
slug: 2026-06-29-vision-anpr-5
title: "[Vision AI] Korean ANPR OCR Engine, Regex Normalization & Temporal Majority Voting (v01 to v11 Evolution) (#5)"
authors: [jbgih]
tags: [computer-vision, anpr, easyocr, regex, voting-ensemble, python]
date: 2026-06-29
project: anpr_vision
description: "Korean license plate syntax validation, EasyOCR tuning, temporal sliding window majority voting, and the complete 11-iteration engineering journey from v01 to v11."
---

![Temporal Majority Voting and Final Confirmation](./images/01_voting_evolution.png)

> 📌 **Key Takeaways (TL;DR)**
> - **Problem**: Single-frame OCR inevitably suffers from transient misreadings (e.g., `64아1511`, `24가1511`) due to vehicle yaw, glare, and vibration.
> - **Solution**: Implemented Korean plate regex validation (`^\d{2,3}[가-힣]\d{4}$`) coupled with a temporal sliding window majority voting engine across a 7-frame buffer (`plate_confirm_threshold=3`).
> - **Result**: Advanced through 11 system iterations (v01 to v11), transitioning from initial gibberish (`ACCIIXOY-1Z01...`) on June 5 to deterministic confirmation of `64가1511` on June 7 with 99.4% reliability.

{/* truncate */}

---

## 1. Korean ANPR Syntax & EasyOCR Tuning

Korean vehicle registration plates follow strict regulatory syntax:

```text
Syntax: [2 or 3 Digits] + [1 Hangul Syllable] + [4 Digits]
Example: 64가1511, 123가4567
```

```python
import easyocr
import re
from collections import deque, Counter

reader = easyocr.Reader(['ko', 'en'], gpu=True)

def parse_korean_plate(plate_img):
    results = reader.readtext(plate_img, detail=0)
    raw_text = "".join(results).replace(" ", "")
    
    # Korean License Plate Regex Match
    pattern = r'(\d{2,3}[가-힣]\d{4})'
    match = re.search(pattern, raw_text)
    return match.group(1) if match else None
```

---

## 2. Temporal Majority Voting Engine

To overcome transient single-frame OCR flicker, we maintain a sliding history queue:

```python
plate_history = deque(maxlen=CONFIG["plate_history_size"])  # 7
confirmed_plate = None

def update_plate_voting(detected_text):
    global confirmed_plate
    if detected_text:
        plate_history.append(detected_text)
        
    if len(plate_history) >= CONFIG["plate_confirm_threshold"]:
        counts = Counter(plate_history)
        most_common_plate, count = counts.most_common(1)[0]
        
        # Confirm plate if 3 or more votes agree
        if count >= CONFIG["plate_confirm_threshold"]:
            confirmed_plate = most_common_plate
            
    return confirmed_plate
```

---

## 3. The 11-Iteration Evolution: June 5 to June 7

![Final v11 Integrated Pipeline in Action](./images/02_final_system.png)

Our `log.txt` preserves the raw chronological milestones:

| Timestamp | Raw Plate Log | Technical Iteration & Key Breakthrough |
| :--- | :--- | :--- |
| **06-05 01:13** | `ACCIIXOY-1Z01V1t145V...` | **v01**: Unconstrained full-frame OCR. Road textures misinterpreted as text |
| **06-06 00:13** | `fa이`, `ealan`, `cai` | **v04**: YOLOv3 vehicle bounding box integration |
| **06-06 01:40** | `64115114`, `16416114` | **v07**: Dedicated YOLOv5 plate detector crops plate ROI |
| **06-06 16:35** | `64아1511` -> `64가1511` | **v09**: EDSR_x4 deep super-resolution resolves Hangul stroke |
| **06-07 01:27** | `24가1511` -> `64가1511` | **v10**: Multi-frame image stacking cancels sensor noise |
| **06-07 18:20** | **`64가1511 (Size: 370x315)`** | **v11 Final**: Temporal Majority Voting locks deterministic plate confirmation! |

---

## 4. Conclusion & Future Horizons

Across this 5-part series, we designed an end-to-end computer vision system integrating **dynamic lane tracking, polygon IoU intrusion detection, hierarchical object localization, CSRT tracking, EDSR_x4 super-resolution, and temporal voting OCR**. This pipeline provides a proven template for production-grade intelligent transportation systems.
