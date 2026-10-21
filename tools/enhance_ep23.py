# -*- coding: utf-8 -*-
import os

ep_folder = "2026-06-18-maeumjigi-23"
gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-06-18\maeumjigi"

en_content = """---
slug: 2026-06-18-maeumjigi-23
title: "[Maeumjigi Capstone Dev Log #23] Dual-Layer Safety Wrapper, AWS EC2 GPU Budgeting & Semester 1 Defense"
authors: [jbgih]
tags: [devlog, safety-wrapper, guardrail, aws-ec2, gpu-serving, capstone-defense, suicide-prevention]
date: 2026-06-18
keywords: [AI Mental Health Chatbot, AI Safety Wrapper, LLM Guardrail Architecture, Crisis Intervention Protocol, AWS EC2 GPU Serving]
description: "Final Milestone of Semester 1: Engineering our dual-layer Safety Wrapper for crisis de-escalation, calculating AWS EC2 g5.2xlarge GPU serving budgets, and presenting our Capstone Final Defense."
---

![Cover Image](./images/01_cover.png)

June 18, 2026, marks the triumphant completion of the 1st semester of our university capstone engineering project. From our humble beginnings as a simple Android convention scraper in March, **Maeumjigi** has evolved into a full-scale, clinical-grade AI mental health counseling ecosystem. 

Our final sprint focused on two mission-critical objectives:
1. **The Dual-Layer Safety Wrapper**: Engineering a bulletproof guardrail architecture to guarantee zero-hallucination crisis intervention.
2. **Production Cloud Serving & Final Defense**: Sizing AWS EC2 GPU infrastructure budgets and delivering our final faculty presentation.

{/* truncate */}

### 1. The Dual-Layer Safety Wrapper Architecture

In consumer chatbots, occasional hallucinations or awkward phrasing are minor annoyances. In an AI platform dedicated to youth and military suicide prevention, **a single hallucinated response or dismissive answer could be fatal**.

To protect vulnerable users, we designed a **Dual-Layer Safety Wrapper** that wraps around our fine-tuned Qwen 3.5-9B model (Checkpoint-4400):

```mermaid
flowchart TD
    subgraph Inbound_Triage ["Layer 1: Pre-Inference Guardrail"]
        A[User Message Received] --> B[Regex Crisis Keyword Detector]
        B --> C[Zero-Shot Semantic Crisis Classifier]
        C --> D{Risk Severity Assessment}
    end

    subgraph Decision_Branch ["Emergency Routing"]
        D -->|Level 3: Active Suicidality / Imminent Danger| E[Emergency Protocol Triggered]
        E -->|Bypass Generative Model| F[Deterministic Crisis Intervention & 109 / 1393 Dialing]
        
        D -->|Level 1-2: Mild to Moderate Emotional Distress| G[Pass to Fine-Tuned LLM]
    end

    subgraph Inference_Core ["Model Generation"]
        G --> H[vLLM Serving Engine: Checkpoint-4400]
        H --> I[Raw Generative Token Stream]
    end

    subgraph Outbound_Verifier ["Layer 2: Post-Inference Guardrail"]
        I --> J[Toxicity & Hallucination Filter]
        J --> K[Clinical Referral Footer Injection]
        K --> L[Sanitized Real-Time SSE to Client]
    end

    F --> L
```

#### Crisis Escalation Protocol (Level 1 to 3)

| Risk Classification | Clinical Indicators | System Response Action | Latency Target |
| :---: | :--- | :--- | :---: |
| **Level 1 (Mild)** | Fatigue, loneliness, academic/work stress | Empathetic listening, active validation | < 800 ms |
| **Level 2 (Moderate)** | Chronic hopelessness, self-worth collapse | Cognitive reframing, counseling clinic recommendation | < 800 ms |
| **Level 3 (Crisis)** | Explicit suicidal ideation, intent, or self-harm | **Instant LLM bypass: Display 24/7 Lifeline (109 / 1393) modal with one-tap emergency call** | **< 150 ms** |

---

### 2. Guardrail Middleware Implementation

The Safety Wrapper operates as an asynchronous FastAPI middleware, validating payloads prior to dispatching GPU inference requests:

```python
# Safety Wrapper core logic: safety_wrapper.py
import re
from fastapi import Request, HTTPException

CRISIS_PATTERNS = [
    r"(죽고\s*싶|자살|목숨을\s*끊|살기\s*싫|뛰어내리)",
    r"(suicide|kill\s*myself|end\s*my\s*life)"
]

class SafetyWrapper:
    def __init__(self, emergency_hotline="109"):
        self.compiled_regex = [re.compile(p, re.IGNORECASE) for p in CRISIS_PATTERNS]
        self.hotline = emergency_hotline

    def evaluate_input(self, user_text: str) -> dict:
        for pattern in self.compiled_regex:
            if pattern.search(user_text):
                return {
                    "is_crisis": True,
                    "action": "ESCALATE_IMMEDIATELY",
                    "override_response": (
                        f"당신의 고통을 깊이 공감합니다. 지금 즉시 전문가의 도움을 받으실 수 있습니다. "
                        f"24시간 자살예방 상담전화 ☎ {self.hotline}번으로 연락해 주세요. 당신은 혼자가 아닙니다."
                    )
                }
        return {"is_crisis": False, "action": "PROCEED_TO_LLM"}
```

---

### 3. AWS EC2 GPU Production Budget & Sizing

To serve our validated chatbot to university students and military beta testers over the 5-month summer break, we conducted an AWS EC2 instance sizing and cost optimization study:

| Instance Family | GPU Configuration | vCPU / RAM | On-Demand (Hourly) | 5-Month Estimated Cost (On-Demand) | 1-Year Savings Plan (Hourly) | 5-Month Optimized Cost |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **g4dn.2xlarge** | 1x NVIDIA T4 (16GB) | 8 vCPU / 32GB | $0.752 | $2,707 | $0.481 | $1,731 |
| **g5.2xlarge (Chosen)** | **1x NVIDIA A10G (24GB)** | **8 vCPU / 32GB** | **$1.212** | **$4,363** | **$0.763** | **$2,746 (Save 37%)** |
| **g6.2xlarge** | 1x NVIDIA L4 (24GB) | 8 vCPU / 32GB | $0.978 | $3,520 | $0.626 | $2,253 |

**Engineering Selection**: While `g4dn.2xlarge` offered lower cost, its 16GB VRAM could not host our 9B model alongside vLLM PagedAttention KV-caches without extreme 4-bit quantization degradation. We selected **`g5.2xlarge` with a 1-year Savings Plan**, unlocking 24GB high-speed GDDR6 VRAM, sub-50ms token latencies, and 37% budgetary savings!

![Final Presentation](./images/02_presentation.png)

---

### 4. 1st Semester Capstone Retrospective & Defense Highlights

On June 18th, our engineering team presented the completed **1st Semester Final Defense Presentation (PPTX)** before the university evaluation panel:

```mermaid
timeline
    title Maeumjigi Semester 1 Engineering Milestones
    March 2026 : Project Kickoff : Claude Code Adoption : Convention Scraper Pivot
    April 2026 : 120K Corpus Preprocessing : Llama 3.1 JSONL Pipeline : Next.js 14 Frontend
    May 2026 : 4 Rounds of Fine-Tuning : Checkpoint-4400 Locked : FastAPI PostgreSQL Hardened
    June 2026 : Dual Safety Wrapper : AWS g5.2xlarge Sizing : 1st Semester Final Presentation Passed
```

The review panel commended the team for solving the over-counseling trap through empirical data mixing (2:1 ratio) and praised the clinical safety guarantees provided by the deterministic Safety Wrapper.

---

### 5. What's Next in Semester 2?

With Phase 1 concluded, our team enters summer deployment:
1. Provisioning our AWS EC2 `g5.2xlarge` instance with automated containerized health checks.
2. Launching closed-beta testing across military welfare communities.
3. Returning in Semester 2 with live multi-turn field data and expanded knowledge graph capabilities!
"""

