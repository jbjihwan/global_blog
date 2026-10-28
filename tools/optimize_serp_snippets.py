# -*- coding: utf-8 -*-
import os
import re
import sys

BASE_DIR = r"D:\ai\antigravity\global_blog"

OPTIMIZATIONS = {
    # 1. Stanford CS146S #1
    "2026-10-22-stanford-cs146s-1": {
        "en": {
            "title": "Stanford CS146S #1: The Modern Software Developer Course Guide",
            "desc": "Complete guide & notes for Stanford CS146S: The Modern Software Developer. Learn Spec-Driven Development (SDD), AI coding agents, and loop engineering.",
            "keywords": ["Stanford CS146S", "The Modern Software Developer", "CS146S Course", "Spec-Driven Development", "Human-Agent Engineering", "Model Context Protocol MCP"]
        },
        "ko": {
            "title": "[스탠포드 CS146S #1] 현대 소프트웨어 개발자 (The Modern Software Developer)",
            "desc": "스탠포드 CS146S 1강 핵심 정리: 현대 소프트웨어 개발자(The Modern Software Developer). 스펙 주도 개발(SDD), AI 코딩 에이전트 루프 엔지니어링 완벽 해설.",
            "keywords": ["스탠포드 CS146S", "The Modern Software Developer", "현대 소프트웨어 개발자", "스펙 주도 개발", "에이전트 엔지니어링", "MCP"]
        },
        "ja": {
            "title": "[スタンフォード CS146S #1] 現代のソフトウェア開発者 (Modern Software Developer)",
            "desc": "スタンフォード大学CS146S第1講：The Modern Software Developer完全解説。仕様駆動開発（SDD）、自律AIエージェント、ループエンジニアリングの実践。",
            "keywords": ["スタンフォード CS146S", "The Modern Software Developer", "現代のソフトウェア開発者", "仕様駆動開発", "AIエージェント"]
        },
        "es": {
            "title": "Stanford CS146S #1: The Modern Software Developer Guía",
            "desc": "Guía de Stanford CS146S: The Modern Software Developer. Aprende Desarrollo Guiado por Especificaciones (SDD), agentes de código IA y Loop Engineering.",
            "keywords": ["Stanford CS146S", "The Modern Software Developer", "Desarrollo Guiado por Especificaciones", "Agentes de IA"]
        },
        "zh-Hans": {
            "title": "[斯坦福 CS146S #1] 现代软件工程师 (The Modern Software Developer)",
            "desc": "斯坦福大学 CS146S 第一讲精要：The Modern Software Developer。规范驱动开发（SDD）、自主 AI Agent 与现代软件工程协作范式。",
            "keywords": ["斯坦福 CS146S", "The Modern Software Developer", "现代软件工程师", "规范驱动开发", "AI Agent"]
        },
        "zh-Hant": {
            "title": "[史丹佛 CS146S #1] 現代軟體工程師 (The Modern Software Developer)",
            "desc": "史丹佛大學 CS146S 第 1 講精華：The Modern Software Developer。規範驅動開發（SDD）、自主 AI Agent 與現代軟體工程協作範式。",
            "keywords": ["史丹佛 CS146S", "The Modern Software Developer", "現代軟體工程師", "規範驅動開發", "AI Agent"]
        },
        "de": {
            "title": "Stanford CS146S #1: The Modern Software Developer Leitfaden",
            "desc": "Stanford CS146S Vorlesung 1: The Modern Software Developer. Spec-Driven Development (SDD), autonome KI-Coding-Agenten und modernes Loop Engineering.",
            "keywords": ["Stanford CS146S", "The Modern Software Developer", "Spec-Driven Development", "KI-Agenten"]
        },
        "fr": {
            "title": "Stanford CS146S #1: The Modern Software Developer Guide",
            "desc": "Guide Stanford CS146S : The Modern Software Developer. Maîtrisez le Spec-Driven Development (SDD), les agents IA autonomes et le Loop Engineering.",
            "keywords": ["Stanford CS146S", "The Modern Software Developer", "Spec-Driven Development", "Agents IA"]
        },
        "pt-BR": {
            "title": "Stanford CS146S #1: The Modern Software Developer Guia",
            "desc": "Guia Stanford CS146S: The Modern Software Developer. Aprenda Spec-Driven Development (SDD), agentes autônomos de IA e engenharia de loop moderno.",
            "keywords": ["Stanford CS146S", "The Modern Software Developer", "Spec-Driven Development", "Agentes de IA"]
        }
    },

    # 2. Static Site Security: npm audit truth
    "2026-10-18-static-site-security-hardening": {
        "en": {
            "title": "Fix npm Vulnerability & Truth of npm audit fix --force",
            "desc": "Fix npm vulnerability alerts without breaking builds. Learn why npm audit fix --force fails on static sites, and how to safely resolve GHSA security risks.",
            "keywords": ["npm vulnerability", "npm audit fix", "npm audit fix --force", "ghsa-rj75-hqrm-r3gf", "static site security", "npm supply chain security"]
        },
        "ko": {
            "title": "[2026] npm audit fix --force 함정과 해결법: npm 취약점 0개 만들기",
            "desc": "npm audit fix --force 실행 시 빌드가 깨지는 이유와 안전한 해결법. GHSA 공급망 보안 취약점의 실제 위협 모델 분석과 정적 사이트 4단계 보안 가이드.",
            "keywords": ["npm 취약점", "npm audit fix", "npm audit fix --force", "정적 사이트 보안", "GHSA 취약점", "Docusaurus 보안"]
        },
        "ja": {
            "title": "npm 脆弱性の真実：npm audit fix --force を避けて安全に解消する法",
            "desc": "npm 脆弱性の正しい解消法：npm audit fix --force でビルドが壊れる原因と、GHSAセキュリティアラートを安全にゼロにする静的サイト実践ガイド。",
            "keywords": ["npm 脆弱性", "npm audit fix", "npm audit fix --force", "静的サイトセキュリティ", "GHSA"]
        },
        "zh-Hant": {
            "title": "npm audit 是什麼？為何不應盲目執行 npm audit fix --force",
            "desc": "什麼是 npm audit？深入解析打包工具 45 個 npm 漏洞真相，為何 npm audit fix --force 會破壞構建，以及如何安全修復 GHSA 依賴漏洞。",
            "keywords": ["npm audit 是什麼", "npm audit fix --force", "npm 漏洞", "靜態網站安全", "GHSA 漏洞修復"]
        },
        "zh-Hans": {
            "title": "npm audit 是什么？为何不应盲目执行 npm audit fix --force",
            "desc": "什么是 npm audit？深入解析打包工具 45 个 npm 漏洞真相，为何 npm audit fix --force 会破坏构建，以及如何安全修复 GHSA 依赖漏洞。",
            "keywords": ["npm audit 是什么", "npm audit fix --force", "npm 漏洞", "静态网站安全", "GHSA 漏洞修复"]
        },
        "de": {
            "title": "npm audit fix --force: Schwachstellen beheben ohne Build-Fehler",
            "desc": "npm audit-Schwachstellen sicher beheben ohne Build-Fehler. Warum npm audit fix --force Builds zerstört und wie Sie GHSA-Sicherheitswarnungen richtig lösen.",
            "keywords": ["npm audit fix", "npm audit fix --force", "npm Schwachstellen", "statische Website Sicherheit"]
        },
        "fr": {
            "title": "Corriger les vulnérabilités npm sans casser vos builds",
            "desc": "Comment corriger les vulnérabilités npm audit sans casser vos builds. Pourquoi npm audit fix --force est dangereux et comment sécuriser un site statique.",
            "keywords": ["npm audit fix", "npm audit fix --force", "vulnérabilités npm", "sécurité site statique"]
        },
        "pt-BR": {
            "title": "Corrigir Vulnerabilidades npm sem Quebrar Builds de Produção",
            "desc": "Como resolver vulnerabilidades do npm audit sem quebrar builds. Por que npm audit fix --force falha em sites estáticos e como tratar alertas GHSA com segurança.",
            "keywords": ["npm audit fix", "npm audit fix --force", "vulnerabilidades npm", "segurança site estático"]
        },
        "es": {
            "title": "Cómo Solucionar Vulnerabilidades npm Sin Romper el Build",
            "desc": "Por qué npm audit fix --force rompe tu sitio web y cómo solucionarlo de forma segura. Análisis de modelos de amenazas en sitios estáticos y alertas GHSA.",
            "keywords": ["npm audit fix", "npm audit fix --force", "vulnerabilidades npm", "seguridad sitio estático"]
        }
    },

    # 3. Stanford CS146S #2
    "2026-10-23-stanford-cs146s-2": {
        "en": {
            "title": "Stanford CS146S #2: Coding LLMs & Prompt Engineering Guide",
            "desc": "Stanford CS146S Lecture 2: Inside coding LLMs, Pre-training, RLHF, Chain-of-Thought prompts, and the Swiss Cheese Model of AI code verification.",
            "keywords": ["Stanford CS146S", "Coding LLMs", "Prompt Engineering", "RLHF", "Chain of Thought", "Swiss Cheese Model"]
        },
        "ko": {
            "title": "[스탠포드 CS146S #2] 코딩 LLM 원리와 프롬프트 엔지니어링 실전",
            "desc": "스탠포드 CS146S 2강: 코딩 LLM의 작동 원리, 사전학습과 RLHF, CoT 프롬프트 기법 및 AI 코드 검증을 위한 스위스 치즈 모델 완벽 해설.",
            "keywords": ["스탠포드 CS146S", "코딩 LLM", "프롬프트 엔지니어링", "RLHF", "스위스 치즈 모델", "CoT"]
        },
        "ja": {
            "title": "[スタンフォード CS146S #2] コーディングLLMとプロンプト工学完全解説",
            "desc": "スタンフォード大学CS146S第2講：コーディングLLMの仕組み、事前学習、RLHF、思考の連鎖（CoT）、スイスチーズモデルによるAIコード検証。",
            "keywords": ["スタンフォード CS146S", "コーディングLLM", "プロンプトエンジニアリング", "RLHF"]
        },
        "zh-Hans": {
            "title": "[斯坦福 CS146S #2] 代码大模型与 Prompt 工程实战全解",
            "desc": "斯坦福大学 CS146S 第二讲：代码大模型预训练、RLHF机制、思维链（CoT）提示工程以及 AI 代码验证的瑞士奶酪模型。",
            "keywords": ["斯坦福 CS146S", "代码大模型", "Prompt 工程", "RLHF", "瑞士奶酪模型"]
        },
        "zh-Hant": {
            "title": "[史丹佛 CS146S #2] 代碼大模型與 Prompt 工程實戰全解",
            "desc": "史丹佛大學 CS146S 第二講：代碼大模型預訓練、RLHF機制、思維鏈（CoT）提示工程以及 AI 代碼驗證的瑞士奶酪模型。",
            "keywords": ["史丹佛 CS146S", "代碼大模型", "Prompt 工程", "RLHF", "瑞士奶酪模型"]
        },
        "es": {
            "title": "Stanford CS146S #2: LLMs de Código e Ingeniería de Prompts",
            "desc": "Stanford CS146S Lección 2: Mecánica de LLMs de código, Preentrenamiento, RLHF, prompts Chain-of-Thought y verificación de código con Modelo del Queso Suizo.",
            "keywords": ["Stanford CS146S", "LLMs de Código", "Ingeniería de Prompts", "RLHF"]
        },
        "de": {
            "title": "Stanford CS146S #2: Coding-LLMs & Prompt Engineering Guide",
            "desc": "Stanford CS146S Vorlesung 2: Funktionsweise von Coding-LLMs, Pre-Training, RLHF, Chain-of-Thought-Prompts und Verifikation im Schweizer-Käse-Modell.",
            "keywords": ["Stanford CS146S", "Coding LLMs", "Prompt Engineering", "RLHF"]
        },
        "fr": {
            "title": "Stanford CS146S #2 : LLMs de Code et Ingénierie de Prompts",
            "desc": "Stanford CS146S Cours 2 : Fonctionnement des LLMs de code, pré-entraînement, RLHF, prompts Chain-of-Thought et vérification par le modèle du fromage suisse.",
            "keywords": ["Stanford CS146S", "LLMs de code", "Ingénierie de Prompts", "RLHF"]
        },
        "pt-BR": {
            "title": "Stanford CS146S #2: LLMs de Código e Engenharia de Prompts",
            "desc": "Stanford CS146S Aula 2: Mecânica de LLMs de código, Pré-treinamento, RLHF, prompts Chain-of-Thought e verificação pelo Modelo do Queijo Suíço.",
            "keywords": ["Stanford CS146S", "LLMs de Código", "Engenharia de Prompts", "RLHF"]
        }
    },

    # 4. Custom Domain & Cloudflare DNS
    "2026-10-21-github-pages-custom-domain-cloudflare-dns": {
        "en": {
            "title": "GitHub Pages Custom Domain & Cloudflare DNS: Migration Guide",
            "desc": "Zero-downtime migration guide for GitHub Pages custom domain with Porkbun, Cloudflare DNS, CNAME flattening, SSL edge certificates, and Docusaurus.",
            "keywords": ["github-pages-custom-domain-cloudflare-dns", "GitHub Pages Custom Domain", "Cloudflare DNS Porkbun CNAME", "CNAME Flattening apex domain", "Free SSL Edge Certificate"]
        },
        "ko": {
            "title": "GitHub Pages 커스텀 도메인 & Cloudflare DNS 무중단 연동 가이드",
            "desc": "GitHub Pages에 Porkbun 커스텀 도메인과 Cloudflare Anycast DNS를 연결하는 완벽 가이드. CNAME Flattening 및 무료 SSL 인증서 무중단 설정법.",
            "keywords": ["GitHub Pages 커스텀 도메인", "Cloudflare DNS", "Porkbun 도메인", "CNAME Flattening", "무료 SSL 인증서"]
        }
    },

    # 5. AdSense & SEO Guide
    "2026-10-20-custom-domain-adsense-seo-guide": {
        "en": {
            "title": "Google AdSense on GitHub Pages: Custom Domain & ads.txt Setup",
            "desc": "How to get Google AdSense approved on GitHub Pages custom domains. Step-by-step ads.txt hosting, Porkbun & Cloudflare DNS, and multi-engine SEO setup.",
            "keywords": ["github pages google adsense", "Google AdSense ads.txt static site", "GitHub Pages Custom Domain AdSense", "Cloudflare DNS Porkbun CNAME"]
        },
        "ko": {
            "title": "GitHub Pages 애드센스 승인 가이드: 커스텀 도메인 & ads.txt 연동",
            "desc": "GitHub Pages 정적 사이트에서 구글 애드센스(Google AdSense) 승인받는 법. 커스텀 도메인 연결, 루트 ads.txt 설정 및 서치 콘솔 색인 최적화 가이드.",
            "keywords": ["GitHub Pages 구글 애드센스", "ads.txt 설정", "커스텀 도메인 애드센스", "Cloudflare DNS", "검색엔진 SEO"]
        }
    },

    # 6. Sim-to-Real RL Q-Learning #5
    "2026-05-21-rl-qlearning-5": {
        "en": {
            "title": "Sim-to-Real RL: Webots to Arduino with ArUco Vision Tracking (#5)",
            "desc": "Deploy simulation-trained 648-bin Q-Learning to a physical Arduino robot using overhead webcam homography and real-time ArUco 6-DoF marker pose tracking.",
            "keywords": ["Sim-to-Real Hardware Transfer", "ArUco Marker Pose Tracking", "Arduino Uno Robot Navigation", "Webots Q-Learning Transfer"]
        },
        "ko": {
            "title": "[RL Q-Learning #5] Sim-to-Real: Webots에서 아두이노 실물 로봇 이식",
            "desc": "Webots 강화학습으로 훈련된 648개 상태 Q-Learning 모델을 아두이노 우노 실물 로봇에 무선(HC-06) 및 ArUco 비전 추적으로 Sim-to-Real 이식 성공기.",
            "keywords": ["Sim-to-Real", "Webots 강화학습", "아두이노 로봇", "ArUco 마커 추적", "Q-Learning 실물 이식"]
        }
    }
}

