---
slug: 2026-06-18-maeumjigi-23
title: "[Registro de Desarrollo Maeumjigi #23] Safety Wrapper y Presentación Final del Semestre"
authors: [jbgih]
tags: [devlog, fine-tuning, safety wrapper, cloud, capstone]
date: 2026-06-18
---

![Imagen de Portada](./images/01_cover.png)

Al entrar en junio, el equipo completó los desarrollos principales del primer semestre y se enfocó en construir **redes de seguridad** y preparar la **presentación final**.

### El Modelo 2:1 y el Safety Wrapper

> "Decidimos la proporción 2:1. Ahora diseña un safety_wrapper como bloqueo de seguridad."

Seleccionamos el modelo mezclado con una proporción de 2:1 de chat 'emocional' a 'cotidiano'. Sin embargo, para prevenir cualquier alucinación en nuestro chatbot de prevención del suicidio, introdujimos un **Safety Wrapper**. Este módulo verifica las entradas y salidas, cambiando instantáneamente a un protocolo de crisis si se detecta alto riesgo.

### Presupuesto de Servidor (EC2) y Presentación Final

> "¿Cuál es el presupuesto para 5 meses de AWS EC2 g5.2xlarge?"

![Presentación Final](./images/02_presentation.png)

Calculamos el presupuesto del servidor AWS EC2 para ejecutar el chatbot. El 18 de junio, reunimos todos los logros del backend, frontend e IA para completar la **Presentación Final del 1er Semestre (PPTX)**.

¡El primer semestre ha concluido con éxito! Regresaremos con un servicio más avanzado en el segundo semestre.
