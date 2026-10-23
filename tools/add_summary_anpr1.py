# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-06-25-vision-anpr-1"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **The Real-World Dashcam Vision Barrier**: Low-resolution dashcam inputs suffer from severe vibration, optical blur, and compressed plates spanning merely $30 \\times 15$ pixels, rendering naive single-stage models ineffective.
2. **6-Stage Decoupled Pipeline Design**: Solves accuracy and throughput bottlenecks by orchestrating lane extraction, vehicle detection, polygon IoU violation calculation, localized plate cropping, EDSR super-resolution, and voting OCR.
3. **Hierarchical Compute Optimization**: Restricting intensive deep learning models to localized vehicle bounding boxes prevents catastrophic full-frame inference slowdowns.
4. **Edge Real-Time Feasibility**: Balancing correlation tracking and temporal voting enables continuous 50+ FPS video processing with deterministic 99.4% plate recognition reliability.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **블랙박스 영상의 광학적 한계**: $30 \\times 15$ 픽셀 수준의 극소형 번호판, 차량 진동, 노면 블러 및 압축 노이즈로 인해 단일 딥러닝 모델의 직접 판독은 오탐율이 극심합니다.
2. **6단계 분리형 파이프라인 아키텍처**: 차선 검출 → 차량 검출 → 폴리곤 IoU 침범 판정 → 번호판 ROI 크롭 → EDSR 초해상화 → 보팅 OCR로 이어지는 모듈형 계층 설계를 도입했습니다.
3. **계층적 연산 최적화**: 고부하 모델의 탐색 영역을 전체 프레임 대신 차량 내부 관심 영역(ROI)으로 한정하여 불필요한 GPU 연산 낭비를 차단했습니다.
4. **엣지 실시간 처리(50+ FPS) 구현**: 상관 필터 추적과 시간 축 다수결 보팅을 결합하여 실시간 50 FPS 이상의 고속 파이프라인과 99.4%의 결정론적 판독 신뢰도를 달성했습니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **車載カメラ映像の光学的課題**: $30 \\times 15$ ピクセル前後の極小プレート、振動、ブレ、圧縮歪みにより、単一モデルによる全画面直接認識は高い誤認率を招きます。
2. **6段階の疎結合パイプライン設計**: 車線抽出 → 車両検知 → ポリゴンIoU侵犯判定 → 局所プレート抽出 → EDSR超解像 → 多数決OCRという堅牢な多層アーキテクチャを構築しました。
3. **階層的な計算コスト最適化**: 重量級モデルの探索領域を車両ROI内に限定することで、全画面走査による致命的なフレームレート低下を回避しました。
4. **エッジ向けリアルタイム処理(50+ FPS)**: 追跡と時間軸アンサンブルの融合により、50 FPS超のリアルタイム推論と99.4%の決定論的認識精度を確立しました。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **La Barrera Óptica en Cámaras de Tablero**: Matrículas de apenas $30 \\times 15$ píxeles, vibraciones de carretera y artefactos de compresión inutilizan los modelos de detección directa en una sola etapa.
2. **Arquitectura Desacoplada en 6 Fases**: Estructura el flujo en extracción de carriles, detección vehicular, IoU poligonal, recorte de matrícula, superresolución EDSR y votación OCR temporal.
3. **Optimización Jerárquica del Cómputo**: Confinar la inferencia neuronal pesada a la ROI del vehículo evita la ralentización global y optimiza el uso de la GPU.
4. **Viabilidad en Tiempo Real Edge (50+ FPS)**: La alternancia con tracking por correlación permite procesar vídeo a más de 50 FPS continuos con una fiabilidad determinista del 99.4%.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **行车记录仪视觉的物理局限**：目标车牌尺寸仅占 $30 \\times 15$ 像素，伴随强烈车体颠簸与压缩噪点，单阶段端到端模型极易发生灾难性误判。
2. **6 阶段解耦式全栈架构设计**：通过“车道拟合 → 车辆定位 → 多边形 IoU 压线判据 → 车牌局部裁剪 → EDSR 超分辨率 → 表决 OCR”构建高鲁棒性工业闭环。
3. **分层计算算力优化策略**：将高开销深度模型严格限制在车辆 ROI 区域内执行，从架构层面避免全画幅特征图搜索带来的帧率崩溃。
4. **边缘端超实时性能落地 (50+ FPS)**：融合相关滤波追踪与时序多帧多数表决，实现 50+ FPS 的超高速流式处理及 99.4% 的确定性识别置信度。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **行車記錄器視覺的物理局限**：目標車牌尺寸僅佔 $30 \\times 15$ 像素，伴隨強烈車體顛簸與壓縮雜訊，單階段端到端模型極易發生災難性誤判。
2. **6 階段解耦式全端架構設計**：透過「車道擬合 → 車輛定位 → 多邊形 IoU 壓線判據 → 車牌局部裁剪 → EDSR 超解析度 → 表決 OCR」構建高魯棒性工業閉環。
3. **分層計算算力優化策略**：將高開銷深度模型嚴格限制在車輛 ROI 區域內執行，從架構層面避免全畫幅特徵圖搜尋帶來的幀率崩潰。
4. **邊緣端超即時效能落地 (50+ FPS)**：融合相關濾波追蹤與時序多幀多數表決，實現 50+ FPS 的超高速串流處理及 99.4% 的確定性辨識信賴度。
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

print("Vision ANPR 1 summary injection finished successfully!")
