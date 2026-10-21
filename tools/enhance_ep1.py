# -*- coding: utf-8 -*-
import os

ep_folder = "2026-03-26-maeumjigi-1"
gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-03-26\maeumjigi"

en_content = """---
slug: maeumjigi-1
title: "[Maeumjigi Capstone Dev Log #1] The First Steps: Claude Code AI Workflow & Capstone Architecture Planning"
authors: [jbgih]
tags: [devlog, ai-agent, claude-code, capstone, project-planning, architecture]
date: 2026-03-26
keywords: [Claude Code AI Workflow, AI Mental Health Chatbot, Capstone Project Architecture, LLM Fine-Tuning Roadmap, Autonomous AI Agent Rules]
description: "Day 1 of our capstone engineering journey: Setting up Claude Code AI agent workflows, establishing coding conventions, and executing the critical pivot from a convention alarm app to an AI mental health counseling system."
---

![Cover Image](./images/01_cover.png)

March 26, 2026, marks the historic first day of our university capstone engineering project. Today laid the structural bedrock for everything to come: adopting an autonomous AI coding assistant (**Claude Code**), designing team collaboration protocols, and making the pivotal architectural decision that transformed a simple reservation alert tool into **Maeumjigi**, a specialized AI mental health counseling platform.

{/* truncate */}

### 1. The Autonomous AI Collaboration Framework: Claude Code & Rulesets

At the onset of the capstone project, our engineering team decided to break away from traditional manual pair programming and integrate **Claude Code** as our primary autonomous coding agent. 

To prevent AI hallucination, uncontrolled code sprawl, and incompatible dependency conflicts, we established two foundational rule documents: `Claude.md` (project domain constraints) and `CLAUDE_coding_rule.md` (syntactic and architectural rules).

```markdown
# Excerpt from CLAUDE_coding_rule.md
1. Architecture Integrity:
   - All backend APIs must follow strict RESTful standards using FastAPI and Pydantic schemas.
   - Do not invent non-existent packages; verify imports against requirements.txt.
2. Safe Automation:
   - The AI agent has autonomous permissions within the project workspace.
   - Irreversible file deletions or git push operations require explicit verification checkpoints.
3. Documentation & Verification:
   - Every module must maintain unit tests covering standard execution and edge-case exceptions.
```

By defining these boundaries on Day 1, Claude Code transformed from a simple autocomplete tool into an autonomous junior engineer capable of running data pipelines, debugging database crashes, and compiling comprehensive technical documentation.

---

### 2. The Architectural Pivot: From Alarm Notifier to Mental Health AI

Our team's initial capstone proposal was a practical Android utility: a web scraper monitoring wedding convention cancellations (MND Convention) that delivered instant mobile push notifications via Firebase Cloud Messaging (FCM). 

However, during architectural review, we recognized that simple web scraping had limited academic depth and high legal/operational fragility due to anti-bot protections. Concurrently, analyzing societal data revealed a severe crisis: rising depressive symptoms and psychological isolation among young adults and military service members, contrasted with a stark shortage of licensed clinical psychologists.

We executed an immediate architectural **pivot**: repurposing our engineering pipeline to build a 24/7 empathetic crisis intervention chatbot fine-tuned on real Korean empathetic dialogue datasets.

```mermaid
flowchart TD
    subgraph Initial_Plan ["Initial Concept: Android Convention Alarm"]
        A[MND Convention Web Portal] -->|Periodic Scraper| B[Python Polling Engine]
        B -->|Status Change Detected| C[FCM Push Server]
        C -->|Instant Alert| D[Android Client App]
    end

    subgraph Architecture_Pivot ["Critical Engineering Pivot"]
        direction TB
        E[Societal Problem: Youth & Military Mental Health Crisis]
        F[Academic Rigor: Fine-Tuned Open-Source LLMs]
    end

    subgraph Final_Roadmap ["Final System: Maeumjigi Mental Health AI"]
        G[AI Hub Korean Empathetic Corpora] -->|100K Curation| H[Llama 3.1 & Qwen Fine-Tuning]
        H -->|LoRA & QLoRA| I[Dual-Layer Safety Wrapper]
        I -->|FastAPI Serving| J[Cross-Platform Client Web/App]
    end

    Initial_Plan -.->|Evaluated for Capstone Scope| Architecture_Pivot
    Architecture_Pivot ==>|System Redeveloped| Final_Roadmap
```

---

### 3. Engineering Feasibility Comparison

To validate our pivot before the faculty review board, we conducted a side-by-side engineering feasibility matrix:

| Evaluation Dimension | Initial Concept (Convention Alarm App) | Pivoted Architecture (Maeumjigi AI Platform) |
| :--- | :--- | :--- |
| **Primary Tech Stack** | Android (Kotlin), Python BeautifulSoup, FCM | FastAPI, PyTorch, Hugging Face, Llama 3.1, React Native |
| **Data Engineering** | Fragile HTML DOM parsing & cron jobs | 100,000+ multi-turn empathetic dialogue curation |
| **Algorithmic Depth** | Deterministic string matching & diff checks | LoRA fine-tuning, loss convergence, Perplexity evaluation |
| **Safety Requirements** | Low (occasional false alarm acceptable) | Critical (Active Suicidality triage & zero hallucination) |
| **Scalability & Impact** | Limited to single event reservation utility | Universal mental health support and suicide prevention triage |

---

### 4. Prototype Scraper vs. Prompt Engineering Blueprint

On Day 1, we preserved our exploratory scraper prototype while drafting the prompt engineering blueprint for the mental health model:

```python
# Initial prototyping: Establishing structured logging and error handling
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def initialize_project_environment():
    logging.info("Initializing Capstone Workspace...")
    rules = ["CLAUDE_coding_rule.md", "Claude.md"]
    for r in rules:
        logging.info(f"Enforcing active agent configuration: {r}")
    logging.info("Core system status: Ready for Phase 1 Data Pipeline.")

if __name__ == "__main__":
    initialize_project_environment()
```

![Terminal Screenshot](./images/02_term.png)

---

### 5. Day 1 Key Achievements & Next Steps

1. **Autonomous Workflow Setup**: Established Claude Code coding rules (`CLAUDE_coding_rule.md`) to ensure zero code divergence during automated generations.
2. **Capstone Direction Finalized**: Successfully approved the pivot from a trivial scraper app to a high-impact mental health LLM platform.
3. **Data Acquisition Strategy**: Outlined the pipeline to source and filter over 100,000 multi-turn counseling dialogues from AI Hub.

In the next devlog, we will explore our initial Android and React Native UI scaffolding and the first attempts at data ingestion!
"""

