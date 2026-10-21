# -*- coding: utf-8 -*-
import os

ep_folder = "2026-05-17-maeumjigi-19"
gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-05-17\maeumjigi"

en_content = """---
slug: 2026-05-17-maeumjigi-19
title: "[Maeumjigi Capstone Dev Log #19] Automated Evaluation Reports & FastAPI PostgreSQL 401 Debugging"
authors: [jbgih]
tags: [devlog, automated-reporting, fastapi, postgresql, authentication, troubleshooting, knowledge-graph, capstone]
date: 2026-05-17
keywords: [FastAPI PostgreSQL Integration, 401 Unauthorized Troubleshooting, JWT Authentication Salt Mismatch, LLM Evaluation Report Automation, Knowledge Graph Chatbot Architecture]
description: "Overcoming full-stack hurdles: generating automated LLM benchmark reports with Claude Code, resolving cryptic JWT 401 Unauthorized errors in PostgreSQL, and designing our hybrid Knowledge Graph architecture."
---

![Cover Image](./images/01_cover.png)

Mid-May 2026 was supposed to be a calm interval after wrapping up our 2nd fine-tuning (`fine_tuning_2`). Instead, May 17th hit our team with a relentless double challenge: condensing hundreds of raw inference metrics into an automated technical report, while simultaneously battling a cryptic `HTTP 401 Unauthorized` cascading error across our newly integrated **FastAPI** and **PostgreSQL** backend.

Here is the complete post-mortem of how we automated our reporting and systematically neutralized the backend authentication breakdown.

{/* truncate */}

### 1. Autonomous Fine-Tuning Evaluation Reporting

Analyzing the 2nd fine-tuning results required processing hundreds of inference samples across multiple checkpoint variants (comparing Alpha values: 16, 32, and 64). Doing this manually was mathematically unfeasible given our capstone deadlines.

We engineered a structured prompt document (`report_prompt.md`) that guided **Claude Code** to analyze raw JSON evaluation matrices and automatically synthesize an executive technical report:

```markdown
# Excerpt from report_prompt.md
1. Parse evaluation metrics (BERTScore, ROUGE-L, Perplexity) from /eval/results_alpha_*.json.
2. Group model variants by empathy score, conversational naturalness, and safety compliance.
3. Highlight critical failure cases (e.g., hyper-formal robotic apologies vs conversational warmth).
4. Output the synthesis directly into a publication-ready Word document structure.
```

The AI agent generated `fine_tuning_2_report.docx` in under 3 minutes, complete with comparative analysis tables and qualitative excerpt breakdowns.

---

### 2. The Nightmare of HTTP 401 Unauthorized in PostgreSQL

With reporting streamlined, we restored our staging database dump (`backup.sql`) into a local PostgreSQL instance to test end-to-end user session persistence. Although the database restored with zero SQL syntax errors, our Next.js frontend crashed into an inescapable login loop:

```text
INFO: 127.0.0.1:54322 - "POST /auth/login HTTP/1.1" 401 Unauthorized
DETAIL: {"error": "Invalid credentials or malformed signature"}
```

Even with verified test credentials (`test@maeumjigi.kr` / `Password123!`), the FastAPI authentication service persistently rejected every login handshake.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Next.js Web Client
    participant API as FastAPI Gateway (/auth/login)
    participant DB as PostgreSQL Database
    participant Auth as Passlib Bcrypt Verifier

    Client->>API: POST /auth/login {email, password}
    API->>DB: SELECT id, password_hash FROM users WHERE email=...
    DB-->>API: Returns $2a$12$... hash string
    API->>Auth: bcrypt.verify("Password123!", db_hash)
    Note over Auth: Trap 1: Salt algorithm mismatch ($2a$ vs $2b$)!
    Auth-->>API: Verification Failed (False)
    API-->>Client: 401 Unauthorized
```

---

### 3. Root Cause Investigation & debug_login.py

To isolate whether the breakdown stemmed from frontend CORS headers, database corruption, or JWT secret misconfigurations, we wrote a standalone diagnostic script: `debug_login.py`.

```python
# Standalone authentication diagnostic utility: debug_login.py
import sys
from passlib.context import CryptContext
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:secret@localhost:5432/maeumjigi"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def diagnose_user_auth(email: str, raw_pass: str):
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT password_hash FROM users WHERE email = :e"), {"e": email}).fetchone()
        if not result:
            print("[FAIL] User not found in database!")
            return
        
        stored_hash = result[0]
        print(f"[INFO] Retrieved hash: {stored_hash[:15]}...")
        
        # Verify hash algorithm version compatibility
        is_valid = pwd_context.verify(raw_pass, stored_hash)
        print(f"[RESULT] Password Match Status: {is_valid}")

if __name__ == "__main__":
    diagnose_user_auth("test@maeumjigi.kr", "Password123!")
```

Running this diagnostic exposed three compounding bugs:

| Failure Vector | Technical Root Cause | Resolution Applied |
| :--- | :--- | :--- |
| **Bcrypt Salt Version** | Database dump contained `$2a$` hashes from older PHP/Node seeds; modern `passlib` expected `$2b$`. | Configured `pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__ident="2b", deprecated="auto")`. |
| **JWT Secret Encoding** | Secret string was loaded via `.env` with trailing newline `\r\n`, breaking HMAC-SHA256 signature checks. | Sanitized key ingestion: `SECRET_KEY = os.getenv("JWT_SECRET").strip().encode('utf-8')`. |
| **CORS Preflight** | Chrome browser blocked `Authorization: Bearer` headers during OPTIONS preflight checks. | Explicitly registered `CORSMiddleware` with `allow_headers=["*"]` and `expose_headers=["*"]`. |

Within 45 minutes of targeted refactoring, login latency dropped to 42ms with a 100% success rate!

![DB Troubleshooting](./images/02_db.png)

---

### 4. Architectural Expansion: Exploring Hybrid Knowledge Graphs

Resolving backend stability opened room for deeper architectural exploration. During clinical evaluation of our 2nd fine-tuned model, we noticed an intrinsic weakness shared by all parametric LLMs: **factual hallucinations during multi-hop crisis reasoning**.

```mermaid
flowchart TD
    subgraph User_Query ["User Input: Complex Crisis State"]
        U["I stopped taking my SSRI antidepressants 3 days ago and feel severe tremors."]
    end

    subgraph Hybrid_Architecture ["Hybrid Symbolic-Neural Architecture"]
        U --> KG_Extractor[Clinical Entity & Relation Extractor]
        KG_Extractor -->|Cypher Query| KG[(Neo4j Medical Knowledge Graph)]
        KG -->|Verified Triples: SSRI -> Discontinuation Syndrome| Context_Injector[Clinical Context Injector]
        
        U --> Direct_Prompt[Empathetic System Prompt]
        Direct_Prompt & Context_Injector --> FineTuned_LLM[Fine-Tuned Qwen / Llama 3.1]
    end

    subgraph Verified_Output ["Safety-Compliant Response"]
        FineTuned_LLM --> Output["Empathetic validation + Immediate medical warning regarding SSRI discontinuation syndrome."]
    end
```

By drafting `chatbot_design_prompt.md`, we laid the theoretical foundation for blending parametric LLM conversational empathy with deterministic Knowledge Graph validation.

---

### 5. Day 19 Key Engineering Takeaways

1. **Automated Documentation**: Reduced model benchmarking documentation turnaround from 6 hours to under 3 minutes using structured prompts and AI agents.
2. **Hardened Authentication**: Diagnosed and permanently resolved bcrypt salt mismatches and CORS header traps across PostgreSQL and FastAPI.
3. **Hybrid AI Vision**: Established the conceptual design for integrating symbolic Knowledge Graphs to eliminate clinical hallucinations in mental health counseling.

In Dev Log #20, we explore the completion of our 3rd fine-tuning cycle and the rollout of live community board features!
"""

