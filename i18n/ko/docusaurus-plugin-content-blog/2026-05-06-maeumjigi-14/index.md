Aquí tienes la traducción de la publicación del blog técnico al español, conservando el formato Markdown, la estructura del *frontmatter* y traduciendo el título según lo solicitado:

```markdown
---
slug: 2026-05-06-maeumjigi-14
title: "[Diario de Desarrollo Capstone Maeumjigi #14] Finalización de todo el fine-tuning y configuración del entorno de inferencia paralela (Eval)"
authors: [jbgih]
tags: [diario-de-desarrollo, fine-tuning, HCX-Omni-8B, Qwen35-9B, evaluacion-de-modelos, inferencia, procesamiento-paralelo]
date: 2026-05-06
---

## 1. Resumen (Overview)

Esta publicación es un documento que registra el estado en el momento de completar el fine-tuning del modelo de lenguaje del proyecto Maeumjigi y el proceso de construcción de un pipeline de inferencia paralela para evaluar el rendimiento de los modelos entrenados.

Los modelos principales son **HCX-Omni-8B** y **Qwen35-9B**, y el enfoque estuvo en optimizar el tiempo de inferencia en un entorno de múltiples GPU y resolver los problemas de administración de fugas de memoria.

## 2. Resultados del fine-tuning y análisis de registros (logs)

Como resultado del ajuste de hiperparámetros y el entrenamiento distribuido a largo plazo, el valor de pérdida (Loss) disminuyó de manera estable y el entrenamiento concluyó con éxito.

```text
step= 1200  loss=0.9698  lr=1.88e-04  gpu=7.7GB
step= 1250  loss=0.8523  lr=1.86e-04  gpu=7.7GB
...
step= 1650  loss=0.8783  lr=1.73e-04  gpu=7.7GB
```

### [Troubleshooting] Omisión en el monitoreo de métricas de pérdida de entrenamiento/validación
* **Problema (Issue)**: No estaba claro si la métrica `loss` que se mostraba en los registros de entrenamiento era Train Loss o Validation Loss. Como resultado de rastrear el código utilizando un asistente de Inteligencia Artificial (IA), se descubrió tardíamente que se omitió el pipeline de registro para `eval loss` en el script de entrenamiento existente.
* **Solución (Solution)**: Dado que ya se había completado todo el fine-tuning (Epoch) del modelo, se determinó que volver a entrenar (Retraining) para comprobar la pérdida de validación en pasos intermedios sería un desperdicio de recursos. Por lo tanto, se decidió cargar el último punto de control (Checkpoint) entrenado y sustituirlo por una evaluación cualitativa/cuantitativa mediante pruebas de generación de texto basadas en prompts reales (Generation Eval).

## 3. Construcción del pipeline de Inferencia Paralela (Parallel Inference)

La evaluación inicial del modelo se llevó a cabo en un entorno Jupyter (`20_eval_ft_models.ipynb`). Para prevenir errores de falta de memoria (OOM) durante la inferencia, se configuró `max_new_tokens` en 1024, proporcionando margen suficiente, y se probó la generación de texto de forma secuencial.

### [Troubleshooting] Cuello de botella en la inferencia debido a la asignación de una sola GPU
* **Problema (Issue)**: A pesar de haber entrenado en un entorno Multi-GPU, solo se utilizó un recurso de GPU durante la inferencia, lo que provocó un cuello de botella y un retraso grave en el tiempo necesario para la evaluación.
* **Solución (Solution)**: Para utilizar el 100% de los recursos de GPU del servidor, se construyó un entorno de inferencia paralela redactando un nuevo script de shell (`run_eval_parallel.sh`) que distribuye el procesamiento de inferencia a través de múltiples dispositivos.

### [Features] Pipeline automatizado para los resultados de inferencia y evaluación
Junto con la introducción del script de inferencia paralela, se completó un pipeline para convertir los resultados de la evaluación en datos.
1. **Inferencia Acelerada (Inference Acceleration)**: Al distribuir y asignar los pesos del modelo y los lotes de prompts a múltiples dispositivos GPU, se redujo drásticamente el tiempo total de inferencia.
2. **Agregación de la Evaluación (Evaluation Aggregation)**: Se implementó una lógica que calcula la respuesta generada (Generated Text) y las métricas de perplejidad (Perplexity) para cada modelo, y las recopila automáticamente en formato de informe de Excel.

## 4. Evaluación de modelos a gran escala y prevención de fugas de memoria

Esta evaluación de inferencia incluyó la inferencia de modelos con parámetros a gran escala, como DSR1-70B, además de los modelos con fine-tuning.

### [Troubleshooting] Error OOM debido a VRAM no devuelta (Memory Leak)
* **Problema (Issue)**: Después de que finalizó el ciclo de inferencia del modelo DSR1-70B, la caché de PyTorch no se liberó correctamente, provocando un fenómeno en el que la VRAM no fue devuelta. Debido a esto, se produjo un error de Falta de Memoria (OOM) en el momento de cargar los modelos posteriores en la GPU, lo que detuvo el pipeline.
* **Solución (Solution)**: Utilizando el script de procesamiento paralelo previamente construido, se mejoró la estructura para que el proceso de inferencia de cada modelo se ejecute en un entorno de Proceso Aislado (Isolated Process). Al ejecutar la inferencia en unidades de subprocesos separados, cuando el proceso finaliza, la memoria de la GPU asignada se recupera de forma forzada a nivel de sistema operativo (OS), lo que permitió bloquear de raíz el problema de fuga de VRAM.

## 5. Próximos pasos (Next Step)

Con la finalización de la construcción de la infraestructura para la inferencia paralela y la agregación automática de evaluaciones, planeamos realizar un análisis comparativo en profundidad de la calidad real de las respuestas y el rendimiento de cada modelo con fine-tuning, como HCX-Omni-8B y Qwen35-9B, basándonos en los informes de Excel generados automáticamente.
```