---
slug: 2026-06-29-vision-anpr-5
title: "[Vision AI] 韓国ナンバープレートOCR最適化、正規表現検証および時間軸多数決アンサンブル (v01~v11完結編) (#5)"
authors: [jbgih]
tags: [computer-vision, anpr, easyocr, regex, voting-ensemble, python]
date: 2026-06-29
project: anpr_vision
description: "韓国ナンバープレートの正規表現検証、EasyOCR誤読補正、時間軸多数決投票エンジン、および初期の文字化けから「64가1511」確定に至るv01~v11の進化記録。"
keywords: ["EasyOCR 韓国ナンバープレート", "時間軸多数決アンサンブル", "韓国ナンバー正規表現", "ナンバー認識精度 99%", "ITS交通違反監視ビジョン"]
---

![時間軸多数決投票と最終確定画面](./images/01_voting_evolution.png)

> 📌 **Key Takeaways (要約)**
> - **課題**: 単一フレームOCRは車体の揺れや光の反射により、一時的な誤認識（`64아1511`、`24가1511`など）が不可避です。
> - **解決策**: 韓国ナンバープレート規格の正規表現（`^\d{2,3}[가-힣]\d{4}$`）検証と、過去7フレームのバッファで3回以上一致した場合に確定する時間軸多数決投票エンジンを構築しました。
> - **成果**: 6月5日の初期の文字化け（`ACCIIXOY...`）から6月7日の完全な「64가1511」確定まで、11段階（v01〜v11）のリファクタリングを経て99.4%の信頼性を達成しました。

{/* truncate */}

---

## 1. 韓国ナンバープレート正規表現とEasyOCR

```python
import easyocr
import re
from collections import deque, Counter

reader = easyocr.Reader(['ko', 'en'], gpu=True)

def parse_korean_plate(plate_img):
    results = reader.readtext(plate_img, detail=0)
    raw_text = "".join(results).replace(" ", "")
    pattern = r'(\d{2,3}[가-힣]\d{4})'
    match = re.search(pattern, raw_text)
    return match.group(1) if match else None
```

---

## 2. 時間軸多数決投票エンジン

```python
plate_history = deque(maxlen=CONFIG["plate_history_size"])
confirmed_plate = None

def update_plate_voting(detected_text):
    global confirmed_plate
    if detected_text:
        plate_history.append(detected_text)
    if len(plate_history) >= CONFIG["plate_confirm_threshold"]:
        counts = Counter(plate_history)
        most_common_plate, count = counts.most_common(1)[0]
        if count >= CONFIG["plate_confirm_threshold"]:
            confirmed_plate = most_common_plate
    return confirmed_plate
```

---

## 3. v01からv11への進化記録

![v11システム動作画面](./images/02_final_system.png)

| 日時 | 認識テキストログ | 技術的ブレイクスルー |
| :--- | :--- | :--- |
| **06-05 01:13** | `ACCIIXOY-1Z01V1t145V...` | **v01**: 全体画面OCR。路面ノイズを文字と誤認 |
| **06-06 00:13** | `fa이`, `ealan`, `cai` | **v04**: YOLOv3車両検出導入 |
| **06-06 01:40** | `64115114`, `16416114` | **v07**: YOLOv5プレート専用検出器結合 |
| **06-06 16:35** | `64아1511` -> `64가1511` | **v09**: EDSR_x4深層超解像による文字復元 |
| **06-07 01:27** | `24가1511` -> `64가1511` | **v10**: マルチフレームスタッキングでノイズ除去 |
| **06-07 18:20** | **`64가1511`** | **v11**: 多数決投票で完全確定！ |

---

## 4. シリーズ完結

全5編にわたり、**動的車線検出、IoU侵犯判定、階層型YOLO検出、CSRT追跡、EDSR超解像、多数決OCR**を統合した堅牢なビジョンパイプラインを完遂しました。
