---
slug: 2026-05-08-maeumjigi-16
title: "[Registro de Desarrollo Maeumjigi #16] Error Fatal, 2do Fine-Tuning y App React Native"
authors: [jbgih]
tags: [devlog, fine-tuning, LoRA, hyperparameters, ReactNative, app-development, frontend]
date: 2026-05-08
keywords: [Chatbot de IA para salud mental, Fine-tuning de LLM, Proyecto Capstone, Seguridad de IA, Ingeniería de Prompts]
description: "Diagnóstico de errores de hardcoding en las plantillas de prompts y depuración urgente para asegurar la integridad de los datos."
---

![Imagen de Portada](./images/01_cover.png)

El 8 de mayo preparábamos la presentación de los resultados. Sin embargo, descubrí un error masivo.

{/* truncate */}

### Error Fatal en los Hiperparámetros de LoRA

> "Las respuestas del modelo son más cortas. Creo que es porque establecer r de LoRA a 8 y alfa a 16 redujo demasiado las características..."
> "Espera, ¿era a/r? Pensé que era r/a...???"

Comprendí mal la ecuación, configurándola de una manera que suprimió severamente o amplificó excesivamente las actualizaciones de peso. Con razón las respuestas eran anormalmente cortas.

### 2da Ronda de Fine-Tuning (fine_tuning_2)

No podíamos simplemente avanzar. Inmediatamente creé una carpeta `fine_tuning_2` para una segunda ronda de fine-tuning.

> "Entrenar con rank=16, alpha=16, y en MIG-1 con rank=16, a=8."
> "Extraiga las 2000 entradas más largas de Daily_train_dataset."

Para evitar respuestas cortas, extrajimos solo los 2000 conjuntos de datos más largos y dividimos nuestros recursos de GPU para ejecutar entrenamiento en paralelo.

### Desarrollo Frontend (App)

![Desarrollo de App](./images/02_app.png)

Mientras los modelos entrenaban, comencé a desarrollar la aplicación frontend.

> "Necesito mostrar un código QR para ejecutar maeum-app... pero cuando escribo npx go start, solo obtengo un error."

Creé el proyecto usando React Native (Expo) y, después de algunos errores tipográficos, logré mostrar el código QR de Expo. Fue un día emocionante construyendo tanto el cerebro (IA) como la cara de la aplicación.

---

## Resumen y Puntos Clave

- **Diagnostico de Hiperparametros LoRA**: Descubierto que las respuestas truncadas se debian a un error en la proporcion de escala entre rank y alpha, reestructurando la configuracion.
- **Lanzamiento del 2o Ciclo de Fine-Tuning**: Iniciado el entrenamiento paralelo dividiendo particiones GPU MIG para comparar `rank=16, alpha=16` frente a `rank=16, alpha=8`.
- **Curacion de Dataset de Texto Largo**: Filtradas las 2,000 conversaciones mas extensas (`Daily_train_dataset_long.jsonl`) para incentivar respuestas de empatia profunda y sostenida.
- **Inicio de la App Movil en React Native**: Creado el proyecto `maeum-app` con Expo, configurando la depuracion por codigo QR y los recursos visuales de la aplicacion.