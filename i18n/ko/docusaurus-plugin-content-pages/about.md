---
title: 소개 (About) & 글로벌 기술 블로그
description: 개발자 박지환(jbjihwan) 및 글로벌 기술 블로그 소개 - AI, 로보틱스, 컴퓨터 비전, 강화학습 엔지니어링 실전 기록.
keywords: [블로그 소개, 개발자 소개, 박지환, 인공지능 엔지니어, 로보틱스, 컴퓨터 비전, 강화학습, 마음지기]
---

# 소개 (About) & 글로벌 기술 블로그

**글로벌 기술 블로그(Global Dev Blog)**에 오신 것을 환영합니다. 본 블로그는 AI 및 로보틱스 소프트웨어 엔지니어 **박지환(jbjihwan)**이 직접 겪은 기술 연구, 실전 구현, 트러블슈팅 및 성능 벤치마크를 기록하는 엔지니어링 연구 일지입니다.

단순한 이론 요약을 넘어, 실제 코드 배포 과정에서 마주치는 하드웨어 한계, 데이터 불균형, 실시간성 제약, 실패와 돌파 과정을 있는 그대로 공유합니다.

---

## 👨‍💻 엔지니어 소개

- **자율주행 & 강화학습 (Reinforcement Learning)**: MDP 정의, 648개 연속 상태 공간 이산화, 조밀한 보상 형성(Reward Shaping), Webots 시뮬레이션 기반 학습 및 아두이노(Arduino) 실기체 Sim-to-Real 하드웨어 전이.
- **딥 컴퓨터 비전 (Computer Vision)**: 초당 30 FPS 실시간 파이프라인, 객체 탐지(YOLOv3/v5/v8), 고속 CSRT 광학 추적, 딥러닝 기반 초해상도(EDSR, FSRCNN) 복원, 다수결 투표 기반 고정밀 한국형 차량 번호판 인식(ANPR) 엔진.
- **자연어 처리 & AI 안전성 (Safety AI)**: Llama 아키텍처 기반 LoRA 경량 파인튜닝, Weak Labeling 과신(p=0.9998) 보정, 순서형 회귀(Ordinal Regression), 누적 확률 판정(P >= Severe), 서브 밀리초 결정론적 Guardrail(Safety Wrapper) 아키텍처.
- **풀스택 ML 엔지니어링**: 고처리량 FastAPI 마이크로서비스, PostgreSQL / Redis 인프라 구축, Docusaurus 4개 국어 기술 문서 허브, React Native 모바일 크로스 플랫폼 연동.

---

## 📚 대표 연재 시리즈

### 1. 🧠 마음지기 캡스톤 개발일지 (총 23편)
- 대규모 LLM 파이프라인을 활용한 위기 상담 합성 데이터 생성.
- 파인튜닝 모델의 극단적 확률 과신 보정 및 순서형 분류기 설계.
- 위기 상황에서 즉각 개입하는 결정론적 Safety Wrapper 가드레일 구현.
- 데이터베이스 커넥션 풀링 트러블슈팅 및 1학기 최종 발표 시연.

### 2. 🤖 Webots Q-Learning 자율주행 강화학습 (총 5편)
- 6개 방향 거리 센서를 648개 이산 상태 공간으로 압축하는 상태 공간 설계.
- 희소 보상(Sparse Reward) 기아 상태를 극복하는 진행 속도 및 거리 델타 기반 조밀 보상 형성.
- 12개 장애물 로컬 미니마(함정) 탈출을 위한 지수 감쇄 탐험율($\epsilon$-decay) 튜닝.
- 학습 완료된 Q-table을 듀얼 모터 아두이노 실기체에 이식하는 Sim-to-Real 성공.

### 3. 🚗 Blackbox ANPR & 차선 침범 비전 AI 시스템 (총 5편)
- 고속도로 블랙박스 저화질/역광 환경을 극복하는 6단계 엔드투엔드 파이프라인 (30 FPS 보장).
- 차선 다항식 피팅 및 기하학적 바운딩 박스 IoU 침범 판정 알고리즘.
- YOLOv3 차량 ROI 검출 ➡️ YOLOv5 번호판 탐지 ➡️ CSRT 추적의 계층적 아키텍처.
- EDSR 초해상도(Super-Resolution) 및 다중 프레임 스태킹을 통한 번호판 디블러링.
- 정규식 정규화와 시간적 11단계 다수결 투표를 결합한 한국형 번호판 완성형 OCR 엔진.

---

## 🛠️ 연구 환경 및 기술 스택

- **딥러닝 프레임워크**: PyTorch, Hugging Face Transformers, Torchvision, ONNX Runtime.
- **컴퓨터 비전**: OpenCV, Albumentations, EasyOCR, Tesseract, EDSR / FSRCNN.
- **로보틱스 & 시뮬레이터**: Webots Robot Simulator, Arduino IDE, ROS 기초.
- **언어 & 백엔드**: Python 3.12, TypeScript, C++, FastAPI, PostgreSQL, Redis.
- **하드웨어 랩**: NVIDIA GeForce RTX 4060 Laptop GPU (8GB VRAM), ESP32 / Arduino Uno, 고화질 엣지 카메라.

---

## 🌐 오픈소스 & 소통

본 블로그의 모든 기술 연재는 실제 작동하는 코드와 재현 가능한 환경을 전제로 합니다. 질문이나 피드백, 협업 제안은 언제든 환영합니다.

- **GitHub 프로필**: [github.com/jbjihwan](https://github.com/jbjihwan)
- **블로그 소스 저장소**: [github.com/jbjihwan/global_blog](https://github.com/jbjihwan/global_blog)
- **문의하기**: [문의 페이지](/global_blog/ko/contact) 또는 [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)
