# -*- coding: utf-8 -*-
import os

gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-10-22\stanford_cs146s_1"
folder_name = "2026-10-22-stanford-cs146s-1"

# 1. English Summary
en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **The Paradigm Shift**: Software engineers have transitioned from manual syntax typists into system orchestra conductors commanding autonomous AI agent squads.
2. **Spec-Driven Development (SDD)**: High-leverage engineering now centers on formalizing invariants and boundary constraints in machine-actionable `SPEC.md` documents rather than typing implementation details.
3. **Loop Engineering & MCP**: Effective AI workflows rely on iterative, self-healing feedback loops backed by automated deterministic test suites and the Model Context Protocol (MCP).
4. **The Reviewer's Burden**: As AI code generation costs approach zero, foundational computer science mastery (operating systems, data structures, concurrency) becomes exponentially more critical for auditing subtle architectural vulnerabilities.
"""

# 2. Korean Summary
ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **패러다임 대전환**: 소프트웨어 엔지니어의 역할이 문법을 손으로 치는 '코드 타이피스트'에서 AI 에이전트 편대를 이끄는 '시스템 오케스트라 지휘자'로 완전히 전환되었습니다.
2. **스펙 주도 개발 (SDD)**: "어떻게(How)" 코딩할지 지시하는 대신, 불변 조건과 성공 기준을 엄격하게 명세한 `SPEC.md`를 설계하는 것이 핵심 역량입니다.
3. **루프 엔지니어링 & MCP**: 단발성 답변에 의존하지 않고, 모델 컨텍스트 프로토콜(MCP)과 자동화 단위 테스트를 결합한 자가 복구 피드백 루프를 구축해야 합니다.
4. **기본기의 역설**: AI가 코드를 빠르게 생성할수록 복잡한 동시성 버그, 알고리즘 병목, 보안 취약점을 검증하기 위한 컴퓨터공학 기초(자료구조·운영체제)가 훨씬 더 중요해집니다.
"""

# 3. Japanese Summary
ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **パラダイムの大転換**: ソフトウェアエンジニアの役割は、手動で構文を入力する「コードタイピスト」から、自律型AIエージェントチームを統率する「オーケストラの指揮者」へと進化しました。
2. **仕様駆動開発 (SDD)**: 実装方法を指示するのではなく、不変条件と受け入れ基準を厳格に定めた `SPEC.md` を設計することが現代エンジニアの最重要スキルです。
3. **ループ工学とMCP**: 単発の回答を期待するのではなく、Model Context Protocol (MCP) と自動単体テストを連動させた自己修復フィードバックループを構築します。
4. **基礎知識の重要性**: AIが高速にコードを生成するからこそ、隠れた並行性バグや脆弱性を見抜くためのコンピュータ科学の基礎（データ構造、OS、分散システム）が極めて重要になります。
"""

# 4. Spanish Summary
es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **El Cambio de Paradigma**: El ingeniero de software pasa de ser un mecanógrafo de sintaxis a un director de orquesta que coordina escuadrones de agentes de IA autónomos.
2. **Desarrollo Guiado por Especificaciones (SDD)**: La habilidad de mayor impacto consiste en diseñar documentos formales `SPEC.md` con invariantes y criterios de aceptación deterministas en lugar de escribir código repetitivo.
3. **Ingeniería de Bucles y MCP**: Los flujos de trabajo de alto rendimiento se basan en bucles de retroalimentación autorreparables respaldados por pruebas automatizadas y el Model Context Protocol (MCP).
4. **La Carga del Revisor**: Con la generación de código a coste marginal casi nulo, los fundamentos de ciencias de la computación (sistemas operativos, concurrencia, algoritmos) son más críticos que nunca para auditar vulnerabilidades sutiles.
"""

# 5. Simplified Chinese Summary
zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **范式巨变**：软件工程师的角色从手工敲击语法的“代码打字员”，彻底转变为调度自律 AI 智能体编队的“系统交响乐指挥家”。
2. **规范驱动开发 (SDD)**：工程核心杠杆在于设计机器可读的 `SPEC.md` 规范与边界不变量契约，而非在对话框中手写具体实现细节。
3. **闭环工程与 MCP**：不再依赖单次直出的代码，而是结合模型上下文协议 (MCP) 与确定性单元测试，构建具备自动自愈能力的工程闭环。
4. **计算机基础的逆向升值**：AI 生成代码速度越快，为排查隐蔽死锁、算法性能瓶颈与安全漏洞所需的底层体系结构与操作系统知识就越显无可替代。
"""

# 6. Traditional Chinese Summary
zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **典範轉移**：軟體工程師的角色從純手工敲擊語法的「程式碼打字員」，徹底轉變為調度多個 AI 智慧代理人的「系統交響樂指揮家」。
2. **規範驅動開發 (SDD)**：工程高槓桿的核心在於撰寫機器可讀的 `SPEC.md` 規格書與邊界不變量契約，而非手寫瑣碎的實作細節。
3. **閉環工程與 MCP**：摒棄單次對話直出程式碼的幻覺，全面結合模型上下文協定 (MCP) 與自動化單元測試，打造具備自動修復能力的工程反饋迴路。
4. **底層基礎的關鍵價值**：AI 產出程式碼的成本趨近於零，審查並排查複雜競爭狀態、效能瓶頸與安全漏洞所需的底層基礎知識反而變得更加不可或缺。
"""

# 7. Naver Blog Summary
nb_summary = """
---

## 📌 3~5줄 최종 요약
1. **역할의 전환**: 코딩 문법을 손으로 치던 '타이피스트'에서 AI 에이전트 편대를 이끄는 '오케스트라 지휘자'로 개발자의 정체성이 진화했습니다.
2. **스펙 주도 개발 (SDD)**: "어떻게 코딩할까"를 고민하기보다 무엇을 만들지 불변 조건과 성공 기준을 엄격하게 명세한 `SPEC.md`를 작성하는 능력이 핵심입니다.
3. **루프 엔지니어링 & MCP**: 모델 컨텍스트 프로토콜(MCP)과 자동화 테스트를 결합하여 AI가 버그를 스스로 수정하는 순환 고리를 만듭니다.
4. **기본기의 역설**: AI 코드가 쏟아질수록 시스템 병목과 보안 구멍을 찾아내기 위한 컴퓨터공학 기본기(자료구조, 알고리즘, OS)가 훨씬 중요해집니다.
"""

def append_summary(file_path, summary_text, ref_marker):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "Executive Summary" in content or "최종 요약" in content or "Resumen Ejecutivo" in content or "核心总结" in content or "核心總結" in content:
        print(f"Summary already present in {file_path}")
        return
    
    if ref_marker in content:
        parts = content.split(ref_marker, 1)
        new_content = parts[0].rstrip() + "\n" + summary_text.strip() + "\n\n" + ref_marker + parts[1]
    else:
        new_content = content.rstrip() + "\n" + summary_text.strip() + "\n"
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Appended summary to: {file_path}")

# Apply to all 6 locales
append_summary(f"{gb_root}/blog/{folder_name}/index.md", en_summary, "### References & Course Materials")
append_summary(f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md", ko_summary, "### 참고 자료 및 공식 출처 (References)")
append_summary(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_summary, "### 参考文献 & 公式教材")
append_summary(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_summary, "### Referencias y Materiales del Curso")
append_summary(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_summary, "### 课程参考资料")
append_summary(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_summary, "### 課程參考資料")

# Apply to Naver Blog
append_summary(f"{nb_root}/post.md", nb_summary, "## 5. 공식 출처 및 스탠포드 강의 영상 안내")

print("Episode 1 summary injection finished successfully!")
