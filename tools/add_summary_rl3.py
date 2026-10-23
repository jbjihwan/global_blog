import os

SUMMARIES = {
    "blog/2026-05-19-rl-qlearning-3/index.md": """

---

## Summary & Key Takeaways

- **Complex Obstacle Arena Design**: Configured a constrained 1.2m × 1.2m environment in Webots featuring 12 randomized interior wall blocks to evaluate non-trivial spatial pathfinding.
- **Dynamic Episode Management**: Implemented automatic collision thresholds, goal radius triggering, and programmatic episode resets via Webots Supervisor IPC.
- **Overcoming Local Minima**: Augmented reward shaping with negative gradient penalties against entrapment and oscillatory turning behaviors near corners.
- **Headless Training Acceleration**: Achieved over 1,000 episodes per hour by disabling 3D rendering and running the Webots physics engine in fast headless batch mode.
""",
    "i18n/ko/docusaurus-plugin-content-blog/2026-05-19-rl-qlearning-3/index.md": """

---

## 핵심 요약 및 배운 점

- **복합 장애물 아레나 환경 구축**: 12개의 내부 장애물 블록이 배치된 1.2m × 1.2m Webots 가상 환경을 구축하여 단순 직진을 넘어선 복합 경로 탐색 과제를 수립했습니다.
- **동적 에피소드 라이프사이클 관리**: 거리 센서 기반의 충돌 임계치 감지, 목표 도달 판정, Supervisor IPC를 통한 에피소드 자동 리셋 파이프라인을 구현했습니다.
- **국소 해(Local Minima) 탈출 기법**: 구석 갇힘 및 진동성 선회 패턴을 방지하기 위해 음수 구배 페널티와 직진 가중치 기반의 보상 성형(Reward Shaping)을 적용했습니다.
- **헤드리스 고속 학습 가속**: 3D 그래픽 렌더링을 비활성화한 헤드리스(Headless) 배치 모드를 통해 시간당 1,000회 이상의 에피소드를 초고속 학습할 수 있는 환경을 달성했습니다.
""",
    "i18n/ja/docusaurus-plugin-content-blog/2026-05-19-rl-qlearning-3/index.md": """

---

## まとめと要点

- **複合障害物アリーナの構築**: 12個の内部障害物ブロックを配置した1.2m × 1.2mのWebots仮想環境を構築し、高度な経路探索タスクを設計しました。
- **動的エピソード管理**: 距離センサーによる衝突検知、ゴール到達判定、Supervisor IPCを通じた自動エピソードリセットパイプラインを実装しました。
- **局所解（Local Minima）の回避**: コーナーでのスタックや振動旋回を防ぐため、負の勾配ペナルティと前進インセンティブを組み合わせた報酬成形（Reward Shaping）を適用しました。
- **ヘッドレス高速学習**: 3Dレンダリングを無効化したヘッドレスモードにより、物理演算のみを高速実行し、1時間あたり1,000エピソード以上の高効率学習を実現しました。
""",
    "i18n/es/docusaurus-plugin-content-blog/2026-05-19-rl-qlearning-3/index.md": """

---

## Resumen y Puntos Clave

- **Diseno de Arena con Obstaculos Complejos**: Configurado un entorno cerrado de 1.2m × 1.2m en Webots con 12 bloques internos para evaluar navegacion y planificacion no trivial.
- **Gestion Dinamica del Ciclo de Episodios**: Implementada deteccion automatica de colisiones mediante sensores de distancia, activacion de objetivos y reinicios por Supervisor IPC.
- **Superacion de Minimos Locales**: Aplicado moldeado de recompensas (Reward Shaping) con penalizaciones de gradiente negativo para evitar bloqueos y oscilaciones en esquinas.
- **Aceleracion de Entrenamiento Headless**: Logrado un rendimiento superior a 1,000 episodios por hora al desactivar la renderizacion 3D y ejecutar Webots en modo rapido.
""",
    "i18n/zh-Hans/docusaurus-plugin-content-blog/2026-05-19-rl-qlearning-3/index.md": """

---

## 核心总结与技术要点

- **复杂障碍物竞技场设计**：在 Webots 中搭建了包含 12 个内部障碍物方块的 1.2m × 1.2m 仿真竞技场，验证复杂空间内的自主避障路径规划。
- **动态回合生命周期管理**：结合距离传感器碰撞阈值检测、目标到达判定以及 Supervisor IPC 自动化重置机制，保障长周期无人值守训练。
- **克服局部最优解（Local Minima）**：针对死角停滞与震荡打转现象引入负梯度惩罚与前进激励奖励塑形（Reward Shaping），引导智能体果断逃逸。
- **无头（Headless）加速训练**：关闭 3D 图形渲染并开启 Webots 极速无头批处理模式，实现每小时超过 1,000 回合的高效离线训练吞吐量。
""",
    "i18n/zh-Hant/docusaurus-plugin-content-blog/2026-05-19-rl-qlearning-3/index.md": """

---

## 核心總結與技術要點

- **複雜障礙物競技場設計**：在 Webots 中建立了包含 12 個內部障礙物方塊的 1.2m × 1.2m 模擬競技場，驗證複雜空間內的自主避障路徑規劃。
- **動態回合生命週期管理**：結合距離感測器碰撞閾值檢測、目標到達判定以及 Supervisor IPC 自動化重設機制，保障長週期無人值守訓練。
- **克服局部最優解（Local Minima）**：針對死角停滯與震盪打轉現象引入負梯度懲罰與前進激勵獎勵塑形（Reward Shaping），引導智慧體果斷逃逸。
- **無頭（Headless）加速訓練**：關閉 3D 圖形渲染並開啟 Webots 極速無頭批次處理模式，實現每小時超過 1,000 回合的高效離線訓練吞吐量。
"""
}

base_dir = r"D:\ai\antigravity\global_blog"

for rel_path, summary_text in SUMMARIES.items():
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    summary_keywords = ["Summary & Key Takeaways", "핵심 요약 및 배운 점", "まとめと要点", "Resumen y Puntos Clave", "核心总结与技术要点", "核心總結與技術要點"]
    if any(kw in content for kw in summary_keywords):
        print(f"Summary already present in: {rel_path}")
        continue
    
    content = content.rstrip() + summary_text + "\n"
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated: {rel_path}")
