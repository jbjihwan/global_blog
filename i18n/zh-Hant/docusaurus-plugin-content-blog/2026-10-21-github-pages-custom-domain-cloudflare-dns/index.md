---
slug: github-pages-custom-domain-cloudflare-dns
title: "[GitHub Pages 獨立網域 #1] 告別免費 github.io：使用 Porkbun + Cloudflare 綁定自訂網域 (CNAME 扁平化與免費 SSL)"
authors: [jbjihwan]
tags: [github-pages, custom-domain, porkbun, cloudflare, docusaurus, devops]
keywords: [Docusaurus GitHub Pages Custom Domain, Cloudflare DNS Porkbun CNAME setup, CNAME 扁平化 根網域 GitHub Pages, Cloudflare 免費 Universal SSL, static CNAME 部署重置解決]
description: "徹底告別免費 github.io 二級子網域，透過 Porkbun 購買頂級網域並委派至 Cloudflare Anycast DNS，利用 CNAME 扁平化 (Flattening) 達成 GitHub Pages 零停機平滑遷移，解決 Docusaurus CNAME 自動重設難題的完整工程實戰。"

---

對於技術開發者而言，利用 GitHub Pages 的免費二級子網域（`username.github.io/project`）架設部落格幾乎是零成本的最佳入門選擇。只需一次 Git Push，即可透過全球 CDN 免費分發靜態頁面，完全無需維護底層伺服器。

然而，一旦你計劃打造具有專業影響力的技術品牌並開啟 **Google AdSense（谷歌廣告聯盟）流量變現** 時，就會遭遇一道無法逾越的規則紅線：**Google AdSense 嚴格禁止針對 `*.github.io` 等免費二級子網域提交網站審查**。此外，搜尋引擎累積的網域權重（Domain Authority）也無法沉澱為個人數位資產。要想通過商業化審查並沉澱 SEO 資產，擁有獨立的**頂級根網域（Apex Custom Domain，例如 `globaldevlog.com`）**是必經之路。

作為靜態網站工程化系列的第一篇，本文將以我們的技術部落格從 `jbjihwan.github.io/global_blog` 遷移至 `https://globaldevlog.com` 的實戰經歷為基礎，詳細拆解由 **Porkbun + Cloudflare + GitHub Pages 構建的高可用三層生產架構與 DNS 深度配置要點**。

{/* truncate */}

---

![靜態工程部落格生產級 DNS 與 CDN 路由架構圖](./images/01_dns_routing_architecture.png)

---

## 1. 架構設計哲學：三層專業化高可用體系

初學者在為 GitHub Pages 綁定獨立網域時，最常規的做法是在網域名稱註冊商處將 `A 記錄` 直接指向 GitHub 的 4 個固定 IP（`185.199.108.153` 等）。

這種傳統模式雖然簡單，但存在明顯的生產運維缺陷：
- 缺乏邊緣層 DDoS 攻擊防護與惡意爬蟲清洗；
- 遭遇故障或底層遷移時，DNS 生效速度緩慢；
- 無法對靜態資源（CSS/JS/圖片）進行靈活的邊緣 CDN 快取調優。

為此，我們將職責解耦為三個專業化的服務層級：

| 層級 | 選用服務 | 核心職責與入選理由 |
| :--- | :--- | :--- |
| **1. 網域註冊商 (Registrar)** | **Porkbun** | 頂級網域首購與每年續費價格全網極具優勢，終身免費贈送 WHOIS 隱私保護，無套路加價 |
| **2. 邊緣 DNS 與安全層** | **Cloudflare** | 全球超低延遲 Anycast DNS，**根網域 CNAME 扁平化 (Flattening)**，免費 Universal SSL，自動化強制 HTTPS |
| **3. 靜態託管源站** | **GitHub Pages** | 承載由 Docusaurus 編譯產生的純靜態產物，`gh-pages` 分支自動化部署，零伺服器成本 |

---

## 2. 第一步：Porkbun 網域購買與 Cloudflare 權威名稱伺服器委派

1. **網域選購**：在 Porkbun 檢索並購買心儀的頂級根網域（如 `globaldevlog.com`）。
2. **接入 Cloudflare**：登入 Cloudflare 控制台，點擊 **[新增網站]** 輸入該網域，方案選擇 **Free (免費版)**。
3. **獲取分配的名稱伺服器**：Cloudflare 會自動分配一對專有的權威 Nameservers，例如：
   ```text
   roan.ns.cloudflare.com
   sneh.ns.cloudflare.com
   ```
4. **修改 Porkbun DNS 委派**：進入 Porkbun 的網域管理面板，找到 `Authoritative Nameservers` 設定項，刪除 Porkbun 預設地址，填入 Cloudflare 分配的 2 個伺服器地址並儲存。通常在 5 到 15 分鐘內全球生效。

---

## 3. 第二步：Cloudflare CNAME 扁平化 (Flattening) 與 Full SSL 模式

按照 DNS 國際標準（RFC 1034），根網域（`@`）必須包含 SOA 和 NS 記錄，因此傳統上無法直接配置 `CNAME 記錄`。

Cloudflare 的 **CNAME 扁平化 (CNAME Flattening)** 技術徹底解決了這一痛點：在 DNS 解析查詢時，Cloudflare 邊緣節點會在底層即時解析目標地址（`username.github.io`）對應的 IP，並以 `A 記錄` 的形式直接向客戶端應答，從而讓根網域完美享有 CNAME 的所有敏捷特性。