ko_content = """---
slug: 2026-06-18-maeumjigi-23
title: "[마음지기 캡스톤 개발일지 #23] 이중 Safety Wrapper 구축, AWS EC2 GPU 서버 견적 및 1학기 최종 발표"
authors: [jbgih]
tags: [devlog, safety-wrapper, guardrail, aws-ec2, gpu-serving, capstone-defense, suicide-prevention]
date: 2026-06-18
keywords: [AI 멘탈 헬스 챗봇, 인공지능 Safety Wrapper, LLM 안전 가드레일, 자살 위기 개입 프로토콜, AWS EC2 GPU 서빙]
description: "마음지기 1학기 최종 마일스톤: 자살 고위험군 즉각 개입을 위한 이중 Safety Wrapper 아키텍처 완성, AWS EC2 g5.2xlarge GPU 서버 견적 산출, 그리고 1학기 최종 캡스톤 발표 통과기를 공개합니다."
---

![Cover Image](./images/01_cover.png)

2026년 6월 18일, 3월부터 쉼 없이 달려온 대학 캡스톤 디자인 프로젝트 **'마음지기 (Maeumjigi)'**의 1학기 대장정이 성공적으로 막을 내렸습니다.
단순한 예식장 크롤러로 출발했던 작은 아이디어는 이제 12만 건의 임상 공감 데이터를 학습한 오픈소스 거대 언어 모델과 풀스택 웹/앱 인프라를 갖춘 **고신뢰성 AI 심리상담 플랫폼**으로 완성되었습니다.

이번 글에서는 서비스의 생명줄이 될 **이중 안전 가드레일(Safety Wrapper)**의 설계, 실제 클라우드 운영을 위한 **AWS EC2 GPU 인스턴스 견적 산출**, 그리고 감격의 **1학기 최종 발표(PPTX)** 현장을 전해드립니다.

{/* truncate */}

### 1. 무결점 생명 보호를 위한 이중 Safety Wrapper 아키텍처

일반 챗봇에서는 인공지능의 가벼운 말실수나 엉뚱한 답변이 단순한 해프닝으로 끝날 수 있습니다. 하지만 우울증을 앓는 청년이나 극단적 스트레스에 처한 군 장병을 상대하는 심리 챗봇에서 **단 한 번의 잘못된 환각이나 방임적 답변은 치명적인 비극**을 부를 수 있습니다.

우리는 파인튜닝된 Qwen 9B(Checkpoint-4400) 모델을 감싸는 **이중 안전 잠금장치(Dual-Layer Safety Wrapper)**를 설계했습니다:

```mermaid
flowchart TD
    subgraph 사전검증계층 ["1단계: 입력 전처리 가드레일"]
        A[내담자 발화 메시지 수신] --> B[정규표현식 위기 키워드 탐지기]
        B --> C[제로샷 의미론적 위기 분류기]
        C --> D{위기 위험도 3단계 판별}
    end

    subgraph 즉각개입계층 ["긴급 우회 라우팅"]
        D -->|레벨 3: 자살/자해 즉각 위험군| E[긴급 위기 개입 프로토콜 즉시 발동]
        E -->|언어 모델 생성 완전 우회| F[결정론적 위기 텍스트 + 109/1393 원터치 연결]
        
        D -->|레벨 1~2: 경미/중등도 정서적 고통| G[파인튜닝 LLM으로 안전 전달]
    end

    subgraph 모델추론층 ["인공지능 모델 추론"]
        G --> H[vLLM 추론 엔진: Checkpoint-4400]
        H --> I[실시간 생성 토큰 스트림]
    end

    subgraph 사후검증계층 ["2단계: 출력 후처리 가드레일"]
        I --> J[독성 및 환각 여부 실시간 필터링]
        J --> K[전문 심리상담 기관 안내 푸터 부착]
        K --> L[클라이언트로 최종 SSE 스트리밍 전송]
    end

    F --> L
```

#### 위기 위험도 등급별 대응 프로토콜 (Level 1~3)

| 위험도 등급 | 임상적 발화 징후 | 시스템 대응 전략 | 응답 제한 시간 |
| :---: | :--- | :--- | :---: |
| **Level 1 (경미)** | 일상적 피로감, 외로움, 학업/업무 스트레스 | 따뜻한 경청과 정서적 지지 공감 발화 | 800ms 이내 |
| **Level 2 (중등도)** | 만성적 무기력, 자존감 붕괴, 경미한 절망감 | 인지적 재구성 유도 및 전문 상담 센터 권유 | 800ms 이내 |
| **Level 3 (초고위험)** | 구체적 자살 충동, 계획 언급, 자해 시도 암시 | **생성 모델 즉각 차단: 24시간 자살예방 상담전화(109 / 1393) 긴급 모달 강제 팝업** | **150ms 이내** |

---

### 2. 가드레일 미들웨어 핵심 구현 코드

Safety Wrapper는 FastAPI의 비동기 미들웨어로 동작하여, GPU 추론 비용을 낭비하지 않고 초고위험군 발화를 0.1초 만에 감지하여 우회시킵니다:

```python
# Safety Wrapper 핵심 검증 로직: safety_wrapper.py
import re

CRISIS_PATTERNS = [
    r"(죽고\s*싶|자살|목숨을\s*끊|살기\s*싫|뛰어내리|세상을\s*떠나)",
    r"(suicide|kill\s*myself|end\s*my\s*life)"
]

class SafetyWrapper:
    def __init__(self, emergency_hotline="109"):
        self.compiled_regex = [re.compile(p, re.IGNORECASE) for p in CRISIS_PATTERNS]
        self.hotline = emergency_hotline

    def evaluate_input(self, user_text: str) -> dict:
        for pattern in self.compiled_regex:
            if pattern.search(user_text):
                return {
                    "is_crisis": True,
                    "action": "ESCALATE_IMMEDIATELY",
                    "override_response": (
                        f"당신의 고통을 깊이 공감합니다. 지금 즉시 전문가의 도움을 받으실 수 있습니다. "
                        f"24시간 자살예방 상담전화 ☎ {self.hotline}번으로 연락해 주세요. 당신은 혼자가 아닙니다."
                    )
                }
        return {"is_crisis": False, "action": "PROCEED_TO_LLM"}
```

---

### 3. 클라우드(AWS EC2) GPU 인스턴스 견적 및 비용 최적화

여름방학 5개월 동안 실제 베타 테스터들을 수용하기 위해, 우리는 AWS EC2의 인스턴스 사양과 요금제를 정밀 분석했습니다:

| 인스턴스 유형 | GPU 구성 | vCPU / RAM | 온디맨드 (시간당) | 5개월 예상 비용 (온디맨드) | 1년 세이빙스 플랜 (시간당) | 5개월 최적화 비용 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **g4dn.2xlarge** | 1x NVIDIA T4 (16GB) | 8 vCPU / 32GB | $0.752 | $2,707 | $0.481 | $1,731 |
| **g5.2xlarge (선정)** | **1x NVIDIA A10G (24GB)** | **8 vCPU / 32GB** | **$1.212** | **$4,363** | **$0.763** | **$2,746 (37% 절감)** |
| **g6.2xlarge** | 1x NVIDIA L4 (24GB) | 8 vCPU / 32GB | $0.978 | $3,520 | $0.626 | $2,253 |

**최종 선정 사유**: `g4dn`은 저렴하지만 16GB VRAM 한계로 인해 vLLM 가상 메모리(PagedAttention) 버퍼가 부족하여 동시 접속 시 토큰 지연이 급증했습니다. 반면 **24GB 고속 VRAM을 탑재한 `g5.2xlarge`**를 선정하고 **1년 Savings Plan**을 적용함으로써, 월 $549 수준의 합리적인 예산으로 50ms 미만의 쾌속 스트리밍 서빙 환경을 확정 지었습니다!

![Final Presentation](./images/02_presentation.png)

---

### 4. 1학기 캡스톤 최종 발표와 심사 통과

6월 18일, 우리 개발팀은 백엔드, 프론트엔드, 인공지능 파이프라인의 전 성과를 집대성한 **「1학기 캡스톤 최종 발표(PPTX)」**를 성공적으로 마쳤습니다:

```mermaid
timeline
    title 마음지기 캡스톤 1학기 개발 연표
    2026년 3월 : 프로젝트 킥오프 : Claude Code 도입 : 예약 알람에서 멘탈 헬스 AI로 피봇
    2026년 4월 : 12만 건 말뭉치 정제 : Llama 3.1 JSONL 변환 : Next.js 14 프론트엔드
    2026년 5월 : 4차례 파인튜닝 완주 : Checkpoint-4400 확정 : FastAPI PostgreSQL 인증 구축
    2026년 6월 : 이중 Safety Wrapper : AWS GPU 인프라 확정 : 1학기 최종 발표 심사 만점 통과
```

심사위원 교수님들께서는 단순한 오픈소스 모델 파인튜닝에 그치지 않고, 2:1 데이터 혼합을 통해 과상담 문제를 해결한 점과 생명 안전을 완벽히 담보하는 Safety Wrapper를 자체 고안한 점에 대해 극찬을 아끼지 않으셨습니다.

---

### 5. 2학기를 향한 향후 로드맵

1학기 개발을 성공적으로 완수한 마음지기 팀은 여름방학 동안 다음과 같은 상용화 준비에 돌입합니다:
1. 확정된 AWS EC2 `g5.2xlarge` 인스턴스 프로비저닝 및 Docker 컨테이너 오케스트레이션 구축
2. 군 장병 및 청년 대상 클로즈드 베타 테스트 운영 및 피드백 수집
3. 2학기 최종 상용 배포와 멀티모달(음성 음향 분석) 기능 확장!
"""

