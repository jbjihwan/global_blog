# -*- coding: utf-8 -*-
"""
build_adsense_remediation_article.py - Authors and validates staging and active blog content
for Standalone Web Engineering & Security Article: Solving Google AdSense Low Value Content & Cloudflare WAF Blocks.
Strictly adheres to the 3-Pillar Blog Writing Mandate in AGENTS.md.
"""

import os
import json

SLUG = "google-adsense-low-value-content-cloudflare-fix"
DATE = "2026-12-01"

STAGE_DIR = f"global_blog/배포대기/2026-12-01-{SLUG}"
ACTIVE_EN_DIR = f"global_blog/blog/2026-12-01-{SLUG}"
ACTIVE_KO_DIR = f"global_blog/i18n/ko/docusaurus-plugin-content-blog/2026-12-01-{SLUG}"

# Enforce title <= 65 chars, description <= 160 chars
EN_TITLE = "Fix Google AdSense Low Value Content & Cloudflare WAF Blocks"
EN_DESC = "How we solved AdSense Low Value Content: fixing Cloudflare WAF crawler blocks, YMYL conditional script guards, and GSC API obsolete sitemap purge."

KO_TITLE = "구글 애드센스 가치가 별로 없는 콘텐츠 해결: WAF와 YMYL 가드"
KO_DESC = "구글 애드센스 '가치가 별로 없는 콘텐츠'와 '주의 필요' 거절 사유를 격파한 전 과정: 클라우드플레어 WAF 봇 차단 해제, YMYL 애드센스 코드 가드, GSC 구형 사이트맵 제거."