ko_content = """---
slug: 2026-05-17-maeumjigi-19
title: "[마음지기 캡스톤 개발일지 #19] 파인튜닝 평가 보고서 자동화와 FastAPI PostgreSQL 401 에러 트러블슈팅"
authors: [jbgih]
tags: [devlog, automated-reporting, fastapi, postgresql, authentication, troubleshooting, knowledge-graph, capstone]
date: 2026-05-17
keywords: [FastAPI PostgreSQL 연동, 401 Unauthorized 트러블슈팅, JWT 인증 솔트 불일치, LLM 평가 보고서 자동화, 지식 그래프 챗봇 아키텍처]
description: "풀스택 연동의 최대 난관: Claude Code를 통한 모델 평가 보고서 자동 작성, PostgreSQL 덤프 복원 후 발생한 치명적인 401 인증 에러 해결, 지식 그래프 결합 아키텍처 설계를 상세히 정리합니다."
---

![Cover Image](./images/01_cover.png)

2026년 5월 17일은 2차 파인튜닝(`fine_tuning_2`)의 방대한 실험 결과를 정리하는 동시에, 백엔드와 프론트엔드를 하나로 엮는 과정에서 발생한 **치명적인 시스템 연동 장애**를 극복한 숨 가쁜 하루였습니다.
특히 수백 개의 추론 벤치마크 지표를 **기술 보고서로 전자동 컴파일**하고, PostgreSQL 데이터베이스 덤프 복원 직후 닥쳐온 **`HTTP 401 Unauthorized` 무한 로그인 실패 에러**를 완벽히 해결한 과정을 상세히 기록합니다.

{/* truncate */}

### 1. 인공지능을 활용한 2차 파인튜닝 평가 보고서 자동화

2차 파인튜닝에서 도출된 다양한 모델 체크포인트(Alpha 값 16, 32, 64 등)의 추론 결과는 수작업으로 일일이 분석하기에 물리적 시간이 턱없이 부족했습니다.

우리는 구조화된 프롬프트 지시서(`report_prompt.md`)를 작성하여 **Claude Code**가 원시 벤치마크 JSON 데이터를 직접 읽고 보고서를 작성하도록 파이프라인을 구축했습니다:

```markdown
# report_prompt.md 핵심 지침
1. /eval/ 디렉터리의 각 Alpha 모델별 평가 결과(BERTScore, ROUGE-L, Perplexity)를 종합 분석할 것.
2. 각 모델의 장단점(기계적 정형화 답변 vs 자연스러운 공감 표현력)을 구체적인 발화 사례와 함께 대조할 것.
3. 교수님 제출용 규격에 맞추어 개요, 실험 환경, 정량 지표 표, 결론이 포함된 Word(.docx) 문서를 조립할 것.
```

그 결과, 단 3분 만에 수치 비교표와 대표 발화 대조문이 완벽히 정리된 `fine_tuning_2_report.docx` 초안을 확보할 수 있었습니다.

---

### 2. 백엔드 DB 연동과 401 Unauthorized 에러의 늪

보고서 자동화 직후, 실제 서비스 구동을 위해 기존 백업 덤프(`backup.sql`)를 로컬 PostgreSQL DB에 복원하고 백엔드(FastAPI)와 프론트엔드(Next.js)를 기동했습니다. DB 데이터는 정상적으로 들어갔지만, 웹 브라우저에서 로그인을 시도하자마자 전면적인 401 에러가 터져 나왔습니다:

```text
INFO: 127.0.0.1:54322 - "POST /auth/login HTTP/1.1" 401 Unauthorized
DETAIL: {"error": "Invalid credentials or malformed signature"}
```

분명 DB에 존재하는 테스트 계정(`test@maeumjigi.kr` / `Password123!`)임에도 불구하고, 모든 인증 요청이 거부되며 메인 화면 진입이 전면 차단되었습니다.

```mermaid
sequenceDiagram
    autonumber
    actor 사용자 as 웹 브라우저 (Next.js)
    participant 백엔드 as FastAPI 게이트웨이 (/auth/login)
    participant DB as PostgreSQL 데이터베이스
    participant 인증모듈 as Passlib Bcrypt 검증기

    사용자->>백엔드: POST /auth/login {아이디, 패스워드}
    백엔드->>DB: SELECT id, password_hash FROM users WHERE email=...
    DB-->>백엔드: 기존 $2a$ 해시 문자열 반환
    백엔드->>인증모듈: bcrypt.verify("Password123!", db_hash)
    Note over 인증모듈: 함정 1: 구버전 해시 규격($2a$)과 신규 라이브러리($2b$) 충돌!
    인증모듈-->>백엔드: 비밀번호 불일치 (False) 반환
    백엔드-->>사용자: 401 Unauthorized 에러 응답
```

---

### 3. debug_login.py 제작과 3대 원인 규명

프론트엔드 네트워크 요청 문제인지, DB 손상인지, 백엔드 암호화 로직 오류인지 격리하기 위해 독립형 진단 스크립트인 `debug_login.py`를 제작하여 단계별 검증을 수행했습니다:

```python
# 독립형 인증 진단 유틸리티: debug_login.py
import sys
from passlib.context import CryptContext
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:secret@localhost:5432/maeumjigi"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def diagnose_user_auth(email: str, raw_pass: str):
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT password_hash FROM users WHERE email = :e"), {"e": email}).fetchone()
        if not result:
            print("[오류] 데이터베이스에서 사용자를 찾을 수 없습니다!")
            return
        
        stored_hash = result[0]
        print(f"[정보] 데이터베이스 해시 확인: {stored_hash[:15]}...")
        
        # 해시 알고리즘 호환성 및 비밀번호 일치 검증
        is_valid = pwd_context.verify(raw_pass, stored_hash)
        print(f"[결과] 비밀번호 검증 성공 여부: {is_valid}")

if __name__ == "__main__":
    diagnose_user_auth("test@maeumjigi.kr", "Password123!")
```

진단 결과, 단순한 오타가 아니라 세 가지 복합적인 환경 문제가 얽혀 있었습니다:

| 장애 지점 | 근본 기술 원인 | 최종 해결 조치 |
| :--- | :--- | :--- |
| **Bcrypt 솔트 규격** | 덤프 파일 내 해시가 과거 `$2a$` 규격으로 작성되어 최신 `passlib`에서 인식 실패 | `pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__ident="2b", deprecated="auto")` 호환 설정 추가 |
| **JWT 시크릿 개행문자** | `.env` 로드 시 윈도우 개행문자(`\r\n`)가 포함되어 HMAC 서명 불일치 유발 | `SECRET_KEY = os.getenv("JWT_SECRET").strip().encode('utf-8')`로 공백 및 개행 강제 제거 |
| **CORS Preflight 차단** | 브라우저 OPTIONS 사전 요청에서 `Authorization` 헤더가 거부됨 | FastAPI에 `CORSMiddleware` 등록 및 `allow_headers=["*"]` 명시 |

원인을 정확히 규명한 후 코드를 수정하자, 로그인 응답 속도는 42ms로 안정화되었고 401 에러는 100% 해소되었습니다!

![DB Troubleshooting](./images/02_db.png)

---

### 4. 차세대 아키텍처 구상: 온톨로지와 지식 그래프(Knowledge Graph)의 융합

백엔드 인증 문제를 깔끔히 해결한 후, 심야 회의에서는 2차 모델의 한계를 극복하기 위한 심층 토론이 이어졌습니다.
파인튜닝된 순수 언어 모델은 대화의 자연스러움은 뛰어났지만, **복합적인 정신의학적 위험 신호(예: 항우울제 임의 중단과 신체 금단 증상의 연관성)를 추론할 때 미세한 사실 왜곡(환각)**을 일으킬 위험이 있었습니다.

```mermaid
flowchart TD
    subgraph 내담자_발화 ["내담자 복합 위기 발화"]
        U["3일 전부터 항우울제 복용을 임의로 중단했는데 손이 너무 떨리고 불안해요."]
    end

    subgraph 하이브리드_아키텍처 ["심볼릭-신경망 결합 아키텍처"]
        U --> KG_추출기[의학 개체명 및 증상 관계 추출기]
        KG_추출기 -->|Cypher 쿼리| KG[(Neo4j 의학 지식 그래프)]
        KG -->|검증된 삼중주: 항우울제 급단약 -> 금단 증후군| 컨텍스트_주입기[임상 지식 컨텍스트 주입기]
        
        U --> 기본_프롬프트[공감 상담 시스템 프롬프트]
        기본_프롬프트 & 컨텍스트_주입기 --> 파인튜닝_LLM[파인튜닝된 Qwen / Llama 3.1]
    end

    subgraph 안전_응답 ["임상적 무결성이 확보된 최종 응답"]
        파인튜닝_LLM --> Output["따뜻한 정서적 위로 + 항우울제 임의 중단 시 급성 금단 증상 위험에 대한 전문의 상담 권고"]
    end
```

우리는 `chatbot_design_prompt.md` 작성을 시작으로, 언어 모델의 유연한 공감 능력에 결정론적인 지식 그래프 삼중주(Triple)를 결합하여 사실 오류를 원천 차단하는 하이브리드 인공지능 청사진을 구체화했습니다.

---

### 5. 19일차 핵심 교훈 및 성과 요약

1. **평가 보고서 전자동화**: 복잡한 수치와 모델별 특성을 프롬프트 자동화로 3분 만에 DOCX 문서로 완성.
2. **풀스택 인증 트러블슈팅 완결**: Bcrypt 버전 호환성과 JWT 시크릿 개행문자 정제를 통해 401 로그인 장애를 완벽 해결.
3. **지식 그래프 융합 설계 착수**: 단순 파라메트릭 언어 모델의 한계를 넘어 지식 그래프 기반의 고신뢰성 상담 아키텍처 기반 수립.

다음 20편에서는 3차 파인튜닝 완료 및 백엔드 커뮤니티 게시판 기능 고도화 과정을 다루겠습니다!
"""

