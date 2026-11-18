# HANDOFF — 글로벌 기술 블로그 (`global_blog`)
> 갱신: 2026-11-18 · 브랜치 `main` · 배포 브랜치 `gh-pages`

## 📌 지금 상태 (2026-11-18 전면 개편 완료)
Google AdSense 「가치가 별로 없는 콘텐츠」 거절 및 Google Search Console `Crawled - currently not indexed` 문제를 근본적으로 해결하기 위해, 사용자 지시(1·2·3 순차 진행)에 따라 다음 3단계를 완수했다.

1. **[Step 1] 83편 전수 감사 및 정예 20편(기존 19편 + 신규 1편) 체제로 선별 (`CURATION_PLAN_83_POSTS.md`)**:
   - **64편 `_old/` 분리 보관**: 대학 공개 강의 요약 27편(`stanford-cs329a` 17, `stanford-cs146s` 10), 단문 캡스톤 일기 20편(`maeumjigi`), `[Simulation]` 재구성 로그 경고문이 붙은 예산 감사 9편(`national-budget`), 자살·정신건강 YMYL 고위험 주제 5편(`mental-crisis` 4 + `maeumjigi-23`), 애드센스 승인 메타 가이드 3편을 `_old/blog` 및 `_old/i18n_ko_blog`로 안전하게 분리했다.
   - **미사용 7개 다국어 폴더(`de`, `es`, `fr`, `ja`, `pt-BR`, `zh-Hans`, `zh-Hant`)**도 `_old/i18n_other/`로 이동하여 `en`·`ko` 2개 핵심 언어만 남겼다.
2. **[Step 2] 기술적 결함·미래 날짜·중복 스크립트·단문 본문 전면 수정**:
   - **`docusaurus.config.ts` 중복 애드센스 스크립트 제거**: `headTags`에서 전역 `adsbygoogle.js`를 제거하여 `src/theme/Root.tsx` 단일 로드로 통합(기존 페이지당 2회 중복 로드 해소).
   - **미래 날짜(`2026-11-28` ~ `2026-12-05`) 4편 교정**: `npm-overrides`(`2026-11-05`), `sdc-01`(`2026-11-10`), `sdc-02`(`2026-11-12`), `sdc-03`(`2026-11-14`)을 실제 과거 날짜로 교정(슬러그 URL은 그대로 유지).
   - **`/ko/` 홈(`src/pages/index.tsx`) 한국어 완전 지원 및 `/ko/terms` 추가**: Search Console에서 `/ko/`가 영문 홈과 동일해 `Duplicate` 판정을 받던 문제를 해결.
   - **사이드바·허브(`BlogSidebar`, `BlogListPage`) 동적 필터링 및 민감어 제거**: `count > 0`인 5개 실전 트랙만 표시하고 번들 내 `Suicide` / `자살` 문구를 전면 제거.
   - **ANPR #2·#3·#4·#5 실제 런타임 디버깅 로그 보강 및 `Claude Code`·로컬 경로 정화**.
3. **[Step 3] AI 요약 템플릿을 버린 순수 디버깅 포스트 1편 신규 작성**:
   - `2026-11-16-python-urlopen-timeout-dns-hang-windows-fix` (영문·한국어): Windows 환경에서 `urllib.request.urlopen` 및 `requests`의 `timeout`이 `socket.getaddrinfo` DNS 조회에서 무한 대기하는 원인과 실패했던 3가지 시도(`setdefaulttimeout`, `SIGALRM`, `with ThreadPoolExecutor`), `executor.shutdown(wait=False, cancel_futures=True)` 및 `UTF-16` 널 바이트(`\x00`) 정규식 실패 해결기.

## 🚀 현재 활성 트랙 및 게시글 (총 20편, 영문 20 + 한국어 20)
1. **항공작전 동적 임무계획 (`sdc_replanning`, 3편)**: `sdc-01`, `sdc-02`, `sdc-03`
2. **보안 · 파이썬 & 웹 인프라 디버깅 (`security`, 4편)**: `python-urlopen-timeout-dns-hang-windows-fix`, `npm-overrides-transitive-vulnerability-fix`, `github-pages-custom-domain-cloudflare-dns`, `static-site-security-npm-audit-truth`
3. **블랙박스 차선침범 & 초해상화 번호판 인식 (`anpr_vision`, 5편)**: `vision-anpr-1` ~ `5`
4. **Webots Q-Learning 자율주행 로봇 (`rl_q_learning`, 5편)**: `rl-qlearning-1` ~ `5`
5. **LLM 파인튜닝 & 백엔드 트러블슈팅 (`maeumjigi`, 3편)**: `maeumjigi-4`, `maeumjigi-10`, `maeumjigi-19`