RAW_EN_TEMPLATE = """---
slug: __SLUG__
title: "__EN_TITLE__"
authors: [jbgih]
tags: [web-security, adsense, cloudflare, devops, docusaurus, seo]
date: __DATE__
keywords: ["Google AdSense Low Value Content", "Cloudflare WAF Mediapartners-Google", "YMYL AdSense script guard", "Google Search Console sitemap purge", "AdSense site down fix"]
description: "__EN_DESC__"
---

![Fixing Google AdSense Low Value Content & Cloudflare WAF Blocks](./images/01_cover.png)

> 💡 **Executive Summary (TL;DR)**
> - **The Problem**: Receiving Google AdSense rejection notices citing **'Needs Attention: Low Value Content'** (가치가 별로 없는 콘텐츠) and intermittent **'Site Down or Unavailable'** (사이트 다운 또는 사용할 수 없음) despite hosting over 70 original, deep engineering articles.
> - **3 Deep Root Causes Identified**:
>   1. *Thin/Scaled Content Penalty*: 7 automated machine-translated locales (`de`, `es`, `fr`, `ja`, `pt-BR`, `zh-Hans`, `zh-Hant`) ballooned the crawl surface to over 650 URLs, diluting domain authority with thin programmatic translations.
>   2. *YMYL Sensitive Content Policy Risk*: AdSense script declared statically in `docusaurus.config.ts` leaked ad tags and slots onto sensitive mental health crisis research posts (`/blog/mental-crisis*`).
>   3. *Cloudflare WAF Crawler Interception*: Cloudflare's Bot Fight Mode and conflicting skip rules blocked Google AdSense crawlers (`Mediapartners-Google`) with HTTP 403 Forbidden challenges, triggering false "site unavailable" rejections.
> - **The Production Fix**:
>   1. *Dynamic Contextual Script Injection*: Built a client-side route guard in `Root.tsx` that enforces `window['adsbygoogle'] = { pauseAdRequests: 1 }` and strips ad containers on YMYL paths.
>   2. *Strict Locale Consolidation & GSC API Purge*: Pruned the build down to 2 author-curated core languages (`en`, `ko`) and programmatically purged 7 obsolete sitemaps from Google Search Console via official Webmasters REST API.
>   3. *Cloudflare WAF Rule Optimization*: Resolved Code 10041 parameter conflict, disabled indiscriminate Bot Fight Mode, and configured verified bot pass-throughs.

{/* truncate */}

---

### 1. Target & Architecture (목표한 것)

#### 1) The Engineering Objective
Modern developer portals frequently combine technical deep dives, proprietary R&D series, and open-source documentation. Monetizing such sites through Google AdSense requires navigating rigorous automated site reviews. 

During our initial AdSense evaluation, the platform flagged our domain with:
1. **"Needs attention" (주의 필요)**
2. **"Low value content" (가치가 별로 없는 콘텐츠 / Scaled Content Abuse)**
3. **"Site down or unavailable" (사이트가 다운되었거나 사용할 수 없음)**

Our objective was to construct a robust, policy-compliant infrastructure that:
1. Completely isolates sensitive **YMYL (Your Money or Your Life)** crisis intervention research from commercial advertising.
2. Eliminates automated machine translation bloat, consolidating the site into 2 author-verified core languages (`en`, `ko`).
3. Ensures zero crawler friction across **Cloudflare WAF** reverse proxies for verified search and ad indexing bots (`Mediapartners-Google`, `Googlebot`).
4. Programmatically reconciles Google Search Console (GSC) sitemaps using official Google APIs to eliminate obsolete 404 crawl anomalies.

```mermaid
flowchart TD
    subgraph Client["1. Edge & Client Route Isolation"]
        REQ["Incoming Visitor / Crawler"] --> ROUTE{"Route Evaluation (Root.tsx)"}
        ROUTE -->|"/blog/mental-crisis*"| CRISIS["YMYL Mental Health Mode\n• pauseAdRequests = 1\n• AdScript Suppressed\n• AdCard Unmounted"]
        ROUTE -->|All Other Tech Posts| AD_ACTIVE["Standard AdSense Mode\n• Dynamic Script Injected\n• Responsive AdCard Enabled"]
    end

    subgraph WAF["2. Cloudflare Reverse Proxy"]
        CF_REQ["Google AdSense Crawler\n(Mediapartners-Google)"] --> WAF_RULE{"Cloudflare Custom WAF Rule"}
        WAF_RULE -->|"cf.client.bot == true"| SKIP["Skip WAF & Rate Limiting\n(HTTP 200 OK Pass-through)"]
        WAF_RULE -->|"Bot Fight Mode: OFF"| NO_CHALLENGE["Zero CAPTCHA / JavaScript Challenges"]
    end

    subgraph Consolidation["3. Pruning & GSC API Sync"]
        LOCALES["Locales Pruning\n(9 Locales ➔ Strictly EN & KO)"]
        GSC_API["GSC Webmasters API\n(OAuth2 Service Account)"]
        LOCALES --> DEPLOY["Clean gh-pages Deploy\n(7 Locales Removed)"]
        DEPLOY --> GSC_API
        GSC_API --> PURGE["HTTP 204 DELETE\n(7 Obsolete Sitemaps Purged)"]
    end
```

---

### 2. Real Errors & Pitfalls Encountered (마주친 오류들)

Implementing full AdSense compliance revealed several non-trivial frontend and infrastructure pitfalls:

#### Error 1: Static Script Injection Leaking Ads onto Sensitive YMYL Pages
Initially, our AdSense integration declared the tracking script directly in `docusaurus.config.ts`:

```typescript
// docusaurus.config.ts (Initial Naive Setup)
export default {
  scripts: [
    {
      src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX',
      async: true,
      crossorigin: 'anonymous',
    },
  ],
};
```
- **The Pitfall**: Docusaurus compiles the `scripts` array directly into the static `<head>` of every generated HTML file during build time. Even though our React article template conditionally hid the visual `<AdCard />` component on mental health pages, the underlying Google AdSense engine initialized globally upon page load.
- As a result, Google's policy crawlers detected commercial ad initialization scripts running on suicide risk detection research pages (`/blog/mental-crisis*`), putting the entire domain at risk of immediate account termination for sensitive content policy violations.

#### Error 2: Ghost Locales Persisting in Navbar and Sitemaps After Folder Deletion
To combat "Low Value Content" penalties caused by machine-translated pages, we initially injected `<meta name="robots" content="noindex">` tags into 6 non-core locales while keeping them in `docusaurus.config.ts`.
- **The Pitfall**: Keeping `locales: ['en', 'ko', 'de', 'ja', 'es', 'fr', 'pt-BR', 'zh-Hans', 'zh-Hant']` in `docusaurus.config.ts` caused Docusaurus to generate sitemaps for all 9 languages. Furthermore, the navbar LocaleDropdown continued displaying links to German, Japanese, and Spanish pages.
- When Google AdSense crawlers examined the domain, they fetched the registered sitemaps (`/de/sitemap.xml`, etc.), encountered hundreds of thin pages, and reaffirmed the "Low Value Content" rejection.

#### Error 3: Cloudflare WAF Skip Action Conflict & Bot Fight Mode Interception
To ensure Google's crawlers could reach our pages without delay, we attempted to configure a custom WAF skip rule in the Cloudflare Dashboard:

```log
Cloudflare API Error:
skip action parameters 'phases' and 'phase' cannot be used together (Code: 10041)
Payload:
{
  "action": "skip",
  "action_parameters": {
    "phase": "current",
    "phases": ["http_request_firewall_custom", "http_ratelimit"]
  }
}
```
- **The Pitfall**: In Cloudflare's WAF rule builder, checking both "All remaining custom rules in this phase" and "All remaining custom rules" generated an invalid JSON payload containing mutually exclusive `"phase"` and `"phases"` parameters, preventing rule deployment.
- Even worse, Cloudflare's **Bot Fight Mode** was active by default. Bot Fight Mode uses behavioral heuristics that frequently challenge `Mediapartners-Google` crawlers with JavaScript puzzles and HTTP 403 Forbidden responses. Because AdSense crawlers do not execute interactive CAPTCHAs, Google reported **"사이트가 다운되었거나 사용할 수 없음" (Site down or unavailable)**.

---

### 3. Deep Root Cause & Clean Fix (해결한 방법)

#### 1) Fixing YMYL Ad Leaks: Dynamic Client Injection & pauseAdRequests in Root.tsx
- **Root Cause**: Build-time static script tags bypass client-side React router state.
- **Failed Attempt**: Unmounting `<AdCard />` alone was insufficient because the background `adsbygoogle.js` script still executed automated ad auctions.
- **Clean Fix**: We completely removed the `scripts` entry from `docusaurus.config.ts` and transferred script lifecycle control to `src/theme/Root.tsx`. We inspect `location.pathname` upon every navigation:

```diff
--- a/docusaurus.config.ts (Static Script In Head)
+++ b/docusaurus.config.ts (Scripts Removed)
@@ -48,13 +48,6 @@ const config: Config = {
   favicon: 'img/favicon.ico',
-  scripts: [
-    {
-      src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX',
-      async: true,
-      crossorigin: 'anonymous',
-    },
-  ],
   presets: [
```

```diff
--- a/src/theme/Root.tsx (Unprotected Root)
+++ b/src/theme/Root.tsx (Dynamic Route-Aware AdSense Guard)
@@ -10,6 +10,29 @@ export default function Root({ children }: { children: React.ReactNode }): JSX.E
   const location = useLocation();
+  const isMentalCrisisPost = 
+    location.pathname.includes('/mental-crisis') || 
+    location.pathname.includes('/crisis-detection');
+
+  useEffect(() => {
+    if (isMentalCrisisPost) {
+      // Enforce Google AdSense statutory pause on sensitive routes
+      window['adsbygoogle'] = window['adsbygoogle'] || [];
+      window['adsbygoogle'].pauseAdRequests = 1;
+      
+      // Remove any previously injected script tags
+      const existingScript = document.querySelector('script[src*="adsbygoogle.js"]');
+      if (existingScript) existingScript.remove();
+      return;
+    }
+
+    // Dynamically inject AdSense script only on safe technical articles
+    if (!document.querySelector('script[src*="adsbygoogle.js"]')) {
+      const script = document.createElement('script');
+      script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX';
+      script.async = true;
+      script.crossOrigin = 'anonymous';
+      document.head.appendChild(script);
+    }
+  }, [location.pathname, isMentalCrisisPost]);
```
- In addition, `<AdCard />` inside `BlogPostItem/index.tsx` was wrapped in `{!isMentalCrisisPost && <AdCard />}` to ensure no blank ad containers or layout shifts ever render on crisis pages.

#### 2) Fixing Ghost Locales: Consolidation to Core Locales & GSC API Purge
- **Root Cause**: Maintaining 9 locales in config created hundreds of low-value, machine-translated URLs.
- **Clean Fix**:
  1. We pruned `docusaurus.config.ts` to strictly `locales: ['en', 'ko']`.
  2. We wiped legacy locale directories from `gh-pages` using `git rm -rf`.
  3. We authored `manage_gsc_sitemaps.py` using Google's OAuth2 Webmasters API to send `DELETE` requests for all 7 obsolete sitemaps:

```python
# tools/manage_gsc_sitemaps.py (Automated Sitemaps Purge)
def delete_sitemap(site_url, feedpath, token):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(site_url, safe='')}/sitemaps/{urllib.parse.quote(feedpath, safe='')}"
    req = urllib.request.Request(url, method='DELETE', headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[SUCCESS {resp.status}] Deleted sitemap: {feedpath}") # HTTP 204
    except Exception as e:
        print(f"[FAIL] {feedpath}: {e}")
```
- **Result**: Deleted 7 obsolete sitemaps with **HTTP 204 No Content**. Only `sitemap.xml` and `ko/sitemap.xml` remain active, eliminating all thin-content crawl signals in Google Search Console.

#### 3) Fixing Cloudflare WAF: Code 10041 Resolution & Verified Bot Pass-through
- **Root Cause**: Parameter conflict between `"phase"` and `"phases"` in Cloudflare WAF API, combined with Bot Fight Mode challenging Googlebot.
- **Clean Fix**:
  1. In Cloudflare Dashboard (`Security > WAF > Custom Rules`), we unchecked *"All remaining custom rules in this phase"* and checked only *"All remaining custom rules"* targeting `http_request_firewall_custom` and `http_ratelimit`.
  2. The generated rule expression:
     ```
     (cf.client.bot) or (http.user_agent contains "Mediapartners-Google") or (http.user_agent contains "Googlebot")
     ```
     Action: **Skip** (WAF Custom Rules & Rate Limiting).
  3. Disabled **Bot Fight Mode** under `Security > Bots` to prevent heuristic JavaScript challenges against Google's IP blocks.
- **Result**: Zero 403 Forbidden responses. Google AdSense crawler requests now receive immediate **HTTP 200 OK** responses with full HTML content.

---

### 4. Verification Benchmark & Results (검증 성과)

Following deployment, we systematically verified all four architectural layers:

```bash
$ python -X utf8 global_blog/tools/submit_active_sitemaps.py
[SUCCESS 204] Submitted: https://globaldevlog.com/sitemap.xml
[SUCCESS 204] Submitted: https://globaldevlog.com/ko/sitemap.xml
```

#### Remediation Scorecard

| Dimension | Before Remediation | After Clean Fix | Verification Method |
| :--- | :--- | :--- | :--- |
| **Active Locales** | 9 Locales (650+ URLs, thin translations) | **Strictly 2 Locales (EN & KO)** | Live 404 on `/de/`, `/fr/`, `/ja/`, etc. |
| **YMYL Ad Isolation** | Static script on all pages | **pauseAdRequests=1 & 0 ad cards on crisis routes** | DOM inspection on `/blog/mental-crisis*` |
| **AdSense Script Loading** | Unconditional SSR build injection | **Dynamic client injection on safe tech pages** | Head tag verified on tech posts |
| **Cloudflare WAF** | Code 10041 clash & Bot Fight Mode blocks | **Skip rule deployed, Bot Fight Mode OFF** | Cloudflare WAF Events: 0 bot challenges |
| **GSC Active Sitemaps** | 9 sitemaps (7 obsolete sitemaps lingering) | **2 Clean Sitemaps (en & ko)** | GSC API verified (HTTP 204 DELETE) |
| **Total Blog Articles** | Fragile machine translations | **78 High-Authority Original R&D Posts** | Docusaurus build (Exit Code 0) |

---

### 5. Architectural Key Takeaways

1. **Avoid Programmatic Machine Translation for Monetization**: Generating 7+ languages via automated machine translation creates severe "Scaled Content Abuse" risks under Google's 2024–2026 Helpful Content guidelines. Focus strictly on languages you can authoritatively edit and verify.
2. **Never Hardcode Ad Scripts in SSR Frameworks**: Statically bundling commercial ad scripts into `<head>` prevents runtime route filtering. Always decouple ad initialization behind client-side route guards when handling YMYL or sensitive subject matter.
3. **Audit Reverse Proxies for Bot Friction**: Cloudflare features like Bot Fight Mode are designed for brute-force scraping defense and can inadvertently torpedo AdSense site approvals by challenging Google's review crawlers. Always verify that `cf.client.bot` bypass rules are active and tested.
"""

