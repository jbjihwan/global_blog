# 글로벌 기술 블로그 포스트 작성 가이드 (WRITING_GUIDE)

글로벌 기술 블로그(`global_blog`)에 새 포스트나 시리즈를 작성할 때 반드시 준수해야 하는 표준 워크플로우입니다.

---

## 1. 🎯 상위 SEO 키워드 5개 필수 조사 및 주입 (조회수 & 애드센스 극대화)

포스트를 작성하기 전, 반드시 해당 기술 주제의 **구글 글로벌 검색량 및 유입을 견인하는 상위 5대 핵심 키워드**를 선정하여 주입합니다.

1. **키워드 선정 기준 (개발자 검색 패턴)**:
   - **오류 해결형 (Troubleshooting)**: 에러 코드, 라이브러리 충돌, 빌드 실패 현상
   - **기술 비교형 (Comparison / Benchmark)**: 라이브러리 간 성능 비교, 트레이드오프 (광고 단가 최고)
   - **구현 방법형 (How-to / Architecture)**: 구체적 알고리즘, 파이프라인 설계
2. **필수 배치 위치**:
   - **FrontMatter `keywords: [...]`**: 5대 핵심 키워드 명시 (Docusaurus가 `<meta name="keywords">` 및 Schema.org JSON-LD로 자동 변환)
   - **제목(Title)**: 영문/한글 제목에 1~2개 핵심 키워드 자연스럽게 포함
   - **소제목(H2, H3)**: 각 섹션 소제목에 기술 스택 및 문제 해결 키워드 배치
   - **첫 문단**: 시작 2~3줄 내에 주제어와 해결하는 문제를 명시

---

## 2. 🛡️ MDX 및 Docusaurus 문법 안전성 규칙

- **수식 및 중괄호(`{}`) 보호**:
  - Docusaurus MDX 파서는 본문이나 인라인 텍스트에 `{...}` 또는 `\text{...}`가 노출되면 이를 JavaScript JSX 표현식으로 오인하여 빌드 에러(`ReferenceError: ... is not defined`)를 일으킵니다.
  - 수식이나 중괄호가 포함된 문법은 반드시 `(P >= Severe)`처럼 일반 기호로 표기하거나, 코드 블록(```text)으로 감싸야 합니다.
- **이미지 상대 경로**:
  - `![설명](./images/파일명.png)` 형식으로 배치하고 모든 로케일 폴더에 실제 이미지를 복사/동기화합니다.

---

## 3. 🌐 4개 국어(en, ko, ja, es) 다국어 동기화

- 기본 언어(`en`): `blog/<날짜>-<주제>/index.md`
- 한국어(`ko`): `i18n/ko/docusaurus-plugin-content-blog/<날짜>-<주제>/index.md`
- 일본어(`ja`): `i18n/ja/docusaurus-plugin-content-blog/<날짜>-<주제>/index.md`
- 스페인어(`es`): `i18n/es/docusaurus-plugin-content-blog/<날짜>-<주제>/index.md`
- 각 로케일별로 자연스러운 현지 기술 용어(한국어, 영어, 일본어, 스페인어)를 반영합니다.

---

## 4. ⏰ 골든 타임 배포 주기

- **최적 배포 요일**: 화요일, 수요일, 목요일
- **최적 배포 시간**: **한국 시간(KST) 밤 10시 ~ 11시**
  - 미국 서부(PST, San Jose) 오전 6~7시 / 미국 동부(EST, Ashburn) 오전 9~10시 출근 피크 동시 공략
  - 대한민국 다음 날 아침 출근길 개발자 피드 연결

---

## 5. 🚀 배포 원칙

- 글 작성 중 중간 Git 커밋 명령을 남발하지 않고, 4개 국어 작성이 모두 완료된 후:
- **`npm run build`로 4개 국어 SSG 컴파일 검증 (exit code 0 확인)**
- **`publish.ps1` 단 1회 실행으로 Git Commit + Push + GitHub Pages 배포 완수**
