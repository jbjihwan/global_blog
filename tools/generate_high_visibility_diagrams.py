#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master High-Visibility Diagram Generator for Global Dev Blog
Renders large, bold, crystal-clear typography across all 6 locales:
[en, ko, ja, es, zh-Hans, zh-Hant]

Diagrams Covered:
1. 01_threat_model.png (2026-10-18-static-site-security-hardening)
2. 02_security_pipeline.png (2026-10-18-static-site-security-hardening)
3. 01_dns_routing_architecture.png (2026-10-20-custom-domain & 2026-10-21-github-pages-custom-domain)
4. 02_indexing_pipeline.png (2026-10-20-custom-domain-adsense-seo-guide)
5. 01_ads_txt_crawler_flow.png (2026-10-21-static-site-adsense-ads-txt-guide)
6. 01_pipeline_diagram.png (2026-06-25-vision-anpr-1)
7. 02_architecture.png (2026-05-17-rl-qlearning-1)
8. 02_presentation.png (2026-06-18-maeumjigi-23 - Safety Wrapper Flowchart)
9. 01_cover.png (Maeumjigi slide summary cards for episodes 3, 4, 5, 6, 7, 8, 19, 23)
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BLOG_ROOT = r"D:\ai\antigravity\global_blog"

LOCALES = {
    "en": os.path.join(BLOG_ROOT, "blog"),
    "ko": os.path.join(BLOG_ROOT, "i18n", "ko", "docusaurus-plugin-content-blog"),
    "ja": os.path.join(BLOG_ROOT, "i18n", "ja", "docusaurus-plugin-content-blog"),
    "es": os.path.join(BLOG_ROOT, "i18n", "es", "docusaurus-plugin-content-blog"),
    "zh-Hans": os.path.join(BLOG_ROOT, "i18n", "zh-Hans", "docusaurus-plugin-content-blog"),
    "zh-Hant": os.path.join(BLOG_ROOT, "i18n", "zh-Hant", "docusaurus-plugin-content-blog"),
}

FONT_FAMILIES = {
    "ko": "Malgun Gothic",
    "ja": "MS Gothic",
    "zh-Hans": "Microsoft YaHei",
    "zh-Hant": "Microsoft JhengHei",
    "en": "Segoe UI",
    "es": "Segoe UI",
}

# ==============================================================================
# 1. THREAT MODELING (01_threat_model.png)
# ==============================================================================
THREAT_TEXTS = {
    "en": {
        "title": "Threat Modeling: Dynamic Server vs Static Site Generation (SSG)",
        "subtitle": "Security Boundary & Attack Surface Comparison",
        "left_title": "[VULNERABLE] Dynamic Server (Node / Django)",
        "left_desc": (
            "• Active Listening Ports: Always open (80/443)\n"
            "• Database Layer: Direct SQL Injection & Auth risks\n"
            "• Runtime Execution: Remote Code Execution (RCE)\n"
            "• OS Vulnerabilities: Server memory exhaustion / DoS\n"
            "• npm Packages: Live exploit execution in production"
        ),
        "right_title": "[SECURE] Static Site (GitHub Pages CDN)",
        "right_desc": (
            "• Pre-compiled Assets: 100% pure HTML, CSS, and JS\n"
            "• No Running Server: Zero backend Node/Python process\n"
            "• No Database Ports: SQL injection attack surface = 0%\n"
            "• Immune to Server RCE: Static edge delivery via CDN\n"
            "• npm Audit: Dev-only bundler scope, zero runtime risk"
        ),
    },
    "ko": {
        "title": "위협 모델링: 동적 웹 서버 vs 정적 사이트 생성(SSG) 보안 비교",
        "subtitle": "아키텍처별 공격 표면(Attack Surface) 및 런타임 침해 위협 분석",
        "left_title": "[위협 노출] 동적 웹 서버 (Node.js / Django)",
        "left_desc": (
            "• 24시간 상시 대기 포트: 외부 침투 경로 항시 노출 (80/443)\n"
            "• 데이터베이스 계층: SQL 인젝션 및 인증 토큰 탈취 위험\n"
            "• 런타임 템플릿 실행: 원격 코드 실행(RCE) 침해 가능성\n"
            "• 서버 리소스 착취: 메모리 고갈 및 분산 서비스 거부(DoS)\n"
            "• npm 취약 패키지: 프로덕션 런타임에서 실시간 공격 체결"
        ),
        "right_title": "[보안 격리] 정적 사이트 (GitHub Pages CDN)",
        "right_desc": (
            "• 빌드 시점 사전 컴파일: 순수 정적 파일(HTML/CSS/JS) 제공\n"
            "• 상시 서버 프로세스 전무: 공격 가능한 백엔드 데몬 부재\n"
            "• 데이터베이스 포트 없음: SQL 인젝션 공격 표면 0%\n"
            "• 서버 사이드 RCE 완전 차단: 글로벌 엣지 CDN 읽기 전용\n"
            "• npm audit 취약점 경고: 번들러 도구 한정, 런타임 위험 0%"
        ),
    },
    "ja": {
        "title": "脅威モデリング: 動的サーバー vs 静的サイト生成(SSG)のセキュリティ比較",
        "subtitle": "アーキテクチャ別の攻撃対象領域(Attack Surface)と侵害リスク分析",
        "left_title": "[脆弱] 動的サーバー (Node.js / Django)",
        "left_desc": (
            "• 24時間常時待受ポート: 外部侵入経路が常に露出 (80/443)\n"
            "• データベース層: SQLインジェクションおよび認証奪取リスク\n"
            "• 動的テンプレート実行: リモートコード実行(RCE)の脅威\n"
            "• サーバーリソース枯渇: メモリ悪用およびDoS攻撃への脆弱性\n"
            "• npm脆弱性: 本番ランタイムにおける実害エクスプロイト"
        ),
        "right_title": "[強固] 静的サイト (GitHub Pages CDN)",
        "right_desc": (
            "• ビルド時事前コンパイル: 純粋な静的ファイル(HTML/CSS/JS)\n"
            "• 常時稼働プロセス皆無: 攻撃可能なバックエンドデーモン不在\n"
            "• DBポート完全非露出: SQLインジェクション攻撃対象 0%\n"
            "• サーバーRCE根本遮断: グローバルエッジCDNによる読取専用\n"
            "• npm audit警告: ビルド時ツールに限定、実行時リスク 0%"
        ),
    },
    "es": {
        "title": "Modelado de Amenazas: Servidor Dinámico vs Sitio Estático (SSG)",
        "subtitle": "Comparación de Superficie de Ataque y Seguridad en Producción",
        "left_title": "[VULNERABLE] Servidor Dinámico (Node.js / Django)",
        "left_desc": (
            "• Puertos Abiertos 24/7: Exposición continua (80/443)\n"
            "• Capa de Base de Datos: Riesgos de Inyección SQL y Auth\n"
            "• Ejecución Dinámica: Ejecución Remota de Código (RCE)\n"
            "• Vulnerabilidades del SO: Agotamiento de memoria y DoS\n"
            "• Paquetes npm: Explotación directa en tiempo de ejecución"
        ),
        "right_title": "[PROTEGIDO] Sitio Estático (GitHub Pages CDN)",
        "right_desc": (
            "• Archivos Precompilados: 100% HTML, CSS y JS puro\n"
            "• Sin Servidor en Ejecución: Cero procesos Node en producción\n"
            "• Sin Puertos de BD: Superficie de ataque SQLi = 0%\n"
            "• Inmune a RCE de Servidor: Entrega estática de solo lectura\n"
            "• npm audit: Limitado al empaquetador, riesgo en runtime = 0%"
        ),
    },
    "zh-Hans": {
        "title": "威胁建模：动态服务器 vs 静态站点生成 (SSG) 安全对比",
        "subtitle": "架构级攻击面 (Attack Surface) 与运行时风险深度剖析",
        "left_title": "[高危暴露] 传统动态服务器 (Node.js / Django)",
        "left_desc": (
            "• 24小时常开监听端口：外部攻击面持续暴露 (80/443)\n"
            "• 数据库交互层：面临 SQL 注入及鉴权凭证泄露风险\n"
            "• 运行时模板执行：存在远程代码执行 (RCE) 漏洞\n"
            "• 操作系统资源剥夺：易遭受内存耗尽与拒绝服务攻击 (DoS)\n"
            "• npm 依赖漏洞：生产环境运行时面临真实利用威胁"
        ),
        "right_title": "[安全加固] 现代静态站点 (GitHub Pages CDN)",
        "right_desc": (
            "• 构建时预编译：100% 纯静态文件 (HTML/CSS/JS) 交付\n"
            "• 无后台驻留进程：不存在可被渗透的 Node/Python 守护进程\n"
            "• 彻底隔离数据库端口：SQL 注入攻击暴露面为 0%\n"
            "• 免疫服务端 RCE 漏洞：全球 Anycast 边缘 CDN 只读访问\n"
            "• npm audit 告警：仅局限于打包工具链，运行时风险为 0%"
        ),
    },
    "zh-Hant": {
        "title": "威脅建模：動態伺服器 vs 靜態網站生成 (SSG) 安全評估",
        "subtitle": "架構級攻擊面 (Attack Surface) 與運行時風險深度剖析",
        "left_title": "[高危暴露] 傳統動態伺服器 (Node.js / Django)",
        "left_desc": (
            "• 24小時常開監聽埠：外部攻擊面持續暴露 (80/443)\n"
            "• 資料庫交互層：面臨 SQL 注入及鑑權憑證洩漏風險\n"
            "• 運行時模板執行：存在遠端程式碼執行 (RCE) 漏洞\n"
            "• 作業系統資源剝奪：易遭受記憶體耗盡與拒絕服務攻擊 (DoS)\n"
            "• npm 依賴漏洞：生產環境運行時面臨真實利用威脅"
        ),
        "right_title": "[安全加固] 現代靜態網站 (GitHub Pages CDN)",
        "right_desc": (
            "• 構建時預編譯：100% 純靜態檔案 (HTML/CSS/JS) 交付\n"
            "• 無後台駐留進程：不存在可被滲透的 Node/Python 守護進程\n"
            "• 徹底隔離資料庫埠：SQL 注入攻擊暴露面為 0%\n"
            "• 免疫伺服端 RCE 漏洞：全球 Anycast 邊緣 CDN 唯讀存取\n"
            "• npm audit 告警：僅局限於打包工具鏈，運行時風險為 0%"
        ),
    },
}

