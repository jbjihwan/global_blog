---
slug: 2026-05-06-maeumjigi-14
title: "[마음지기 캡스톤 개발일지 #14] 모든 파인튜닝 완료 및 병렬 추론(Eval) 환경 구축"
authors: [jbgih]
tags: [개발일지, 파인튜닝, HCX-Omni-8B, Qwen35-9B, 모델평가, 추론, 병렬처리]
date: 2026-05-06
keywords: [마음지기 AI 챗봇, LLM 파인튜닝, AI 안전 가드레일, 캡스톤 디자인, 프롬프트 엔지니어링]
description: "HCX-Omni-8B와 Qwen35-9B의 파인튜닝을 완수하고, 듀얼 GPU를 100% 활용하는 멀티 GPU 병렬 추론(Eval) 자동화 스크립트를 구축한 내용입니다."
---

![사진 01](./images/01_cover.png)

5월 6일, 드디어 길고 길었던 파인튜닝의 늪에서 빠져나왔습니다! 며칠간의 밤샘 작업과 하이퍼파라미터 조율 끝에 **HCX-Omni-8B**와 **Qwen35-9B** 등 중소형 모델들의 학습이 성공적으로 마무리되었습니다.

{/* truncate */}
