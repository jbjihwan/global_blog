# -*- coding: utf-8 -*-
import os
import re

gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-10-20\custom_domain"
folder_name = "2026-10-21-github-pages-custom-domain-cloudflare-dns"

en_summary = """
---

### 📌 3–5 Line Executive Summary
1. **Architectural Cost-Efficiency**: By combining Porkbun (wholesale domain registrar), Cloudflare (enterprise Anycast CDN & DNS), and GitHub Pages (zero-cost static hosting), you achieve enterprise-grade global edge distribution at $0 hosting overhead.
2. **Overcoming RFC 1034 via CNAME Flattening**: Cloudflare resolves the DNS zone apex limitation by dynamically synthesizing pseudo-A records for `@`, allowing clean root domain routing (`https://domain.com`) directly to GitHub Pages.
3. **End-to-End Strict Encryption**: Configuring Cloudflare SSL/TLS to 'Full (Strict)' establishes verified, bidirectional cryptographic protection from the visitor's browser all the way to GitHub's origin servers.
4. **Permanent Deployment Persistence**: Hardcoding `static/CNAME` in Docusaurus and configuring `docusaurus.config.ts` prevents GitHub Pages from resetting your custom domain during automated CI/CD and deploy cycles.
"""

ko_summary = """
---

### 📌 3~5줄 최종 요약 (Executive Summary)
1. **서버 비용 0원의 엔터프라이즈 아키텍처**: 최저가 도메인 등록대행사(Porkbun), 글로벌 Anycast CDN·DNS(Cloudflare), 무료 정적 호스팅(GitHub Pages)을 결합하여 유지비용 없이 기업급 블로그 인프라를 구축합니다.
2. **CNAME Flattening으로 루트 제약 극복**: DNS 표준(RFC 1034)상 루트 도메인(`@`)에 CNAME을 지정할 수 없는 한계를 Cloudflare 평탄화 기술로 해결하여 apex 도메인을 GitHub Pages로 직결합니다.
3. **Full Strict 전 구간 암호화**: Cloudflare SSL 암호화 모드를 'Full (Strict)'로 지정하여 방문자-Cloudflare 구간뿐 아니라 Cloudflare-GitHub Pages 오리진 구간까지 완벽한 HTTPS 보안을 적용합니다.
4. **static/CNAME 영구 고정**: Docusaurus의 `static/CNAME` 파일 배치 및 설정 파일 업데이트를 통해 `npm run deploy` 시 도메인 연결이 초기화되는 배포 유실 문제를 완벽히 차단합니다.
"""

ja_summary = """
---

### 📌 3〜5行のエグゼクティブサマリー (Executive Summary)
1. **サーバー費用ゼロのエンタープライズ構成**: 卸値ドメインレジストラ(Porkbun)、Anycast CDN・DNS(Cloudflare)、無料静的ホスティング(GitHub Pages)を組み合わせ、運用費ゼロで世界最高峰のエッジ配信網を実現します。
2. **CNAME Flattening によるルート制限の克服**: DNS標準(RFC 1034)で禁止されているルートドメイン(`@`)へのCNAME割り当てをCloudflare平坦化技術で解決し、直接GitHub Pagesへ紐付けます。
3. **Full Strict による完全な通信暗号化**: CloudflareのSSLモードを「Full (Strict)」に設定することで、訪問者〜CDN間だけでなくCDN〜GitHub Pagesオリジン間も強固なHTTPS暗号化を確立します。
4. **static/CNAME によるデプロイ永続化**: Docusaurusの `static/CNAME` 配置と設定ファイル更新により、デプロイ時にカスタムドメイン設定が初期化・消失するトラブルを恒久的に防ぎます。
"""

es_summary = """
---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **Arquitectura Empresarial con Costo Cero de Servidor**: La combinación de Porkbun (registro al costo), Cloudflare (Anycast CDN y DNS global) y GitHub Pages (alojamiento estático gratuito) ofrece infraestructura de alto rendimiento sin costes operativos.
2. **Superación del Límite RFC 1034 con CNAME Flattening**: Resuelve la restricción técnica de asignar CNAMEs en el dominio raíz (`@`) mediante la técnica de aplanamiento de Cloudflare, conectando el apex directamente a GitHub Pages.
3. **Cifrado Extremo a Extremo en Modo Full (Strict)**: Establece túneles HTTPS seguros tanto entre el visitante y Cloudflare como entre Cloudflare y los servidores de origen de GitHub Pages.
4. **Persistencia Garantizada con static/CNAME**: Alojar el archivo `CNAME` en el directorio `static/` de Docusaurus evita que los despliegues automatizados eliminen la configuración del dominio personalizado.
"""

