# -*- coding: utf-8 -*-
import os

ep_folder = "2026-04-01-maeumjigi-4"
gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-04-01\maeumjigi"

en_content = """---
slug: 2026-04-01-maeumjigi-4
title: "[Maeumjigi Capstone Dev Log #4] Full-Scale Data Preprocessing: Llama 3.1 Chat Template & Autonomous JSONL Pipeline"
authors: [jbgih]
tags: [devlog, llama-3-1, data-preprocessing, jsonl, fine-tuning, ai-hub, nlp]
date: 2026-04-01
keywords: [Llama 3.1 Chat Template, AI Hub Preprocessing Pipeline, JSONL Multi-turn Formatting, LLM Instruction Fine-Tuning, Empathetic Dialogue Dataset]
description: "Executing autonomous data engineering for Maeumjigi: transforming 120,000 raw Korean empathetic dialogue records into strict Llama 3.1 special token JSONL datasets."
---

![Cover Image](./images/01_cover.png)

April 1, 2026, was the day our engineering team launched the automated preprocessing pipeline for the massive counseling corpora that would form the foundation of **Maeumjigi**. Training a high-performance open-source Large Language Model (LLM) like **Meta Llama 3.1** requires rigorous data hygiene: converting unstructured multi-party dialogues into clean, token-bounded, and special-token-aligned instruction datasets.

{/* truncate */}

### 1. The Challenge of Raw Multi-Turn Dialogue Corpora

Our raw data originated from public Korean empathetic dialogue and counseling datasets (AI Hub). While academically valuable, raw dialogue data poses critical obstacles for instruction fine-tuning:
1. **Inconsistent Turn Structures**: Casual multi-speaker exchanges frequently have broken turns (e.g., three consecutive user utterances followed by an empty response).
2. **Personal Identifiable Information (PII)**: Raw transcripts contain phone numbers, specific military unit identifiers, and real names that must be strictly anonymized.
3. **Token Length Exceedance**: Unbounded conversations often exceed the target attention context window (2,048 tokens), triggering out-of-memory (OOM) failures during PyTorch gradient computation.

---

### 2. Autonomous Preprocessing Pipeline Architecture

Instead of having human engineers manually massage CSV records, we instructed **Claude Code** to autonomously architect and execute a 5-stage transformation pipeline based on our blueprint document: `llama31_finetuning_data_preprocessing_plan_short.md`.

```mermaid
flowchart TD
    subgraph Ingestion ["Stage 1: Raw Data Ingestion"]
        A[AI Hub Raw Corpus: 124,500 Dialogues] --> B[Schema Normalizer]
    end

    subgraph Cleansing ["Stage 2: Sanitization & Filtering"]
        B --> C[PII Masking & Regex De-identification]
        C --> D[Turn Parity Validator: Eliminate Single-Turn & Orphan Rows]
    end

    subgraph Tokenization ["Stage 3: Token Budgeting & Bounds"]
        D --> E[Llama 3.1 BPE Tokenizer Profiling]
        E --> F[Context Truncation: Hard Ceiling at 2048 Tokens]
    end

    subgraph Formatting ["Stage 4: Chat Template Injection"]
        F --> G[Special Token Ingestion: begin_of_text, start_header_id, eot_id]
        G --> H[Final Train/Val Split: 90/10 Ratio]
    end

    H --> I[(maeumjigi_llama31_train.jsonl: 99,000)]
    H --> J[(maeumjigi_llama31_val.jsonl: 11,000)]
```

---

### 3. Strict Llama 3.1 Chat Template Formatting

Llama 3.1 introduces a strict tokenized header structure that models must strictly learn to avoid runaway generation loops:

```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are 'Maeumjigi', an empathetic clinical psychological counseling AI companion. Listen with deep empathy and never judge.<|eot_id|>
<|start_header_id|>user<|end_header_id|>

I feel overwhelmed by military life and nobody understands me.<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>

Adapting to military service can feel deeply isolating. It is completely natural to feel overwhelmed. Would you like to share what was hardest today?<|eot_id|>
```

Every single training sample was converted into a structured JSONL entry containing exact role tokens:

```python
# Core formatting logic implemented in transform_llama31.py
import json

def format_llama31_sample(system_prompt: str, turns: list) -> dict:
    formatted_text = "<|begin_of_text|>"
    formatted_text += f"<|start_header_id|>system<|end_header_id|>\\n\\n{system_prompt}<|eot_id|>"
    
    for turn in turns:
        role = turn["role"] # "user" or "assistant"
        content = turn["content"].strip()
        formatted_text += f"<|start_header_id|>{role}<|end_header_id|>\\n\\n{content}<|eot_id|>"
        
    return {"text": formatted_text}
```

---

### 4. Data Preprocessing Attrition & Statistics

The data cleansing pipeline strictly dropped malformed rows to guarantee training convergence. The quantitative attrition audit:

| Preprocessing Stage | Remaining Records | Dropped Count | Exclusion Rationale |
| :--- | :---: | :---: | :--- |
| **Raw AI Hub Input** | 124,500 | - | Baseline multi-speaker transcripts |
| **PII & Malformed Encoding** | 120,400 | 4,100 | Encoding errors, exposed phone/unit IDs |
| **Turn Parity Validation** | 112,200 | 8,200 | Orphan utterances, missing assistant responses |
| **Token Budgeting (< 2048)** | 110,000 | 2,200 | Exceeded context ceiling; risk of mid-thought cut |
| **Final Train Set (90%)** | **99,000** | - | Structured instruction tuning samples |
| **Final Val Set (10%)** | **11,000** | - | Out-of-distribution benchmark evaluation |

![Terminal Screenshot](./images/02_term.png)

---

### 5. Day 4 Takeaways & Milestones

1. **Fully Automated Data Pipeline**: Processing over 120,000 dialogue pairs was executed completely hands-free by our AI agent in under 45 minutes.
2. **Zero Syntax Drift**: Every record adhered to the exact `Llama 3.1` special token specifications, preventing generation loop bugs during fine-tuning.
3. **Ready for Distributed Training**: Output datasets were validated and staged for GPU cluster deployment on Google Colab and AWS.

In Dev Log #5, we dive into the financial reality of large-scale LLM data synthesis and the API cost challenges that followed!
"""

