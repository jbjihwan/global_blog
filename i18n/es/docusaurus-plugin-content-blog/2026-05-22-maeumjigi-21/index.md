---
slug: 2026-05-22-maeumjigi-21
title: "[Registro de Desarrollo Maeumjigi #21] Optimizando Proporciones de Datos y el 4to Fine-Tuning"
authors: [jbgih]
tags: [devlog, fine-tuning, dataset, prompt, capstone]
date: 2026-05-22
---

![Imagen de Portada](./images/01_cover.png)

El 21 y 22 de mayo, el equipo de Maeumjigi se embarcó en la generación masiva de datos y la preparación para el **Cuarto Fine-Tuning (fine_tuning_4)**.

### Conversaciones Emocionales vs. Cotidianas

Mientras probaba el modelo del tercer fine-tuning, descubrí un problema crítico.

> "Las respuestas están demasiado inclinadas hacia la consejería emocional. ¿Cómo mantenemos las habilidades de conversación cotidiana del modelo?"

Nuestro modelo mostraba signos de sobreajuste, dando respuestas excesivamente serias a preguntas mundanas. Para resolver esto, planeamos mezclar datos emocionales y cotidianos.

### Generando 10,000 Datos Emocionales (v6)

Utilicé el modo Batch de la API de Anthropic (Haiku) para generar 10,000 entradas de datos de conversaciones emocionales. Completé las entradas faltantes con un script adicional para asegurar la calidad.

### Buscando la Proporción Dorada

> "Genera un dataset de 7:3, otro de 2:1 y otro de 5:5."
> "Este cuarto fine-tuning se basará en la proporción de mezcla (mixed_2_1, mixed_5_5, mixed_7_3)."

![Experimento de Proporción](./images/02_ratio.png)

El 4to fine-tuning ahora verifica qué proporción armoniza la 'casualidad diaria' con la 'consejería profesional'. ¡Comenzamos a inyectar estos 3 datasets en el modelo Qwen3.5-9B!