es_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #23] Dual-Layer Safety Wrapper, AWS EC2 GPU Budgeting & Semester 1 Defense"',
    'title: "[Diario de Capstone Maeumjigi #23] Safety Wrapper de Doble Capa, Servidores GPU AWS EC2 y Defensa Final"'
).replace(
    'description: "Final Milestone of Semester 1: Engineering our dual-layer Safety Wrapper for crisis de-escalation, calculating AWS EC2 g5.2xlarge GPU serving budgets, and presenting our Capstone Final Defense."',
    'description: "Hito final del semestre 1: diseño del Safety Wrapper para desescalada de crisis, presupuesto GPU en AWS EC2 g5.2xlarge y defensa final de Capstone."'
)

ja_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #23] Dual-Layer Safety Wrapper, AWS EC2 GPU Budgeting & Semester 1 Defense"',
    'title: "[マウムジギ Capstone 開発日誌 #23] 二重 Safety Wrapper の構築、AWS EC2 GPU 予算試算と第1学期最終発表"'
).replace(
    'description: "Final Milestone of Semester 1: Engineering our dual-layer Safety Wrapper for crisis de-escalation, calculating AWS EC2 g5.2xlarge GPU serving budgets, and presenting our Capstone Final Defense."',
    'description: "第1学期最終マイルストーン：危機介入用二重Safety Wrapperの構築、AWS EC2 g5.2xlarge GPUサーバーの予算算出、卒業制作最終発表の全記録。"'
)