def render_threat_model_high_vis():
    print("\n--- Rendering High-Visibility Threat Model Diagrams (All 6 Locales) ---")
    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-10-18-static-site-security-hardening", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = THREAT_TEXTS[loc]

        fig, ax = plt.subplots(figsize=(13, 7.5), dpi=150)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(6.5, 6.9, data["title"], color='#ffffff', fontsize=18, fontweight='bold', ha='center')
        ax.text(6.5, 6.45, data["subtitle"], color='#38bdf8', fontsize=13, fontweight='bold', ha='center')

        rect_left = patches.FancyBboxPatch((0.6, 0.8), 5.6, 5.2, boxstyle="round,pad=0.25",
                                           linewidth=2.5, edgecolor='#ef4444', facecolor='#1e293b')
        ax.add_patch(rect_left)
        ax.text(3.4, 5.5, data["left_title"], color='#fca5a5', fontsize=15.0, fontweight='bold', ha='center')
        ax.plot([1.2, 5.6], [5.2, 5.2], color='#ef4444', linewidth=1.5)
        ax.text(1.1, 4.8, data["left_desc"], color='#f1f5f9', fontsize=13,
                fontweight='medium', ha='left', va='top', linespacing=1.65)

        rect_right = patches.FancyBboxPatch((6.8, 0.8), 5.6, 5.2, boxstyle="round,pad=0.25",
                                            linewidth=2.5, edgecolor='#10b981', facecolor='#1e293b')
        ax.add_patch(rect_right)
        ax.text(9.6, 5.5, data["right_title"], color='#6ee7b7', fontsize=15.0, fontweight='bold', ha='center')
        ax.plot([7.4, 11.8], [5.2, 5.2], color='#10b981', linewidth=1.5)
        ax.text(7.3, 4.8, data["right_desc"], color='#f1f5f9', fontsize=13,
                fontweight='medium', ha='left', va='top', linespacing=1.65)

        ax.set_xlim(0, 13)
        ax.set_ylim(0.4, 7.4)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "01_threat_model.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered high-visibility: {out_path}")


# ==============================================================================
# 2. SECURITY PIPELINE (02_security_pipeline.png)
# ==============================================================================
SECURITY_PIPELINE_TEXTS = {
    "en": {
        "title": "4-Layer Static Blog Security Hardening Pipeline",
        "steps": [
            ("1. Git Secret Scanning", "Regex detection for API keys,\nPAT tokens & certificates", "#38bdf8"),
            ("2. PII Protection", "Phone numbers, resident IDs,\nand team member privacy", "#818cf8"),
            ("3. Supply Chain Audit", "Rational triage of npm audit\nwithout breaking build integrity", "#fbbf24"),
            ("4. Client Privacy", "Strict Referrer Policy, Giscus\niframe sandboxing & .gitignore", "#34d399"),
        ]
    },
    "ko": {
        "title": "정적 블로그 4단계 심층 보안 강화 파이프라인",
        "steps": [
            ("1. 시크릿 유출 스캔", "API 키, PAT 토큰, 인증서\n정규식 패턴 자동 검출 및 차단", "#38bdf8"),
            ("2. 개인정보(PII) 격리", "전화번호, 주민등록번호, 팀원 실명\n민감 정보 사전 마스킹 필터링", "#818cf8"),
            ("3. 공급망(npm) 검토", "npm audit fix 무차별 적용 배제\n런타임 영향도 기반 이성적 분류", "#fbbf24"),
            ("4. 클라이언트 프라이버시", "엄격한 Referrer Policy 적용\nGiscus iframe 격리 및 .gitignore 강화", "#34d399"),
        ]
    },
    "ja": {
        "title": "静的ブログ 4段階 多層セキュリティ強化パイプライン",
        "steps": [
            ("1. シークレット検知", "APIキー、PATトークン、認証情報\n正規表現パターンによる自動遮断", "#38bdf8"),
            ("2. 個人情報(PII)保護", "電話番号・身元情報・チーム実名\n機密情報の自動マスキング除去", "#818cf8"),
            ("3. サプライチェーン監査", "npm audit fix の盲信・破壊を防止\n実行時影響度に基づく論理的トリアージ", "#fbbf24"),
            ("4. クライアント保護", "厳格なReferrer Policyポリシー適用\nGiscus iframeサンドボックス化", "#34d399"),
        ]
    },
    "es": {
        "title": "Pipeline de Blindaje de Seguridad en 4 Capas para Sitios Estáticos",
        "steps": [
            ("1. Escaneo de Secretos", "Detección Regex de API keys,\ntokens PAT y certificados", "#38bdf8"),
            ("2. Protección de PII", "Validación estricta de teléfonos\ny datos personales sensibles", "#818cf8"),
            ("3. Auditoría de Cadena", "Triaje racional de npm audit\nsin comprometer la compilación", "#fbbf24"),
            ("4. Privacidad del Cliente", "Referrer Policy estricta, Giscus\nsandbox iframe y .gitignore", "#34d399"),
        ]
    },
    "zh-Hans": {
        "title": "静态博客 4 级纵深安全防护流水线",
        "steps": [
            ("1. 敏感凭证扫描", "API Key、PAT 令牌与数字证书\n正则特征模式自动化拦截", "#38bdf8"),
            ("2. 隐私数据 (PII) 隔离", "电话号码、身份证件与团队实名\n敏感信息预编译脱敏过滤", "#818cf8"),
            ("3. 软件供应链审计", "理性评估 npm audit 漏洞告警\n杜绝盲目修复导致构建损坏", "#fbbf24"),
            ("4. 客户端隐私加固", "配置严格 Referrer Policy 策略\nGiscus iframe 沙箱隔离保护", "#34d399"),
        ]
    },
    "zh-Hant": {
        "title": "靜態網站 4 級縱深安全防護流水線",
        "steps": [
            ("1. 敏感憑證掃描", "API Key、PAT 權杖與數位憑證\n正則特徵模式自動化攔截", "#38bdf8"),
            ("2. 隱私數據 (PII) 隔離", "電話號碼、身分證件與團隊實名\n敏感資訊預編譯去識別化過濾", "#818cf8"),
            ("3. 軟體供應鏈審計", "理性評估 npm audit 漏洞告警\n杜絕盲目修復導致構建損壞", "#fbbf24"),
            ("4. 客戶端隱私加固", "配置嚴格 Referrer Policy 策略\nGiscus iframe 沙箱隔離保護", "#34d399"),
        ]
    },
}

def render_security_pipeline_high_vis():
    print("\n--- Rendering High-Visibility Security Pipeline Diagrams (All 6 Locales) ---")
    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-10-18-static-site-security-hardening", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = SECURITY_PIPELINE_TEXTS[loc]

        fig, ax = plt.subplots(figsize=(14, 6.5), dpi=150)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(7.0, 5.8, data["title"], color='#ffffff', fontsize=18, fontweight='bold', ha='center')

        for i, (title, desc, col) in enumerate(data["steps"]):
            x = 0.5 + i * 3.3
            rect = patches.FancyBboxPatch((x, 1.0), 3.0, 4.2, boxstyle="round,pad=0.2",
                                          linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + 1.5, 4.6, title, color=col, fontsize=14, fontweight='bold', ha='center')
            ax.plot([x + 0.3, x + 2.7], [4.2, 4.2], color=col, linewidth=1.5)
            ax.text(x + 1.5, 2.7, desc, color='#f1f5f9', fontsize=12.5,
                    fontweight='medium', ha='center', va='center', linespacing=1.5)

            if i < 3:
                arrow = patches.FancyArrowPatch((x + 3.1, 3.1), (x + 3.4, 3.1),
                                               arrowstyle='->', mutation_scale=20, color='#94a3b8', linewidth=2.5)
                ax.add_patch(arrow)

        ax.set_xlim(0, 14)
        ax.set_ylim(0.5, 6.4)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "02_security_pipeline.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered high-visibility: {out_path}")


