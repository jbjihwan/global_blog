---
slug: 2026-06-28-vision-anpr-4
title: "[Vision AI] 低解像度ドラレコのぼやけ克服: EDSR深層超解像とマルチフレームスタッキングノイズ除去 (#4)"
authors: [jbgih]
tags: [computer-vision, super-resolution, edsr, image-stacking, anpr, deep-learning, python]
date: 2026-06-28
project: anpr_vision
description: "切り出された低解像度ナンバープレートを4倍復元するEDSR深層超解像と、複数フレーム平均化スタッキングによるノイズ除去手法。"
keywords: ["EDSR 超解像", "低解像度ナンバープレート復元", "OpenCV dnn_superres", "マルチフレームスタッキング", "深層残差4倍拡大"]
---

![EDSR深層超解像適用結果](./images/01_edsr_sr_comparison.png)

> 📌 **Key Takeaways (要約)**
> - **課題**: ドラレコ映像から抽出されたプレート領域は40x20ピクセル以下と極小で、バイキュービック補間では輪郭がぼやけて文字認識が不可能です。
> - **解決策**: バッチ正規化を除去してテクスチャ復元力を高めたEDSR_x4深層残差ネットワーク（EDSR_x4.pb）を導入し、連続3〜5フレームを平均化するマルチフレーム画像スタッキングを併用しました。
> - **成果**: プレート解像度を4倍に拡大し文字のエッジを鮮明化、EasyOCRのハングル認識成功率を32%から91%以上へ大幅に向上させました。

{/* truncate */}

---

## 1. EDSR_x4深層超解像エンジン

```python
import cv2
from cv2 import dnn_superres

sr = dnn_superres.DnnSuperResImpl_create()
sr.readModel("EDSR_x4.pb")
sr.setModel("edsr", 4)
enhanced_plate = sr.upsample(plate_roi)
```

---

## 2. マルチフレームスタッキング

![マルチフレームスタッキング](./images/02_frame_stacking.png)

時間軸で連続するフレームを整列・平均化することで、ランダムなノイズを打ち消し、文字のコントラストを強調します。

---

## 3. 次回予告

最終回（第5編）では、**EasyOCR韓国ナンバープレート正規表現検証**、初期の文字化けから「64가1511」確定に至る**多数決投票アンサンブルとv01~v11の進化記録**を総括します。

---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **低解像度と圧縮ノイズの壁**: ドライブレコーダー映像から切り出したナンバー画像は $40 \times 20$ ピクセル未満と極小で、Bicubic補間では文字輪郭が潰れてOCRが不可能です。
2. **EDSR_x4 による深層超解像の導入**: バッチ正規化層を排して高周波テクスチャを保持するEDSR残差ネットワークをOpenCV `dnn_superres` で稼働させ、エッジを鮮明に復元します。
3. **時系列マルチフレーム画像スタッキング**: 連続する3〜5フレームのナンバー領域を位置合わせして平均合成することで、センサーノイズとモーションブラーを大幅に除去します。
4. **OCR認識精度の大幅向上**: 4倍の超解像処理と画像スタッキングの相乗効果により、EasyOCRの後続文字認識率を32%から91%超へと飛躍的に改善しました。
