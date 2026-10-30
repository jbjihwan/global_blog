---
title: 소개 (About) & 글로벌 기술 블로그
description: 개발자 박지환(jbjihwan) 및 글로벌 기술 블로그 소개 - AI 시스템, 로보틱스, 컴퓨터 비전, 재정 감사 AI, 공급망 보안 엔지니어링 실전 기록.
keywords: [블로그 소개, 개발자 소개, 박지환, 인공지능 엔지니어, 로보틱스, 컴퓨터 비전, 강화학습, 예산 AI, 위기 감지, 편집 원칙]
---

# 소개 (About) & 글로벌 기술 블로그

**글로벌 기술 블로그(Global Dev Blog)**에 오신 것을 환영합니다. 본 블로그는 AI 및 로보틱스 소프트웨어 엔지니어 **박지환(jbjihwan)**이 직접 연구하고 구축한 실전 소프트웨어 시스템, 엣지·서버 배포 트러블슈팅, 아키텍처 트레이드오프 및 성능 벤치마크를 기록하는 엔지니어링 연구 일지입니다.

단순한 이론 요약을 넘어, 실제 코드 배포 과정에서 마주치는 하드웨어 한계, 데이터 불균형, 실시간성 제약, 실패와 돌파 과정을 있는 그대로 공유합니다.

---

## 👨‍💻 엔지니어 소개

- **자율주행 & 강화학습 (Reinforcement Learning)**: MDP 정의, 648개 연속 상태 공간 이산화, 조밀한 진행 보상 형성(Reward Shaping), Webots 시뮬레이션 기반 학습 및 아두이노(Arduino) 실기체 Sim-to-Real 하드웨어 전이.
- **딥 컴퓨터 비전 & 지능형 교통 (ITS)**: 초당 30 FPS 실시간 파이프라인, 객체 탐지(YOLOv3/v5/v8), 고속 CSRT 광학 추적, 딥러닝 초해상도(EDSR, FSRCNN) 복원, 다수결 투표 기반 한국형 차량 번호판 인식(ANPR) 엔진.
- **고위험 특화 NLP & AI 안전성 (Safety AI)**: 극단적 클래스 불균형(524:1) 하에서의 순서형 회귀(Ordinal Regression), 약지도 레이블 과신 보정, 순서형 트리 단조성 보장, 서브 밀리초 결정론적 Safety Wrapper 가드레일.
- **공공 재정 감사 AI (Autonomous Budget Audit)**: 환각율 0.00%의 Text-to-SQL 정밀 금융 산출, 3차원 표적 분할(85% 일상 노이즈 제거), GraphRAG 법인등기 지배구조 연계 바지사장 담합 적발.
- **풀스택 ML 인프라 & 공급망 보안**: 고처리량 FastAPI 마이크로서비스, PostgreSQL / Redis 인프라, `npm overrides` 및 `--omit=dev` 기반 전이 의존성 보안 하드닝.

---

## 🛡️ 콘텐츠 검증 및 편집 원칙 (Editorial Policy)

범람하는 단순 생성형 AI 요약 사이트와 차별화하기 위해, **Global Dev Blog는 엄격한 엔지니어링 집필 원칙을 준수합니다**:

1. **100% 실험 재현 및 직접 검증 원칙**:  
   본 블로그에 게재되는 모든 아키텍처 패턴, SQL 쿼리, 머신러닝 파이프라인 및 보안 해결책은 실제 하드웨어 랩(NVIDIA RTX 4060 GPU, Ubuntu Linux / WSL2, Python 3.12, TypeScript, Webots)에서 직접 코드를 실행하고 테스트를 통과한 결과만을 기반으로 작성됩니다.
2. **환각 코드(Zero Hallucination) 배제**:  
   검증되지 않은 이론적 코드나 일반론적인 AI 답변을 복사하지 않습니다. 모든 장애 사례, 벤치마크 지표, 예외 트레이스는 실제 테스트 하네스 및 배포 로그에서 직접 캡처합니다.
3. **실패 사례와 트레이드오프 투명 공개**:  
   버퍼 데드락, 순환 참조 크래시, 베이즈 사전확률 붕괴 등 실제 시스템 구축 시 겪은 난제와 방어 노하우를 솔직하게 공유하는 것이 동료 엔지니어들에게 가장 가치 있다고 믿습니다.