# ==============================================================================
# 3. DNS ROUTING (01_dns_routing_architecture.png)
# ==============================================================================
DNS_TEXTS = {
    "en": {
        "title": "Production DNS & CDN Routing Architecture for Static Engineering Blog",
        "boxes": [
            ("1. Domain Registrar\n(Porkbun)", "- Custom Domain: globaldevlog.com\n- Free WHOIS Privacy Guard\n- Authoritative Nameserver (NS)\n  Delegated to Cloudflare", "#38bdf8"),
            ("2. Cloudflare Edge DNS\n& Security Shield", "- CNAME Flattening (@ Apex -> GitHub)\n- CNAME www -> Apex Domain\n- Global Anycast CDN Caching\n- Automatic Universal SSL (HTTPS)\n- DDoS & Bot Protection Shield", "#f59e0b"),
            ("3. GitHub Pages Origin\n(Docusaurus SSG)", "- static/CNAME: globaldevlog.com\n- Pre-compiled Multilingual HTML\n- 6 Independent Locales Active\n- Zero Server Infrastructure Cost\n- High Availability Edge Delivery", "#10b981")
        ]
    },
    "ko": {
        "title": "글로벌 정적 엔지니어링 블로그 DNS 및 CDN 라우팅 아키텍처",
        "boxes": [
            ("1. 도메인 등록기관\n(Porkbun)", "• 커스텀 도메인: globaldevlog.com\n• 무료 WHOIS 개인정보 보호\n• 공인 네임서버(NS) 위임:\n  Cloudflare Anycast 네임서버 지정", "#38bdf8"),
            ("2. Cloudflare Edge DNS\n& 보안 보호막", "• CNAME 플래트닝 (@ 루트 도메인 연동)\n• CNAME www -> 루트 도메인 포워딩\n• 전 세계 Anycast CDN 초고속 캐싱\n• 자동 유니버설 SSL 인증서 (HTTPS)\n• DDoS 및 악성 봇 차단 보호막", "#f59e0b"),
            ("3. GitHub Pages 오리진\n(Docusaurus SSG)", "• static/CNAME 파일: 도메인 바인딩\n• 사전 컴파일된 다국어 정적 빌드\n• 6개 국어 완전 독립 서빙\n• 서버 호스팅 및 인프라 비용 $0\n• 99.99% 고가용성 글로벌 전송", "#10b981")
        ]
    },
    "ja": {
        "title": "グローバル静的ブログ DNS＆CDNルーティング・アーキテクチャ",
        "boxes": [
            ("1. レジストラ\n(Porkbun)", "• 独自ドメイン: globaldevlog.com\n• 無料WHOISプライバシー保護\n• ネームサーバー(NS)委任:\n  Cloudflare Anycast NS設定", "#38bdf8"),
            ("2. Cloudflare Edge DNS\n＆ セキュリティ防御", "• CNAMEフラット化 (@ルート解決)\n• CNAME www転送設定\n• 全世界Anycast CDN高速キャッシュ\n• 自動ユニバーサルSSL (HTTPS)\n• DDoSおよび不正ボット遮断", "#f59e0b"),
            ("3. GitHub Pages オリジン\n(Docusaurus SSG)", "• static/CNAME による確実なバインド\n• 事前コンパイルされた多言語HTML\n• 6言語の完全独立配信\n• サーバー維持インフラ費用 0円\n• 99.99%高可用性エッジ配信", "#10b981")
        ]
    },
    "es": {
        "title": "Arquitectura de Enrutamiento DNS y CDN para Blog Estático",
        "boxes": [
            ("1. Registrador\n(Porkbun)", "• Dominio: globaldevlog.com\n• Privacidad WHOIS gratuita\n• Delegación de NS autoritativo\n  hacia Anycast Cloudflare", "#38bdf8"),
            ("2. Cloudflare Edge DNS\n& Capa de Seguridad", "• Aplanamiento CNAME (@ -> GitHub)\n• CNAME www hacia dominio raíz\n• Caché Anycast CDN Global\n• Certificado SSL Universal (HTTPS)\n• Escudo Anti-DDoS y Bots", "#f59e0b"),
            ("3. GitHub Pages Origen\n(Docusaurus SSG)", "• Archivo static/CNAME verificado\n• HTML multilingüe precompilado\n• 6 idiomas completamente activos\n• Cero coste de infraestructura\n• Alta disponibilidad global", "#10b981")
        ]
    },
    "zh-Hans": {
        "title": "静态工程技术博客 DNS 与全球 CDN 智能路由架构",
        "boxes": [
            ("1. 域名注册商\n(Porkbun)", "• 专属顶级域名：globaldevlog.com\n• 免费开启 WHOIS 隐私保护\n• 权威域名解析服务器 (NS) 委派：\n  指向 Cloudflare Anycast", "#38bdf8"),
            ("2. Cloudflare 边缘 DNS\n与安全防护层", "• CNAME 展平技术 (@ 根域名直通)\n• CNAME www 二级域名自动跳转\n• 全球 Anycast CDN 静态缓存加速\n• 自动化 Universal SSL 证书 (HTTPS)\n• 拦截 DDoS 流量与恶意爬虫攻击", "#f59e0b"),
            ("3. GitHub Pages 源站\n(Docusaurus SSG)", "• static/CNAME 域名双向绑定\n• 预编译生成的多语言纯静态包\n• 6 大语言版本全域独立访问\n• 零服务器云端运行成本支出\n• 99.99% 超高可用性全天候交付", "#10b981")
        ]
    },
    "zh-Hant": {
        "title": "靜態工程技術網站 DNS 與全球 CDN 智慧路由架構",
        "boxes": [
            ("1. 域名註冊商\n(Porkbun)", "• 專屬頂級域名：globaldevlog.com\n• 免費開啟 WHOIS 隱私保護\n• 權威域名解析伺服器 (NS) 委派：\n  指向 Cloudflare Anycast", "#38bdf8"),
            ("2. Cloudflare 邊緣 DNS\n與安全防護層", "• CNAME 展平技術 (@ 根域名直通)\n• CNAME www 二級域名自動跳轉\n• 全球 Anycast CDN 靜態快取加速\n• 自動化 Universal SSL 證書 (HTTPS)\n• 攔截 DDoS 流量與惡意爬蟲攻擊", "#f59e0b"),
            ("3. GitHub Pages 源站\n(Docusaurus SSG)", "• static/CNAME 域名雙向綁定\n• 預編譯生成的多語言純靜態包\n• 6 大語言版本全域獨立存取\n• 零伺服器雲端運行成本支出\n• 99.99% 超高可用性全天候交付", "#10b981")
        ]
    },
}

def render_dns_diagram_high_vis():
    print("\n--- Rendering High-Visibility DNS Architecture Diagrams (All 6 Locales) ---")
    posts_to_update = [
        "2026-10-20-custom-domain-adsense-seo-guide",
        "2026-10-21-github-pages-custom-domain-cloudflare-dns"
    ]

    for loc, root_dir in LOCALES.items():
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = DNS_TEXTS[loc]

        fig, ax = plt.subplots(figsize=(14, 7), dpi=150)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(7.0, 6.3, data["title"], color='#ffffff', fontsize=18, fontweight='bold', ha='center')

        box_width = 3.9
        for i, (title, desc, col) in enumerate(data["boxes"]):
            x = 0.6 + i * 4.35
            rect = patches.FancyBboxPatch((x, 0.9), box_width, 4.8, boxstyle="round,pad=0.25",
                                          linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + box_width/2, 5.0, title, color=col, fontsize=15, fontweight='bold', ha='center')
            ax.plot([x + 0.3, x + box_width - 0.3], [4.3, 4.3], color=col, linewidth=1.5)
            ax.text(x + 0.3, 4.0, desc, color='#f1f5f9', fontsize=12.5,
                    fontweight='medium', ha='left', va='top', linespacing=1.6)

            if i < 2:
                arrow = patches.FancyArrowPatch((x + box_width + 0.05, 3.2), (x + box_width + 0.4, 3.2),
                                               arrowstyle='->', mutation_scale=20, color='#94a3b8', linewidth=2.5)
                ax.add_patch(arrow)

        ax.set_xlim(0, 14)
        ax.set_ylim(0.5, 7.0)
        ax.axis('off')
        plt.tight_layout()

        for post_slug in posts_to_update:
            target_dir = os.path.join(root_dir, post_slug, "images")
            os.makedirs(target_dir, exist_ok=True)
            out_path = os.path.join(target_dir, "01_dns_routing_architecture.png")
            fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
            print(f"  [OK] [{loc}] Rendered DNS diagram: {out_path}")
        plt.close()


# ==============================================================================
# 4. INDEXING PIPELINE (02_indexing_pipeline.png)
# ==============================================================================
INDEXING_TEXTS = {
    "en": {
        "title": "Global Search Engine Indexing & AdSense Monetization Pipeline",
        "boxes": [
            ("Google Search\nConsole", "• DNS TXT Domain Ownership\n• 6 Multilingual Sitemaps Active\n• Direct URL Inspection Requests\n• Core Web Vitals Monitoring", "#60a5fa"),
            ("Naver Search\nAdvisor", "• Host-Level Site Registration\n• Dual Auth (HTML File + Meta)\n• RSS & Sitemaps Ingestion\n• Yeti Crawler Priority Request", "#4ade80"),
            ("Bing Webmaster\n& AI Search", "• Instant GSC 1-Click Import\n• Skip 48-Hour Crawl Delay\n• Direct URL Submission API\n• ChatGPT & Copilot Ingestion", "#2dd4bf"),
            ("Google AdSense\nMonetization", "• Custom Apex Domain Approved\n• Automated Ad Tag Deployment\n• static/ads.txt Crawler Ready\n• High-Value Technical CPM", "#fbbf24")
        ]
    },
    "ko": {
        "title": "글로벌 검색엔진 인덱싱 및 구글 애드센스 수익화 4단계 파이프라인",
        "boxes": [
            ("구글 서치콘솔\n(Google Search)", "• DNS TXT 레코드 소유권 확인\n• 6개 국어 sitemap.xml 제출\n• 실시간 색인 생성 요청(URL 검사)\n• Core Web Vitals 성능 모니터링", "#60a5fa"),
            ("네이버 서치어드바이저\n(Naver Search)", "• 루트 호스트 단위 사이트 등록\n• HTML 파일 + 메타태그 이중 인증\n• RSS 피드 및 사이트맵 자동 수집\n• Yeti 검색 로봇 우선 수집 요청", "#4ade80"),
            ("Bing 웹마스터\n& AI 검색", "• GSC 연동 원클릭 즉시 가져오기\n• 48시간 대기 없는 수동 사이트맵\n• IndexNow 실시간 URL 전송 API\n• ChatGPT Search & Copilot 반영", "#2dd4bf"),
            ("구글 애드센스\n(AdSense 승인)", "• 커스텀 Apex 루트 도메인 승인\n• 전역 자동 광고 스크립트 삽입\n• static/ads.txt 배포 (HTTP 200)\n• 고단가 IT 개발 기술 타겟팅 CPM", "#fbbf24")
        ]
    },
    "ja": {
        "title": "グローバル検索エンジン・インデックス登録＆AdSense収益化パイプライン",
        "boxes": [
            ("Google Search\nConsole", "• DNS TXT ドメイン所有権認証\n• 6言語対応 sitemap.xml 提出\n• URL検査による即時インデックス要求\n• ウェブに関する主な指標の監視", "#60a5fa"),
            ("Naver Search\nAdvisor", "• ホスト単位のサイト登録完了\n• HTMLファイル＋メタタグ二重認証\n• RSSフィード＆サイトマップ自動巡回\n• Yeti 検索クローラー優先収集要求", "#4ade80"),
            ("Bing Webmaster\n＆ AI 検索", "• GSC連携によるワンクリック同期\n• 48時間待機を回避する手動登録\n• IndexNow 即時URL送信API連携\n• ChatGPT Search ＆ Copilot反映", "#2dd4bf"),
            ("Google AdSense\n収益化審査", "• 独自Apexルートドメイン審査通過\n• 自動広告スクリプトの全域配置\n• static/ads.txt 正常配信 (HTTP 200)\n• 高単価エンジニア向け技術広告配信", "#fbbf24")
        ]
    },
    "es": {
        "title": "Pipeline de Indexación en Motores de Búsqueda y Monetización AdSense",
        "boxes": [
            ("Google Search\nConsole", "• Autenticación DNS TXT de Dominio\n• 6 Sitemaps Multilingües Enviados\n• Petición de Inspección de URL\n• Monitoreo de Core Web Vitals", "#60a5fa"),
            ("Naver Search\nAdvisor", "• Registro de Sitio a Nivel de Host\n• Doble Auth (Archivo HTML + Meta)\n• Recolección de Feed RSS y Sitemaps\n• Petición Prioritaria para Robot Yeti", "#4ade80"),
            ("Bing Webmaster\ny Búsqueda IA", "• Importación Instantánea desde GSC\n• Registro Directo sin Espera 48h\n• API IndexNow para Envío Rápido\n• Indexación en ChatGPT y Copilot", "#2dd4bf"),
            ("Google AdSense\nMonetización", "• Dominio Apex Personalizado Aprobado\n• Código de Anuncios Automáticos Activo\n• static/ads.txt Verificado (HTTP 200)\n• Anuncios Técnicos de Alto CPM", "#fbbf24")
        ]
    },
    "zh-Hans": {
        "title": "全球主流搜索引擎收录索引与 Google AdSense 商业变现流水线",
        "boxes": [
            ("Google Search\nConsole", "• DNS TXT 域名所有权极速验证\n• 提交 6 大多语言 sitemap.xml\n• 实时发起 URL 网页抓取收录索引\n• 核心网页指标 (Core Web Vitals)", "#60a5fa"),
            ("Naver Search\nAdvisor", "• 顶级主机域名层级站点注册\n• HTML 验证文件 + Meta 标签双保险\n• 自动抓取 RSS 订阅源与多语言地图\n• Yeti 搜索引擎爬虫高优先级抓取", "#4ade80"),
            ("Bing Webmaster\n与 AI 搜索集成", "• 关联 GSC 一键极速导入配置\n• 免除 48 小时审查延迟手动提交\n• IndexNow 实时 URL 极速推送 API\n• ChatGPT Search 与 Copilot 数据源", "#2dd4bf"),
            ("Google AdSense\n广告收益变现", "• 专属 Apex 顶级根域名顺利过审\n• 全局自动化自适应广告代码注入\n• static/ads.txt 成功挂载 (HTTP 200)\n• 锁定高价值 IT 研发技术领域 CPM", "#fbbf24")
        ]
    },
    "zh-Hant": {
        "title": "全球主流搜尋引擎收錄索引與 Google AdSense 商業變現流水線",
        "boxes": [
            ("Google Search\nConsole", "• DNS TXT 網域名稱所有權極速驗證\n• 提交 6 大多語言 sitemap.xml\n• 即時發起 URL 網頁抓取收錄索引\n• 核心網頁指標 (Core Web Vitals)", "#60a5fa"),
            ("Naver Search\nAdvisor", "• 頂級主機網域名稱層級網站註冊\n• HTML 驗證檔案 + Meta 標籤雙保險\n• 自動抓取 RSS 訂閱源與多語言地圖\n• Yeti 搜尋引擎爬蟲高優先級抓取", "#4ade80"),
            ("Bing Webmaster\n與 AI 搜尋整合", "• 關聯 GSC 一鍵極速匯入配置\n• 免除 48 小時審查延遲手動提交\n• IndexNow 即時 URL 極速推送 API\n• ChatGPT Search 與 Copilot 資料源", "#2dd4bf"),
            ("Google AdSense\n廣告收益變現", "• 專屬 Apex 頂級根網域名稱順利過審\n• 全域自動化自適應廣告程式碼注入\n• static/ads.txt 成功掛載 (HTTP 200)\n• 鎖定高價值 IT 研發技術領域 CPM", "#fbbf24")
        ]
    },
}

