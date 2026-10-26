#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Vertical & High-Visibility Diagram Generator for Global Dev Blog
Renders large, bold, crystal-clear typography across all 6 locales:
[en, ko, ja, es, zh-Hans, zh-Hant]

Key Innovation:
- Replaces wide multi-column squished layouts with vertical full-width stacked layouts.
- Canvas width: ~920px (matches blog max-width 1:1 on desktop/tablet).
- Fonts: 20~22pt Title, 16.5~18.5pt Box Header, 14~15.5pt Bullets & Descriptions.
- Text is massive, bold, and instantly readable without zooming in.
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
# 1. THREAT MODELING (01_threat_model.png) - VERTICAL TOP / BOTTOM LAYOUT
# ==============================================================================
THREAT_TEXTS_VERTICAL = {
    "ko": {
        "title": "위협 모델링: 동적 웹 서버 vs 정적 사이트(SSG)",
        "subtitle": "공격 표면(Attack Surface) 및 런타임 침해 위협 심층 비교",
        "top_title": "[위협 노출] 전통적 동적 웹 서버 (Node.js / Django)",
        "top_desc": (
            "• 24시간 상시 대기 포트: 외부 침투 경로 항시 노출 (Port 80/443)\n"
            "• 데이터베이스 계층: SQL 인젝션 및 인증 토큰 탈취 위험 상존\n"
            "• 런타임 템플릿 실행: 원격 코드 실행(RCE) 침해 가능성\n"
            "• 서버 리소스 착취: 메모리 고갈 및 분산 서비스 거부(DoS) 공격 노출\n"
            "• npm 취약 패키지: 프로덕션 런타임에서 실시간 공격 체결"
        ),
        "bot_title": "[보안 격리] 모던 정적 사이트 (GitHub Pages CDN)",
        "bot_desc": (
            "• 빌드 시점 사전 컴파일: 순수 정적 파일(HTML/CSS/JS)만 제공\n"
            "• 상시 서버 프로세스 전무: 공격 가능한 백엔드 데몬 부재\n"
            "• 데이터베이스 포트 없음: SQL 인젝션 공격 표면 0%\n"
            "• 서버 사이드 RCE 완전 차단: 글로벌 엣지 CDN 읽기 전용 배포\n"
            "• npm audit 취약점 경고: 번들러 도구 한정, 런타임 위험 0%"
        ),
    },
    "en": {
        "title": "Threat Modeling: Dynamic Server vs Static Site (SSG)",
        "subtitle": "In-Depth Comparison of Attack Surface & Runtime Breach Risks",
        "top_title": "[VULNERABLE] Traditional Dynamic Web Server (Node / Django)",
        "top_desc": (
            "• 24/7 Active Listening Ports: External attack paths always open (80/443)\n"
            "• Database Connection Layer: Direct SQL Injection & credential theft risks\n"
            "• Runtime Template Execution: Server-side Remote Code Execution (RCE)\n"
            "• Host Resource Exploitation: Server memory exhaustion & DoS attack surface\n"
            "• npm Dependencies: High vulnerability packages executed live in production"
        ),
        "bot_title": "[SECURE] Modern Static Site Generation (GitHub Pages CDN)",
        "bot_desc": (
            "• Pre-compiled at Build Time: Delivers 100% pure static assets (HTML/CSS/JS)\n"
            "• Zero Running Backend Server: No vulnerable daemons or process execution\n"
            "• No Database Ports Exposed: SQL injection attack surface is completely 0%\n"
            "• Immune to Server-Side RCE: Read-only delivery from global Anycast edge CDN\n"
            "• npm Audit Vulnerabilities: Bundler scope only, exactly 0% runtime exploit risk"
        ),
    },
    "ja": {
        "title": "脅威モデリング: 動的サーバー vs 静的サイト(SSG)",
        "subtitle": "攻撃対象領域(Attack Surface)と実行時侵害リスクの深層比較",
        "top_title": "[脆弱性露出] 伝統的動的サーバー (Node.js / Django)",
        "top_desc": (
            "• 24時間常時待受ポート: 外部侵入経路が常に露出 (Port 80/443)\n"
            "• データベース層: SQLインジェクションおよび認証情報奪取リスク\n"
            "• 動的テンプレート実行: リモートコード実行(RCE)の重大な脅威\n"
            "• サーバー資源搾取: メモリ枯渇およびDoS攻撃への脆弱性\n"
            "• npmパッケージ脆弱性: 本番ランタイムにおける実害エクスプロイト"
        ),
        "bot_title": "[セキュリティ隔離] 現代的静的サイト (GitHub Pages CDN)",
        "bot_desc": (
            "• ビルド時事前コンパイル: 純粋な静的ファイル(HTML/CSS/JS)のみ配信\n"
            "• 常時稼働プロセス皆無: 攻撃可能なバックエンドデーモン不在\n"
            "• DBポート完全非露出: SQLインジェクション攻撃対象領域 0%\n"
            "• サーバーRCE根本遮断: グローバルAnycast CDNによる読取専用配信\n"
            "• npm監査警告: ビルド時ツールに限定、実行時リスク 0%"
        ),
    },
    "es": {
        "title": "Modelado de Amenazas: Servidor Dinámico vs Sitio Estático (SSG)",
        "subtitle": "Comparación Profunda de Superficie de Ataque y Riesgos en Runtime",
        "top_title": "[VULNERABLE] Servidor Web Dinámico Tradicional (Node / Django)",
        "top_desc": (
            "• Puertos Abiertos 24/7: Superficie de ataque siempre expuesta (80/443)\n"
            "• Capa de Base de Datos: Riesgos directos de Inyección SQL y robo de Auth\n"
            "• Ejecución Dinámica de Plantillas: Vulnerabilidad a RCE en el servidor\n"
            "• Agotamiento de Recursos: Susceptible a saturación de memoria y DoS\n"
            "• Paquetes npm: Explotación directa de vulnerabilidades en producción"
        ),
        "bot_title": "[AISLAMIENTO SEGURO] Sitio Estático Moderno (GitHub Pages CDN)",
        "bot_desc": (
            "• Precompilado en Tiempo de Build: Entrega de activos 100% estáticos\n"
            "• Sin Servidor Backend en Ejecución: Cero demonios o procesos vulnerables\n"
            "• Sin Puertos de BD Expuestos: Superficie de ataque para SQLi = 0%\n"
            "• Inmune a RCE de Servidor: Entrega de solo lectura vía Anycast Edge CDN\n"
            "• Auditoría npm: Limitada al empaquetador de build, riesgo en runtime = 0%"
        ),
    },
    "zh-Hans": {
        "title": "威胁建模：动态服务器 vs 静态站点生成 (SSG)",
        "subtitle": "架构级攻击面 (Attack Surface) 与运行时风险深度剖析",
        "top_title": "[高危暴露] 传统动态 Web 服务器 (Node.js / Django)",
        "top_desc": (
            "• 24小时常开监听端口：外部网络渗透攻击面持续暴露 (Port 80/443)\n"
            "• 数据库数据交互层：面临 SQL 注入漏洞及鉴权凭证被窃取风险\n"
            "• 运行时模板动态解析：存在严重的远程代码执行 (RCE) 漏洞隐患\n"
            "• 主机操作系统资源剥夺：极易遭受内存耗尽与拒绝服务攻击 (DoS)\n"
            "• npm 依赖包漏洞链：生产环境运行时面临黑客真实反弹利用威胁"
        ),
        "bot_title": "[安全隔离] 现代静态站点架构 (GitHub Pages CDN)",
        "bot_desc": (
            "• 构建时预编译：100% 交付经哈希校验的纯静态文件 (HTML/CSS/JS)\n"
            "• 无后台驻留常驻进程：根本不存在可被入侵利用的 Node/Python 守护进程\n"
            "• 彻底物理隔离数据库端口：SQL 注入与数据库提权暴露面绝对为 0%\n"
            "• 免疫服务端 RCE 漏洞：全球 Anycast 边缘高速 CDN 只读安全分发\n"
            "• npm 依赖安全告警：仅局限于本地打包编译工具链，生产运行时风险为 0%"
        ),
    },
    "zh-Hant": {
        "title": "威脅建模：動態伺服器 vs 靜態網站生成 (SSG)",
        "subtitle": "架構級攻擊面 (Attack Surface) 與運行時風險深度剖析",
        "top_title": "[高危暴露] 傳統動態 Web 伺服器 (Node.js / Django)",
        "top_desc": (
            "• 24小時常開監聽埠：外部網路滲透攻擊面持續暴露 (Port 80/443)\n"
            "• 資料庫資料互動層：面臨 SQL 注入漏洞及鑑權憑證被竊取風險\n"
            "• 運行時模板動態解析：存在嚴重的遠端程式碼執行 (RCE) 漏洞隱患\n"
            "• 主機作業系統資源剝奪：極易遭受記憶體耗盡與拒絕服務攻擊 (DoS)\n"
            "• npm 依賴套件漏洞鏈：生產環境運行時面臨黑客真實反彈利用威脅"
        ),
        "bot_title": "[安全隔離] 現代靜態網站架構 (GitHub Pages CDN)",
        "bot_desc": (
            "• 構建時預編譯：100% 交付經雜湊校驗的純靜態檔案 (HTML/CSS/JS)\n"
            "• 無後台駐留常駐進程：根本不存在可被入侵利用的 Node/Python 守護進程\n"
            "• 徹底物理隔離資料庫埠：SQL 注入與資料庫提權暴露面絕對為 0%\n"
            "• 免疫伺服端 RCE 漏洞：全球 Anycast 邊緣高速 CDN 唯讀安全分發\n"
            "• npm 依賴安全告警：僅局限於本地打包編譯工具鏈，生產運行時風險為 0%"
        ),
    },
}

