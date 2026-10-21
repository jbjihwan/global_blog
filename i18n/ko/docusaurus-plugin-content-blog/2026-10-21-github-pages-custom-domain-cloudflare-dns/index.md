---
slug: github-pages-custom-domain-cloudflare-dns
title: "[GitHub Pages 독립 도메인 #1] 무료 github.io 버리고 Porkbun + Cloudflare로 내 도메인 연결하기: CNAME 평탄화와 무료 SSL"
authors: [jbjihwan]
tags: [github-pages, custom-domain, porkbun, cloudflare, docusaurus, devops]
keywords: [Docusaurus GitHub Pages Custom Domain, Cloudflare DNS Porkbun CNAME setup, CNAME Flattening apex domain GitHub Pages, Cloudflare Full SSL Edge Certificate, static CNAME deployment reset bug fix]
description: "무료 github.io 서브도메인을 탈출하여 Porkbun에서 구매한 독립 도메인을 Cloudflare Anycast DNS와 CNAME 평탄화(Flattening)를 통해 GitHub Pages에 무중단 연결하고, Docusaurus CNAME 리셋 버그를 완벽히 해결하는 프로덕션 실전 가이드."
---

개발자라면 누구나 한 번쯤 GitHub Pages의 무료 서브도메인(`username.github.io/project`)을 이용해 블로그를 운영해 보았을 것입니다. Git 푸시 한 번으로 전 세계에 정적 사이트가 배포되고 서버 유지비가 들지 않는다는 점은 초기 개발자 블로그에 최고의 장점입니다.

하지만 전문적인 기술 브랜딩과 **구글 애드센스(Google AdSense) 수익화**를 준비하는 순간 타협할 수 없는 기술적 한계에 부딪힙니다. **구글 애드센스는 `*.github.io`와 같은 무료 2차 서브도메인의 사이트 등록 및 심사 신청을 정책적으로 원천 차단**하기 때문입니다. 또한 포털 검색엔진에서 쌓이는 도메인 지수(Domain Authority)가 깃허브가 아닌 온전한 '내 자산'으로 누적되게 하려면 반드시 **독립 커스텀 도메인(Apex Domain, 예: `globaldevlog.com`)**이 필수적입니다.

정적 사이트(SSG) 엔지니어링 시리즈의 첫 번째 편인 이번 글에서는, 기존 `jbjihwan.github.io/global_blog`에서 독립 도메인 `https://globaldevlog.com`으로의 무중단 마이그레이션을 완수한 **Porkbun + Cloudflare + GitHub Pages 3계층 고가용성 아키텍처와 DNS 설정 실무**를 완벽하게 정리합니다.

{/* truncate */}

---

![정적 엔지니어링 블로그를 위한 프로덕션 DNS 및 CDN 라우팅 아키텍처](./images/01_dns_routing_architecture.png)

---

## 1. 아키텍처 설계 철학: 3계층 고가용성 구성

GitHub Pages에 개인 도메인을 연결할 때 초보 엔지니어들이 가장 흔히 쓰는 방식은 도메인 등록기관에서 깃허브의 고정 IP(`185.199.108.153` 등 4개)를 향해 직접 `A 레코드`를 지정하는 것입니다.

이 전통적인 방식은 단순하지만 운영상 치명적인 약점들이 있습니다:
- 엣지 디도스(DDoS) 방어 및 악성 봇 차단 계층의 부재.
- DNS 네임서버 변경 시 글로벌 전파 속도 지연.
- 정적 자산(CSS, JS, WebP)에 대한 글로벌 CDN 캐싱 최적화 불가.

우리는 책임과 역할을 전문화된 3개 레이어로 분리했습니다:

