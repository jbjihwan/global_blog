---
slug: 2026-05-17-maeumjigi-19
title: "[Maeumjigi Capstone Dev Log #19] Automating Reports and Backend DB Troubleshooting"
authors: [jbgih]
tags: [devlog, fine-tuning, report, backend, DB, troubleshooting, capstone]
date: 2026-05-17
---

![Cover Image](./images/01_cover.png)

I must correct my previous assumption that "May 13th was the last of Maeumjigi's May development"! On May 17th, a massive wave of backend integration testing and report drafting hit us.

### Automating the Fine-Tuning Report using AI

There was simply not enough time for a human to manually analyze the massive result graphs from the 2nd fine-tuning (`fine_tuning_2`).

> "Create a prompt to write a report comparing the inference results of the models. Save it as report_prompt.md and write the report."

I attempted prompt engineering to have the AI interpret the metrics and automatically draft the report. Ultimately, the AI analyzed the pros and cons of each model and the differences based on Alpha values, generating an excellent Word (.docx) report draft.

### Backend DB Integration and the Swamp of 401 Unauthorized

Right after the report, I started pushing `backup.sql` data into the local PostgreSQL DB to test the system stability of the frontend and backend.

> "I logged in successfully after running the backend and frontend, but nothing responds when I click menus."
> "Email or password incorrect... INFO: POST /auth/login 401 Unauthorized"

I successfully pushed the DB dump and accessed the web, but fell into a hell of `401 Unauthorized` login errors. I created `debug_login.py` and endlessly restarted the uvicorn server for troubleshooting.

![DB Troubleshooting](./images/02_db.png)

### Contemplating Knowledge Graphs

> "Techniques using ontology and knowledge graphs are rising. Using these might create a chatbot with better stability than just focusing on a single LLM."

Late at night, to overcome the limitations of simple LLM fine-tuning, I began designing `chatbot_design_prompt.md` to explore fusing ontologies and Knowledge Graphs. As we pass mid-May, the scale of the project is growing massive!
