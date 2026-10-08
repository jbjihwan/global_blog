---
slug: 2026-04-05-maeumjigi-6
title: "[Maeumjigi Capstone Dev Log #6] Preprocessing Final Report Automation and Frontend Kickoff"
authors: [jbgih]
tags: [devlog, final-report, automation, Next.js, capstone, data-preprocessing]
date: 2026-04-05
---

![Cover Image](./images/01_cover.png)

April 5th marks the day we wrapped up the arduous data preprocessing journey (v1~v4) by generating a final report, 
while simultaneously kicking off the frontend project that will become the face of the Maeumjigi web service.

### Perfect Documentation: From Markdown to DOCX and Graphs

- **Problem**: We needed to share the massive preprocessing journey with our advising professor and team members in a visually understandable way.
- **Process**: 
  > To Claude Code: "Please write a final report summarizing the data preprocessing process (v1, v2, v3, v4)... Add representative examples for each version."
  > "Please convert this md file to a docx file... Express things that can be graphed as graphs and add them."
- **Result**: Surprisingly, the AI analyzed the Python scripts and JSON data we had worked on and effortlessly wrote a core summary report in Markdown. Going even further, it independently installed Python libraries (`python-docx`, `matplotlib`), wrote a script, converted the Markdown into a neat Word (DOCX) file, and even drew and inserted emotion distribution graphs! It was a moment that drastically reduced the time wasted on documentation.

### Next.js Based Frontend Project Kickoff

- **Problem**: Separate from training the AI model, we needed a web interface where users could actually chat with the bot.
- **Process**: (Background Task) We instructed the setup of a Next.js-based frontend project to provide a fast and familiar UI for users (soldiers).
- **Result**: `package.json`, `tsconfig.json`, etc., were generated in the `maeumjigi/frontend/` path, successfully setting up the latest trending Next.js-based frontend environment.

![Terminal Screenshot](./images/02_term.png)

Today was the day we proved that AI's capabilities go far beyond simple coding, perfectly performing the role of an excellent office assistant through 'document summarization, graph visualization, and DOCX generation'.
Having climbed the huge mountain of data preprocessing, we have now officially raised the anchor for the frontend development that will meet the users!
