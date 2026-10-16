# HANDOFF — 글로벌 기술 블로그 (`global_blog`)
> 갱신: 2026-10-16 · 브랜치 `main` (`43d5458`) · 배포 브랜치 `gh-pages`

## 📌 지금 하는 일
Docusaurus 기반 4개 국어(한국어, 영어, 일본어, 스페인어) 다국어 기술 블로그 운영 및 프로젝트별 개발 일지 연재.

## 🚀 마지막으로 확인된 상태 (2026-10-16)
- **블로그 라이브 배포 완료**: [https://jbjihwan.github.io/global_blog/](https://jbjihwan.github.io/global_blog/)
- **Git 상태**: `main` 브랜치에 `43d5458` 커밋 및 `origin main` 푸시 완료, `gh-pages` 배포 완료.
- **연재 완료 시리즈**:
  1. **마음지기 캡스톤 개발일지 (총 23편)**
     - 2026-03-26 ~ 2026-06-18
     - en, es, ja, ko 4개 국어 번역 및 대표/본문 이미지 매핑 완료.
  2. **Webots Q-Learning 로봇 자율주행 강화학습 (총 5편)**
     - `#1`: 648-Bin State Discretization & Socket Architecture
     - `#2`: Tabular Q-Learning Implementation & Reward Shaping Tuning
     - `#3`: Conquering Local Minima in 12-Wall Obstacles (Headless Simulation)
     - `#4`: Deterministic Evaluation & Benchmark vs DQN/SARSA
     - `#5`: Sim-to-Real: Hardware Transfer via Arduino, HC-06 & ArUco Vision
     - 4개 국어 전편 수록 완료.
- **UI & 테마 커스텀**:
  - `src/theme/BlogListPage`: 프로젝트 선택 허브(마음지기, Q-Learning, 전체 피드 탭) 및 4개 국어 배너/뱃지 UI 적용.
  - `src/pages/index.tsx`: `/global_blog/blog` 자동 리다이렉트 처리.
  - `static/robots.txt`: 검색엔진 크롤링 최적화 설정.

## 📋 다음 한 걸음
1. **2학기 프로젝트 연재 기획**:
   - 캡스톤 디자인 2학기: 위기감지 NLP 모델 고도화(순서형 회귀, MIL, Guardrail 파이프라인 등) 시리즈 기획.
   - SDC 동적 임무계획 변경 연구 관련 기술 아티클 연재 검토.
2. **SEO 및 블로그 추가 기능 고도화**:
   - Giscus 댓글 설정 완료 및 확인.
   - 태그별/카테고리별 검색 및 소셜 프리뷰 카드 메타태그 보완.
