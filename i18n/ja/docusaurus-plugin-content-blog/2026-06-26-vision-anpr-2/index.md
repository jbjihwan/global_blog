---
slug: 2026-06-26-vision-anpr-2
title: "[Vision AI] 動的車線境界抽出および幾何学的IoU車線侵犯判定アルゴリズム (#2)"
authors: [jbgih]
tags: [computer-vision, anpr, lane-detection, hough-transform, iou, opencv, python]
date: 2026-06-26
project: anpr_vision
description: "Cannyエッジ検出、確率的ハフ変換、左右の傾きフィルタリング、および車両接地領域と車線ポリゴン間の幾何学的IoU侵犯判定数学。"
keywords: ["OpenCV 車線検出", "ハフ変換 車線追跡", "車線侵犯 アルゴリズム", "多角形 IoU 計算", "Canny エッジ抽出"]
---

![動的車線検出オーバーレイ](./images/01_lane_detection.png)

> 📌 **Key Takeaways (要約)**
> - **課題**: ドラレコ映像は路面反射、アスファルトの亀裂、影によって誤検出が多発し、単純な座標判定では車線変更の瞬間を正確に捉えられません。
> - **解決策**: 消失点基準の台形ROIマスク、傾きフィルタリング（|slope| > 0.5）、および7フレーム移動平均キューを採用しました。侵犯判定は車両接地領域（下部30%）と車線ポリゴン間の幾何学的IoU（> 0.05）で定式化しました。
> - **成果**: 路面ノイズを95%以上除外しながら、車線侵犯の瞬間をサブフレーム単位で安定して検出することに成功しました。

{/* truncate */}

---

## 1. 動的車線検出: Cannyと確率的ハフ変換

```python
def detect_lanes(frame):
    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    mask = np.zeros_like(edges)
    roi_polygon = np.array([[
        (int(width * 0.1), height),
        (int(width * 0.45), int(height * 0.6)),
        (int(width * 0.55), int(height * 0.6)),
        (int(width * 0.9), height)
    ]], np.int32)
    cv2.fillPoly(mask, roi_polygon, 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    
    return cv2.HoughLinesP(masked_edges, 1, np.pi/180, 20, minLineLength=20, maxLineGap=10)
```

---

## 2. 傾きフィルタリングと平滑化

線分の傾き `m = (y2 - y1) / (x2 - x1)` を評価:
* **左車線**: `m < -0.5`
* **右車線**: `m > 0.5`
* **路面ノイズ（横線）**: `|m| <= 0.5` は即座に棄却

さらに `deque(maxlen=7)` を用いてフレーム間の揺れ（ジッター）を除去します。

---

## 3. 幾何学的IoU侵犯判定

![車線侵犯IoU判定画面](./images/02_intrusion_iou.png)

```text
Footprint = [x_min, y_min + 0.7*h, x_max, y_max]
IoU = Area(Footprint ∩ Lane_Polygon) / Area(Footprint)
```

`IoU > 0.05` を超えた段階で侵犯フラグを有効化し、ナンバープレート検出器を起動します。

---

## 4. 次回予告

第3編では、**階層的物体検出（YOLOv3 + YOLOv5プレート専用モデル）**と、GPU負荷を大幅に削減する**CSRT追跡器の統合**について解説します。
