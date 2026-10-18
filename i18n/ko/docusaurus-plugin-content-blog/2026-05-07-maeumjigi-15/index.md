---
slug: 2026-05-07-maeumjigi-15
title: "[마음지기 캡스톤 개발일지 #15] 5개 모델 파인튜닝 결과 시각화 및 로컬 환경 세팅"
authors: [jbgih]
tags: [개발일지, 파인튜닝, 결과분석, 시각화, Jupyter, 캡스톤디자인, AI]
date: 2026-05-07
keywords: [마음지기 AI 챗봇, LLM 파인튜닝, AI 안전 가드레일, 캡스톤 디자인, 프롬프트 엔지니어링]
description: "파인튜닝된 각 모델의 Perplexity와 벤치마크 지표를 분석하고, matplotlib을 활용해 모델별 성능 격차를 한눈에 파악하는 시각화 파이프라인을 구축합니다."
---

![사진 01](./images/01_cover.png)

5월 7일은 그동안 피땀 흘려 파인튜닝한 총 5개의 모델(Llama3.3-70B, DSR1-70B, HCX-Omni-8B, Qwen35-9B, HCX-Text-1.5B)의 결과를 집대성하고, 본격적인 시각화와 로컬 환경 구성을 진행한 날입니다. 

{/* truncate */}
