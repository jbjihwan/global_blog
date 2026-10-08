---
slug: maeumjigi-3
title: "[Registro de Desarrollo Maeumjigi #3] Prueba de Compilación de la App y Preprocesamiento de Fine-Tuning"
authors: [jbgih]
tags: [devlog, IA-coding, ClaudeCode, capstone, Android, build-test, Llama3.1]
date: 2026-03-31
---

![Imagen de Portada](./images/01_cover.png)

Este es el registro del 31 de marzo, cuando realizamos la prueba de compilación de Android de la aplicación de alarma de reservas, que fue la dirección inicial del proyecto Maeumjigi, mientras simultáneamente comenzábamos el **preprocesamiento de datos de fine-tuning de Llama 3.1**, insinuando una transición completa a un proyecto basado en IA.

### Compilación de la App Android y Pruebas Unitarias

- **Problema**: Necesitábamos verificar si los códigos del cliente Android y del servidor planeados y generados ayer se compilarían con éxito y pasarían las pruebas en el entorno real de Android Studio.
- **Proceso**: 
  > A Claude Code: "Progreso actual... Detener todo el trabajo... ¿En qué estabas trabajando?"
- **Resultado**: Se generaron numerosos artefactos de compilación y metadatos en la ruta `mnd-reservation-alarm/android/app/build/...`. Ejecutamos pruebas unitarias como `NotificationBuilderTest` y comprobamos la canalización de compilación específica de Android. Se probó la lógica central para detectar cambios en las reservas en segundo plano y lanzar alarmas.

### El Gran Punto de Inflexión: Inicio del Preprocesamiento para Llama 3.1

- **Problema**: Más allá de una simple aplicación de alarma, se necesitaba preparación para integrar una IA avanzada que entienda el contexto de reserva y el estado emocional del usuario.
- **Proceso**:
  > A Claude Code: "Por favor, proceda con el trabajo de acuerdo con llama31_finetuning_data_preprocessing_plan_short.md"
  > "No se necesita permiso adicional para ninguna elección con respecto a esta tarea."
- **Resultado**: Dimos un primer paso crucial que cambiaría por completo la naturaleza del proyecto. Instruimos el trabajo de acuerdo con el plan de preprocesamiento de datos para el ajuste fino (fine-tuning) del modelo Llama 3.1. Para acelerar el proceso, otorgamos a la IA una fuerte autoridad diciendo: "ejecuta inmediatamente sin pedir permiso adicional para todas las elecciones", y comenzamos la enorme canalización de procesamiento de datos.

![Captura de Terminal](./images/02_term.png)

Este día fue significativo ya que el trabajo de compilación de Android para mejorar la aplicación y el preprocesamiento de datos de la IA comenzaron en paralelo.
¡A partir de ahora, comenzará en serio el arduo viaje de preprocesamiento de decenas de miles de datos de conversación para ajustarse a Llama 3.1!
