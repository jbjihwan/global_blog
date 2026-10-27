---
slug: 2026-04-09-maeumjigi-9
title: "[Journal de bord Maeumjigi Capstone #9] Résolution des erreurs de fine-tuning Llama 3.1 & Soutenance intermédiaire de mi-semestre"
authors: [jbgih]
tags: [devlog, Llama3.1, fine-tuning, troubleshooting, PPT-generation, ERD]
date: 2026-04-09
keywords: ["Résolution Erreurs CUDA OOM", "Entraînement Llama 3.1 QLoRA", "Soutenance Mi-Semestre Capstone", "Gestion Mémoire GPU", "Gradient Checkpointing"]
description: "Résolution des erreurs CUDA Out-of-Memory (OOM) lors de l'entraînement et succès de la présentation académique de mi-parcours."
---

![Cover Image](./images/01_cover.png)

On April 9, using the Colab notebook we ambitiously completed yesterday, we finally attempted the first training (fine-tuning) of our artificial intelligence model (Llama 3.1). However, reality was not that easy, and we had to face numerous errors. It was also a tough day as we had to simultaneously create the presentation materials for the 6th week of the Capstone Design project.

{/* truncate */}

### The Endless Struggle with Colab Fine-Tuning Errors

- **Problem**: As soon as we executed `llama31_finetuning_colab.ipynb` created yesterday, various errors poured out.
- **Process**: 
  > "Why is an error occurring during M1 fine-tuning in llama31_finetuning_colab (3).ipynb?"
  > "The executed result contains the eos_token. Why is this problem occurring?"
- **Result**: A series of problems occurred, such as the special token (`eos_token`) not being processed correctly when the Artificial Intelligence (AI) model spit out the training data, and memory overflow issues. We repeated the process of copying and pasting the entire error log to Claude to get solutions and modifying the code multiple times. Finally, after many twists and turns, the training was completed, and we were able to extract a meaningful result graph called `학습데이터별학습결과.png`!

### The AI Assistant's Presentation (PPT) Creation

- **Problem**: While staying up all night training the model, we had to immediately create a PPT on the 6th-week frontend and database progress for the presentation next week.
- **Process**:
  > "Capstone_Week6_Frontend.pptx is a collection of images introducing the overview so far. Please use this to create a presentation for this week's progress."
  > "Please express the tables of the database design so that the relationships can be seen, referring to the tables implemented in the backend... The table is too large and messy. Please place the User table in the center."
- **Result**: Surprisingly, the AI wove the frontend image screenshots together to create a presentation script and slide skeleton. Even when I persistently gave feedback (centering the User table) asking it to draw a complex database ERD (Entity Relationship Diagram) based on the backend code, it perfectly organized and explained the database relationship diagram.

![Terminal Screenshot](./images/02_term.png)

Today was a day to feel the thrill of directly tuning the latest language model called Llama 3.1 with my own hands (and the AI's brain). At the same time, we are learning how to fully utilize AI not only for coding but also for creating presentation materials and designing Database (DB) architecture diagrams. How smart has our Maeumjigi AI become? We will reveal the test results next time!

---

## Summary & Key Takeaways

- **First Llama 3.1 Fine-Tuning Run**: Executed initial LoRA fine-tuning on Llama 3.1 8B via Google Colab, resolving critical `eos_token` formatting and memory overflow issues.
- **Empirical Training Diagnostics**: Extracted empirical loss convergence graphs across dataset variants, confirming valid weight updates for specialized empathetic counseling.
- **AI-Assisted Slide Deck Synthesis**: Leveraged LLMs to convert frontend interface screenshots into a polished 6th-week capstone presentation script and slide structure.
- **Automated Database ERD Architecture**: Directed AI to reverse-engineer backend models into a user-centric Entity-Relationship Diagram (ERD), clarifying schema constraints.