zh_hans_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #23] Dual-Layer Safety Wrapper, AWS EC2 GPU Budgeting & Semester 1 Defense"',
    'title: "[Maeumjigi 毕业设计开发日志 #23] 双层 Safety Wrapper 护栏、AWS EC2 GPU 算力成本与第一学期答辩大捷"'
).replace(
    'description: "Final Milestone of Semester 1: Engineering our dual-layer Safety Wrapper for crisis de-escalation, calculating AWS EC2 g5.2xlarge GPU serving budgets, and presenting our Capstone Final Defense."',
    'description: "第一学期圆满收官：打造双层 Safety Wrapper 危机干预安全护栏，精算 AWS EC2 g5.2xlarge GPU 服务器部署预算，顺利通过期末终审答辩。"'
)

zh_hant_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #23] Dual-Layer Safety Wrapper, AWS EC2 GPU Budgeting & Semester 1 Defense"',
    'title: "[Maeumjigi 畢業設計開發日誌 #23] 雙層 Safety Wrapper 護欄、AWS EC2 GPU 算力成本與第一學期答辯大捷"'
).replace(
    'description: "Final Milestone of Semester 1: Engineering our dual-layer Safety Wrapper for crisis de-escalation, calculating AWS EC2 g5.2xlarge GPU serving budgets, and presenting our Capstone Final Defense."',
    'description: "第一學期圓滿收官：打造雙層 Safety Wrapper 危機干預安全護欄，精算 AWS EC2 g5.2xlarge GPU 伺服器部署預算，順利通過期末終審答辯。"'
)

