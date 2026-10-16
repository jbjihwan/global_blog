```markdown
---
slug: 2026-04-01-maeumjigi-4
title: "[Diario de Desarrollo Capstone Maeumjigi #4] Puesta en Marcha del Preprocesamiento de Datos para Fine-tuning"
authors: [jbgih]
tags: [개발일지, 인공지능(AI)코딩, ClaudeCode, 캡스톤디자인, 파인튜닝, 데이터전처리, Llama3.1]
date: 2026-04-01
---

## Overview

Este es un registro de la puesta en marcha del pipeline de preprocesamiento de datos (Data Preprocessing) para realizar el fine-tuning del modelo Llama 3.1, que es el motor de inferencia central del proyecto 'Maeumjigi'. El proceso de transformar grandes volúmenes de datos de conversación sin procesar a un formato JSONL especial que el modelo puede aprender se automatizó utilizando el agente de inteligencia artificial (IA) Claude Code.

## Tech Stack
- **Target Model**: Llama 3.1
- **Automation Agent**: Claude Code
- **Data Format**: JSONL (Basado en roles de System, User, Assistant)

## Features: Construcción del Pipeline de Preprocesamiento de Datos basado en Markdown

En lugar de limpiar manualmente decenas de miles de datos sin procesar, se redactó un plan de preprocesamiento en formato Markdown llamado `llama31_finetuning_data_preprocessing_plan_short.md` y se entregó al agente. Claude Code analizó las reglas y la estructura del pipeline definidas en el documento para construir y ejecutar de forma autónoma scripts de Python para la limpieza y el procesamiento de los datos.

## Troubleshooting

### Issue: Fusión de Datos de Categorías Dispersas y Conversión al Formato Llama 3.1
El proceso de preprocesamiento estaba dividido en varios pasos (Steps), y para el fine-tuning final, era necesario integrar los datos de conversación de categorías dispersas en un único conjunto de datos (dataset). Además, existía el requisito técnico de mapear perfectamente los datos integrados al formato JSONL del tipo Chat/Instruct que Llama 3.1 puede reconocer. Más allá de simplemente combinar el texto, era necesario transformar sin omisiones la distinción de los roles (Roles) de User y Assistant, manteniendo inyectado el prompt del System.

### Solution: Fusión de Datos de Categorías y Ejecución Automática de Scripts de Conversión JSONL (Step 4)

Para desencadenar la etapa final del pipeline, se dio la siguiente instrucción a Claude Code:

> "Ejecuta el Step 4. Integra los datos de las dos categorías y conviértelos al formato JSONL de Llama 3.1."

Al recibir la orden, el agente ejecutó inmediatamente el Step 4, completando con éxito las siguientes tareas:
1. Fusión (Merge) de los datos de conversación de cada categoría que estaban dispersos en una única estructura.
2. Conversión de los datos en un objeto de la forma `{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}` de acuerdo con las especificaciones de la plantilla de prompts de Llama 3.1.
3. Limpieza del conjunto de datos mediante un script de Python, seguida de la exportación final (Export) al formato JSONL adecuado para el entrenamiento.

## Result & Next Step
A través del pipeline automatizado de preprocesamiento, numerosos datos sin procesar se transformaron a un estado en el que pueden ser introducidos inmediatamente en el entrenamiento de fine-tuning. En el próximo hito (milestone), utilizaremos este conjunto de datos preprocesado para llevar a cabo el proceso de entrenamiento (Training) y validación (Validation) del modelo Llama 3.1 real.
```