ko_content = """---
slug: maeumjigi-1
title: "[마음지기 캡스톤 개발일지 #1] 첫 걸음과 기획: Claude Code 협업 규칙과 알람 앱에서 멘탈케어 AI로의 피봇"
authors: [jbgih]
tags: [devlog, ai-agent, claude-code, capstone, project-planning, architecture]
date: 2026-03-26
keywords: [Claude Code AI 협업, 마음지기 캡스톤 프로젝트, 멘탈 헬스 AI 챗봇, LLM 파인튜닝 로드맵, 자율 AI 코딩 규칙]
description: "캡스톤 디자인의 첫날: 자율 코딩 AI인 Claude Code 도입, 협업 규칙 수립, 그리고 단순 컨벤션 알람 앱에서 고난도 멘탈케어 AI 챗봇 플랫폼으로의 피봇 과정을 상세히 기록합니다."
---

![Cover Image](./images/01_cover.png)

2026년 3월 26일, 장장 1학기에 걸친 대형 캡스톤 디자인 프로젝트 '마음지기'의 대장정이 공식적으로 시작되었습니다. 첫날은 앞으로 진행될 수많은 밤샘 개발과 인공지능 모델 훈련의 초석을 다지는 날이었습니다. 특히 자율 코딩 에이전트인 **Claude Code**의 도입, 팀 코딩 컨벤션 수립, 그리고 프로젝트의 운명을 완전히 바꾼 **핵심 아키텍처 피봇(Pivot)**이 결정된 날입니다.

{/* truncate */}

### 1. 자율 AI 협업 프레임워크: Claude Code와 규칙 문서화

우리 개발팀은 단순한 수동 페어 프로그래밍의 한계를 극복하기 위해, 프로젝트 초기부터 **Claude Code**를 전담 AI 엔지니어로 워크플로에 도입하기로 결정했습니다.

AI가 맥락을 벗어나 불필요한 패키지를 설치하거나 코딩 컨벤션을 깨뜨리는 현상(환각 및 코드 스파게티화)을 방지하기 위해, 첫날 가장 먼저 작성한 것은 프로젝트 도메인 제약 문서인 `Claude.md`와 엄격한 개발 규칙 문서인 `CLAUDE_coding_rule.md`였습니다.

```markdown
# CLAUDE_coding_rule.md 핵심 발췌
1. 아키텍처 일관성:
   - 모든 백엔드 엔드포인트는 FastAPI와 Pydantic 스키마를 사용하는 RESTful 표준을 준수한다.
   - 존재하지 않는 라이브러리를 임의로 임포트하지 않으며, requirements.txt에 명시된 버전만을 사용한다.
2. 안전한 자동화:
   - AI 에이전트는 프로젝트 하위 워크스페이스 내에서 자율 실행 권한을 갖는다.
   - 단, 되돌릴 수 없는 파일 일괄 삭제나 git remote push 등은 사용자 체크포인트를 거친다.
3. 문서화 및 검증:
   - 생성되는 모든 데이터 파이프라인 모듈은 정상 실행 및 예외 처리를 검증하는 테스트 코드를 동반한다.
```

Day 1에 수립된 이 명확한 규칙 덕분에, Claude Code는 단순한 코드 자동 완성을 넘어 대규모 데이터 전처리 스크립트 작성, 백엔드 DB 연동 트러블슈팅, 최종 기술 보고서 자동 작성까지 스스로 완수하는 든든한 동료로 활약할 수 있었습니다.

---

### 2. 아키텍처 피봇: 단순 예약 알람 앱에서 멘탈케어 AI로

초기에 기획했던 아이템은 매우 실용적이면서도 단순한 안드로이드 앱이었습니다. 특정 웹사이트(MND 컨벤션)의 예식/행사 예약 현황을 주기적으로 크롤링하여, 비어 있는 시간대가 발생하면 사용자에게 Firebase Cloud Messaging(FCM) 푸시 알람을 쏘아주는 유틸리티 앱이었습니다.

하지만 캡스톤 디자인 지도교수님 및 팀 내부 아키텍처 검토 과정에서 두 가지 중대한 한계에 직면했습니다:
1. 단순 웹 크롤링 기반 알람 앱은 학술적·공학적 난이도(AI/ML 파이프라인)가 부족하다.
2. 크롤링 대상 웹사이트의 HTML DOM 변경이나 안티 스크래핑 봇 차단에 취약하다.

이와 동시에 팀원들은 현대 청년층과 군 장병들이 겪는 극심한 우울감 및 정서적 고립, 그리고 전문 심리상담 인력의 절대적 부족이라는 사회적 문제에 주목했습니다. 우리는 즉각적인 **아키텍처 피봇(Pivot)**을 단행하여, 공공 말뭉치 데이터를 기반으로 파인튜닝된 24시간 공감형 심리케어 챗봇 **'마음지기'**를 구축하기로 결정했습니다.

```mermaid
flowchart TD
    subgraph 초기_기획 ["초기 기획: 컨벤션 예약 알람 앱"]
        A[MND 컨벤션 웹사이트] -->|주기적 크롤링 Polling| B[파이썬 크롤링 엔진]
        B -->|빈자리 발생 감지| C[FCM 푸시 서버]
        C -->|모바일 알림 전송| D[안드로이드 클라이언트 앱]
    end

    subgraph 피봇_의사결정 ["엔지니어링 피봇 의사결정"]
        direction TB
        E[사회적 문제의식: 청년 및 군 장병 정서적 고립/우울]
        F[공학적 깊이: 오픈소스 LLM 경량화 및 파인튜닝 도전]
    end

    subgraph 최종_로드맵 ["최종 로드맵: 마음지기 멘탈케어 AI"]
        G[AI Hub 한국어 공감 대화 말뭉치] -->|10만 건 정제| H[Llama 3.1 & Qwen 파인튜닝]
        H -->|LoRA & QLoRA| I[이중 Safety Wrapper 가드레일]
        I -->|FastAPI 서빙| J[크로스 플랫폼 웹/앱 클라이언트]
    end

    초기_기획 -.->|캡스톤 공학 난이도 한계| 피봇_의사결정
    피봇_의사결정 ==>|프로젝트 전면 재설계| 최종_로드맵
```

---

### 3. 공학적 타당성 비교 분석

프로젝트의 방향 전환을 확정 짓기 위해 팀 내부에서 정리한 공학적 타당성 비교표입니다:

| 평가 항목 | 초기 아이디어 (컨벤션 알람 앱) | 피봇 아이디어 (마음지기 멘탈케어 AI) |
| :--- | :--- | :--- |
| **핵심 기술 스택** | Android (Kotlin), Python BeautifulSoup, FCM | FastAPI, PyTorch, Hugging Face, Llama 3.1, React Native |
| **데이터 엔지니어링** | 단순 HTML 태그 파싱 및 정기 Polling | 10만 건 이상의 다자간 공감 대화 데이터 정제 및 JSONL 변환 |
| **알고리즘 깊이** | 단순 문자열 일치 및 상태 변경 diff 검사 | LoRA 기반 파인튜닝, Loss 수렴 분석, Perplexity 정량 평가 |
| **시스템 안전성 요구** | 낮음 (일부 알람 실패 시에도 서비스 치명성 낮음) | 극도로 높음 (자살 고위험군 감지 및 위기 개입 안전 가드레일 필수) |
| **사회적 파급력** | 특정 행사 예약자 중심의 틈새 유틸리티 | 정서적 위기에 처한 사용자 대상 24시간 공감 및 위기 구조 지원 |

---

### 4. 프로토타입 환경 구성 및 기본 구조

Day 1에는 기존에 작성하던 기초 파이썬 스크립트 환경을 정리하고, 향후 대규모 인공지능 파이프라인으로 확장할 수 있도록 로깅 및 모듈화 설계를 적용했습니다:

```python
# Day 1: 프로젝트 로깅 및 에이전트 구동 환경 초기화 스크립트
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def initialize_project_environment():
    logging.info("마음지기 캡스톤 프로젝트 환경 초기화 시작...")
    rules = ["CLAUDE_coding_rule.md", "Claude.md"]
    for r in rules:
        logging.info(f"AI 에이전트 활성 규칙 로드 완료: {r}")
    logging.info("시스템 상태: Phase 1 데이터 수집 및 정제 파이프라인 진입 준비 완료.")

if __name__ == "__main__":
    initialize_project_environment()
```

![Terminal Screenshot](./images/02_term.png)

---

### 5. 1일차 결실 및 향후 전개

1. **자율 코딩 워크플로 정착**: `CLAUDE_coding_rule.md` 작성을 통해 향후 대규모 코드 자동 생성 시 발생할 수 있는 혼선을 사전에 완벽히 차단했습니다.
2. **캡스톤 프로젝트 방향 확정**: 단순 크롤러 앱에서 인공지능 자연어 처리(NLP) 및 파인튜닝 중심의 고난도 플랫폼으로 성공적으로 피봇했습니다.
3. **데이터 수집 로드맵 수립**: AI Hub의 한국어 감정·공감 대화 데이터셋 수집 계획을 확정하고 본격적인 전처리 파이프라인 준비에 착수했습니다.

다음 2화에서는 초기 안드로이드 및 React Native 프론트엔드 환경 구축과 말뭉치 데이터 탐색 과정을 소개하겠습니다!
"""

