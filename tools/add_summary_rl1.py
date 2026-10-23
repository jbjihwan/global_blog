import os

SUMMARIES = {
    "blog/2026-05-17-rl-qlearning-1/index.md": """

---

## Summary & Key Takeaways

- **Webots Robotics Simulation Setup**: Established a differential-drive mobile robotics environment in Webots featuring real-time physics and infrared proximity sensing.
- **Low-Latency TCP Socket IPC**: Engineered an asynchronous TCP socket bridge decoupling the simulator physics loop from the external Python reinforcement learning engine.
- **648-Bin State Space Discretization**: Mapped continuous poses and sensor readings into a compact 648-state discrete grid (3 distance bins × 12 heading bins × 18 obstacle zones).
- **Differential Kinematic Actions**: Defined three fundamental discrete velocity actions (Straight, Turn Left, Turn Right) to ensure deterministic robot control and rapid convergence.
""",
    "i18n/ko/docusaurus-plugin-content-blog/2026-05-17-rl-qlearning-1/index.md": """

---

## 핵심 요약 및 배운 점

- **Webots 로봇 시뮬레이션 환경 구축**: 실시간 물리 연산과 적외선 거리 센서가 탑재된 차동 구동(Differential-Drive) 모바일 로봇 주행 환경을 Webots에 구성했습니다.
- **저지연 TCP 소켓 IPC 아키텍처**: 시뮬레이터 물리 제어 루프와 외부 Python 강화학습 엔진을 비동기 분리하는 고속 TCP 소켓 브리지 통신을 구현했습니다.
- **648개 상태 공간 이산화 설계**: 연속적인 로봇 좌표 및 센서 값을 648개 이산 상태(거리 3구간 × 목표 각도 12구간 × 장애물 감지 18조합)로 압축하여 표 형식 학습을 가능하게 했습니다.
- **차동 구동 액션 스페이스 정의**: 직진(Straight), 좌회전(Turn Left), 우회전(Turn Right)의 3가지 이산 속도 명령 체계를 수립하여 안정적인 주행 제어 기반을 마련했습니다.
""",
    "i18n/ja/docusaurus-plugin-content-blog/2026-05-17-rl-qlearning-1/index.md": """

---

## まとめと要点

- **Webotsロボットシミュレーションの構築**: リアルタイム物理演算と赤外線距離センサーを備えた差動二輪駆動型モバイルロボット環境をWebots上に構築しました。
- **低遅延TCPソケットIPC通信**: シミュレーターの物理制御ループと外部Python強化学習エンジンを分離する高速TCPソケット通信ブリッジを実装しました。
- **648状態空間の離散化設計**: 連続的な位置姿勢およびセンサー値を648個の離散状態（距離3区画 × 目標角12区画 × 障害物検知18パターン）に圧縮し、表形式学習を可能にしました。
- **差動キネマティクスのアクション空間**: 直進・左旋回・右旋回の3つの離散速度アクションを定義し、決定論的かつ安定したロボット制御の基礎を確立しました。
""",
    "i18n/es/docusaurus-plugin-content-blog/2026-05-17-rl-qlearning-1/index.md": """

---

## Resumen y Puntos Clave

- **Configuracion de Simulacion en Webots**: Construido un entorno de robot movil con traccion diferencial, fisica realista y sensores infrarrojos de proximidad en Webots.
- **Arquitectura IPC por Sockets TCP**: Disenado un puente de comunicacion TCP de baja latencia que desacopla la simulacion fisica del motor de aprendizaje por refuerzo en Python.
- **Discretizacion del Espacio a 648 Estados**: Reducidas las coordenadas continuas y lecturas de sensores a 648 estados discretos (3 de distancia × 12 de orientacion × 18 de obstaculos).
- **Espacio de Acciones Cinematicas**: Definidas tres acciones discretas de velocidad (Avanzar, Girar Izquierda, Girar Derecha) para garantizar un control determinista y estable.
""",
    "i18n/zh-Hans/docusaurus-plugin-content-blog/2026-05-17-rl-qlearning-1/index.md": """

---

## 核心总结与技术要点

- **Webots 移动机器人仿真环境**：在 Webots 中搭建了具备实时物理刚体动力学与红外测距传感器的差动驱动轮式机器人基准环境。
- **低延迟 TCP Socket IPC 通信**：设计了异步 TCP 套接字 IPC 桥接层，将 Webots 仿真控制器与外部独立 Python 强化学习引擎高效解耦。
- **648 维紧凑状态空间离散化**：将连续位姿坐标与传感器数据压缩映射为 648 个离散状态组合（距离 3 档 × 目标偏角 12 档 × 避障测距 18 档）。
- **差动运动学动作空间构建**：规范了直行、左转、右转 3 类离散轮速控制指令，确保了表格型 Q 学习算法的快速收敛与确定性执行。
""",
    "i18n/zh-Hant/docusaurus-plugin-content-blog/2026-05-17-rl-qlearning-1/index.md": """

---

## 核心總結與技術要點

- **Webots 行動機器人模擬環境**：在 Webots 中建立了具備即時物理剛體動力學與紅外線測距感測器的差動驅動輪式機器人基準環境。
- **低延遲 TCP Socket IPC 通訊**：設計了非同步 TCP 通訊端 IPC 橋接層，將 Webots 模擬控制器與外部獨立 Python 強化學習引擎高效解耦。
- **648 維緊湊狀態空間離散化**：將連續位姿座標與感測器數據壓縮映射為 648 個離散狀態組合（距離 3 檔 × 目標偏角 12 檔 × 避障測距 18 檔）。
- **差動運動學動作空間構建**：規範了直行、左轉、右轉 3 類離散輪速控制指令，確保了表格型 Q 學習演算法的快速收斂與確定性執行。
"""
}

base_dir = r"D:\ai\antigravity\global_blog"

for rel_path, summary_text in SUMMARIES.items():
    full_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    summary_keywords = ["Summary & Key Takeaways", "핵심 요약 및 배운 점", "まとめと要点", "Resumen y Puntos Clave", "核心总结与技术要点", "核心總結與技術要點"]
    if any(kw in content for kw in summary_keywords):
        print(f"Summary already present in: {rel_path}")
        continue
    
    content = content.rstrip() + summary_text + "\n"
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated: {rel_path}")
