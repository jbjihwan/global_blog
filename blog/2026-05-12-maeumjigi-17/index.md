---
slug: 2026-05-12-maeumjigi-17
title: "[Maeumjigi Capstone Dev Log #17] 2nd Fine-Tuning Complete & The Trap of the Automation Pipeline"
authors: [jbgih]
tags: [devlog, fine-tuning, best-performance, checkpoint, hardcoding, capstone]
date: 2026-05-12
---

![Cover Image](./images/01_cover.png)

The 2nd round of fine-tuning (`fine_tuning_2`) parallel training, which was ambitiously started to correct the LoRA hyperparameter mistake (alpha/rank setup error), finally ended on May 12th!

### Extracting the Best Checkpoint and Building the Inference Pipeline

The fine-tuning for 3 models with 6 hyperparameter combinations was all completed. I immediately compared the `eval_loss` to extract the best performing checkpoints and moved them to the `adapter` folders for each model.

I also created a new `run_test_20_30.sh` script to run evaluation and result comparison all at once in the background on the server.

> "Currently, the HCX-Text-1p5B models generated 12 outputs in 15 minutes. GPU Util is 1.6GB per graphics card..."

However, the inference speed was still hopeless. Even the lightest 1.5B model couldn't even generate 1 answer per minute. The VRAM usage was only 1.6GB, meaning a bottleneck occurred because the Batch Size was set to 1. On top of this, server storage issues forced us to urgently migrate the project's base path from `~/home/` to `~/home/data/temporary/`, causing a huge fuss to modify all script paths.

### Falling into the Trap of Hardcoding

![Hardcoding Bug](./images/02_bug.png)

After painstakingly running all the evaluation codes, I discovered a horrifying fact.

> "Why is MODEL_ALIAS hardcoded to 'Qwen35-9B_a16' in 20_eval_ft_models.ipynb?"
> "So in the server logs, even for 20_eval_HCX-Text-1p5B_a8.ipynb, MODEL_ALIAS was defined as 'Qwen35-9B_a16'. You're telling me it's normal that the filename and model name are different?"

Yes. While writing the evaluation automation script, I accidentally hardcoded `MODEL_ALIAS`. The script diligently copied files to test the HCX model, but inside the code, it kept repeatedly loading only the `Qwen35-9B_a16` model and doing the same inference over and over!

It was a day that made me realize once again that fine-tuning is not a science, but a battle of meticulousness. I'll have to fix this hardcoded bug and run the inferences again tomorrow.
