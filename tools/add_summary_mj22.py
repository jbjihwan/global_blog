import os

SUMMARIES = {
    "blog/2026-05-30-maeumjigi-22/index.md": """

---

## Summary & Key Takeaways

- **Over-Counseling Paradox Resolved**: Eliminated hyper-formal, robotic therapeutic reactions by curating a balanced 2:1 training data mix ratio of clinical counseling to daily casual chit-chat.
- **Golden Weight Checkpoint-4400**: Identified Checkpoint-4400 as our optimal fine-tuned weight, achieving the project's lowest validation loss (2.68) and peak human empathy scores.
- **Production Full-Stack Architecture**: Established an end-to-end serving blueprint integrating Next.js, FastAPI orchestration, vLLM continuous batching, and Redis session caching.
- **Milestone Validation**: Confirmed stable sub-second response latencies and high conversational fluency, completing our Phase 1 experimental modeling sprint.
""",
    "i18n/ko/docusaurus-plugin-content-blog/2026-05-30-maeumjigi-22/index.md": """

---

## 핵심 요약 및 배운 점

- **과상담(Over-Counseling) 트랩 종결**: 일상 인사에도 과도한 심리 치료 어투로 반응하던 문제를 해결하기 위해 심리 상담과 일상 대화를 2:1로 조합한 황금 데이터 믹스를 규명했습니다.
- **골든 가중치 Checkpoint-4400 확보**: 4차 파인튜닝 실험을 통해 검증 손실 2.68로 역대 최저치를 달성하고 정성 평가에서 가장 높은 공감 점수를 기록한 최적 가중치를 확보했습니다.
- **프로덕션 풀스택 서빙 아키텍처**: Next.js 프론트엔드, FastAPI 비동기 오케스트레이터, vLLM 고속 추론 엔진, Redis 세션 캐시를 결합한 상용급 시스템 파이프라인을 구축했습니다.
- **1단계 모델링 마일스톤 달성**: 1초 미만의 응답 지연 시간과 자연스러운 대화 전환을 입증하여 1학기 최종 방어 심사를 위한 완성도 높은 AI 코어를 확립했습니다.
""",
    "i18n/ja/docusaurus-plugin-content-blog/2026-05-30-maeumjigi-22/index.md": """

---

## まとめと要点

- **過剰カウンセリング問題の解決**: 日常的な会話にも過度に重い治療的応答をしてしまう問題を、専門相談と日常会話を2:1で配合した最適データミックスにより解決しました。
- **ゴールデン重み Checkpoint-4400 の確定**: 第4次ファインチューニングを通じて検証損失2.68の最小値を達成し、共感性評価で最高スコアを記録した最良モデルを確立しました。
- **本番向けフルスタックアーキテクチャ**: Next.js、FastAPI、vLLM高速推論エンジン、Redisセッションキャッシュを連携したエンドツーエンドのシステム基盤を完成させました。
- **フェーズ1モデル検証の達成**: 1秒未満の応答レイテンシと自然な対話フローを実現し、第1学期最終審査に向けた堅牢なAIコアを構築しました。
""",
    "i18n/es/docusaurus-plugin-content-blog/2026-05-30-maeumjigi-22/index.md": """

---

## Resumen y Puntos Clave

- **Resolucion de la Sobrecounseling**: Superada la reaccion terapeutica rigida e hiperformal en charlas cotidianas implementando una proporcion de mezcla de datos 2:1 (clinico frente a casual).
- **Identificacion del Checkpoint-4400 Dorado**: Confirmado el Checkpoint-4400 como el peso optimo, logrando la menor perdida de validacion del proyecto (2.68) y maximas puntuaciones de empatia humana.
- **Arquitectura Full-Stack de Produccion**: Integrado un pipeline integral con frontend en Next.js, orquestacion con FastAPI, inferencia acelerada con vLLM y cache de sesiones en Redis.
- **Validacion de Rendimiento en Tiempo Real**: Demostradas latencias de respuesta inferiores a un segundo y alta fluidez conversacional para la defensa final del semestre.
""",
    "i18n/zh-Hans/docusaurus-plugin-content-blog/2026-05-30-maeumjigi-22/index.md": """

---

## 核心总结与技术要点

- **攻克“过度心理咨询”病理缺陷**：通过创新设计的 2:1 黄金数据配比（66.7% 临床危机对话 + 33.3% 开放域日常社交闲聊），彻底治愈了模型草木皆兵的死板治疗反应。
- **锁定黄金权重 Checkpoint-4400**：在第 4 轮微调实验中，该检查点录得全项目历史最低验证集损失（2.68），并在人工盲测盲评中夺得同理心最高评分。
- **落地生产级全栈服务架构**：构建了无缝串联 Next.js 前端交互、FastAPI 异步编排调度、vLLM 连续批处理推理与 Redis 高速会话缓存的高可用生产底座。
- **达成一阶段模型收官里程碑**：实测端到端首字响应延迟稳定在 1 秒以内，为毕业设计第一学期终审答辩奠定了坚实的技术底牌。
""",
    "i18n/zh-Hant/docusaurus-plugin-content-blog/2026-05-30-maeumjigi-22/index.md": """

---

## 核心總結與技術要點

- **攻克「過度心理諮商」病理缺陷**：透過創新設計的 2:1 黃金數據配比（66.7% 臨床危機對話 + 33.3% 開放域日常社交閒聊），徹底治癒了模型草木皆兵的死板治療反應。
- **鎖定黃金權重 Checkpoint-4400**：在第 4 輪微調實驗中，該檢查點錄得全專案歷史最低驗證集損失（2.68），並在人工盲測盲評中奪得同理心最高評分。
- **落地生產級全端服務架構**：建立了無縫串聯 Next.js 前端互動、FastAPI 非同步編排調度、vLLM 連續批次處理推論與 Redis 高速對話快取的高可用生產底座。
- **達成一階段模型收官里程碑**：實測端到端首字響應延遲穩定在 1 秒以內，為畢業設計第一學期終審答辯奠定了堅實的技術底牌。
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
