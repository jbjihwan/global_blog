```markdown
---
slug: 2026-04-07-maeumjigi-7
title: "[Registro de Desarrollo de Capstone Maeumjigi #7] Optimización de Generación de Datos Sintéticos (v5) e Integración Frontend"
authors: [jbgih]
tags: [registro-de-desarrollo, datos-sintéticos, ClaudeAPI, generación-de-datos, frontend, optimización-de-costos]
date: 2026-04-07
---

## 1. Resumen (Overview)

En esta publicación, cubrimos el proceso de ejecutar el servidor frontend (`mental-health`) del proyecto capstone Maeumjigi en un entorno local para prepararse para la integración con el backend, y la construcción de un canal (pipeline) para generar a gran escala datos de entrenamiento faltantes utilizando inteligencia artificial (IA). Hemos resumido el proceso de generación de 60.000 datos sintéticos (Synthetic Data) para el ajuste fino (fine-tuning) de Llama 3.1, la optimización de los costos de API resultantes (Optimization) y los problemas resueltos (troubleshooting) durante la integración del frontend.

## 2. Generación de Datos Sintéticos (v5) y Optimización de Costos

### 2.1 Feature: Construcción de un Canal de Datos Sintéticos a Gran Escala
Los datos refinados (v4) a través del canal existente carecían de diversidad para cubrir líneas emocionales específicas o escenarios de asesoramiento psicológico detallados. Para resolver esto, planificamos la generación del conjunto de datos v5, que contiene 60.000 conversaciones virtuales de asesoramiento de alta calidad adaptadas al formato de entrenamiento de Llama 3.1 (`System`, `User`, `Assistant`), utilizando la API de Claude. Establecimos el plan `v5_plan.md` para generar datos estructurados en formato `jsonl` y comenzamos la ejecución del script a gran escala.

### 2.2 Troubleshooting: Problema de Aumento en los Costos de Llamadas a la API
Tan pronto como se ejecutó el script, surgió un problema en el que el costo de las llamadas a la API superó significativamente las estimaciones. Durante el proceso de generación de 60.000 datos, a pesar de estar en la etapa de progreso inicial (Progress), nos enfrentamos a una rápida reducción de 10 dólares en créditos y al riesgo de facturas masivas debido al desperdicio de tokens de salida causado por respuestas detalladas (Verbose) del modelo.

![데이터 생성 파이프라인 비용 및 아키텍처](D:/서울과기대 컴퓨터공학과/26-1/TNS/조별발표/PPT 이미지/3장.png)

### 2.3 Solution: Ingeniería de Prompts y Optimización de Código
Para reducir costos y asegurar la recopilación estable de datos, escribimos el script `step8_generate_v5_optimized.py` y procedimos con la optimización del canal.

- **Ajuste de Prompts (Prompt Engineering)**: Rediseñamos el System Prompt para que Claude excluya introducciones innecesarias o formato markdown, y devuelva estrictamente datos de conversación en formato JSONL, reduciendo drásticamente el uso de Output Tokens.
- **Gestión y Recuperación de Estado (State Management)**: Agregamos una lógica de puntos de control (checkpoint) para que, incluso si el script se detiene debido a errores de red o por exceder el límite de facturación durante solicitudes de API a gran escala, el progreso de generación anterior (Progress) y los datos se puedan guardar de forma segura localmente y reanudar (Resume).

## 3. Traspaso de Frontend e Integración en Entorno Local

### 3.1 Feature: Preparación para la Integración Frontend
Tomamos el relevo del repositorio `mental-health` desarrollado por un compañero de equipo, lo ejecutamos en el entorno local y procedimos con la configuración del entorno de ejecución del cliente para la futura integración con la API del modelo backend.

### 3.2 Troubleshooting: Error de Migración de Base de Datos
Durante la fase de configuración inicial para levantar el servidor frontend, mientras se ejecutaba el script de migración de base de datos (DB) número 4, ocurrió un error en la DB debido a un conflicto de esquemas (Schema), lo que impidió que el servidor arrancara normalmente.

![프론트엔드 DB 마이그레이션 오류 트러블슈팅](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week6/프론트엔드버그.png)

### 3.3 Solution: Resolución de Errores de Migración y Estandarización de Ejecución
- Analizamos los registros de errores de migración de la DB para restablecer el historial de migraciones en conflicto y sincronizamos correctamente el esquema con el comando adecuado.
- Ejecutamos con éxito el servidor frontend en el entorno local y, para evitar cuellos de botella en el mismo proceso durante la colaboración futura, documentamos el método de apagado del servidor (Graceful Shutdown) y un procedimiento simple para el reinicio (Start-up Sequence), finalizando así el proceso de traspaso.

## 4. Retrospectiva (Wrap-up)

Hoy fue un día significativo en el que fuimos más allá del simple preprocesamiento de datos y construimos un canal de **Generación de Datos Sintéticos (Synthetic Data Generation)**, haciendo que un modelo generativo cree directamente los libros de texto (Data) para ajustar (fine-tune) a otro modelo. Incluso ante la crisis de cargos excesivos de la API, resolvimos el problema a través de la ingeniería de prompts y la optimización a nivel de código, y logramos levantar con éxito el cliente frontend, completando así una etapa de preparación de la infraestructura para el desarrollo full-stack y el servicio de modelos.
```