zh_hans_summary = """
---

### 📌 3~5 行核心总结 (Executive Summary)
1. **零服务器成本的企业级全栈架构**：通过融合成本价域名注册商 (Porkbun)、全球 Anycast CDN 与 DNS (Cloudflare) 以及零成本静态托管 (GitHub Pages)，以零运维开销打造毫秒级全球加速博客。
2. **借助 CNAME 扁平化技术突破 RFC 1034 限制**：利用 Cloudflare 的 CNAME Flattening 机制，完美攻克根域名 (`@`) 无法配置别名解析的行业死结，将裸域名平滑直连 GitHub Pages。
3. **Full (Strict) 全链路 HTTPS 强加密**：开启 Cloudflare 严格加密模式，实现“访客 ↔ CDN 边缘 ↔ GitHub Pages 源站”的全程双向 TLS 加密防护。
4. **static/CNAME 实现部署配置永固**：将 `CNAME` 文件固化在 Docusaurus 的 `static/` 目录下，彻底杜绝 CI/CD 自动发布时自定义域名被冲刷重置的行业顽疾。
"""

zh_hant_summary = """
---

### 📌 3~5 行核心總結 (Executive Summary)
1. **零伺服器成本的企業級全端架構**：透過融合成本價網域註冊商 (Porkbun)、全球 Anycast CDN 與 DNS (Cloudflare) 以及零成本靜態代管 (GitHub Pages)，以零維運開銷打造毫秒級全球加速部落格。
2. **藉助 CNAME 扁平化技術突破 RFC 1034 限制**：利用 Cloudflare 的 CNAME Flattening 機制，完美攻克根網域 (`@`) 無法設定別名解析的產業死結，將裸網域平滑直連 GitHub Pages。
3. **Full (Strict) 全鏈路 HTTPS 強加密**：開啟 Cloudflare 嚴格加密模式，實現「訪客 ↔ CDN 邊緣 ↔ GitHub Pages 來源站」的全程雙向 TLS 加密防護。
4. **static/CNAME 實現部署配置永固**：將 `CNAME` 檔案固化在 Docusaurus 的 `static/` 目錄下，徹底杜絕 CI/CD 自動發布時自訂網域被沖刷重設的產業頑疾。
"""

nb_summary = """
---

## 📌 3~5줄 최종 요약
1. **서버비 0원 인프라**: Porkbun(도메인), Cloudflare(DNS/CDN), GitHub Pages(호스팅) 조합으로 유지비 0원에 엔터프라이즈급 개발 블로그를 운영합니다.
2. **CNAME 평탄화(Flattening)**: RFC 표준상 루트 도메인에 CNAME을 달 수 없는 문제를 Cloudflare 기술로 해결하여 apex 도메인을 직결합니다.
3. **Full Strict 전 구간 보안**: Cloudflare SSL을 Full Strict 모드로 설정하여 방문자부터 GitHub 오리진까지 안전한 HTTPS 암호화를 적용합니다.
4. **static/CNAME 영구 배포**: Docusaurus `static/CNAME`에 도메인을 넣어 배포할 때마다 도메인 연결이 풀리는 문제를 영구적으로 해결합니다.
"""

def append_summary(file_path, summary_text, ref_marker=None):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "Executive Summary" in content or "최종 요약" in content or "Resumen Ejecutivo" in content or "核心总结" in content or "核心總結" in content:
        print(f"Summary already present in {file_path}")
        return
    
    if ref_marker and ref_marker in content:
        parts = content.split(ref_marker, 1)
        new_content = parts[0].rstrip() + "\n" + summary_text.strip() + "\n\n" + ref_marker + parts[1]
    else:
        new_content = content.rstrip() + "\n" + summary_text.strip() + "\n"
        
    # Clean double hr
    new_content = re.sub(r'---\s*\r?\n\s*---', '---', new_content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Appended summary to: {file_path}")

# Apply to all 6 locales (at end of file)
append_summary(f"{gb_root}/blog/{folder_name}/index.md", en_summary)
append_summary(f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md", ko_summary)
append_summary(f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md", ja_summary)
append_summary(f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md", es_summary)
append_summary(f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hans_summary)
append_summary(f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md", zh_hant_summary)

# Apply to Naver Blog (before the bottom link)
append_summary(f"{nb_root}/post.md", nb_summary, "> 📌 **상세 기술 스택 & 4개 언어 글로벌 라이브 아티클 보러가기**:")

print("Custom domain guide summary injection finished successfully!")
