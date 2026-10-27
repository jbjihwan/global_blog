# -*- coding: utf-8 -*-
import os
import shutil

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")

def save_pt_post(slug, pt_content):
    # 1. Save to Staging
    stage_dir = os.path.join(STAGING_ROOT, slug)
    stage_pt_dir = os.path.join(stage_dir, "i18n", "pt-BR")
    os.makedirs(stage_pt_dir, exist_ok=True)
    with open(os.path.join(stage_pt_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(pt_content.strip() + "\n")
    print(f"[STAGING OK] {slug} -> {stage_pt_dir}\\index.md")

    # 2. Save to i18n/pt-BR production blog dir (ready for build)
    prod_pt_dir = os.path.join(GB_ROOT, "i18n", "pt-BR", "docusaurus-plugin-content-blog", slug)
    os.makedirs(prod_pt_dir, exist_ok=True)
    with open(os.path.join(prod_pt_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(pt_content.strip() + "\n")
    
    # 3. Copy images from blog/<slug>/images
    src_images = os.path.join(GB_ROOT, "blog", slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_pt_dir, "images")
        os.makedirs(dst_images, exist_ok=True)
        for item in os.listdir(src_images):
            s = os.path.join(src_images, item)
            d = os.path.join(dst_images, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
        print(f"[IMAGES OK] Copied images to {dst_images}")

# ==============================================================================
# RL 1 PORTUGUESE
# ==============================================================================
r1_slug = "2026-05-17-rl-qlearning-1"
r1_content = """---
slug: 2026-05-17-rl-qlearning-1
title: "[Robótica Webots] Navegação Autônoma com Q-Learning: Discretização em 648 Estados & Arquitetura Socket (#1)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, webots, robotics, discretization, python]
date: 2026-05-17
project: rl_q_learning
description: "Desenvolvimento de um discretizador de 648 estados e arquitetura IPC via sockets TCP para robôs móveis autônomos na simulação Webots com Q-Learning tabular."
keywords: [Webots Robô Autônomo, Q-Learning Tabular Robótica, Discretização de Estados 648 Bins, TCP Socket IPC Python, Navegação com Tração Diferencial]
---

![Ambiente de Simulação Webots](./images/01_webots_arena.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Dados contínuos de sensores (distância e ângulo para a meta) causam explosão do espaço de estados no Q-Learning tabular; a comunicação IPC síncrona com o simulador Webots exige latência mínima.
> - **Solução**: Redução para 648 estados discretos distribuídos em 3 setores de distância e 4 zonas de orientação, operados por um servidor socket TCP em Python de alto desempenho.

{/* truncate */}

---

### 1. Discretização do Espaço de Estados: 648 Bins Compactos

Leituras sensoriais contínuas não podem ser indexadas diretamente em uma tabela Q discreta. Para contornar essa limitação, realizamos uma discretização geométrica:
- **3 Setores de Sensores** (Esquerda, Centro, Direita): Cada setor é dividido em 3 faixas discretas de distância (Perto, Médio, Longe) $\\rightarrow 3^3 = 27$ combinações.
- **Ângulo Relativo para o Alvo ($\\theta_{\\text{alvo}}$)**: 4 quadrantes direcionais (Frente-Esquerda, Frente-Direita, Trás-Esquerda, Trás-Direita) $\\rightarrow 4$ estados.
- **Distância Euclidianana até a Meta**: 6 zonas de proximidade radial $\\rightarrow 6$ estados.

$$\\text{Total de Estados} = 27 \\times 4 \\times 6 = 648 \\text{ estados discretos}$$

Essa formulação permite que a Q-Table inteira ocupe menos de 15 Kilobytes de memória RAM e convirja de forma estável em poucas centenas de episódios.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Discretização Otimizada**: 648 bins viabilizam aprendizado tabular ultrarrápido sem a sobrecarga computacional de Deep RL.
2. **IPC de Baixa Latência**: Um socket TCP local sincroniza o motor de física do Webots com o agente Python a mais de 100 passos por segundo.
3. **Estabilidade Numérica**: A arquitetura previne estouro de memória e garante total reprodutibilidade dos experimentos.
4. **Compatibilidade com Hardware**: O consumo enxuto de memória permite exportar a tabela aprendida diretamente para um microcontrolador Arduino Uno.
"""

# ==============================================================================
# RL 2 PORTUGUESE
# ==============================================================================
r2_slug = "2026-05-18-rl-qlearning-2"
r2_content = """---
slug: 2026-05-18-rl-qlearning-2
title: "[Robótica Webots] Implementação do Q-Learning Tabular & Ajuste de Reward Shaping (#2)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, reward-shaping, webots, robotics, machine-learning, python]
date: 2026-05-18
project: rl_q_learning
description: "Análise aprofundada da atualização TD(0) no Q-Learning tabular, decaimento exponencial de epsilon e modelagem densa de recompensas contra o problema de sparse rewards."
keywords: [Q-Learning Reward Shaping, Exploração Epsilon Greedy, Sparse Rewards Aprendizado por Reforço, Otimalidade de Bellman TD, Desvio de Obstáculos Robótica]
---

![Curva de Recompensa de Treinamento](./images/01_reward_curve.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Recompensas esparsas (+1,0 ao atingir a meta, -1,0 em colisão) resultam em estagnação do aprendizado; o robô gira em círculos sem direção.
> - **Solução**: Modelagem de recompensa densa (Reward Shaping) utilizando delta de distância ($\\Delta d$) e bônus de velocidade para a frente, combinada com decaimento exponencial de $\\epsilon$ ($0.95 \\rightarrow 0.05$).

{/* truncate */}

---

### 1. A Regra de Atualização de Bellman (Diferença Temporal TD-0)

A cada passo de tempo $t$, o valor da ação selecionada é atualizado na tabela Q:

$$Q(s_t, a_t) \\leftarrow Q(s_t, a_t) + \\alpha \\left[ r_{t+1} + \\gamma \\max_{a} Q(s_{t+1}, a) - Q(s_t, a_t) \\right]$$

- **Taxa de Aprendizado ($\\alpha = 0.15$)**: Modula a velocidade de absorção de novas experiências.
- **Fator de Desconto ($\\gamma = 0.95$)**: Pondera a importância de recompensas futuras em relação a ganhos imediatos.

---

### 2. Função de Recompensa Densa (Reward Shaping)

$$R(s, a, s') = R_{\\text{terminal}} + c_1 \\cdot (d_t - d_{t+1}) + c_2 \\cdot v_{\\text{frente}} - c_3 \\cdot \\mathbb{I}_{\\text{giro}}$$

Ao recompensar a aproximação contínua em relação ao alvo ($d_t - d_{t+1} > 0$), o robô descobre trajetórias ótimas em menos de 50 episódios.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Feedback Denso vs. Esparso**: Recompensas contínuas de aproximação aceleram a convergência em mais de 10 vezes.
2. **Equilíbrio Exploração/Explotação**: O decaimento exponencial do epsilon assegura exploração inicial ampla e estabilidade final.
3. **Convergência Firme**: Os valores da Q-Table estabilizam-se após 200 episódios sem oscilações destrutivas.
4. **Prevenção de Giros Viciosos**: A penalidade por giros no próprio eixo força o agente a buscar avanço espacial contínuo.
"""

# ==============================================================================
# RL 3 PORTUGUESE
# ==============================================================================
r3_slug = "2026-05-19-rl-qlearning-3"
r3_content = """---
slug: 2026-05-19-rl-qlearning-3
title: "[Robótica Webots] Superando Mínimos Locais em Ambientes com 12 Obstáculos: Simulação Headless Multi-Seed (#3)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, webots, obstacle-avoidance, local-minima, headless, python]
date: 2026-05-19
project: rl_q_learning
description: "Resolução do dilema de mínimos locais em labirintos complexos com 12 paredes (obstacle12) e orquestração de simulações automatizadas headless com múltiplas sementes aleatórias."
keywords: [Mínimos Locais Aprendizado por Reforço, Webots Simulação Headless, Desvio de Obstáculos Multi-Seed, Q-Learning Tabular vs DQN, Pipeline Automatizado de Treinamento]
---

![Arena de Simulação obstacle12](./images/01_obstacle12_arena.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Quando o alvo está situado logo atrás de uma parede, a recompensa por proximidade puxa o robô diretamente contra o obstáculo, prendendo-o em um **mínimo local**.
> - **Solução**: Repulsão dinâmica por proximidade na função de recompensa e aceleração do treinamento via simulação headless com 10 sementes aleatórias.

{/* truncate */}

---

### 1. O Dilema do Mínimo Local

Se a linha reta em direção ao alvo está bloqueada por um obstáculo, o contorno exige afastar-se temporariamente da meta para contornar a barreira. Recompensas de proximidade puras punem esse movimento correto, prendendo o agente.

Para solucionar isso, implementamos um **campo de repulsão de emergência**: quando o sensor frontal detecta perigo crítico ($d_{\\text{frente}} < 0.2\\,\\text{m}$), a penalidade por risco de colisão supera o incentivo de proximidade, forçando o desvio lateral.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Ponderação Repulsiva**: Impede colisões frontais mesmo quando a meta atrai o robô em direção à parede.
2. **Aceleração Headless**: Desativar a interface gráfica (GUI) eleva a velocidade de treinamento em 8 vezes.
3. **Robustez Multi-Seed**: Testes sistemáticos em 10 sementes aleatórias comprovam a consistência das rotas aprendidas.
4. **Taxa de Sucesso > 90%**: O robô aprende a escapar com sucesso até mesmo de armadilhas em formato de U.
"""

# ==============================================================================
# RL 4 PORTUGUESE
# ==============================================================================
r4_slug = "2026-05-20-rl-qlearning-4"
r4_content = """---
slug: 2026-05-20-rl-qlearning-4
title: "[Robótica Webots] Avaliação Determinística via evaluate_qlearning & Benchmark Contra DQN e SARSA (#4)"
authors: [jbgih]
tags: [reinforcement-learning, q-learning, evaluation, benchmark, dqn, sarsa, robotics, python]
date: 2026-05-20
project: rl_q_learning
description: "Avaliação determinística sem ruído de exploração (ε=0) com evaluate_qlearning.py, análise de eficiência de rota, métricas de quase-colisão e benchmark contra DQN e SARSA."
keywords: [Avaliação Determinística de Política, Métrica Near-Miss Obstáculos, Q-Learning vs DQN vs SARSA, Benchmark de Navegação Autônoma, Inferência Zero Exploração]
---

![Benchmark de Sucesso e Passos](./images/01_eval_success_steps.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Objetivo**: Medir a capacidade pura da política gulosa aprendida (Greedy Policy, $\\epsilon = 0$) sem exploração estocástica, validando a viabilidade de implantação no mundo real.
> - **Resultado**: O Q-Learning tabular atingiu 92% de taxa de sucesso com demanda computacional 15 vezes menor em comparação com Deep Q-Networks (DQN).

{/* truncate */}

---

### 1. Benchmark Comparativo de Algoritmos

| Algoritmo | Taxa de Sucesso (%) | Média de Passos até a Meta | Eventos de Quase-Colisão | Consumo de Memória |
| :--- | :--- | :--- | :--- | :--- |
| **Q-Learning Tabular (Proposto)** | **92.0 %** | **48.2** | **1.2** | **< 15 KB** |
| **SARSA (On-Policy)** | 84.0 % | 56.4 | 0.8 | < 15 KB |
| **Deep Q-Network (DQN)** | 88.5 % | 52.1 | 2.1 | ~ 12 MB (PyTorch) |

O Q-Learning tabular demonstrou-se extraordinariamente eficiente em termos de consumo energético e altamente imune ao sobreajuste (*overfitting*).

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Teste Determinístico ($\\epsilon=0$)**: Confirma a solidez da política sem depender de ações aleatórias de sorte.
2. **Eficiência Extrema**: Ocupando menos de 15 KB, a abordagem é ideal para computação embarcada de ultra-baixo custo.
3. **Latência Mínima**: Respostas em frações de milissegundo evitam acidentes em velocidades de tráfego mais altas.
4. **Pronto para Hardware**: A política atende a todos os critérios para transferência direta para robôs reais.
"""

# ==============================================================================
# RL 5 PORTUGUESE
# ==============================================================================
r5_slug = "2026-05-21-rl-qlearning-5"
r5_content = """---
slug: 2026-05-21-rl-qlearning-5
title: "[Robótica Webots] Sim-to-Real: Transferência para Hardware com Arduino Uno, Bluetooth HC-06 & Rastreamento ArUco (#5)"
authors: [jbgih]
tags: [reinforcement-learning, sim-to-real, arduino, robotics, computer-vision, aruco, python]
date: 2026-05-21
project: rl_q_learning
description: "Implantação da política de 648 estados treinada em simulação em um robô físico Arduino Uno, com homografia de câmera zenital e rastreamento de pose 6-DoF com marcadores ArUco."
keywords: [Sim-to-Real Hardware Transfer, ArUco Marker Pose Tracking, Arduino Uno Roboter Navigation, HC-06 Bluetooth IPC, Webots Simulation zu Realität]
---

![Rastreamento Visual com Marcadores ArUco](./images/01_aruco_vision.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Limitações severas de hardware (Arduino Uno com apenas 2 KB de SRAM), deslizamento não linear das rodas e o clássico abismo da realidade (**Reality Gap**) entre simulação e ambiente físico.
> - **Solução**: Desacoplamento da visão computacional para um PC Host através de câmera superior com homografia e transmissão sem fio de comandos compactos via Bluetooth HC-06.

{/* truncate */}

---

### 1. A Arquitetura Sim-to-Real

```mermaid
flowchart TD
    Cam[Câmera Superior 1080p] --> ArUco[Rastreamento de Pose ArUco 6-DoF OpenCV]
    ArUco --> Homography[Transformação Homográfica para Coordenadas 2D da Arena]
    Homography --> Host[PC Host: Discretização em 648 Bins & Consulta na Tabela Q]
    Host -->|Comando Serial Bluetooth HC-06| Arduino[Arduino Uno: Controlador PWM Dual Motor]
    Arduino --> Motors[Motores Físicos com Caixa de Redução Esquerda/Direita]
```

Graças ao sistema de rastreamento visual externo, o robô móvel não precisa carregar sensores LiDAR pesados. O microcontrolador Arduino Uno processa comandos de apenas 2 bytes e controla a ponte H de potência com precisão milimétrica.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Transposição Bem-Sucedida**: A política treinada no Webots guiou o robô real sem necessidade de novo treinamento físico.
2. **Rastreamento ArUco Confiável**: Entrega telemetria em alta frequência a 60 FPS com precisão milimétrica.
3. **Hardware Minimalista**: Um microcontrolador simples de 8 bits foi suficiente para condução autônoma sofisticada.
4. **Ciclo Completo de Engenharia**: Do design do MDP matemático à validação em hardware físico, todo o ciclo foi comprovado.
"""

def main():
    print("=" * 65)
    print("Translating Section 4: RL Q-Learning (5 posts) into pt-BR...")
    print("=" * 65)
    save_pt_post(r1_slug, r1_content)
    save_pt_post(r2_slug, r2_content)
    save_pt_post(r3_slug, r3_content)
    save_pt_post(r4_slug, r4_content)
    save_pt_post(r5_slug, r5_content)
    print("\n[SECTION 4 COMPLETE] All 5 RL Q-Learning posts staged and saved in pt-BR!")

if __name__ == "__main__":
    main()