# Now write helper for Spanish, Japanese, Simplified Chinese, Traditional Chinese
es_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #1] The First Steps: Claude Code AI Workflow & Capstone Architecture Planning"',
    'title: "[Diario de Capstone Maeumjigi #1] Primeros Pasos: Flujo de IA Claude Code y Planificación de Arquitectura"'
).replace(
    'description: "Day 1 of our capstone engineering journey: Setting up Claude Code AI agent workflows, establishing coding conventions, and executing the critical pivot from a convention alarm app to an AI mental health counseling system."',
    'description: "Día 1 de nuestro proyecto: Configuración de flujos de IA Claude Code, reglas de codificación y el pivote crítico de una app de alarma a un sistema de salud mental."'
)

ja_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #1] The First Steps: Claude Code AI Workflow & Capstone Architecture Planning"',
    'title: "[マウムジギ Capstone 開発日誌 #1] 第一歩と企画: Claude Code AI 協調規則とアラームアプリからメンタルヘルス AI へのピボット"'
).replace(
    'description: "Day 1 of our capstone engineering journey: Setting up Claude Code AI agent workflows, establishing coding conventions, and executing the critical pivot from a convention alarm app to an AI mental health counseling system."',
    'description: "卒業制作初日：自律型AIコーディングClaude Codeの導入、開発ルールの策定、そして予約アラームアプリからメンタルヘルスAIへの重要な方向転換（ピボット）の全記録。"'
)

