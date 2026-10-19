---
title: About Me & Global Dev Blog
description: About Jihwan Park and the Global Dev Blog - Engineering Deep Dives in AI, Robotics, Computer Vision, and Reinforcement Learning.
keywords: [About Me, Jihwan Park, AI Engineer, Robotics, Computer Vision, Reinforcement Learning, Maeumjigi]
---

# About Me & Global Dev Blog

Welcome to **Global Dev Blog**, an engineering lab notebook and technical publication authored by **Jihwan Park (jbjihwan)**.

This blog documents hands-on engineering journeys, real-world deployment challenges, architecture trade-offs, and empirical benchmarks in **Artificial Intelligence, Robotics, Deep Computer Vision, and Reinforcement Learning**.

---

## 👨‍💻 Who I Am

I am an AI and Robotics Software Engineer passionate about transforming theoretical algorithms into robust, real-time edge and server systems. My work spans:

- **Autonomous Systems & Reinforcement Learning**: Formulating Markov Decision Processes (MDP), continuous-to-discrete state-action mappings, dense reward shaping, and Sim-to-Real hardware transfer.
- **Deep Computer Vision**: Real-time multi-stage inference pipelines, object detection (YOLOv3/v5/v8), multi-object tracking (CSRT, DeepSORT), deep super-resolution (EDSR, FSRCNN), and optical character recognition (OCR) with temporal filtering.
- **Natural Language Processing & Safety AI**: Parameter-Efficient Fine-Tuning (PEFT/LoRA) on Llama architectures, ordinal regression under extreme class imbalance, weak-label calibration, and deterministic guardrail wrappers.
- **Full-Stack ML Engineering**: High-throughput FastAPI microservices, containerization, Docusaurus multi-lingual documentation, and cross-platform mobile interfaces (React Native).

---

## 📚 Core Series on This Blog

### 1. 🧠 Maeumjigi Capstone Dev Log (23 Episodes)
A comprehensive chronicle of developing an AI-driven crisis detection and suicide prevention system:
- Synthetic clinical dialogue generation using large-scale LLM pipelines.
- Overcoming severe weak-labeling overconfidence (p=0.9998) through ordinal regression and cumulative thresholding (P >= Severe).
- Designing deterministic Safety Wrapper guardrails to guarantee sub-millisecond crisis intervention.
- Database schema migration, connection pooling troubleshooting, and live production presentation.

### 2. 🤖 Webots Q-Learning Autonomous Mobile Robot (5 Episodes)
From zero-knowledge exploration to deterministic obstacle avoidance:
- Discretizing 6-sector continuous distance sensors into 648 compact states.
- Counteracting sparse reward starvation with geometric velocity and distance-delta reward shaping.
- Escaping 12-obstacle local minima traps through calibrated exploration decay ($\epsilon$-decay).
- Deploying the learned Q-table onto physical dual-motor differential drive robots via Arduino Uno.

### 3. 🚗 Blackbox ANPR & Lane Intrusion Vision AI (5 Episodes)
Real-time embedded vision system tackling high-speed highway dashcam footage:
- 6-Stage end-to-end pipeline with strict 30 FPS latency constraints.
- Dynamic lane polynomial fitting and geometric IoU intrusion criteria.
- Hierarchical vehicle-to-plate localization using YOLOv3, YOLOv5, and CSRT optical tracking.
- Restoring blurry, motion-degraded plate patches using Deep Super-Resolution (EDSR) and multi-frame stacking.
- Korean license plate OCR engine with regex syntax normalization and 11-step temporal majority voting.

---

## 🛠️ Lab & Tech Stack

- **Deep Learning Frameworks**: PyTorch, Hugging Face Transformers, Torchvision, ONNX Runtime.
- **Computer Vision**: OpenCV, Albumentations, EasyOCR, Tesseract, EDSR / FSRCNN.
- **Robotics & Simulation**: Webots Robot Simulator, Arduino IDE, ROS / ROS2 fundamentals.
- **Languages & Backend**: Python 3.12, TypeScript, C++, FastAPI, PostgreSQL, Redis, Node.js.
- **Hardware Rig**: NVIDIA GeForce RTX 4060 Laptop GPU (8GB VRAM), Dual-Core ESP32 / Arduino Microcontrollers, Edge Cameras.

---

## 🌐 Open Source & Community

All technical series published on this blog are backed by real, executable repositories and codebases. I believe that documenting failures, dead ends, and troubleshooting steps is far more valuable to fellow engineers than presenting polished final products without context.

- **GitHub Profile**: [github.com/jbjihwan](https://github.com/jbjihwan)
- **Blog Source Repository**: [github.com/jbjihwan/global_blog](https://github.com/jbjihwan/global_blog)
- **Get in Touch**: Visit the [Contact Page](/contact) or reach out via [jbgihwan@gmail.com](mailto:jbgihwan@gmail.com).
