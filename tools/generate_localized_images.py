import os
from PIL import Image, ImageDraw, ImageFont
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
}

FONTS = {
    "ko": r"C:\Windows\Fonts\malgun.ttf",
    "ja": r"C:\Windows\Fonts\msgothic.ttc",
    "en": r"C:\Windows\Fonts\segoeui.ttf",
    "es": r"C:\Windows\Fonts\segoeui.ttf",
}

def get_font(loc, size):
    font_path = FONTS.get(loc, FONTS["en"])
    return ImageFont.truetype(font_path, size)

# ==========================================
# 1. SECURITY POST DIAGRAMS (4 Locales)
# ==========================================
def generate_security_diagrams():
    print("=== Generating Localized Security Diagrams ===")
    
    threat_texts = {
        "en": {
            "title": "Threat Modeling: Dynamic Server vs Static Site Generation (SSG)",
            "left_title": "Dynamic Server (Node/Django)",
            "left_desc": "- Active Listening Daemon (Port 80/443)\n- Database Connection (SQLi, Auth)\n- Dynamic Template Execution (RCE)\n- Server Memory Exploitation\n- npm Vulnerabilities = LIVE THREAT",
            "right_title": "Static Site (GitHub Pages CDN)",
            "right_desc": "- Pre-compiled Pure HTML/CSS/JS\n- NO Running Node Server in Prod\n- NO Database / Backend Ports\n- Immune to Server-Side RCE / DoS\n- npm audit in Bundler = ZERO RUNTIME RISK",
        },
        "ko": {
            "title": "위협 모델링: 동적 서버 vs 정적 사이트 생성(SSG) 보안 비교",
            "left_title": "동적 서버 (Node.js / Django)",
            "left_desc": "- 24시간 상시 대기 포트 (Port 80/443)\n- 데이터베이스 연결 (SQL 인젝션, 탈취)\n- 런타임 템플릿 실행 (원격 코드 실행 RCE)\n- 서버 메모리 / OS 침투 공격 노출\n- npm 취약점 = 런타임 실시간 침해 위협",
            "right_title": "정적 사이트 (GitHub Pages CDN)",
            "right_desc": "- 빌드 시점 사전 컴파일 (순수 HTML/CSS/JS)\n- 프로덕션 상시 Node 런타임 프로세스 전무\n- 노출된 DB 포트 및 백엔드 인터페이스 없음\n- 서버 사이드 RCE / DoS 공격 원천 무력화\n- 번들러 npm 취약점 경고 = 런타임 위험 0%",
        },
        "ja": {
            "title": "脅威モデリング: 動的サーバー vs 静的サイト生成(SSG)のセキュリティ比較",
            "left_title": "動的サーバー (Node.js / Django)",
            "left_desc": "- 常時リッスンポート (Port 80/443)\n- データベース接続 (SQLi、認証奪取)\n- テンプレート動的実行 (リモートコード実行 RCE)\n- サーバーメモリ・OSへの侵入攻撃リスク\n- npm脆弱性 ＝ 本番稼働時の実害脅威",
            "right_title": "静的サイト (GitHub Pages CDN)",
            "right_desc": "- ビルド時事前コンパイル (純粋なHTML/CSS/JS)\n- 本番環境でNodeサーバープロセス一切不在\n- DB接続ポートやバックエンドAPIの露出なし\n- サーバー側RCE / DoS攻撃の根本的遮断\n- バンドラーのnpm監査警告 ＝ 実行時リスク0%",
        },
        "es": {
            "title": "Modelado de Amenazas: Servidor Dinámico vs Generación de Sitio Estático (SSG)",
            "left_title": "Servidor Dinámico (Node / Django)",
            "left_desc": "- Demonio en Escucha Activa (Puerto 80/443)\n- Conexión a Base de Datos (SQLi, Robo de Auth)\n- Ejecución Dinámica de Plantillas (RCE)\n- Explotación de Memoria y SO del Servidor\n- Vulnerabilidades npm = AMENAZA EN TIEMPO REAL",
            "right_title": "Sitio Estático (GitHub Pages CDN)",
            "right_desc": "- HTML/CSS/JS Puro Precompilado en Build\n- SIN Servidor Node en Producción\n- SIN Base de Datos ni Puertos Expuestos\n- Inmune a RCE y DoS en el Servidor\n- npm audit en Bundler = CERO RIESGO EN RUNTIME",
        },
    }

    pipeline_texts = {
        "en": {
            "title": "Comprehensive 4-Layer Static Blog Security Hardening Pipeline",
            "steps": [
                ("1. Git Secret Scanning", "Regex detection for API keys,\nPAT tokens & certs", "#38bdf8"),
                ("2. PII Protection", "Phone & Resident Number\nRegex validation", "#818cf8"),
                ("3. Supply Chain Audit", "Rational triage of npm audit\nwithout breaking builds", "#fbbf24"),
                ("4. Client Privacy", "Referrer Policy, Giscus iframe\n& Strict .gitignore", "#34d399"),
            ]
        },
        "ko": {
            "title": "정적 블로그 4단계 심층 보안 강화 파이프라인",
            "steps": [
                ("1. 시크릿 유출 스캔", "API 키, 토큰, 인증서\n정규식 자동 탐지", "#38bdf8"),
                ("2. 개인정보(PII) 검증", "전화번호·주민번호·팀원 실명\n완전 격리 필터링", "#818cf8"),
                ("3. 공급망(npm) 검토", "npm audit fix 무차별 실행 배제\n영향도 기반 이성적 분류", "#fbbf24"),
                ("4. 클라이언트 프라이버시", "엄격한 Referrer Policy 설정\nGiscus iframe & .gitignore 보호", "#34d399"),
            ]
        },
        "ja": {
            "title": "静的ブログ 4段階 多層セキュリティ強化パイプライン",
            "steps": [
                ("1. シークレット検知", "APIキー、PATトークン、証明書\n正規表現による自動検知", "#38bdf8"),
                ("2. 個人情報(PII)保護", "電話番号・身元情報・チーム員名\n安全フィルタリング", "#818cf8"),
                ("3. サプライチェーン監査", "npm audit fix の盲信を排除\n影響度に基づく論理的トリアージ", "#fbbf24"),
                ("4. クライアント保護", "厳格なReferrer Policyの適用\nGiscus iframe ＆ .gitignore 強化", "#34d399"),
            ]
        },
        "es": {
            "title": "Pipeline de Blindaje de Seguridad en 4 Capas para Sitios Estáticos",
            "steps": [
                ("1. Escaneo de Secretos", "Detección Regex de API keys,\ntokens PAT y certificados", "#38bdf8"),
                ("2. Protección de PII", "Validación estricta de teléfonos\ny datos personales de terceros", "#818cf8"),
                ("3. Auditoría de Cadena", "Triaje racional de npm audit\nsin romper dependencias", "#fbbf24"),
                ("4. Privacidad del Cliente", "Referrer Policy estricta, Giscus\niframe y .gitignore blindado", "#34d399"),
            ]
        },
    }

    font_fam = {
        "ko": "Malgun Gothic",
        "ja": "MS Gothic",
        "en": "Segoe UI",
        "es": "Segoe UI",
    }

    for loc, root in LOCALES.items():
        target_dir = os.path.join(root, "2026-10-18-static-site-security-hardening", "images")
        os.makedirs(target_dir, exist_ok=True)
        t_data = threat_texts[loc]
        plt.rcParams['font.family'] = font_fam[loc]

        # 1. Threat Model
        fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')
        rect1 = patches.FancyBboxPatch((0.5, 1.0), 4.1, 3.5, boxstyle="round,pad=0.2", linewidth=2, edgecolor='#ef4444', facecolor='#1e293b')
        ax.add_patch(rect1)
        ax.text(2.55, 4.1, t_data["left_title"], color='#f87171', fontsize=11, fontweight='bold', ha='center')
        ax.text(2.55, 3.4, t_data["left_desc"], color='#cbd5e1', fontsize=8.5, ha='center', va='center', linespacing=1.4)
        
        rect2 = patches.FancyBboxPatch((5.4, 1.0), 4.1, 3.5, boxstyle="round,pad=0.2", linewidth=2, edgecolor='#10b981', facecolor='#1e293b')
        ax.add_patch(rect2)
        ax.text(7.45, 4.1, t_data["right_title"], color='#34d399', fontsize=11, fontweight='bold', ha='center')
        ax.text(7.45, 3.4, t_data["right_desc"], color='#cbd5e1', fontsize=8.5, ha='center', va='center', linespacing=1.4)
        
        ax.text(5.0, 4.85, t_data["title"], color='#ffffff', fontsize=12, fontweight='bold', ha='center')
        ax.set_xlim(0, 10)
        ax.set_ylim(0.5, 5.2)
        ax.axis('off')
        plt.tight_layout()
        fig.savefig(os.path.join(target_dir, "01_threat_model.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()

        # 2. Pipeline
        p_data = pipeline_texts[loc]
        fig, ax = plt.subplots(figsize=(10, 4.5), dpi=200)
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')
        
        for i, (st_title, st_desc, col) in enumerate(p_data["steps"]):
            x = 0.4 + i * 2.4
            rect = patches.FancyBboxPatch((x, 1.0), 2.2, 2.5, boxstyle="round,pad=0.15", linewidth=2, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + 1.1, 3.1, st_title, color=col, fontsize=9.5, fontweight='bold', ha='center')
            ax.text(x + 1.1, 2.0, st_desc, color='#e2e8f0', fontsize=8, ha='center', va='center', linespacing=1.35)
            if i < 3:
                arrow = patches.FancyArrowPatch((x + 2.25, 2.25), (x + 2.5, 2.25), arrowstyle='->', mutation_scale=15, color='#94a3b8', linewidth=2)
                ax.add_patch(arrow)
                
        ax.text(5.0, 4.2, p_data["title"], color='#ffffff', fontsize=12, fontweight='bold', ha='center')
        ax.set_xlim(0, 10)
        ax.set_ylim(0.5, 4.6)
        ax.axis('off')
        plt.tight_layout()
        fig.savefig(os.path.join(target_dir, "02_security_pipeline.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  [{loc}] Generated security diagrams successfully")

# ==========================================
# 2. ANPR PIPELINE DIAGRAMS (4 Locales)
# ==========================================
def generate_anpr_diagrams():
    print("=== Generating Localized ANPR Pipeline Diagrams ===")
    
    anpr_data = {
        "en": {
            "title": "End-to-End Blackbox ANPR & Lane Intrusion Detection Architecture",
            "stages": [
                ("1. Dashcam Input", "Real-Time 1080p\nDriving Footage"),
                ("2. Lane Detection", "Dynamic ROI &\nHough Boundary"),
                ("3. Vehicle / Plate", "YOLOv3 Vehicle ROI\n& YOLOv5 Plate Net"),
                ("4. CSRT Tracking", "Temporal Track &\nMotion Continuity"),
                ("5. Super Resolution", "EDSR_x4 Deep Net\nReconstruction"),
                ("6. OCR Ensemble", "Korean Regex &\nTemporal Voting"),
            ]
        },
        "ko": {
            "title": "실시간 블랙박스 차선 침범 적발 및 초해상화 번호판 인식 6단계 파이프라인",
            "stages": [
                ("1. 블랙박스 입력", "1080p 30fps 실시간\n차량 주행 비디오"),
                ("2. 동적 차선 검출", "원근 투영(BEV) &\n동적 ROI 경계선"),
                ("3. 차량/번호판 탐지", "YOLOv3 차량 바운딩\n& YOLOv5 번호판 망"),
                ("4. CSRT 고속 추적", "프레임간 연속성 &\n고속 실시간 트래커"),
                ("5. EDSR 초해상화", "저해상도 번호판\n4배 딥러닝 고화질 복원"),
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
    }

    font_fam = {
        "ko": "Malgun Gothic",
        "ja": "MS Gothic",
        "en": "Segoe UI",
        "es": "Segoe UI",
    }

    colors = ["#38bdf8", "#818cf8", "#a855f7", "#ec4899", "#f59e0b", "#10b981"]

    for loc, root in LOCALES.items():
        target_dir = os.path.join(root, "2026-06-25-vision-anpr-1", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = font_fam[loc]
        d = anpr_data[loc]

        fig, ax = plt.subplots(figsize=(11, 4.5), dpi=200)
        fig.patch.set_facecolor('#0b1329')
        ax.set_facecolor('#0b1329')

        for i, (st_name, st_desc) in enumerate(d["stages"]):
            x = 0.35 + i * 1.72
            col = colors[i]
            rect = patches.FancyBboxPatch((x, 1.0), 1.55, 2.5, boxstyle="round,pad=0.12", linewidth=2, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + 0.775, 3.1, st_name, color=col, fontsize=8.5, fontweight='bold', ha='center')
            ax.text(x + 0.775, 2.0, st_desc, color='#e2e8f0', fontsize=7.5, ha='center', va='center', linespacing=1.35)
            if i < 5:
                arrow = patches.FancyArrowPatch((x + 1.58, 2.25), (x + 1.76, 2.25), arrowstyle='->', mutation_scale=12, color='#94a3b8', linewidth=1.5)
                ax.add_patch(arrow)

        ax.text(5.5, 4.15, d["title"], color='#ffffff', fontsize=11.5, fontweight='bold', ha='center')
        ax.set_xlim(0, 11)
        ax.set_ylim(0.5, 4.6)
        ax.axis('off')
        plt.tight_layout()
        fig.savefig(os.path.join(target_dir, "01_pipeline_diagram.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  [{loc}] Generated ANPR pipeline diagram successfully")

# ==========================================
# 3. RL Q-LEARNING ARCHITECTURE (4 Locales)
# ==========================================
def generate_rl_diagrams():
    print("=== Generating Localized RL Q-Learning Diagrams ===")
    
    rl_data = {
        "en": {
            "title": "Webots Autonomous Robot Q-Learning Architecture & Sim-to-Real Pipeline",
            "blocks": [
                ("1. Physics Simulation", "Webots Differential Robot\nDistance Sensors (IR)", "#38bdf8"),
                ("2. State Discretization", "648 Discrete Bins\n(Dist 9 × Angle 8 × Obstacle)", "#818cf8"),
                ("3. Tabular Q-Learning", "Reward Shaping Optimization\nQ(s, a) Bellman Convergence", "#fbbf24"),
                ("4. Sim-to-Real Transfer", "Socket IPC -> Arduino Uno\nHC-06 & ArUco Vision Track", "#10b981"),
            ]
        },
        "ko": {
            "title": "Webots 자율주행 로봇 Q-Learning 아키텍처 및 Sim-to-Real 파이프라인",
            "blocks": [
                ("1. 물리 시뮬레이션 환경", "Webots 2륜 차동 구동 로봇\n거리 센서 (8방향 IR 계측)", "#38bdf8"),
                ("2. 상태 공간 이산화", "648개 이산 상태 공간 설계\n(거리 9구간 × 각도 8구간 × 장애물)", "#818cf8"),
                ("3. 표 형식 Q-Learning", "보상 함수 튜닝 및 최적화\nQ(s, a) 벨만 방정식 수렴", "#fbbf24"),
                ("4. Sim-to-Real 실기 전이", "소켓 IPC -> Arduino Uno\nHC-06 블루투스 & ArUco 비전", "#10b981"),
            ]
        },
        "ja": {
            "title": "Webots 自律走行ロボット Q-Learning アーキテクチャ＆Sim-to-Real パイプライン",
            "blocks": [
                ("1. 物理シミュレーション", "Webots 2輪差動駆動ロボット\n距離センサー (8方向IR計測)", "#38bdf8"),
                ("2. 状態空間の離散化", "648個の離散状態空間設計\n(距離9区間 × 角度8区間 × 障害物)", "#818cf8"),
                ("3. 表形式 Q-Learning", "報酬関数の最適化チューニング\nQ(s, a) ベルマン方程式収束", "#fbbf24"),
                ("4. Sim-to-Real 実機転移", "ソケットIPC -> Arduino Uno\nHC-06 Bluetooth ＆ ArUco視覚追跡", "#10b981"),
            ]
        },
        "es": {
            "title": "Arquitectura de Robot Autónomo con Q-Learning en Webots y Pipeline Sim-to-Real",
            "blocks": [
                ("1. Simulación Física", "Robot Diferencial en Webots\nSensores de Distancia IR", "#38bdf8"),
                ("2. Discretización de Estados", "648 Bins de Estados Discretos\n(Dist 9 × Ángulo 8 × Obstáculo)", "#818cf8"),
                ("3. Q-Learning Tabular", "Optimización de Recompensas\nConvergencia Bellman Q(s, a)", "#fbbf24"),
                ("4. Transferencia Sim-to-Real", "Socket IPC -> Arduino Uno\nBluetooth HC-06 y Visión ArUco", "#10b981"),
            ]
        },
    }

    font_fam = {
        "ko": "Malgun Gothic",
        "ja": "MS Gothic",
        "en": "Segoe UI",
        "es": "Segoe UI",
    }

    for loc, root in LOCALES.items():
        target_dir = os.path.join(root, "2026-05-17-rl-qlearning-1", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = font_fam[loc]
        d = rl_data[loc]

        fig, ax = plt.subplots(figsize=(10, 4.5), dpi=200)
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')

        for i, (b_title, b_desc, col) in enumerate(d["blocks"]):
            x = 0.4 + i * 2.4
            rect = patches.FancyBboxPatch((x, 1.0), 2.2, 2.5, boxstyle="round,pad=0.15", linewidth=2, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + 1.1, 3.1, b_title, color=col, fontsize=9, fontweight='bold', ha='center')
            ax.text(x + 1.1, 2.0, b_desc, color='#e2e8f0', fontsize=8, ha='center', va='center', linespacing=1.35)
            if i < 3:
                arrow = patches.FancyArrowPatch((x + 2.25, 2.25), (x + 2.5, 2.25), arrowstyle='->', mutation_scale=15, color='#94a3b8', linewidth=2)
                ax.add_patch(arrow)

        ax.text(5.0, 4.2, d["title"], color='#ffffff', fontsize=12, fontweight='bold', ha='center')
        ax.set_xlim(0, 10)
        ax.set_ylim(0.5, 4.6)
        ax.axis('off')
        plt.tight_layout()
        fig.savefig(os.path.join(target_dir, "02_architecture.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  [{loc}] Generated RL architecture diagram successfully")

# ==========================================
# 4. MAEUMJIGI LOCALIZED SLIDE INFOGRAPHICS (EN, JA, ES)
# ==========================================
def generate_maeumjigi_slides():
    print("=== Generating Localized Maeumjigi Slides for EN, JA, ES ===")
    
    # We generate dedicated localized slide cards for key episodes where presentation slides were used
    slide_episodes = {
        "2026-03-26-maeumjigi-1": {
            "img": "01_cover.png",
            "en": ("Capstone Design Kickoff: Social Value AI", "Project Start: Autonomous Agent Collaboration", "Maeumjigi Team · AI Mental Health Counseling Chatbot Roadmap"),
            "ja": ("卒業研究 開発キックオフ: 社会的価値AI", "プロジェクト開始: 自律型AIエージェント協調開発", "マウムジギチーム · AI心理相談チャットボット ロードマップ"),
            "es": ("Kickoff Diseño Capstone: IA de Valor Social", "Inicio del Proyecto: Colaboración con Agente de IA", "Equipo Maeumjigi · Chatbot de Apoyo Emocional y Hoja de Ruta"),
        },
        "2026-03-31-maeumjigi-3": {
            "img": "01_cover.png",
            "en": ("Overall Capstone Plan: 3 of 5 Stages Completed", "Safe & Affordable Korean Crisis Prevention AI Chatbot", "1. Model Selection 7:3 [Done] -> 2. Web/App Full-Stack -> 3. Safety Wrapper -> 4. Server -> 5. Release"),
            "ja": ("全体計画: 5段階中3段階完了", "安全で低コストな韓国語 危機予防・心理相談AIチャットボット", "1. モデル選定 7:3 完了 -> 2. Web/アプリ実装 -> 3. 安全網(Safety Wrapper) -> 4. サーバー -> 5. リリース"),
            "es": ("Plan General: 3 de 5 Etapas Completadas", "Chatbot de IA Seguro y Accesible para Prevención de Crisis", "1. Selección de Modelo 7:3 [Hecho] -> 2. Web/App Full-Stack -> 3. Safety Wrapper -> 4. Servidor -> 5. Lanzamiento"),
        },
        "2026-04-01-maeumjigi-4": {
            "img": "01_cover.png",
            "en": ("Training Dataset Preprocessing & Distribution", "Large-Scale Empathy & Counseling Corpus Extraction", "Emotion Dialogue (100k) + Crisis Transcripts -> Unified Llama 3.1 JSONL Format"),
            "ja": ("学習データセット前処理＆カテゴリ別分布", "大規模な共感・心理相談コーパス抽出パイプライン", "感情対話(10万件) ＋ 危機スクリプト -> 統一Llama 3.1 JSONL形式変換"),
            "es": ("Preprocesamiento y Distribución del Dataset de Entrenamiento", "Extracción Masiva de Corpus de Empatía y Apoyo Emocional", "Diálogos Emocionales (100k) + Transcripciones de Crisis -> Formato Llama 3.1 JSONL"),
        },
        "2026-04-03-maeumjigi-5": {
            "img": "01_cover.png",
            "en": ("Validation Metrics & Baseline Evaluation (M0~M6)", "Quantitative Benchmark: BLEU-4, ROUGE-L, BERTScore", "Filtering Hallucinations & Measuring Counseling Empathy Scores"),
            "ja": ("検証メトリクス＆ベースライン評価 (M0~M6)", "定量的ベンチマーク: BLEU-4, ROUGE-L, BERTScore", "幻覚のフィルタリングと共感相談スコアの定量的測定"),
            "es": ("Métricas de Validación y Evaluación Baseline (M0~M6)", "Benchmark Cuantitativo: BLEU-4, ROUGE-L, BERTScore", "Filtrado de Alucinaciones y Puntuación de Empatía en Diálogo"),
        },
        "2026-04-05-maeumjigi-6": {
            "img": "01_cover.png",
            "en": ("Frontend Architecture & Mobile Bug Triage", "React Native Client & FastAPI Integration", "State Management, Error Boundaries, Real-time Chat UI Debugging"),
            "ja": ("フロントエンド設計とモバイルバグ修正", "React Nativeクライアント＆FastAPIバックエンド統合", "状態管理、エラーバウンダリ、リアルタイム相談UIデバッグ"),
            "es": ("Arquitectura Frontend y Depuración en Móvil", "Integración de Cliente React Native y Backend FastAPI", "Gestión de Estado, Error Boundaries y UI de Chat en Tiempo Real"),
        },
        "2026-04-07-maeumjigi-7": {
            "img": "01_cover.png",
            "en": ("Synthetic Data Pipeline (v5) & Model Fine-Tuning", "Comparative Analysis of Emotion-to-Daily Mix Ratios", "7:3 Golden Ratio Selected for Optimal Emotional Resonance"),
            "ja": ("合成データセット(v5)生成＆モデル微調整", "感情対話と日常対話の混合比率比較分析", "情緒的共鳴に最適な 7:3 黄金比率モデルの採択"),
            "es": ("Pipeline de Datos Sintéticos (v5) y Ajuste Fino", "Análisis Comparativo de Proporciones de Diálogo", "Selección de Proporción Dorada 7:3 para Máxima Resonancia Emocional"),
        },
        "2026-04-08-maeumjigi-8": {
            "img": "01_cover.png",
            "en": ("Colab GPU VRAM Optimization & Training Metrics", "Managing OOM Limits on Large Language Model Fine-Tuning", "Gradient Accumulation (Steps=4), LoRA Rank=16, 4-bit Quantization"),
            "ja": ("Colab GPU VRAM最適化＆学習メトリクス", "大規模言語モデルのOOM(メモリ不足)制約の克服", "勾配累積 (Steps=4)、LoRA Rank=16、4-bit量子化導入"),
            "es": ("Optimización de VRAM en Colab y Métricas de Entrenamiento", "Superando Límites de OOM en Modelos Masivos de Lenguaje", "Acumulación de Gradientes (Steps=4), LoRA Rank=16, Cuantización 4-bit"),
        },
        "2026-05-17-maeumjigi-19": {
            "img": "01_cover.png",
            "en": ("Cloud Infrastructure & AWS Deployment Estimation", "EC2 GPU Server Cost Simulation & Cloud Database", "Balancing Monthly Budget vs Real-Time LLM Inference Latency"),
            "ja": ("クラウドインフラ＆AWSデプロイ見積もり試算", "EC2 GPUサーバーコストシミュレーション＆クラウドDB", "月額予算とリアルタイムLLM推論レイテンシの最適バランス"),
            "es": ("Infraestructura en la Nube y Estimación en AWS", "Simulación de Costes de GPU en EC2 y Base de Datos Cloud", "Equilibrio entre Presupuesto Mensual y Latencia de Inferencia LLM"),
        },
        "2026-06-18-maeumjigi-23": {
            "img": "01_cover.png",
            "en": ("Maeumjigi System: 6 Core Completed Features", "Unified Backend & Cloud DB for Web/App Co-Deployment", "1. Home Hero  2. Auth/Profile  3. AI Counselor  4. Crisis 109  5. Community  6. Mood Diary"),
            "ja": ("マウムジギ システム: 6大コア機能完成", "統合バックエンド＆クラウドDBによるWeb/アプリ同時提供", "1. ホームHero  2. 認証/マイページ  3. AI相談室  4. 危機109  5. 掲示板  6. 気分記録"),
            "es": ("Sistema Maeumjigi: 6 Funciones Principales Completadas", "Backend Unificado y BD Cloud para Despliegue Web/App", "1. Inicio Hero  2. Auth/Perfil  3. Consejero IA  4. Crisis 109  5. Foro  6. Diario"),
        },
    }

    # Flowchart for Episode 23 (02_presentation.png)
    flowchart_data = {
        "en": {
            "title": "Deterministic Safety Wrapper Architecture Flowchart",
            "subtitle": "Guaranteed 100% Crisis Detection Without LLM Hallucinations",
            "steps": [
                ("User Input", "Raw User Utterance\n(Text Message)", "#38bdf8"),
                ("Crisis Classifier", "Intent & Risk Analysis\n(Suicide / Self-Harm)", "#ec4899"),
                ("Bypass Decision", "Risk >= Threshold ?\nBypass Generative LLM", "#fbbf24"),
                ("Deterministic Wrapper", "Inject Hotline (109/988)\n& Emergency Protocol", "#10b981"),
                ("Safe Output", "Empathetic Safe Response\n+ Lifeline Hotline Card", "#34d399"),
            ]
        },
        "ja": {
            "title": "決定論的 Safety Wrapper 安全網アーキテクチャ フローチャート",
            "subtitle": "LLMの幻覚を排除した100%確実な危機介入・ホットライン案内",
            "steps": [
                ("ユーザー入力", "相談者の発話テキスト\n(メッセージ受信)", "#38bdf8"),
                ("危機分類器", "意図およびリスク判定\n(自傷・自死の兆候)", "#ec4899"),
                ("迂回判断", "閾値以上の場合\n生成LLMを完全バイパス", "#fbbf24"),
                ("決定論的ラッパー", "相談窓口(109/988)および\n緊急プロトコルの注入", "#10b981"),
                ("安全な応答", "共感型安全メッセージ\n＋ 緊急ホットラインカード", "#34d399"),
            ]
        },
        "es": {
            "title": "Flujograma de Arquitectura Determinista Safety Wrapper",
            "subtitle": "Intervención de Crisis 100% Confiable sin Alucinaciones de LLM",
            "steps": [
                ("Entrada de Usuario", "Mensaje de Texto\n(Expresión del Usuario)", "#38bdf8"),
                ("Clasificador de Crisis", "Análisis de Intención y Riesgo\n(Suicidio / Autolesión)", "#ec4899"),
                ("Decisión de Bypass", "¿Riesgo >= Umbral?\nBypass Total del LLM", "#fbbf24"),
                ("Wrapper Determinista", "Inyección de Línea de Ayuda\ny Protocolo de Emergencia", "#10b981"),
                ("Respuesta Segura", "Mensaje Empático Seguro\n+ Tarjeta de Hotline Vital", "#34d399"),
            ]
        },
    }

    font_fam = {
        "ja": "MS Gothic",
        "en": "Segoe UI",
        "es": "Segoe UI",
    }

    # Render localized slide cards for EN, JA, ES
    for ep_slug, ep_info in slide_episodes.items():
        img_name = ep_info["img"]
        for loc in ["en", "ja", "es"]:
            target_dir = os.path.join(LOCALES[loc], ep_slug, "images")
            os.makedirs(target_dir, exist_ok=True)
            plt.rcParams['font.family'] = font_fam[loc]
            h1, h2, sub = ep_info[loc]

            fig, ax = plt.subplots(figsize=(10, 5.625), dpi=200) # 16:9 Slide Ratio
            fig.patch.set_facecolor('#0f172a')
            ax.set_facecolor('#0f172a')

            # Card background
            card = patches.FancyBboxPatch((0.5, 0.5), 9.0, 4.6, boxstyle="round,pad=0.25", linewidth=2, edgecolor='#3b82f6', facecolor='#1e293b')
            ax.add_patch(card)

            # Header Accent Bar
            bar = patches.Rectangle((1.0, 4.4), 8.0, 0.1, color='#38bdf8')
            ax.add_patch(bar)

            ax.text(5.0, 3.8, h1, color='#ffffff', fontsize=14, fontweight='bold', ha='center')
            ax.text(5.0, 3.1, h2, color='#38bdf8', fontsize=11, fontweight='bold', ha='center')
            
            # Content Box
            inner = patches.FancyBboxPatch((1.2, 1.0), 7.6, 1.6, boxstyle="round,pad=0.2", linewidth=1.5, edgecolor='#64748b', facecolor='#0f172a')
            ax.add_patch(inner)
            ax.text(5.0, 1.8, sub, color='#cbd5e1', fontsize=9.5, ha='center', va='center', wrap=True)

            ax.text(5.0, 0.75, "Maeumjigi AI Engineering Series", color='#64748b', fontsize=8, ha='center')

            ax.set_xlim(0, 10)
            ax.set_ylim(0, 5.625)
            ax.axis('off')
            plt.tight_layout()
            fig.savefig(os.path.join(target_dir, img_name), facecolor=fig.get_facecolor(), edgecolor='none')
            plt.close()

    # Render localized Flowchart for Episode 23
    for loc in ["en", "ja", "es"]:
        target_dir = os.path.join(LOCALES[loc], "2026-06-18-maeumjigi-23", "images")
        os.makedirs(target_dir, exist_ok=True)
        plt.rcParams['font.family'] = font_fam[loc]
        fc = flowchart_data[loc]

        fig, ax = plt.subplots(figsize=(10, 5.625), dpi=200)
        fig.patch.set_facecolor('#0a0f1d')
        ax.set_facecolor('#0a0f1d')

        ax.text(5.0, 5.1, fc["title"], color='#ffffff', fontsize=13, fontweight='bold', ha='center')
        ax.text(5.0, 4.65, fc["subtitle"], color='#38bdf8', fontsize=9.5, ha='center')

        colors = ["#38bdf8", "#ec4899", "#fbbf24", "#10b981", "#34d399"]
        for i, (s_title, s_desc, col) in enumerate(fc["steps"]):
            x = 0.4 + i * 1.9
            rect = patches.FancyBboxPatch((x, 1.2), 1.7, 2.9, boxstyle="round,pad=0.15", linewidth=2, edgecolor=col, facecolor='#1e293b')
            ax.add_patch(rect)
            ax.text(x + 0.85, 3.6, s_title, color=col, fontsize=9, fontweight='bold', ha='center')
            ax.text(x + 0.85, 2.3, s_desc, color='#e2e8f0', fontsize=7.8, ha='center', va='center', linespacing=1.35)
            if i < 4:
                arrow = patches.FancyArrowPatch((x + 1.72, 2.65), (x + 1.9, 2.65), arrowstyle='->', mutation_scale=12, color='#94a3b8', linewidth=1.5)
                ax.add_patch(arrow)

        ax.set_xlim(0, 10)
        ax.set_ylim(0.5, 5.625)
        ax.axis('off')
        plt.tight_layout()
        fig.savefig(os.path.join(target_dir, "02_presentation.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        print(f"  [{loc}] Generated Episode 23 Safety Wrapper Flowchart")

if __name__ == "__main__":
    generate_security_diagrams()
    generate_anpr_diagrams()
    generate_rl_diagrams()
    generate_maeumjigi_slides()
    print("\n[SUCCESS] All localized images generated across 4 locales!")
