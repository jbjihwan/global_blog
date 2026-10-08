---
slug: 2026-05-30-maeumjigi-22
title: "[Maeumjigi Capstone Dev Log #22] 4th Fine-Tuning Complete! Architecture Design & Final Report"
authors: [jbgih]
tags: [devlog, fine-tuning, architecture, capstone, final report]
date: 2026-05-30
---

![Cover Image](./images/01_cover.png)

In the final week of May (27th-30th), we dedicated our efforts to wrapping up the results of the highly anticipated **4th Fine-Tuning (fine_tuning_4)** and solidifying the system's framework.

### Final Checkpoint 4400 and Graph Analysis

> "Qwen35-9B_mixed_7_3/checkpoints/checkpoint-4400/adapter_config.json"

The 4th fine-tuning model, trained with a mix of daily casual chat and emotional counseling data, finally finished training and yielded the optimal weight: `checkpoint-4400`.

In previous fine-tunings, there was an overfitting issue where the model would respond in an overly serious counseling mode even to casual chat. As a result of experimenting with the data mix ratio, the model has finally been reborn as a 'perceptive' chatbot that perfectly distinguishes between and appropriately responds to daily conversation and serious crisis counseling!

We visualized all evaluation metrics with `matplotlib` graphs to prove the performance differences at a glance.

### Chatbot System Architecture Design and Final Report

> "chatbot_architecture.html generation complete"
> "Please write the results of fine_tuning_4 as a report (.docx)."

![System Architecture](./images/02_architecture.png)

To serve the verified model as a real app, we designed the entire system architecture and Knowledge Graph integration plan under the name `chatbot_architecture.html`.

And on May 30th, with the AI's help, we automatically generated the `fine_tuning_4_report.docx`, successfully concluding Phase 1 of our fine-tuning project. The report bluntly contains the actual response text comparisons between the original base model and our fine-tuned model, proving that all our hard work was not in vain!

With this, the breathless May dev logs of the Maeumjigi project are all wrapped up. What new challenges await in June?
