# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-10-23\stanford_cs146s_2"
folder_name = "2026-10-23-stanford-cs146s-2"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **The Nature of Coding LLMs**: LLMs are statistical simulators forged through a 3-stage pipeline (Pre-training next-token prediction, SFT instruction protocols, and RLHF/DPO alignment) rather than conscious reasoning agents.
2. **Prompting as Software Engineering**: For complex concurrency and logic, forcing Chain-of-Thought (CoT) reasoning steps and negative constraints provides critical self-grounding tokens that eliminate hallucinations.
3. **The Swiss Cheese Hazard**: Impeccably formatted AI code frequently harbors latent off-by-one errors and race conditions; engineering teams must actively counteract automation bias.
4. **The "Trust but Verify" Doctrine**: Deploy a rigorous four-gate verification harness—strict static typing, deterministic unit tests, property-based invariant fuzzing, and human architectural code review—before any AI code reaches production.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **3단계 훈련의 본질**: 코딩 LLM은 의식을 가진 존재가 아니라, 사전 학습(다음 토큰 확률 예측), SFT(지시 프로토콜 튜닝), RLHF/DPO(인간 선호도 정렬)를 거쳐 완성된 '수석 엔지니어 코드의 초고속 통계 시뮬레이터'입니다.
2. **소프트웨어 공학으로서의 프롬프트**: 복잡한 비즈니스 로직과 동시성 제어 시 생각의 사슬(CoT)을 강제하여 중간 추론 토큰을 확보하고, 엄격한 부정 제약 조건을 부여해야 환각을 차단할 수 있습니다.
3. **스위스 치즈 모델의 경고**: AI가 생성한 코드는 겉보기에 유려해도 배열 인덱스 초과, 경합 상태, 보안 취약점이라는 치명적인 구멍(Hole)을 내포하므로 '자동화 편향'을 경계해야 합니다.
4. **Trust but Verify (신뢰하되 검증하라)**: 정적 타입 분석(Gate 1) → 단위 테스트 계약(Gate 2) → 속성 기반 퍼징(Gate 3) → 인간 아키텍처 서명(Gate 4)으로 이어지는 다층 방어 하네스를 구축해야만 안전하게 프로덕션에 배포할 수 있습니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **コーディングLLMの本質**: LLMは意識ある知能ではなく、事前学習（次トークン予測）、SFT（対話プロトコル注入）、RLHF/DPO（選好アライメント）を経て完成した「熟練コードの高速統計シミュレーター」です。
2. **工学としてのプロンプト設計**: 複雑な並行処理やアルゴリズムに対し、思考の連鎖(CoT)を強制して中間推論トークンを生成させ、明示的な禁止制約を課すことで論理エラーを防ぎます。
3. **スイスチーズモデルの警告**: 完璧に見えるAIコードの裏には、境界外エラーや競合状態という致命的な穴（Hole）が潜んでおり、自動化バイアスを捨てて疑う必要があります。
4. **「信頼せよ、されど検証せよ」**: 厳格な静的型検査、決定論的単体テスト、境界ファジング、人間によるアーキテクチャ監査という多層防衛ハーネスの構築が本番運用の前提です。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **La Naturaleza de los LLMs de Código**: Los LLMs no son entidades conscientes, sino simuladores estadísticos de tokens forjados a través de pre-entrenamiento, SFT y alineación por RLHF/DPO.
2. **Ingeniería de Prompts Disciplinada**: Para lógicas complejas y concurrencia, exigir razonamiento paso a paso (Chain-of-Thought) y restricciones negativas previene alucinaciones y valida invariantes.
3. **El Peligro del Queso Suizo**: El código generado con IA luce impecable superficialmente pero oculta agujeros sutiles (off-by-one, deadlocks); los desarrolladores deben vencer el sesgo de automatización.
4. **Doctrina "Confía pero Verifica"**: Implementar una compuerta defensiva de cuatro capas—tipado estricto, pruebas unitarias deterministas, fuzzing de invariantes y revisión arquitectónica humana—es indispensable para producción.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **代码大模型的数理本质**：大模型并非具备意识的智慧体，而是历经海量无监督预训练、SFT 规范微调与 RLHF/DPO 人类偏好对齐打造的高速统计概率模拟器。
2. **严密的提示词工程**：在处理并发与复杂算法时，强制引入思维链 (CoT) 显式推导步骤并施加严密否定约束，是消解模型幻觉的关键技术。
3. **警惕瑞士奶酪模型**：AI 生成的代码在语法上高度规范，却极易隐藏数组越界与死锁等隐蔽孔洞，工程师切忌陷入盲信系统的自动化偏差。
4. **“信任但必须验证”架构**：构建由严格类型检查、确定性单元测试、属性模糊测试与人类资深架构师把关组成的多层自动化门禁，方可确保生产级交付。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **程式碼大模型的數理本質**：大模型並非具備意識的實體，而是歷經海量無監督預訓練、SFT 規範微調與 RLHF/DPO 人類偏好對齊打造的高速統計機率模擬器。
2. **嚴密的提示詞工程**：在處理並發與複雜演算法時，強制引入思維鏈 (CoT) 顯式推導步驟並施加嚴密否定約束，是消解模型幻覺的關鍵技術。
3. **警惕瑞士起司模型**：AI 生成的程式碼在語法上高度規範，卻極易隱藏陣列越界與死鎖等隱蔽孔洞，工程師切忌陷入盲信系統的自動化偏差。
4. **「信任但必須驗證」架構**：構建由嚴格型別檢查、確定性單元測試、屬性模糊測試與人類資深架構師把關組成的多層自動化門禁，方可確保生產級交付。
"""

nb_summary = """
---

## 📌 3~5줄 최종 요약
1. **코딩 LLM의 본질**: AI는 생각하는 존재가 아니라 사전 학습, SFT, RLHF를 거친 '수석 엔지니어 코드의 초고속 통계 시뮬레이터'입니다.
2. **소프트웨어 공학적 프롬프트**: 생각의 사슬(CoT)로 단계별 추론 과정을 먼저 출력하게 만들고 엄격한 제약 조건을 주어야 환각을 잡을 수 있습니다.
3. **스위스 치즈 모델 경고**: AI가 짠 코드는 겉보기에 우아해도 미세한 버그와 보안 구멍이 숨어 있으므로 '자동화 편향'을 경계해야 합니다.
4. **Trust but Verify**: 정적 분석, 단위 테스트, 무작위 퍼징, 인간 최종 검토로 이어지는 4대 방어선을 거쳐야 안전한 코드가 완성됩니다.
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
        
    # Clean double hr
    new_content = re.sub(r'---\s*\r?\n\s*---', '---', new_content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Appended summary to: {file_path}")

# Apply to all 6 locales
append_summary(f"{gb_root}/blog/{folder_name}/index.md", en_summary, "### References & Course Materials")
append_summary(f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md", ko_summary, "### References & Course Materials")
append_summary(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_summary, "### 参考文献 & 公式教材")
append_summary(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_summary, "### Referencias y Materiales del Curso")
append_summary(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_summary, "### 课程参考资料")
append_summary(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_summary, "### 課程參考資料")

# Apply to Naver Blog
append_summary(f"{nb_root}/post.md", nb_summary, "## 4. 글로벌 기술 블로그에서 상세 아키텍처 다이어그램 확인하기")

print("Episode 2 summary injection finished successfully!")
