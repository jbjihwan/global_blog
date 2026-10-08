---
slug: 2026-05-17-maeumjigi-19
title: "[Registro de Desarrollo Maeumjigi #19] Automatización de Informes y Problemas de BD"
authors: [jbgih]
tags: [devlog, fine-tuning, report, backend, DB, troubleshooting, capstone]
date: 2026-05-17
---

![Imagen de Portada](./images/01_cover.png)

¡Debo corregir mi suposición de que el 13 de mayo fue el último día! El 17 de mayo hubo una ola masiva de pruebas de backend y redacción de informes.

### Automatizando el Informe con IA

No había tiempo suficiente para analizar manualmente los gráficos masivos del segundo fine-tuning.

> "Crea un prompt para escribir un informe comparando los resultados. Guárdalo y escribe el informe."

Intenté utilizar ingeniería de prompts para que la IA interpretara las métricas. La IA analizó los pros y contras de cada modelo, generando un excelente borrador en Word (.docx).

### Integración de Base de Datos y el Error 401

Comencé a insertar datos de `backup.sql` en la BD local de PostgreSQL para probar la estabilidad.

> "Contraseña incorrecta... POST /auth/login 401 Unauthorized"

Caí en un infierno de errores de inicio de sesión. Creé scripts de depuración y reinicié el servidor uvicorn sin fin.

![Problemas de BD](./images/02_db.png)

### Gráficos de Conocimiento (Knowledge Graphs)

A altas horas de la noche, para superar las limitaciones del simple LLM, comencé a diseñar un plan para explorar la fusión de ontologías y Gráficos de Conocimiento. ¡El proyecto se está volviendo masivo!
