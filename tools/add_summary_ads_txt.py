# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-10-21\adsense_ads_txt"
folder_name = "2026-10-21-static-site-adsense-ads-txt-guide"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **Static Site Ownership Verification**: Bypassing client-side hydration delays, inject the AdSense publisher verification meta tag directly into `<head>` via Docusaurus `headTags` for instantaneous crawler detection.
2. **Eliminating the ads.txt 404 Crawl Trap**: Placing `ads.txt` in the root `static/` directory ensures it is deployed directly to `https://domain.com/ads.txt`, permanently preventing the "Earnings at Risk" penalty.
3. **Cloudflare WAF Bot Bypass**: Configure Cloudflare custom WAF rules to skip Managed Challenge on `Googlebot-AdsTxt` and `Mediapartners-Google`, averting false-positive CAPTCHA crawl dropouts.
4. **4-Pillar AdSense Review Readiness**: Guarantee first-attempt approval by establishing statutory privacy/about/contact pages, maintaining zero 404 broken links, and offering 20+ comprehensive technical articles.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **정적 사이트 소유권 메타태그 주입**: 클라이언트 사이드 하이드레이션 지연을 피하기 위해 Docusaurus `headTags` 설정을 통해 애드센스 소유권 확인 태그를 `<head>`에 직접 정적으로 삽입합니다.
2. **ads.txt 404 크롤링 누락 방지**: `static/ads.txt`에 게시자 ID를 배치하여 루트 경로(`https://도메인/ads.txt`)로 직접 배포되도록 구성함으로써 '수익 손실 위험' 경고를 원천 차단합니다.
3. **Cloudflare WAF 봇 바이패스**: Cloudflare 보안 설정에서 `Googlebot-AdsTxt`와 `Mediapartners-Google`에 대해 봇 챌린지(CAPTCHA)를 건너뛰는 바이패스 규칙을 등록해야 크롤링 실패를 막을 수 있습니다.
4. **애드센스 원패스 4대 기준**: 개인정보처리방침/소개/문의 필수 페이지 완비, 20편 이상의 심화 기술 포스트, 깨진 링크(404) 0건, 완벽한 모바일 반응형 뷰포트를 갖추어야 거절 없이 승인됩니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **静的サイトの所有権確認メタタグ注入**: クライアント側のハイドレーション遅延を排除するため、Docusaurusの `headTags` 設定を用いて `<head>` 直下に所有権確認メタタグを直接静的出力します。
2. **ads.txt 404クロールエラーの完全防止**: ルートの `static/ads.txt` にパブリッシャー情報を配置し、`https://ドメイン/ads.txt` で即座に配信されるようにすることで「収益の危険」警告を未然に防ぎます。
3. **Cloudflare WAF によるボットバイパス**: `Googlebot-AdsTxt` や `Mediapartners-Google` に対し、Cloudflareのボットチャレンジ（CAPTCHA）をスキップする許可ルールを設定しクローラー遮断を回避します。
4. **アドセンス一発合格のための4大基準**: プライバシーポリシー・運営者情報・お問い合わせページの完備、20本以上の独自技術記事、404リンクのゼロ化、モバイル最適化を完了して審査に臨む必要があります。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **Verificación Estática de Propiedad**: Inyecta la metaetiqueta de verificación de Google AdSense directamente en `<head>` mediante la configuración `headTags` de Docusaurus, evitando retrasos de hidratación en el cliente.
2. **Solución al Error 404 en ads.txt**: Ubicar `ads.txt` dentro del directorio `static/` garantiza su despliegue en la raíz (`https://dominio/ads.txt`), eliminando permanentemente la alerta de "Ingresos en riesgo".
3. **Bypass del WAF en Cloudflare**: Configura reglas de omisión en Cloudflare para que los rastreadores `Googlebot-AdsTxt` y `Mediapartners-Google` no sean bloqueados por desafíos de CAPTCHA automatizados.
4. **Los 4 Pilares de Aprobación Inmediata**: Disponer de páginas estatutarias (política de privacidad, contacto), más de 20 artículos técnicos originales, cero enlaces rotos (404) y diseño móvil responsivo garantizan el éxito en la revisión.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **静态网站所有权验证标签注入**：规避客户端 Hydration 渲染延迟，直接通过 Docusaurus 的 `headTags` 配置将 AdSense 验证元标签硬编码注入 `<head>`，确保爬虫瞬时捕获。
2. **根除 ads.txt 404 抓取陷阱**：将发布商凭据置于根目录 `static/ads.txt`，保障其直达 `https://域名/ads.txt`，彻底消除“收益存在风险”惩罚警告。
3. **Cloudflare WAF 爬虫白名单放行**：针对 `Googlebot-AdsTxt` 与 `Mediapartners-Google` 配置专属 WAF 绕过规则，防止 Bot Fight Mode 误触发人机验证拦截抓取。
4. **一次性过审的 4 大黄金标准**：健全隐私政策/关于/联系页面、储备 20 篇以上原创深度技术长文、保持 404 死链率为零，并确保极致的移动端自适应排版。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **靜態網站所有權驗證標籤注入**：規避用戶端 Hydration 渲染延遲，直接透過 Docusaurus 的 `headTags` 設定將 AdSense 驗證中繼標籤硬編碼注入 `<head>`，確保檢索器瞬時捕獲。
2. **根除 ads.txt 404 檢索陷阱**：將發布商憑證置於根目錄 `static/ads.txt`，保障其直達 `https://網域/ads.txt`，徹底消除「收益面臨風險」懲罰警告。
3. **Cloudflare WAF 檢索器白名單放行**：針對 `Googlebot-AdsTxt` 與 `Mediapartners-Google` 設定專屬 WAF 繞過規則，防止 Bot Fight Mode 誤觸發人機驗證攔截檢索。
4. **一次性過審的 4 大黃金標準**：健全隱私權政策/關於/聯絡頁面、儲備 20 篇以上原創深度技術長文、保持 404 死鏈率為零，並確保極致的行動裝置自適應排版。
"""

nb_summary = """
---

