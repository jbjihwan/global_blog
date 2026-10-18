---
slug: 2026-05-04-maeumjigi-13
title: "[Registro de Desarrollo Maeumjigi #13] Límites de Entrenamiento de 70B y el Giro a Modelos Medianos (HCX, Qwen)"
authors: [jbgih]
tags: [devlog, fine-tuning, HCX-Omni-8B, Qwen35-9B, checkpoints, hyperparameters, Inteligencia Artificial (AI)]
date: 2026-05-04
keywords: [Chatbot de IA para salud mental, Fine-tuning de LLM, Proyecto Capstone, Seguridad de IA, Ingeniería de Prompts]
description: "Reestructuración del dataset con una proporción 2:1 de datos humanos y sintéticos para recuperar la naturalidad conversacional."
---

![Imagen de Portada](./images/01_cover.png)

Después de experimentar el infierno del OOM durante el entrenamiento de los masivos modelos de 70B, el 4 de mayo intentamos un cambio audaz de estrategia. Reduciendo drásticamente el tamaño del lote, apenas logramos empujar los modelos 70B a `checkpoint-1200`, pero el tiempo de entrenamiento fue absurdamente largo.

{/* truncate */}
