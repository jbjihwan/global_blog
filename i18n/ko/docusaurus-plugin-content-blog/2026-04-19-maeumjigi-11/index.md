Here is the translated blog post in Spanish. The Markdown formatting, frontmatter structure, and image paths have been preserved as requested, while the content and title have been translated into Spanish.

```markdown
---
slug: 2026-04-19-maeumjigi-11
title: "[Registro de Desarrollo Capstone de Maeumjigi #11] Evaluación del Modelo M6 con Resultados de Entrenamiento de Datos Sintéticos (v5)"
authors: [jbgih]
tags: [개발일지, 합성데이터, 모델평가, M6, FAISS, 주간보고서]
date: 2026-04-19
---

## 1. Resumen (Overview)

Esta publicación es el registro de desarrollo de la séptima semana del proyecto del chatbot de asesoramiento psicológico 'Maeumjigi'. El objetivo principal de esta semana es evaluar cuantitativa y cualitativamente el rendimiento del **Modelo M6**, el cual fue ajustado (Fine-tuned) con el conjunto de datos sintéticos (v5) recientemente construido, y verificar los resultados de la integración con la **base de datos vectorial FAISS (DB)** para la mejora del pipeline de Generación Aumentada por Recuperación (RAG, por sus siglas en inglés) basado en Inteligencia Artificial (IA).

## 2. Evaluación del Rendimiento del Modelo: M0 vs M5 vs M6 (Model Evaluation)

Para verificar el impacto que tiene la calidad de los datos de entrenamiento en la capacidad de generación del modelo durante el ajuste fino del modelo de lenguaje, realizamos un experimento comparativo dirigido a tres versiones del modelo.

- **M0 (Base Model):** Modelo Llama 3.1 original preentrenado.
- **M5 (Data v4):** Modelo de ajuste fino basado en el conjunto de datos existente (v4) que pasó por el primer proceso de refinamiento.
- **M6 (Data v5):** Modelo de ajuste fino basado en un conjunto de datos sintéticos virtuales de alta calidad (v5) generado con una inversión de aproximadamente $10 en costos de API.

### 2.1 Análisis de la Pérdida de Entrenamiento (Training Loss)

![Training Result M3-M6](D:/Projects/26_1/CapDe/TestClaudeCode/data_preprocessing/for_Llama/data/output/M6/training_result(M3~M6).png)

Esta es la métrica de pérdida de entrenamiento (Training Loss) registrada durante el proceso de aprendizaje del modelo. A través de los experimentos desde M3 hasta M6, confirmamos la sección donde el aprendizaje converge de manera estable y, en particular en el caso del modelo M6, alcanzó el valor de pérdida (Loss) objetivo de forma estable sin sobreajuste (Overfitting).

### 2.2 Comparación de Textos Generados (Troubleshooting & Solution)

**Problema Ocurrido (Troubleshooting):**
Necesitábamos demostrar la mejora del rendimiento del modelo con datos comparativos objetivos e intuitivos, y no simplemente con la sensación cualitativa de que "las respuestas se han vuelto más naturales". En el informe semanal se requirió específicamente material de ejemplo que mostrara claramente la diferencia en la capacidad de empatía en coreano entre el modelo M0 (modelo base) y los modelos ajustados.

**Solución (Solution):**
Inyectamos el mismo prompt en cada modelo (M0, M5, M6) para extraer los textos de respuesta generados, y construimos un pipeline de análisis comparativo coherente al parsear esto en formato `m0_m6_compare.json`.

![Test Result M0, M5, M6](D:/Projects/26_1/CapDe/TestClaudeCode/data_preprocessing/for_Llama/data/output/M6/test_result(M0,M5,M6).png)

**Resultado de la Evaluación:**
- **M0 (Base):** Se confirmó que no es adecuado para el dominio del asesoramiento psicológico, ya que no logró comprender el contexto ni las líneas emocionales propias del idioma coreano, generando respuestas con un tono de traducción mecánica.
- **M5 (Data v4):** Aunque mantiene el flujo de conversación básico, mostró ciertas limitaciones en cuanto a la intervención psicológica (Intervention) para empatizar profundamente con las emociones subyacentes del cliente.
- **M6 (Data v5):** No solo empatizó profundamente con las emociones del usuario, sino que también emuló con éxito el tono cálido y profesional propio de un consejero psicológico experto real. Este es un resultado que demuestra que la construcción de un conjunto de datos sintéticos (v5) de alta calidad es un factor determinante en el rendimiento del modelo especializado en el dominio.

## 3. Arquitectura RAG y Construcción de FAISS DB (Features)

**Características Clave Implementadas (Features):**
Introdujimos la arquitectura RAG para controlar el problema de las alucinaciones (Hallucination) del LLM, que es difícil de resolver con un simple ajuste fino, y para generar respuestas basadas en conocimientos psicológicos verificados.

**Tecnología Utilizada (Tech Stack):**
- Vector DB: **FAISS (Facebook AI Similarity Search)**
- Embedding: Modelo de incrustación (embedding) especializado en textos en coreano

**Resultados de Implementación y Evaluación:**
1. Completamos la indexación (Indexing) en la FAISS DB después de dividir los documentos de la base de conocimientos profesionales de asesoramiento psicológico en fragmentos (Chunks) e incrustarlos (embedding) como vectores.
2. Realizamos una prueba para recuperar (Retrieve) el documento con alta similitud a la consulta (Query) de entrada del usuario e inyectarlo en la ventana de contexto.
3. Como resultado de la ejecución del script de evaluación (`FAISS_DB_구축_평가.md`), verificamos que la arquitectura de la base de datos vectorial construida aumentó significativamente la confiabilidad de la respuesta al realizar una búsqueda de similitud rápida y precisa.

## 4. Automatización del Pipeline de Reportes (Reporting)

Avanzamos con la automatización de la generación de documentos para minimizar los recursos necesarios en la redacción del informe semanal.
- Con base en los datos de prueba comparativos extraídos (`m0_m6_compare.json`), generamos automáticamente `7주차_보고서_v1_간결.md` (versión resumida) y `7주차_보고서_v2_상세.md` (versión detallada) mediante un script.
- Aseguramos rápidamente el documento final para la entrega al construir un proceso de conversión que compila el formato Markdown a archivos DOCX (Word).

## 5. Conclusión y Tareas Futuras

A través de esta evaluación del modelo M6, demostramos que el ajuste fino (fine-tuning) basado en datos sintéticos de alta calidad (v5) aporta una mejora drástica en el rendimiento del chatbot de asesoramiento psicológico. Además, el desarrollo del motor central del chatbot 'Maeumjigi' se ha encaminado correctamente tras completar con éxito la verificación de la arquitectura RAG basada en FAISS DB. En la siguiente etapa, planeamos continuar con la integración real de la API de backend y las pruebas de integración del sistema (Integration Test) basándonos en esto.
```