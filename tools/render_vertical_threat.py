#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update generate_high_visibility_diagrams.py to use vertical layout for 01_threat_model.png
and optimized layouts for all diagrams.
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
    print("\n--- Rendering Vertical High-Visibility Threat Model (All 6 Locales) ---")
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

if __name__ == "__main__":
    render_vertical_threat_model()