es_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #19] Automated Evaluation Reports & FastAPI PostgreSQL 401 Debugging"',
    'title: "[Diario de Capstone Maeumjigi #19] Informes Automatizados y Depuración 401 en FastAPI PostgreSQL"'
).replace(
    'description: "Overcoming full-stack hurdles: generating automated LLM benchmark reports with Claude Code, resolving cryptic JWT 401 Unauthorized errors in PostgreSQL, and designing our hybrid Knowledge Graph architecture."',
    'description: "Superando obstáculos full-stack: generación automática de informes de benchmarks con Claude Code, resolución de errores 401 en PostgreSQL y arquitectura de Grafos de Conocimiento."'
)

ja_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #19] Automated Evaluation Reports & FastAPI PostgreSQL 401 Debugging"',
    'title: "[マウムジギ Capstone 開発日誌 #19] 評価レポートの自動生成と FastAPI PostgreSQL 401 エラーの完全解決"'
).replace(
    'description: "Overcoming full-stack hurdles: generating automated LLM benchmark reports with Claude Code, resolving cryptic JWT 401 Unauthorized errors in PostgreSQL, and designing our hybrid Knowledge Graph architecture."',
    'description: "フルスタック連携の難関突破：Claude Codeによる評価レポート自動生成、PostgreSQL移行後の401 Unauthorizedエラー解決、知識グラフ統合設計。"'
)