def render_indexing_pipeline_high_vis():
    print("\n--- Rendering High-Visibility Indexing Pipeline Diagrams (All 6 Locales) ---")
    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-10-20-custom-domain-adsense-seo-guide", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = INDEXING_TEXTS[loc]

        fig, ax = plt.subplots(figsize=(15, 7), dpi=150)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(7.5, 6.35, data["title"], color='#ffffff', fontsize=18, fontweight='bold', ha='center')

        box_width = 3.3
        for i, (title, desc, col) in enumerate(data["boxes"]):
            x = 0.5 + i * 3.65
            rect = patches.FancyBboxPatch((x, 0.9), box_width, 4.8, boxstyle="round,pad=0.2",
                                          linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + box_width/2, 5.0, title, color=col, fontsize=14.5, fontweight='bold', ha='center')
            ax.plot([x + 0.3, x + box_width - 0.3], [4.3, 4.3], color=col, linewidth=1.5)
            ax.text(x + 0.25, 3.95, desc, color='#f1f5f9', fontsize=12,
                    fontweight='medium', ha='left', va='top', linespacing=1.6)

            if i < 3:
                arrow = patches.FancyArrowPatch((x + box_width + 0.05, 3.2), (x + box_width + 0.35, 3.2),
                                               arrowstyle='->', mutation_scale=18, color='#94a3b8', linewidth=2.2)
                ax.add_patch(arrow)

        ax.set_xlim(0, 15)
        ax.set_ylim(0.5, 7.0)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "02_indexing_pipeline.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered indexing pipeline: {out_path}")


# ==============================================================================
# 5. ADS.TXT CRAWLER FLOW (01_ads_txt_crawler_flow.png)
# ==============================================================================
ADS_TXT_TEXTS = {
    "en": {
        "title": "Google AdSense ads.txt Crawler Verification & Routing Flow",
        "boxes": [
            ("1. Root Repository\n(static/ads.txt)", "• File: static/ads.txt\n• Publisher ID Record:\n  google.com, pub-XXXX,\n  DIRECT, f08c47fec0942fa0\n• Pure UTF-8 Plain Text", "#38bdf8"),
            ("2. Edge CDN & Origin\n(GitHub & Cloudflare)", "• Direct URL Routing:\n  globaldevlog.com/ads.txt\n• HTTP Status: 200 OK\n• MIME: text/plain; charset=utf-8\n• Zero Subdomain Redirection", "#f59e0b"),
            ("3. AdSense Bot Crawl\n(Google-adstxt)", "• User-Agent: Google-adstxt\n• Crawler Scans Apex Domain\n• Instant Record Match\n• Zero Authorization Delay", "#818cf8"),
            ("4. Revenue Protection\n(Active Monetization)", "• Ads.txt Status: Authorized\n• Prevents Ad Spoofing\n• Zero Ad Serving Restrictions\n• 100% Monetization Health", "#10b981")
        ]
    },
    "ko": {
        "title": "구글 애드센스 ads.txt 크롤러 검증 및 전송 라우팅 플로우",
        "boxes": [
            ("1. 정적 저장소 배포\n(static/ads.txt)", "• 파일 경로: static/ads.txt\n• 고유 게시자 ID 레코드 선언:\n  google.com, pub-XXXX,\n  DIRECT, f08c47fec0942fa0\n• 순수 UTF-8 일반 텍스트 포맷", "#38bdf8"),
            ("2. CDN 엣지 및 오리진\n(GitHub & Cloudflare)", "• 루트 직통 URL 라우팅:\n  globaldevlog.com/ads.txt\n• HTTP 응답 코드: 200 OK\n• Content-Type: text/plain\n• 불필요한 서브도메인 리다이렉트 배제", "#f59e0b"),
            ("3. 애드센스 봇 크롤링\n(Google-adstxt)", "• 봇 User-Agent: Google-adstxt\n• Apex 루트 도메인 정밀 탐색\n• 게시자 ID 일치 여부 자동 대조\n• 24시간 내 크롤러 수집 체결", "#818cf8"),
            ("4. 수익 손실 방지 승인\n(광고 송출 정상화)", "• ads.txt 상태: 승인됨 (녹색)\n• 도메인 스푸핑 광고 사기 방지\n• 광고 게재 제한 및 손실 0건\n• 100% 정상 광고 입찰 및 수익 창출", "#10b981")
        ]
    },
    "ja": {
        "title": "Google AdSense ads.txt クローラー検証＆配信ルーティング・フロー",
        "boxes": [
            ("1. 静的リポジトリ配置\n(static/ads.txt)", "• ファイル配置: static/ads.txt\n• 固有パブリッシャーID宣言:\n  google.com, pub-XXXX,\n  DIRECT, f08c47fec0942fa0\n• 純粋なUTF-8プレーンテキスト", "#38bdf8"),
            ("2. CDNエッジ＆オリジン\n(GitHub & Cloudflare)", "• ルート直通URL配信:\n  globaldevlog.com/ads.txt\n• HTTPレスポンス: 200 OK\n• Content-Type: text/plain\n• サブドメイン転送の完全排除", "#f59e0b"),
            ("3. AdSenseボット巡回\n(Google-adstxt)", "• User-Agent: Google-adstxt\n• Apexルートドメイン自動スキャン\n• レコード一致の瞬時検証\n• 24時間以内のクローラー巡回", "#818cf8"),
            ("4. 収益損失ゼロ防衛\n(広告配信ステータス正常)", "• ads.txt ステータス: 承認済 (緑)\n• ドメインなりすまし詐欺の防止\n• 広告配信制限リスク完全排除\n• 100%健全な広告収益の最大化", "#10b981")
        ]
    },
    "es": {
        "title": "Flujo de Verificación y Enrutamiento del Rastreador ads.txt de AdSense",
        "boxes": [
            ("1. Repositorio Estático\n(static/ads.txt)", "• Archivo: static/ads.txt\n• Registro de ID de Editor:\n  google.com, pub-XXXX,\n  DIRECT, f08c47fec0942fa0\n• Texto Plano UTF-8 Puro", "#38bdf8"),
            ("2. CDN Edge y Origen\n(GitHub y Cloudflare)", "• Enrutamiento Directo:\n  globaldevlog.com/ads.txt\n• Estado HTTP: 200 OK\n• MIME: text/plain; charset=utf-8\n• Sin Redirecciones de Subdominio", "#f59e0b"),
            ("3. Rastreo del Bot\n(Google-adstxt)", "• User-Agent: Google-adstxt\n• Escaneo en Dominio Raíz Apex\n• Coincidencia Exacta de Registros\n• Indexación Rápida en 24 Horas", "#818cf8"),
            ("4. Protección de Ingresos\n(Monetización Activa)", "• Estado Ads.txt: Autorizado\n• Prevención de Fraude y Suplantación\n• Cero Restricciones de Anuncios\n• 100% Saludable en Monetización", "#10b981")
        ]
    },
    "zh-Hans": {
        "title": "Google AdSense ads.txt 官方爬虫验证与 CDN 边缘路由全流程",
        "boxes": [
            ("1. 静态源码挂载\n(static/ads.txt)", "• 文件路径：static/ads.txt\n• 声明专属发布商 ID 记录：\n  google.com, pub-XXXX,\n  DIRECT, f08c47fec0942fa0\n• 纯净 UTF-8 纯文本格式", "#38bdf8"),
            ("2. CDN 边缘全球分发\n(GitHub & Cloudflare)", "• 根目录直通 URL 路由：\n  globaldevlog.com/ads.txt\n• HTTP 响应状态：200 OK\n• Content-Type: text/plain\n• 杜绝二级子域名重定向损耗", "#f59e0b"),
            ("3. AdSense 爬虫巡检\n(Google-adstxt)", "• 爬虫标识：Google-adstxt\n• 自动抓取 Apex 根域名文件\n• 瞬时比对发布商 ID 记录一致性\n• 24 小时内完成官方认证收录", "#818cf8"),
            ("4. 广告收益零损失\n(商业变现通道畅通)", "• ads.txt 状态：已获授权 (绿色)\n• 彻底规避域名仿冒欺诈流量\n• 杜绝广告投放被限制与收入受损\n• 100% 确保高单价技术广告正常竞价", "#10b981")
        ]
    },
    "zh-Hant": {
        "title": "Google AdSense ads.txt 官方爬蟲驗證與 CDN 邊緣路由全流程",
        "boxes": [
            ("1. 靜態原始碼掛載\n(static/ads.txt)", "• 檔案路徑：static/ads.txt\n• 聲明專屬發布商 ID 記錄：\n  google.com, pub-XXXX,\n  DIRECT, f08c47fec0942fa0\n• 純淨 UTF-8 純文字格式", "#38bdf8"),
            ("2. CDN 邊緣全球分發\n(GitHub & Cloudflare)", "• 根目錄直通 URL 路由：\n  globaldevlog.com/ads.txt\n• HTTP 回應狀態：200 OK\n• Content-Type: text/plain\n• 杜絕二級子網域名稱重新導向損耗", "#f59e0b"),
            ("3. AdSense 爬蟲巡檢\n(Google-adstxt)", "• 爬蟲標識：Google-adstxt\n• 自動抓取 Apex 根網域名稱檔案\n• 瞬時比對發布商 ID 記錄一致性\n• 24 小時內完成官方認證收錄", "#818cf8"),
            ("4. 廣告收益零損失\n(商業變現通道暢通)", "• ads.txt 狀態：已獲授權 (綠色)\n• 徹底規避網域名稱仿冒欺詐流量\n• 杜絕廣告投放被限制與收入受損\n• 100% 確保高單價技術廣告正常競價", "#10b981")
        ]
    },
}

