# 글로벌 블로그 83편 전수 선별 및 정예화 결과표 (Step 1~3 완료)

> 작성일: 2026-11-18 · 기준: Google AdSense 「가치가 별로 없는 콘텐츠」 및 Search Console `Crawled - currently not indexed` 해소

## 1. 최종 선별 및 고도화 요약

- **기존 전체 게시글**: 83편 (영문 `blog/` 83편, 한국어 `i18n/ko/` 83편)
- **최종 라이브 게시(`ACTIVE`)**: **20편** (기존 핵심 엔지니어링·오류 해결 19편 고도화 + Step 3 신규 오류 해결 글 1편 추가)
- **보관 이동(`_old/` 분리)**: **64편**
  - `ARCHIVE_LECTURE` (27편): 스탠포드 CS329A(17편)·CS146S(10편) 공개 강의 요약본 (2차 요약 콘텐츠 성격)
  - `ARCHIVE_DIARY` (20편): 마음지기 캡스톤 단문 일기·중간보고·일반 진행 기록 (`#9`, `#12`, `#16` 추가 포함)
  - `ARCHIVE_SIMULATION` (9편): `[Simulation]` 합성 데이터·재구성 로그 경고문이 포함된 공공예산 감사 시리즈
  - `ARCHIVE_YMYL` (5편): 자살·정신건강 위기 감지 YMYL 고위험 민감 주제 시리즈 (`mental-crisis` 4편 + 자살 정규식 포함 `maeumjigi-23` 1편)
  - `ARCHIVE_ADSENSE_META` (3편): 애드센스 승인·ads.txt 메타 가이드

---

## 2. 라이브 게시 및 고도화 완료 목록 (20편)

