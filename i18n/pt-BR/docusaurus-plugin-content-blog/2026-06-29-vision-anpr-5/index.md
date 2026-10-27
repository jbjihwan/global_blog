---
slug: 2026-06-29-vision-anpr-5
title: "[Visão Computacional] Motor de OCR para ANPR, Normalização com Regex & Votação Majoritária Temporal (Evolução de v01 a v11) (#5)"
authors: [jbgih]
tags: [computer-vision, anpr, easyocr, regex, voting-ensemble, python]
date: 2026-06-29
project: anpr_vision
description: "Validação sintática de placas, otimização do EasyOCR, votação por maioria em janela deslizante temporal e a jornada de desenvolvimento ao longo de 11 iterações de v01 a v11."
keywords: [EasyOCR Reconhecimento de Placas, ANPR Majority Voting Ensemble, Normalização Regex Placas, Acurácia OCR Visão, Sistemas Inteligentes de Transporte ITS]
---

![Votação Majoritária Temporal e Validação Final](./images/01_voting_evolution.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Quadros isolados sofrem inevitavelmente com erros de leitura pontuais por reflexo ou vibração (ex.: confundir `6` com `8` ou `B` com `8`).
> - **Solução**: Combinação de EasyOCR, correção sintática por expressões regulares (Regex) e comitê de decisão por maioria temporal (*Sliding-Window Majority Voting*) sobre 11 quadros sucessivos.

{/* truncate */}

---

### 1. O Mecanismo de Votação por Maioria Temporal

Em vez de confiar no resultado de um único quadro instável, o sistema agrega predições em uma janela deslizante contínua de 11 frames:

```mermaid
flowchart TD
    F1["Quadro 1: 24가1511"] --> Buffer[Buffer Circular: 11 Quadros]
    F2["Quadro 2: 24가1511"] --> Buffer
    F3["Quadro 3: 24가1571 (Erro de Leitura)"] --> Buffer
    F4["Quadro 4: 24가1511"] --> Buffer
    Buffer --> Voting{"Votação Majoritária: Qual string tem maior frequência?"}
    Voting -->|8 de 11 Votos| Confirmed["Placa Confirmada: 24가1511 (Confiança: 94.2%)"]
```

---

### 2. A Evolução do Projeto: De v01 a v11

Ao longo de 11 iterações de engenharia, a equipe elevou a precisão global de ponta a ponta de modestos 31% para impressionantes 96% em condições reais de tráfego.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Consenso Temporal**: A votação por maioria em janela deslizante neutraliza erros transientes de vibração da câmera.
2. **Correção Sintática por Regex**: Padrões sintáticos inválidos são tratados antes da computação dos votos.
3. **Robustez Comprovada**: Mais de 11 ciclos evolutivos consolidaram uma precisão superior a 96% em tráfego real.
4. **Sistema Completo**: A integração dos 6 módulos resulta em uma solução pronta para produção em sistemas ITS.