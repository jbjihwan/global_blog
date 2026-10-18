---
slug: 2026-04-08-maeumjigi-8
title: "[마음지기 캡스톤 개발일지 #8] API 요금 폭탄 사태와 Colab 파인튜닝 준비"
authors: [jbgih]
tags: [개발일지, API과금, Llama3.1, 파인튜닝, GoogleColab, 데이터전처리]
date: 2026-04-08
keywords: [마음지기 AI 챗봇, LLM 파인튜닝, AI 안전 가드레일, 캡스톤 디자인, 프롬프트 엔지니어링]
description: "단일 동기 호출의 병목을 해결하기 위해 비동기(Async) 병렬 처리 크롤링 및 데이터 생성 파이프라인을 구축하여 처리 속도를 5배 향상시킨 기록입니다."
---

![사진 01](./images/01_cover.png)

4월 8일은 마음지기 프로젝트를 진행하면서 가장 큰 위기이자 '웃픈' 해프닝이 발생한 날입니다. 바로 **Claude API 월별 한도 초과 및 요금 폭탄 사태**입니다.

{/* truncate */}