def render_vertical_threat_model():
    print("\n--- 1. Rendering Vertical Threat Model (All 6 Locales) ---")
    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-10-18-static-site-security-hardening", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = THREAT_TEXTS_VERTICAL[loc]

        fig, ax = plt.subplots(figsize=(9.2, 10.2), dpi=100)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        # Header
        ax.text(4.6, 9.75, data["title"], color='#ffffff', fontsize=21.5, fontweight='bold', ha='center')
        ax.text(4.6, 9.35, data["subtitle"], color='#38bdf8', fontsize=14.5, fontweight='bold', ha='center')

        # Top Box: Dynamic Server (Red)
        box_top = patches.FancyBboxPatch((0.4, 5.0), 8.4, 4.05, boxstyle="round,pad=0.25",
                                        linewidth=2.8, edgecolor='#ef4444', facecolor='#1e293b')
        ax.add_patch(box_top)

        ax.text(4.6, 8.65, data["top_title"], color='#fca5a5', fontsize=18.0, fontweight='bold', ha='center')
        ax.plot([0.8, 8.4], [8.4, 8.4], color='#ef4444', linewidth=1.8)

        ax.text(0.75, 8.0, data["top_desc"], color='#f8fafc', fontsize=15.0,
                fontweight='bold', ha='left', va='top', linespacing=1.75)

        # Bottom Box: Static Site (Green)
        box_bot = patches.FancyBboxPatch((0.4, 0.6), 8.4, 4.05, boxstyle="round,pad=0.25",
                                        linewidth=2.8, edgecolor='#10b981', facecolor='#1e293b')
        ax.add_patch(box_bot)

        ax.text(4.6, 4.25, data["bot_title"], color='#6ee7b7', fontsize=18.0, fontweight='bold', ha='center')
        ax.plot([0.8, 8.4], [4.0, 4.0], color='#10b981', linewidth=1.8)

        ax.text(0.75, 3.6, data["bot_desc"], color='#f8fafc', fontsize=15.0,
                fontweight='bold', ha='left', va='top', linespacing=1.75)

        ax.set_xlim(0, 9.2)
        ax.set_ylim(0.2, 10.2)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "01_threat_model.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered vertical threat model: {out_path}")


# ==============================================================================
# 2. SECURITY PIPELINE (02_security_pipeline.png) - VERTICAL STACKED
# ==============================================================================
SECURITY_PIPELINE_VERTICAL = {
    "ko": {
        "title": "정적 블로그 4단계 심층 보안 강화 파이프라인",
        "steps": [
            ("1. 시크릿 유출 스캔 (Git Secret Scanning)", "• API 키, PAT 토큰, 인증서 정규식 패턴 사전 검출 및 커밋 원천 차단", "#38bdf8"),
            ("2. 개인정보(PII) 격리 (Privacy Filter)", "• 전화번호, 주민등록번호, 팀원 실명 등 개인 식별 정보 자동 마스킹", "#818cf8"),
            ("3. 공급망(npm) 검토 (Supply Chain Audit)", "• npm audit fix 맹신 배제 및 빌드 무결성 보존, 런타임 영향도 기반 분류", "#fbbf24"),
            ("4. 클라이언트 프라이버시 (Client Privacy)", "• 엄격한 Referrer Policy 적용, Giscus 댓글 iframe 샌드박스화 및 .gitignore 강화", "#34d399"),
        ]
    },
    "en": {
        "title": "4-Layer Static Blog Security Hardening Pipeline",
        "steps": [
            ("1. Git Secret Scanning", "• Regex pattern detection for API keys, PAT tokens & certificates before commit", "#38bdf8"),
            ("2. PII Protection (Privacy Filter)", "• Automatic masking of phone numbers, resident IDs, and sensitive team privacy", "#818cf8"),
            ("3. Supply Chain Audit (npm)", "• Rational audit triage without breaking builds; isolate dev vs runtime scopes", "#fbbf24"),
            ("4. Client Privacy & Hardening", "• Strict Referrer Policy, sandboxed Giscus iframe comments & hardened .gitignore", "#34d399"),
        ]
    },
    "ja": {
        "title": "静的ブログ 4段階 多層セキュリティ強化パイプライン",
        "steps": [
            ("1. シークレット検知 (Secret Scan)", "• APIキー、PATトークン、証明書の正規表現パターンによるコミット前自動遮断", "#38bdf8"),
            ("2. 個人情報(PII)保護 (Privacy)", "• 電話番号・身元情報・チーム実名など機密プライバシーの自動マスキング", "#818cf8"),
            ("3. サプライチェーン監査 (npm)", "• npm audit fix の盲信・破壊を防止、実行時影響度に基づく論理的トリアージ", "#fbbf24"),
            ("4. クライアント保護 (Client Privacy)", "• 厳格なReferrer Policy適用、Giscus iframeサンドボックス化＆.gitignore強化", "#34d399"),
        ]
    },
    "es": {
        "title": "Pipeline de Blindaje de Seguridad en 4 Capas para Sitios Estáticos",
        "steps": [
            ("1. Escaneo de Secretos (Git Secret Scan)", "• Detección Regex de API keys, tokens PAT y certificados antes de cada commit", "#38bdf8"),
            ("2. Protección de PII (Filtro de Privacidad)", "• Enmascaramiento automático de teléfonos, números de identidad y datos privados", "#818cf8"),
            ("3. Auditoría de Cadena de Suministro (npm)", "• Triaje racional de npm audit sin romper dependencias; aislar ámbito de build", "#fbbf24"),
            ("4. Privacidad del Cliente y Blindaje", "• Referrer Policy estricta, Giscus sandbox iframe y archivo .gitignore blindado", "#34d399"),
        ]
    },
    "zh-Hans": {
        "title": "静态博客 4 级纵深安全防护全流程流水线",
        "steps": [
            ("1. 敏感凭证扫描 (Git Secret Scanning)", "• API Key、PAT 访问令牌与数字证书正则特征自动化检测与提交阻断", "#38bdf8"),
            ("2. 隐私数据隔离 (PII Privacy Filter)", "• 电话号码、居民身份证件与团队成员真实身份预编译脱敏掩码过滤", "#818cf8"),
            ("3. 软件供应链审计 (Supply Chain Audit)", "• 理性评估 npm audit 漏洞告警，杜绝盲目自动修复导致代码编译破坏", "#fbbf24"),
            ("4. 客户端隐私加固 (Client Privacy)", "• 配置严苛 Referrer Policy 策略、Giscus 评论 iframe 沙箱与 .gitignore 加固", "#34d399"),
        ]
    },
    "zh-Hant": {
        "title": "靜態網站 4 級縱深安全防護全流程流水線",
        "steps": [
            ("1. 敏感憑證掃描 (Git Secret Scanning)", "• API Key、PAT 存取權杖與數位憑證正則特徵自動化檢測與提交阻斷", "#38bdf8"),
            ("2. 隱私數據隔離 (PII Privacy Filter)", "• 電話號碼、居民身分證件與團隊成員真實身分預編譯去識別化遮罩過濾", "#818cf8"),
            ("3. 軟體供應鏈審計 (Supply Chain Audit)", "• 理性評估 npm audit 漏洞告警，杜絕盲目自動修復導致程式碼編譯破壞", "#fbbf24"),
            ("4. 客戶端隱私加固 (Client Privacy)", "• 配置嚴苛 Referrer Policy 策略、Giscus 評論 iframe 沙箱與 .gitignore 加固", "#34d399"),
        ]
    },
}

