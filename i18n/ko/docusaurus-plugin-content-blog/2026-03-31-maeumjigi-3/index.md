Here is the Spanish translation of the technical blog post with the markdown formatting and frontmatter structure preserved:

```markdown
---
slug: maeumjigi-3
title: "[Registro de Desarrollo Capstone Maeumjigi #3] Pruebas de compilación de la aplicación de alarma e inicio del preprocesamiento para fine-tuning"
authors: [jbgih]
tags: [diario de desarrollo, codificación con IA, ClaudeCode, proyecto capstone, Android, prueba de compilación, Llama3.1]
date: 2026-03-31
---

El 31 de marzo, procedimos con la compilación y las pruebas unitarias del cliente Android de la "Aplicación de alarma de reservas de la Convención de Defensa", que era el objetivo inicial del proyecto Maeumjigi. Al mismo tiempo, iniciamos a gran escala el funcionamiento del pipeline de preprocesamiento de datos para el fine-tuning (ajuste fino) del modelo de inteligencia artificial (IA) Llama 3.1, que será el núcleo del proyecto. En esta publicación, resumimos el proceso de automatización del preprocesamiento de datos para el ajuste del modelo de lenguaje grande (LLM) y la verificación del entorno de compilación de la aplicación Android.

## 1. Verificación de la compilación y pruebas unitarias del cliente Android

Verificamos si el código del servidor y del cliente Android, creados mediante generación de código, pasan el pipeline de compilación en un entorno real de Android Studio y si la lógica del dominio funciona correctamente.

### Tech Stack
- Android SDK, Gradle, JUnit

### Features
- Detección de cambios en el estado de reserva basado en servicios en segundo plano.
- Activador de notificaciones push utilizando la API de notificaciones de Android.

### Troubleshooting & Solution
- **Issue**: Era necesario comprobar si el código del cliente Android y la lógica de alarma en segundo plano, diseñados y generados en la etapa anterior, se compilaban satisfaciendo el árbol de dependencias real de Android, y si la fusión del manifiesto (Manifest Merger) específica de Android y el procesamiento de recursos se ejecutaban correctamente.
- **Solution**: 
  Para verificar la compilación, ejecutamos el proceso de compilación de Gradle apuntando a la ruta `mnd-reservation-alarm/android/app/build/`. Durante este proceso, revisamos la fusión de recursos de depuración generados y los resultados del procesamiento del manifiesto. Además, ejecutamos pruebas unitarias, incluyendo `NotificationBuilderTest` para la lógica principal de notificaciones push, garantizando la estabilidad del ciclo de vida central que detecta cambios en las reservas en segundo plano y genera alertas.

## 2. Construcción del pipeline de preprocesamiento de datos para el fine-tuning de Llama 3.1

Para ir más allá de una simple aplicación de notificaciones, comenzamos los preparativos para el fine-tuning de Llama 3.1 con el fin de integrar un modelo avanzado capaz de comprender y reaccionar de manera integral al contexto de la reserva y al estado emocional del usuario (soldado).

### Tech Stack
- Llama 3.1, Claude Code

### Features
- Automatización del funcionamiento del pipeline para limpiar conjuntos de datos de conversación a gran escala y convertirlos al formato de entrenamiento de Llama 3.1 (Instruction).

### Troubleshooting & Solution
- **Issue**: Tuvimos que limpiar decenas de miles de datos de conversación que se utilizarían para el fine-tuning, convirtiéndolos en un formato que el modelo pudiera aprender. Este proceso incluía pasos complejos como limpieza de datos, eliminación de ruido y mapeo de plantillas. Existía la preocupación de que se produjeran graves cuellos de botella en el trabajo si intervenía el control manual o la aprobación de prompts paso a paso.
- **Solution**:
  Dimos instrucciones para el trabajo basándonos en un documento de especificaciones de preprocesamiento diseñado previamente (`llama31_finetuning_data_preprocessing_plan_short.md`). En particular, para maximizar la velocidad y la tasa de automatización del pipeline de procesamiento de datos, otorgamos al agente autoridad de ejecución total: **"No se requieren permisos adicionales para ninguna elección relacionada con este trabajo"**. A través de esto, eliminamos los retrasos causados por la intervención del usuario y logramos establecer con éxito el funcionamiento del pipeline de datos, realizando el preprocesamiento de conjuntos de datos masivos sin interrupciones.

## Next Step
Dado que hemos confirmado la estructura básica de la aplicación Android y la estabilidad del pipeline de compilación, en el próximo paso verificaremos formalmente los resultados del preprocesamiento de los datos masivos de conversación que se inyectarán en el modelo Llama 3.1, e ingresaremos a la fase de entrenamiento (Training) del modelo en toda regla.
```