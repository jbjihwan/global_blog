---
slug: 2026-04-05-maeumjigi-6
title: "[Registro de Desarrollo Maeumjigi #6] Automatización del Informe Final de Preprocesamiento y Kickoff del Frontend"
authors: [jbgih]
tags: [devlog, informe-final, automatización, Next.js, capstone, preprocesamiento]
date: 2026-04-05
---

![Imagen de Portada](./images/01_cover.png)

El 5 de abril marca el día en que concluimos el arduo viaje de preprocesamiento de datos (v1~v4) generando un informe final, 
al tiempo que iniciamos (kickoff) el proyecto de frontend que se convertirá en el rostro del servicio web Maeumjigi.

### Documentación Perfecta: De Markdown a DOCX y Gráficos

- **Problema**: Necesitábamos compartir el masivo proceso de preprocesamiento con nuestro profesor asesor y los miembros del equipo de una manera visualmente comprensible.
- **Proceso**: 
  > A Claude Code: "Por favor, escriba un informe final que resuma el proceso de preprocesamiento de datos... Añada ejemplos representativos para cada versión."
  > "Convierta este archivo md en un archivo docx... Exprese las cosas que se pueden graficar como gráficos y añádalos."
- **Resultado**: Sorprendentemente, la IA analizó los scripts de Python y los datos JSON en los que habíamos trabajado y redactó un informe resumido en Markdown sin esfuerzo. Yendo aún más lejos, instaló de forma independiente bibliotecas de Python (`python-docx`, `matplotlib`), escribió un script, convirtió el Markdown en un archivo Word (DOCX) ordenado, ¡e incluso dibujó e insertó gráficos de distribución de emociones! Fue un momento que redujo drásticamente el tiempo perdido en documentación.

### Kickoff del Proyecto Frontend Basado en Next.js

- **Problema**: Aparte de entrenar el modelo de IA, necesitábamos una interfaz web donde los usuarios pudieran chatear realmente con el bot.
- **Proceso**: (Tarea en segundo plano) Instruimos la configuración de un proyecto frontend basado en Next.js para proporcionar una interfaz de usuario rápida y familiar para los usuarios.
- **Resultado**: Se generaron `package.json`, `tsconfig.json`, etc., en la ruta `maeumjigi/frontend/`, configurando con éxito el entorno frontend más moderno basado en Next.js.

![Captura de Terminal](./images/02_term.png)

Hoy probamos que las capacidades de la IA van mucho más allá de la simple programación, desempeñando a la perfección el papel de un excelente asistente de oficina mediante el 'resumen de documentos, la visualización de gráficos y la generación de DOCX'.
