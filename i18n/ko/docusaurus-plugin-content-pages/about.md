---
title: 블로그 및 엔지니어 소개
description: 박지환(Jihwan Park)의 Global Dev Blog 소개 — AI 시스템, 로보틱스, 컴퓨터 비전, 파이썬 및 웹 보안 실전 오류 해결 기록.
keywords: [블로그 소개, 박지환, AI 엔지니어, 로보틱스, 컴퓨터 비전, 강화학습, 파이썬 디버깅, 편집 원칙]
---

# 블로그 및 엔지니어 소개 (About Global Dev Blog)

**Global Dev Blog**는 소프트웨어·AI 엔지니어 **박지환(`jbjihwan`)**이 실제 프로젝트를 개발하고 운영하며 겪은 **런타임 에러 로그, 성능 병목 원인, 실패했던 우회 시도와 검증된 해결 코드**를 기록하는 기술 블로그입니다.

---

## 👨‍💻 다루는 5대 핵심 엔지니어링 영역

1. **항공작전 동적 임무계획 아키텍처 (SDC)**: 전술 데이터링크(Link 16) MTU 제약 하의 RFC 8785 결정론적 JCS 정규화, Ed25519 다중 서명 검증, CPython 3D A* 탐색 병목(`31.4초 → 0.259초`) 해결 및 RK4 수치적분 연료 검증.
2. **실시간 컴퓨터 비전 & 고속도로 번호판 인식 (ANPR)**: 30 FPS 실시간 블랙박스 영상에서 동적 차선 검출(허프 변환·Shapely IoU), 계층적 YOLOv3/v5 번호판 검출, CSRT 추적기, EDSR_x4 초해상화 및 시간 축 다수결 보팅 OCR 구현.
3. **자율주행 로보틱스 & 강화학습 (Webots Q-Learning)**: 648개 이산 상태 공간 설계, 12개 벽 장애물 국소 최적해(Local Minima) 탈출 보상 설계, Webots 시뮬레이터에서 아두이노 실제 하드웨어로의 Sim-to-Real 이식.
4. **LLM 파인튜닝 & 풀스택 백엔드 디버깅**: Llama 3.1 `<|eot_id|>` 누락으로 인한 무한 생성 버그 해결, HTTP 429 쿼터 제한 복구용 SQLite 체크포인트 상태머신, FastAPI + PostgreSQL `$2a$`/`$2b$` Bcrypt 401 인증 오류 해결.
5. **파이썬 시스템 디버깅 & 웹 공급망 보안**: Windows `socket.getaddrinfo` DNS 무한 대기 현상과 `ThreadPoolExecutor(wait=False)` 격리, UTF-16 널 바이트(`\x00`) 디코딩 오류, `npm overrides` 전이 취약점 해결 및 Cloudflare DNS 운영.

---

## 🛡️ 작성 및 검증 원칙

1. **직접 실행·검증한 코드만 게시**: 모든 에러 트레이스백과 수정 코드는 실제 개발 장비(NVIDIA GeForce RTX 4060 GPU, AMD Ryzen 7, 32GB RAM, Windows 11 / WSL2 Ubuntu, Python 3.12, Node.js 20+)에서 직접 재현하고 통과한 결과만 기록합니다.
2. **실패한 가설과 근본 원인 명시**: 단순히 최종 정답 코드만 적지 않고, 처음 시도했다가 실패한 이유와 운영체제·라이브러리 내부 동작 원리를 함께 설명합니다.
3. **오픈소스 공개**: 관련 코드와 이슈는 GitHub([github.com/jbjihwan](https://github.com/jbjihwan))를 통해 투명하게 관리합니다.

---

## 📬 연락처 (Contact)

- **작성자**: 박지환 (Jihwan Park)
- **이메일**: [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com)
- **GitHub**: [https://github.com/jbjihwan](https://github.com/jbjihwan)
