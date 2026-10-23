import os

SUMMARIES = {
    "blog/2026-06-18-maeumjigi-23/index.md": """

---

## Summary & Key Takeaways

- **Dual-Layer Safety Wrapper Architecture**: Engineered a mission-critical guardrail combining pre-inference crisis keyword/semantic triage with post-generation ethical compliance checks.
- **Zero-Hallucination Emergency Routing**: Implemented deterministic emergency bypass protocols that immediately route high-risk suicidal ideation directly to 24/7 lifeline hotlines.
- **Production GPU Serving Economics**: Benchmarked AWS EC2 `g5.2xlarge` (NVIDIA A10G 24GB) instances, establishing 60+ concurrent session capacity within an optimized student capstone budget.
- **Semester 1 Final Defense Success**: Concluded Phase 1 with a successful faculty defense, validating end-to-end clinical empathy, pipeline safety, and system resilience.
""",
    "i18n/ko/docusaurus-plugin-content-blog/2026-06-18-maeumjigi-23/index.md": """

---

## 핵심 요약 및 배운 점

- **이중 계층 안전 래퍼(Safety Wrapper) 구축**: 추론 전 위기 키워드 및 의미론적 분류 트리아지와 생성 후 임상 윤리 검증을 결합한 무결점 가드레일 아키텍처를 구현했습니다.
- **위기 즉각 개입 프로토콜**: 자살 고위험군 발언 감지 시 LLM 환각 가능성을 차단하고 24시간 자살예방 상담전화 및 긴급 기관으로 즉각 우회 라우팅하는 결정론적 방어선을 구축했습니다.
- **상용 클라우드 GPU 서빙 비용 최적화**: AWS EC2 `g5.2xlarge`(NVIDIA A10G 24GB) 인스턴스를 벤치마킹하여 예산 범위 내에서 60명 동시 접속을 수용하는 경제적 서빙 파이프라인을 확립했습니다.
- **1학기 캡스톤 최종 심사 통과**: 기술 검증 및 임상 공감도 시연을 통해 1학기 최종 발표 평가를 우수한 성적으로 마무리하며 2학기 현장 실증의 토대를 완성했습니다.
""",
    "i18n/ja/docusaurus-plugin-content-blog/2026-06-18-maeumjigi-23/index.md": """

---

## まとめと要点

- **2層セーフティラッパー（Safety Wrapper）の構築**: 推論前の危機キーワード・意味分類トリアージと、生成後の臨床倫理検証を組み合わせた安全アーキテクチャを実装しました。
- **緊急即時バイパスプロトコル**: 自殺高リスク発言を検知した場合、LLMのハルシネーションを排除し、24時間相談窓口へ即座に誘導する決定論的フェイルセーフを確立しました。
- **本番GPUサービングのコスト最適化**: AWS EC2 `g5.2xlarge`（NVIDIA A10G 24GB）を検証し、予算制約下で60ユーザー同時アクセスを処理できる高効率インフラを策定しました。
- **第1学期キャップストーン最終審査合格**: 技術実証と共感対話デモを通じて学部最終審査を成功裏に終え、第2学期の実フィールド展開への足がかりを築きました。
""",
    "i18n/es/docusaurus-plugin-content-blog/2026-06-18-maeumjigi-23/index.md": """

---

## Resumen y Puntos Clave

- **Arquitectura de Safety Wrapper de Doble Capa**: Implementado un guardarrail critico que combina triaje semantico previo con validacion etica posterior a la generacion.
- **Protocolo de Intervencion Inmediata en Crisis**: Disenado un bypass determinista que redirige inmediatamente expresiones suicidas de alto riesgo hacia lineas de ayuda 24/7 sin riesgo de alucinacion.
- **Optimizacion de Costes de GPU en Cloud**: Evaluada la instancia AWS EC2 `g5.2xlarge` (NVIDIA A10G 24GB) para soportar mas de 60 sesiones concurrentes dentro del presupuesto academico.
- **Defensa Exitosa del Capstone Semestre 1**: Concluido el primer semestre con una evaluacion sobresaliente del tribunal universitario, validando la empatia clinica y la robustez del sistema.
""",
    "i18n/zh-Hans/docusaurus-plugin-content-blog/2026-06-18-maeumjigi-23/index.md": """

---

## 核心总结与技术要点

- **双层安全包装器（Safety Wrapper）架构**：结合推理前的危机关键词与语义分类分流，以及推理后的临床伦理合规校验，构建了零容错的安全护栏。
- **自杀危机实时阻断与确定性路由**：一旦识别极高危自杀倾向，坚决切断模型幻觉，毫秒级直接旁路引流至官方 24 小时生命救助热线。
- **生产级云端 GPU 推理成本精算**：实测 AWS EC2 `g5.2xlarge`（NVIDIA A10G 24GB）实例，在严格项目预算内达成支撑 60 路并发对话的高效吞吐。
- **大一学期毕业设计终审答辩通关**：圆满完成第一阶段答辩，全面验证了端到端临床共情度、护栏拦截准确率以及工程高可用底座。
""",
    "i18n/zh-Hant/docusaurus-plugin-content-blog/2026-06-18-maeumjigi-23/index.md": """

---

## 核心總結與技術要點

- **雙層安全包裝器（Safety Wrapper）架構**：結合推論前的危機關鍵詞與語意分類分流，以及推論後的臨床倫理合規校驗，建立了零容錯的安全護欄。
- **自殺危機即時阻斷與確定性路由**：一旦識別極高危自殺傾向，堅決切斷模型幻覺，毫秒級直接旁路引流至官方 24 小時生命救助專線。
- **生產級雲端 GPU 推論成本精算**：實測 AWS EC2 `g5.2xlarge`（NVIDIA A10G 24GB）實例，在嚴格專案預算內達成支撐 60 路並發對話的高效吞吐。
- **大一學期畢業設計終審答辯通關**：圓滿完成第一階段答辯，全面驗證了端到端臨床共情度、護欄攔截準確率以及工程高可用底座。
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
