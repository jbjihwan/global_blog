---
slug: 2026-05-20-maeumjigi-20
title: "[Registro de Desarrollo Maeumjigi #20] 3er Fine-Tuning y Mejoras del Backend"
authors: [jbgih]
tags: [devlog, fine-tuning, backend, frontend, database, capstone]
date: 2026-05-20
keywords: [Chatbot de IA para salud mental, Fine-tuning de LLM, Proyecto Capstone, Seguridad de IA, Ingeniería de Prompts]
description: "Estrategia para el 3º fine-tuning: calibración de la proporción entre charla casual y diálogo de crisis para evitar respuestas exageradas."
---

![Imagen de Portada](./images/01_cover.png)

Durante el 19 y 20 de mayo, la evaluación del tercer fine-tuning (`fine_tuning_3`) y la mejora de las características de backend y frontend procedieron en paralelo.

{/* truncate */}

### Concluyendo el 3er Fine-Tuning

El entrenamiento para el 3er fine-tuning, configurado con conceptos de gráficos de conocimiento en mente, se completó.

> "Selecciona el checkpoint con el mejor eval, reemplaza los archivos en la carpeta adapter."

En lugar de copiar checkpoints manualmente, le indiqué a la IA que escribiera un script que extrajera automáticamente los mejores pesos del modelo y los configurara. Luego, ejecuté el script de inferencia paralela en el servidor.

### Backend y Frontend: Base de Datos y Foro

Mientras los modelos trabajaban en el servidor, aceleré el trabajo de integración de la aplicación y la BD.

Para resolver el frustrante error `401 Unauthorized` de la última vez, examiné `seed_data.sql` para verificar las contraseñas. Como resultado, logré un importante commit en Git:
`feat: Añadido guardado de chatbot en BD, paginación de foro y filtro de diario de emociones`

![Características de la App](./images/02_app_feature.png)

¡Finalmente, los registros de conversación de nuestro chatbot comenzaron a guardarse oficialmente en la base de datos! Además, se añadieron la paginación para el foro comunitario y el filtro del diario de emociones. 

Fue un momento emocionante cuando el modelo finalmente comenzó a servirse en una aplicación móvil.

---

## Resumen y Puntos Clave

- **Seleccion Automatizada de Checkpoints**: Implementados scripts de evaluacion en servidor que extraen y configuran automaticamente los mejores pesos de adaptadores sin intervencion manual.
- **Benchmarking Paralelo Multimodelo**: Orquestado un pipeline de evaluacion en segundo plano ejecutando inferencias simultaneas sobre cuatro modelos candidatos en GPUs remotas.
- **Persistencia de Conversaciones en Base de Datos**: Resueltos los bloqueos de autenticacion (`401 Unauthorized`) y asegurado el registro permanente de los dialogos en PostgreSQL/MySQL.
- **Ampliacion de Funciones en App Movil**: Integradas la paginacion del foro comunitario y el filtrado avanzado del diario de animo en el cliente movil React Native.