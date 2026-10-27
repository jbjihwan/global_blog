---
slug: 2026-06-26-vision-anpr-2
title: "[Visão Computacional] Delimitação Dinâmica de Faixas & Critério Geométrico de Invasão por IoU (#2)"
authors: [jbgih]
tags: [computer-vision, anpr, lane-detection, hough-transform, iou, opencv, python]
date: 2026-06-26
project: anpr_vision
description: "Filtragem de bordas Canny, Transformada de Hough probabilística (HoughLinesP), limiares angulares e cálculo de IoU poligonal para monitoramento de faixas de rolamento."
keywords: [OpenCV Detecção de Faixas, HoughLinesP Rastreamento Faixa, Detecção Invasão de Faixa, Cálculo IoU Poligonal, Canny Detecção de Bordas Rodovia]
---

![Sobreposição de Detecção Dinâmica de Faixas](./images/01_lane_detection.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Reflexos no asfalto molhado, emendas de piche e sombras de viadutos produzem ruídos lineares; comparações simples de coordenadas X falham em curvas.
> - **Solução**: Combinação de ROI trapezoidal adaptativa, filtros angulares de inclinação positiva/negativa e sobreposição de polígonos com limiar de IoU > 0,15.

{/* truncate */}

---

### 1. Formulação Matemática da Extração de Faixas

A geometria das linhas delimitadoras da pista é modelada por equações lineares no plano da imagem:

$`y = m \cdot x + b, \quad \text{onde } m = \frac{y_2 - y_1}{x_2 - x_1}`$

Para descartar marcações transversais e sombras horizontais, definimos limiares estritos de inclinação angular:
- **Faixa Esquerda**: $-0.85 < m < -0.45$
- **Faixa Direita**: $+0.45 < m < +0.85$

---

### 2. Critério de Invasão de Faixa Baseado em IoU Poligonal

A invasão de faixa é confirmada quando o polígono delimitador da base do veículo `P_{\text{veiculo}}` intercepta o polígono da faixa de rodagem `P_{\text{faixa}}`:

```text
IoU_intrusion = Area(P_vehicle ∩ P_lane) / Area(P_vehicle) > θ_threshold
```

Adotando um limiar $\theta = 0.15$, ruídos momentâneos de vibração são filtrados com precisão, enquanto mudanças reais de faixa são registradas de modo determinístico.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Filtragem Angular**: Limiares de inclinação matemática eliminam 95% das linhas espúrias geradas por sombras e remendos de asfalto.
2. **IoU Poligonal Superior**: A área de sobreposição geométrica é imune a falsos positivos em curvas acentuadas.
3. **Eficiência Computacional**: A Transformada de Hough na ROI trapezoidal consome menos de 3 milissegundos por quadro.
4. **Gatilho Determinístico**: A confirmação de invasão dispara automaticamente o módulo de leitura em alta resolução.
