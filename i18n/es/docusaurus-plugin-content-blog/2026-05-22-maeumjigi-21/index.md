---
slug: 2026-05-22-maeumjigi-21
title: "[Registro de Desarrollo Maeumjigi #21] Optimizando Proporciones de Datos y el 4to Fine-Tuning"
authors: [jbgih]
tags: [devlog, fine-tuning, dataset, prompt, capstone]
date: 2026-05-22
keywords: [Chatbot de IA para salud mental, Fine-tuning de LLM, Proyecto Capstone, Seguridad de IA, Ingeniería de Prompts]
description: "Alcance del rendimiento óptimo mediante la proporción 2:1 entre diálogo emocional y cotidiano, logrando empatía y coherencia."
---

![Imagen de Portada](./images/01_cover.png)

El 21 y 22 de mayo, el equipo de Maeumjigi se embarcó en la generación masiva de datos y la preparación para el **Cuarto Fine-Tuning (fine_tuning_4)**.

{/* truncate */}

### Conversaciones Emocionales vs. Cotidianas

Mientras probaba el modelo del tercer fine-tuning, descubrí un problema crítico.

> "Las respuestas están demasiado inclinadas hacia la consejería emocional. ¿Cómo mantenemos las habilidades de conversación cotidiana del modelo?"

Nuestro modelo mostraba signos de sobreajuste, dando respuestas excesivamente serias a preguntas mundanas. Para resolver esto, planeamos mezclar datos emocionales y cotidianos.

### Generando 10,000 Datos Emocionales (v6)

Utilicé el modo Batch de la Interfaz de Programación de Aplicaciones (API) de Anthropic (Haiku) para generar 10,000 entradas de datos de conversaciones emocionales. Completé las entradas faltantes con un script adicional para asegurar la calidad.

### Buscando la Proporción Dorada

> "Genera un dataset de 7:3, otro de 2:1 y otro de 5:5."
> "Este cuarto fine-tuning se basará en la proporción de mezcla (mixed_2_1, mixed_5_5, mixed_7_3)."

![Experimento de Proporción](./images/02_ratio.png)

El 4to fine-tuning ahora verifica qué proporción armoniza la 'casualidad diaria' con la 'consejería profesional'. ¡Comenzamos a inyectar estos 3 datasets en el modelo Qwen3.5-9B!

---

## Resumen y Puntos Clave

- **Deteccion del Sesgo Emocional**: Identificado un sesgo excesivo donde el modelo de la 3a fase respondia con gravedad terapeutica a preguntas cotidianas sencillas.
- **Generacion de Corpus Sintetico a Gran Escala**: Creadas 10,000 entradas estandarizadas de dialogo emocional (`v6.jsonl`) mediante Anthropic Haiku Batch API con 20 personas distintas y limite de 500 tokens.
- **Diseno de Matriz de Mezcla de Datos**: Formuladas tres proporciones experimentales (`mixed_7_3`, `mixed_2_1` y `mixed_5_5`) para equilibrar terapia psicologica y conversacion informal.
- **Lanzamiento del 4o Ciclo de Fine-Tuning**: Iniciado el entrenamiento sobre Qwen 3.5-9B para determinar la proporcion dorada que garantice empatia clinica sin perder naturalidad.