def render_ads_txt_crawler_high_vis():
    print("\n--- Rendering High-Visibility ads.txt Crawler Flow Diagrams (All 6 Locales) ---")
    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-10-21-static-site-adsense-ads-txt-guide", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = ADS_TXT_TEXTS[loc]

        fig, ax = plt.subplots(figsize=(15, 7), dpi=150)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(7.5, 6.35, data["title"], color='#ffffff', fontsize=18, fontweight='bold', ha='center')

        box_width = 3.3
        for i, (title, desc, col) in enumerate(data["boxes"]):
            x = 0.5 + i * 3.65
            rect = patches.FancyBboxPatch((x, 0.9), box_width, 4.8, boxstyle="round,pad=0.2",
                                          linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + box_width/2, 5.0, title, color=col, fontsize=14.5, fontweight='bold', ha='center')
            ax.plot([x + 0.3, x + box_width - 0.3], [4.3, 4.3], color=col, linewidth=1.5)
            ax.text(x + 0.25, 3.95, desc, color='#f1f5f9', fontsize=12,
                    fontweight='medium', ha='left', va='top', linespacing=1.6)

            if i < 3:
                arrow = patches.FancyArrowPatch((x + box_width + 0.05, 3.2), (x + box_width + 0.35, 3.2),
                                               arrowstyle='->', mutation_scale=18, color='#94a3b8', linewidth=2.2)
                ax.add_patch(arrow)

        ax.set_xlim(0, 15)
        ax.set_ylim(0.5, 7.0)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "01_ads_txt_crawler_flow.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered ads.txt crawler diagram: {out_path}")


# ==============================================================================
# 6. ANPR VISION (01_pipeline_diagram.png)
# ==============================================================================
ANPR_TEXTS = {
    "en": {
        "title": "End-to-End Blackbox ANPR & Lane Intrusion Detection Architecture",
        "stages": [
            ("1. Video Feed", "1080p 30fps Real-Time\nDashcam Footage"),
            ("2. Lane Detection", "Bird's-Eye View (BEV)\nDynamic Lane ROI"),
            ("3. Vehicle / Plate", "YOLOv3 Vehicle Box\n& YOLOv5 Plate Net"),
            ("4. CSRT Tracking", "Temporal Tracking &\nMotion Continuity"),
            ("5. Super Resolution", "EDSR_x4 Deep Net\nPlate Reconstruction"),
            ("6. OCR Ensemble", "Regex Validation &\nTemporal Voting"),
        ]
    },
    "ko": {
        "title": "실시간 블랙박스 차선 침범 적발 및 초해상화 번호판 인식 6단계 파이프라인",
        "stages": [
            ("1. 블랙박스 입력", "1080p 30fps 실시간\n차량 주행 비디오"),
            ("2. 동적 차선 검출", "원근 투영(BEV) 변환\n동적 ROI 경계선 추출"),
            ("3. 차량/번호판 탐지", "YOLOv3 차량 바운딩\n& YOLOv5 번호판 망"),
            ("4. CSRT 고속 추적", "프레임 간 연속성 보장\n고속 실시간 트래커"),
            ("5. EDSR 초해상화", "저해상도 번호판 영역\n4배 딥러닝 고화질 복원"),
            ("6. OCR 앙상블", "한국 번호판 정규식 &\n시간축 다수결 투표"),
        ]
    },
    "ja": {
        "title": "リアルタイム ドライブレコーダー車線侵犯検知＆超解像ANPR 6段階パイプライン",
        "stages": [
            ("1. ドラレコ入力", "1080p 30fps リアルタイム\n走行ビデオ映像"),
            ("2. 動的車線検出", "俯瞰変換(BEV)＆\n動的ROI境界線抽出"),
            ("3. 車両・ナンバー検出", "YOLOv3 車両領域\n＆ YOLOv5 ナンバー検出"),
            ("4. CSRT高速追跡", "フレーム間連続性＆\n実時間トラッカー統合"),
            ("5. EDSR深層超解像", "低解像度ナンバーを\n4倍ディープラーニング復元"),
            ("6. OCRアンサンブル", "正規表現バリデーション＆\n時間軸多数決アンサンブル"),
        ]
    },
    "es": {
        "title": "Arquitectura de Detección de Invasión de Carril y ANPR con Superresolución",
        "stages": [
            ("1. Entrada de Video", "Video de Caja Negra\n1080p a 30fps"),
            ("2. Detección de Carril", "Transformación BEV y\nLímites Dinámicos ROI"),
            ("3. Vehículo y Matrícula", "ROI Vehicular YOLOv3\ny Detector YOLOv5"),
            ("4. Rastreo CSRT", "Continuidad Temporal\ny Rastreo en Tiempo Real"),
            ("5. Superresolución", "Reconstrucción 4x con\nRed Profunda EDSR"),
            ("6. Ensamble de OCR", "Regex de Matrículas y\nVotación Mayoritaria"),
        ]
    },
    "zh-Hans": {
        "title": "实景行车记录仪车道违章压线抓拍与超分辨率车牌识别全流程架构",
        "stages": [
            ("1. 实时视频输入", "1080p 30fps 实景\n行车记录仪视频流"),
            ("2. 动态车道检测", "逆透视鸟瞰图变换 (BEV)\n动态 ROI 兴趣边界"),
            ("3. 目标车辆/车牌", "YOLOv3 车辆目标框\n与 YOLOv5 车牌定位网"),
            ("4. CSRT 跟踪器", "跨帧时序空间连续性\n高帧率实时运动追踪"),
            ("5. EDSR 深度超分", "模糊低像素车牌图像\n4 倍深度重建超分辨率"),
            ("6. OCR 投票集成", "标准车牌正则校验\n多帧时序加权投票集成"),
        ]
    },
    "zh-Hant": {
        "title": "實景行車記錄器車道違章壓線抓拍與超解析度車牌辨識全流程架構",
        "stages": [
            ("1. 即時視訊輸入", "1080p 30fps 實景\n行車記錄器視訊流"),
            ("2. 動態車道檢測", "逆透視鳥瞰圖變換 (BEV)\n動態 ROI 興趣邊界"),
            ("3. 目標車輛/車牌", "YOLOv3 車輛目標框\n與 YOLOv5 車牌定位網"),
            ("4. CSRT 追蹤器", "跨幀時序空間連續性\n高幀率即時運動追蹤"),
            ("5. EDSR 深度超分", "模糊低像素車牌圖像\n4 倍深度重建超解析度"),
            ("6. OCR 投票集成", "標準車牌正則校驗\n多幀時序加權投票集成"),
        ]
    },
}

def render_anpr_diagram_high_vis():
    print("\n--- Rendering High-Visibility ANPR Pipeline Diagrams (All 6 Locales) ---")
    colors = ["#38bdf8", "#818cf8", "#a855f7", "#ec4899", "#f59e0b", "#10b981"]

    for loc, root_dir in LOCALES.items():
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = ANPR_TEXTS[loc]

        fig, ax = plt.subplots(figsize=(15, 6.2), dpi=150)
        fig.patch.set_facecolor('#0b1329')
        ax.set_facecolor('#0b1329')

        ax.text(7.5, 5.5, data["title"], color='#ffffff', fontsize=18, fontweight='bold', ha='center')

        for i, (st_name, st_desc) in enumerate(data["stages"]):
            x = 0.4 + i * 2.42
            col = colors[i]
            rect = patches.FancyBboxPatch((x, 0.9), 2.2, 4.1, boxstyle="round,pad=0.2",
                                          linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + 1.1, 4.3, st_name, color=col, fontsize=13, fontweight='bold', ha='center')
            ax.plot([x + 0.2, x + 2.0], [3.8, 3.8], color=col, linewidth=1.5)
            ax.text(x + 1.1, 2.35, st_desc, color='#f1f5f9', fontsize=12,
                    fontweight='medium', ha='center', va='center', linespacing=1.5)

            if i < 5:
                arrow = patches.FancyArrowPatch((x + 2.25, 2.8), (x + 2.42, 2.8),
                                               arrowstyle='->', mutation_scale=16, color='#94a3b8', linewidth=2.0)
                ax.add_patch(arrow)

        ax.set_xlim(0, 15)
        ax.set_ylim(0.4, 6.2)
        ax.axis('off')
        plt.tight_layout()

        target_dir = os.path.join(root_dir, "2026-06-25-vision-anpr-1", "images")
        os.makedirs(target_dir, exist_ok=True)
        out_path = os.path.join(target_dir, "01_pipeline_diagram.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered ANPR diagram: {out_path}")


