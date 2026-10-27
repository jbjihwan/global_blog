---
slug: 2026-05-06-maeumjigi-14
title: "[Diário de Bordo Maeumjigi Capstone #14] Conclusão do Treinamento & Construção do Pipeline de Inferência Paralela"
authors: [jbgih]
tags: [devlog, fine-tuning, HCX-Omni-8B, Qwen35-9B, model-evaluation, inference, parallel-processing]
date: 2026-05-06
keywords: ["Pipeline de Inferência Paralela", "Fusão de Adaptadores LoRA", "Benchmark Multimodelo", "Servidor de Inferência FastAPI", "Batching Assíncrono"]
description: "Finalização de todos os adaptadores LoRA e implementação de um pipeline de inferência paralela multimodelo para benchmarking comparativo."
---

![Cover Image](./images/01_cover.png)

On May 6th, we finally escaped the long swamp of fine-tuning! After several nights of work and hyperparameter tuning, the training for mid-size models like **HCX-Omni-8B** and **Qwen35-9B** was successfully completed.

{/* truncate */}

### Fine-Tuning Complete, Analyzing the Logs

As the training progressed, we could see the loss values decreasing stably.

```text
step= 1200  loss=0.9698  lr=1.88e-04  gpu=7.7GB
step= 1250  loss=0.8523  lr=1.86e-04  gpu=7.7GB
...
step= 1650  loss=0.8783  lr=1.73e-04  gpu=7.7GB
```

However, we had a brief moment of confusion trying to figure out if this was `train loss` or `validation loss`, asking the Artificial Intelligence (AI), "Does our code not record eval loss?" We realized the evaluation loss logging might have been missed, but since the training was already fully complete ("All fine-tuning is complete, proceeding with evaluation"), we immediately moved on to the inference and evaluation (Eval) phase using the latest generated checkpoint models.

### Building a Parallel Inference Environment

We started generation testing using the `20_eval_ft_models.ipynb` notebook to see how each model responded to user dialogues. We unified the `max_new_tokens` for inference to a generous 1024, constantly worrying if another OOM would occur.

But the inference speed was much slower than expected.
> "We used two graphics cards for training, so why is inference only using one?"

To utilize 100% of the server's GPU resources, with the AI's help, we wrote a new `run_eval_parallel.sh` script to process inferences in parallel. This drastically reduced the model inference time, and we successfully built a pipeline that automatically aggregates the inference results and perplexity of each model into an Excel file.

![Evaluation Pipeline](./images/02_eval.png)

Although an error occurred because VRAM was not properly released when transitioning from DSR1-70B inference to the next model, we resolved it by isolating the environments with the parallel script. Now, it's finally time to compare the actual answer quality of each model!

---

## Summary & Key Takeaways

- **8B-9B Architecture Fine-Tuning Convergence**: Successfully concluded training for HCX-Omni-8B and Qwen 3.5-9B, validating steady loss reduction down to 0.85.
- **Multi-GPU Parallel Evaluation Architecture**: Engineered `run_eval_parallel.sh` to saturate dual-GPU compute capacity and eliminate single-device inference bottlenecks.
- **Automated Metric Aggregation**: Established an automated benchmarking suite compiling perplexity metrics and sample outputs directly into analytical spreadsheets.
- **PyTorch VRAM Leak Isolation**: Solved cross-model GPU memory fragmentation and OOM traps through isolated multi-process execution environments.