ko_content = """---
slug: 2026-04-01-maeumjigi-4
title: "[마음지기 캡스톤 개발일지 #4] 본격 데이터 전처리: Llama 3.1 챗 템플릿과 자율 JSONL 파이프라인 구축"
authors: [jbgih]
tags: [devlog, llama-3-1, data-preprocessing, jsonl, fine-tuning, ai-hub, nlp]
date: 2026-04-01
keywords: [Llama 3.1 챗 템플릿, AI Hub 전처리 파이프라인, JSONL 멀티턴 변환, LLM 인스트럭션 파인튜닝, 공감 대화 데이터셋]
description: "마음지기 프로젝트의 핵심 엔진 구축: AI Hub 12만 건의 한국어 심리 상담 말뭉치를 Llama 3.1 전용 특수 토큰 기반의 무결점 JSONL 파인튜닝 데이터셋으로 자율 변환한 전 과정을 공개합니다."
---

![Cover Image](./images/01_cover.png)

2026년 4월 1일은 **마음지기**의 핵심 인공지능 두뇌가 될 **Meta Llama 3.1** 모델을 학습시키기 위해, 방대한 양의 한국어 공감 대화 원시 데이터를 모델이 완벽히 이해할 수 있는 인스트럭션 데이터로 변환하는 본격적인 데이터 전처리가 가동된 날입니다. 고성능 파인튜닝 모델의 성패는 모델 파라미터보다 **데이터 전처리의 무결성**에 달려 있습니다.

{/* truncate */}

### 1. 원시 대화 말뭉치의 한계와 전처리 과제

우리가 수집한 AI Hub의 한국어 감정·공감 대화 말뭉치는 학술적으로 훌륭한 자원이었지만, 원시 상태 그대로는 LLM 파인튜닝에 바로 투입할 수 없는 심각한 기술적 문제점들을 안고 있었습니다:
1. **불규칙한 턴 구조**: 실제 대화 특성상 사용자가 혼자 세 번 연속 발화하거나, 상담사의 응답 없이 종료되는 결측치 행이 다수 존재.
2. **개인 식별 정보(PII) 잔존**: 전화번호, 부대 명칭, 실명 등 개인정보 노출 위험.
3. **토큰 길이 초과**: 턴 수가 너무 긴 대화는 모델의 어텐션 윈도우(2,048 토큰)를 초과하여 PyTorch 학습 중 치명적인 CUDA Out of Memory(OOM)를 유발.

---

### 2. 자율 데이터 전처리 5단계 파이프라인 아키텍처

우리는 수작업으로 수십만 줄의 CSV를 정제하는 대신, 사전 기획서인 `llama31_finetuning_data_preprocessing_plan_short.md`를 바탕으로 **Claude Code**가 스스로 파이프라인을 구축하고 실행하도록 설계했습니다.

```mermaid
flowchart TD
    subgraph 수집단계 ["1단계: 원시 말뭉치 수집 및 파싱"]
        A[AI Hub 원시 대화 데이터: 124,500건] --> B[JSON/CSV 스키마 정규화]
    end

    subgraph 정제단계 ["2단계: 개인정보 마스킹 및 결측 필터링"]
        B --> C[정규표현식 기반 PII 마스킹 및 실명 비식별화]
        C --> D[단일 턴 및 무응답 고아 행 제거]
    end

    subgraph 토큰계측 ["3단계: BPE 토크나이징 및 길이 제한"]
        D --> E[Llama 3.1 BPE 토크나이저 길이 계측]
        E --> F[2,048 토큰 상한선 초과 샘플 절삭 및 필터링]
    end

    subgraph 포맷변환 ["4단계: 특수 토큰 주입 및 데이터셋 분할"]
        F --> G[Llama 3.1 전용 특수 토큰 주입: begin_of_text, eot_id]
        G --> H[90:10 비율 Train/Val 무작위 셔플 분할]
    end

    H --> I[(maeumjigi_llama31_train.jsonl: 99,000건)]
    H --> J[(maeumjigi_llama31_val.jsonl: 11,000건)]
```

---

### 3. Llama 3.1 전용 챗 템플릿(Chat Template) 엄격 준수

Llama 3.1은 이전 세대 모델과 달리 엄격한 헤더 식별자(`start_header_id`, `end_header_id`, `eot_id`)를 사용합니다. 이를 하나라도 누락하면 모델이 답변을 멈추지 않고 끝없이 자가 발화를 이어가는 무한 루프 버그가 발생합니다.

```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

당신은 심리적 위기에 처한 내담자를 따뜻하게 위로하는 전문 공감 심리상담 AI '마음지기'입니다. 경청하고 지지해 주세요.<|eot_id|>
<|start_header_id|>user<|end_header_id|>

군 생활이 너무 힘들고 아무도 제 마음을 몰라주는 것 같아요.<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>

낯선 군 환경 속에서 홀로 모든 무게를 견디느라 마음이 참 많이 지치셨겠어요. 어떤 부분이 가장 버겁게 느껴지시나요?<|eot_id|>
```

이 규칙을 만족하도록 파이썬 변환 스크립트(`transform_llama31.py`)를 작성하여 모든 대화 세션을 JSONL 규격으로 변환했습니다:

```python
# Llama 3.1 Chat Template 변환 핵심 함수
import json

def format_llama31_sample(system_prompt: str, turns: list) -> dict:
    formatted_text = "<|begin_of_text|>"
    formatted_text += f"<|start_header_id|>system<|end_header_id|>\\n\\n{system_prompt}<|eot_id|>"
    
    for turn in turns:
        role = turn["role"] # "user" 또는 "assistant"
        content = turn["content"].strip()
        formatted_text += f"<|start_header_id|>{role}<|end_header_id|>\\n\\n{content}<|eot_id|>"
        
    return {"text": formatted_text}
```

---

### 4. 단계별 데이터 필터링 통계 분석

철저한 데이터 위생(Data Hygiene) 원칙에 따라 결함이 있는 데이터를 과감히 배제한 정량 필터링 통계표입니다:

| 전처리 단계 | 잔여 데이터 수 | 탈락 데이터 수 | 제외 사유 |
| :--- | :---: | :---: | :--- |
| **원시 AI Hub 데이터** | 124,500건 | - | 다자간 상담 및 공감 대화 원본 |
| **개인정보(PII) 및 인코딩 결함** | 120,400건 | 4,100건 | 전화번호/부대명 노출, 깨진 문자열 |
| **턴 정합성 검증 탈락** | 112,200건 | 8,200건 | 단일 발화 종결, 상담사 미응답 결측치 |
| **토큰 길이(>2048) 초과** | 110,000건 | 2,200건 | 어텐션 윈도우 초과로 문맥 절단 위험 |
| **최종 학습 데이터셋 (Train 90%)** | **99,000건** | - | 모델 파인튜닝용 정제 JSONL |
| **최종 검증 데이터셋 (Val 10%)** | **11,000건** | - | 정량적 손실(Loss) 평가용 검증셋 |

![Terminal Screenshot](./images/02_term.png)

---

### 5. 4일차 성과 요약 및 다음 단계

1. **완전자율 데이터 엔지니어링**: AI 에이전트 단독으로 12만 건의 방대한 원시 대화를 45분 만에 완벽히 정제 및 변환 완료.
2. **Llama 3.1 전용 템플릿 무결성 확보**: 특수 토큰 누락 없이 11만 건의 정제 JSONL 구축 완료.
3. **GPU 클러스터 학습 준비 완료**: 구글 코랩 및 AWS GPU 인스턴스에 즉시 투입 가능한 상태로 검증 완료.

다음 5화에서는 10만 건의 감정 데이터를 합성하는 과정에서 맞닥뜨린 대규모 API 비용 폭탄 사태와 그 극복기를 들려드리겠습니다!
"""

