# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-06-27-vision-anpr-3"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **The Global Search Bottleneck**: Detecting tiny $30 \\times 15$ pixel license plates directly on raw full-frame inputs triggers heavy background false positives from billboards and bogs down inference below 10 FPS.
2. **Two-Stage Hierarchical Localization**: Deploying lightweight YOLOv3-tiny for coarse vehicle ROI extraction followed by dedicated YOLOv5 plate detection within the vehicle patch eliminates 98% of false alarms.
3. **CSRT Correlation Filter Tracking**: Utilizing OpenCV CSRT tracker with a 15-frame periodic redetection schedule reduces full-model inference frequency while maintaining stable bounding box continuity.
4. **80% GPU Overhead Reduction & 50+ FPS**: Decoupling continuous detection from correlation tracking slashes GPU computational load by 80%, sustaining real-time processing exceeding 50 FPS.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **전체 화면 단일 검출의 한계**: $640 \\times 480$ 전체 프레임에서 $30 \\times 15$ 픽셀 수준의 미소 번호판을 직접 탐색하면 도로 표지판·간판 오탐율이 급증하고 처리 속도가 10 FPS 이하로 급락합니다.
2. **2단계 계층형 객체 검출(Hierarchical Detection)**: YOLOv3-tiny로 차량 관심 영역(ROI)을 1차 크롭한 뒤, 차량 내부에서 전용 YOLOv5 모델로 번호판을 2차 정밀 검출하여 오탐을 98% 제거했습니다.
3. **CSRT 상관 필터 기반 추적 연동**: 매 프레임 딥러닝 추론을 돌리는 대신 OpenCV CSRT 트래커를 결합하고 15프레임 주기 재검출 인터벌을 적용하여 추적 연속성을 확보했습니다.
4. **GPU 연산량 80% 절감 및 50+ FPS 달성**: 추적과 검출의 하이브리드 파이프라인 설계를 통해 GPU 부하를 80% 이상 감축하며 실시간 50 FPS 이상의 고속 처리를 완성했습니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **全画面単一推論の限界**: $640 \\times 480$ の画像全体から極小のナンバープレートを直接探索すると、看板等の誤検知が多発し推論速度も10 FPS未満に低下します。
2. **2段階の階層型オブジェクト検出**: 軽量なYOLOv3-tinyで車両領域(ROI)を大まかに切り出し、その内部でのみ特化型YOLOv5を走らせることで誤認を98%排除しました。
3. **CSRT相関フィルタ追跡の融合**: 毎フレームのDNN推論を避け、OpenCV CSRTトラッカーと15フレーム周期の再検出を組み合わせることで追跡の安定性と高速性を両立しました。
4. **GPU負荷80%削減と50+ FPSの実現**: 検出と追跡のハイブリッド設計によりGPUリソース消費を80%カットし、50 FPSを超える超高速リアルタイムパイプラインを確立しました。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **El Cuello de Botella de Detección Global**: Buscar placas diminutas de $30 \\times 15$ píxeles en el fotograma completo genera falsos positivos masivos con carteles y colapsa la tasa de cuadros por debajo de 10 FPS.
2. **Localización Jerárquica en Dos Etapas**: Usar YOLOv3-tiny para extraer la región de interés (ROI) del vehículo y un YOLOv5 especializado para la placa dentro de dicho recorte erradica el 98% de falsas alarmas.
3. **Seguimiento por Filtros de Correlación CSRT**: Integrar el rastreador CSRT de OpenCV con un intervalo de redetección periódica cada 15 fotogramas asegura la continuidad visual sin sobrecargar el pipeline.
4. **Reducción del 80% en GPU y 50+ FPS**: Al alternar inferencia y tracking por correlación, se alivia el cómputo de la GPU en un 80%, manteniendo más de 50 FPS estables en tiempo real.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **全图直接检测的工程缺陷**：在全景图像中直接搜寻 $30 \\times 15$ 像素的微小车牌极易将路旁广告牌误识为目标，且会导致帧率骤降至 10 FPS 以下。
2. **两阶段分层目标定位架构 (Hierarchical Detection)**：先借助轻量级 YOLOv3-tiny 快速截取车辆 ROI，再在限定区域内运行专用 YOLOv5 探测车牌，强力剔除 98% 的背景误报。
3. **融合 CSRT 相关滤波实时追踪**：规避逐帧运行深度神经网络，将 OpenCV CSRT 追踪器与 15 帧周期重检机制深度结合，完美维持目标框时序连续性。
4. **释放 80% GPU 算力并达标 50+ FPS**：通过“检测 + 相关滤波追踪”的混合调度，大幅削减 80% 的 GPU 运算负载，实现 50+ FPS 的高帧率实时交通监控。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **全圖直接檢測的工程缺陷**：在全景影像中直接搜尋 $30 \\times 15$ 像素的微小車牌極易將路旁廣告牌誤識為目標，且會導致幀率驟降至 10 FPS 以下。
2. **兩階段分層目標定位架構 (Hierarchical Detection)**：先藉助輕量級 YOLOv3-tiny 快速截取車輛 ROI，再在限定區域內運行專用 YOLOv5 探測車牌，強力剔除 98% 的背景誤報。
3. **融合 CSRT 相關濾波即時追蹤**：規避逐幀運行深度神經網路，將 OpenCV CSRT 追蹤器與 15 幀週期重檢機制深度結合，完美維持目標框時序連續性。
4. **釋放 80% GPU 算力並達標 50+ FPS**：透過「檢測 + 相關濾波追蹤」的混合排程，大幅削減 80% 的 GPU 運算負載，實現 50+ FPS 的高幀率即時交通監控。
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

print("Vision ANPR 3 summary injection finished successfully!")
