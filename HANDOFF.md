# HANDOFF — 글로벌 기술 블로그 (`global_blog`)
> 갱신: 2026-10-16 · 브랜치 `main` · 배포 브랜치 `gh-pages`

## 📌 지금 하는 일
Docusaurus 기반 4개 국어(한국어, 영어, 일본어, 스페인어) 다국어 기술 블로그 운영 및 프로젝트별 개발 일지 연재.

## 🚀 마지막으로 확인된 상태 (2026-10-16)
- **블로그 라이브 배포 URL**: [https://jbjihwan.github.io/global_blog/](https://jbjihwan.github.io/global_blog/)
- **연재 완료 시리즈**:
  1. **마음지기 캡스톤 개발일지 (총 23편)**
     - 2026-03-26 ~ 2026-06-18
     - en, es, ja, ko 4개 국어 번역 및 대표/본문 이미지 매핑 완료.
  2. **Webots Q-Learning 로봇 자율주행 강화학습 (총 5편)**
     - 2026-05-17 ~ 2026-05-21
     - 648개 상태 공간 이산화, 조밀한 보상 형성, 12개 장애물 로컬 미니마 극복, 무탐색 결정론적 평가, Arduino Sim-to-Real 전이.
     - 4개 국어 전편 수록 완료.
  3. **Blackbox ANPR & Lane Intrusion 비전 AI 시스템 (총 5편)**
     - 2026-06-25 ~ 2026-06-29 (`D:\CV` 프로젝트 기반)
     - `#1`: 6-Stage End-to-End Pipeline & Real-Time Constraints
     - `#2`: Dynamic Lane Boundary Extraction & Geometric IoU Intrusion Criterion
     - `#3`: Hierarchical Object Detection: YOLOv3 Vehicle ROI, YOLOv5 Plate Detector & CSRT Tracking
     - `#4`: Overcoming Blurry Blackbox Artifacts: Deep Super-Resolution (EDSR) & Multi-Frame Image Stacking
     - `#5`: Korean ANPR OCR Engine, Regex Normalization & Temporal Majority Voting (v01 to v11 Evolution)
     - 4개 국어(en, ko, ja, es) 및 실제 시뮬레이션/주행 결과 이미지 일괄 수록 완료.
- **UI & 테마 커스텀**:
  - `src/theme/BlogListPage`: 프로젝트 선택 허브(마음지기, Q-Learning, ANPR Vision, 전체 피드 탭) 및 4개 국어 배너/뱃지 UI 적용.
  - `src/pages/index.tsx`: `/global_blog/blog` 자동 리다이렉트 처리.
  - `tools/publish.ps1`: 원스톱 자동 배포(Git Stage -> Commit -> Push -> GitHub Pages Deploy) 스크립트 구축.

## 📋 다음 한 걸음
1. **2학기 프로젝트 연재 기획**:
   - 캡스톤 디자인 2학기: 위기감지 NLP 모델 고도화(순서형 회귀, MIL, Guardrail 파이프라인 등) 시리즈 기획.
   - SDC 동적 임무계획 변경 연구 관련 기술 아티클 연재 검토.
2. **블로그 추가 기능 고도화**:
   - Giscus 댓글 설정 완료 및 확인.
   - 소셜 공유 메타태그(OpenGraph) 점검.