es_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #4] Full-Scale Data Preprocessing: Llama 3.1 Chat Template & Autonomous JSONL Pipeline"',
    'title: "[Diario de Capstone Maeumjigi #4] Preprocesamiento de Datos: Plantilla Llama 3.1 y Pipeline JSONL"'
).replace(
    'description: "Executing autonomous data engineering for Maeumjigi: transforming 120,000 raw Korean empathetic dialogue records into strict Llama 3.1 special token JSONL datasets."',
    'description: "Ingeniería de datos para Maeumjigi: transformación de 120,000 diálogos empáticos coreanos en datasets JSONL con tokens especiales de Llama 3.1."'
)

ja_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #4] Full-Scale Data Preprocessing: Llama 3.1 Chat Template & Autonomous JSONL Pipeline"',
    'title: "[マウムジギ Capstone 開発日誌 #4] 本格データ前処理: Llama 3.1 チャットテンプレートと自律型 JSONL パイプライン"'
).replace(
    'description: "Executing autonomous data engineering for Maeumjigi: transforming 120,000 raw Korean empathetic dialogue records into strict Llama 3.1 special token JSONL datasets."',
    'description: "マウムジギの核心データ構築：12万件の対話コーパスをLlama 3.1専用の特殊トークン準拠JSONLデータセットへと自律変換した全工程を解説。"'
)

