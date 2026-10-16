import os
import re

blog_root = r"D:\ai\antigravity\global_blog"

seo_data = {
    # ANPR Series
    "2026-06-25-vision-anpr-1": {
        "en": ["ANPR Pipeline", "Dashcam Video Analytics", "Computer Vision Pipeline", "Real-Time Vehicle Tracking", "YOLO Super Resolution"],
        "ko": ["블랙박스 번호판 인식", "차선 침범 감지", "컴퓨터 비전 파이프라인", "실시간 차량 추적", "YOLO 초해상화"],
        "ja": ["ドラレコ ナンバープレート認識", "車線侵犯 検知", "コンピュータビジョン パイプライン", "リアルタイム車両追跡", "YOLO 超解像"],
        "es": ["Reconocimiento de Matrículas ANPR", "Detección Invasión de Carril", "Pipeline Visión por Computadora", "Seguimiento Vehicular Tiempo Real", "Superresolución YOLO"]
    },
    "2026-06-26-vision-anpr-2": {
        "en": ["OpenCV Lane Detection", "HoughLinesP Lane Tracking", "Lane Intrusion Detection", "Polygon IoU Calculation", "Canny Edge Boundary"],
        "ko": ["OpenCV 차선 검출", "허프 변환 차선 추적", "차선 침범 알고리즘", "다각형 IoU 계산", "Canny 에지 필터링"],
        "ja": ["OpenCV 車線検出", "ハフ変換 車線追跡", "車線侵犯 アルゴリズム", "多角形 IoU 計算", "Canny エッジ抽出"],
        "es": ["Detección de Carril OpenCV", "Rastreo de Carriles HoughLinesP", "Invasión de Carril Algoritmo", "Cálculo IoU Poligonal", "Bordes Canny Carretera"]
    },
    "2026-06-27-vision-anpr-3": {
        "en": ["YOLOv5 License Plate Detection", "CSRT Tracker OpenCV", "Hierarchical Object Detection", "Real-Time Tracking 50FPS", "Vehicle ROI Localization"],
        "ko": ["YOLOv5 번호판 검출", "CSRT 추적기 OpenCV", "계층적 객체 탐지", "실시간 50FPS 추적", "차량 ROI 국소 탐색"],
        "ja": ["YOLOv5 ナンバープレート検出", "CSRT トラッカー OpenCV", "階層型物体検出", "50FPS リアルタイム追跡", "車両ROI 局所特定"],
        "es": ["Detección de Matrículas YOLOv5", "Rastreador CSRT OpenCV", "Detección Jerárquica de Objetos", "Seguimiento Tiempo Real 50FPS", "Localización ROI Vehículo"]
    },
    "2026-06-28-vision-anpr-4": {
        "en": ["EDSR Super Resolution", "License Plate Image Deblurring", "OpenCV dnn_superres", "Multi-Frame Image Stacking", "Deep Residual Upscaling"],
        "ko": ["EDSR 초해상화", "저화질 번호판 복원", "OpenCV dnn_superres", "다중 프레임 스태킹", "딥러닝 4배 업스케일링"],
        "ja": ["EDSR 超解像", "低解像度ナンバープレート復元", "OpenCV dnn_superres", "マルチフレームスタッキング", "深層残差4倍拡大"],
        "es": ["Superresolución EDSR", "Restauración de Matrículas Borrosas", "OpenCV dnn_superres", "Apilamiento Multifotograma", "Escalado Profundo 4x"]
    },
    "2026-06-29-vision-anpr-5": {
        "en": ["EasyOCR Korean License Plate", "ANPR Majority Voting Ensemble", "Korean Plate Regex Normalization", "License Plate Recognition Accuracy", "ITS Traffic Violation Vision"],
        "ko": ["EasyOCR 한국 번호판", "시간 축 다수결 투표 앙상블", "한국 번호판 정규식", "번호판 인식 정확도 99%", "지능형 교통 단속 비전"],
        "ja": ["EasyOCR 韓国ナンバープレート", "時間軸多数決アンサンブル", "韓国ナンバー正規表現", "ナンバー認識精度 99%", "ITS交通違反監視ビジョン"],
        "es": ["EasyOCR Matrículas Coreanas", "Ensamble Votación por Mayoría", "Normalización Regex Matrículas", "Precisión Reconocimiento 99%", "Monitoreo Vial Inteligente"]
    },
    # Q-Learning Series
    "2026-05-17-rl-qlearning-1": {
        "en": ["Webots Autonomous Robot", "Tabular Q-Learning Robotics", "State Discretization 648 Bins", "TCP Socket IPC Python", "Differential Drive Navigation"],
        "ko": ["Webots 자율주행 로봇", "테이블 Q-러닝 로보틱스", "648개 상태 공간 이산화", "TCP 소켓 IPC 통신", "차동 구동 로봇 주행"],
        "ja": ["Webots 自律走行ロボット", "テーブルQ学習 ロボティクス", "648状態空間離散化", "TCPソケットIPC通信", "差動二輪ナビゲーション"],
        "es": ["Robot Autónomo Webots", "Q-Learning Tabular Robótica", "Discretización de 648 Estados", "Comunicación Socket TCP IPC", "Navegación Tracción Diferencial"]
    },
    "2026-05-18-rl-qlearning-2": {
        "en": ["Q-Learning Reward Shaping", "Epsilon Greedy Exploration", "Sparse Reward Reinforcement Learning", "Bellman Optimality TD", "Robot Obstacle Avoidance"],
        "ko": ["Q-러닝 보상 형성", "엡실론 그리디 탐색", "희소 보상 강화학습", "벨만 최적 방정식 TD", "로봇 장애물 회피"],
        "ja": ["Q学習 報酬シェイピング", "イプシロングリーディ探索", "スパース報酬強化学習", "ベルマン最適性TD", "ロボット障害物回避"],
        "es": ["Configuración de Recompensas Q-Learning", "Exploración Epsilon-Greedy", "Aprendizaje por Refuerzo Recompensa Escasa", "Ecuación de Bellman TD", "Evasión de Obstáculos Robot"]
    },
    "2026-05-19-rl-qlearning-3": {
        "en": ["Local Minima Reinforcement Learning", "Webots Headless Simulation", "Obstacle Avoidance Multi-Seed", "Deep RL vs Tabular Q", "PowerShell Automated Training"],
        "ko": ["강화학습 로컬 미니마", "Webots 헤드리스 시뮬레이션", "장애물 회피 멀티 시드", "심층 강화학습 vs 테이블 Q", "파워쉘 자동화 학습"],
        "ja": ["強化学習 局所解回避", "Webots ヘッドレスシミュレーション", "マルチシード障害物回避", "深層強化学習 vs テーブルQ", "PowerShell自動化学習"],
        "es": ["Mínimos Locales Aprendizaje Refuerzo", "Simulación Webots Sin Interfaz", "Evasión Obstáculos Multi-Semilla", "RL Profundo vs Q Tabular", "Entrenamiento Automatizado PowerShell"]
    },
    "2026-05-20-rl-qlearning-4": {
        "en": ["Deterministic Policy Evaluation", "Near-Miss Obstacle Metric", "Q-Learning vs DQN vs SARSA", "Autonomous Navigation Benchmark", "Zero Exploration Inference"],
        "ko": ["결정론적 정책 평가", "장애물 근접 통과 지표", "Q-러닝 DQN SARSA 비교", "자율주행 벤치마크 평가", "무탐색 추론 파이프라인"],
        "ja": ["決定論的ポリシー評価", "障害物ニアミス指標", "Q学習 DQN SARSA比較", "自律走行ベンチマーク", "探索ゼロ推論パイプライン"],
        "es": ["Evaluación Determinista de Políticas", "Métrica de Proximidad a Obstáculos", "Comparativa Q-Learning vs DQN vs SARSA", "Benchmark Navegación Autónoma", "Inferencia Sin Exploración"]
    },
    "2026-05-21-rl-qlearning-5": {
        "en": ["Sim-to-Real Hardware Transfer", "ArUco Marker Pose Tracking", "Arduino Uno Robot Navigation", "HC-06 Bluetooth IPC", "Webcam Homography Robotics"],
        "ko": ["Sim-to-Real 하드웨어 전이", "아루코 마커 포즈 추적", "아두이노 우노 로봇 주행", "HC-06 블루투스 통신", "웹캠 호모그래피 로보틱스"],
        "ja": ["Sim-to-Real ハードウェア転移", "ArUcoマーカー ポーズ追跡", "Arduino Uno ロボットナビゲーション", "HC-06 Bluetooth通信", "ウェブカメラ ホモグラフィ"],
        "es": ["Transferencia Sim-to-Real Hardware", "Seguimiento de Pose con Marcadores ArUco", "Navegación Robot Arduino Uno", "Comunicación Bluetooth HC-06", "Homografía con Cámara Web"]
    }
}