### A. 配置 Cloudflare DNS 解析記錄
在 Cloudflare 儀表板 **[DNS] > [記錄]** 中，新增以下兩條開啟代理的記錄：

| 類型 (Type) | 名稱 (Name) | 目標 (Target) | 代理狀態 (Proxy status) | TTL |
| :--- | :--- | :--- | :--- | :--- |
| **CNAME** | `@` | `jbjihwan.github.io` | **已代理 (點亮橘色雲朵)** | 自動 |
| **CNAME** | `www` | `jbjihwan.github.io` | **已代理 (點亮橘色雲朵)** | 自動 |

> **必須點亮橘色雲朵**：只有處於代理模式下，造訪流量才會經由 Cloudflare 全球 Anycast 節點接入，享受自動化邊緣 SSL 終結、Brotli 極速壓縮以及抗 DDOS 保護。

### B. 設定 SSL/TLS 加密模式
前往 Cloudflare 左側導覽列 **[SSL/TLS] > [概述]**：
- 將加密模式設為 **Full (完全)** 或 **Full (Strict) (完全嚴格)**；
- 確保從訪客瀏覽器到 Cloudflare、以及從 Cloudflare 到 GitHub Pages 源站的端到端 HTTPS 雙向鏈路均得到高強度加密。

---

## 4. 第三步：更新 Docusaurus 核心配置 (`docusaurus.config.ts`)

當部落格從子目錄路徑（`/global_blog/`）整體遷移至獨立根網域時，必須相應修正 `docusaurus.config.ts`：

```typescript
const config: Config = {
  title: 'Global Dev Blog',
  tagline: 'Engineering Deep Dives in AI, Robotics, Computer Vision',

  // 替換為全新的頂級自訂網域
  url: 'https://globaldevlog.com',
  // 從子目錄 '/global_blog/' 改為頂級根路徑 '/'
  baseUrl: '/',

  organizationName: 'jbjihwan',
  projectName: 'global_blog',
  trailingSlash: false,
  // ...
};
```

---

## 5. 第四步：徹底攻克 GitHub Pages 部署後網域被重設的隱蔽陷阱 (`static/CNAME`)

在配置 GitHub Pages 自訂網域時，幾乎所有開發者都踩過這個著名的“大坑”：
1. 在 GitHub 儲存庫頁面的 `Settings > Pages > Custom domain` 中手動填入 `globaldevlog.com` 並儲存生效；
2. 本地寫完新文章，終端執行 `npm run deploy` 重新部署；
3. 部署一完成，重新整理 GitHub 頁面發現自訂網域輸入框**再次變成了空白**，線上網站瞬間爆出 404 錯誤或 SSL 憑證失效警告！

### 陷阱根源
Docusaurus 的發布指令碼在編譯完成後，會將 `build/` 目錄強制推送到 `gh-pages` 分支（`git push --force`）。如果該打包產物的根目錄下缺少純文字 `CNAME` 檔案，GitHub 會預設判定使用者已主動取消了自訂網域綁定。

### 永久解決方案
在專案的 `static/` 目錄下建立一個名為 `CNAME` 的純文字檔案（無任何副檔名），內容僅寫入一行你的網域：

```text
globaldevlog.com
```

由於 Docusaurus 在建構時會自動將 `static/` 目錄下的所有檔案原封不動複製到打包輸出根目錄，因此每次執行部署時，`CNAME` 檔案都會被永久提交至 `gh-pages` 分支的最頂層，網域綁定永不丟失。

---

## 6. 生產環境連通性驗證

在專案根目錄下執行部署指令：
```bash
npm run deploy
```

部署成功後，在終端機透過 curl 命令驗證 HTTP 狀態碼與 SSL 憑證鏈回應：

```bash
curl -I https://globaldevlog.com
# HTTP/2 200
# server: cloudflare
# strict-transport-security: max-age=31536000

curl -I https://www.globaldevlog.com
# HTTP/2 200 (或 301 重新導向至根網域)
```

---

## 🔜 下篇預告

獨立網域成功上線後，真正的商業化與多引擎搜尋獲客工作才剛剛拉開序幕：
- **第二篇**：*[靜態網站商業化 #2] Docusaurus 接入 Google AdSense 審查實戰：解決 ads.txt 404 爬取故障與非同步指令碼安全植入*
- **第三篇**：*[全球多搜尋引擎 SEO #3] Google、Naver 與 Bing 站長平台權威配置：Sitemap 無法刪除之謎與主機層級報錯排查*

---

### 📌 3~5 行核心總結 (Executive Summary)
1. **零伺服器成本的企業級全端架構**：透過融合成本價網域註冊商 (Porkbun)、全球 Anycast CDN 與 DNS (Cloudflare) 以及零成本靜態代管 (GitHub Pages)，以零維運開銷打造毫秒級全球加速部落格。
2. **藉助 CNAME 扁平化技術突破 RFC 1034 限制**：利用 Cloudflare 的 CNAME Flattening 機制，完美攻克根網域 (`@`) 無法設定別名解析的產業死結，將裸網域平滑直連 GitHub Pages。
3. **Full (Strict) 全鏈路 HTTPS 強加密**：開啟 Cloudflare 嚴格加密模式，實現「訪客 ↔ CDN 邊緣 ↔ GitHub Pages 來源站」的全程雙向 TLS 加密防護。
4. **static/CNAME 實現部署配置永固**：將 `CNAME` 檔案固化在 Docusaurus 的 `static/` 目錄下，徹底杜絕 CI/CD 自動發布時自訂網域被沖刷重設的產業頑疾。