# ==============================================================================
# 7. RL Q-LEARNING (02_architecture.png)
# ==============================================================================
RL_TEXTS = {
    "en": {
        "title": "Webots Autonomous Robot Q-Learning Architecture & Sim-to-Real Pipeline",
        "blocks": [
            ("1. Simulation Physics", "• Webots 2-Wheel Differential\n• 8-Direction Infrared (IR)\n• Real-Time Collision Physics\n• Environment Boundary Bounds", "#38bdf8"),
            ("2. State Discretization", "• 648 Discrete State Bins\n• Distance: 9 Granular Bins\n• Angle: 8 Heading Sectors\n• Obstacle Proximity Vectors", "#818cf8"),
            ("3. Tabular Q-Learning", "• Bellman Equation Convergence\n• Goal Reward (+100) / Crash (-50)\n• Epsilon-Greedy Exploration\n• Optimal Action Table Synthesis", "#fbbf24"),
            ("4. Sim-to-Real Transfer", "• High-Speed Python Socket IPC\n• HC-06 Bluetooth Telemetry\n• Arduino Uno Motor Control\n• Real-Time ArUco Vision Tracking", "#10b981")
        ]
    },
    "ko": {
        "title": "Webots 자율주행 로봇 Q-Learning 강화학습 아키텍처 및 Sim-to-Real 실기 전이 파이프라인",
        "blocks": [
            ("1. 물리 시뮬레이션 환경", "• Webots 2륜 차동 구동 로봇\n• 8방향 적외선(IR) 거리 센서\n• 실시간 강체 충돌 물리 연산\n• 경기장 경계 장애물 환경 구축", "#38bdf8"),
            ("2. 상태 공간 이산화", "• 648개 이산 상태 공간 설계\n• 거리 센서 9구간 세분화\n• 목표물 상대각도 8구간 분할\n• 장애물 근접 회피 벡터 융합", "#818cf8"),
            ("3. 표 형식 Q-Learning", "• 벨만 최적 방정식 정책 수렴\n• 보상 함수: 도달(+100) / 충돌(-50)\n• ε-탐욕(Epsilon) 탐색 전략\n• 최적 Q-Table 정책 행렬 완성", "#fbbf24"),
            ("4. Sim-to-Real 실기 전이", "• 초고속 파이썬 소켓 IPC 통신\n• HC-06 블루투스 무선 원격 제어\n• 아두이노 우노 모터 드라이버\n• ArUco 비전 마커 실시간 오버헤드 추적", "#10b981")
        ]
    },
    "ja": {
        "title": "Webots 自律走行ロボット Q-Learning アーキテクチャ＆Sim-to-Real パイプライン",
        "blocks": [
            ("1. 物理シミュレーション", "• Webots 2輪差動駆動ロボット\n• 8方向赤外線(IR)距離センサー\n• リアルタイム衝突物理シミュレーション\n• アリーナ環境と障害物配置", "#38bdf8"),
            ("2. 状態空間の離散化", "• 648個の離散状態空間設計\n• 距離センサー 9分割ビン\n• 目標相対角度 8分割セクター\n• 障害物接近ベクトル統合", "#818cf8"),
            ("3. 表形式 Q-Learning", "• ベルマン最適方程式の収束\n• 報酬設計: 目標到達(+100) / 衝突(-50)\n• ε-Greedy 探索・活用バランス\n• 最適 Q-Table ポリシー行列の確立", "#fbbf24"),
            ("4. Sim-to-Real 実機転移", "• Python ソケットIPC高速通信\n• HC-06 Bluetooth 無線テレメトリ\n• Arduino Uno モーター制御\n• ArUco ビジョンマーカー実時間追跡", "#10b981")
        ]
    },
    "es": {
        "title": "Arquitectura de Robot Autónomo con Q-Learning en Webots y Pipeline Sim-to-Real",
        "blocks": [
            ("1. Simulación Física", "• Robot Diferencial en Webots\n• Sensores Infrarrojos IR (8 Vías)\n• Física de Colisión en Tiempo Real\n• Entorno Cerrado con Obstáculos", "#38bdf8"),
            ("2. Discretización de Estados", "• 648 Bins de Estados Discretos\n• Distancia: 9 Bins Granulares\n• Ángulo: 8 Sectores de Orientación\n• Vectores de Proximidad de Peligro", "#818cf8"),
            ("3. Q-Learning Tabular", "• Convergencia Ecuación de Bellman\n• Recompensa: Meta (+100) / Choque (-50)\n• Exploración Epsilon-Greedy\n• Matriz de Política Óptima Q-Table", "#fbbf24"),
            ("4. Transferencia Sim-to-Real", "• Socket IPC de Alta Velocidad\n• Telemetría Bluetooth HC-06\n• Control de Motores con Arduino Uno\n• Rastreo Visual ArUco en Tiempo Real", "#10b981")
        ]
    },
    "zh-Hans": {
        "title": "Webots 自主移动机器人 Q-Learning 强化学习架构与虚实迁移 (Sim-to-Real) 流程",
        "blocks": [
            ("1. 物理仿真实验环境", "• Webots 双轮差速移动底盘\n• 8 方向高灵敏红外 (IR) 测距传感器\n• 实时刚体碰撞动力学仿真计算\n• 自定义封闭赛道障碍物场景构建", "#38bdf8"),
            ("2. 状态空间连续值离散化", "• 规划构建 648 个离散状态空间 Bin\n• 目标欧氏距离精细划分为 9 档区间\n• 相对航向夹角划分为 8 个朝向扇区\n• 融合近邻障碍物碰撞排斥向量", "#818cf8"),
            ("3. 表格式 Q-Learning 求解", "• 贝尔曼最优方程 (Bellman) 收敛\n• 密集奖励设计：到达(+100) / 碰撞(-50)\n• ε-贪婪算法动态平衡探索与利用\n• 训练合成高泛化全局最优 Q-Table", "#fbbf24"),
            ("4. 虚实无缝迁移 (Sim-to-Real)", "• 高并发 Python 底层 Socket IPC 通信\n• HC-06 蓝牙串口低延迟无线遥控\n• Arduino Uno 硬件电机双驱执行\n• 顶置 ArUco 视觉位姿实时闭环追踪", "#10b981")
        ]
    },
    "zh-Hant": {
        "title": "Webots 自主移動機器人 Q-Learning 強化學習架構與虛實遷移 (Sim-to-Real) 流程",
        "blocks": [
            ("1. 物理仿真實驗環境", "• Webots 雙輪差速移動底盤\n• 8 方向高靈敏紅外 (IR) 測距感測器\n• 即時剛體碰撞動力學仿真計算\n• 自定義封閉賽道障礙物場景構建", "#38bdf8"),
            ("2. 狀態空間連續值離散化", "• 規劃構建 648 個離散狀態空間 Bin\n• 目標歐氏距離精細劃分為 9 檔區間\n• 相對航向夾角劃分為 8 個朝向扇區\n• 融合近鄰障礙物碰撞排斥向量", "#818cf8"),
            ("3. 表格式 Q-Learning 求解", "• 貝爾曼最優方程 (Bellman) 收斂\n• 密集獎勵設計：到達(+100) / 碰撞(-50)\n• ε-貪婪演算法動態平衡探索與利用\n• 訓練合成高泛化全局最優 Q-Table", "#fbbf24"),
            ("4. 虛實無縫遷移 (Sim-to-Real)", "• 高並發 Python 底層 Socket IPC 通訊\n• HC-06 藍牙串口低延遲無線遙控\n• Arduino Uno 硬體電機雙驅執行\n• 頂置 ArUco 視覺位姿即時閉環追蹤", "#10b981")
        ]
    },
}

def render_rl_diagram_high_vis():
    print("\n--- Rendering High-Visibility RL Q-Learning Diagrams (All 6 Locales) ---")
    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-05-17-rl-qlearning-1", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = RL_TEXTS[loc]

        fig, ax = plt.subplots(figsize=(15, 7), dpi=150)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(7.5, 6.35, data["title"], color='#ffffff', fontsize=18, fontweight='bold', ha='center')

        box_width = 3.3
        items = data["blocks"]
        for i, (title, desc, col) in enumerate(items):
            x = 0.5 + i * 3.65
            rect = patches.FancyBboxPatch((x, 0.9), box_width, 4.8, boxstyle="round,pad=0.2",
                                          linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + box_width/2, 5.0, title, color=col, fontsize=14.5, fontweight='bold', ha='center')
            ax.plot([x + 0.3, x + box_width - 0.3], [4.3, 4.3], color=col, linewidth=1.5)
            ax.text(x + 0.25, 3.95, desc, color='#f1f5f9', fontsize=12,
                    fontweight='medium', ha='left', va='top', linespacing=1.6)

            if i < 3:
                arrow = patches.FancyArrowPatch((x + box_width + 0.05, 3.2), (x + box_width + 0.35, 3.2),
                                               arrowstyle='->', mutation_scale=18, color='#94a3b8', linewidth=2.2)
                ax.add_patch(arrow)

        ax.set_xlim(0, 15)
        ax.set_ylim(0.5, 7.0)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "02_architecture.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered RL architecture diagram: {out_path}")


