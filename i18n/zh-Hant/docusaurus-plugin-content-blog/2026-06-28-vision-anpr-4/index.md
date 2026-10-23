---
slug: 2026-06-28-vision-anpr-4
title: "[Vision AI] 攻克行車記錄器模糊雜訊：深度超解析度 (EDSR vs FSRCNN) 與多幀影像疊加降噪 (#4)"
authors: [jbjihwan]
tags: [computer-vision, super-resolution, edsr, image-stacking, anpr, deep-learning, python]
date: 2026-06-28
project: anpr_vision
description: "透過 EDSR 4倍深度超解析度網路與時序多幀影像疊加降噪，從極度模糊的行車記錄器畫面中高保真重建低解析度車牌局部補丁。"
keywords: ["EDSR 深度超解析度", "車牌影像去模糊", "OpenCV dnn_superres", "多幀影像疊加降噪", "深度殘差上取樣"]
---

![EDSR 深度超解析度重建前後對比](./images/01_edsr_sr_comparison.png)

> 📌 **核心要點 (Key Takeaways)**
> - **問題痛點**：從高速行車記錄器畫面裁剪出的遠距離車牌區域往往不足 40x20 像素，且伴隨嚴重的 H.264 編碼巨集區塊效應；傳統的雙三次插值（Bicubic）演算法只會讓字體邊緣更加模糊，無法還原字元有效筆畫。
> - **解決方案**：引入移除了 Batch Normalization 層以保留高動態像素範圍的 EDSR_x4 深度殘差模型 (`EDSR_x4.pb`)，並結合連續 3 至 5 幀的時序多幀加權疊加（Multi-Frame Image Stacking）技術。
> - **落地成效**：車牌像素密度提升 4 倍，筆畫邊緣顯著銳化，使得下游 EasyOCR 對韓文字元的辨識準確率從最初的 32% 飆升至 91% 以上。

{/* truncate */}

---

## 1. 光學解析度極限與深度超解析度的必要性

在惡劣的高速公路行車環境下，即使透過 YOLOv5 精準裁剪出車牌區域，常規 OCR 依舊頻繁失效：

1. **傳統雙三次插值失效**：數學插值演算法僅在相鄰像素間進行線性過渡，根本無法憑空“腦補”出高頻邊緣特徵。
2. **H.264 壓縮與感光雜訊**：視訊編碼壓縮帶來的馬賽克雜訊會導致字元筆畫斷裂粘連。

為此，我們在推論管線中透過 **OpenCV DNN Super-Resolution 模組** 深度整合了經過精細預訓練的 **EDSR_x4 深度模型**：

```python
import cv2
from cv2 import dnn_superres

def init_super_resolution_engine(model_path="EDSR_x4.pb"):
    # 建立深度學習超解析度引擎介面
    sr = dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    
    # 配置模型架構為 edsr，放大倍率為 4x
    sr.setModel("edsr", 4)
    
    # 強制將推論後端綁定至 CUDA GPU 加速
    sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    return sr
```

---

## 2. 基於時序多幀影像疊加的物理級降噪

![多幀影像疊加降噪對比](./images/02_frame_stacking.png)

由於車載攝影機感光晶片在每一幀產生的電子熱雜訊是高斯隨機分佈的，而真實車牌的物理文字在連續幀內具有空間相關性。我們透過對齊連續 $N$ 幀車牌補丁進行加權均值疊加：

```text
I_stacked(x, y) = (1 / N) * Σ Warp(I_i(x, y))
```

這種時序疊加機制不僅在不損失邊緣銳度的前提下消除了高達 70% 的高頻隨機雜訊，還顯著增強了字元與反光底板之間的明暗對比度。

---

## 3. 下篇預告

在接下來的第 5 篇（收尾篇）中，我們將全面揭秘 **韓國車牌語法校驗、EasyOCR 字元辨識調校** 以及核心的 **時序滑動視窗多數表決引擎**，復盤從最初一堆全螢幕亂碼到最終百分之百鎖定目標車牌（`64가1511`）的完整工程突破歷程。

---

### 📌 3~5 行核心總結 (Executive Summary)
1. **低解析度與壓縮雜訊瓶頸**：行車記錄器畫面中裁切出的車牌區域往往不足 $40 \times 20$ 像素，雙三次插值 (Bicubic) 演算法無法恢復因 H.264 壓縮而遺失的文字筆畫邊緣。
2. **引入 EDSR_x4 深度殘差超解析度**：EDSR 架構剝離了批次正規化 (BatchNorm) 層以保留像素級動態範圍，依託 OpenCV `dnn_superres` 高效重建高頻字元輪廓細節。
3. **時序多幀影像疊加降噪 (Image Stacking)**：對連續 $3 \sim 5$ 幀的車牌候選框進行亞像素幾何對齊並像素均值化，強力消除相機感測器隨機雜訊與抖動模糊。
4. **下游 OCR 準確率爆發式提升**：經由 4 倍超分與影像疊加複合增強，下游 EasyOCR 的複雜字元辨識準確率由最初的 32% 跨越式躍升至 91% 以上。
