# [운영 가이드] GA4 내부 트래픽 필터 및 애드센스 민감 페이지 제외 설정
**Internal Traffic Filtering & AdSense Sensitive Page Exclusion Guide**

> **작성 일자**: 2026-10-30  
> **대상 도메인**: `https://globaldevlog.com`  
> **목적**: 개발자/운영자 자체 트래픽(460 PV 등) 분리를 통한 순수 외부 유입 측정 & 위기 감지 AI 페이지의 애드센스 광고 노출 제외(독자 신뢰 및 YMYL 규정 준수)

---

## 1. GA4 내부 IP 필터 설정 (본인 트래픽 분리)

한국 독자 10명 / 460 PV는 블로그 작성, 수정, 빌드, 배포 과정에서 운영팀이 브라우저로 사이트를 반복 열람하며 발생한 트래픽입니다. 이를 순수 외부 독자 지표에서 배제하기 위해 다음 설정을 적용합니다.

### 설정 단계:
1. **Google Analytics (GA4)** 콘솔 접속 (`https://analytics.google.com/`)
2. 좌측 하단 **[관리(Admin)] ➔ [데이터 스트림(Data Streams)]** 클릭
3. `Global Dev Blog` 웹 스트림 선택
4. 하단 **[태그 설정 구성(Configure tag settings)]** 클릭
5. **[모두 표시(Show all)] ➔ [내부 트래픽 정의(Define internal traffic)]** 클릭
6. **[만들기(Create)]** 버튼 클릭:
   - **규칙 이름**: `Office & Dev Environment`
   - **traffic_type 값**: `internal` (기본값)
   - **IP 주소 일치 유형**: `IP 주소가 다음과 같음(IP address equals)`
   - **값**: 본인의 공인 IP 입력 (네이버/구글에서 '내 IP 확인' 검색 시 나오는 IPv4 주소)
7. 좌측 메뉴 **[관리] ➔ [데이터 필터(Data Filters)]** 이동:
   - `Internal Traffic` 필터 클릭
   - **필터 상태**: `테스트(Testing)` ➔ **`활성(Active)`**으로 변경 후 저장.

> 💡 **효과**: 개발 및 검수 시 발생하는 수백 회의 페이지뷰가 GA4 실시간 리포트 및 기본 보고서에서 자동 제외되어 순수 외부 독자(미국, 대만, 순수 국내 유입) 지표만 정밀하게 집계됩니다.

---

## 2. 애드센스 위기 감지 AI(YMYL) 페이지 광고 제외 설정

자살/위기 감지 AI 관련 글은 정신건강 위기 관련 검색어로 유입될 수 있으므로, 해당 페이지에 상업적 광고가 노출되면 독자 신뢰가 훼손될 수 있습니다.

### 설정 단계:
1. **Google AdSense** 콘솔 접속 (`https://www.google.com/adsense/`)
2. 좌측 메뉴 **[광고(Ads)] ➔ [사이트 기준(By site)]** 클릭
3. 등록된 사이트 목록에서 **`globaldevlog.com`**의 우측 연필 아이콘(수정) 클릭
4. 우측 설정 패널에서 **[페이지 제외(Page exclusions)]** 클릭
5. **[제외 추가(Add exclusion)]** 클릭:
   - 제외할 URL 경로(접두사):  
     - `globaldevlog.com/blog/mental-crisis`
     - `globaldevlog.com/ko/blog/mental-crisis`
     - `globaldevlog.com/*/blog/mental-crisis`
   - **페이지 제외 유형**: `이 섹션의 모든 페이지(All pages in this section)`
6. **[저장 및 사이트에 적용(Apply to site)]** 완료.

> 💡 **효과**: 위기 감지 R&D 아티클에서는 자동 광고가 완전히 비활성화되어 순수 학술/엔지니어링 백서의 신뢰성을 유지하고, 기술 및 튜토리얼 포스트에만 고단가 광고가 집중 노출됩니다.
