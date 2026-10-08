---
slug: 2026-04-03-maeumjigi-5
title: "[Maeumjigi Capstone Dev Log #5] Purifying 100,000 Emotion Data Points and the Pressure of API Costs"
authors: [jbgih]
tags: [devlog, data-cleaning, ClaudeAPI, emotion-classification, Llama3.1, api-cost]
date: 2026-04-03
---

![Cover Image](./images/01_cover.png)

This is the record of April 3, the day we began in earnest the task of refining the training conversation data to feed into the deep learning model (Llama 3.1).
It was also the day we ran a massive pipeline that makes the AI read the text and judge the emotion on its own, going beyond simple data merging.

### Reclassifying Data Emotions (v3 -> v4)

- **Problem**: The emotion labeling of the existing dataset (`Emotion_train_dataset_v3`) did not perfectly align with our specific psychological counseling goals. Out of a total of 1 million data points, we needed to filter only the meaningful ones and accurately map their emotions.
- **Process**: 
  > "The scope is the entire 1 million... Because Claude, as a psychological counseling expert, will read the conversation and directly map the emotion. We are filtering only what falls under our emotion classification and excluding the rest."
- **Result**: We established `v4_plan.md` and started the work. Initially targeting 100,000 lines of data, we wrote and ran a script that integrates the Claude API to grasp the conversational context and reclassify emotions.

### The Horror of LLM API Billing

- **Problem**: As we threw massive amounts of text data at an LLM (Claude) for evaluation, the API usage (token count) increased exponentially.
- **Process**:
  > "I'm already using Claude with a Pro subscription, do I need a separate API?"
  > "Is there a way to use Claude Code instead of the Anthropic API? The billing is burdensome."
  > "The actual cost came out to $10.27."
- **Result**: We painfully realized that, completely separate from the Claude Pro subscription ($20/month), the Anthropic API called by the Python script for automated batch processing is billed on a pay-as-you-go basis depending on usage. Just processing 100,000 test lines instantly cost us about $10.27. Realizing that processing all 1 million records would cost a fortune, it was a day we learned firsthand the importance of model optimization and data sampling.

![Terminal Screenshot](./images/02_term.png)

Today was the day we hit the realistic wall of 'computing costs' inevitably encountered during deep learning data preprocessing.
Although we successfully obtained high-quality, refined data (`v4_report.md`), it was a valuable experience that left us deeply contemplating how to balance cost and efficiency as we proceed with fine-tuning!