# ==============================================================================
# 8. MAEUMJIGI #23 SAFETY WRAPPER FLOWCHART (02_presentation.png)
# ==============================================================================
SAFETY_WRAPPER_TEXTS = {
    "en": {
        "title": "Deterministic Safety Wrapper Architecture Flowchart",
        "subtitle": "Guaranteed 100% Crisis Detection Without Generative LLM Hallucinations",
        "steps": [
            ("1. User Input", "Counseling Utterance\n& Raw Chat Message", "#38bdf8"),
            ("2. Crisis Classifier", "Intent & Risk Scoring\n(Suicide / Self-Harm)", "#ec4899"),
            ("3. Bypass Decision", "Risk >= Threshold ?\nBypass Generative Model", "#fbbf24"),
            ("4. Deterministic Wrapper", "Inject Emergency Lifeline\nHotline (109 / 988)", "#10b981"),
            ("5. Verified Safe Output", "Empathetic Safety Response\n& Lifeline Contact Card", "#34d399"),
        ]
    },
    "ko": {
        "title": "결정론적 Safety Wrapper 안전망 아키텍처 플로우차트",
        "subtitle": "생성형 LLM 환각을 100% 원천 배제한 위기 개입 및 24시간 긴급 상담 안내",
        "steps": [
            ("1. 사용자 입력", "상담자 발화 텍스트\n실시간 메시지 수신", "#38bdf8"),
            ("2. 위기 분류기", "위험도 점수 분석\n(자해·자살 위기 신호 감지)", "#ec4899"),
            ("3. 바이패스 판단", "임계값 초과 여부 확인\n생성형 LLM 완전 우회", "#fbbf24"),
            ("4. 결정론적 래퍼", "국가 위기 상담 전화\n109 / 988 긴급 프로토콜", "#10b981"),
            ("5. 검증된 안전 출력", "공감형 안전 안심 메시지\n+ 긴급 상담 다이얼로그 카드", "#34d399"),
        ]
    },
    "ja": {
        "title": "決定論的 Safety Wrapper 安全網アーキテクチャ フローチャート",
        "subtitle": "生成LLMの幻覚を100%根本排除した危機介入＆24時間緊急ホットライン案内",
        "steps": [
            ("1. 相談者入力", "相談者の発話テキスト\nリアルタイム受信", "#38bdf8"),
            ("2. 危機分類器", "リスクスコア判定\n(自傷・自死の兆候検知)", "#ec4899"),
            ("3. バイパス判定", "閾値超過の判定\n生成LLMを完全バイパス", "#fbbf24"),
            ("4. 決定論的ラッパー", "国家緊急ホットライン\n(109 / 988) プロトコル注入", "#10b981"),
            ("5. 検証済の安全応答", "共感型セーフティ応答\n＋ 緊急相談ダイアログカード", "#34d399"),
        ]
    },
    "es": {
        "title": "Flujograma de Arquitectura Determinista Safety Wrapper",
        "subtitle": "Intervención de Crisis 100% Confiable sin Alucinaciones de Modelos Generativos",
        "steps": [
            ("1. Entrada de Usuario", "Expresión del Usuario\ny Mensaje de Chat en Vivo", "#38bdf8"),
            ("2. Clasificador de Crisis", "Evaluación de Riesgo\n(Suicidio / Autolesión)", "#ec4899"),
            ("3. Decisión de Bypass", "¿Riesgo >= Umbral?\nBypass Total del LLM", "#fbbf24"),
            ("4. Wrapper Determinista", "Inyección de Línea Vital\n(Hotline 109 / 988)", "#10b981"),
            ("5. Salida Segura", "Respuesta Segura Empática\n+ Tarjeta de Línea de Emergencia", "#34d399"),
        ]
    },
    "zh-Hans": {
        "title": "确定性 Safety Wrapper 兜底安全防护架构流程图",
        "subtitle": "100% 根除生成式大模型幻觉风险，筑牢生命危机实时干预防线",
        "steps": [
            ("1. 用户原始输入", "咨询者实时口语文本\n与对话消息流输入", "#38bdf8"),
            ("2. 危机意图分类器", "自残自杀高危倾向识别\n与危机严重度量化打分", "#ec4899"),
            ("3. 动态熔断决策", "研判风险分是否超阈值\n完全熔断绕开生成式大模型", "#fbbf24"),
            ("4. 确定性安全包装器", "强制注入国家援助热线\n(109 / 988) 紧急应急协议", "#10b981"),
            ("5. 权威安全输出交付", "高度共情安抚文本响应\n+ 紧急心理援助绿色通道卡片", "#34d399"),
        ]
    },
    "zh-Hant": {
        "title": "確定性 Safety Wrapper 兜底安全防護架構流程圖",
        "subtitle": "100% 根除生成式大模型幻覺風險，築牢生命危機即時干預防線",
        "steps": [
            ("1. 使用者原始輸入", "諮詢者即時口語文字\n與對話消息流輸入", "#38bdf8"),
            ("2. 危機意圖分類器", "自殘自殺高危傾向識別\n與危機嚴重度量化打分", "#ec4899"),
            ("3. 動態熔斷決策", "研判風險分是否超閾值\n完全熔斷繞開生成式大模型", "#fbbf24"),
            ("4. 確定性安全包裝器", "強制注入國家援助熱線\n(109 / 988) 緊急應急協議", "#10b981"),
            ("5. 權威安全輸出交付", "高度共情安撫文字回應\n+ 緊急心理援助綠色通道卡片", "#34d399"),
        ]
    },
}

def render_safety_wrapper_flowchart_high_vis():
    print("\n--- Rendering High-Visibility Safety Wrapper Flowcharts (All 6 Locales) ---")
    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-06-18-maeumjigi-23", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = SAFETY_WRAPPER_TEXTS[loc]

        fig, ax = plt.subplots(figsize=(15, 6.6), dpi=150)
        fig.patch.set_facecolor('#0a0f1d')
        ax.set_facecolor('#0a0f1d')

        ax.text(7.5, 6.0, data["title"], color='#ffffff', fontsize=18, fontweight='bold', ha='center')
        ax.text(7.5, 5.5, data["subtitle"], color='#38bdf8', fontsize=12.5, fontweight='bold', ha='center')

        box_width = 2.6
        for i, (s_title, s_desc, col) in enumerate(data["steps"]):
            x = 0.5 + i * 2.9
            rect = patches.FancyBboxPatch((x, 1.0), box_width, 4.0, boxstyle="round,pad=0.2",
                                          linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + box_width/2, 4.35, s_title, color=col, fontsize=13, fontweight='bold', ha='center')
            ax.plot([x + 0.2, x + box_width - 0.2], [3.9, 3.9], color=col, linewidth=1.5)
            ax.text(x + box_width/2, 2.4, s_desc, color='#f1f5f9', fontsize=12,
                    fontweight='medium', ha='center', va='center', linespacing=1.5)

            if i < 4:
                arrow = patches.FancyArrowPatch((x + box_width + 0.05, 2.9), (x + box_width + 0.25, 2.9),
                                               arrowstyle='->', mutation_scale=18, color='#94a3b8', linewidth=2.2)
                ax.add_patch(arrow)

        ax.set_xlim(0, 15)
        ax.set_ylim(0.4, 6.6)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "02_presentation.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered safety wrapper diagram: {out_path}")


