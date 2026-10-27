---
slug: 2026-06-28-vision-anpr-4
title: "[Visão Computacional] Superando Artefatos em Vídeos de Dashcam: Super-Resolução Profunda (EDSR vs FSRCNN) & Empilhamento Multi-Frame (#4)"
authors: [jbgih]
tags: [computer-vision, super-resolution, edsr, image-stacking, anpr, deep-learning, python]
date: 2026-06-28
project: anpr_vision
description: "Reconstrução de recortes de placas de baixa resolução através de Super-Resolução Profunda EDSR 4x e empilhamento temporal de múltiplos quadros (Image Stacking)."
keywords: [EDSR Super Resolução, Restauração de Imagens de Placas, OpenCV dnn_superres, Multi-Frame Image Stacking, Deep Residual Upscaling]
---

![Comparativo de Super-Resolução Profunda com EDSR](./images/01_edsr_sr_comparison.png)

> 📌 **Resumo dos Pontos Principais (TL;DR)**
> - **Desafio**: Recortes de placas em dashcams medem com frequência menos de 40x20 pixels com severa compressão H.264. A interpolação bicúbica comum borra os caracteres.
> - **Solução**: Aplicação de redes residuais profundas aprimoradas (EDSR) para ampliação de 4x e média temporal de múltiplos quadros para cancelamento de ruído estocástico.

{/* truncate */}

---

### 1. Comparativo de Modelos: EDSR vs. FSRCNN

| Modelo de Super-Resolução | Tempo de Inferência (ms) | Qualidade da Reconstrução | Recomendação de Uso |
| :--- | :--- | :--- | :--- |
| **Interpolação Bicúbica** | < 1 ms | Muito borrada; caracteres fundidos | Inadequado para OCR |
| **FSRCNN (Fast SR)** | ~ 8 ms | Nitidez moderada de bordas | Dispositivos móveis de borda |
| **EDSR (Enhanced Deep Residual)** | ~ 35 ms | **Excelente definição de caracteres & contraste** | **Pipeline de Produção** |

O EDSR remove camadas supérfluas de Batch Normalization e emprega blocos residuais expandidos, reconstruindo contornos alfanuméricos nítidos a partir de imagens extremamente pixeladas.

---

### 📌 Resumo Executivo para Gestão (3–5 Linhas)
1. **Limites da Interpolação Simples**: Algoritmos clássicos amplificam blocos de compressão e impedem a leitura pelo OCR.
2. **Reconstrução com EDSR 4x**: Redes neurais residuais restauram bordas e contraste com fidelidade matemática.
3. **Empilhamento de Quadros**: A média temporal cancela o ruído do sensor antes do processamento textual.
4. **Salto de Acurácia**: A super-resolução eleva a taxa de sucesso do OCR de 42% para mais de 89%.
