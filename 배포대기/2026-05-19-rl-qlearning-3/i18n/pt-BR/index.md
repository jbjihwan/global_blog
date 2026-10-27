---
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

Para solucionar isso, implementamos um **campo de repulsão de emergência**: quando o sensor frontal detecta perigo crítico (`d_{\text{frente}} < 0.2\,\text{m}`), a penalidade por risco de colisão supera o incentivo de proximidade, forçando o desvio lateral.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Ponderação Repulsiva**: Impede colisões frontais mesmo quando a meta atrai o robô em direção à parede.
2. **Aceleração Headless**: Desativar a interface gráfica (GUI) eleva a velocidade de treinamento em 8 vezes.
3. **Robustez Multi-Seed**: Testes sistemáticos em 10 sementes aleatórias comprovam a consistência das rotas aprendidas.
4. **Taxa de Sucesso > 90%**: O robô aprende a escapar com sucesso até mesmo de armadilhas em formato de U.
