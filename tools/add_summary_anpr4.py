# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-06-28-vision-anpr-4"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **The Low-Resolution Optical Barrier**: Cropped license plate patches from dashcam video often measure under $40 \\times 20$ pixels with heavy compression artifacts, causing standard bicubic interpolation to blur critical character strokes.
2. **EDSR_x4 Deep Super-Resolution**: By removing batch normalization layers, the EDSR residual architecture preserves pixel-level dynamic range and reconstructs sharp high-frequency edges via OpenCV `dnn_superres`.
3. **Temporal Multi-Frame Image Stacking**: Aligning and averaging $3 \\sim 5$ consecutive bounding box patches cancels out stochastic camera sensor noise and motion jitter before feeding the image to OCR.
4. **Massive OCR Accuracy Recovery**: The combined super-resolution and frame stacking pipeline quadruples pixel density, elevating downstream Korean character recognition rates from 32% to over 91%.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **저해상도 및 압축 노이즈의 한계**: 블랙박스 원거리 영상에서 크롭된 번호판은 $40 \\times 20$ 픽셀 미만의 극소형 크기와 H.264 압축 아티팩트로 인해 일반 보간법(Bicubic)으로는 글자 획이 뭉개집니다.
2. **EDSR_x4 딥러닝 초해상화 도입**: 배치 정규화(BatchNorm)를 제거하여 고주파 디테일의 동적 범위를 보존하는 EDSR 잔차 구조를 OpenCV `dnn_superres`로 구동하여 번호판 윤곽선을 복원합니다.
3. **다중 프레임 이미지 스태킹 (Image Stacking)**: 연속된 3~5개 프레임의 크롭 패치를 정렬 및 평균화하여 카메라 센서 노이즈와 블러를 상쇄하고 신호 대 잡음비(SNR)를 극대화합니다.
4. **OCR 인식률 극적 개선**: 해상도 4배 복원과 노이즈 캔슬링 파이프라인을 통해 하류 EasyOCR의 한글 및 숫자 판독 정확도를 기존 32%에서 91% 이상으로 대폭 끌어올렸습니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **低解像度と圧縮ノイズの壁**: ドライブレコーダー映像から切り出したナンバー画像は $40 \\times 20$ ピクセル未満と極小で、Bicubic補間では文字輪郭が潰れてOCRが不可能です。
2. **EDSR_x4 による深層超解像の導入**: バッチ正規化層を排して高周波テクスチャを保持するEDSR残差ネットワークをOpenCV `dnn_superres` で稼働させ、エッジを鮮明に復元します。
3. **時系列マルチフレーム画像スタッキング**: 連続する3〜5フレームのナンバー領域を位置合わせして平均合成することで、センサーノイズとモーションブラーを大幅に除去します。
4. **OCR認識精度の大幅向上**: 4倍の超解像処理と画像スタッキングの相乗効果により、EasyOCRの後続文字認識率を32%から91%超へと飛躍的に改善しました。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **La Barrera Óptica de Baja Resolución**: Las placas recortadas de cámaras de tablero miden menos de $40 \\times 20$ píxeles, donde la interpolación bicúbica tradicional solo incrementa el desenfoque sin aportar nitidez.
2. **Superresolución Profunda con EDSR_x4**: Al omitir la normalización por lotes, la red residual EDSR preserva el rango dinámico de píxeles y reconstruye bordes de alta frecuencia con OpenCV `dnn_superres`.
3. **Apilamiento Temporal Multifotograma**: El alineamiento y promediado de $3 \\sim 5$ fotogramas consecutivos cancela el ruido estocástico del sensor y el desenfoque por movimiento.
4. **Recuperación Masiva de Precisión OCR**: Esta combinación de superresolución y cancelación de ruido cuadruplica la densidad de píxeles, elevando el éxito de EasyOCR del 32% a más del 91%.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **低分辨率与压缩噪点瓶颈**：行车记录仪画面中裁切出的车牌区域往往不足 $40 \\times 20$ 像素，双三次插值 (Bicubic) 算法无法恢复因 H.264 压缩而丢失的文字笔画边缘。
2. **引入 EDSR_x4 深度残差超分辨率**：EDSR 架构剥离了批归一化 (BatchNorm) 层以保留像素级动态范围，依托 OpenCV `dnn_superres` 高效重建高频字符轮廓细节。
3. **时序多帧图像叠加降噪 (Image Stacking)**：对连续 $3 \\sim 5$ 帧的车牌候选框进行亚像素几何对齐并像素均值化，强力消除相机传感器随机噪点与抖动模糊。
4. **下游 OCR 准确率爆发式提升**：经由 4 倍超分与图像叠加复合增强，下游 EasyOCR 的复杂字符识别准确率由最初的 32% 跨越式跃升至 91% 以上。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **低解析度與壓縮雜訊瓶頸**：行車記錄器畫面中裁切出的車牌區域往往不足 $40 \\times 20$ 像素，雙三次插值 (Bicubic) 演算法無法恢復因 H.264 壓縮而遺失的文字筆畫邊緣。
2. **引入 EDSR_x4 深度殘差超解析度**：EDSR 架構剝離了批次正規化 (BatchNorm) 層以保留像素級動態範圍，依託 OpenCV `dnn_superres` 高效重建高頻字元輪廓細節。
3. **時序多幀影像疊加降噪 (Image Stacking)**：對連續 $3 \\sim 5$ 幀的車牌候選框進行亞像素幾何對齊並像素均值化，強力消除相機感測器隨機雜訊與抖動模糊。
4. **下游 OCR 準確率爆發式提升**：經由 4 倍超分與影像疊加複合增強，下游 EasyOCR 的複雜字元辨識準確率由最初的 32% 跨越式躍升至 91% 以上。
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

print("Vision ANPR 4 summary injection finished successfully!")
