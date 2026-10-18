# HANDOFF — 글로벌 기술 블로그 (`global_blog`)
> 갱신: 2026-10-18 · 브랜치 `main` · 배포 브랜치 `gh-pages`

## 📌 지금 하는 일
Docusaurus 기반 4개 국어(한국어, 영어, 일본어, 스페인어) 다국어 기술 블로그 운영, 구글 애드센스 승인 요건 구축 및 정기 연재 루틴 확립.

## 🚀 마지막으로 확인된 상태 (2026-10-18)
- **블로그 라이브 배포 URL**: [https://jbjihwan.github.io/global_blog/](https://jbjihwan.github.io/global_blog/)
- **구글 애드센스(AdSense) 승인 인프라 구축**:
  - `About Me` (소개): 4개 국어(`src/pages/about.md`, `i18n/*/about.md`) 엔지니어링 경력, 연구 분야, 오픈소스 철학 명시 (E-E-A-T 충족).
  - `Privacy Policy` (개인정보처리방침): 4개 국어(`privacy-policy.md`) GA4(`G-VM2CVW28SL`), 쿠키 및 AdSense 맞춤 광고 Opt-out 조항 완비 (GDPR/CCPA 준수).
  - `Contact` (문의처): 4개 국어(`contact.md`) 공식 이메일(`jbgihwan@gmail.com`) 및 GitHub Issue 링크 배치.
  - 불필요한 기본 템플릿 문서(`docs/`, `markdown-page.mdx`) `_old\`로 아카이빙 및 `docs: false` 비활성화로 404 에러 원천 차단.
  - 내비게이션 바 및 푸터 전면 개편 (다국어 공통 안전 경로로 정비).
- **연재 완료 시리즈 및 스페셜 아티클**:
  1. **마음지기 캡스톤 개발일지 (총 23편)**
  2. **Webots Q-Learning 로봇 자율주행 강화학습 (총 5편)**
  3. **Blackbox ANPR & Lane Intrusion 비전 AI 시스템 (총 5편)**
  4. **[스페셜 테크 아티클] 정적 사이트 보안 하드닝 & npm audit의 진실 (1편)**:
     - *From 45 npm Vulnerabilities to Zero-Risk: Why You Shouldn't Blindly Run npm audit fix --force on Static Sites*
     - 4개 국어(en, ko, ja, es) 완간, 위협 모델/파이프라인 다이어그램 2종 수록, 상위 5대 SEO 키워드 주입.
- **100% 실제 연구/발표자료 이미지 교체 완료 (34편 전편)**:
  - 기존 AI 생성 이미지들을 사용자의 실제 **PPT 발표자료 슬라이드(`1학기_최종발표_마음이.pptx` 등)**, **Matplotlib 손실/레이더/지표 그래프**, **GPU VRAM 프로파일링 차트**, **실제 웹/앱 UI 캡처(2500x1400 고해상도)**로 전면 교체 완료 (23편 마음지기 + 5편 Q-Learning + 5편 ANPR + 1편 보안 아티클).
  - 4개 국어(en, ko, ja, es) 136개 포스트의 이미지 디렉토리 전수 동기화 완료.
- **빌드 상태**: 4개 국어(en, es, ja, ko) SSG 전체 빌드 PASS (`exit code 0`).

## 📋 다음 한 걸음
1. **[골든 타임 루틴] 화/목 밤 10~11시 정기 연재 루틴**:
   - 마음지기 2학기 AI 고도화(순서형 회귀, Guardrail 파이프라인) 신규 시리즈 1편 발행.
2. **[할 일 보관] 네이버 블로그 전용 원고 변환 (총 10편)**:
   - Webots Q-Learning (5편) 및 Blackbox ANPR 비전 (5편) 스마트에디터 최적화 원고 생성.
3. **구글 서치 콘솔 및 네이버 서치어드바이저 사이트맵 점검**:
   - `sitemap.xml` 및 신규 3개 페이지 색인 요청.

