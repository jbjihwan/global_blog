---
slug: 2026-05-03-maeumjigi-12
title: "[Maeumjigi Capstone Dev Log #12] 70B Massive Model Fine-Tuning and GPU Memory (OOM) Struggle"
authors: [jbgih]
tags: [devlog, fine-tuning, Llama3.3-70B, DeepSeek-R1-70B, OOM, troubleshooting, GPU]
date: 2026-05-03
keywords: [AI Mental Health Chatbot, LLM Fine-tuning, AI Safety Wrapper, Capstone Project, Prompt Engineering]
description: "Tackling 70B parameter model fine-tuning with 4-bit QLoRA and resolving GPU VRAM OOM errors through aggressive memory offloading."
---

![Cover Image](./images/01_cover.png)

On May 3, having gained enough experience with the 8B models, our team finally challenged the ultimate kings of performance: fine-tuning massive **70B (70 billion parameters)** models. We attempted to train both Llama 3.3 70B and DeepSeek-R1 70B, but as expected, we hit a massive hardware resource wall.

{/* truncate */}