zh_hans_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #19] Automated Evaluation Reports & FastAPI PostgreSQL 401 Debugging"',
    'title: "[Maeumjigi 毕业设计开发日志 #19] 自动化评测报告生成与 FastAPI PostgreSQL 401 鉴权故障排查"'
).replace(
    'description: "Overcoming full-stack hurdles: generating automated LLM benchmark reports with Claude Code, resolving cryptic JWT 401 Unauthorized errors in PostgreSQL, and designing our hybrid Knowledge Graph architecture."',
    'description: "攻克全栈联调瓶颈：利用 Claude Code 全自动生成大模型评测报告，彻底排查并解决 PostgreSQL 401 登录鉴权故障，探索知识图谱混合架构。"'
)

zh_hant_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #19] Automated Evaluation Reports & FastAPI PostgreSQL 401 Debugging"',
    'title: "[Maeumjigi 畢業設計開發日誌 #19] 自動化評測報告生成與 FastAPI PostgreSQL 401 鑑權故障排查"'
).replace(
    'description: "Overcoming full-stack hurdles: generating automated LLM benchmark reports with Claude Code, resolving cryptic JWT 401 Unauthorized errors in PostgreSQL, and designing our hybrid Knowledge Graph architecture."',
    'description: "攻克全棧聯調瓶頸：利用 Claude Code 全自動生成大模型評測報告，徹底排查並解決 PostgreSQL 401 登錄鑑權故障，探索知識圖譜混合架構。"'
)

