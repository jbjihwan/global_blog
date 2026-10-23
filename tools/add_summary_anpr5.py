# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-06-29-vision-anpr-5"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **Korean License Plate Syntax Validation**: EasyOCR character output is strictly filtered against standardized Korean plate regex patterns (`^\d{2,3}[가-힣]\d{4}$`), discarding syntactically invalid character fragments.
2. **Temporal Sliding Window Majority Voting**: To counteract frame-level yaw, glare, and vibration, OCR hypotheses are buffered across a 7-frame sliding window, requiring 3 identical matches before confirming the plate.
3. **11-Iteration System Evolution (v01 to v11)**: Systematically progressed from unconstrained raw OCR gibberish on June 5 to deterministic, noise-resilient recognition (`64가1511`) on June 7 with 99.4% accuracy.
4. **End-to-End ITS Architectural Pipeline**: Concludes the 5-part series by unifying dynamic lane detection, polygon IoU violation checks, hierarchical YOLOv5 localization, CSRT tracking, EDSR super-resolution, and voting OCR into an edge-ready pipeline.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **국내 번호판 정규식 구문 검증**: EasyOCR 판독 결과를 표준 번호판 정규식(`^\d{2,3}[가-힣]\d{4}$`)으로 엄격히 필터링하여 노이즈로 인한 비정상 문자열을 원천 배제합니다.
2. **시간 축 다수결 보팅 앙상블(Temporal Majority Voting)**: 차량 흔들림과 빛 반사로 인한 프레임별 오인식을 극복하기 위해 7프레임 슬라이딩 윈도우 버퍼에서 3회 이상 일치할 때만 번호판을 최종 확정합니다.
3. **11단계 아키텍처 진화 (v01 → v11)**: 6월 5일 초기 판독 실패(`ACCIIXOY-1Z01...`)에서 시작하여 6월 7일 결정론적 고신뢰 판독(`64가1511`, 신뢰도 99.4%)을 달성하기까지의 11단계 고도화 과정을 완성했습니다.
4. **엔드투엔드 ANPR 파이프라인 완성**: 동적 차선 인식, 폴리곤 IoU 침범 판정, 계층형 YOLOv5 검출, CSRT 추적, EDSR 초해상화, 보팅 OCR을 통합하여 엣지 배포 가능한 상용 수준의 지능형 교통 시스템을 구축했습니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **正規表現によるナンバー構文検証**: EasyOCRの出力文字列を韓国標準規格(`^\d{2,3}[가-힣]\d{4}$`)で厳格に正規表現照合し、ノイズ起因の不正な断片文字列を排除します。
2. **時間軸スライディングウィンドウ多数決(Voting)**: 車両の揺れや逆光による単一フレーム誤読を防ぐため、直近7フレームのバッファ内で3回以上一致した場合にのみ確定する多数決アンサンブルを構築しました。
3. **11段階のシステム進化 (v01 → v11)**: 初期バージョンの意味不明な文字化け出力から、ノイズを完全に克服した高信頼確定（`64가1511`, 精度99.4%）に至る11回の技術的改善を完遂しました。
4. **統合ITSビジョンパイプラインの完成**: 車線逸脱IoU判定、階層型YOLO検出、CSRT追跡、EDSR超解像、多数決OCRをシームレスに統合し、商用エッジAIに耐えうる交通管制基盤を確立しました。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **Validación Sintáctica de Matrículas**: Filtra las predicciones de EasyOCR mediante expresiones regulares estrictas (`^\d{2,3}[가-힣]\d{4}$`), descartando caracteres espurios generados por ruido visual.
2. **Ensemble de Votación por Ventana Deslizante Temporal**: Supera vibraciones y destellos ópticos almacenando lecturas en un búfer de 7 fotogramas, confirmando la matrícula solo tras 3 coincidencias idénticas consecutivas.
3. **Evolución en 11 Iteraciones (v01 a v11)**: Del texto incoherente inicial del 5 de junio al reconocimiento determinista y robusto del 7 de junio (`64가1511`) con una fiabilidad del 99.4%.
4. **Cierre de la Arquitectura Integral de Tráfico**: Culmina la serie unificando seguimiento de carriles, IoU de invasión poligonal, detección jerárquica YOLO, seguimiento CSRT, superresolución EDSR y OCR con votación.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **车牌语法正则校验**：借助韩国机动车号牌标准正则式 (`^\d{2,3}[가-힣]\d{4}$`) 过滤 EasyOCR 字符流，从源头剔除因光照与抖动产生的畸变字符。
2. **时序滑动窗口多数表决引擎 (Temporal Majority Voting)**：引入 7 帧时序缓冲队列，要求同构识别结果命中 3 次以上方予以最终确认，彻底解决单帧置信度漂移。
3. **历经 11 次工程迭代进化 (v01 → v11)**：系统从 6 月 5 日的严重乱码输出 (`ACCIIXOY-1Z01...`) 蜕变为 6 月 7 日的超高可靠确定性识别 (`64가1511`, 准确率 99.4%)。
4. **构建端到端 ITS 视觉全栈闭环**：贯通动态车道线拟合、多边形 IoU 压线违章判定、分层 YOLOv5 定位、CSRT 追踪、EDSR 超分辨率与表决 OCR，打造工业级边缘视觉系统。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **車牌語法正規表示式校驗**：藉助韓國機動車號牌標準正規式 (`^\d{2,3}[가-힣]\d{4}$`) 過濾 EasyOCR 字元串流，從源頭剔除因光照與抖動產生的畸變字元。
2. **時序滑動窗口多數表決引擎 (Temporal Majority Voting)**：引入 7 幀時序緩衝佇列，要求同構識別結果命中 3 次以上方予以最終確認，徹底解決單幀信賴度漂移。
3. **歷經 11 次工程迭代進化 (v01 → v11)**：系統從 6 月 5 日的嚴重亂碼輸出 (`ACCIIXOY-1Z01...`) 蛻變為 6 月 7 日的超高可靠確定性識別 (`64가1511`, 準確率 99.4%)。
4. **構建端到端 ITS 視覺全端閉環**：貫通動態車道線擬合、多邊形 IoU 壓線違章判定、分層 YOLOv5 定位、CSRT 追蹤、EDSR 超解析度與表決 OCR，打造工業級邊緣視覺系統。
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

print("Vision ANPR 5 summary injection finished successfully!")