| 계층 | 사용 서비스 | 핵심 역할 및 선정 근거 |
| :--- | :--- | :--- |
| **1. 도메인 등록기관** | **Porkbun** | 도메인 최초 구매 및 매년 갱신 비용이 글로벌 최저가 수준, WHOIS 개인정보 보호 평생 무료, 투명한 가격 정책 |
| **2. 엣지 DNS & 보안** | **Cloudflare** | 글로벌 초저지연 Anycast DNS, **루트 도메인 CNAME 평탄화(Flattening)**, 무료 Universal SSL, 자동 HTTPS 강제 리다이렉트 |
| **3. 정적 호스팅 오리진** | **GitHub Pages** | Docusaurus 컴파일 아티팩트 서빙, `gh-pages` 브랜치 자동 배포, 서버 관리 및 호스팅 비용 0원 유지 |

---

## 2. Step 1: Porkbun 도메인 구매 및 Cloudflare 네임서버 위임

1. **도메인 구매**: Porkbun에서 원하는 루트 도메인(`globaldevlog.com`)을 검색하여 구매합니다. (연 1만 원대 초반으로 매우 저렴합니다.)
2. **Cloudflare에 도메인 추가**: Cloudflare 콘솔에서 **[사이트 추가]**를 클릭하고 구매한 도메인을 입력한 뒤 **무료 플랜(Free Plan)**을 선택합니다.
3. **할당된 네임서버 확인**: Cloudflare가 발급해 준 고유 네임서버 주소 2개를 확인합니다:
   ```text
   roan.ns.cloudflare.com
   sneh.ns.cloudflare.com
   ```
4. **Porkbun 네임서버 교체**: Porkbun 대시보드의 `Authoritative Nameservers` 메뉴에서 기존 Porkbun 기본 주소들을 모두 지우고, Cloudflare 네임서버 2개로 변경 저장합니다. (보통 5~15분 내 전파 완료)

---

## 3. Step 2: Cloudflare CNAME Flattening(평탄화) 및 Full SSL 설정

DNS 표준(RFC 1034)에 따르면 루트 도메인(`@`)에는 SOA 및 NS 레코드와의 충돌 방지를 위해 `CNAME` 레코드를 등록할 수 없습니다. 과거에는 이 때문에 어쩔 수 없이 취약한 A 레코드를 썼습니다.

하지만 Cloudflare의 **CNAME 평탄화(Flattening)** 기능을 사용하면 루트 도메인에서도 `CNAME` 레코드의 모든 장점을 온전히 누릴 수 있습니다. DNS 쿼리 시점에 Cloudflare 엣지가 타깃 주소(`username.github.io`)의 IP를 스스로 확인하여 질의자에게 즉시 반환하기 때문입니다.

### A. Cloudflare DNS 레코드 등록
Cloudflare **[DNS] > [레코드]** 메뉴에서 아래 2개의 프록시 레코드를 추가합니다:

| 유형 (Type) | 이름 (Name) | 대상 (Target) | 프록시 상태 (Proxy status) | TTL |
| :--- | :--- | :--- | :--- | :--- |
| **CNAME** | `@` | `jbjihwan.github.io` | **프록시됨 (주황색 구름 켜기)** | 자동 |
| **CNAME** | `www` | `jbjihwan.github.io` | **프록시됨 (주황색 구름 켜기)** | 자동 |

> **주황색 구름(프록시) 활성화 필수**: 프록시를 켜야만 모든 트래픽이 Cloudflare의 글로벌 Anycast 엣지를 통과하며 무료 SSL 암호화, Brotli 압축 전송, 캐싱 혜택을 받게 됩니다.

### B. SSL/TLS 암호화 모드 전환
Cloudflare 좌측 메뉴의 **[SSL/TLS] > [개요]**로 이동합니다:
- 암호화 모드를 **Full (또는 Full Strict)**로 설정합니다.
- 방문자 브라우저와 Cloudflare 간은 물론, Cloudflare와 GitHub Pages 오리진 서버 사이의 통신까지 전 구간 종단간(End-to-End) 암호화가 보장됩니다.

---

