---
slug: 2026-04-14-maeumjigi-10
title: "[Maeumjigi 毕业设计开发日志 #10] 解决 API 速率限制: 无人自动化与高可用数据合成流水线"
authors: [jbgih]
tags: [devlog, api-rate-limits, synthetic-data, data-generation, fault-tolerance, state-machine, capstone]
date: 2026-04-14
keywords: [Anthropic API Rate Limit, Synthetic Data Generation Pipeline, Unmanned Autonomous Script, Exponential Backoff Jitter, Atomic JSON Checkpointing]
description: "攻克 API 速率限制困境：升级 Anthropic 账单层级，构建具备原子检查点机制的无人值守容错流水线，平稳恢复 v5 合成数据工程。"
---

![Cover Image](./images/01_cover.png)

April 14, 2026, was a masterclass in distributed pipeline fault tolerance. Following our temporary halt from unexpected API expenditure spikes, our team resumed synthetic data generation (v5) to enrich our empathy training set. However, unlocking higher billing tiers immediately exposed our worker scripts to severe rate-limiting (`HTTP 429 Too Many Requests`), partial file corruptions, and pipeline stalls. 

Here is how we re-engineered the synthesis architecture into a self-healing, unmanned autonomous pipeline.

{/* truncate */}

### 1. The Anatomy of API Rate Limits: Tier Escalation & Throttling

When synthesizing multi-turn empathetic dialogues at scale using foundation models (such as Claude 3.5 Sonnet), standard API tiers quickly become an engineering bottleneck. Ingestion of large system contexts causes rapid exhaustion of both Requests Per Minute (RPM) and Tokens Per Minute (TPM).

| API Tier Level | Requests Per Minute (RPM) | Tokens Per Minute (TPM) | Monthly Credit Cap | Concurrency Strategy |
| :---: | :---: | :---: | :---: | :--- |
| **Tier 1 (Default)** | 50 RPM | 40,000 TPM | $100 | Serial requests only; high latency |
| **Tier 2 (Deposit)** | 1,000 RPM | 80,000 TPM | $500 | Modest concurrency (4 workers); frequent 429s |
| **Tier 3 (Enterprise)** | **2,000 RPM** | **160,000 TPM** | **$1,000+** | **Asynchronous batching (16 workers) with jitter** |

After negotiating a tier escalation and depositing preliminary billing credits, our rate ceiling lifted. Yet raw speed triggered an unexpected secondary problem: network micro-outages and API dropouts began corrupting intermediate progress markers (`v5_sync_progress.json`).

---

### 2. The Resilient Unmanned State Machine

To run massive overnight generation batches without human babysitting, we refactored our worker script into an autonomous state machine equipped with **Atomic File Operations** and **Full Jitter Exponential Backoff**.

```mermaid
stateDiagram-v2
    [*] --> Idle: Initialize Worker
    Idle --> Fetch_Batch: Read Last Valid Index from Checkpoint
    
    state Fetch_Batch {
        [*] --> LoadSlice
        LoadSlice --> ValidateInput
    }

    Fetch_Batch --> Dispatch_API: Async Request to LLM Engine
    
    state Dispatch_API {
        [*] --> SendRequest
        SendRequest --> CheckResponse
    }

    Dispatch_API --> Backoff_Retry: HTTP 429 / 503 Detected
    Backoff_Retry --> Dispatch_API: Exponential Backoff with Jitter (2^n + uniform)
    
    Dispatch_API --> Process_Result: HTTP 200 OK
    Process_Result --> Atomic_Save: Append to JSONL & Write Temp Checkpoint
    Atomic_Save --> Commit_State: Atomic os.replace (v5_sync_progress.json)
    
    Commit_State --> Fetch_Batch: More Samples Pending
    Commit_State --> Shutdown_Safe: Target Threshold Reached
    
    Shutdown_Safe --> [*]: Disconnect API & Log Final Summary
```

---

### 3. Engineering Atomic Checkpointing & Exponential Backoff

A critical vulnerability in our early script was opening `v5_sync_progress.json` with standard `w` mode: if an unhandled OS kill signal arrived while writing, the file truncated to 0 bytes, losing days of progress tracking.

We solved this via POSIX/Windows atomic file swapping and exponential backoff retry decorators:

```python
# Fault-tolerant atomic progress tracking & backoff implementation
import os
import json
import time
import random

def save_atomic_progress(filepath: str, data: dict):
    temp_filepath = f"{filepath}.tmp"
    with open(temp_filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Atomic swap guarantees zero file corruption even during crashes
    os.replace(temp_filepath, filepath)

def call_api_with_resilient_backoff(api_func, payload, max_retries=5):
    retries = 0
    base_delay = 1.5
    while retries < max_retries:
        try:
            return api_func(payload)
        except Exception as e:
            if "429" in str(e) or "503" in str(e):
                retries += 1
                # Exponential backoff with Full Jitter
                sleep_time = (base_delay * (2 ** retries)) + random.uniform(0.1, 1.0)
                time.sleep(sleep_time)
            else:
                raise e
    raise RuntimeError(f"Max retries exceeded for payload: {payload}")
```

---

### 4. Unmanned Automation Directive

Because our team members needed uninterrupted rest, we granted Claude Code full autonomous watchdog authority:

> **Execution Directive**:  
> *"All permissions are granted. Monitor synthesis progress continuously. If a connection failure occurs, recover from the last atomic checkpoint. Once all 25,000 synthetic pairs are generated and validated, automatically terminate the background API worker and safely power down the compute instance."*

The AI agent executed this directive flawlessly between 23:30 and 06:15 without a single human intervention.

![Terminal Screenshot](./images/02_term.png)

---

### 5. Day 10 Milestones & Metrics

| Quantitative Metric | Measurement | Technical Impact |
| :--- | :---: | :--- |
| **Synthesis Batch Target** | 25,000 Pairs | Emotion-enriched high-difficulty counseling scenarios |
| **API Failure Rate (Post-Backoff)** | **0.00%** | Zero lost payloads over 7-hour overnight run |
| **Throughput Rate** | 62.4 requests/min | Sustained near maximum Tier 2/3 allocation |
| **Checkpoint Integrity** | 100% | Flawless atomic state persistence despite 3 network blips |

In Dev Log #11, we evaluate our first model checkpoint (M6) trained on this synthesized dataset and benchmark its empathetic resonance!

---

## 核心总结与技术要点

- **攻克 API 频控与并发瓶颈**：针对大规模多轮心理对话合成，升级 API 计费层级并精细化调配 RPM 与 TPM 资源配额。
- **高弹性自愈状态机架构**：针对 HTTP 429 限流与 503 服务抖动，设计融合指数退避与随机抖动 (Full Jitter) 的自适应重试管道。
- **原子级检查点机制保障零损耗**：采用基于 `os.replace` 的原子化文件替换方案，彻底杜绝意外断电或进程中断造成的进度文件破坏与数据归零。
- **全无人值守夜间全自动合成**：赋予 AI 智能体自主看门狗权限，在无人工干预的情况下通宵高效完成 25,000 组高质量心理咨询对话数据的合成与校验。