| 구분 | 폴더명 | 게시일 | 영문 본문(단어) | 한국어 본문(자) | 영문 제목 | 조치 내용 |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| `KEEP_CLEANED` | `2026-04-01-maeumjigi-4` | 2026-04-01 | 774w | 4107자 | [Maeumjigi Capstone Dev Log #4] Full-Scale Data Preprocessing: Llama 3.1 Chat Template & Autonomous JSONL Pipeline | 실제 에러 해결(Llama 3.1 Chat Template·API 429·FastAPI 401) 집중 유지 및 AI/임상 문구 정화 완료 |
| `KEEP_CLEANED` | `2026-04-14-maeumjigi-10` | 2026-04-14 | 844w | 4368자 | [Maeumjigi Capstone Dev Log #10] Resolving API Rate Limits: Unmanned Automation & Resilient Data Synthesis Pipeline | 실제 에러 해결(Llama 3.1 Chat Template·API 429·FastAPI 401) 집중 유지 및 AI/임상 문구 정화 완료 |
| `KEEP_CLEANED` | `2026-05-17-maeumjigi-19` | 2026-05-17 | 930w | 5439자 | [Maeumjigi Capstone Dev Log #19] Automated Evaluation Reports & FastAPI PostgreSQL 401 Debugging | 실제 에러 해결(Llama 3.1 Chat Template·API 429·FastAPI 401) 집중 유지 및 AI/임상 문구 정화 완료 |
| `KEEP_CORE` | `2026-05-17-rl-qlearning-1` | 2026-05-17 | 850w | 5382자 | [Webots Robotics] Q-Learning Autonomous Navigation: 648-Bin State Discretization & Socket Architecture (#1) | 핵심 엔지니어링 오류 해결·구현기 유지 |
| `KEEP_CORE` | `2026-05-18-rl-qlearning-2` | 2026-05-18 | 979w | 5497자 | [Webots Robotics] Tabular Q-Learning Implementation & Reward Shaping Tuning (#2) | 핵심 엔지니어링 오류 해결·구현기 유지 |
| `KEEP_CORE` | `2026-05-19-rl-qlearning-3` | 2026-05-19 | 741w | 4094자 | [Webots Robotics] Conquering Local Minima in 12-Wall Obstacles: Multi-Seed Headless Simulation (#3) | 핵심 엔지니어링 오류 해결·구현기 유지 |
| `KEEP_CORE` | `2026-05-20-rl-qlearning-4` | 2026-05-20 | 764w | 4231자 | [Webots Robotics] Deterministic Evaluation via evaluate_qlearning & Benchmark vs. DQN and SARSA (#4) | 핵심 엔지니어링 오류 해결·구현기 유지 |
| `KEEP_CORE` | `2026-05-21-rl-qlearning-5` | 2026-05-21 | 1150w | 5521자 | Sim-to-Real RL: Webots to Arduino with ArUco Vision Tracking (#5) | 핵심 엔지니어링 오류 해결·구현기 유지 |
| `KEEP_CORE` | `2026-06-25-vision-anpr-1` | 2026-06-25 | 596w | 3497자 | [Vision AI] Blackbox Lane Intrusion & Super-Resolution ANPR: 6-Stage End-to-End Pipeline & Real-Time Constraints (#1) | 핵심 엔지니어링 오류 해결·구현기 유지 |
| `KEEP_ENRICHED` | `2026-06-26-vision-anpr-2` | 2026-06-26 | 770w | 4631자 | [Vision AI] Dynamic Lane Boundary Extraction & Geometric IoU Intrusion Criterion (#2) | 실제 OpenCV/CUDA/EasyOCR 런타임 에러 트레이스백 및 해결 코드 대폭 보강 완료 |
| `KEEP_ENRICHED` | `2026-06-27-vision-anpr-3` | 2026-06-27 | 621w | 3942자 | [Vision AI] Hierarchical Object Detection: YOLOv3 Vehicle ROI, YOLOv5 Plate Detector & CSRT Tracking (#3) | 실제 OpenCV/CUDA/EasyOCR 런타임 에러 트레이스백 및 해결 코드 대폭 보강 완료 |
| `KEEP_ENRICHED` | `2026-06-28-vision-anpr-4` | 2026-06-28 | 622w | 4058자 | [Vision AI] Overcoming Blurry Blackbox Artifacts: Deep Super-Resolution (EDSR vs FSRCNN) & Multi-Frame Image Stacking (#4) | 실제 OpenCV/CUDA/EasyOCR 런타임 에러 트레이스백 및 해결 코드 대폭 보강 완료 |
| `KEEP_ENRICHED` | `2026-06-29-vision-anpr-5` | 2026-06-29 | 690w | 3504자 | [Vision AI] Korean ANPR OCR Engine, Regex Normalization & Temporal Majority Voting (v01 to v11 Evolution) (#5) | 실제 OpenCV/CUDA/EasyOCR 런타임 에러 트레이스백 및 해결 코드 대폭 보강 완료 |
| `KEEP_CORE` | `2026-10-18-static-site-security-hardening` |  | 1026w | 5112자 | npm audit fix: How to Fix npm Vulnerability & GHSA Alerts | 핵심 엔지니어링 오류 해결·구현기 유지 |
| `KEEP_CORE` | `2026-10-21-github-pages-custom-domain-cloudflare-dns` |  | 1168w | 5738자 | GitHub Pages Custom Domain & Cloudflare DNS: Migration Guide | 핵심 엔지니어링 오류 해결·구현기 유지 |
| `KEEP_DATE_FIXED` | `2026-11-05-npm-overrides-transitive-vulnerability-fix` | 2026-11-05 | 619w | 4235자 | Fix Transitive npm Vulnerabilities with overrides & --omit=dev | 미래 날짜(11/28~12/05)를 실제 과거 날짜(11/05~11/14)로 교정 (기존 slug URL 유지) |
| `KEEP_DATE_FIXED` | `2026-11-10-sdc-01-architecture-klm-model` | 2026-11-10 | 2634w | 17290자 | Air Combat Mission Replanning #1: Overcoming CPython Latency & VRAM OOM | 미래 날짜(11/28~12/05)를 실제 과거 날짜(11/05~11/14)로 교정 (기존 slug URL 유지) |
| `KEEP_DATE_FIXED` | `2026-11-12-sdc-02-stack-spike-doctrine-hypotheses` | 2026-11-12 | 2344w | 12140자 | Air Combat Mission Replanning #2: Stack Spike & Doctrine | 미래 날짜(11/28~12/05)를 실제 과거 날짜(11/05~11/14)로 교정 (기존 slug URL 유지) |
| `KEEP_DATE_FIXED` | `2026-11-14-sdc-03-deterministic-jcs-ed25519-fragmentation` | 2026-11-14 | 2012w | 12035자 | Air Combat Replanning #3: Deterministic JCS & Ed25519 Frag Fix | 미래 날짜(11/28~12/05)를 실제 과거 날짜(11/05~11/14)로 교정 (기존 slug URL 유지) |
| `NEW_STEP3` | `2026-11-16-python-urlopen-timeout-dns-hang-windows-fix` | 2026-11-16 | 1110w | 6716자 | Python urllib urlopen timeout Not Working on Windows: Fixing socket.getaddrinfo DNS Hangs | 신규 작성: Windows Python `urlopen(timeout=8)` DNS 블로킹(`_socket.getaddrinfo`) 및 UTF-16 널 바이트 해결기 |

---

## 3. `_old/` 보관(비공개 분리) 목록 (64편)

| 분류 | 폴더명 | 기존 날짜 | 영문 본문(단어) | 제목 | 분리 사유 |
| :---: | :--- | :---: | :---: | :--- | :--- |
| `ARCHIVE_DIARY` | `2026-03-26-maeumjigi-1` | 2026-03-26 | 865w | [Maeumjigi Capstone Dev Log #1] The First Steps: Claude Code AI Workflow & Capstone Architecture Planning | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-03-30-maeumjigi-2` | 2026-03-30 | 426w | [Maeumjigi Capstone Dev Log #2] Initial Alarm App Planning and Testing | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-03-31-maeumjigi-3` | 2026-03-31 | 436w | [Maeumjigi Capstone Dev Log #3] Alarm App Build Test and Fine-Tuning Preprocessing Kickoff | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-04-03-maeumjigi-5` | 2026-04-03 | 484w | [Maeumjigi Capstone Dev Log #5] Purifying 100,000 Emotion Data Points and the Pressure of Application Programming Interface (API) Costs | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-04-05-maeumjigi-6` | 2026-04-05 | 821w | [Maeumjigi Capstone Dev Log #6] Automated Report Pipeline: python-docx Visualization & Next.js 14 Frontend Kickoff | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-04-07-maeumjigi-7` | 2026-04-07 | 496w | [Maeumjigi Capstone Dev Log #7] Synthetic Data (v5) Generation Optimization and Frontend Integration | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-04-08-maeumjigi-8` | 2026-04-08 | 445w | [Maeumjigi Capstone Dev Log #8] Application Programming Interface (API) Bill Bomb Incident and Preparing Colab Fine-Tuning | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-04-09-maeumjigi-9` | 2026-04-09 | 510w | [Maeumjigi Capstone Dev Log #9] Llama 3.1 Fine-Tuning Error Struggle and Week 6 Mid-term Presentation | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-04-19-maeumjigi-11` | 2026-04-19 | 510w | [Maeumjigi Capstone Dev Log #11] Evaluating M6 Model Trained on Synthetic Data (v5) | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-03-maeumjigi-12` | 2026-05-03 | 439w | [Maeumjigi Capstone Dev Log #12] 70B Massive Model Fine-Tuning and GPU Memory (OOM) Struggle | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-04-maeumjigi-13` | 2026-05-04 | 446w | [Maeumjigi Capstone Dev Log #13] Limits of 70B Training and the Pivot to Mid-Size Models (HCX, Qwen) | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-06-maeumjigi-14` | 2026-05-06 | 386w | [Maeumjigi Capstone Dev Log #14] All Fine-Tuning Completed and Parallel Inference (Eval) Pipeline Built | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-07-maeumjigi-15` | 2026-05-07 | 406w | [Maeumjigi Capstone Dev Log #15] Visualizing Fine-Tuning Results of 5 Models & Local Environment Setup | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-08-maeumjigi-16` | 2026-05-08 | 538w | [Maeumjigi Capstone Dev Log #16] Fatal Mistake, 2nd Fine-Tuning, and React Native App Launch | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-12-maeumjigi-17` | 2026-05-12 | 412w | [Maeumjigi Capstone Dev Log #17] 2nd Fine-Tuning Complete & The Trap of the Automation Pipeline | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-13-maeumjigi-18` | 2026-05-13 | 428w | [Maeumjigi Capstone Dev Log #18] Expanding Inference Tokens and Comparing 2nd Fine-Tuning Results | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-20-maeumjigi-20` | 2026-05-20 | 457w | [Maeumjigi Capstone Dev Log #20] 3rd Fine-Tuning Complete & Backend Feature Enhancements | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-22-maeumjigi-21` | 2026-05-22 | 402w | [Maeumjigi Capstone Dev Log #21] Optimizing Data Mix Ratios and Starting the 4th Fine-Tuning | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-05-30-maeumjigi-22` | 2026-05-30 | 852w | [Maeumjigi Capstone Dev Log #22] 4th Fine-Tuning Triumph: Checkpoint-4400, Data Mix Ratios & Full System Architecture | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_YMYL` | `2026-06-18-maeumjigi-23` | 2026-06-18 | 936w | [Maeumjigi Capstone Dev Log #23] Dual-Layer Safety Wrapper, AWS EC2 GPU Budgeting & Semester 1 Defense | 자살/위기 감지 YMYL 민감 키워드 및 정규식 포함 — 애드센스 정책 리스크 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-09-16-maeumjigi-24` | 2026-09-16 | 1266w | [Maeumjigi Capstone Dev Log #24] Fall Semester Kickoff: Longitudinal Clinical Preprocessing & Informative Missingness (MNAR) Modeling | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_ADSENSE_META` | `2026-10-20-custom-domain-adsense-seo-guide` |  | 1180w | Google AdSense on GitHub Pages: Custom Domain & ads.txt Setup | 애드센스 승인/ads.txt 메타 가이드 — 사이트 주제 통일성을 위해 `_old/` 이동 |
| `ARCHIVE_ADSENSE_META` | `2026-10-21-static-site-adsense-ads-txt-guide` | 2026-10-21 | 1139w | Google AdSense on GitHub Pages: ads.txt 404 Fix & Setup Guide | 애드센스 승인/ads.txt 메타 가이드 — 사이트 주제 통일성을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-22-stanford-cs146s-1` | 2026-10-22 | 1983w | Stanford CS146S: The Modern Software Developer Complete Notes | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-23-stanford-cs146s-2` | 2026-10-23 | 2334w | Stanford CS146S: Coding LLMs & Prompt Engineering (Notes #2) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-24-stanford-cs146s-3` | 2026-10-24 | 1866w | Stanford CS146S: Model Context Protocol MCP Guide (Notes #3) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-25-stanford-cs146s-4` | 2026-10-25 | 1732w | Stanford CS146S: Spec-Driven Code Generation (Notes #4) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-26-stanford-cs146s-5` | 2026-10-26 | 1291w | Stanford CS146S: Multi-Agent Systems & Swarms (Notes #5) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-27-stanford-cs146s-6` | 2026-10-27 | 1378w | Stanford CS146S: AI Debugging & eBPF Profiling (Notes #6) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-28-stanford-cs146s-7` | 2026-10-28 | 1606w | Stanford CS146S: Automated Code Review at Scale (Notes #7) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-29-stanford-cs146s-8` | 2026-10-29 | 2049w | Stanford CS146S: AI Software Architecture (Notes #8) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-30-stanford-cs146s-9` | 2026-10-30 | 1713w | Stanford CS146S: Autonomous TDD & Formal Proofs (Notes #9) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-10-31-stanford-cs146s-10` | 2026-10-31 | 2073w | Stanford CS146S: Future of Software Engineering (Notes #10) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-01-stanford-cs329a-1` | 2026-11-01 | 2284w | [Stanford CS329A #1] Course Overview: From Large Language Models to Self-Improving AI Agents | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-02-stanford-cs329a-2` | 2026-11-02 | 2309w | [Stanford CS329A #2] Test-Time Compute Scaling: Beyond Train-Time Scaling Laws to Compute-Optimal Inference | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-03-stanford-cs329a-3` | 2026-11-03 | 2511w | [Stanford CS329A #3] Robust Verification: Process Reward Models (PRM), Ensembles, and Scalable Oversight | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-04-stanford-cs329a-4` | 2026-11-04 | 2697w | [Stanford CS329A #4] Tool Use & Code Feedback: ReAct, RLEF, and Constitutional Self-Correction | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-05-stanford-cs329a-5` | 2026-11-05 | 2835w | [Stanford CS329A #5] Multi-Step Planning & Tree Search: ADaPT, LATS, SPRINT, and Language Agent MCTS | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-06-stanford-cs329a-6` | 2026-11-06 | 2733w | [Stanford CS329A #6] Train-Time Scaling & RL: DeepSeekMath, GRPO, and Large-Scale Reasoning Optimization | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-07-stanford-cs329a-7` | 2026-11-07T10:00:00.000Z | 2135w | Stanford CS329A (Ep 7): Open-Ended Evolution: ADAS, The AI Scientist, and AlphaEvolve — When Code Becomes the Genome | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-08-stanford-cs329a-8` | 2026-11-08T10:00:00.000Z | 1865w | Stanford CS329A (Ep 8): Search & Deep Research — Program Space Search (AlphaCode), Search-o1, and Autonomous Investigation | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-09-stanford-cs329a-9` | 2026-11-09T10:00:00.000Z | 2054w | Stanford CS329A (Ep 9): Post-Training Evolution — From Next-Token Chatbots to Autonomous Agentic Fleets (SFT, RLHF, RLVR, and Agent RL) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-10-stanford-cs329a-10` | 2026-11-10T10:00:00.000Z | 2049w | Stanford CS329A (Ep 10): SWE-Agents — Autonomous Software Engineering, CodeMonkeys, KernelBench, and Agent-System Interface | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-11-stanford-cs329a-11` | 2026-11-11T10:00:00.000Z | 2406w | Stanford CS329A (Ep 11): Agent Memory — MemGPT, Cartridges, CacheBlend, and Long-Horizon Context Architecture | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-12-stanford-cs329a-12` | 2026-11-12T10:00:00.000Z | 2191w | Stanford CS329A (Ep 12): Agent Evaluation & Long Tasks — METR Time Horizons, OpenAI GDPval, and DeepScholar-Bench | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-13-stanford-cs329a-13` | 2026-11-13T10:00:00.000Z | 2351w | Stanford CS329A (Ep 13): LLM Reasoning — Denny Zhou, Chain-of-Thought (CoT), Self-Consistency, and Emergent Abilities | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-14-stanford-cs329a-14` | 2026-11-14T10:00:00.000Z | 2013w | Stanford CS329A (Ep 14): AlphaProof & Mathematical Reasoning — Formal Verification, Lean 4, AlphaGeometry, and Gemini Deep Think | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-15-stanford-cs329a-15` | 2026-11-15T10:00:00.000Z | 2045w | Stanford CS329A (Ep 15): Autonomous Systems & Reliability — The 3 Layers of Reliability, Trust Boundaries, and AI Control | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-16-stanford-cs329a-16` | 2026-11-16T10:00:00.000Z | 2080w | Stanford CS329A (Ep 16): Multimodal & Embodied Agents — Vision-Language-Action (VLA) Models, RT-2, OpenVLA, and π₀ | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_LECTURE` | `2026-11-17-stanford-cs329a-17` | 2026-11-17 | 1858w | [Stanford CS329A #17] Future Research Directions: Self-Improving AI Agents Grand Finale (Recursive Self-Improvement, Swarms, and Safe Superintelligence) | 스탠포드 공개 강의 2차 요약본 — 독창적 1차 경험 집중을 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-11-18-autonomous-budget-audit-agent-text-to-sql-graphrag` | 2026-11-18 | 2025w | Autonomous Budget Audit Agent: Text-to-SQL & GraphRAG | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-11-19-national-budget-ai-audit-findings-performance-evaluation` | 2026-11-19 | 1744w | Public Budget AI Audit: 5 Fraud Findings & System Evaluation | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-11-20-national-budget-ai-sector-partition-live-monitoring` | 2026-11-20 | 1761w | Public Budget AI #3: 3D Sector Partitioning & Live API Audit | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-11-21-national-budget-ai-corporate-registry-cartel-detection` | 2026-11-21 | 1476w | Public Budget AI #4: Breaking Cartels via DART & Registries | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-11-22-national-budget-ai-6-sector-full-suite` | 2026-11-22 | 1315w | Public Budget AI #5: 6-Sector Audit Suite & Year-End Dumps | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-11-23-national-budget-ai-inspector-portal-verification-system` | 2026-11-23 | 2246w | Public Budget AI #6: Inspector Web Portal & Full Verification | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_YMYL` | `2026-11-24-mental-crisis-nlp-suicide-risk-detection-fnr-zero` | 2026-11-24 | 2634w | [Crisis AI #1] Minimizing FNR in Crisis NLP & Bayes Distortion | 자살/위기 감지 YMYL 민감 키워드 및 정규식 포함 — 애드센스 정책 리스크 해소를 위해 `_old/` 이동 |
| `ARCHIVE_YMYL` | `2026-11-25-mental-crisis-nlp-longitudinal-fusion-extreme-value-bias` | 2026-11-25 | 2135w | [Crisis AI #2] 14-Day Longitudinal Fusion & Extreme Value Bias | 자살/위기 감지 YMYL 민감 키워드 및 정규식 포함 — 애드센스 정책 리스크 해소를 위해 `_old/` 이동 |
| `ARCHIVE_YMYL` | `2026-11-26-mental-crisis-nlp-ordinal-lightgbm-zero-probability-collapse` | 2026-11-26 | 1617w | LightGBM Ordinal Trees: Defeating -log(0)=inf Collapse | 자살/위기 감지 YMYL 민감 키워드 및 정규식 포함 — 애드센스 정책 리스크 해소를 위해 `_old/` 이동 |
| `ARCHIVE_YMYL` | `2026-11-27-mental-crisis-nlp-nested-cv-secondary-leakage-threshold-bias` | 2026-11-27 | 1594w | Nested CV: Defeating Secondary Leakage & Threshold Bias | 자살/위기 감지 YMYL 민감 키워드 및 정규식 포함 — 애드센스 정책 리스크 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-11-29-national-budget-local-subsidy-ehojo-audit` | 2026-11-29 | 2455w | Public Budget AI #7: Local Subsidy Audit Simulation | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_DIARY` | `2026-11-30-national-budget-education-grant-audit` | 2026-11-30 | 2389w | Public Budget AI #8: Education Grant Audit Simulation | 단문 캡스톤 일기/중간보고 성격 — 얇은 일기성 콘텐츠 해소를 위해 `_old/` 이동 |
| `ARCHIVE_ADSENSE_META` | `2026-12-01-google-adsense-low-value-content-cloudflare-fix` | 2026-12-01 | 1807w | Fix Google AdSense Low Value Content & Cloudflare WAF Blocks | 애드센스 승인/ads.txt 메타 가이드 — 사이트 주제 통일성을 위해 `_old/` 이동 |
| `ARCHIVE_SIMULATION` | `2026-12-02-national-budget-surveillance-automated-audit-ledger` | 2026-12-02 | 1788w | Public Budget AI #9: Budget Anomaly Audit Engine Simulation | `[Simulation]` 합성/재구성 데이터 면책조항 포함 — 실제 엔지니어링 기록만 남기기 위해 `_old/` 이동 |
