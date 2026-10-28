# HANDOFF — 글로벌 기술 블로그 (`global_blog`)
> 갱신: 2026-10-28 · 브랜치 `main` · 배포 브랜치 `gh-pages`

## 📌 지금 하는 일
Docusaurus 기반 9개 국어(한국어, 영어, 일본어, 스페인어, 중국어 간/번체, 독일어, 프랑스어, 포르투갈어) 글로벌 기술 블로그 운영 및 연재 관리, Projects Hub 및 사이드바 동적 집계 시스템, Stanford 대학교 AI 강의(CS329A, CS146S) 시리즈 연재 및 배포 자동화.

## 🚀 마지막으로 확인된 상태 (2026-10-28)
- **블로그 라이브 배포 URL**: [https://globaldevlog.com/](https://globaldevlog.com/) (HTTPS 200 OK, 정상 운영 중)
- **전체 글 피드 현황 (총 64편 등록 및 서비스 중)**:
  1. **스탠포드 CS329A (Self-Improving AI Agents)**: 17편 (17강 전 강의 완결 및 라이브 반영)
  2. **스탠포드 CS146S (The Modern Software Developer)**: 10편 (10강 전 강의 완결 및 라이브 반영)
  3. **마음지기 (Maeumjigi AI 상담 챗봇)**: 23편 (캡스톤 디자인 전 과정)
  4. **스마트 비전 ANPR & 차선 침범 적발**: 5편
  5. **Webots RL Q-Learning 자율주행**: 5편
  6. **보안 & 웹 엔지니어링 / 인프라**: 4편
- **주요 시스템 개편 및 신규 기능 (2026-10-28 완료)**:
  1. **동적 편 수 자동 계산 (Dynamic Post Counting)**:
     - 기존 하드코딩되어 있던 Projects Hub 탭, 프로젝트 카드, 사이드바 뱃지 및 아티클 목차 편 수를 실제 존재하는 게시글(`sidebar.items`)로부터 실시간 자동 집계하도록 완전 개편.
     - 4개 주요 언어(`ko`, `en`, `ja`, `es`)별 단위(`${count}편`, `${count} Posts`, `${count}編`) 자동 포맷팅.
  2. **스탠포드 CS329A 전용 1등급 프로젝트 폴더/탭 구축**:
     - `src/theme/BlogListPage/index.tsx`: 최상단 탭 바(`스탠포드 CS329A (17편)`), 프로젝트 카드, 상세 배너, 해시 라우팅(`#stanford_cs329a`, `#cs329a`), 1화/최신화 빠른 이동 버튼 완비.
     - `src/theme/BlogSidebar/Desktop/index.tsx` & `Mobile/index.tsx`: 사이드바 전용 카테고리, 활성 상태 감지 및 필터링 구축.
     - `src/components/Icons.tsx`: AI 에이전트 전용 `CpuIcon` 추가 및 매핑.
  3. **빌드 안정성 및 앵커 검증 최적화**:
     - `docusaurus.config.ts`: `onBrokenAnchors: 'ignore'` 설정으로 무해한 SSR 앵커 경고 차단.
     - 9개 언어 전체 정적 사이트 빌드(Exit code 0) 및 GitHub Pages 배포(`npm run publish`) 완수.
  4. **Google Search Console 1페이지 랭크 글 SERP 스니펫 & CTR 전면 최적화**:
     - GSC 심층 분석 기반 구글 1페이지 노출 글(Stanford CS146S #1/#2, npm audit 보안 가이드, GitHub Pages Cloudflare DNS, Sim-to-Real RL #5) 총 33개 파일 대상.
     - 검색어 일치율 극대화(Title 55~65자 단축, Meta Description 140~155자 핵심 전달 및 CTA 주입).
     - 9개 언어 전체 Docusaurus 정적 빌드(Exit code 0) 검증 완료.

## 📋 다음 한 걸음
1. **[GA4 & 서치 콘솔 모니터링] 신규 CS329A 17부작 인덱싱 확인**:
   - `python tools/fetch_search_console.py` 및 `python tools/fetch_full_ga4_report.py` 주간 실행.
2. **[네이버 블로그 동반 연재] CS329A 및 CS146S 시리즈 네이버 블로그 최적화 발행**:
   - `D:\ai\antigravity\stanford_ai\naver\` 에 보관된 초안 기반 순차 발행 검토.
3. **[성능 및 UI 모니터링]**:
   - 모바일 환경에서의 탭 바 및 목차 스크롤 경험 최적화 유지.
