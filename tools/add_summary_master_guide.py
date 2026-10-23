# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
folder_name = "2026-10-20-custom-domain-adsense-seo-guide"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **Zero-Cost Edge Infrastructure**: Transitioning from free `github.io` to an apex domain via Porkbun, Cloudflare DNS, and GitHub Pages achieves enterprise CDN caching and SSL security at $0 server cost.
2. **CNAME Flattening & Route Canonicalization**: Resolves RFC 1034 apex limitations and canonicalizes `www` to root domain with zero SSL handshake friction or redirect loops.
3. **AdSense Ownership & ads.txt Hardening**: Directly injects publisher verification into static `<head>` and serves `static/ads.txt` from site root, averting crawler 404 traps.
4. **Multi-Engine Search Indexing Triad**: Synchronizes localized sitemaps and RSS feeds across Google Search Console, Naver Search Advisor, and Bing Webmaster Tools with zero host mismatches.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **비용 0원의 고성능 엣지 인프라**: 무료 `github.io`에서 Porkbun, Cloudflare DNS, GitHub Pages 결합 구조로 전환하여 서버 비용 0원으로 글로벌 Anycast 캐싱과 자동 SSL 보안을 구축합니다.
2. **CNAME 평탄화 및 정규 도메인 단일화**: RFC 1034 루트 제약을 Cloudflare CNAME Flattening으로 극복하고 `www` 접속을 apex 도메인으로 매끄럽게 리다이렉트합니다.
3. **애드센스 소유권 및 ads.txt 완벽 방어**: `<head>` 정적 메타태그 삽입과 `static/ads.txt` 루트 배포를 통해 404 크롤링 실패 및 심사 거절을 사전에 방지합니다.
4. **3대 검색엔진(구글·네이버·빙) 동시 색인**: 6개 국어 다국어 사이트맵과 RSS를 구글 서치콘솔, 네이버 서치어드바이저, 빙 웹마스터에 완벽 동기화하여 글로벌 오가닉 트래픽을 극대화합니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **運用費0円の高可用性エッジ基盤**: 無料の `github.io` からPorkbun、Cloudflare DNS、GitHub Pagesの3層構成へ移行し、サーバー費完全ゼロでAnycast配信と常時SSL化を達成します。
2. **CNAME Flattening と正規化ルーティング**: DNSのルート制約をCloudflareの平坦化技術で突破し、`www` からネイキッドドメインへの正規化リダイレクトを安全に統合します。
3. **アドセンス審査と ads.txt の完全対策**: 静的 `<head>` への確認タグ直埋め込みと `static/ads.txt` のルート配信により、クローラーの404エラーや審査脱落を確実に防止します。
4. **3大検索エンジンへの網羅的インデックス**: 多言語サイトマップとRSSフィードをGoogle、Naver、Bingに正確に連携し、ホストエラーを回避してグローバル検索流入を最大化します。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **Infraestructura Edge con Costo Cero de Servidor**: Migrar del subdominio gratuito `github.io` a un dominio apex combinando Porkbun, Cloudflare DNS y GitHub Pages brinda CDN Anycast y SSL sin pagar hosting.
2. **Aplanamiento CNAME y Enrutamiento Canónico**: Supera las restricciones de RFC 1034 para dominios raíz mediante CNAME Flattening, redirigiendo tráfico de `www` al apex de forma transparente.
3. **Verificación de AdSense y Despliegue de ads.txt**: Inserta etiquetas de propiedad en `<head>` y expone `static/ads.txt` en la raíz para garantizar la aprobación sin errores 404 de rastreo.
4. **Indexación Integral en Tres Buscadores**: Sincroniza sitemaps multilingües y canales RSS en Google Search Console, Naver Search Advisor y Bing Webmaster Tools sin fallos de host.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **零成本企业级边缘架构**：告别免费 `github.io` 二级域名，通过 Porkbun、Cloudflare Anycast DNS 与 GitHub Pages 组合，在零服务器账单前提下实现全球加速与全链路 SSL。
2. **CNAME 扁平化与标准域名规范化**：借助 Cloudflare CNAME Flattening 攻克 RFC 1034 根域名解析瓶颈，实现 `www` 向主域名的无缝平滑重定向。
3. **AdSense 验证与 ads.txt 全面护航**：在静态页面 `<head>` 中硬编码所有权元标签并根目录部署 `static/ads.txt`，彻底阻断爬虫 404 抓取失败陷阱。
4. **全球三大搜索引擎全量收录**：将多语言站点地图与 RSS 订阅源同步提交至 Google、Naver 与 Bing 站长平台，规避主机级报错并最大化自然搜索流量。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **零成本企業級邊緣架構**：告別免費 `github.io` 次網域，透過 Porkbun、Cloudflare Anycast DNS 與 GitHub Pages 組合，在零伺服器帳單前提下實現全球加速與全鏈路 SSL。
2. **CNAME 扁平化與標準網域規範化**：藉助 Cloudflare CNAME Flattening 攻克 RFC 1034 根網域解析瓶頸，實現 `www` 向主網域的無縫平滑重定向。
3. **AdSense 驗證與 ads.txt 全面護航**：在靜態頁面 `<head>` 中硬編碼所有權中繼標籤並根目錄部署 `static/ads.txt`，徹底阻斷檢索器 404 檢索失敗陷阱。
4. **全球三大搜尋引擎全量收錄**：將多語言網站地圖與 RSS 訂閱源同步提交至 Google、Naver 與 Bing 站長平台，規避主機級報錯並最大化自然搜尋流量。
"""

def append_summary(file_path, summary_text):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "Executive Summary" in content or "최종 요약" in content or "Resumen Ejecutivo" in content or "核心总结" in content or "核心總結" in content:
        print(f"Summary already present in {file_path}")
        return
    
    new_content = content.rstrip() + "\n\n" + summary_text.strip() + "\n"
    new_content = re.sub(r'---\s*\r?\n\s*---', '---', new_content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Appended summary to: {file_path}")

# Apply to all 6 locales (at bottom of file)
append_summary(f"{gb_root}/blog/{folder_name}/index.md", en_summary)
append_summary(f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md", ko_summary)
append_summary(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_summary)
append_summary(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_summary)
append_summary(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_summary)
append_summary(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_summary)

print("Master guide summary injection finished successfully!")