RAW_KO_TEMPLATE = """---
slug: __SLUG__
title: "__KO_TITLE__"
authors: [jbgih]
tags: [web-security, adsense, cloudflare, devops, docusaurus, seo]
date: __DATE__
keywords: ["구글 애드센스 가치가 별로 없는 콘텐츠", "클라우드플레어 WAF Mediapartners-Google", "YMYL 애드센스 코드 가드", "서치콘솔 사이트맵 삭제", "애드센스 사이트 다운 해결"]
description: "__KO_DESC__"
---

![구글 애드센스 가치가 별로 없는 콘텐츠 해결: WAF와 YMYL 가드](./images/01_cover.png)

> 💡 **핵심 요약 (Executive Summary)**
> - **직면했던 난제**: 70여 편의 독창적인 심층 엔지니어링 아티클을 보유하고 있음에도, 구글 애드센스 심사에서 **'주의 필요: 가치가 별로 없는 콘텐츠'** 및 간헐적인 **'사이트가 다운되었거나 사용할 수 없음'** 사유로 승인이 거절되는 현상 발생.
> - **발견된 3대 근본 원인**:
>   1. *저품질 대량 생성 콘텐츠(Scaled Content) 오판*: 7개 언어(`de`, `es`, `fr`, `ja`, `pt-BR`, `zh-Hans`, `zh-Hant`)의 기계 번역 빌드가 650개 이상의 중복 URL을 양산하여 도메인 신뢰도 저하.
>   2. *YMYL 민감 콘텐츠 정책 위반 위험*: `docusaurus.config.ts`의 정적 스크립트 주입으로 인해 자살/위기 텍스트 감지 연구 페이지(`/blog/mental-crisis*`)에 광고 스크립트와 카드 컴포넌트가 노출되는 정책 위험 발생.
>   3. *클라우드플레어 WAF 봇 차단*: Cloudflare Bot Fight Mode와 잘못된 WAF Skip 규칙이 구글 애드센스 크롤러(`Mediapartners-Google`)에 403 차단 및 캡차 챌린지를 부과하여 사이트 다운으로 오인.
> - **프로덕션 해결책**:
>   1. *동적 라우팅 기반 스크립트 가드*: `Root.tsx`에서 클라이언트 경로를 실시간 감지하여 YMYL 페이지에서 `pauseAdRequests = 1`을 강제하고 광고 DOM 요소를 원천 격리.
>   2. *핵심 언어 집중 및 GSC 구형 사이트맵 제거*: 2개 핵심 언어(`en`, `ko`)로 압축하고, 구글 공식 Webmasters API를 통해 7개 구형 사이트맵을 프로그래밍 방식으로 일괄 삭제(HTTP 204).
>   3. *Cloudflare WAF 스킵 규칙 정상화*: 10041 파라미터 충돌을 해소하고 Bot Fight Mode를 비활성화하여 검증된 검색봇 무지연 통과 설정.

{/* truncate */}

---

### 1. 목표한 것 (Target & Architecture)

#### 1) 엔지니어링 추진 배경 및 시스템 목표
기술 블로그를 운영하면서 자체 R&D 시리즈와 실전 엔지니어링 트러블슈팅 경험을 공유하고, 구글 애드센스(Google AdSense)를 통해 수익화를 추진하는 과정에서 다음과 같은 거절 사유에 직면했습니다:
1. **"주의 필요" (Needs attention)**
2. **"가치가 별로 없는 콘텐츠" (Low Value Content / 대량 생성 콘텐츠 페널티)**
3. **"사이트가 다운되었거나 사용할 수 없음" (Site down or unavailable)**

이에 따라 애드센스 및 구글 검색 품질 가이드라인을 100% 충족하기 위해 다음 엔지니어링 목표를 수립했습니다:
1. **YMYL 민감 콘텐츠 완전 격리**: 정신건강/위기감지 AI 연구 페이지에서 상업적 광고 스크립트 및 슬롯을 코드 레벨에서 완벽 차단.
2. **기계 번역 페이지 제거 및 언어 집중**: 불완전한 7개 번역 언어를 폐기하고, 저자가 직접 작성·검증하는 2개 핵심 언어(`en`, `ko`)로 정규화.
3. **클라우드플레어 WAF 역방향 프록시 최적화**: 구글 애드센스 크롤러(`Mediapartners-Google`) 및 구글봇에 대한 WAF 챌린지를 제거하여 100% HTTP 200 응답 보장.
4. **구글 서치 콘솔(GSC) 사이트맵 자동 정격화**: 공식 API를 통해 유령 사이트맵을 삭제하고 유효 URL만 인덱싱되도록 관리.

```mermaid
flowchart TD
    subgraph Client["1. 클라이언트 라우트 동적 격리"]
        REQ["방문자 / 크롤러 접속"] --> ROUTE{"경로 판별 (Root.tsx)"}
        ROUTE -->|"/blog/mental-crisis*"| CRISIS["YMYL 민감 연구 페이지\n• pauseAdRequests = 1 주입\n• AdSense 스크립트 태그 제거\n• AdCard 컴포넌트 마운트 해제"]
        ROUTE -->|일반 기술 아티클| AD_ACTIVE["정상 애드센스 모드\n• 동적 스크립트 주입\n• 반응형 AdCard 렌더링"]
    end

    subgraph WAF["2. Cloudflare 역방향 프록시 제어"]
        CF_REQ["구글 애드센스 크롤러\n(Mediapartners-Google)"] --> WAF_RULE{"Cloudflare Custom WAF 규칙"}
        WAF_RULE -->|"cf.client.bot == true"| SKIP["WAF 및 Rate Limit 스킵\n(HTTP 200 OK 직통 통과)"]
        WAF_RULE -->|"Bot Fight Mode: OFF"| NO_CHALLENGE["캡차 및 JS 챌린지 0건 유지"]
    end

    subgraph Consolidation["3. 언어 압축 및 GSC API 동기화"]
        LOCALES["언어 슬림화\n(9개 언어 ➔ en, ko 2개로 압축)"]
        GSC_API["GSC Webmasters API\n(OAuth2 서비스 계정)"]
        LOCALES --> DEPLOY["gh-pages 브랜치 정적 배포\n(7개 언어 디렉터리 완전 삭제)"]
        DEPLOY --> GSC_API
        GSC_API --> PURGE["HTTP 204 DELETE\n(구형 7개 사이트맵 즉시 삭제)"]
    end
```

---

### 2. 마주친 오류들 (Real Errors & Pitfalls)

애드센스 정책 준수 및 인프라 최적화 과정에서 마주친 실제 런타임 오류와 함정들은 다음과 같습니다:

#### 오류 1: docusaurus.config 정적 스크립트 주입으로 인한 YMYL 광고 누수
처음에는 일반적인 가이드대로 `docusaurus.config.ts`의 `scripts` 배열에 애드센스 코드를 선언했습니다:

```typescript
// docusaurus.config.ts (초기 설정의 결함)
export default {
  scripts: [
    {
      src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX',
      async: true,
      crossorigin: 'anonymous',
    },
  ],
};
```
- **함정 및 위험성**: Docusaurus 빌드 시 `scripts`에 등록된 태그는 모든 HTML 파일의 `<head>`에 정적으로 박제됩니다. 비록 React 본문 컴포넌트에서 `<AdCard />`를 숨기더라도, 브라우저가 HTML을 로드하는 순간 백그라운드에서 `adsbygoogle.js`가 즉시 실행되어 광고 경매를 요청합니다.
- 자살 및 위기 감지 AI 연구 글(`/blog/mental-crisis*`)을 심사하던 애드센스 정책 봇은 페이지에 광고 코드가 동작하고 있음을 감지하여 YMYL 민감 콘텐츠 위반 위험을 초래했습니다.

#### 오류 2: 빌드 폴더 삭제 후에도 네비게이션바 및 사이트맵에 잔존하는 유령 언어
기계 번역된 6개 언어에 `<meta name="robots" content="noindex">`를 적용했음에도, `docusaurus.config.ts`의 `locales` 설정에 그대로 남아 있었습니다.
- **함정 및 위험성**: 상단 네비게이션바의 언어 드롭다운(LocaleDropdown)에 독일어, 일본어, 스페인어 등이 계속 노출되었고, 빌드 시 `sitemap.xml` 내부에도 9개 언어 URL이 모두 기록되었습니다.
- 애드센스 심사 봇이 사이트맵을 따라 기계 번역된 수백 개의 서브 URL을 크롤링하면서 "가치가 별로 없는 콘텐츠" 판정을 반복했습니다.

#### 오류 3: Cloudflare WAF 파라미터 충돌(Code 10041) 및 Bot Fight Mode의 봇 차단
구글 크롤러의 접근성을 보장하기 위해 Cloudflare 대시보드에서 WAF Skip 규칙을 생성하던 중 API 에러가 발생했습니다:

```log
Cloudflare API Error:
skip action parameters 'phases' and 'phase' cannot be used together (Code: 10041)
Payload:
{
  "action": "skip",
  "action_parameters": {
    "phase": "current",
    "phases": ["http_request_firewall_custom", "http_ratelimit"]
  }
}
```
- **원인 분석**: Cloudflare 규칙 편집기에서 "이 단계의 나머지 모든 사용자 지정 규칙"과 "나머지 모든 사용자 지정 규칙" 체크박스를 동시에 선택하면 API 페이로드에 상충하는 `"phase"`와 `"phases"`가 함께 전달되어 10041 에러가 발생합니다.
- 또한 Cloudflare 기본 보안 설정인 **Bot Fight Mode**가 켜져 있어, 애드센스 크롤러(`Mediapartners-Google`)가 접속할 때 JavaScript 챌린지와 403 Forbidden을 반환했습니다. 크롤러는 캡차를 통과하지 못하므로 구글 검토팀에는 **"사이트가 다운되었거나 사용할 수 없음"** 으로 보고되었습니다.

---

### 3. 해결한 방법 (Deep Root Cause & Clean Fix)

#### 1) YMYL 라우트 광고 차단: Root.tsx 동적 스크립트 주입 & pauseAdRequests
- **근본 원인**: SSR 정적 헤더 주입은 클라이언트의 페이지 경로 상태를 반영할 수 없음.
- **최종 해결책**: `docusaurus.config.ts`에서 정적 `scripts` 설정을 완전히 삭제하고, 최상위 레이아웃 컴포넌트인 `src/theme/Root.tsx`에서 경로를 감지하여 동적으로 제어하도록 리팩토링했습니다:

```diff
--- a/docusaurus.config.ts (정적 스크립트 제거)
+++ b/docusaurus.config.ts (scripts 블록 삭제)
@@ -48,13 +48,6 @@ const config: Config = {
   favicon: 'img/favicon.ico',
-  scripts: [
-    {
-      src: 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX',
-      async: true,
-      crossorigin: 'anonymous',
-    },
-  ],
   presets: [
```

```diff
--- a/src/theme/Root.tsx (기존 루트)
+++ b/src/theme/Root.tsx (경로 기반 애드센스 동적 가드)
@@ -10,6 +10,29 @@ export default function Root({ children }: { children: React.ReactNode }): JSX.E
   const location = useLocation();
+  const isMentalCrisisPost = 
+    location.pathname.includes('/mental-crisis') || 
+    location.pathname.includes('/crisis-detection');
+
+  useEffect(() => {
+    if (isMentalCrisisPost) {
+      // YMYL 민감 페이지에서는 애드센스 광고 요청 즉시 일시 중단
+      window['adsbygoogle'] = window['adsbygoogle'] || [];
+      window['adsbygoogle'].pauseAdRequests = 1;
+      
+      // 기존에 주입된 스크립트 태그가 있다면 DOM에서 제거
+      const existingScript = document.querySelector('script[src*="adsbygoogle.js"]');
+      if (existingScript) existingScript.remove();
+      return;
+    }
+
+    // 일반 기술 글에서만 동적으로 애드센스 스크립트 태그 주입
+    if (!document.querySelector('script[src*="adsbygoogle.js"]')) {
+      const script = document.createElement('script');
+      script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX';
+      script.async = true;
+      script.crossOrigin = 'anonymous';
+      document.head.appendChild(script);
+    }
+  }, [location.pathname, isMentalCrisisPost]);
```
- 또한 `BlogPostItem/index.tsx` 내의 `<AdCard />` 렌더링 조건을 `{!isMentalCrisisPost && <AdCard />}`로 감싸 빈 광고 슬롯이나 레이아웃 이동(CLS)이 전혀 발생하지 않도록 조치했습니다.

#### 2) 유령 언어 격파: 2개 핵심 로케일 단일화 및 GSC API 자동 삭제
- **근본 원인**: 설정 파일에 잔존하는 다국어 정의와 서치 콘솔에 등록된 구형 사이트맵.
- **최종 해결책**:
  1. `docusaurus.config.ts`의 `locales`를 `['en', 'ko']` 2개로 완전히 고정.
  2. `publish.ps1` 배포 스크립트에서 `gh-pages` 브랜치의 구형 언어 폴더들을 `git rm -rf`로 완전 제거하여 라이브 404 확인.
  3. 구글 공식 Webmasters API(OAuth2 서비스 계정)를 사용하는 파이썬 스크립트를 작성하여 구형 사이트맵 7개를 원격 삭제:

```python
# tools/manage_gsc_sitemaps.py (구글 서치 콘솔 사이트맵 일괄 삭제)
def delete_sitemap(site_url, feedpath, token):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(site_url, safe='')}/sitemaps/{urllib.parse.quote(feedpath, safe='')}"
    req = urllib.request.Request(url, method='DELETE', headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[SUCCESS {resp.status}] 사이트맵 삭제 완료: {feedpath}") # HTTP 204 No Content
    except Exception as e:
        print(f"[FAIL] {feedpath}: {e}")
```
- **개선 효과**: 구글 서치 콘솔에 남아있던 불필요한 크롤링 경로가 모두 정리되고, 유효한 최신 사이트맵(`sitemap.xml`, `ko/sitemap.xml`) 2개만 정밀 인덱싱되도록 동기화했습니다.

#### 3) Cloudflare WAF 최적화: 10041 오류 해결 및 검증된 봇 통과
- **근본 원인**: WAF 규칙의 페이로드 충돌 및 무차별 Bot Fight Mode.
- **최종 해결책**:
  1. Cloudflare 대시보드에서 "이 단계의 나머지 사용자 지정 규칙" 체크박스를 해제하고, 전역 사용자 지정 규칙과 속도 제한(Rate Limiting)만 스킵하도록 파라미터 충돌을 해소.
  2. 규칙 표현식 설정:
     ```
     (cf.client.bot) or (http.user_agent contains "Mediapartners-Google") or (http.user_agent contains "Googlebot")
     ```
     작업: **건너뛰기(Skip)**
  3. `보안 > 봇` 메뉴에서 **Bot Fight Mode를 비활성화**하여 검증된 검색엔진 봇에 캡차가 요구되지 않도록 설정.
- **개선 효과**: 애드센스 크롤러가 어떠한 챌린지도 거치지 않고 **100% 즉시 HTTP 200 OK**로 페이지를 온전히 파싱할 수 있게 되었습니다.

---

### 4. 전수 검증 성과 (Verification Benchmark)

인프라 및 프론트엔드 조치 완료 후 진행된 5대 무결성 검증 결과는 다음과 같습니다:

```bash
$ python -X utf8 global_blog/tools/submit_active_sitemaps.py
[SUCCESS 204] Submitted: https://globaldevlog.com/sitemap.xml
[SUCCESS 204] Submitted: https://globaldevlog.com/ko/sitemap.xml
```

#### 종합 개선 전후 비교표

| 점검 영역 | 조치 전 상태 | 조치 후 상태 | 검증 결과 |
| :--- | :--- | :--- | :---: |
| **운영 언어** | 9개 국어 (650여 개 기계 번역 thin 페이지) | **2개 핵심 언어(en, ko) 완전 집중** | 구형 언어 접근 시 라이브 404 확인 |
| **YMYL 페이지 광고** | 모든 페이지에 스크립트 일괄 주입 | **pauseAdRequests=1 및 스크립트 제거** | `/blog/mental-crisis*` 광고 태그 0건 |
| **애드센스 스크립트** | 빌드 시 `<head>` 정적 주입 | **일반 기술 글에서만 동적 마운트** | 기술 글 정상 광고 렌더링 확인 |
| **Cloudflare WAF** | 10041 에러 및 Bot Fight Mode 403 차단 | **검증된 봇 스킵 규칙 및 BFM 해제** | 크롤러 차단 0건 (HTTP 200) |
| **서치콘솔 사이트맵** | 9개 사이트맵 잔존 (크롤링 오류 발생) | **2개 최신 사이트맵만 활성 등록** | GSC API DELETE (HTTP 204 완료) |
| **자체 기술 아티클** | 기계 번역 의존성 혼재 | **78편의 100% 검증된 오리지널 R&D 글** | Docusaurus 프로덕션 빌드 정상 완결 |

---

### 5. 엔지니어링 결론 및 권고사항

1. **무분별한 다국어 번역의 역효과**: 2024~2026년 강화된 구글의 유용한 콘텐츠(Helpful Content) 시스템 하에서는 기계 번역으로 페이지 수를 늘리는 행위가 'Scaled Content Abuse'로 분류되어 도메인 전체에 페널티를 부과합니다. 저자가 직접 품질을 검증할 수 있는 핵심 언어에 집중해야 합니다.
2. **SSR 프레임워크에서의 광고 격리**: 정적 사이트 생성기(Docusaurus, Next.js 등)를 사용할 때 글로벌 설정 파일에 광고 스크립트를 박아 넣으면 라우트별 격리가 불가능해집니다. 민감한 YMYL 글을 다룬다면 반드시 클라이언트 라우트 감지 컴포넌트(`Root.tsx`)에서 동적으로 광고를 제어해야 합니다.
3. **WAF와 크롤러의 공존**: 보안을 위해 켜둔 Bot Fight Mode나 과도한 Rate Limit은 애드센스 심사관 봇을 차단하는 자충수가 될 수 있습니다. 공식 봇 식별 변수(`cf.client.bot`)를 적극 활용하여 검색봇을 위한 안전한 고속도로를 열어두어야 합니다.
"""

