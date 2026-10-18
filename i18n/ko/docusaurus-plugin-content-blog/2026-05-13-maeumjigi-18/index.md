---
slug: 2026-05-13-maeumjigi-18
title: "[마음지기 캡스톤 개발일지 #18] 추론 토큰(Token) 확장과 2차 파인튜닝 결과 비교"
authors: [jbgih]
tags: [개발일지, 파인튜닝, 추론, max_new_tokens, 공감능력, 캡스톤디자인]
date: 2026-05-13
keywords: [마음지기 AI 챗봇, LLM 파인튜닝, AI 안전 가드레일, 캡스톤 디자인, 프롬프트 엔지니어링]
description: "짧고 경직된 답변 문제를 해결하기 위해 max_new_tokens를 384로 확장하고, LoRA alpha 파라미터(8 vs 16)에 따른 답변 공감도 변화를 분석합니다."
---

![사진 01](./images/01_cover.png)

어제 발견했던 하드코딩 버그를 모두 고치고, 드디어 제대로 된 2차 파인튜닝 모델들의 추론(Inference) 테스트를 재개한 5월 13일입니다.

{/* truncate */}