## 4. Step 3: Docusaurus 설정 파일 갱신 (`docusaurus.config.ts`)

기존 깃허브 서브경로(`baseUrl: '/global_blog/'`)에서 도메인 최상단 루트(`/`)로의 라우팅 매핑을 위해 `docusaurus.config.ts`를 수정합니다:

```typescript
const config: Config = {
  title: 'Global Dev Blog',
  tagline: 'Engineering Deep Dives in AI, Robotics, Computer Vision',

  // 새로운 커스텀 도메인 주소로 교체
  url: 'https://globaldevlog.com',
  // 서브패스에서 도메인 루트로 수정
  baseUrl: '/',

  organizationName: 'jbjihwan',
  projectName: 'global_blog',
  trailingSlash: false,
  // ...
};
```

---

## 5. Step 4: GitHub Pages 배포 시 도메인 초기화 버그 해결 (`static/CNAME`)

GitHub Pages로 커스텀 도메인을 운영할 때 가장 흔히 겪는 치명적인 버그가 바로 **도메인 연결 리셋 현상**입니다:
1. GitHub 저장소의 `Settings > Pages > Custom domain`에 `globaldevlog.com`을 입력해 둡니다.
2. 로컬에서 글을 작성하고 `npm run deploy` 명령어로 배포합니다.
3. 배포가 끝나면 깃허브의 Custom domain 입력칸이 빈칸으로 초기화되어 사이트가 404 에러를 뿜거나 SSL 인증서 경고가 뜹니다!

### 원인
Docusaurus의 배포 스크립트는 `build/` 폴더를 새로 컴파일한 후 `gh-pages` 브랜치를 강제로 덮어씌웁니다(`git push --force`). 이 과정에서 최상위 루트에 `CNAME` 파일이 없으면 깃허브 서버는 커스텀 도메인 매핑이 취소된 것으로 간주합니다.

### 완벽한 해결책
프로젝트의 `static/` 디렉터리에 `CNAME` 파일(확장자 없음)을 생성하고 도메인만 적어 넣습니다:

```text
globaldevlog.com
```

Docusaurus는 빌드 시 `static/` 내의 모든 파일을 결과물 루트로 복사하므로, 배포가 발생할 때마다 `CNAME` 파일이 `gh-pages` 브랜치 최상단에 자동으로 영구 보존됩니다.

---

## 6. 프로덕션 라이브 검증

터미널에서 최종 배포를 실행합니다:
```bash
npm run deploy
```

배포가 완료되면 터미널에서 헤더 응답과 SSL 작동 상태를 확인합니다:

```bash
curl -I https://globaldevlog.com
# HTTP/2 200
# server: cloudflare
# strict-transport-security: max-age=31536000

curl -I https://www.globaldevlog.com
# HTTP/2 200 (또는 루트로의 301 리다이렉트)
```

### 아키텍처 이전의 성과
- **서버 비용 0원 유지**: 무거운 웹 서버 인프라 없이도 GitHub Pages의 안정적인 호스팅 활용.
- **엔터프라이즈급 보안 & 속도**: Cloudflare 엣지가 트래픽 스파이크를 흡수하고 SSL 인증서를 완전 자동 관리.
- **수익화 및 SEO 독립성**: 구글 애드센스 승인 신청 요건 및 4대 검색엔진 소유권 인증의 기반 완성.

---

## 🔜 다음 편 예고

독립 도메인 연동을 완수했다면, 이제 본격적인 블로그 수익화와 검색엔진 트래픽 확장을 시작해야 합니다:
- **제2편**: *[정적 사이트 수익화 #2] Docusaurus 구글 애드센스 승인 신청: ads.txt 404 해결과 스크립트 비동기 주입 실전*
- **제3편**: *[4대 검색엔진 SEO #3] 구글·네이버·빙 웹마스터 도구 완벽 등록: 사이트맵 삭제 트랩과 네이버 호스트 오류 탈출기*
