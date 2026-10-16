Here is the translated blog post in Spanish, preserving the frontmatter structure, markdown formatting, and original tags:

```markdown
---
slug: 2026-05-22-maeumjigi-21
title: "[Diario de desarrollo de Capstone Maeumjigi #21] Optimización de la proporción de mezcla de datos e inicio del 4º fine-tuning"
authors: [jbgih]
tags: [개발일지, 파인튜닝, 데이터셋, 프롬프트, 캡스톤디자인]
date: 2026-05-22
---

En esta publicación, tratamos el progreso del cuarto fine-tuning (`fine_tuning_4`) del proyecto Maeumjigi y el proceso de experimentación de optimización de la mezcla del conjunto de datos para resolver el problema de sobreajuste (overfitting) del modelo de inteligencia artificial (IA).

## 1. Problema: Sesgo hacia el dominio de la conversación emocional y sobreajuste

Durante las pruebas del tercer modelo con fine-tuning (`fine_tuning_3`), descubrimos un fenómeno fatal de sobreajuste (overfitting) en el que la calidad de las respuestas del modelo estaba excesivamente sesgada hacia el dominio de la asesoría emocional. 

Como resultado de realizar el fine-tuning únicamente con el conjunto de datos `haiku_pred` existente, se produjo un problema en el que el modelo respondía con la personalidad de un asesor excesivamente serio y pesado, incluso cuando el usuario hacía preguntas cotidianas como "¿Cómo está el clima hoy?" o "¿Qué deberíamos comer?". Este es un fenómeno en el que el modelo base pierde su capacidad original para la conversación diaria de propósito general durante el proceso de aprendizaje del dominio objetivo (asesoría), y era un desafío que debía resolverse necesariamente para lograr la intención de planificación original de "un asesor de prevención del suicidio que transmite una cálida empatía".

## 2. Implementación: Construcción de un conjunto de datos emocionales propio (v6) de 10,000 casos

### Tubería de datos a gran escala utilizando Anthropic Batch API
Para resolver el problema anterior y mejorar la calidad del aprendizaje, procedimos a construir un conjunto de datos propio a gran escala (`Emotion_train_dataset_v6.jsonl`) utilizando el modo Batch de la API de Anthropic (Claude 3 Haiku). 

- **Especificaciones de los datos (Data Specification)**: Promedio de 500 tokens por dato (unificado a un máximo de 512 tokens), aplicación de un total de 20 tipos de personalidades detalladas.
- **Tamaño objetivo (Target Size)**: 10,000 casos.

### Solución de problemas (Troubleshooting): Imposibilidad de rastrear el procesamiento asíncrono y aparición de datos faltantes
Aunque introdujimos el modo Batch de la API para lograr eficiencia de costos, hubo un problema por el cual no podíamos rastrear el progreso y el consumo de créditos en tiempo real debido a la naturaleza del procesamiento asíncrono en segundo plano. Esto provocó la pérdida de algunos datos, pero desarrollamos un script de Python adicional (`fill_v6.py`) que analiza los resultados de la respuesta asíncrona para identificar los elementos faltantes y realizar llamadas a la API complementarias, logrando construir perfectamente el conjunto de datos de alta calidad objetivo de 10,000 casos.

## 3. Experimento principal: Optimización de la proporción de mezcla de datos (Data Mixing) para fine_tuning_4

Con base en el conjunto de datos emocionales v6 recién construido, comenzamos a diseñar el experimento para el cuarto fine-tuning (`fine_tuning_4`). 

El núcleo de este fine-tuning es alejarse del ajuste de hiperparámetros existente, como el valor Alpha de LoRA, y equilibrar el rendimiento específico del dominio y el rendimiento de propósito general en función de la **proporción de mezcla del conjunto de datos de entrenamiento (Data Mixing Ratio)**. Con el fin de mezclar y entrenar datos de conversación diaria como un tipo de regularización (Regularization), construimos conjuntos de datos de entrenamiento en las siguientes tres proporciones:

- `mixed_7_3` (Emocional 7 : Cotidiano 3)
- `mixed_5_5` (Emocional 5 : Cotidiano 5)
- `mixed_2_1` (Emocional 2 : Cotidiano 1)

Actualmente, utilizando los 3 tipos de conjuntos de datos anteriores, estamos aplicando de lleno el cuarto fine-tuning al modelo `Qwen3.5-9B`. A través de la verificación de los modelos entrenados en cada proporción, planeamos derivar la proporción áurea de la mezcla de datos que armonice de manera ideal la "cotidianidad" del chatbot y la "experiencia" del asesor.
```