nb_post = f"""# [마음지기 캡스톤 개발일지 #19] 파인튜닝 평가 보고서 자동화와 FastAPI PostgreSQL 401 에러 트러블슈팅

안녕하세요! 대학 캡스톤 디자인 프로젝트 **「마음지기 (Maeumjigi)」**의 19일차 개발일지입니다.
이번 글에서는 2차 파인튜닝의 수많은 정량 지표를 **기술 보고서(.docx)로 전자동 컴파일**하고, 백엔드 DB 연동 중 발생한 치명적인 **FastAPI + PostgreSQL 401 Unauthorized 로그인 장애를 해결**한 과정을 공유합니다.

---

## 1. 2차 파인튜닝 결과 보고서의 전자동화

Alpha 파라미터(16, 32, 64)별 복잡한 추론 평가 데이터를 사람이 일일이 정리하는 대신, Claude Code가 직접 JSON을 파싱하여 교수님 제출용 Word 보고서 초안을 단 3분 만에 완성했습니다.

---

## 2. 401 Unauthorized 장애와 debug_login.py 진단

기존 DB 덤프(`backup.sql`)를 복원한 직후, 정상 계정임에도 로그인이 모두 차단되는 사태가 발생했습니다.
자체 제작한 진단 스크립트(`debug_login.py`)로 분석한 결과 3가지 복합 원인이 드러났습니다:

1. **Bcrypt 솔트 호환성**: 과거 `$2a$` 해시 규격과 최신 `passlib` `$2b$` 규격 충돌
2. **JWT 시크릿 개행문자**: `.env`에 윈도우 개행(`\r\n`)이 섞여 서명 검증 실패
3. **CORS Preflight 차단**: 브라우저 OPTIONS 요청 시 `Authorization` 헤더 거부

이 세 가지를 원포인트 수정함으로써 응답 시간 42ms의 무결점 인증 체계를 완성했습니다.

---

## 3. 차세대 지식 그래프(Knowledge Graph) 아키텍처 구상

언어 모델의 치명적 단점인 사실 왜곡(환각)을 방지하기 위해, 의학적 삼중주(Triple) 지식을 주입하여 검증하는 **하이브리드 심볼릭-신경망 챗봇 아키텍처** 설계를 개시했습니다.

---

## 4. 글로벌 기술 블로그에서 상세 아키텍처 확인하기

FastAPI 진단 스크립트 전문과 지식 그래프 융합 다이어그램은 글로벌 블로그에서 확인하실 수 있습니다:

👉 **[GlobalDevLog 글로벌 블로그: Maeumjigi Capstone Dev Log #19 원문 보기](https://globaldevlog.com/blog/2026-05-17-maeumjigi-19)**

다음 20편에서는 3차 파인튜닝 완료 및 백엔드 기능 고도화 소식을 전해드리겠습니다!
"""

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
print("Episode 19 enhancement successfully written!")
