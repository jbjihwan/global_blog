---
slug: 2026-05-30-maeumjigi-22
title: "[Registro de Desarrollo Maeumjigi #22] ¡4to Fine-Tuning Completo! Arquitectura e Informe Final"
authors: [jbgih]
tags: [devlog, fine-tuning, architecture, capstone, final report]
date: 2026-05-30
---

![Imagen de Portada](./images/01_cover.png)

En la última semana de mayo, nos dedicamos a concluir los resultados del tan esperado **4to Fine-Tuning (fine_tuning_4)** y solidificar la estructura del sistema.

### Checkpoint Final 4400 y Análisis

> "Qwen35-9B_mixed_7_3/checkpoints/checkpoint-4400/adapter_config.json"

El cuarto modelo, entrenado con una mezcla de chat casual y datos de consejería emocional, finalmente terminó el entrenamiento y produjo el peso óptimo: `checkpoint-4400`. 

Al experimentar con la proporción de mezcla de datos, el modelo finalmente renació como un chatbot perceptivo que distingue perfectamente entre conversaciones diarias y consejería de crisis seria.

### Arquitectura del Sistema e Informe Final

> "Generación de chatbot_architecture.html completa"

![Arquitectura del Sistema](./images/02_architecture.png)

Para servir el modelo verificado como una aplicación real, diseñamos la arquitectura de todo el sistema y el plan de integración de Gráficos de Conocimiento (Knowledge Graph) bajo el nombre `chatbot_architecture.html`.

Y el 30 de mayo generamos automáticamente el `informe_fine_tuning_4.docx`. El informe contiene comparaciones de respuestas reales entre el modelo original y el nuestro, ¡demostrando que nuestro arduo trabajo no fue en vano!

Con esto concluyen los registros de desarrollo de mayo.
