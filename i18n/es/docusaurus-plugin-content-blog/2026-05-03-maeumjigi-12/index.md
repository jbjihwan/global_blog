---
slug: 2026-05-03-maeumjigi-12
title: "[Registro de Desarrollo Maeumjigi #12] Fine-Tuning de Modelos Masivos de 70B y Lucha con la Memoria GPU (OOM)"
authors: [jbgih]
tags: [devlog, fine-tuning, Llama3.3-70B, DeepSeek-R1-70B, OOM, troubleshooting, GPU]
date: 2026-05-03
keywords: [Chatbot de IA para salud mental, Fine-tuning de LLM, Proyecto Capstone, Seguridad de IA, Ingeniería de Prompts]
description: "Desafío del ajuste fino en modelos de 70B parámetros con QLoRA de 4 bits y resolución de errores OOM de memoria VRAM."
---

![Imagen de Portada](./images/01_cover.png)

El 3 de mayo, habiendo ganado suficiente experiencia con los modelos 8B, nuestro equipo finalmente desafió a los reyes del rendimiento: el fine-tuning de modelos masivos de **70B (70 mil millones de parámetros)**. Intentamos entrenar tanto Llama 3.3 70B como DeepSeek-R1 70B, pero chocamos con un muro de recursos de hardware.

{/* truncate */}