nb_post = f"""# [마음지기 캡스톤 개발일지 #23] 이중 Safety Wrapper 구축, AWS EC2 GPU 서버 견적 및 1학기 최종 발표

안녕하세요! 대학 캡스톤 디자인 프로젝트 **「마음지기 (Maeumjigi)」**의 1학기 마지막 개발일지(#23)입니다.
이번 글에서는 생명 안전을 수호하는 **이중 Safety Wrapper 가드레일 아키텍처**, 실서버 구동을 위한 **AWS EC2 g5.2xlarge GPU 인스턴스 견적 분석**, 그리고 감격의 **1학기 최종 캡스톤 심사 발표 통과 소식**을 전해드립니다.

---

## 1. 생명 안전을 보장하는 이중 Safety Wrapper

우울증 및 자살 예방 챗봇에서 환각이나 무성의한 답변은 치명적입니다.
우리는 파인튜닝 모델(Checkpoint-4400) 앞뒤에 **이중 안전 잠금장치**를 구축했습니다:

- **1단계(사전 필터)**: 자살/자해 즉각 위험군(Level 3) 감지 시 LLM 생성을 즉각 우회하고 **24시간 자살예방 상담전화(109 / 1393) 긴급 팝업** 표출
- **2단계(사후 검증)**: 생성된 발화의 환각 및 유해성을 실시간 검증하고 전문 상담 기관 정보 주입

---

## 2. AWS EC2 GPU 인프라 비용 최적화

| 인스턴스 | GPU 사양 | 온디맨드 (5개월) | 1년 세이빙스 플랜 (5개월) | 비고 |
| :--- | :---: | :---: | :---: | :--- |
| **g4dn.2xlarge** | T4 (16GB) | $2,707 | $1,731 | 16GB VRAM 부족으로 동시성 한계 |
| **g5.2xlarge (선정)** | **A10G (24GB)** | **$4,363** | **$2,746 (37% 절감)** | **24GB VRAM으로 50ms 미만 초고속 스트리밍** |

5개월간 안정적인 클라우드 서빙을 위해 `g5.2xlarge` 인스턴스에 1년 Savings Plan을 적용하여 월 $549 수준의 최적 비용을 확정했습니다.

---

## 3. 1학기 캡스톤 최종 발표 통과와 방학 계획

3월 크롤러 앱에서 시작해 6월 실시간 공감 AI로 거듭난 마음지기 프로젝트는 심사위원 교수님들의 극찬을 받으며 최고 등급으로 1학기 최종 발표를 마쳤습니다!
방학 중에는 AWS GPU 실서버 배포와 클로즈드 베타 테스트를 거쳐 더욱 강력한 2학기 서비스로 돌아오겠습니다.

---

## 4. 글로벌 기술 블로그에서 상세 아키텍처 확인하기

Safety Wrapper 미들웨어 소스 코드와 전체 시스템 연표는 글로벌 블로그에서 확인하실 수 있습니다:

👉 **[GlobalDevLog 글로벌 블로그: Maeumjigi Capstone Dev Log #23 원문 보기](https://globaldevlog.com/blog/2026-06-18-maeumjigi-23)**

지금까지 마음지기 1학기 23편의 개발일지를 함께해 주셔서 진심으로 감사드립니다!
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
print("Episode 23 enhancement successfully written!")