# ==============================================================================
# 9. MAEUMJIGI LOCALIZED SLIDE SUMMARY CARDS (01_cover.png for EN, JA, ES, ZH)
# ==============================================================================
MAEUMJIGI_SLIDES_DATA = {
    "2026-03-31-maeumjigi-3": {
        "en": ("Overall Capstone Plan: 3 of 5 Stages Completed", "Safe & Affordable Korean Crisis Prevention AI Chatbot", "1. Model Selection 7:3 [Done]  ->  2. Web/App Full-Stack  ->  3. Safety Wrapper  ->  4. Server  ->  5. Release"),
        "ja": ("全体計画: 5段階中3段階完了報告", "安全で低コストな韓国語 危機予防・心理相談AIチャットボット", "1. モデル選定 7:3 完了  →  2. Web/アプリ実装  →  3. 安全網(Safety Wrapper)  →  4. サーバー運用  →  5. リリース"),
        "es": ("Plan General Capstone: 3 de 5 Etapas Completadas", "Chatbot de IA Seguro y Accesible para Prevención de Crisis", "1. Selección de Modelo 7:3 [Hecho]  →  2. Web/App Full-Stack  →  3. Safety Wrapper  →  4. Servidor  →  5. Lanzamiento"),
        "zh-Hans": ("毕业设计总体规划：5 大研发阶段已顺利推进完成第 3 阶段", "安全合规且经济实惠的韩语心理危机预防 AI 聊天机器人系统", "第 1 阶段：7:3 黄金比例模型确立 [已完成]  →  第 2 阶段：Web/App 全栈研发  →  第 3 阶段：安全网包装器  →  第 4 阶段：云端部署  →  第 5 阶段：正式发布"),
        "zh-Hant": ("畢業設計總體規劃：5 大研發階段已順利推進完成第 3 階段", "安全合規且經濟實惠的韓語心理危機預防 AI 聊天機器人系統", "第 1 階段：7:3 黃金比例模型確立 [已完成]  →  第 2 階段：Web/App 全端研發  →  第 3 階段：安全網包裝器  →  第 4 階段：雲端部署  →  第 5 階段：正式發布"),
    },
    "2026-04-01-maeumjigi-4": {
        "en": ("Training Dataset Preprocessing & Distribution", "Large-Scale Empathy & Counseling Corpus Extraction", "Emotion Dialogue (100k) + Crisis Transcripts -> Unified Llama 3.1 JSONL Format"),
        "ja": ("学習データセット前処理＆カテゴリ別分布分析", "大規模な共感・心理相談コーパス抽出パイプライン", "感情対話(10万件) ＋ 危機スクリプト -> 統一Llama 3.1 JSONL形式変換"),
        "es": ("Preprocesamiento y Distribución del Dataset de Entrenamiento", "Extracción Masiva de Corpus de Empatía y Apoyo Emocional", "Diálogos Emocionales (100k) + Transcripciones de Crisis -> Formato Llama 3.1 JSONL"),
        "zh-Hans": ("训练数据集全流程预处理与情感类别分布分析", "超大规模韩语同理心共情心理咨询语料库清洗与提取", "AI-Hub 情感对话 (10万条) + 心理危机干预脚本 → 统一 Llama 3.1 JSONL 训练集"),
        "zh-Hant": ("訓練資料集全流程預處理與情感類別分布分析", "超大規模韓語同理心共情心理諮詢語料庫清洗與提取", "AI-Hub 情感對話 (10萬條) + 心理危機干預腳本 → 統一 Llama 3.1 JSONL 訓練集"),
    },
    "2026-04-03-maeumjigi-5": {
        "en": ("Validation Metrics & Baseline Evaluation (M0~M6)", "Quantitative Benchmark: BLEU-4, ROUGE-L, BERTScore", "Filtering Hallucinations & Measuring Counseling Empathy Scores"),
        "ja": ("検証メトリクス＆ベースライン評価 (M0~M6)", "定量的ベンチマーク: BLEU-4, ROUGE-L, BERTScore 多角分析", "幻覚のフィルタリングと共感相談スコアの定量的測定"),
        "es": ("Métricas de Validación y Evaluación Baseline (M0~M6)", "Benchmark Cuantitativo: BLEU-4, ROUGE-L, BERTScore", "Filtrado de Alucinaciones y Puntuación de Empatía en Diálogo"),
        "zh-Hans": ("评估指标体系构建与基线模型客观量化评测 (M0~M6)", "全面量化基准测试：BLEU-4、ROUGE-L 与 BERTScore 多维对比", "严格过滤大模型事实性幻觉 (Hallucination) 并精确量化共情关怀评分"),
        "zh-Hant": ("評估指標體系構建與基準模型客觀量化評測 (M0~M6)", "全面量化基準測試：BLEU-4、ROUGE-L 與 BERTScore 多維對比", "嚴格過濾大模型事實性幻覺 (Hallucination) 並精確量化共情關懷評分"),
    },
    "2026-04-05-maeumjigi-6": {
        "en": ("Frontend Architecture & Mobile Bug Triage", "React Native Client & FastAPI Integration", "State Management, Error Boundaries, Real-time Chat UI Debugging"),
        "ja": ("フロントエンド設計とモバイルバグ修正", "React Nativeクライアント＆FastAPIバックエンド統合", "状態管理、エラーバウンダリ、リアルタイム相談UIデバッグ"),
        "es": ("Arquitectura Frontend y Depuración en Móvil", "Integración de Cliente React Native y Backend FastAPI", "Gestión de Estado, Error Boundaries y UI de Chat en Tiempo Real"),
        "zh-Hans": ("前端架构设计与移动端跨平台疑难 Bug 深度排查", "React Native 客户端与 FastAPI 高性能异步后端深度打通", "全局状态机管理、全局异常边界保护 (Error Boundaries) 与实时对话 UI 调优"),
        "zh-Hant": ("前端架構設計與行動端跨平台疑難 Bug 深度排查", "React Native 客戶端與 FastAPI 高效能非同步後端深度打通", "全域狀態機管理、全域例外邊界保護 (Error Boundaries) 與即時對話 UI 調優"),
    },
    "2026-04-07-maeumjigi-7": {
        "en": ("Synthetic Data Pipeline (v5) & Model Fine-Tuning", "Comparative Analysis of Emotion-to-Daily Mix Ratios", "7:3 Golden Ratio Selected for Optimal Emotional Resonance"),
        "ja": ("合成データセット(v5)生成＆モデル微調整", "感情対話と日常対話の混合比率比較分析 (5:5 vs 7:3 vs 8:2)", "情緒的共鳴に最適な 7:3 黄金比率モデルの採択"),
        "es": ("Pipeline de Datos Sintéticos (v5) y Ajuste Fino", "Análisis Comparativo de Proporciones de Diálogo (5:5 vs 7:3 vs 8:2)", "Selección de Proporción Dorada 7:3 para Máxima Resonancia Emocional"),
        "zh-Hans": ("合成数据增强流水线 (v5) 与模型参数微调 (Fine-Tuning)", "深度对比分析共情关怀对话与日常闲聊配比 (5:5 vs 7:3 vs 8:2)", "经过严谨盲测确立兼顾同理心与自然流畅度的 7:3 黄金配比模型方案"),
        "zh-Hant": ("合成資料增強流水線 (v5) 與模型參數微調 (Fine-Tuning)", "深度對比分析共情關懷對話與日常閒聊配比 (5:5 vs 7:3 vs 8:2)", "經過嚴謹盲測確立兼顧同理心與自然流暢度的 7:3 黃金配比模型方案"),
    },
    "2026-04-08-maeumjigi-8": {
        "en": ("Colab GPU VRAM Optimization & Training Metrics", "Managing OOM Limits on Large Language Model Fine-Tuning", "Gradient Accumulation (Steps=4), LoRA Rank=16, 4-bit Quantization"),
        "ja": ("Colab GPU VRAM最適化＆学習メトリクス", "大規模言語モデルのOOM(メモリ不足)制約の克服", "勾配累積 (Steps=4)、LoRA Rank=16、QLoRA 4-bit量子化導入"),
        "es": ("Optimización de VRAM en Colab y Métricas de Entrenamiento", "Superando Límites de OOM en Modelos Masivos de Lenguaje", "Acumulación de Gradientes (Steps=4), LoRA Rank=16, Cuantización QLoRA 4-bit"),
        "zh-Hans": ("Google Colab 显存极限制约突破与训练收敛指标复盘", "大语言模型参数高效微调面临的 OOM 显存崩溃防御实战", "梯度累加 (Steps=4)、LoRA Rank=16 与 QLoRA 4-bit 混合精度量化全开"),
        "zh-Hant": ("Google Colab 顯存極限制約突破與訓練收斂指標複盤", "大語言模型參數高效微調面臨的 OOM 顯存崩潰防禦實戰", "梯度累加 (Steps=4)、LoRA Rank=16 與 QLoRA 4-bit 混合精度量化全開"),
    },
    "2026-05-17-maeumjigi-19": {
        "en": ("Cloud Infrastructure & AWS Deployment Estimation", "EC2 GPU Server Cost Simulation & Cloud Database", "Balancing Monthly Budget vs Real-Time LLM Inference Latency"),
        "ja": ("クラウドインフラ＆AWSデプロイ見積もり試算", "EC2 GPUサーバーコストシミュレーション＆クラウドDB連携", "月額予算制約とリアルタイムLLM推論レイテンシの最適バランス"),
        "es": ("Infraestructura en la Nube y Estimación en AWS", "Simulación de Costes de GPU en EC2 y Base de Datos Cloud", "Equilibrio entre Presupuesto Mensual y Latencia de Inferencia LLM"),
        "zh-Hans": ("云原生底层基础设施架构设计与 AWS 云端部署成本测算", "AWS EC2 GPU 实例规格选型测算与高可用云端 PostgreSQL 数据库联调", "在有限学生毕业设计预算制约与大模型实时推理延迟之间寻求黄金平衡点"),
        "zh-Hant": ("雲端原生底層基礎設施架構設計與 AWS 雲端部署成本測算", "AWS EC2 GPU 執行個體規格選型測算與高可用雲端 PostgreSQL 資料庫聯調", "在有限學生畢業設計預算制約與大模型即時推理延遲之間尋求黃金平衡點"),
    },
    "2026-06-18-maeumjigi-23": {
        "en": ("Maeumjigi System: 6 Core Completed Features", "Unified Backend & Cloud DB for Web/App Co-Deployment", "1. Home Hero  2. Auth/Profile  3. AI Counselor  4. Crisis 109  5. Community  6. Mood Diary"),
        "ja": ("マウムジギ システム: 6大コア機能完成報告", "統合バックエンド＆クラウドDBによるWeb/アプリ同時提供", "① ホームHero  ② 認証/マイページ  ③ AI相談室  ④ 危機対応109  ⑤ 掲示板  ⑥ 気分日記"),
        "es": ("Sistema Maeumjigi: 6 Funciones Principales Completadas", "Backend Unificado y BD Cloud para Despliegue Web/App", "1. Inicio Hero  2. Auth/Perfil  3. Consejero IA  4. Crisis 109  5. Foro  6. Diario de Ánimo"),
        "zh-Hans": ("心之守护 (Maeumjigi) 系统：6 大核心业务功能全面交付落成", "统一云端后端与关系型数据库驱动 Web 官网与手机 App 双端协同交付", "① 首页引导看板  ② 用户鉴权与画像  ③ AI 共情咨询室  ④ 109 危机干预  ⑤ 树洞交流社区  ⑥ 心情晴雨表日记"),
        "zh-Hant": ("心之守護 (Maeumjigi) 系統：6 大核心業務功能全面交付落成", "統一雲端後端與關聯式資料庫驅動 Web 官網與手機 App 雙端協同交付", "① 首頁引導看板  ② 使用者鑑權與畫像  ③ AI 共情諮詢室  ④ 109 危機干預  ⑤ 樹洞交流社群  ⑥ 心情晴雨表日記"),
    },
}

def render_maeumjigi_slides_high_vis():
    print("\n--- Rendering High-Visibility Maeumjigi Slide Summary Cards (EN, JA, ES, ZH-Hans, ZH-Hant) ---")
    for ep_slug, ep_texts in MAEUMJIGI_SLIDES_DATA.items():
        for loc in ["en", "ja", "es", "zh-Hans", "zh-Hant"]:
            target_dir = os.path.join(LOCALES[loc], ep_slug, "images")
            os.makedirs(target_dir, exist_ok=True)
            plt.rcParams['font.family'] = FONT_FAMILIES[loc]

            h1, h2, sub = ep_texts[loc]

            fig, ax = plt.subplots(figsize=(14, 7.875), dpi=150) # 16:9 Slide Ratio
            fig.patch.set_facecolor('#0b1120')
            ax.set_facecolor('#0b1120')

            card = patches.FancyBboxPatch((0.6, 0.6), 12.8, 6.6, boxstyle="round,pad=0.3",
                                          linewidth=2.5, edgecolor='#3b82f6', facecolor='#1e293b')
            ax.add_patch(card)

            bar = patches.Rectangle((1.2, 6.4), 11.6, 0.12, color='#38bdf8')
            ax.add_patch(bar)

            ax.text(7.0, 5.5, h1, color='#ffffff', fontsize=18, fontweight='bold', ha='center')
            ax.text(7.0, 4.6, h2, color='#38bdf8', fontsize=15, fontweight='bold', ha='center')

            inner = patches.FancyBboxPatch((1.4, 1.4), 11.2, 2.5, boxstyle="round,pad=0.25",
                                          linewidth=1.8, edgecolor='#475569', facecolor='#0b1120')
            ax.add_patch(inner)
            ax.text(7.0, 2.65, sub, color='#f1f5f9', fontsize=13.5,
                    fontweight='medium', ha='center', va='center', wrap=True)

            ax.text(7.0, 1.0, "Maeumjigi AI Engineering Capstone Series", color='#94a3b8', fontsize=11, ha='center')

            ax.set_xlim(0, 14)
            ax.set_ylim(0.4, 7.875)
            ax.axis('off')
            plt.tight_layout()

            out_path = os.path.join(target_dir, "01_cover.png")
            fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
            plt.close()
            print(f"  [OK] [{loc}] Rendered Maeumjigi slide card: {ep_slug}/01_cover.png")


def main():
    print("================================================================================")
    print("STARTING HIGH-VISIBILITY MASTER DIAGRAM RENDERING FOR ALL 6 LOCALES")
    print("================================================================================")
    render_threat_model_high_vis()
    render_security_pipeline_high_vis()
    render_dns_diagram_high_vis()
    render_indexing_pipeline_high_vis()
    render_ads_txt_crawler_high_vis()
    render_anpr_diagram_high_vis()
    render_rl_diagram_high_vis()
    render_safety_wrapper_flowchart_high_vis()
    render_maeumjigi_slides_high_vis()
    print("\n================================================================================")
    print("ALL 9 DIAGRAM CATEGORIES GENERATED WITH ENLARGED, HIGH-VISIBILITY TYPOGRAPHY!")
    print("================================================================================")


if __name__ == "__main__":
    main()
