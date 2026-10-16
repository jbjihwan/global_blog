Here is the translated technical blog post in Spanish:

```markdown
---
slug: 2026-05-30-maeumjigi-22
title: "[Registro de Desarrollo de Capstone Maeumjigi #22] ¡Finalización del 4º Fine-Tuning! Diseño de la Arquitectura del Chatbot y Reporte Final"
authors: [jbgih]
tags: [Registro de Desarrollo, Fine-Tuning, Arquitectura, Diseño Capstone, Reporte Final]
date: 2026-05-30
---

## 1. Descripción General (Overview)
Esta publicación es un registro de desarrollo (Dev Log) sobre el análisis de resultados del cuarto fine-tuning (`fine_tuning_4`) y el diseño de la arquitectura del sistema del proyecto de chatbot 'Maeumjigi', realizado del 27 al 30 de mayo. Aborda la estrategia de mezcla de datos (Data Mixing) para resolver el problema de sesgo de dominio del modelo, la visualización de las métricas de evaluación del modelo final y el diseño de la arquitectura considerando la integración de un grafo de conocimiento (Knowledge Graph).

## 2. Tecnologías Utilizadas (Tech Stack)
- **Model**: Qwen35-9B
- **Fine-Tuning**: LoRA (Low-Rank Adaptation)
- **Data Analysis & Visualization**: `matplotlib`
- **Architecture**: HTML-based Architecture Diagram, Knowledge Graph
- **Automation**: Pipeline de generación automática de documentos utilizando Inteligencia Artificial (IA)

## 3. Solución de Problemas (Troubleshooting & Solution)

### 3.1. Solución al Problema de Sobreajuste (Overfitting) en un Dominio Específico
- **Problem**: En el proceso de fine-tuning anterior, el modelo se sobreajustó al dominio de 'Consejería Emocional (Daily)', provocando un fenómeno en el que respondía con un tono excesivamente serio incluso cuando el usuario intentaba una conversación cotidiana (Common) (Olvido Catastrófico y Cambio de Dominio).
- **Solution**: 
  - Para solucionar esto, se realizó un reentrenamiento mezclando datos de conversación cotidiana (Common) y emocional (Daily) en una proporción de 7:3 (`Qwen35-9B_mixed_7_3`).
  - Como resultado del experimento, el modelo pudo asegurar la capacidad de cambio de personalidad (Persona Switching), clasificando claramente la intención (Intent) del usuario para distinguir y responder adecuadamente entre una conversación cotidiana y una consejería de crisis seria.

### 3.2. Obtención de Pesos Óptimos y Evaluación de Rendimiento
- **Solution**: A través del monitoreo continuo del estado de entrenamiento, se obtuvieron los pesos óptimos del adaptador (`adapter_config.json`) en el `checkpoint-4400`. 
- **Evaluation**: Se visualizaron cuantitativamente todas las métricas de evaluación utilizando `matplotlib`. Se verificó la estabilidad del entrenamiento a través de `01_loss_curves.png` y `04_pareto_efficiency.png`, y en particular, se demostró el equilibrio de pérdida (Loss) entre los dos dominios de datos mediante el análisis del gráfico `06_common_vs_daily.png`.

![Visualización de métricas de evaluación](D:/서울과기대 컴퓨터공학과/26-1/WS/보고서 작성 양식_0001.png)

## 4. Implementación de Funciones Clave (Features)

### 4.1. Arquitectura del Sistema del Chatbot y Diseño del Grafo de Conocimiento (KG)
Para vincular el modelo `checkpoint-4400`, cuyo rendimiento ha sido verificado, con el entorno de servicio de la aplicación real, se diseñó la arquitectura general del sistema a través de `chatbot_architecture.html`. 
Más allá de la simple generación de texto, para controlar el fenómeno de alucinación (Hallucination) y mejorar la precisión de las respuestas basadas en el contexto, se incluyó en la estructura del sistema un plan de integración de grafos de conocimiento (Knowledge Graph).

![Diseño de la arquitectura del sistema](D:/서울과기대 컴퓨터공학과/26-1/WS/보고서 작성 양식_0001.png)

### 4.2. Prueba A/B (Base vs Fine-tuned) y Automatización del Reporte Final
Para concluir la primera fase del cuarto proyecto de fine-tuning, se implementó un script que genera automáticamente el documento `fine_tuning_4_보고서.docx` con la ayuda de la IA. 
Dentro del reporte, se diseñó para incluir automáticamente los resultados de la comparación de texto de respuestas reales (Prueba A/B) entre el modelo base original y nuestro modelo ajustado (fine-tuned), demostrando objetivamente la mejora cualitativa del rendimiento.
```