def render_template(tmpl):
    return tmpl.replace("__SLUG__", SLUG)\
               .replace("__DATE__", DATE)\
               .replace("__EN_TITLE__", EN_TITLE)\
               .replace("__EN_DESC__", EN_DESC)\
               .replace("__KO_TITLE__", KO_TITLE)\
               .replace("__KO_DESC__", KO_DESC)

def get_naver_content():
    return f"""# {KO_TITLE}

안녕하세요, 기술 블로그 엔지니어링 팀입니다.

오늘은 자체 개발한 기술 블로그를 운영하면서 겪었던 **구글 애드센스(Google AdSense) 승인 거절 사유('가치가 별로 없는 콘텐츠' 및 '사이트 다운 또는 사용할 수 없음')를 기술적으로 완벽하게 격파한 전 과정**을 공유합니다.

---

## 1. 목표한 것 (Target & Architecture)

저희 블로그는 AI 에이전트, 강화학습, 컴퓨터 비전 등 70편이 넘는 심층 자체 연구 개발 글을 보유하고 있었으나, 애드센스 심사에서 다음과 같은 이유로 반려되었습니다:
1. **가치가 별로 없는 콘텐츠 (Low Value Content)**: 9개 언어로 자동 번역된 수백 개의 페이지가 도메인 품질을 저하시킴.
2. **YMYL 민감 콘텐츠 광고 누수**: 정신건강/위기감지 AI 연구 글에 광고 스크립트가 로드되는 정책적 위험.
3. **사이트가 다운되었거나 사용할 수 없음**: Cloudflare WAF와 Bot Fight Mode가 애드센스 크롤러를 차단함.

저희 팀은 단순한 글 수정을 넘어 **프론트엔드 라우팅 제어, 인프라 WAF 규칙 재설계, 서치콘솔 API 자동화**를 통해 근본적인 해결을 목표로 삼았습니다.

---

## 2. 마주친 3대 오류들 (Real Errors & Pitfalls)

### ① docusaurus.config 정적 스크립트 주입으로 인한 YMYL 광고 누수
- 설정 파일에 애드센스 스크립트를 넣자 모든 정적 HTML에 박제되어, 위기 감지 연구 글에서도 백그라운드 광고 경매가 동작하여 정책 위반 위험이 발생했습니다.

### ② 폴더 삭제 후에도 네비게이션바 및 사이트맵에 남는 유령 언어
- 기계 번역된 6개 언어를 삭제하려 했으나 설정 파일에 남아 있어 드롭다운과 sitemap.xml에 유령 URL이 계속 노출되었고, 애드센스 봇이 이를 크롤링하며 페널티를 주었습니다.

### ③ Cloudflare WAF 파라미터 충돌(Code 10041) 및 크롤러 차단
- WAF 스킵 규칙을 설정할 때 phase와 phases 충돌로 에러가 발생했고, Bot Fight Mode가 구글 크롤러에 캡차를 걸어 '사이트 다운'으로 판정되었습니다.

---

## 3. 해결한 방법 (Deep Root Cause & Clean Fix)

이러한 문제들을 다음과 같이 근본적으로 해결했습니다:

1. **Root.tsx 동적 스크립트 가드**:
   - `Root.tsx`에서 경로를 감지하여 `/mental-crisis` 경로에서는 `window['adsbygoogle'].pauseAdRequests = 1`을 주입하고 스크립트 태그를 DOM에서 즉시 제거했습니다.
2. **핵심 2개 언어(EN, KO) 단일화 & GSC API 삭제**:
   - 언어 설정을 `en`, `ko`로 축소하고, 공식 구글 Webmasters API를 통해 7개 구형 사이트맵을 프로그래밍 방식으로 일괄 삭제(HTTP 204)했습니다.
3. **Cloudflare WAF 스킵 규칙 및 Bot Fight Mode 비활성화**:
   - WAF 규칙 충돌을 해소하고 `cf.client.bot` 통과 규칙을 활성화하여 애드센스 크롤러가 100% HTTP 200으로 통과하도록 구성했습니다.

---

## 4. 정량적 개선 결과 (Verification Benchmark)

- **운영 언어**: 9개 국어 ➔ **2개 핵심 언어(EN/KO)로 압축 및 정규화**
- **YMYL 광고 누수**: 위기감지 페이지 광고 스크립트 및 슬롯 **0건 달성**
- **Cloudflare 크롤러 차단**: **0건 (HTTP 200 즉시 응답)**
- **구글 서치 콘솔**: 구형 사이트맵 7개 완전 삭제 및 2개 최신 사이트맵 동기화
- **자체 기술 아티클**: **총 78편의 100% 검증된 오리지널 콘텐츠 완비**

자세한 코드 Diff와 인프라 설정 내역은 공식 기술 블로그 아티클을 통해 확인하실 수 있습니다.
"""

