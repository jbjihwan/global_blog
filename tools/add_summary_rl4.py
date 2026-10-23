# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-05-20-rl-qlearning-4"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **Zero-Exploration Deterministic Evaluation**: Evaluated the greedy policy with exploration set to zero (ε=0) across 30 trials and 5 evaluation seeds via `evaluate_qlearning.py` to verify true deployment readiness.
2. **Three-Dimensional Metric Triad**: Measured not just success rates, but path efficiency ratios against theoretical shortest paths and safety near-miss counts to guarantee collision avoidance.
3. **Triangular Benchmark (Q-Learning vs SARSA vs DQN)**: Tabular Q-Learning achieved 93.3% success in the 12-wall obstacle arena, outperforming on-policy SARSA (80.0%) and off-policy DQN (86.7%).
4. **Microcontroller Latency Dominance**: Discretized Q-table lookups executed in 0.02ms with negligible memory footprints, decisively outclassing deep neural network inference on constrained embedded hardware.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **무탐색 결정론적 평가 파이프라인**: 훈련 중의 확률적 잡음을 완전히 배제하고 탐색률을 0(ε=0)으로 고정한 뒤, 5개 평가 시드 기반의 30회 독립 주행(`evaluate_qlearning.py`)으로 배포 성능을 검증했습니다.
2. **3차원 정량 평가 지표 도입**: 단순 목적지 도달률 외에 이론적 최단 경로 대비 주행 효율(Path Efficiency)과 장애물 근접 위험도(Near-Miss)를 정량화하여 안전성을 입증했습니다.
3. **3각 벤치마크 (Q-Learning vs SARSA vs DQN)**: 복잡한 12벽 아레나에서 Tabular Q-Learning은 93.3%의 결정론적 성공률을 달성하여 SARSA(80.0%) 및 DQN(86.7%)을 능가했습니다.
4. **마이크로컨트롤러 최적화 추론 속도**: 룩업 테이블 기반 인퍼런스는 단 0.02ms만에 완료되어, 고사양 신경망 연산이 불가능한 저전력 임베디드 로봇 제어에 가장 적합함을 확인했습니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **完全決定論的評価パイプライン**: 探索ノイズを排除し ε=0 に固定した greedy 方策を `evaluate_qlearning.py` により 5 シード・30 試行で厳密に検証しました。
2. **多次元定量評価指標の導入**: 単なる到達成功率にとどまらず、理論的最短距離に対する移動効率比や障害物近接度（Near-Miss）を計測し安全走行を保証しました。
3. **3者比較ベンチマーク (Q-Learning vs SARSA vs DQN)**: 12壁の高難度アリーナにおいて、テーブル型Q学習が93.3%の決定論的成功率を記録し、SARSA(80.0%)やDQN(86.7%)を凌駕しました。
4. **組込みマイコン向けの超低遅延**: テーブル参照推論はわずか0.02msで完了し、ニューラルネットの重い行列演算が不可能な超低消費電力マイコンに最適な特性を実証しました。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **Evaluación Determinista sin Exploración**: Evaluó la política puramente voraz (ε=0) mediante `evaluate_qlearning.py` a lo largo de 30 ensayos independientes y 5 semillas de prueba.
2. **Tríada de Métricas de Calidad de Ruta**: Cuantificó la tasa de éxito, el ratio de eficiencia frente al camino óptimo teórico y el recuento de roces cercanos (Near-Miss) con muros.
3. **Benchmark Triangular (Q-Learning vs SARSA vs DQN)**: En la arena de 12 paredes, Q-Learning tabular alcanzó un 93.3% de éxito determinista, superando a SARSA (80.0%) y DQN (86.7%).
4. **Ventaja Extrema de Latencia Embebida**: Con un tiempo de inferencia de 0.02ms por búsqueda directa en tabla, superó decisivamente la sobrecarga neuronal de DQN en microcontroladores de baja potencia.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **零探索确定性评测流水线**：彻底剥离训练探索噪声，将探索率锁定为零 (ε=0)，依托 `evaluate_qlearning.py` 在 5 组独立评估随机种子上展开 30 轮确定性闭环推演。
2. **三维立体评估指标矩阵**：除终点抵达率外，创新引入理论最优路径效率比 (Path Efficiency) 与障碍物近距离惊险擦碰次数 (Near-Miss) 双重严苛安全度量。
3. **三方算法基准横评 (Q-Learning vs SARSA vs DQN)**：在 12 墙高阻碍迷宫中，表格型 Q-Learning 斩获 93.3% 的确定性通关率，显著超越同策略 SARSA (80.0%) 与离线 DQN (86.7%)。
4. **低功耗嵌入式端延时统治力**：基于状态索引的查表决策耗时仅 0.02ms，内存开销微乎其微，为低算力单片机机器人自主导航确立了算力能效典范。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **零探索確定性評測流水線**：徹底剝離訓練探索雜訊，將探索率鎖定為零 (ε=0)，依託 `evaluate_qlearning.py` 在 5 組獨立評估隨機種子上展開 30 輪確定性閉環推演。
2. **三維立體評估指標矩陣**：除終點抵達率外，創新引入理論最佳路徑效率比 (Path Efficiency) 與障礙物近距離驚險擦碰次數 (Near-Miss) 雙重嚴苛安全度量。
3. **三方演算法基準橫評 (Q-Learning vs SARSA vs DQN)**：在 12 牆高阻礙迷宮中，表格型 Q-Learning 斬獲 93.3% 的確定性通關率，顯著超越同策略 SARSA (80.0%) 與離線 DQN (86.7%)。
4. **低功耗嵌入式端延時統治力**：基於狀態索引的查表決策耗時僅 0.02ms，記憶體開銷微乎其微，為低算力單晶片機器人自主導航確立了算力能效典範。
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

print("RL Q-Learning 4 summary injection finished successfully!")