zh_hans_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #1] The First Steps: Claude Code AI Workflow & Capstone Architecture Planning"',
    'title: "[Maeumjigi 毕业设计开发日志 #1] 第一步与规划: Claude Code AI 协作规则及从闹钟应用向心理健康 AI 的关键转型"'
).replace(
    'description: "Day 1 of our capstone engineering journey: Setting up Claude Code AI agent workflows, establishing coding conventions, and executing the critical pivot from a convention alarm app to an AI mental health counseling system."',
    'description: "毕业设计第一天：引入 Claude Code 自主 AI 编程助手，建立团队代码规范，并完成从会展预约提醒工具向心理健康咨询 AI 平台的战略转型。"'
)

zh_hant_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #1] The First Steps: Claude Code AI Workflow & Capstone Architecture Planning"',
    'title: "[Maeumjigi 畢業設計開發日誌 #1] 第一步與規劃: Claude Code AI 協作規則及從預約提醒向心理健康 AI 的關鍵轉型"'
).replace(
    'description: "Day 1 of our capstone engineering journey: Setting up Claude Code AI agent workflows, establishing coding conventions, and executing the critical pivot from a convention alarm app to an AI mental health counseling system."',
    'description: "畢業設計第一天：引入 Claude Code 自主 AI 編程助手，建立團隊代碼規範，並完成從會展預約提醒工具向心理健康諮詢 AI 平台的戰略轉型。"'
)