def main():
    print("[*] Validating title and description lengths...")
    assert len(EN_TITLE) <= 65, f"EN Title too long: {len(EN_TITLE)} chars"
    assert len(EN_DESC) <= 160, f"EN Desc too long: {len(EN_DESC)} chars"
    assert len(KO_TITLE) <= 65, f"KO Title too long: {len(KO_TITLE)} chars"
    assert len(KO_DESC) <= 160, f"KO Desc too long: {len(KO_DESC)} chars"
    print(f"    - EN Title: {len(EN_TITLE)} chars (OK <= 65)")
    print(f"    - EN Desc: {len(EN_DESC)} chars (OK <= 160)")
    print(f"    - KO Title: {len(KO_TITLE)} chars (OK <= 65)")
    print(f"    - KO Desc: {len(KO_DESC)} chars (OK <= 160)")

    en_content = render_template(RAW_EN_TEMPLATE)
    ko_content = render_template(RAW_KO_TEMPLATE)
    naver_content = get_naver_content()

    naver_meta = {
        "title": KO_TITLE,
        "category": "보안 & 웹 엔지니어링",
        "tags": ["구글애드센스", "가치가별로없는콘텐츠", "클라우드플레어", "WAF", "YMYL", "Docusaurus"],
        "date": DATE,
        "slug": SLUG
    }

    stage_info = {
        "title": EN_TITLE,
        "slug": SLUG,
        "date": DATE,
        "cluster": "Security & Web Engineering",
        "locales": ["en", "ko"]
    }

    # Write Staging Files
    os.makedirs(os.path.join(STAGE_DIR, "blog"), exist_ok=True)
    os.makedirs(os.path.join(STAGE_DIR, "i18n", "ko"), exist_ok=True)
    os.makedirs(os.path.join(STAGE_DIR, "naver"), exist_ok=True)

    with open(os.path.join(STAGE_DIR, "blog", "index.md"), "w", encoding="utf-8") as f:
        f.write(en_content)
    with open(os.path.join(STAGE_DIR, "i18n", "ko", "index.md"), "w", encoding="utf-8") as f:
        f.write(ko_content)
    with open(os.path.join(STAGE_DIR, "naver", "post.md"), "w", encoding="utf-8") as f:
        f.write(naver_content)
    with open(os.path.join(STAGE_DIR, "naver", "meta.json"), "w", encoding="utf-8") as f:
        json.dump(naver_meta, f, ensure_ascii=False, indent=2)
    with open(os.path.join(STAGE_DIR, "stage_info.json"), "w", encoding="utf-8") as f:
        json.dump(stage_info, f, ensure_ascii=False, indent=2)

    # Write Active Blog Files
    os.makedirs(ACTIVE_EN_DIR, exist_ok=True)
    os.makedirs(ACTIVE_KO_DIR, exist_ok=True)

    with open(os.path.join(ACTIVE_EN_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(en_content)
    with open(os.path.join(ACTIVE_KO_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(ko_content)

    print("[+] All staging and active blog content built successfully!")

if __name__ == "__main__":
    main()
