---
slug: 2026-04-14-maeumjigi-10
title: "[Maeumjigi Capstone Dev Log #10] Lifting API Limits and Resuming Data Synthesis"
authors: [jbgih]
tags: [devlog, API-limits, synthetic-data, data-generation, troubleshooting]
date: 2026-04-14
---

![Cover Image](./images/01_cover.png)

April 14 is the day we resumed the synthetic data (v5) generation work, which had been temporarily halted since the bill bomb incident. We increased the API billing limit (lifted the restriction) and ran the system, but once again, it didn't go smoothly.

### "API limit lifted, please resume operation!"

- **Problem**: During our last attempt at massive data generation, the script was forcibly stopped because we exceeded the monthly API limit.
- **Process**: 
  > "Proceed with work according to v5_emotion_data_generation_commands.md"
  > "API limit lifted, please resume operation" (23:32)
  > "API limit lifted, please resume operation" (00:11)
- **Result**: We logged into the Claude API console, boldly increased the billing limit, and lifted the restriction. We repeatedly instructed the AI to resume generating data from where it stopped and restarted the pipeline.

### Repairing the Broken Pipeline and Unmanned Automation

- **Problem**: The API limit was lifted, but for some reason, new data was not being generated properly.
- **Process**:
  > "Nothing is being generated. Please check"
  > "When the task is complete, automatically disconnect the API after checking the results (All related permissions are granted, so no need to ask for permission)"
- **Result**: We made the AI independently check and fix the tangles that occurred in the middle of the generation logic (tracking `v5_sync_progress.json`). Since we couldn't stand by and fix errors every time, we gave an unmanned automation instruction: "I will give you all permissions, so when the task is done, automatically disconnect the API on your own and safely shut down."

![Terminal Screenshot](./images/02_term.png)

Today was a tough journey of balancing money (API fees), time, and automation scripts for data preprocessing. If the data generation is completed safely, we can finally move on to the next step, right?
See you in the next dev log!