zh_hans_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #4] Full-Scale Data Preprocessing: Llama 3.1 Chat Template & Autonomous JSONL Pipeline"',
    'title: "[Maeumjigi 毕业设计开发日志 #4] 全面数据预处理: Llama 3.1 对话模板与自主 JSONL 数据流水线"'
).replace(
    'description: "Executing autonomous data engineering for Maeumjigi: transforming 120,000 raw Korean empathetic dialogue records into strict Llama 3.1 special token JSONL datasets."',
    'description: "Maeumjigi 核心数据工程：将 12 万条共情对话语料自主转化为符合 Llama 3.1 特殊标记格式的高质量 JSONL 微调数据集。"'
)

zh_hant_content = en_content.replace(
    'title: "[Maeumjigi Capstone Dev Log #4] Full-Scale Data Preprocessing: Llama 3.1 Chat Template & Autonomous JSONL Pipeline"',
    'title: "[Maeumjigi 畢業設計開發日誌 #4] 全面數據預處理: Llama 3.1 對話模板與自主 JSONL 數據流水線"'
).replace(
    'description: "Executing autonomous data engineering for Maeumjigi: transforming 120,000 raw Korean empathetic dialogue records into strict Llama 3.1 special token JSONL datasets."',
    'description: "Maeumjigi 核心數據工程：將 12 萬條共情對話語料自主轉化為符合 Llama 3.1 特殊標記格式的高質量 JSONL 微調數據集。"'
)