locales = {
    'en': os.path.join(blog_root, 'blog'),
    'ko': os.path.join(blog_root, 'i18n', 'ko', 'docusaurus-plugin-content-blog'),
    'ja': os.path.join(blog_root, 'i18n', 'ja', 'docusaurus-plugin-content-blog'),
    'es': os.path.join(blog_root, 'i18n', 'es', 'docusaurus-plugin-content-blog'),
}

updated_count = 0

for slug, loc_dict in seo_data.items():
    for lang, kw_list in loc_dict.items():
        base_dir = locales[lang]
        md_path = os.path.join(base_dir, slug, "index.md")
        if not os.path.exists(md_path):
            print(f"Skipping missing: {md_path}")
            continue
            
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Match frontmatter block
        parts = content.split("---", 2)
        if len(parts) < 3:
            print(f"Cannot split frontmatter: {md_path}")
            continue
            
        header = parts[0]
        fm = parts[1]
        body = parts[2]
        
        kw_line = "keywords: [" + ", ".join([f'"{k}"' for k in kw_list]) + "]"
        
        # Remove existing keywords line if present
        fm_lines = [line for line in fm.strip().splitlines() if not line.strip().startswith("keywords:")]
        
        # Add keywords line
        fm_lines.append(kw_line)
        
        new_fm = "\n".join(fm_lines)
        new_content = f"---\n{new_fm}\n---{body}"
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        updated_count += 1
        print(f"Updated keywords [{lang}] -> {slug}")

print(f"Successfully processed {updated_count} files!")