def render_vertical_security_pipeline():
    print("\n--- 2. Rendering Vertical Security Pipeline (All 6 Locales) ---")
    y_coords = [7.1, 5.2, 3.3, 1.4]

    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-10-18-static-site-security-hardening", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = SECURITY_PIPELINE_VERTICAL[loc]

        fig, ax = plt.subplots(figsize=(9.2, 9.4), dpi=100)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(4.6, 8.95, data["title"], color='#ffffff', fontsize=21.0, fontweight='bold', ha='center')

        for i, (title, desc, col) in enumerate(data["steps"]):
            y = y_coords[i]
            card = patches.FancyBboxPatch((0.4, y), 8.4, 1.5, boxstyle="round,pad=0.2",
                                         linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(card)
            
            ax.text(0.7, y + 1.05, title, color=col, fontsize=16.5, fontweight='bold', ha='left', va='center')
            ax.text(0.7, y + 0.45, desc, color='#f8fafc', fontsize=13.8, fontweight='bold', ha='left', va='center')

            if y > 1.5:
                arrow = patches.FancyArrowPatch((4.6, y - 0.05), (4.6, y - 0.35),
                                               arrowstyle='->', mutation_scale=20, color='#94a3b8', linewidth=2.5)
                ax.add_patch(arrow)

        ax.set_xlim(0, 9.2)
        ax.set_ylim(0.9, 9.4)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "02_security_pipeline.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered vertical security pipeline: {out_path}")


# ==============================================================================
# 3. DNS ROUTING ARCHITECTURE (01_dns_routing_architecture.png) - VERTICAL
# ==============================================================================
DNS_ROUTING_VERTICAL = {
    "ko": {
        "title": "글로벌 정적 엔지니어링 블로그 DNS & CDN 라우팅 아키텍처",
        "steps": [
            ("1. 도메인 등록기관 (Porkbun)", 
             "• 커스텀 도메인: globaldevlog.com 등록 및 무료 WHOIS 개인정보 보호 활성화\n• 공인 네임서버(NS) 위임: Cloudflare Anycast 글로벌 네임서버 지정", 
             "#38bdf8", 6.8),
            ("2. Cloudflare Edge DNS & Anycast 보안 보호막", 
             "• CNAME 플래트닝: 루트(@) 도메인을 GitHub Pages 오리진으로 직통 연동\n• CNAME www 리다이렉트 포워딩 & 전 세계 300+ 엣지 초고속 CDN 캐싱\n• 자동 유니버설 SSL 인증서(HTTPS) & DDoS 및 악성 봇 차단 보호막 가동", 
             "#f59e0b", 3.8),
            ("3. GitHub Pages 오리진 (Docusaurus SSG)", 
             "• static/CNAME 바인딩: 사전 컴파일된 다국어(6개 국어) 순수 정적 웹 서빙\n• 서버 호스팅 및 인프라 유지비용 $0 & 99.99% 고가용성 글로벌 엣지 전송", 
             "#10b981", 0.8),
        ]
    },
    "en": {
        "title": "Production DNS & CDN Routing Architecture for Static Engineering Blog",
        "steps": [
            ("1. Domain Registrar (Porkbun)", 
             "• Custom Domain: globaldevlog.com registration with free WHOIS Privacy Guard\n• Authoritative Nameserver (NS) delegation to Cloudflare Anycast servers", 
             "#38bdf8", 6.8),
            ("2. Cloudflare Edge DNS & Security Shield", 
             "• CNAME Flattening: Route apex (@) domain directly to GitHub Pages origin\n• CNAME www subdomain forwarding & 300+ global edge Anycast CDN caching\n• Automatic Universal SSL certificate (HTTPS) & L3/L4/L7 DDoS protection", 
             "#f59e0b", 3.8),
            ("3. GitHub Pages Origin (Docusaurus SSG)", 
             "• static/CNAME binding: Delivers pre-compiled 6-locale static assets (HTML/CSS/JS)\n• Zero cloud server infrastructure costs & 99.99% high availability delivery", 
             "#10b981", 0.8),
        ]
    },
    "ja": {
        "title": "グローバル静的ブログ DNS＆CDNルーティング・アーキテクチャ",
        "steps": [
            ("1. ドメインレジストラ (Porkbun)", 
             "• 独自ドメイン: globaldevlog.com 登録＆無料WHOISプライバシー保護\n• 権威ネームサーバー(NS)委任: Cloudflare Anycast NSサーバーを指定", 
             "#38bdf8", 6.8),
            ("2. Cloudflare Edge DNS ＆ Anycast セキュリティ防御", 
             "• CNAMEフラット化: ルート(@)をGitHub Pagesオリジンへ直接バインド\n• CNAME www転送設定＆全世界300+エッジAnycast CDN高速キャッシュ\n• 自動ユニバーサルSSL (HTTPS) ＆ DDoS・悪質ボット遮断シールド", 
             "#f59e0b", 3.8),
            ("3. GitHub Pages オリジン (Docusaurus SSG)", 
             "• static/CNAME バインド: 事前コンパイルされた6言語の静的ファイルを配信\n• サーバー維持インフラ費用 0円 ＆ 99.99% 高可用性グローバル配信", 
             "#10b981", 0.8),
        ]
    },
    "es": {
        "title": "Arquitectura de Enrutamiento DNS y CDN para Blog Estático",
        "steps": [
            ("1. Registrador de Dominio (Porkbun)", 
             "• Dominio: globaldevlog.com con protección de privacidad WHOIS gratuita\n• Delegación de servidores de nombres autoritativos (NS) hacia Cloudflare Anycast", 
             "#38bdf8", 6.8),
            ("2. Cloudflare Edge DNS y Escudo de Seguridad", 
             "• Aplanamiento CNAME: Enrutar ápice (@) directamente al origen de GitHub Pages\n• CNAME www hacia raíz & caché global Anycast CDN en más de 300 ciudades\n• Certificado SSL Universal automático (HTTPS) & protección Anti-DDoS y Bots", 
             "#f59e0b", 3.8),
            ("3. GitHub Pages Origen (Docusaurus SSG)", 
             "• Archivo static/CNAME: Entrega precompilada en 6 idiomas estáticos puros\n• Cero coste de infraestructura de servidor & 99.99% de alta disponibilidad", 
             "#10b981", 0.8),
        ]
    },
    "zh-Hans": {
        "title": "静态工程技术博客 DNS 与全球 CDN 智能路由架构",
        "steps": [
            ("1. 域名注册商 (Porkbun)", 
             "• 专属顶级域名：globaldevlog.com 注册并开启免费 WHOIS 隐私保护\n• 权威域名解析服务器 (NS) 委派：指向 Cloudflare 全球 Anycast 节点", 
             "#38bdf8", 6.8),
            ("2. Cloudflare 边缘 DNS 与 Anycast 安全防护层", 
             "• CNAME 展平技术：根域名 (@) 直通 GitHub Pages 源站，解析无损耗\n• CNAME www 自动跳转与全球 300+ 边缘数据中心 Anycast CDN 极速缓存\n• 自动化 Universal SSL 证书 (HTTPS) 签发与拦截 DDoS/恶意爬虫流量", 
             "#f59e0b", 3.8),
            ("3. GitHub Pages 源站 (Docusaurus SSG)", 
             "• static/CNAME 双向绑定：预编译 6 大语言纯静态站点资源包极速分发\n• 零云端服务器运营与维护成本支出，保障 99.99% 全天候超高可用交付", 
             "#10b981", 0.8),
        ]
    },
    "zh-Hant": {
        "title": "靜態工程技術網站 DNS 與全球 CDN 智慧路由架構",
        "steps": [
            ("1. 域名註冊商 (Porkbun)", 
             "• 專屬頂級域名：globaldevlog.com 註冊並開啟免費 WHOIS 隱私保護\n• 權威域名解析伺服器 (NS) 委派：指向 Cloudflare 全球 Anycast 節點", 
             "#38bdf8", 6.8),
            ("2. Cloudflare 邊緣 DNS 與 Anycast 安全防護層", 
             "• CNAME 展平技術：根域名 (@) 直通 GitHub Pages 源站，解析無損耗\n• CNAME www 自動跳轉與全球 300+ 邊緣資料中心 Anycast CDN 極速快取\n• 自動化 Universal SSL 證書 (HTTPS) 簽發與攔截 DDoS/惡意爬蟲流量", 
             "#f59e0b", 3.8),
            ("3. GitHub Pages 源站 (Docusaurus SSG)", 
             "• static/CNAME 雙向綁定：預編譯 6 大語言純靜態網站資源包極速分發\n• 零雲端伺服器營運與維護成本支出，保障 99.99% 全天候超高可用交付", 
             "#10b981", 0.8),
        ]
    },
}

