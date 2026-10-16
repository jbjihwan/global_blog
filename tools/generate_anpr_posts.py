import os

blog_root = r"D:\ai\antigravity\global_blog"

# Directory mapping for locales
locale_dirs = {
    'en': os.path.join(blog_root, 'blog'),
    'ko': os.path.join(blog_root, 'i18n', 'ko', 'docusaurus-plugin-content-blog'),
    'ja': os.path.join(blog_root, 'i18n', 'ja', 'docusaurus-plugin-content-blog'),
    'es': os.path.join(blog_root, 'i18n', 'es', 'docusaurus-plugin-content-blog'),
}

# Episode 1 Data
ep1_content = {
    'slug': '2026-06-25-vision-anpr-1',
    'date': '2026-06-25',
    'en': {
        'title': '[Vision AI] Blackbox Lane Intrusion & Super-Resolution ANPR: 6-Stage End-to-End Pipeline & Real-Time Constraints (#1)',
        'description': 'Architecting a 6-stage computer vision pipeline combining dynamic lane detection, IoU intrusion metrics, YOLOv5 license plate detection, EDSR super-resolution, and OCR voting.',
        'tags': ['computer-vision', 'anpr', 'object-detection', 'super-resolution', 'opencv', 'deep-learning'],
        'tldr_prob': 'Low-resolution dashcam footage suffers from severe vehicle vibration, nighttime backlighting, and heavy motion blur, making direct license plate recognition and lane violation tracking extremely error-prone.',
        'tldr_sol': 'Designed a unified 6-stage vision architecture: Canny/Hough lane extraction -> YOLOv3 vehicle detection -> polygon IoU lane violation calculation -> YOLOv5 plate localization -> EDSR_x4 super-resolution -> EasyOCR temporal voting.',
        'tldr_res': 'Constructed an end-to-end Python pipeline achieving robust vehicle tracking and lane boundary monitoring even under degraded dashcam conditions.',
        'h2_1': '1. The Real-World Challenge: Why Dashcam Vision is Hard',
        'p_1': 'Autonomous traffic monitoring and law enforcement automation demand high reliability. However, off-the-shelf dashcam recordings captured from moving vehicles introduce brutal optical degradations: heavy compression artifacts, non-linear perspective warping, severe motion blur during vehicle lane changes, and tiny license plate regions often measuring less than 40x20 pixels.',
        'h2_2': '2. The 6-Stage Hierarchical Architecture',
        'p_2': 'Rather than attempting end-to-end heavy neural network inference on raw 640x480 video frames, we decomposed the task into six decoupled, specialized stages:',
        'pipeline_steps': [
            '**Stage 1 (Lane Detection)**: Canny edge filtering and HoughLinesP with dynamic trapezoidal ROI masking and slope thresholding.',
            '**Stage 2 (Vehicle Detection)**: Lightweight YOLOv3-tiny generating fast candidate bounding boxes around traffic actors.',
            '**Stage 3 (Intrusion Criterion)**: Calculating dynamic polygon Intersection-over-Union (IoU) between vehicle footprints and detected lane boundaries.',
            '**Stage 4 (Plate Localization)**: Cropping candidate vehicle ROIs and applying a fine-tuned YOLOv5 (`lp_det.pt`) plate detector.',
            '**Stage 5 (Super-Resolution)**: Feeding tiny cropped plate patches into a deep EDSR_x4 neural network to reconstruct crisp alphanumeric edges.',
            '**Stage 6 (OCR & Majority Voting)**: Running EasyOCR on super-resolved plates followed by regex parsing and a multi-frame voting engine to eliminate temporal noise.'
        ],
        'h2_3': '3. System Configuration & Hardware Orchestration',
        'p_3': 'Balancing real-time FPS constraints with heavy deep learning models required an asynchronous GPU/CPU pipeline:',
        'h2_4': '4. Looking Forward',
        'p_4': 'In the next post (#2), we dive deep into the geometric mathematics of dynamic lane boundary extraction, slope-based outlier pruning, and the dynamic IoU intrusion criterion.'
    },
    'ko': {
        'title': '[Vision AI] 블랙박스 차선 침범 적발 & 초해상화 번호판 인식: 6단계 파이프라인 및 실시간 설계 과제 (#1)',
        'description': '동적 차선 검출, IoU 침범 판정, YOLOv5 번호판 탐지, EDSR 딥러닝 초해상화, OCR 투표 앙상블을 결합한 6단계 비전 시스템 아키텍처 설계.',
        'tags': ['computer-vision', 'anpr', 'object-detection', 'super-resolution', 'opencv', 'deep-learning'],
        'tldr_prob': '주행 중인 블랙박스 저화질 영상은 차량 흔들림, 역광, 모션 블러, 심한 압축 노이즈로 인해 번호판이 뭉개지고 차선 침범을 실시간으로 정확히 추적하기 어렵습니다.',
        'tldr_sol': 'Canny/Hough 동적 차선 추출 -> YOLOv3 차량 검출 -> 다각형 IoU 차선 침범 계산 -> YOLOv5 번호판 정밀 검출 -> EDSR_x4 초해상화 복원 -> EasyOCR 시간 축 투표 앙상블의 6단계 통합 파이프라인을 구축했습니다.',
        'tldr_res': '열악한 블랙박스 환경에서도 프레임 간 일관성을 유지하며 차선 침범 차량을 감지하고 번호판을 판독하는 End-to-End 시스템을 완성했습니다.',
        'h2_1': '1. 실제 현장의 난제: 왜 블랙박스 비전은 어려운가?',
        'p_1': '지능형 교통 시스템(ITS)과 무인 단속 자동화는 높은 신뢰성을 요구합니다. 그러나 실제 차량에 장착된 블랙박스 영상은 가혹한 광학적 한계를 지닙니다: H.264 압축 아티팩트, 노면 진동에 따른 흔들림, 차선 변경 시 발생하는 모션 블러, 그리고 대상 차량 번호판이 40x20 픽셀 미만으로 극도로 작아지는 해상도 뭉개짐 현상입니다.',
        'h2_2': '2. 6단계 계층형 아키텍처 설계',
        'p_2': '원본 640x480 영상에 단일 대형 딥러닝 모델을 무겁게 적용하는 대신, 계산 효율과 정확도를 모두 잡기 위해 작업을 6단계로 분할했습니다:',
        'pipeline_steps': [
            '**1단계 (차선 검출)**: 동적 사다리꼴 관심영역(ROI) 마스킹, Canny 에지 검출 및 HoughLinesP 기반 좌우 차선 분리.',
            '**2단계 (차량 탐지)**: 경량 YOLOv3-tiny를 활용하여 주행 차로 주변 차량의 바운딩 박스를 신속하게 추출.',
            '**3단계 (침범 판정)**: 차량의 하단 풋프린트와 검출된 차선 영역 간의 기하학적 교집합 면적비(IoU > 0.05)를 실시간 연산.',
            '**4단계 (번호판 정밀 탐지)**: 침범 판정을 받은 차량의 ROI만을 크롭하여 파인튜닝된 YOLOv5(`lp_det.pt`)로 번호판을 정밀 위치 검출.',
            '**5단계 (초해상화 복원)**: 뭉개진 저해상도 번호판 패치를 EDSR_x4 심층신경망에 통과시켜 4배 확대 및 선명한 텍스트 엣지 복원.',
            '**6단계 (OCR 및 다수결 투표)**: 복원된 번호판에 EasyOCR을 수행하고, 정규식 검증 및 프레임 간 이동 큐 Majority Voting으로 최종 번호를 확정.'
        ],
        'h2_3': '3. 시스템 파라미터 및 하이브리드 파이프라인 구성',
        'p_3': '실시간 처리 속도(FPS)와 딥러닝의 높은 연산량을 조화시키기 위해 CPU와 GPU 역할을 분담하는 하이브리드 구조를 설계했습니다:',
        'h2_4': '4. 다음 편 예고',
        'p_4': '다음 2편에서는 허프 변환을 통한 동적 차선 경계선 검출 수학, 기울기 기반 노이즈 제거, 그리고 차량 바운딩 박스와 차선 간의 기하학적 IoU 침범 판정 알고리즘을 상세히 다룹니다.'
    },
    'ja': {
        'title': '[Vision AI] ドライブレコーダー車線侵犯検知＆超解像ANPR: 6段階パイプラインとリアルタイム設計課題 (#1)',
        'description': '動的車線検出、IoU侵犯判定、YOLOv5ナンバープレート検出、EDSR超解像復元、OCR投票アンサンブルを統合した6段階ビジョンシステムのアーキテクチャ設計。',
        'tags': ['computer-vision', 'anpr', 'object-detection', 'super-resolution', 'opencv', 'deep-learning'],
        'tldr_prob': '走行中のドラレコ低解像度映像は、車体振動、逆光、モーションブラー、激しい圧縮ノイズにより、ナンバープレートが潰れ車線侵犯追跡の誤認識が多発します。',
        'tldr_sol': 'Canny/Hough動的車線抽出 -> YOLOv3車両検出 -> 多角形IoU侵犯計算 -> YOLOv5プレート局所検出 -> EDSR_x4超解像 -> EasyOCR時間軸多数決投票の6段階パイプラインを設計しました。',
        'tldr_res': '過酷なドラレコ環境下でもフレーム間の一貫性を保ち、侵犯車両の特定とナンバー読取を可能にするEnd-to-Endシステムを構築しました。',
        'h2_1': '1. 現場の課題: なぜドラレコ映像認識は難しいのか？',
        'p_1': '高度道路交通システム（ITS）や自動取締システムには極めて高い信頼性が求められます。しかし車載ドラレコ映像は、激しい路面振動、不可避なモーションブラー、激しい圧縮アーティファクト、そしてナンバープレートが40x20ピクセル以下に縮小されるという過酷な光学的限界に直面します。',
        'h2_2': '2. 6段階の階層型アーキテクチャ',
        'p_2': '生映像全体に単一の巨大モデルを適用する代わりに、計算効率と精度を両立する6段階のパイプラインにタスクを分割しました:',
        'pipeline_steps': [
            '**第1段階 (車線検出)**: 台形動的ROIマスク、Cannyエッジ、確率的ハフ変換（HoughLinesP）による左右車線分離。',
            '**第2段階 (車両検出)**: 軽量YOLOv3-tinyによる対象車両の高速バウンディングボックス生成。',
            '**第3段階 (侵犯判定)**: 車両フットプリントと車線境界間の幾何学的IoU（> 0.05）のリアルタイム交差判定。',
            '**第4段階 (プレート検出)**: 侵犯車両ROIを切り出し、ファインチューニングされたYOLOv5（`lp_det.pt`）で高精度位置特定。',
            '**第5段階 (超解像復元)**: ぼやけたプレート画像をEDSR_x4深層残差ネットワークで4倍高解像度化。',
            '**第6段階 (OCRと多数決投票)**: EasyOCRでの文字認識、正規表現フィルタ、複数フレーム間の時間的多数決投票による確定。'
        ],
        'h2_3': '3. システム設定とハードウェア最適化',
        'p_3': 'リアルタイムFPS制約と深層学習の演算負荷のバランスをとるため、CPUとGPUのハイブリッドパイプラインを構築しました:',
        'h2_4': '4. 次回予告',
        'p_4': '次回（第2編）では、ハフ変換を用いた動的車線検出、傾きフィルタリング、および車両バウンディングボックスと車線間の幾何学的IoU侵犯判定アルゴリズムを詳細に解説します。'
    },
    'es': {
        'title': '[Vision AI] Detección de Invasión de Carril en Caja Negra y ANPR con Superresolución: Pipeline de 6 Etapas y Desafíos en Tiempo Real (#1)',
        'description': 'Diseño de un pipeline de visión de 6 etapas que combina detección dinámica de carril, métricas de invasión IoU, detección de matrículas YOLOv5, superresolución EDSR y votación OCR.',
        'tags': ['computer-vision', 'anpr', 'object-detection', 'super-resolution', 'opencv', 'deep-learning'],
        'tldr_prob': 'Las grabaciones de baja resolución de cámaras de tablero (dashcam) sufren vibraciones, contraluces y desenfoque de movimiento, dificultando el reconocimiento de matrículas y el rastreo de invasión de carril.',
        'tldr_sol': 'Diseñamos una arquitectura integrada de 6 etapas: extracción de carril Canny/Hough -> detección de vehículos YOLOv3 -> cálculo de IoU de invasión -> localización de matrícula YOLOv5 -> superresolución EDSR_x4 -> votación temporal EasyOCR.',
        'tldr_res': 'Construimos un pipeline de extremo a extremo capaz de rastrear vehículos y monitorear límites de carril incluso bajo condiciones ópticas degradadas.',
        'h2_1': '1. El Desafío Real: Por qué la Visión en Cámaras de Tablero es Compleja',
        'p_1': 'La automatización de la vigilancia vial requiere alta confiabilidad. Sin embargo, las grabaciones de dashcam en vehículos en movimiento presentan severos artefactos de compresión, vibraciones de calzada y regiones de matrículas diminutas, a menudo menores a 40x20 píxeles.',
        'h2_2': '2. Arquitectura Jerárquica de 6 Etapas',
        'p_2': 'En lugar de aplicar una red neuronal pesada sobre todo el cuadro de 640x480, descompusimos la tarea en seis etapas especializadas:',
        'pipeline_steps': [
            '**Etapa 1 (Detección de Carril)**: Filtro de bordes Canny y HoughLinesP con máscara trapezoidal dinámica y umbrales de pendiente.',
            '**Etapa 2 (Detección de Vehículos)**: YOLOv3-tiny ligero que genera cuadros delimitadores rápidos.',
            '**Etapa 3 (Criterio de Invasión)**: Cálculo de Intersection-over-Union (IoU > 0.05) entre la base del vehículo y los carriles detectados.',
            '**Etapa 4 (Localización de Matrícula)**: Recorte del ROI del vehículo y detección precisa con YOLOv5 (`lp_det.pt`).',
            '**Etapa 5 (Superresolución)**: Restauración de parches de matrículas borrosas mediante la red neuronal profunda EDSR_x4.',
            '**Etapa 6 (OCR y Votación por Mayoría)**: Reconocimiento con EasyOCR, filtrado regex y motor de votación temporal entre fotogramas.'
        ],
        'h2_3': '3. Configuración del Sistema y Orquestación de Hardware',
        'p_3': 'Para equilibrar los requisitos de FPS en tiempo real con modelos pesados de deep learning, diseñamos un flujo híbrido CPU/GPU:',
        'h2_4': '4. Próxima Entrega',
        'p_4': 'En el próximo artículo (#2), profundizaremos en las matemáticas geométricas de la detección dinámica de carriles y el criterio de invasión basado en IoU.'
    }
}

print("Base schema loaded.")