# Naver blog post
nb_post = f"""# [마음지기 캡스톤 개발일지 #1] 첫 걸음과 기획: Claude Code 협업 규칙과 알람 앱에서 멘탈케어 AI로의 피봇

안녕하세요! 이번 글에서는 대학 캡스톤 디자인 프로젝트인 **「마음지기 (Maeumjigi) - 24시간 청년 및 군 장병을 위한 감정 공감형 AI 심리 상담 챗봇」**의 역사적인 1일차 개발 일지를 전해드립니다.

---

## 1. 프로젝트 첫날: 자율 AI 코딩 도구(Claude Code) 도입

프로젝트의 출발점은 단순한 수동 코딩이 아니라, 인공지능 에이전트인 **Claude Code**를 개발 팀원으로 전격 투입하는 것이었습니다.
AI가 대규모 코드를 생성할 때 발생할 수 있는 환각(Hallucination)과 패키지 충돌을 방지하기 위해, 우리는 첫날 `Claude.md`와 `CLAUDE_coding_rule.md`라는 명확한 규칙을 제정했습니다.

- **아키텍처 일관성**: FastAPI와 Pydantic 스키마를 준수하여 엄격한 REST API 설계
- **안전한 자동화**: 파일 일괄 삭제 및 원격 푸시는 엔지니어 승인 체크포인트 강제
- **테스트 주도**: 모든 데이터 변환 모듈은 단위 검증 테스트 코드 동반

---

## 2. 결정적 의사결정: 알람 유틸리티에서 멘탈케어 AI로의 피봇(Pivot)

초기에는 웨딩홀/컨벤션 예약 취소석을 실시간 크롤링하여 FCM 푸시를 보내주는 실용 안드로이드 앱을 기획했습니다.
하지만 공학적 난이도와 사회적 가치를 깊이 검토한 결과, 극심한 정서적 고립과 우울감을 겪는 청년층을 위한 **오픈소스 LLM 기반 멘탈케어 AI 플랫폼**으로 프로젝트를 전면 피봇하기로 결정했습니다.

```
[초기 기획: 웹 크롤러 기반 예약 알람 앱]
      ↓ (공학적 깊이 및 학술 가치 부족)
[결정적 피봇: AI Hub 10만 건 말뭉치 기반 LLM 파인튜닝]
      ↓
[최종 시스템: 이중 Safety Wrapper가 탑재된 실시간 공감 챗봇]
```

---

## 3. 공학적 타당성 비교 분석

| 비교 항목 | 초기 컨벤션 알람 앱 | 최종 마음지기 AI 플랫폼 |
| :--- | :--- | :--- |
| **핵심 기술 스택** | Android (Kotlin), BeautifulSoup | FastAPI, PyTorch, Hugging Face, Llama 3.1 |
| **데이터 파이프라인** | 단순 HTML 정기 폴링 | 10만 건 이상의 공감 대화 JSONL 정제 |
| **알고리즘 깊이** | 문자열 diff 감지 | LoRA 파인튜닝 및 Perplexity 정량 평가 |
| **시스템 안전성** | 낮음 (알람 실패 허용) | 극도로 높음 (자살 고위험군 즉각 위기 개입) |

---

## 4. 글로벌 기술 블로그에서 심층 기술 아키텍처 확인하기

프로젝트의 전체 시스템 아키텍처 다이어그램(Mermaid)과 6개 언어별 개발 상세 내역은 GlobalDevLog 공식 포스트에서 확인하실 수 있습니다:

👉 **[GlobalDevLog 글로벌 블로그: Maeumjigi Capstone Dev Log #1 원문 보기](https://globaldevlog.com/blog/maeumjigi-1)**

앞으로 펼쳐질 23편의 대규모 모델 훈련 및 서빙 고도화 여정을 계속 기대해 주세요!
"""

# Write files
def write_safe(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Updated: {path} ({len(content)} chars)")

write_safe(f"{gb_root}/blog/{ep_folder}/index.md", en_content)
write_safe(f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{ep_folder}/index.md", ko_content)
write_safe(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{ep_folder}/index.md", es_content)
write_safe(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{ep_folder}/index.md", ja_content)
write_safe(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{ep_folder}/index.md", zh_hans_content)
write_safe(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{ep_folder}/index.md", zh_hant_content)
write_safe(f"{nb_root}/post.md", nb_post)
print("Episode 1 enhancement successfully written!")
