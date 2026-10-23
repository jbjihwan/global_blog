import os

SUMMARIES = {
    "blog/2026-05-18-rl-qlearning-2/index.md": """

---

## Summary & Key Takeaways

- **Bellman Optimality Formulation**: Formulated tabular Q-value updates with learning rate α = 0.1 and discount factor γ = 0.95 to guarantee mathematical convergence across discrete state transitions.
- **Multi-Objective Reward Shaping**: Engineered a balanced reward function combining distance-delta incentives (+10 × Δd), goal arrival bonuses (+100), step costs (-0.1), and collision penalties (-50).
- **Adaptive Exploration Schedule**: Applied an exponential ε-decay policy from 1.0 down to a floor of 0.05 over 1,000 episodes, effectively balancing exploration with exploitation.
- **Empirical Convergence**: Validated rapid policy convergence within 300 to 500 episodes in open benchmark environments before scaling to obstacle-dense arenas.
""",
    "i18n/ko/docusaurus-plugin-content-blog/2026-05-18-rl-qlearning-2/index.md": """

---

## 핵심 요약 및 배운 점

- **벨만 최적 방정식 수립**: 학습률 α = 0.1 및 할인율 γ = 0.95를 적용한 Tabular Q-Learning 업데이트 수식을 정립하여 이산 상태 전이에서의 수렴성을 확보했습니다.
- **다목적 보상 성형(Reward Shaping)**: 목표 거리 감소 인센티브(+10 × Δd), 도달 보너스(+100), 타임스텝 소모 페널티(-0.1), 벽 충돌 페널티(-50)를 결합한 최적 보상 함수를 설계했습니다.
- **적응형 탐색 스케줄(ε-Decay)**: 초기 1.0에서 최저 0.05까지 지수적으로 감소하는 엡실론 감쇠 정책을 적용하여 초기 광범위 탐색과 후반 최적 경로 활용(Exploitation)의 균형을 완성했습니다.
- **수렴 검증 및 성능 확인**: 평원 환경에서 300~500 에피소드 이내에 안정적으로 최단 경로 정책에 수렴함을 실험적으로 검증하여 복합 장애물 환경으로의 확장 기반을 마련했습니다.
""",
    "i18n/ja/docusaurus-plugin-content-blog/2026-05-18-rl-qlearning-2/index.md": """

---

## まとめと要点

- **ベルマン最適方程式の定式化**: 学習率 α = 0.1、割引率 γ = 0.95 を採用したQ値更新則を構築し、離散状態空間における数学的収束性を保証しました。
- **多目的報酬成形（Reward Shaping）**: ゴール接近インセンティブ（+10 × Δd）、到達ボーナス（+100）、ステップコスト（-0.1）、壁衝突ペナルティ（-50）を組み合わせたバランス設計を行いました。
- **ε-Decay探査スケジューリング**: 初期値 1.0 から下限 0.05 まで指数関数的に減衰する探索戦略を実装し、広範な初期探索と後期の活用（Exploitation）を両立させました。
- **実験的収束の検証**: 障害物のない環境において300〜500エピソードで最短経路ポリシーへ安定収束することを確認し、複雑マップ検証への確固たる基盤を確立しました。
""",
    "i18n/es/docusaurus-plugin-content-blog/2026-05-18-rl-qlearning-2/index.md": """

---

## Resumen y Puntos Clave

- **Optimizacion de Ecuaciones de Bellman**: Formulada la actualizacion tabular con tasa de aprendizaje α = 0.1 y factor de descuento γ = 0.95 para garantizar convergencia matematica.
- **Moldeado de Recompensas Multiobjetivo**: Disenada una funcion de recompensas equilibrada con incentivos por reduccion de distancia (+10 × Δd), bonus de llegada (+100), coste de tiempo (-0.1) y penalizacion por colision (-50).
- **Estrategia de Exploracion Adaptativa**: Aplicado un decaimiento exponencial ε de 1.0 a 0.05 a lo largo de 1,000 episodios para balancear exploracion y explotacion.
- **Validacion de Convergencia**: Verificada la convergencia estable a politicas optimas entre 300 y 500 episodios en pistas abiertas antes de escalar a laberintos densos.
""",
    "i18n/zh-Hans/docusaurus-plugin-content-blog/2026-05-18-rl-qlearning-2/index.md": """

---

## 核心总结与技术要点

- **贝尔曼最优方程公式化**：设定学习率 α = 0.1 与折扣因子 γ = 0.95 构建表格型 Q 值更新准则，在离散状态空间下确保算法收敛的数学确定性。
- **多目标奖励塑形（Reward Shaping）**：精心配置逼近目标增量激励（+10 × Δd）、目标终点奖励（+100）、时间步消耗惩罚（-0.1）与碰撞严厉惩罚（-50）。
- **自适应探索衰减调度（ε-Decay）**：采用从 1.0 指数衰减至底线 0.05 的 ε-贪婪策略，完美平衡了前期全局试错探索与后期确定性收益利用。
- **实证收敛效率验证**：在开阔竞技场基准测试中，算法在 300 至 500 回合内迅速收敛至最短最优路径，为应对复杂墙体迷宫奠定了坚实算法基石。
""",
    "i18n/zh-Hant/docusaurus-plugin-content-blog/2026-05-18-rl-qlearning-2/index.md": """

---

## 核心總結與技術要點

- **貝爾曼最佳方程式公式化**：設定學習率 α = 0.1 與折扣因子 γ = 0.95 建立表格型 Q 值更新準則，在離散狀態空間下確保演算法收斂的數學確定性。
- **多目標獎勵塑形（Reward Shaping）**：精心配置逼近目標增量激勵（+10 × Δd）、目標終點獎勵（+100）、時間步消耗懲罰（-0.1）與碰撞嚴厲懲罰（-50）。
- **自適應探索衰減調度（ε-Decay）**：採用從 1.0 指數衰減至底線 0.05 的 ε-貪婪策略，完美平衡了前期全域試錯探索與後期確定性收益利用。
- **實證收斂效率驗證**：在開闊競技場基準測試中，演算法在 300 至 500 回合內迅速收斂至最短最佳路徑，為應對複雜牆體迷宮奠定了堅實演算法基石。
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
