---
slug: 2026-04-01-maeumjigi-4
title: "[Maeumjigi Capstone Dev Log #4] Full-Scale Fine-Tuning Data Preprocessing"
authors: [jbgih]
tags: [devlog, AI-coding, ClaudeCode, capstone, fine-tuning, data-preprocessing, Llama3.1]
date: 2026-04-01
---

![Cover Image](./images/01_cover.png)

This is the record of April 1, when we began processing a massive amount of conversation data into a format suitable for training the Llama 3.1 model, which will become the core engine of the Maeumjigi project.

### Automated Execution According to the Preprocessing Plan

- **Problem**: To fine-tune the model, the raw data containing user utterances and chatbot responses had to be perfectly converted into a special JSONL format that Llama 3.1 can understand.
- **Process**: 
  > To Claude Code: "Proceed with the work according to llama31_finetuning_data_preprocessing_plan_short.md"
- **Result**: Based on the preprocessing plan document written yesterday, the AI agent independently built and executed the data cleaning and processing pipeline. Instead of a human manually converting tens of thousands of data points one by one, we simply handed over a single Markdown document with the rules and instructed it, "Process it exactly like this."

### Integrating Category Data and JSONL Conversion

- **Problem**: The preprocessing process was broken down into several steps, and finally, all the data had to be combined into one to complete the training dataset.
- **Process**:
  > To Claude Code: "Execute Step 4. Integrate the data of the two categories and convert it to the Llama 3.1 JSONL format."
- **Result**: The AI immediately executed Step 4 and merged the scattered conversation data from each category into one. It then wrote and executed a script to convert it into a JSONL file, strictly adhering to the precise prompt template required by Llama 3.1 (differentiating System, User, and Assistant roles).

![Terminal Screenshot](./images/02_term.png)

Today is the day when 'data preprocessing', the core of fine-tuning, began to run fully automatically via AI. It was a magical experience to see countless data points transformed into a trainable state with a single instruction: "Do it exactly as written in the document."
In the next post, we will continue with exciting dev logs on how we actually train and validate the model using this preprocessed data!
