---
slug: 2026-05-04-maeumjigi-13
title: "[Maeumjigi Capstone Dev Log #13] Limits of 70B Training and the Pivot to Mid-Size Models (HCX, Qwen)"
authors: [jbgih]
tags: [devlog, fine-tuning, HCX-Omni-8B, Qwen35-9B, checkpoints, hyperparameters, Artificial Intelligence (AI)]
date: 2026-05-04
keywords: [AI Mental Health Chatbot, LLM Fine-tuning, AI Safety Wrapper, Capstone Project, Prompt Engineering]
description: "Recognizing synthetic data fatigue and restructuring training corpora with a 2:1 human-to-synthetic ratio to restore genuine conversational depth."
---

![Cover Image](./images/01_cover.png)

After experiencing the OOM (Out of Memory) hell during the fine-tuning of massive 70B models, on May 4th, we attempted a bold change in strategy. By drastically reducing the batch size, we barely managed to push the 70B models (Llama3.3, DeepSeek-R1) to `checkpoint-1200` and `1300`, but the training time was absurdly long, resulting in terrible efficiency.

{/* truncate */}