## 📌 3~5줄 최종 요약
1. **정적 사이트 소유권 태그 주입**: Docusaurus `headTags` 설정을 통해 `<head>`에 소유권 확인 태그를 직접 삽입하여 크롤러 인식 지연을 방지합니다.
2. **ads.txt 404 오류 차단**: `static/ads.txt`에 파일을 넣어 루트 경로로 바로 배포되게 함으로써 '수익 손실 위험' 경고를 사전에 차단합니다.
3. **Cloudflare WAF 예외 처리**: 구글 ads.txt 크롤러(`Googlebot-AdsTxt`)가 봇 챌린지 캡차에 걸리지 않도록 WAF 바이패스 규칙을 등록합니다.
4. **애드센스 원패스 준비**: 개인정보처리방침/소개 페이지 완비, 고품질 기술 글 20편 이상, 깨진 링크 0건, 모바일 최적화를 완료하고 심사를 신청합니다.
"""

def append_summary(file_path, summary_text, ref_marker):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "Executive Summary" in content or "최종 요약" in content or "Resumen Ejecutivo" in content or "核心总结" in content or "核心總結" in content:
        print(f"Summary already present in {file_path}")
        return
    
    if ref_marker in content:
        parts = content.split(ref_marker, 1)
        new_content = parts[0].rstrip() + "\n" + summary_text.strip() + "\n\n" + ref_marker + parts[1]
    else:
        new_content = content.rstrip() + "\n" + summary_text.strip() + "\n"
        
    # Clean double hr
    new_content = re.sub(r'---\s*\r?\n\s*---', '---', new_content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Appended summary to: {file_path}")

# Apply to all 6 locales
append_summary(f"{gb_root}/blog/{folder_name}/index.md", en_summary, "> 📌 **Explore the Production Implementation**:")
append_summary(f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md", ko_summary, "> 📌 **프로덕션 라이브 구현체 살펴보기**:")
append_summary(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_summary, "> 📌 **Global Dev Blog の関連記事**:")
append_summary(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_summary, "> 📌 **Artículos Relacionados en Global Dev Blog**:")
append_summary(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_summary, "> 📌 **Global Dev Blog 精选技术推荐**：")
append_summary(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_summary, "> 📌 **Global Dev Blog 精選技術推薦**：")

# Apply to Naver Blog
append_summary(f"{nb_root}/post.md", nb_summary, "> 📌 **함께 읽으면 좋은 글로벌 개발 블로그 글**:")

print("Ads.txt guide summary injection finished successfully!")
