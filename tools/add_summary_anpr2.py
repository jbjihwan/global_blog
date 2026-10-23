# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-06-26-vision-anpr-2"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **Vanishing-Point Trapezoidal Masking**: Focusing edge analysis within a geometric perspective ROI eliminates 95% of irrelevant roadside background clutter and false edge artifacts.
2. **Probabilistic Hough Transform & Slope Filtering**: Applying `HoughLinesP` combined with strict slope boundaries ($|\\text{slope}| > 0.5$) separates true lane markers from pavement cracks and tar seams.
3. **Temporal Moving Average Smoothing**: Buffering slope and intercept coefficients across a 7-frame temporal queue prevents erratic lane jitter caused by bumps and lighting changes.
4. **Geometric Polygon IoU Intrusion Criterion**: Replaces naive point-in-polygon checks with strict tire-footprint intersection-over-union (IoU), reliably triggering violation events without false alarms.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **소실점 사다리꼴 ROI 마스킹**: 원근 투시 변환 영역에 맞춘 사다리꼴 마스크를 적용하여 도로변 구조물과 하늘 등 95% 이상의 불필요한 배경 노이즈를 사전에 차단했습니다.
2. **확률적 허프 변환 및 기울기 필터링**: Canny 엣지와 `HoughLinesP`를 결합하고 임계 기울기($|\\text{slope}| > 0.5$) 조건을 부여하여 아스팔트 균열과 타르 자국을 차선에서 완벽히 분리했습니다.
3. **7프레임 이동 평균 큐 스무딩**: 프레임별 차선 기울기와 절편을 7프레임 이동 평균 큐로 완충하여 노면 요철이나 조명 변화에 따른 차선 흔들림을 안정화했습니다.
4. **기하학적 폴리곤 IoU 침범 판정**: 단순 좌표 검사 대신 타이어 접지면 폴리곤과 차선 경계선 간의 기하학적 교차(IoU)를 정량 계산하여 차선 침범 이벤트를 정밀 감지합니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **消失点台形ROIマスキング**: 遠近法に基づいた台形マスクを適用することで、路肩の看板や空など95%以上の無関係なエッジノイズをカットします。
2. **確率的ハフ変換と傾きフィルタリング**: Canny輪郭抽出に `HoughLinesP` と傾き閾値制約（$|\\text{slope}| > 0.5$）を適用し、道路の亀裂や影を本物の白線から分離します。
3. **7フレーム移動平均によるジッター抑制**: 検出された直線パラメータを直近7フレームの移動平均で平滑化し、路面の振動による車線検出の激しいブレを防止します。
4. **幾何学的ポリゴンIoU侵犯判定**: 単純な点接触判定ではなく、車両タイヤ接地ポリゴンと車線間の幾何学的IoUを算出して確実な車線逸脱・侵犯を判定します。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **Enmascaramiento Trapezoidal con Punto de Fuga**: Confinar la detección de bordes a una ROI trapezoidal perspectival descarta más del 95% de artefactos de fondo ajenos a la calzada.
2. **Transformada de Hough Probabilística y Filtrado de Pendiente**: Combina Canny y `HoughLinesP` con restricciones de pendiente ($|\\text{pendiente}| > 0.5$) para aislar líneas reales de grietas en el pavimento.
3. **Suavizado por Media Móvil de 7 Fotogramas**: Amortigua los coeficientes de recta en una cola temporal de 7 fotogramas, eliminando oscilaciones visuales por baches o cambios de luz.
4. **Criterio Geométrico de Invasión por IoU de Polígonos**: Evalúa la intersección entre la huella de los neumáticos y el carril mediante IoU, asegurando alertas precisas sin falsas alarmas.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **灭点梯形透视 ROI 掩膜**：基于道路灭点建立梯形感兴趣区域掩码，预先过滤超 95% 的路侧广告牌、天空与无关边缘噪点。
2. **概率霍夫变换与斜率严密过滤**：深度融合 Canny 边缘算子与 `HoughLinesP`，施加斜率阈值约束 ($|\\text{slope}| > 0.5$)，精准剥离沥青裂缝与阴影干扰。
3. **7 帧时序滑动平均平滑队列**：对车线拟合参数建立 7 帧移动均值滤波，彻底抚平因路面颠簸与光影瞬变导致的车道线剧烈抖动。
4. **几何多边形 IoU 压线侵入判据**：摒弃粗糙的单点碰撞检测，计算车轮接地多边形与车道实线的几何交并比 (IoU)，实现高精度违章压线事件触发。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **滅點梯形透視 ROI 遮罩**：基於道路滅點建立梯形感興趣區域遮罩，預先過濾超 95% 的路側廣告牌、天空與無關邊緣雜訊。
2. **機率霍夫變換與斜率嚴密過濾**：深度融合 Canny 邊緣運算子與 `HoughLinesP`，施加斜率閾值約束 ($|\\text{slope}| > 0.5$)，精準剝離瀝青裂縫與陰影干擾。
3. **7 幀時序滑動平均平滑佇列**：對車線擬合參數建立 7 幀移動均值濾波，徹底撫平因路面顛簸與光影瞬變導致的車道線劇烈抖動。
4. **幾何多邊形 IoU 壓線侵入判據**：釋棄粗糙的單點碰撞檢測，計算車輪接地多邊形與車道實線的幾何交並比 (IoU)，實現高精度違章壓線事件觸發。
"""

def append_summary(file_path, summary_text):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "Executive Summary" in content or "최종 요약" in content or "Resumen Ejecutivo" in content or "核心总结" in content or "核心總結" in content:
        print(f"Summary already present in {file_path}")
        return
    
    new_content = content.rstrip() + "\n\n" + summary_text.strip() + "\n"
    new_content = re.sub(r'---\s*\r?\n\s*---', '---', new_content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Appended summary to: {file_path}")

# Apply to all 6 locales (at bottom of file)
append_summary(f"{gb_root}/blog/{folder_name}/index.md", en_summary)
append_summary(f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md", ko_summary)
append_summary(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_summary)
append_summary(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_summary)
append_summary(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_summary)
append_summary(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_summary)

print("Vision ANPR 2 summary injection finished successfully!")
