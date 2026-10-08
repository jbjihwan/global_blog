---
slug: 2026-05-08-maeumjigi-16
title: "[Maeumjigi Capstone Dev Log #16] Fatal Mistake, 2nd Fine-Tuning, and React Native App Launch"
authors: [jbgih]
tags: [devlog, fine-tuning, LoRA, hyperparameters, ReactNative, app-development, frontend]
date: 2026-05-08
---

![Cover Image](./images/01_cover.png)

May 8th was the day we were building our capstone design mid-term presentation (PPT) based on the fine-tuning results. However, while happily filling in the slides, I discovered a massive, chilling mistake.

### Discovering the Fatal LoRA Hyperparameter Mistake

I was refining the model structure diagrams and hyperparameter info with the AI for the PPT.

> "Looking at the fine-tuning examples, the answers are shorter than the base model. I think this is because setting LoRA's r to 8 and alpha to 16 reduced the intermediate features too much..."
> "Wait, it was a/r? I thought it was r/a...??? I really applied LoRA greedily..."

When fine-tuning with LoRA, it's standard to set the `alpha` value equal to or twice the `rank` value. However, I completely misunderstood the scaling ratio equation, setting it in a way that either severely suppressed or excessively amplified the weight updates. No wonder the fine-tuned models' answers were unnaturally short and chopped off—the fault lay right at my fingertips.

### The Decision for 2nd Round Fine-Tuning (fine_tuning_2)

Although we already had the 1st round results, we couldn't just move on for a perfect 'Maeumjigi'. I immediately created a `fine_tuning_2` folder and decided on a 2nd round of fine-tuning.

> "The models to use this time are HCX-Text-1p5B, Llama33-70B, and Qwen35-9B. Train on MIG-0 with rank=16, alpha=16, and on MIG-1 with rank=16, a=8."
> "Extract the top 2000 longest entries from Daily_train_dataset.jsonl and create a file named Daily_train_dataset_long.jsonl."

To prevent the answers from becoming too short, we extracted only the top 2000 datasets with the longest text length. We also split our MIG (Multi-Instance GPU) resources to run parallel training, directly comparing the performance differences based on the rank and alpha ratios.

### Starting Frontend (App) Development While the Backend Trains

![App Development](./images/02_app.png)

While the models fell back into the cycle of training, I didn't just sit around. I finally started developing the frontend app where actual users will meet 'Maeumjigi'!

> "I need to show a QR code to run maeum-app... but when I type npx go start, I only get an error message. How and where can the QR code be shown?"

I created the `maeum-app` project using React Native (Expo) and struggled to launch the local server and connect it to my smartphone. I even mistakenly typed `npx go start` instead of `expo`, but I finally succeeded in pulling up the Expo QR code and setting up the app icons (`assets/logo.png`). It was a thrilling day where the brain of the backend (AI) and the face of the frontend (App) were being built simultaneously.