def render_vertical_dns_architecture():
    print("\n--- 3. Rendering Vertical DNS Architecture (All 6 Locales) ---")
    posts_to_update = [
        "2026-10-20-custom-domain-adsense-seo-guide",
        "2026-10-21-github-pages-custom-domain-cloudflare-dns"
    ]

    for loc, root_dir in LOCALES.items():
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = DNS_ROUTING_VERTICAL[loc]

        fig, ax = plt.subplots(figsize=(9.2, 9.8), dpi=100)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(4.6, 9.35, data["title"], color='#ffffff', fontsize=20.0, fontweight='bold', ha='center')

        for title, desc, col, y in data["steps"]:
            h = 2.4 if y == 3.8 else 2.1
            card = patches.FancyBboxPatch((0.4, y), 8.4, h, boxstyle="round,pad=0.2",
                                         linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(card)
            
            ax.text(0.7, y + h - 0.5, title, color=col, fontsize=17.0, fontweight='bold', ha='left', va='center')
            ax.plot([0.7, 8.4], [y + h - 0.8, y + h - 0.8], color=col, linewidth=1.5)
            
            ax.text(0.7, y + (h - 0.8)/2, desc, color='#f8fafc', fontsize=13.8,
                    fontweight='bold', ha='left', va='center', linespacing=1.65)

            if y > 1.0:
                arrow = patches.FancyArrowPatch((4.6, y - 0.1), (4.6, y - 0.45),
                                               arrowstyle='->', mutation_scale=20, color='#94a3b8', linewidth=2.5)
                ax.add_patch(arrow)

        ax.set_xlim(0, 9.2)
        ax.set_ylim(0.4, 9.8)
        ax.axis('off')
        plt.tight_layout()

        for p_slug in posts_to_update:
            target_dir = os.path.join(root_dir, p_slug, "images")
            os.makedirs(target_dir, exist_ok=True)
            out_path = os.path.join(target_dir, "01_dns_routing_architecture.png")
            fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
            print(f"  [OK] [{loc}] Rendered vertical DNS: {out_path}")
        plt.close()


# ==============================================================================
# 4. INDEXING & ADSENSE PIPELINE (02_indexing_pipeline.png) - VERTICAL
# ==============================================================================
INDEXING_VERTICAL = {
    "ko": {
        "title": "글로벌 검색엔진 인덱싱 및 애드센스 수익화 파이프라인",
        "steps": [
            ("1. 구글 서치콘솔 (Google Search Console)", "• DNS TXT 소유권 확인, 6개 국어 sitemap.xml 제출, URL 실시간 색인 생성 요청", "#60a5fa"),
            ("2. 네이버 서치어드바이저 (Naver Search Advisor)", "• 호스트 단위 사이트 등록, HTML+메타태그 이중 인증, Yeti 검색로봇 수집 가속", "#4ade80"),
            ("3. Bing 웹마스터 & AI 검색 (Bing & Copilot)", "• GSC 원클릭 즉시 동기화, IndexNow 실시간 URL 전송 API, ChatGPT Search 반영", "#2dd4bf"),
            ("4. 구글 애드센스 (Google AdSense 승인)", "• Apex 커스텀 루트 도메인 승인, static/ads.txt 배포 검증, IT 고단가 광고 입찰", "#fbbf24"),
        ]
    },
    "en": {
        "title": "Global Search Engine Indexing & AdSense Monetization Pipeline",
        "steps": [
            ("1. Google Search Console", "• DNS TXT ownership verification, 6 sitemaps submission & live URL inspections", "#60a5fa"),
            ("2. Naver Search Advisor", "• Host-level registration, HTML+Meta dual auth & Yeti crawler priority indexing", "#4ade80"),
            ("3. Bing Webmaster & AI Search", "• Instant 1-click GSC import, IndexNow real-time URL push API & Copilot ingestion", "#2dd4bf"),
            ("4. Google AdSense Monetization", "• Custom apex domain approval, static/ads.txt crawler verified & high technical CPM", "#fbbf24"),
        ]
    },
    "ja": {
        "title": "グローバル検索エンジン・インデックス登録＆AdSense収益化",
        "steps": [
            ("1. Google Search Console", "• DNS TXT 所有権確認、6言語対応 sitemap.xml 提出、URL検査による即時登録", "#60a5fa"),
            ("2. Naver Search Advisor", "• ホスト単位サイト登録、HTML＋メタタグ二重認証、Yetiクローラー優先収集", "#4ade80"),
            ("3. Bing Webmaster ＆ AI検索", "• GSCワンクリック同期、IndexNow即時URL送信API連携、ChatGPT Search反映", "#2dd4bf"),
            ("4. Google AdSense 収益化審査", "• 独自Apexルートドメイン審査通過、static/ads.txt正常配信、高単価技術広告", "#fbbf24"),
        ]
    },
    "es": {
        "title": "Pipeline de Indexación en Motores de Búsqueda y Monetización AdSense",
        "steps": [
            ("1. Google Search Console", "• Verificación DNS TXT, envío de 6 sitemaps multilingües e inspección de URL", "#60a5fa"),
            ("2. Naver Search Advisor", "• Registro de host, doble autenticación HTML+Meta y rastreo prioritario Yeti", "#4ade80"),
            ("3. Bing Webmaster y Búsqueda IA", "• Importación desde GSC, API IndexNow en tiempo real e indexación en Copilot", "#2dd4bf"),
            ("4. Google AdSense Monetización", "• Dominio Apex aprobado, static/ads.txt verificado y anuncios de alto CPM", "#fbbf24"),
        ]
    },
    "zh-Hans": {
        "title": "全球主流搜索引擎收录索引与 Google AdSense 商业变现流水线",
        "steps": [
            ("1. Google Search Console", "• DNS TXT 域名所有权极速验证，提交 6 大多语言 sitemap.xml 与实时收录", "#60a5fa"),
            ("2. Naver Search Advisor", "• 顶级主机层级站点注册，HTML+Meta 双保险认证，Yeti 爬虫高优先级抓取", "#4ade80"),
            ("3. Bing Webmaster 与 AI 搜索", "• 关联 GSC 一键极速导入配置，IndexNow 实时 URL 推送 API 与 Copilot 接入", "#2dd4bf"),
            ("4. Google AdSense 商业变现", "• 专属 Apex 顶级根域名顺利过审，static/ads.txt 成功挂载，锁定高价值 CPM", "#fbbf24"),
        ]
    },
    "zh-Hant": {
        "title": "全球主流搜尋引擎收錄索引與 Google AdSense 商業變現流水線",
        "steps": [
            ("1. Google Search Console", "• DNS TXT 網域名稱所有權極速驗證，提交 6 大多語言 sitemap.xml 與即時收錄", "#60a5fa"),
            ("2. Naver Search Advisor", "• 頂級主機層級網站註冊，HTML+Meta 雙保險認證，Yeti 爬蟲高優先級抓取", "#4ade80"),
            ("3. Bing Webmaster 與 AI 搜尋", "• 關聯 GSC 一鍵極速匯入配置，IndexNow 即時 URL 推送 API 與 Copilot 接入", "#2dd4bf"),
            ("4. Google AdSense 商業變現", "• 專屬 Apex 頂級根網域名稱順利過審，static/ads.txt 成功掛載，鎖定高價值 CPM", "#fbbf24"),
        ]
    },
}

def render_vertical_indexing_pipeline():
    print("\n--- 4. Rendering Vertical Indexing Pipeline (All 6 Locales) ---")
    y_coords = [7.1, 5.2, 3.3, 1.4]

    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-10-20-custom-domain-adsense-seo-guide", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = INDEXING_VERTICAL[loc]

        fig, ax = plt.subplots(figsize=(9.2, 9.4), dpi=100)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(4.6, 8.95, data["title"], color='#ffffff', fontsize=21.0, fontweight='bold', ha='center')

        for i, (title, desc, col) in enumerate(data["steps"]):
            y = y_coords[i]
            card = patches.FancyBboxPatch((0.4, y), 8.4, 1.5, boxstyle="round,pad=0.2",
                                         linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(card)
            
            ax.text(0.7, y + 1.05, title, color=col, fontsize=16.5, fontweight='bold', ha='left', va='center')
            ax.text(0.7, y + 0.45, desc, color='#f8fafc', fontsize=13.8, fontweight='bold', ha='left', va='center')

            if y > 1.5:
                arrow = patches.FancyArrowPatch((4.6, y - 0.05), (4.6, y - 0.35),
                                               arrowstyle='->', mutation_scale=20, color='#94a3b8', linewidth=2.5)
                ax.add_patch(arrow)

        ax.set_xlim(0, 9.2)
        ax.set_ylim(0.9, 9.4)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "02_indexing_pipeline.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered vertical indexing pipeline: {out_path}")


# ==============================================================================
# 5. ADS.TXT CRAWLER FLOW (01_ads_txt_crawler_flow.png) - VERTICAL
# ==============================================================================
ADS_TXT_VERTICAL = {
    "ko": {
        "title": "구글 애드센스 ads.txt 크롤러 검증 및 전송 라우팅 플로우",
        "steps": [
            ("1. 정적 소스코드 배포 (static/ads.txt)", "• 게시자 ID 선언 (google.com, pub-XXXXX, DIRECT, f08c47fec0942fa0), 순수 UTF-8 포맷", "#38bdf8"),
            ("2. CDN 엣지 및 글로벌 배포 (GitHub & Cloudflare)", "• 루트 URL 직통 라우팅 (globaldevlog.com/ads.txt), HTTP 200 OK, text/plain 서빙", "#f59e0b"),
            ("3. 애드센스 크롤러 순회 (Google-adstxt Bot)", "• Apex 루트 도메인 자동 스캔, 게시자 ID 일치 여부 대조 및 24시간 내 수집 체결", "#818cf8"),
            ("4. 광고 수익 손실 0건 보장 (Monetization Active)", "• ads.txt 상태: 승인됨 (녹색), 도메인 스푸핑 차단, 100% 정상 광고 입찰 가동", "#10b981"),
        ]
    },
    "en": {
        "title": "Google AdSense ads.txt Crawler Verification & Routing Flow",
        "steps": [
            ("1. Static Repository (static/ads.txt)", "• Publisher ID declaration (google.com, pub-XXXXX, DIRECT, f08c47fec0942fa0) in UTF-8", "#38bdf8"),
            ("2. Edge CDN & Origin Delivery (Cloudflare & GitHub)", "• Direct root URL routing (globaldevlog.com/ads.txt), HTTP 200 OK & MIME text/plain", "#f59e0b"),
            ("3. AdSense Bot Crawl (Google-adstxt)", "• Automated scan on Apex domain, instant record match verification within 24h", "#818cf8"),
            ("4. 100% Monetization Protection", "• Ads.txt status: Authorized (Green), zero revenue loss & full programmatic bidding", "#10b981"),
        ]
    },
    "ja": {
        "title": "Google AdSense ads.txt クローラー検証＆配信ルーティング",
        "steps": [
            ("1. 静的リポジトリ配置 (static/ads.txt)", "• パブリッシャーID宣言 (google.com, pub-XXXXX, DIRECT), UTF-8プレーンテキスト", "#38bdf8"),
            ("2. CDNエッジ＆オリジン配信 (Cloudflare & GitHub)", "• ルート直通URL配信 (globaldevlog.com/ads.txt), HTTP 200 OK, text/plainヘッダー", "#f59e0b"),
            ("3. AdSenseボット巡回 (Google-adstxt)", "• Apexルートドメイン自動スキャン、レコード一致検証および24時間以内巡回完了", "#818cf8"),
            ("4. 広告収益損失ゼロ防衛 (ステータス正常)", "• ads.txt ステータス: 承認済 (緑)、なりすまし防止、100%正常な広告配信", "#10b981"),
        ]
    },
    "es": {
        "title": "Flujo de Verificación y Enrutamiento del Rastreador ads.txt de AdSense",
        "steps": [
            ("1. Repositorio Estático (static/ads.txt)", "• Declaración de ID de editor (google.com, pub-XXXXX, DIRECT) en formato UTF-8", "#38bdf8"),
            ("2. Entrega en Edge CDN y Origen (Cloudflare & GitHub)", "• Enrutamiento directo (globaldevlog.com/ads.txt), Estado HTTP 200 OK y MIME text/plain", "#f59e0b"),
            ("3. Rastreo del Bot (Google-adstxt)", "• Escaneo automático en dominio Apex, verificación exacta de registros en 24h", "#818cf8"),
            ("4. Protección de Ingresos al 100%", "• Estado Ads.txt: Autorizado (Verde), prevención de fraude y monetización activa", "#10b981"),
        ]
    },
    "zh-Hans": {
        "title": "Google AdSense ads.txt 官方爬虫验证与 CDN 路由全流程",
        "steps": [
            ("1. 静态源码挂载 (static/ads.txt)", "• 声明专属发布商 ID 记录 (google.com, pub-XXXXX, DIRECT), 纯净 UTF-8 格式", "#38bdf8"),
            ("2. CDN 边缘直通分发 (GitHub & Cloudflare)", "• 根目录直通 URL 路由 (globaldevlog.com/ads.txt), HTTP 200 OK, text/plain 响应", "#f59e0b"),
            ("3. AdSense 爬虫巡检 (Google-adstxt)", "• 自动抓取 Apex 根域名文件，瞬时比对发布商记录，24 小时内完成收录认证", "#818cf8"),
            ("4. 商业变现收益零损失保障", "• ads.txt 状态：已获授权 (绿色)，彻底杜绝域名仿冒，保障高价值竞价投放", "#10b981"),
        ]
    },
    "zh-Hant": {
        "title": "Google AdSense ads.txt 官方爬蟲驗證與 CDN 路由全流程",
        "steps": [
            ("1. 靜態原始碼掛載 (static/ads.txt)", "• 聲明專屬發布商 ID 記錄 (google.com, pub-XXXXX, DIRECT), 純淨 UTF-8 格式", "#38bdf8"),
            ("2. CDN 邊緣直通分發 (GitHub & Cloudflare)", "• 根目錄直通 URL 路由 (globaldevlog.com/ads.txt), HTTP 200 OK, text/plain 回應", "#f59e0b"),
            ("3. AdSense 爬蟲巡檢 (Google-adstxt)", "• 自動抓取 Apex 根網域名稱檔案，瞬時比對發布商記錄，24 小時內完成收錄認證", "#818cf8"),
            ("4. 商業變現收益零損失保障", "• ads.txt 狀態：已獲授權 (綠色)，徹底杜絕網域名稱仿冒，保障高價值競價投放", "#10b981"),
        ]
    },
}

def render_vertical_ads_txt():
    print("\n--- 5. Rendering Vertical ads.txt Flow (All 6 Locales) ---")
    y_coords = [7.1, 5.2, 3.3, 1.4]

    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-10-21-static-site-adsense-ads-txt-guide", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = ADS_TXT_VERTICAL[loc]

        fig, ax = plt.subplots(figsize=(9.2, 9.4), dpi=100)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(4.6, 8.95, data["title"], color='#ffffff', fontsize=21.0, fontweight='bold', ha='center')

        for i, (title, desc, col) in enumerate(data["steps"]):
            y = y_coords[i]
            card = patches.FancyBboxPatch((0.4, y), 8.4, 1.5, boxstyle="round,pad=0.2",
                                         linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(card)
            
            ax.text(0.7, y + 1.05, title, color=col, fontsize=16.5, fontweight='bold', ha='left', va='center')
            ax.text(0.7, y + 0.45, desc, color='#f8fafc', fontsize=13.8, fontweight='bold', ha='left', va='center')

            if y > 1.5:
                arrow = patches.FancyArrowPatch((4.6, y - 0.05), (4.6, y - 0.35),
                                               arrowstyle='->', mutation_scale=20, color='#94a3b8', linewidth=2.5)
                ax.add_patch(arrow)

        ax.set_xlim(0, 9.2)
        ax.set_ylim(0.9, 9.4)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "01_ads_txt_crawler_flow.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered vertical ads.txt: {out_path}")


# ==============================================================================
# 6. WEBOTS RL Q-LEARNING (02_architecture.png) - VERTICAL
# ==============================================================================
RL_VERTICAL = {
    "ko": {
        "title": "Webots 자율주행 로봇 Q-Learning & Sim-to-Real 파이프라인",
        "steps": [
            ("1. 물리 시뮬레이션 환경 (Webots Physics)", "• Webots 2륜 차동 구동 로봇, 8방향 IR 적외선 센서 및 실시간 강체 충돌 물리 연산", "#38bdf8"),
            ("2. 상태 공간 이산화 (State Discretization)", "• 648개 이산 상태 공간 (거리 9구간 × 각도 8구간 × 장애물 회피 근접 벡터 융합)", "#818cf8"),
            ("3. 표 형식 Q-Learning (Tabular Bellman)", "• 벨만 최적 방정식 수렴, 도달(+100) / 충돌(-50) 보상, ε-탐욕(Epsilon) 최적 Q-Table", "#fbbf24"),
            ("4. Sim-to-Real 실기 전이 (Hardware Transfer)", "• 초고속 파이썬 소켓 IPC, HC-06 블루투스, 아두이노 Uno 모터 및 ArUco 비전 추적", "#10b981"),
        ]
    },
    "en": {
        "title": "Webots Autonomous Robot Q-Learning & Sim-to-Real Pipeline",
        "steps": [
            ("1. Simulation Physics Environment (Webots)", "• Differential robot, 8-direction IR sensors & real-time rigid body collision physics", "#38bdf8"),
            ("2. State Space Discretization (648 Bins)", "• 648 discrete state bins (Distance 9 bins × Heading 8 sectors × Obstacle vectors)", "#818cf8"),
            ("3. Tabular Q-Learning (Bellman Convergence)", "• Bellman optimization, Goal (+100) / Crash (-50) rewards & Epsilon-Greedy policy", "#fbbf24"),
            ("4. Sim-to-Real Transfer (Hardware Socket)", "• Python Socket IPC, HC-06 Bluetooth, Arduino Uno dual motors & ArUco vision tracking", "#10b981"),
        ]
    },
    "ja": {
        "title": "Webots 自律走行ロボット Q-Learning＆Sim-to-Real パイプライン",
        "steps": [
            ("1. 物理シミュレーション (Webots)", "• 2輪差動駆動ロボット、8方向IR距離センサー、リアルタイム衝突物理演算", "#38bdf8"),
            ("2. 状態空間の離散化 (648分割)", "• 648個の離散状態空間設計 (距離9分割 × 角度8セクター × 障害物接近ベクトル)", "#818cf8"),
            ("3. 表形式 Q-Learning (ベルマン方程式)", "• ベルマン最適方程式収束、到達(+100)/衝突(-50)報酬、ε-Greedy最適Q-Table", "#fbbf24"),
            ("4. Sim-to-Real 実機転移 (ハードウェア統合)", "• PythonソケットIPC、HC-06 Bluetooth、Arduino Unoモーター制御＆ArUco追跡", "#10b981"),
        ]
    },
    "es": {
        "title": "Robot Autónomo con Q-Learning en Webots y Pipeline Sim-to-Real",
        "steps": [
            ("1. Simulación Física en Webots", "• Robot diferencial, sensores IR de 8 vías y física de colisión en tiempo real", "#38bdf8"),
            ("2. Discretización de Estados (648 Bins)", "• 648 bins discretos (Distancia 9 bins × Ángulo 8 sectores × Vectores de proximidad)", "#818cf8"),
            ("3. Q-Learning Tabular (Ecuación Bellman)", "• Convergencia Bellman, Recompensa: Meta (+100) / Choque (-50) y Epsilon-Greedy", "#fbbf24"),
            ("4. Transferencia Sim-to-Real (Hardware)", "• Socket IPC Python, Bluetooth HC-06, motores Arduino Uno y visión ArUco en vivo", "#10b981"),
        ]
    },
    "zh-Hans": {
        "title": "Webots 自主移动机器人 Q-Learning 强化学习与虚实迁移流程",
        "steps": [
            ("1. 物理仿真实验环境 (Webots Physics)", "• 双轮差速底盘底座、8 方向红外测距传感器与实时刚体碰撞动力学计算", "#38bdf8"),
            ("2. 状态空间连续值离散化 (648 Bins)", "• 规划构建 648 个离散 Bin (距离 9 档 × 朝向 8 扇区 × 近邻障碍物排斥向量)", "#818cf8"),
            ("3. 表格式 Q-Learning 求解 (Bellman 收敛)", "• 贝尔曼最优方程收敛、到达(+100)/碰撞(-50)密集奖励与 ε-贪婪策略", "#fbbf24"),
            ("4. 虚实无缝迁移落地 (Sim-to-Real)", "• Python Socket IPC 通信、HC-06 蓝牙串口、Arduino Uno 与顶置 ArUco 视觉追踪", "#10b981"),
        ]
    },
    "zh-Hant": {
        "title": "Webots 自主移動機器人 Q-Learning 強化學習與虛實遷移流程",
        "steps": [
            ("1. 物理仿真實驗環境 (Webots Physics)", "• 雙輪差速底盤底座、8 方向紅外測距感測器與即時剛體碰撞動力學計算", "#38bdf8"),
            ("2. 狀態空間連續值離散化 (648 Bins)", "• 規劃構建 648 個離散 Bin (距離 9 檔 × 朝向 8 扇區 × 近鄰障礙物排斥向量)", "#818cf8"),
            ("3. 表格式 Q-Learning 求解 (Bellman 收斂)", "• 貝爾曼最優方程收斂、到達(+100)/碰撞(-50)密集獎勵與 ε-貪婪策略", "#fbbf24"),
            ("4. 虛實無縫遷移落地 (Sim-to-Real)", "• Python Socket IPC 通訊、HC-06 藍牙串口、Arduino Uno 與頂置 ArUco 視覺追蹤", "#10b981"),
        ]
    },
}

def render_vertical_rl_architecture():
    print("\n--- 6. Rendering Vertical RL Q-Learning Architecture (All 6 Locales) ---")
    y_coords = [7.1, 5.2, 3.3, 1.4]

    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-05-17-rl-qlearning-1", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = RL_VERTICAL[loc]

        fig, ax = plt.subplots(figsize=(9.2, 9.4), dpi=100)
        fig.patch.set_facecolor('#0b1120')
        ax.set_facecolor('#0b1120')

        ax.text(4.6, 8.95, data["title"], color='#ffffff', fontsize=21.0, fontweight='bold', ha='center')

        for i, (title, desc, col) in enumerate(data["steps"]):
            y = y_coords[i]
            card = patches.FancyBboxPatch((0.4, y), 8.4, 1.5, boxstyle="round,pad=0.2",
                                         linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(card)
            
            ax.text(0.7, y + 1.05, title, color=col, fontsize=16.5, fontweight='bold', ha='left', va='center')
            ax.text(0.7, y + 0.45, desc, color='#f8fafc', fontsize=13.8, fontweight='bold', ha='left', va='center')

            if y > 1.5:
                arrow = patches.FancyArrowPatch((4.6, y - 0.05), (4.6, y - 0.35),
                                               arrowstyle='->', mutation_scale=20, color='#94a3b8', linewidth=2.5)
                ax.add_patch(arrow)

        ax.set_xlim(0, 9.2)
        ax.set_ylim(0.9, 9.4)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "02_architecture.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered vertical RL architecture: {out_path}")


# ==============================================================================
# 7. SAFETY WRAPPER FLOWCHART (02_presentation.png) - VERTICAL FLOWCHART
# ==============================================================================
SAFETY_WRAPPER_VERTICAL = {
    "ko": {
        "title": "결정론적 Safety Wrapper 안전망 아키텍처 플로우차트",
        "steps": [
            ("1. 상담자 발화 입력 (User Utterance)", "• 사용자 고민 텍스트 및 실시간 상담 메시지 스트림 수신", "#38bdf8"),
            ("2. 위기 분류기 평가 (Crisis Classifier)", "• 자해 및 자살 위험 신호 실시간 감지 및 위험도 점수 산출", "#ec4899"),
            ("3. 안전 임계값 분기 (Bypass Decision)", "• 위험도 >= 임계값: 생성형 대규모 언어 모델(LLM) 100% 바이패스", "#fbbf24"),
            ("4. 결정론적 안전 래퍼 (Deterministic Wrapper)", "• 24시간 국가 자살예방 상담전화 (109 / 988) 긴급 개입 프로토콜 강제 주입", "#10b981"),
            ("5. 무환각 안전 출력 제공 (Safe Verified Output)", "• 환각 0% 공감 안전 메시지 및 생명의 전화 긴급 다이얼로그 카드 출력", "#34d399"),
        ]
    },
    "en": {
        "title": "Deterministic Safety Wrapper Architecture Flowchart",
        "steps": [
            ("1. User Utterance Input (Raw Text)", "• Real-time user message stream & counseling emotional utterance received", "#38bdf8"),
            ("2. Crisis Classifier Scoring", "• High-risk intent & suicide/self-harm severity assessment scoring", "#ec4899"),
            ("3. Dynamic Bypass Decision Gate", "• Risk >= Threshold: 100% completely bypass generative LLM response", "#fbbf24"),
            ("4. Deterministic Wrapper Protocol", "• Mandatory injection of 24/7 Lifeline Hotline (109 / 988) emergency directives", "#10b981"),
            ("5. Verified Safe Output Delivery", "• Zero hallucination empathetic safety response + emergency contact lifeline card", "#34d399"),
        ]
    },
    "ja": {
        "title": "決定論的 Safety Wrapper 安全網アーキテクチャ フローチャート",
        "steps": [
            ("1. 相談者発話テキスト入力 (User Input)", "• ユーザーの悩みメッセージおよびリアルタイム相談テキストを受信", "#38bdf8"),
            ("2. 危機分類器リスク判定 (Crisis Classifier)", "• 自傷・自死の兆候検知および危険度スコアのリアルタイム算出", "#ec4899"),
            ("3. 安全閾値バイパス分岐 (Bypass Gate)", "• 危険度 >= 閾値: 生成LLMを完全バイパスし幻覚リスクを根本排除", "#fbbf24"),
            ("4. 決定論的ラッパー注入 (Safety Wrapper)", "• 24時間国家緊急相談ホットライン (109 / 988) プロトコルを強制注入", "#10b981"),
            ("5. 検証済安全レスポンス提供 (Safe Output)", "• 幻覚0%の共感型安全メッセージ＋緊急ダイヤルカードを確実に表示", "#34d399"),
        ]
    },
    "es": {
        "title": "Flujograma de Arquitectura Determinista Safety Wrapper",
        "steps": [
            ("1. Entrada de Mensaje del Usuario", "• Recepción en tiempo real de texto de consulta y expresiones emocionales", "#38bdf8"),
            ("2. Clasificador de Crisis y Riesgo", "• Detección inmediata de señales de autolesión o suicidio y cálculo de riesgo", "#ec4899"),
            ("3. Compuerta de Decisión de Bypass", "• Riesgo >= Umbral: Bypass total del modelo generativo (cero alucinación)", "#fbbf24"),
            ("4. Protocolo Wrapper Determinista", "• Inyección obligatoria de líneas de ayuda de emergencia 24/7 (109 / 988)", "#10b981"),
            ("5. Entrega de Respuesta Segura Verificada", "• Mensaje empático seguro sin alucinaciones + tarjeta de contacto vital", "#34d399"),
        ]
    },
    "zh-Hans": {
        "title": "确定性 Safety Wrapper 兜底安全防护架构流程图",
        "steps": [
            ("1. 用户原始口语文本输入 (User Utterance)", "• 接收咨询者实时情感倾诉与心理咨询对话消息流", "#38bdf8"),
            ("2. 危机意图分类器精准研判 (Crisis Classifier)", "• 实时捕捉自残与自杀高危倾向，量化危机严重度打分", "#ec4899"),
            ("3. 动态熔断绕开决策 (Bypass Decision)", "• 风险分 >= 阈值：100% 物理熔断绕开生成式大模型", "#fbbf24"),
            ("4. 确定性安全包装器强介入 (Safety Wrapper)", "• 强制注入国家 24 小时援助热线 (109 / 988) 紧急应急干预指令", "#10b981"),
            ("5. 权威无幻觉安全输出交付 (Safe Output)", "• 0% 幻觉共情安抚文本响应 + 紧急援助电话绿色通道直通卡片", "#34d399"),
        ]
    },
    "zh-Hant": {
        "title": "確定性 Safety Wrapper 兜底安全防護架構流程圖",
        "steps": [
            ("1. 使用者原始口語文字輸入 (User Utterance)", "• 接收諮詢者即時情感傾訴與心理諮詢對話消息流", "#38bdf8"),
            ("2. 危機意圖分類器精準研判 (Crisis Classifier)", "• 即時捕捉自殘與自殺高危傾向，量化危機嚴重度打分", "#ec4899"),
            ("3. 動態熔斷繞開決策 (Bypass Decision)", "• 風險分 >= 閾值：100% 物理熔斷繞開生成式大模型", "#fbbf24"),
            ("4. 確定性安全包裝器強介入 (Safety Wrapper)", "• 強制注入國家 24 小時援助熱線 (109 / 988) 緊急應急干預指令", "#10b981"),
            ("5. 權威無幻覺安全輸出交付 (Safe Output)", "• 0% 幻覺共情安撫文字回應 + 緊急援助電話綠色通道直通卡片", "#34d399"),
        ]
    },
}

def render_vertical_safety_wrapper():
    print("\n--- 7. Rendering Vertical Safety Wrapper Flowchart (All 6 Locales) ---")
    y_coords = [7.5, 5.8, 4.1, 2.4, 0.7]

    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-06-18-maeumjigi-23", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = SAFETY_WRAPPER_VERTICAL[loc]

        fig, ax = plt.subplots(figsize=(9.2, 9.8), dpi=100)
        fig.patch.set_facecolor('#0a0f1d')
        ax.set_facecolor('#0a0f1d')

        ax.text(4.6, 9.35, data["title"], color='#ffffff', fontsize=20.5, fontweight='bold', ha='center')

        for i, (title, desc, col) in enumerate(data["steps"]):
            y = y_coords[i]
            card = patches.FancyBboxPatch((0.4, y), 8.4, 1.35, boxstyle="round,pad=0.2",
                                         linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(card)
            
            ax.text(0.7, y + 0.95, title, color=col, fontsize=16.0, fontweight='bold', ha='left', va='center')
            ax.text(0.7, y + 0.40, desc, color='#f8fafc', fontsize=13.5, fontweight='bold', ha='left', va='center')

            if y > 1.0:
                arrow = patches.FancyArrowPatch((4.6, y - 0.05), (4.6, y - 0.32),
                                               arrowstyle='->', mutation_scale=18, color='#94a3b8', linewidth=2.5)
                ax.add_patch(arrow)

        ax.set_xlim(0, 9.2)
        ax.set_ylim(0.4, 9.8)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "02_presentation.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered vertical safety wrapper: {out_path}")


# ==============================================================================
# 8. ANPR PIPELINE (01_pipeline_diagram.png) - 2-COLUMN X 3-ROW GRID
# ==============================================================================
ANPR_GRID = {
    "ko": {
        "title": "실시간 블랙박스 차선 침범 적발 및 초해상화 번호판 인식 6단계 파이프라인",
        "stages": [
            ("1. 블랙박스 영상 입력", "1080p 30fps 실시간 주행 비디오 수신", "#38bdf8"),
            ("2. 동적 차선 검출 (BEV)", "원근 투영 변환 및 동적 ROI 차선 경계선", "#818cf8"),
            ("3. 차량 및 번호판 탐지", "YOLOv3 차량 바운딩 및 YOLOv5 번호판 검출", "#a855f7"),
            ("4. CSRT 고속 공간 추적", "프레임 간 연속성 보장 실시간 트래커", "#ec4899"),
            ("5. EDSR 초해상화 복원", "저화질 번호판 영역 4배 심층 신경망 복원", "#f59e0b"),
            ("6. 번호판 OCR 다수결 투표", "한국 번호판 정규식 검증 및 시간축 앙상블", "#10b981"),
        ]
    },
    "en": {
        "title": "End-to-End Blackbox ANPR & Lane Intrusion Detection Architecture",
        "stages": [
            ("1. Video Feed Input", "1080p 30fps real-time driving footage stream", "#38bdf8"),
            ("2. Lane Detection (BEV)", "Bird's-Eye View dynamic ROI lane boundaries", "#818cf8"),
            ("3. Vehicle & Plate Detection", "YOLOv3 vehicle bbox & YOLOv5 plate network", "#a855f7"),
            ("4. CSRT Tracking", "Temporal continuity tracking & high-fps tracker", "#ec4899"),
            ("5. Super Resolution (EDSR)", "4x deep neural network plate reconstruction", "#f59e0b"),
            ("6. OCR Voting Ensemble", "Regex format validation & temporal consensus", "#10b981"),
        ]
    },
    "ja": {
        "title": "リアルタイム ドライブレコーダー車線侵犯検知＆超解像ANPR パイプライン",
        "stages": [
            ("1. ドラレコ映像入力", "1080p 30fps リアルタイム走行映像", "#38bdf8"),
            ("2. 動的車線検出 (BEV)", "俯瞰変換(BEV)＆動的ROI境界線抽出", "#818cf8"),
            ("3. 車両・ナンバー検出", "YOLOv3車両領域＆YOLOv5ナンバー検出", "#a855f7"),
            ("4. CSRT 高速追跡", "フレーム間連続性保証＆実時間トラッカー", "#ec4899"),
            ("5. EDSR 深層超解像", "低解像度ナンバーを4倍ディープラーニング復元", "#f59e0b"),
            ("6. OCR 多数決アンサンブル", "正規表現バリデーション＆時間軸投票統合", "#10b981"),
        ]
    },
    "es": {
        "title": "Arquitectura de Detección de Invasión de Carril y ANPR con Superresolución",
        "stages": [
            ("1. Entrada de Video", "Video de caja negra en tiempo real a 1080p 30fps", "#38bdf8"),
            ("2. Detección de Carril (BEV)", "Transformación BEV y límites dinámicos ROI", "#818cf8"),
            ("3. Vehículo y Matrícula", "Cajas YOLOv3 vehicular y red YOLOv5 de matrícula", "#a855f7"),
            ("4. Rastreo CSRT", "Continuidad temporal y rastreador en tiempo real", "#ec4899"),
            ("5. Superresolución (EDSR)", "Reconstrucción 4x con red neuronal profunda", "#f59e0b"),
            ("6. Ensamble de OCR", "Validación Regex y votación temporal mayoritaria", "#10b981"),
        ]
    },
    "zh-Hans": {
        "title": "实景行车记录仪车道违章压线抓拍与超分辨率车牌识别架构",
        "stages": [
            ("1. 实时视频流输入", "1080p 30fps 实景行车记录仪视频流", "#38bdf8"),
            ("2. 动态车道检测 (BEV)", "逆透视鸟瞰图变换与动态 ROI 兴趣边界", "#818cf8"),
            ("3. 目标车辆与车牌定位", "YOLOv3 车辆目标框与 YOLOv5 车牌定位网", "#a855f7"),
            ("4. CSRT 高速空间跟踪", "跨帧时序空间连续性高帧率实时运动追踪", "#ec4899"),
            ("5. EDSR 深度超分辨率", "模糊低像素车牌图像 4 倍深度重建超分", "#f59e0b"),
            ("6. OCR 时序加权投票", "标准车牌格式正则校验与多帧投票集成", "#10b981"),
        ]
    },
    "zh-Hant": {
        "title": "實景行車記錄器車道違章壓線抓拍與超解析度車牌辨識架構",
        "stages": [
            ("1. 即時視訊流輸入", "1080p 30fps 實景行車記錄器視訊流", "#38bdf8"),
            ("2. 動態車道檢測 (BEV)", "逆透視鳥瞰圖變換與動態 ROI 興趣邊界", "#818cf8"),
            ("3. 目標車輛與車牌定位", "YOLOv3 車輛目標框與 YOLOv5 車牌定位網", "#a855f7"),
            ("4. CSRT 高速空間追蹤", "跨幀時序空間連續性高幀率即時運動追蹤", "#ec4899"),
            ("5. EDSR 深度超解析度", "模糊低像素車牌圖像 4 倍深度重建超分", "#f59e0b"),
            ("6. OCR 時序加權投票", "標準車牌格式正則校驗與多幀投票集成", "#10b981"),
        ]
    },
}

def render_grid_anpr_pipeline():
    print("\n--- 8. Rendering 2x3 Grid ANPR Pipeline (All 6 Locales) ---")
    grid_positions = [
        (0.4, 5.8),  # Row 1 Left
        (4.8, 5.8),  # Row 1 Right
        (0.4, 3.4),  # Row 2 Left
        (4.8, 3.4),  # Row 2 Right
        (0.4, 1.0),  # Row 3 Left
        (4.8, 1.0),  # Row 3 Right
    ]

    for loc, root_dir in LOCALES.items():
        target_dir = os.path.join(root_dir, "2026-06-25-vision-anpr-1", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = FONT_FAMILIES[loc]
        data = ANPR_GRID[loc]

        fig, ax = plt.subplots(figsize=(9.2, 9.2), dpi=100)
        fig.patch.set_facecolor('#0b1329')
        ax.set_facecolor('#0b1329')

        ax.text(4.6, 8.6, data["title"], color='#ffffff', fontsize=19.5, fontweight='bold', ha='center')

        for i, (st_name, st_desc, col) in enumerate(data["stages"]):
            gx, gy = grid_positions[i]
            card = patches.FancyBboxPatch((gx, gy), 4.0, 1.9, boxstyle="round,pad=0.2",
                                         linewidth=2.5, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(card)
            
            ax.text(gx + 2.0, gy + 1.35, st_name, color=col, fontsize=15.5, fontweight='bold', ha='center')
            ax.plot([gx + 0.3, gx + 3.7], [gy + 1.05, gy + 1.05], color=col, linewidth=1.5)
            ax.text(gx + 2.0, gy + 0.55, st_desc, color='#f8fafc', fontsize=13.0,
                    fontweight='bold', ha='center', va='center', wrap=True)

        ax.set_xlim(0, 9.2)
        ax.set_ylim(0.5, 9.2)
        ax.axis('off')
        plt.tight_layout()

        out_path = os.path.join(target_dir, "01_pipeline_diagram.png")
        fig.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        plt.close()
        print(f"  [OK] [{loc}] Rendered grid ANPR: {out_path}")


def main():
    print("================================================================================")
    print("STARTING REDESIGNED VERTICAL & GRID HIGH-VISIBILITY DIAGRAM RENDERING")
    print("================================================================================")
    render_vertical_threat_model()
    render_vertical_security_pipeline()
    render_vertical_dns_architecture()
    render_vertical_indexing_pipeline()
    render_vertical_ads_txt()
    render_vertical_rl_architecture()
    render_vertical_safety_wrapper()
    render_grid_anpr_pipeline()
    print("\n================================================================================")
    print("ALL DIAGRAMS SUCCESSFULLY GENERATED WITH TRUE LARGE FONT VERTICAL ARCHITECTURE!")
    print("================================================================================")


if __name__ == "__main__":
    main()