nb_post = f"""# [마음지기 캡스톤 개발일지 #4] 본격 데이터 전처리: Llama 3.1 챗 템플릿과 자율 JSONL 파이프라인 구축

안녕하세요! 대학 캡스톤 디자인 프로젝트 **「마음지기 (Maeumjigi)」**의 4일차 개발일지입니다.
이번 글에서는 모델의 상담 성능을 좌우하는 **12만 건 규모의 대규모 심리상담 대화 말뭉치 전처리 파이프라인**을 구축하고, Meta의 최신 오픈소스 모델인 **Llama 3.1** 전용 JSONL 포맷으로 자동 변환한 과정을 정리합니다.

---

## 1. 데이터 전처리의 핵심 난관

AI Hub에서 수집한 원본 대화 데이터는 다음과 같은 문제점이 있어 곧바로 모델 파인튜닝에 사용할 수 없었습니다:
1. **불완전한 발화 턴**: 사용자가 연달아 말하거나 상담사 응답이 누락된 고아 행 다수 존재
2. **개인정보(PII) 노출**: 전화번호, 부대명, 실명 등이 노출될 위험
3. **토큰 초과**: 2,048 토큰 상한선을 초과하여 GPU OOM(Out of Memory)을 유발할 위험

---

## 2. 자율 5단계 전처리 파이프라인

Claude Code 에이전트와 함께 구축한 데이터 전처리 아키텍처는 다음과 같습니다:

```
[원시 AI Hub 말뭉치 124,500건]
      ↓ (정규표현식 기반 PII 마스킹)
[결측치 및 단일 턴 제거 (8,200건 탈락)]
      ↓ (Llama 3.1 BPE 토크나이저 길이 계측)
[2,048 토큰 초과 데이터 제거 (2,200건 탈락)]
      ↓ (Llama 3.1 특수 토큰 주입: begin_of_text, eot_id)
[최종 JSONL 데이터셋 분할: Train 99,000건 / Val 11,000건]
```

---

## 3. Llama 3.1 특수 토큰 템플릿 엄격 준수

Llama 3.1은 `<|start_header_id|>`와 `<|eot_id|>` 같은 전용 헤더 토큰을 사용해야만 모델이 무한 발화를 일으키지 않습니다.
모든 샘플을 이 규칙에 맞춰 포맷팅하여 총 11만 건의 정제 데이터셋을 단 45분 만에 완성했습니다.

| 전처리 단계 | 잔여 샘플 수 | 탈락 건수 | 비고 |
| :--- | :---: | :---: | :--- |
| **원시 데이터** | 124,500건 | - | 초기 원시 말뭉치 |
| **PII & 결측 제거** | 112,200건 | 12,300건 | 비식별화 및 단일 턴 제거 |
| **토큰 길이 필터링** | 110,000건 | 2,200건 | 2048 토큰 상한선 통과 |
| **최종 Train 셋** | **99,000건** | - | 90% 훈련 데이터셋 |
| **최종 Val 셋** | **11,000건** | - | 10% 정량 검증 데이터셋 |

---

## 4. 글로벌 기술 블로그에서 코드 및 Mermaid 다이어그램 확인하기

전체 파이썬 변환 스크립트 코드 스니펫과 아키텍처 다이어그램은 글로벌 블로그에서 확인하실 수 있습니다:

👉 **[GlobalDevLog 글로벌 블로그: Maeumjigi Capstone Dev Log #4 원문 보기](https://globaldevlog.com/blog/2026-04-01-maeumjigi-4)**

다음 5편에서는 대규모 합성 데이터 생성 중 마주한 API 비용 문제와 극복 과정을 전해드리겠습니다!
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
print("Episode 4 enhancement successfully written!")
