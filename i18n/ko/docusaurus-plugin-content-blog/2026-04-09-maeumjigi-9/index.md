Aquí tienes la traducción al español, manteniendo intactos el formato markdown, la estructura del *frontmatter* y las rutas de las imágenes, tal como solicitaste:

```markdown
---
slug: 2026-04-09-maeumjigi-9
title: "[Diario de Desarrollo del Capstone Maeumjigi #9] Lucha contra Errores en el Fine-Tuning de Llama 3.1 y Presentación Intermedia de la Semana 6"
authors: [jbgih]
tags: [Diario de desarrollo, Llama3.1, Fine-tuning, Troubleshooting, Generación de PPT, ERD]
date: 2026-04-09
---

## 1. Overview
El 9 de abril, llevamos a cabo el primer fine-tuning del modelo de inteligencia artificial (IA) Llama 3.1 en el entorno de Colab (`llama31_finetuning_colab.ipynb`) configurado el día anterior. Depuramos y resolvimos un error de análisis de tokens (token parsing error) y un problema de desbordamiento de memoria (OOM) que ocurrieron durante el entrenamiento. Paralelamente, completamos la organización del progreso del frontend y el diseño del diagrama de relación de entidades (ERD) de la base de datos para la presentación intermedia de la sexta semana del proyecto Capstone.

## 2. Tech Stack
- **Model**: Llama 3.1
- **Environment**: Google Colab
- **Task**: LLM Fine-Tuning
- **Documentation**: AI-assisted Presentation & DB Architecture Diagram

## 3. Troubleshooting: Fine-Tuning de Llama 3.1

### Issue 1: Fuga de `eos_token` y error de procesamiento
- **Síntoma (Symptom)**: Inmediatamente después de ejecutar el script de fine-tuning, el token de finalización `eos_token` no se escapaba en los resultados de generación de texto y aparecía como texto sin formato (Raw text), o provocaba un error de procesamiento.
- **Causa (Cause)**: Ocurrió debido a un error de configuración del tokenizador (Tokenizer) o a que el mapeo de las señales de padding y finalización de oración no se realizó correctamente durante el proceso de preprocesamiento del conjunto de datos.
- **Solución (Solution)**: Analizamos los registros de errores (error logs) para corregir la lógica de procesamiento de tokens especiales (Special tokens) del tokenizador. Revisamos la estructura de formato del conjunto de datos para garantizar que el modelo reconociera correctamente el rol semántico del `eos_token`.

### Issue 2: Desbordamiento de memoria (CUDA OOM)
- **Síntoma (Symptom)**: Se produjo un error de ejecución (Runtime Error) tras entrar en el bucle de entrenamiento del modelo debido a que se superó la cuota asignada de VRAM de la GPU.
- **Solución (Solution)**: Rastreamos el punto de fuga de memoria (memory leak) basándonos en el seguimiento de la pila (stack trace) generado. Ajustamos el parámetro del tamaño de lote (batch size) y resolvimos el cuello de botella mediante la elaboración de perfiles de memoria (memory profiling) del proceso de entrenamiento. Tras varias sesiones de ajuste de parámetros, establecimos un entorno de entrenamiento estable.

### Resultado (Result)
Completamos con éxito el fine-tuning del modelo y calculamos las métricas de resultados según la distribución del conjunto de datos de entrenamiento.

![학습데이터별학습결과](D:/Projects/26_1/CapDe/TestClaudeCode/data_preprocessing/for_Llama/data/output/학습데이터별학습결과.png)

## 4. Características (Features): Automatización de Material de Presentación y Diseño de ERD

### Creación del material para la presentación intermedia de la sexta semana (Frontend y BD)
- **Generación de diapositivas del Frontend (Frontend Slide Generation)**: Proporcionamos capturas de pantalla de la interfaz de usuario del frontend creadas previamente (`캡디_6주차_Frontend.pptx`) como contexto para generar automáticamente la estructura de las diapositivas de la presentación y un borrador del guión (Script).
- **Refactorización del ERD de la base de datos (Database ERD Refactoring)**: Aplicamos el ajuste de prompts (prompt tuning) durante el proceso de generación del diagrama de relaciones de las tablas basado en el esquema del backend, con el fin de resolver la complejidad del resultado inicial.
    - **Optimización (Optimization)**: Añadimos la restricción: "Coloca la tabla User en el centro y estructura el diagrama para que las relaciones de referencia entre las tablas se visualicen claramente".
    - **Resultado (Result)**: Obtuvimos un ERD con una legibilidad significativamente mejorada mediante una distribución radial centralizada (User-centric) y lo integramos en los materiales de la presentación intermedia.

![테스트 결과](D:/서울과기대%20컴퓨터공학과/26-1/CapDe/팀플/Week6/테스트%20결과.png)

## 5. Próximos pasos (Next Steps)
Validamos con éxito el primer ciclo de fine-tuning del modelo Llama 3.1 y establecimos un pipeline automatizado para la creación de documentación utilizando los recursos de desarrollo (entregables, estructura de la base de datos). La próxima semana, realizaremos pruebas de inferencia (Inference) del modelo ajustado y analizaremos los resultados de la evaluación de rendimiento.
```