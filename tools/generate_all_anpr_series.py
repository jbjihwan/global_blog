import os

blog_root = r"D:\ai\antigravity\global_blog"

locales = {
    'en': os.path.join(blog_root, 'blog'),
    'ko': os.path.join(blog_root, 'i18n', 'ko', 'docusaurus-plugin-content-blog'),
    'ja': os.path.join(blog_root, 'i18n', 'ja', 'docusaurus-plugin-content-blog'),
    'es': os.path.join(blog_root, 'i18n', 'es', 'docusaurus-plugin-content-blog'),
}

# Episode 1
def generate_ep1(lang):
    if lang == 'ko':
        return """---
slug: 2026-06-25-vision-anpr-1
title: "[Vision AI] 블랙박스 차선 침범 적발 & 초해상화 번호판 인식: 6단계 파이프라인 및 실시간 설계 과제 (#1)"
authors: [jbgih]
tags: [computer-vision, anpr, object-detection, super-resolution, opencv, deep-learning, python]
date: 2026-06-25
project: anpr_vision
description: "동적 차선 검출, IoU 침범 판정, YOLOv5 번호판 탐지, EDSR 딥러닝 초해상화, OCR 투표 앙상블을 결합한 6단계 실시간 비전 시스템 아키텍처 설계."
---

![6단계 ANPR 파이프라인 구조도](./images/01_pipeline_diagram.png)

> 📌 **Key Takeaways (핵심 요약)**
> - **문제점**: 저화질 차량용 블랙박스 영상은 노면 진동, 역광, 모션 블러, 심한 H.264 압축 아티팩트로 인해 번호판이 심하게 뭉개지며 차선 침범 상황을 실시간으로 추적하기 극도로 어렵습니다.
> - **해결책**: 작업 단계를 6단계 계층형 파이프라인(Canny/Hough 동적 차선 추출 -> YOLOv3 차량 검출 -> 다각형 IoU 침범 판정 -> YOLOv5 번호판 국소 탐지 -> EDSR_x4 심층 초해상화 복원 -> EasyOCR 시간 축 Majority Voting)으로 모듈화 설계했습니다.
> - **결과**: 과도한 GPU 부하 없이 30 FPS 이상의 처리 속도를 확보하면서도, 열악한 블랙박스 환경에서 차선 침범 차량의 번호판을 완벽하게 판독하는 End-to-End 파이프라인을 구축했습니다.

{/* truncate */}

---

## 1. 프로젝트 배경: 왜 블랙박스 컴퓨터 비전은 어려운가?

스마트 모빌리티와 지능형 교통 시스템(ITS)에서 **실시간 차선 침범 차량 감지 및 자동 번호판 인식(ANPR)**은 자율주행과 법규 단속 자동화의 핵심 기술입니다. 하지만 실제 현장 블랙박스 영상을 처리할 때는 다음과 같은 복합적인 물리적·광학적 난제에 직면합니다:

1. **심각한 저해상도와 텍스처 뭉개짐**: 후방 또는 전방 주행 차량의 번호판 영역은 전체 640x480 프레임에서 불과 `30x15` ~ `50x25` 픽셀에 불과하여 한글 음절과 숫자의 획이 하나로 뭉개집니다.
2. **카메라 노면 진동 및 롤링 셔터 왜곡**: 주행 중 발생하는 수직 진동과 급제동, 차선 변경 시의 급격한 각도 변화로 인해 직선 차선이 왜곡됩니다.
3. **실시간 연산 병목**: 거대 비전 트랜스포머나 풀 프레임 고밀도 모델을 매 프레임 실행하면 심각한 프레임 드롭이 발생하여 실시간 추적이 불가능합니다.

---

## 2. 6단계 계층형 파이프라인 아키텍처

이를 해결하기 위해 우리는 연산 효율과 판독 정확도를 동시에 극대화하는 **6단계 계층형(Hierarchical) 파이프라인**을 설계했습니다.

```mermaid
flowchart TD
    Raw[원본 블랙박스 프레임 640x480] --> L1[1단계: Canny + Hough 동적 차선 추출]
    Raw --> L2[2단계: YOLOv3-tiny 차량 영역 검출]
    L1 & L2 --> L3[3단계: 차량 풋프린트 & 차선 다각형 IoU 침범 판정]
    L3 -- 침범 발생 시 --> L4[4단계: 차량 ROI 내 YOLOv5 번호판 국소 탐지]
    L4 --> L5[5단계: EDSR_x4 딥러닝 4배 초해상화 복원]
    L5 --> L6[6단계: EasyOCR + 정규식 + Majority Voting 앙상블]
    L6 --> Result[최종 위반 차량 번호판 확정 64가1511]
```

![최종 감지 및 판독 결과 화면](./images/02_final_result.png)

### 각 단계별 역할 분담
1. **차선 추출 (Lane Extraction)**: 소실점을 고려한 사다리꼴 ROI 마스킹 및 기울기(Slope) 필터링으로 차로 경계선을 동적 추적합니다.
2. **차량 검출 (Vehicle Detection)**: 가벼운 YOLOv3-tiny 모델로 주변 주행 차량의 바운딩 박스를 밀리초 단위로 생성합니다.
3. **침범 판정 (Intrusion Criterion)**: 차량의 하단 접지면과 차선 다각형 간의 기하학적 교집합 면적비(IoU)가 임계치(0.05)를 초과하는지 평가합니다.
4. **번호판 위치 특정 (Plate Localization)**: 전체 화면이 아닌, 침범 차량 ROI 내부에서만 파인튜닝된 YOLOv5(`lp_det.pt`)를 실행하여 불필요한 연산을 제거합니다.
5. **초해상화 복원 (Super-Resolution)**: 저해상도 번호판 크롭 패치를 딥러닝 EDSR_x4 신경망에 전달하여 엣지와 획을 4배 확대 복원합니다.
6. **문자 인식 및 투표 (OCR & Majority Voting)**: EasyOCR 추출 결과에 한국 번호판 정규식 필터를 적용하고, 최근 7개 프레임 히스토리 큐에서 다수결로 최종 번호를 확정합니다.

---

## 3. 핵심 시스템 파라미터 (`CONFIG`)

안정적인 파이프라인 구동을 위해 튜닝된 핵심 설정값은 다음과 같습니다:

```python
CONFIG = {
    "output_width": 640,
    "output_height": 480,
    
    # 차량 탐지 및 차선 침범 임계값
    "conf_threshold_vehicle": 0.5,
    "nms_threshold_vehicle": 0.4,
    "min_vehicle_w": 70,
    "min_vehicle_h": 70,
    "lane_iou_threshold": 0.05,
    "detection_interval": 15,       # 15프레임마다 재검출, 중간은 CSRT 추적
    
    # 번호판 OCR 및 초해상화 파라미터
    "min_plate_area_for_ocr": 1200, # 최소 픽셀 면적 확보 후 OCR 수행
    "plate_history_size": 7,        # 시간 축 슬라이딩 윈도우 크기
    "plate_confirm_threshold": 3,   # 3회 이상 일치 시 번호판 최종 확정
    
    # 모델 가중치 파일
    "sr_model": "EDSR_x4.pb",
    "yolo_plate_model": "lp_det.pt"
}
```

---

## 4. 다음 편 예고

다음 2편에서는 **Canny 에지 검출, 확률적 허프 변환(HoughLinesP), 좌우 기울기 필터링 수학**, 그리고 차량 바운딩 박스와 차선 간의 **동적 다각형 IoU 침범 판정 알고리즘**을 상세히 분석합니다.
"""
    elif lang == 'en':
        return """---
slug: 2026-06-25-vision-anpr-1
title: "[Vision AI] Blackbox Lane Intrusion & Super-Resolution ANPR: 6-Stage End-to-End Pipeline & Real-Time Constraints (#1)"
authors: [jbgih]
tags: [computer-vision, anpr, object-detection, super-resolution, opencv, deep-learning, python]
date: 2026-06-25
project: anpr_vision
description: "Architecting a 6-stage computer vision pipeline combining dynamic lane detection, IoU intrusion metrics, YOLOv5 license plate detection, EDSR super-resolution, and OCR voting."
---

![6-Stage ANPR Pipeline Diagram](./images/01_pipeline_diagram.png)

> 📌 **Key Takeaways (TL;DR)**
> - **Problem**: Low-resolution dashcam footage suffers from severe vehicle vibration, nighttime backlighting, and heavy motion blur, making direct license plate recognition and lane violation tracking extremely error-prone.
> - **Solution**: Designed a unified 6-stage vision architecture: Canny/Hough lane extraction -> YOLOv3 vehicle detection -> polygon IoU lane violation calculation -> YOLOv5 plate localization -> EDSR_x4 super-resolution -> EasyOCR temporal voting.
> - **Result**: Constructed an end-to-end Python pipeline achieving robust vehicle tracking and lane boundary monitoring even under degraded dashcam conditions.

{/* truncate */}

---

## 1. Project Background: Why Dashcam Vision is Hard

In intelligent transportation systems (ITS) and autonomous traffic enforcement, **real-time lane intrusion detection and automatic number plate recognition (ANPR)** are foundational capabilities. However, real-world dashcam footage presents severe optical challenges:

1. **Extreme Low Resolution & Blurred Textures**: The license plate of a leading or overtaking vehicle often spans merely `30x15` to `50x25` pixels across a 640x480 frame, causing alphanumeric strokes to merge into indistinct blobs.
2. **Vehicle Vibration & Rolling Shutter Distortions**: Road bumps, sudden decelerations, and perspective shifts distort straight lane boundaries.
3. **Real-Time Latency Bottlenecks**: Executing heavy full-frame vision transformers per frame results in fatal FPS drops, disabling real-time tracking.

---

## 2. 6-Stage Hierarchical Pipeline Architecture

To achieve both high precision and high throughput, we modularized the system into a **6-stage decoupled pipeline**:

```mermaid
flowchart TD
    Raw[Raw Dashcam Frame 640x480] --> L1[Stage 1: Canny + Hough Dynamic Lane Extraction]
    Raw --> L2[Stage 2: YOLOv3-tiny Vehicle Detection]
    L1 & L2 --> L3[Stage 3: Vehicle Footprint & Lane Polygon IoU Intrusion Metric]
    L3 -- If Intrusion Triggered --> L4[Stage 4: Localized YOLOv5 Plate Detection in Vehicle ROI]
    L4 --> L5[Stage 5: EDSR_x4 Deep 4x Super-Resolution]
    L5 --> L6[Stage 6: EasyOCR + Regex + Temporal Majority Voting]
    L6 --> Result[Confirmed Violation Plate: 64가1511]
```

![Final Detection and ANPR Recognition Output](./images/02_final_result.png)

### Decoupled Processing Responsibilities
1. **Lane Extraction**: Trapezoidal dynamic ROI masking, Canny edge detection, and slope filtering isolate driving corridor bounds.
2. **Vehicle Detection**: Lightweight YOLOv3-tiny outputs candidate vehicle bounding boxes in milliseconds.
3. **Intrusion Criterion**: Computes geometric Intersection-over-Union (IoU > 0.05) between vehicle tire footprint and the lane boundary polygon.
4. **Plate Localization**: YOLOv5 (`lp_det.pt`) evaluates only the cropped vehicle ROI, saving immense compute cycles.
5. **Super-Resolution**: The cropped plate patch is passed through a deep EDSR_x4 neural network, reconstructing high-frequency character contours.
6. **OCR & Majority Voting**: EasyOCR extracts alphanumeric tokens, which undergo Korean syntax regex validation and temporal multi-frame voting to confirm the plate number.

---

## 3. Core System Parameters (`CONFIG`)

```python
CONFIG = {
    "output_width": 640,
    "output_height": 480,
    "conf_threshold_vehicle": 0.5,
    "nms_threshold_vehicle": 0.4,
    "min_vehicle_w": 70,
    "min_vehicle_h": 70,
    "lane_iou_threshold": 0.05,
    "detection_interval": 15,
    "min_plate_area_for_ocr": 1200,
    "plate_history_size": 7,
    "plate_confirm_threshold": 3,
    "sr_model": "EDSR_x4.pb",
    "yolo_plate_model": "lp_det.pt"
}
```

---

## 4. Looking Forward

In Post #2, we dive deep into **Canny edge filtering, probabilistic Hough transform mathematics (HoughLinesP), slope-based outlier rejection**, and the geometric polygon IoU intrusion criterion.
"""
    elif lang == 'ja':
        return """---
slug: 2026-06-25-vision-anpr-1
title: "[Vision AI] ドライブレコーダー車線侵犯検知＆超解像ANPR: 6段階パイプラインとリアルタイム設計課題 (#1)"
authors: [jbgih]
tags: [computer-vision, anpr, object-detection, super-resolution, opencv, deep-learning, python]
date: 2026-06-25
project: anpr_vision
description: "動的車線検出、IoU侵犯判定、YOLOv5ナンバープレート検出、EDSR超解像復元、OCR投票アンサンブルを統合した6段階ビジョンシステムのアーキテクチャ設計。"
---

![6段階ANPRパイプライン構成図](./images/01_pipeline_diagram.png)

> 📌 **Key Takeaways (要約)**
> - **課題**: ドラレコの低解像度映像は、車体振動、逆光、モーションブラー、強いH.264圧縮ノイズにより、ナンバープレートが著しく潰れ、車線侵犯のリアルタイム追跡が極めて困難です。
> - **解決策**: Canny/Hough動的車線抽出 -> YOLOv3車両検出 -> 多角形IoU侵犯判定 -> YOLOv5プレート局所検出 -> EDSR_x4深層超解像復元 -> EasyOCR時間軸多数決投票という6段階の階層型パイプラインを設計しました。
> - **成果**: 過度なGPU負荷を回避し30 FPS以上を維持しながら、過酷なドラレコ環境下でも侵犯車両のナンバープレートを正確に確定するEnd-to-Endシステムを構築しました。

{/* truncate */}

---

## 1. プロジェクト背景: なぜドラレコ映像の認識は難しいのか？

高度道路交通システム（ITS）や自動交通違反取締において、**リアルタイム車線侵犯検知と自動ナンバープレート認識（ANPR）**は中核となる技術です。しかし実際の車載ドラレコ映像を処理する際には、多くの光学的・物理的障害に直面します:

1. **極端な低解像度とテクスチャの潰れ**: 640x480フレーム内において、対象車両のナンバープレート領域はわずか`30x15`〜`50x25`ピクセル程度しかなく、文字の線画が完全に一体化してしまいます。
2. **路面振動とローリングシャッター歪み**: 走行中の段差や急ブレーキ、急な車線変更による角度変化が直線の幾何学的推定を妨げます。
3. **リアルタイム処理のレイテンシ**: 重大なフレーム単位の重層モデル適用は深刻なフレーム落ちを引き起こし、実時間の追跡を破綻させます。

---

## 2. 6段階の階層型パイプラインアーキテクチャ

```mermaid
flowchart TD
    Raw[ドラレコ生フレーム 640x480] --> L1[第1段階: Canny + Hough 動的車線抽出]
    Raw --> L2[第2段階: YOLOv3-tiny 車両領域検出]
    L1 & L2 --> L3[第3段階: 車両底面＆車線ポリゴンIoU侵犯判定]
    L3 -- 侵犯検知時 --> L4[第4段階: 車両ROI内のYOLOv5プレート局所特定]
    L4 --> L5[第5段階: EDSR_x4 深層超解像4倍復元]
    L5 --> L6[第6段階: EasyOCR + 正規表現 + 時間軸多数決投票]
    L6 --> Result[確定違反ナンバー: 64가1511]
```

![最終検出および認識結果](./images/02_final_result.png)

---

## 3. 主要システム設定値 (`CONFIG`)

```python
CONFIG = {
    "output_width": 640,
    "output_height": 480,
    "conf_threshold_vehicle": 0.5,
    "nms_threshold_vehicle": 0.4,
    "min_vehicle_w": 70,
    "min_vehicle_h": 70,
    "lane_iou_threshold": 0.05,
    "detection_interval": 15,
    "min_plate_area_for_ocr": 1200,
    "plate_history_size": 7,
    "plate_confirm_threshold": 3,
    "sr_model": "EDSR_x4.pb",
    "yolo_plate_model": "lp_det.pt"
}
```

---

## 4. 次回予告

第2編では、**Cannyエッジ検出、確率的ハフ変換（HoughLinesP）、傾きフィルタリング数学**、および車両バウンディングボックスと車線間の**動的ポリゴンIoU侵犯判定アルゴリズム**を詳しく解説します。
"""
    elif lang == 'es':
        return """---
slug: 2026-06-25-vision-anpr-1
title: "[Vision AI] Detección de Invasión de Carril en Caja Negra y ANPR con Superresolución: Pipeline de 6 Etapas y Desafíos en Tiempo Real (#1)"
authors: [jbgih]
tags: [computer-vision, anpr, object-detection, super-resolution, opencv, deep-learning, python]
date: 2026-06-25
project: anpr_vision
description: "Diseño de un pipeline de visión de 6 etapas que combina detección dinámica de carril, métricas de invasión IoU, detección de matrículas YOLOv5, superresolución EDSR y votación OCR."
---

![Diagrama del Pipeline ANPR de 6 Etapas](./images/01_pipeline_diagram.png)

> 📌 **Key Takeaways (Puntos Clave)**
> - **Problema**: Las grabaciones de baja resolución de cámaras de tablero sufren vibraciones, contraluces y desenfoque de movimiento, lo que hace que el reconocimiento de matrículas y el monitoreo de invasión de carril fallen con frecuencia.
> - **Solución**: Diseñamos una arquitectura desacoplada de 6 etapas: extracción de carril Canny/Hough -> detección de vehículos YOLOv3 -> IoU de invasión -> localización de matrícula YOLOv5 -> superresolución EDSR_x4 -> votación temporal EasyOCR.
> - **Resultado**: Construimos un pipeline en Python de alto rendimiento que mantiene más de 30 FPS identificando con precisión matrículas infractoras bajo condiciones ópticas severas.

{/* truncate */}

---

## 1. Contexto del Proyecto: Por qué la Visión en Dashcams es Difícil

En sistemas de transporte inteligente (ITS), la **detección en tiempo real de invasión de carril y el reconocimiento automático de matrículas (ANPR)** son desafíos esenciales. Las grabaciones reales presentan barreras ópticas críticas:

1. **Baja Resolución Extrema**: La matrícula del vehículo objetivo a menudo ocupa apenas `30x15` a `50x25` píxeles dentro de un fotograma de 640x480.
2. **Vibración de Calzada y Distorsión de Perspectiva**: Las irregularidades del asfalto deforman las líneas viales rectas.
3. **Cuellos de Botella de Cómputo**: Aplicar modelos masivos en cada fotograma completo colapsa la tasa de FPS.

---

## 2. Arquitectura Jerárquica de 6 Etapas

```mermaid
flowchart TD
    Raw[Fotograma Dashcam 640x480] --> L1[Etapa 1: Extracción Dinámica de Carril Canny + Hough]
    Raw --> L2[Etapa 2: Detección Rápida de Vehículos YOLOv3-tiny]
    L1 & L2 --> L3[Etapa 3: Métrica IoU entre Base del Vehículo y Polígono de Carril]
    L3 -- Si Ocurre Invasión --> L4[Etapa 4: Detección Localizada de Matrícula YOLOv5]
    L4 --> L5[Etapa 5: Superresolución Profunda 4x con EDSR_x4]
    L5 --> L6[Etapa 6: EasyOCR + Regex + Votación Temporal por Mayoría]
    L6 --> Result[Matrícula Final Confirmada: 64가1511]
```

![Salida de Detección y Reconocimiento ANPR](./images/02_final_result.png)

---

## 3. Parámetros Principales del Sistema (`CONFIG`)

```python
CONFIG = {
    "output_width": 640,
    "output_height": 480,
    "conf_threshold_vehicle": 0.5,
    "nms_threshold_vehicle": 0.4,
    "min_vehicle_w": 70,
    "min_vehicle_h": 70,
    "lane_iou_threshold": 0.05,
    "detection_interval": 15,
    "min_plate_area_for_ocr": 1200,
    "plate_history_size": 7,
    "plate_confirm_threshold": 3,
    "sr_model": "EDSR_x4.pb",
    "yolo_plate_model": "lp_det.pt"
}
```

---

## 4. Próxima Entrega

En la Entrega #2, exploraremos a fondo las matemáticas de la **transformada probabilística de Hough, el filtrado de pendientes** y el **criterio geométrico de invasión basado en IoU**.
"""

print("ep1 generator defined.")
