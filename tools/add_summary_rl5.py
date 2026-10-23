# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-05-21-rl-qlearning-5"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **Closing the Sim-to-Real Reality Gap**: Solves microcontroller computational limits (Arduino Uno 2KB SRAM) and physical wheel slip by zero-shot transferring the Webots-trained 648-state Q-Table to physical hardware.
2. **Distributed Brain-Muscle Architecture**: A host PC executes heavy OpenCV vision and tabular Q-learning inference, transmitting binary movement commands via HC-06 Bluetooth SPP at 115,200 baud to the Arduino PWM motor controller.
3. **Sub-Centimeter ArUco Vision Homography**: An overhead camera calibrated for barrel distortion tracks 6-DoF ArUco markers (`DICT_4X4_50`), transforming raw pixels into accurate real-world metric coordinates $(x, y, \\theta)$.
4. **86.7% Physical Hardware Target Success**: Achieved a 26/30 successful target-reaching benchmark in a physical $1.2\\text{m} \\times 1.2\\text{m}$ arena, demonstrating that discretized state spaces bridge the simulation-to-reality divide without on-device retraining.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **Sim-to-Real Reality Gap 극복**: 마이크로컨트롤러(Arduino Uno 2KB SRAM)의 연산 한계와 휠 슬립 오차를 Webots 가상 시뮬레이션에서 사전 훈련된 648개 상태 Q-Table 제로샷 이식으로 극복했습니다.
2. **분산형 두뇌-근육(Brain-Muscle) 아키텍처**: 고부하 컴퓨터 비전과 Q-Table 추론은 호스트 PC(두뇌)가 전담하고, 115,200 baud HC-06 블루투스 통신을 통해 아두이노(근육)가 모터 PWM을 실시간 제어합니다.
3. **서브 센티미터급 ArUco 비전 호모그래피**: 렌즈 왜곡을 보정한 천장 웹캠이 로봇 상단의 ArUco 마커(`DICT_4X4_50`)를 추적하고, 원근 호모그래피 변환을 통해 물리 좌표계 $(x, y, \\theta)$를 정밀 복원합니다.
4. **실제 하드웨어 성공률 86.7% 달성**: 가상 환경 정책을 실제 $1.2\\text{m} \\times 1.2\\text{m}$ 물리 아레나에 배포하여 30회 중 26회(86.7%) 목표 도달에 성공하며 재학습 없는 실물 로봇 제어를 입증했습니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **Sim-to-Real Reality Gapの克服**: マイコン(Arduino Uno 2KB SRAM)の計算限界と車輪スリップ誤差を、Webotsで事前学習した648状態のQ-Tableゼロショット転移により解決しました。
2. **分散型ブレイン・マッスル構成**: 高負荷な画像処理とQテーブル推論をホストPC（頭脳）が担い、115,200 baudのHC-06 Bluetooth経由でArduino（筋肉）へPWM制御指示をリアルタイム伝送します。
3. **ミリ単位精度のArUco視覚ホモグラフィ**: 歪み補正済み天井カメラがArUcoマーカー（`DICT_4X4_50`）を検出し、透視射影変換により実空間座標 $(x, y, \\theta)$ をリアルタイムに算出します。
4. **実機環境で86.7%の到達成功率を実証**: $1.2\\text{m} \\times 1.2\\text{m}$ の物理アリーナで30回中26回のゴール到達（86.7%）を記録し、追加学習なしでのシミュレーションから実機への完全移植を達成しました。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **Superación de la Brecha Realidad-Simulación**: Supera la memoria limitada del microcontrolador (Arduino Uno 2KB SRAM) y el deslizamiento mecánico transfiriendo la Q-Table de 648 estados entrenada en Webots.
2. **Arquitectura Distribuida Cerebro-Músculo**: El PC anfitrión ejecuta la visión artificial y la inferencia Q-Learning, enviando órdenes de movimiento por Bluetooth HC-06 a 115,200 baudios al Arduino para accionar los motores PWM.
3. **Homografía de Visión ArUco Subcentimétrica**: Una cámara cenital con corrección de distorsión óptica rastrea marcadores ArUco (`DICT_4X4_50`), mapeando píxeles a coordenadas métricas reales $(x, y, \\theta)$.
4. **86.7% de Éxito en Hardware Físico**: Registró 26 aciertos en 30 pruebas en un cuadrilátero físico de $1.2\\text{m} \\times 1.2\\text{m}$, demostrando que la discretización tabular cierra la brecha Sim-to-Real sin reentrenamiento.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **跨越 Sim-to-Real 仿真现实鸿沟**：针对嵌入式微控制器 (Arduino Uno 2KB SRAM) 极端算力瓶颈与物理打滑扰动，零样本迁移 Webots 仿真中淬炼的 648 状态 Q-Table。
2. **分布式大脑-肌肉 (Brain-Muscle) 架构**：上位机 PC 承担 OpenCV 视觉定位与 Q-Table 决策运算，通过 115,200 波特率的 HC-06 蓝牙串口向 Arduino 下发毫秒级电机 PWM 驱动指令。
3. **亚厘米级 ArUco 视觉单应性标定**：架设顶部超广角相机消除桶形畸变，高频追踪机体顶部的 ArUco 二维标章 (`DICT_4X4_50`)，经透视单应性变换解算物理位姿 $(x, y, \\theta)$。
4. **实体机器人达成 86.7% 导航成功率**：在 $1.2\\text{m} \\times 1.2\\text{m}$ 真实物理场地中斩获 30 轮测试中 26 次精准抵达目标点 (86.7%)，证实无需实机微调即可闭环控制。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **跨越 Sim-to-Real 模擬現實鴻溝**：針對嵌入式微控制器 (Arduino Uno 2KB SRAM) 極端算力瓶頸與物理打滑擾動，零樣本遷移 Webots 模擬中淬煉的 648 狀態 Q-Table。
2. **分散式大腦-肌肉 (Brain-Muscle) 架構**：上位機 PC 承擔 OpenCV 視覺定位與 Q-Table 決策運算，透過 115,200 鮑率的 HC-06 藍牙串列埠向 Arduino 下發毫秒級馬達 PWM 驅動指令。
3. **亞厘米級 ArUco 視覺單應性標定**：架設頂部超廣角相機消除桶形畸變，高頻追蹤機體頂部的 ArUco 二維標章 (`DICT_4X4_50`)，經透視單應性變換解算物理姿態 $(x, y, \\theta)$。
4. **實體機器人達成 86.7% 導航成功率**：在 $1.2\\text{m} \\times 1.2\\text{m}$ 真實物理場地中斬獲 30 輪測試中 26 次精準抵達目標點 (86.7%)，證實無需實機微調即可閉環控制。
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

print("RL Q-Learning 5 summary injection finished successfully!")
