```markdown
---
slug: 2026-04-03-maeumjigi-5
title: "[Diario de Desarrollo Capstone Maeumjigi #5] Refinamiento de 100 mil datos de emociones y la presión de los costos de la Interfaz de Programación de Aplicaciones (API)"
authors: [jbgih]
tags: [개발일지, 데이터정제, ClaudeAPI, 감정분류, Llama3.1, 비용문제]
date: 2026-04-03
---

El 3 de abril, llevamos a cabo la construcción de un flujo (pipeline) de preprocesamiento y refinamiento del conjunto de datos de entrenamiento para el fine-tuning (ajuste fino) del modelo de Aprendizaje Profundo (Deep Learning) (Llama 3.1), el cual será el motor central del proyecto Maeumjigi. En esta publicación, abordamos el proceso de automatización del etiquetado de emociones de un conjunto de datos de conversaciones a gran escala, así como el problema de los costos de las llamadas a la Interfaz de Programación de Aplicaciones (API) de grandes modelos de lenguaje (LLM) que surgió durante este proceso, y sus soluciones.

## 🛠 Tech Stack
- **Model**: Llama 3.1 (Fine-tuning Target)
- **Data Pipeline**: Python, Pandas
- **AI/LLM**: Anthropic Claude API (Data Annotation)

## 🚀 Features: Flujo de reclasificación de emociones de datos (v3 -> v4)

El conjunto de datos existente `Emotion_train_dataset_v3`, compuesto por 1 millón de registros, estaba etiquetado con clasificaciones emocionales generales, por lo que su nivel de detalle era insuficiente para ser utilizado tal cual con el propósito específico del dominio de 'consejería psicológica'. Por lo tanto, el objetivo fue redefinir las categorías emocionales adecuadas para un chatbot de consejería y, basándonos en esto, construir un **conjunto de datos v4** filtrando y remapeando únicamente los datos significativos.

Para ello, en lugar de usar un simple emparejamiento de palabras clave, diseñamos un flujo de trabajo automatizado (`v4_plan.md`) utilizando la API de Claude para permitir que la Inteligencia Artificial (IA) comprendiera el contexto del texto y pudiera juzgar las emociones por sí misma.

- **Ingeniería de Prompts (Prompt Engineering)**: Asignamos la persona (rol) de 'experto en consejería psicológica' al modelo Claude, instruyéndole analizar el contexto (Context) de toda la conversación y extraer únicamente los datos que pertenecieran a una tabla de clasificación de emociones previamente definida.
- **Procesamiento por Lotes (Batch Processing)**: Antes de procesar todos los datos, en una primera etapa implementamos y ejecutamos un script que tomó una muestra de 100,000 datos para verificar la precisión y el rendimiento del flujo de trabajo.

## 🔧 Troubleshooting

### 1. Problema de precisión del etiquetado de emociones específico del dominio
- **Problem**: Los datos existentes estaban clasificados solo con emociones unidimensionales, lo que limitaba la capacidad de reflejar el estado psicológico complejo del cliente. El enfoque anterior basado en reglas (Rule-based) o los métodos simples de filtrado de palabras no podían captar las emociones ocultas en el contexto.
- **Solution**: Adoptamos un enfoque utilizando el LLM como Data Annotator. En lugar de expresiones regulares, pasamos el script de conversación completo como un prompt a través de la API de Claude para que realizara una inferencia basada en el contexto, aumentando drásticamente la calidad del etiquetado. Filtramos solo los datos claros y excluimos los datos ambiguos que no entraban en la clasificación de emociones para eliminar el ruido.

### 2. Problema de facturación por uso de la API del LLM y explosión de Tokens (Token)
- **Problem**: En el proceso de enviar 100,000 datos de conversación a la API, el uso de Tokens aumentó exponencialmente. Originalmente, esperábamos que el uso de la API estuviera cubierto por la suscripción Claude Pro ($20 al mes) o que podríamos evitar el cargo utilizando Claude Code en lugar de la API de Anthropic. Sin embargo, la API de Anthropic llamada desde el script de automatización de Python facturó de forma completamente independiente como pago por uso (pay-as-you-go) basado en tokens. Como resultado, ocurrió el problema de que solo la ejecución de la lógica de prueba para 100,000 casos facturó rápidamente $10.27 (aproximadamente 14,000 KRW).
- **Solution**:
  1. En lugar de investigar exhaustivamente los 1 millón de casos, cambiamos la estructura del flujo de trabajo para seleccionar y procesar solo los datos mínimos válidos esenciales para el fine-tuning (ajuste fino) mediante el muestreo de datos.
  2. Establecimos una estrategia para minimizar la longitud del Token de entrada (Input Token) optimizando la estructura del prompt, reduciendo así los costos de llamadas a la API de los datos a procesar en el futuro junto con la optimización del modelo.

## 📝 Conclusión

A través del trabajo de hoy, logramos asegurar un conjunto de datos refinado de alta calidad (`v4_report.md`), pero sentimos profundamente la barrera realista de 'recursos informáticos y costos de la API' que es inevitable en el proceso de preprocesamiento de datos de Aprendizaje Profundo. Planeamos continuar mejorando el fine-tuning (ajuste fino) de Llama 3.1 manteniendo un equilibrio eficiente entre la calidad del modelo y el costo de procesamiento de datos.
```