4. **오픈소스 책임성**:  
   모든 아티클은 검증 가능한 실제 GitHub 저장소([github.com/jbjihwan](https://github.com/jbjihwan))와 연결되어 있으며, 누구나 소스코드를 클론하여 검증할 수 있습니다.

---

## 📚 독창적 자체 개발 R&D 시리즈 (총 44편)

### 1. 🚨 [고위험 특화 AI] 자살/위기 텍스트 정밀 감지 파이프라인 (총 4편)
생명과 직결된 심리적 위기 발화의 미탐(FNR)을 원천 차단하기 위한 임상 특화 NLP 파이프라인:
- 524배 베이즈 사전확률 왜곡을 극복하는 2단계 하이브리드 트리아지(누적 관문 + Argmax).
- 순서형 LightGBM 트리 단조성 보장 및 0% 확률 붕괴 방어.
- 14일 시계열 감정 극단값 편향 방어 (86.7% 오경보 제거).
- 25-Fold 중첩 교차검증(Nested CV) 기반 2차 데이터 누수 완벽 차단.

### 2. 🏛️ 국가 예산 AI 감사 6부작 (총 6편)
공공 조달 및 재정 데이터셋의 부정 수급을 자율 추적하는 전주기 시스템:
- 0.00% 금융 계산 환각을 보장하는 Text-to-SQL 감사 쿼리 엔진.
- 수십만 건 조달 데이터에서 85% 일상 소모품을 걷어내는 3차원 표적 분할.
- 법인등기부 및 DART 지배구조 연계 GraphRAG 바지사장 카르텔 격파.
- 20개 테스트 하네스 전수 검증 및 실시간 감사관 종합 웹 포털 v3.0.

### 3. 🧠 마음지기 캡스톤 개발일지 (총 23편)
AI 자살 예방 상담 챗봇 캡스톤 디자인 전주기 개발 기록:
- 대규모 LLM 파이프라인을 활용한 위기 상담 합성 데이터 생성.
- Llama 3.1 LoRA 경량 파인튜닝 (2:1 감성:일상 황금 비율).
- 위기 상황 즉각 개입을 위한 서브 밀리초 결정론적 Safety Wrapper 가드레일.
- AWS EC2 GPU 인프라 배포 및 1학기 최종 발표 시연.

### 4. 🚗 Blackbox ANPR & 차선 침범 비전 AI 시스템 (총 5편)
고속도로 블랙박스 저화질 영상을 실시간 처리하는 엣지 비전 시스템:
- 6단계 엔드투엔드 파이프라인 (30 FPS 실시간 보장).
- 차선 다항식 피팅 및 기하학적 바운딩 박스 IoU 침범 판정.
- YOLOv3 차량 ROI ➡️ YOLOv5 번호판 ➡️ CSRT 광학 추적 계층 구조.
- EDSR 딥 초해상도 복원 및 11단계 다수결 투표 한국형 번호판 OCR.

### 5. 🤖 Webots Q-Learning 자율주행 강화학습 (총 5편)
제로 지식 탐험에서 결정론적 장애물 회피까지의 강화학습 여정:
- 6개 방향 거리 센서를 648개 이산 상태 공간으로 압축하는 설계.
- 희소 보상 기아 상태를 극복하는 진행 속도/거리 델타 기반 조밀 보상 형성.
- 12개 장애물 로컬 미니마 탈출을 위한 지수 감쇄 탐험율($\epsilon$-decay) 튜닝.
- 듀얼 모터 아두이노 실기체 Sim-to-Real 하드웨어 이식 성공.

### 6. 🔒 웹 인프라 & 공급망 보안 (총 5편)
정적 사이트, CI/CD 파이프라인 및 패키지 공급망 실전 방어 가이드:
- `package.json`의 `overrides`와 `--omit=dev`를 활용한 핀포인트 전이 의존성 취약점 해결.
- Docusaurus MDX 파서 보안 하드닝 및 Cloudflare WAF 연동.

---

## 🎓 학술 심층 분석 & 최신 연구 스터디

자체 개발 프로젝트와 병행하여, 프론티어 AI 커리큘럼을 실무 엔지니어의 시각에서 재해석하고 강의에서 다루지 않는 **실전 프로덕션 함정(Gotchas)**을 주입한 연구 시리즈를 연재합니다:
- **스탠포드 CS329A (자가 진화 AI 에이전트, 총 17편)**: 추론 연산 스케일링, 프로세스 보상 모델(PRM), MCTS 계획 탐색, GRPO 강화학습, 개방형 코드 진화(AlphaEvolve), VLA 피지컬 인텔리전스.
- **스탠포드 CS146S (현대 소프트웨어 개발자, 총 10편)**: 스펙 주도 개발(SDD), 루프 엔지니어링, 모델 컨텍스트 프로토콜(MCP), 무한 루프 토큰 서킷 브레이커, Stdio 64KB 파이프 데드락 방어.

---

## 🛠️ 연구 랩 및 기술 스택

- **메인 랩 워크스테이션**: NVIDIA GeForce RTX 4060 Laptop GPU (8GB VRAM), AMD Ryzen 7, 32GB RAM, Ubuntu Linux / Windows 11.
- **로보틱스 & 마이크로컨트롤러**: ESP32, Arduino Uno, Webots Robot Simulator.
- **ML / AI 프레임워크**: PyTorch 2.4, Hugging Face Transformers, LightGBM, OpenCV, Albumentations, ONNX Runtime.
- **백엔드 & 시스템 언어**: Python 3.12, TypeScript 5.x, C++, FastAPI, PostgreSQL, Redis, Node.js 20+.
- **프론트엔드 & 문서 엔진**: React 19, Docusaurus 3.10, Tailwind CSS, Prism.

---

## 🌐 오픈소스 & 소통

- **저자**: 박지환 (Jihwan Park)
- **GitHub 프로필**: [github.com/jbjihwan](https://github.com/jbjihwan)
- **블로그 소스 저장소**: [github.com/jbjihwan/global_blog](https://github.com/jbjihwan/global_blog)
- **문의 이메일**: [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)
- **문의 페이지**: [문의하기](/contact)