def update_file(filepath, meta):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Frontmatter regex
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n(.*)$', content, re.DOTALL)
    if not m:
        print(f"Failed to parse frontmatter: {filepath}")
        return False

    fm_raw = m.group(1)
    body = m.group(2)

    # Replace title
    new_title = meta["title"].replace('"', '\\"')
    if re.search(r'^title:\s*.*$', fm_raw, re.MULTILINE):
        fm_raw = re.sub(r'^title:\s*.*$', f'title: "{new_title}"', fm_raw, flags=re.MULTILINE)
    else:
        fm_raw += f'\ntitle: "{new_title}"'

    # Replace description
    new_desc = meta["desc"].replace('"', '\\"')
    if re.search(r'^description:\s*.*$', fm_raw, re.MULTILINE):
        fm_raw = re.sub(r'^description:\s*.*$', f'description: "{new_desc}"', fm_raw, flags=re.MULTILINE)
    else:
        fm_raw += f'\ndescription: "{new_desc}"'

    # Replace keywords if provided
    if "keywords" in meta:
        kw_str = "[" + ", ".join([f'"{k}"' for k in meta["keywords"]]) + "]"
        if re.search(r'^keywords:\s*.*$', fm_raw, re.MULTILINE):
            fm_raw = re.sub(r'^keywords:\s*.*$', f'keywords: {kw_str}', fm_raw, flags=re.MULTILINE)
        else:
            fm_raw += f'\nkeywords: {kw_str}'

    new_content = f"---\n{fm_raw}\n---\n{body}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    print("=" * 70)
    print("🚀 [SERP 최적화] Google 1페이지 랭크 글 메타 제목/스니펫 일괄 최적화")
    print("=" * 70)

    updated_count = 0
    for post_dir, locale_dict in OPTIMIZATIONS.items():
        for locale, meta in locale_dict.items():
            if locale == "en":
                # Primary blog directory
                path = os.path.join(BASE_DIR, "blog", post_dir, "index.md")
            else:
                path = os.path.join(BASE_DIR, "i18n", locale, "docusaurus-plugin-content-blog", post_dir, "index.md")

            if update_file(path, meta):
                t_len = len(meta["title"])
                d_len = len(meta["desc"])
                print(f"[{locale:^7}] {post_dir}")
                print(f"          Title ({t_len:2d}c): {meta['title']}")
                print(f"          Desc  ({d_len:2d}c): {meta['desc'][:70]}...")
                updated_count += 1
            else:
                print(f"[SKIP/NF] [{locale}] {path}")

    print("=" * 70)
    print(f"✅ 총 {updated_count}개 파일의 SERP 스니펫 최적화 완료!")

if __name__ == "__main__":
    main()
