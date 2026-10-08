---
slug: 2026-04-08-maeumjigi-8
title: "[Registro de Desarrollo Maeumjigi #8] Incidente de la Factura de API y Preparación del Fine-Tuning en Colab"
authors: [jbgih]
tags: [devlog, API-billing, Llama3.1, fine-tuning, GoogleColab, preprocesamiento]
date: 2026-04-08
---

![Imagen de Portada](./images/01_cover.png)

El 8 de abril fue el día en que experimentamos la mayor crisis y un suceso de 'reír y llorar' mientras trabajábamos en el proyecto Maeumjigi. Fue el **incidente de exceso del límite mensual y la bomba de facturación de la API de Claude**.

### La Traición del Segundo Plano: "¿$1 por 10 registros?"

- **Problema**: Aliviados de haber terminado la optimización ayer, dejamos el script de generación de conjuntos de datos masivos ejecutándose en segundo plano sin supervisión.
- **Proceso**: 
  > "Problema: Facturado excediendo el límite mensual. Lo dejé funcionando pensando que solo estaba trabajando en segundo plano, y sucedió esto."
  > "De ninguna manera, ¿cuesta $1 generar 10 registros? ¿Tiene sentido?"
- **Resultado**: Durante el proceso de sintetizar datos de asesoramiento de alta calidad, el contexto del prompt (tokens de entrada) se acumuló, lo que provocó que el costo aumentara exponencialmente. El script se detuvo porque se excedió el límite de facturación mensual. Instruimos urgentemente a la IA: "Agrega de inmediato una función para imprimir el consumo estimado, el costo y el progreso en tiempo real en la consola". Aprendimos por las malas lo crucial que es el monitoreo de facturación.

### Escribiendo un Cuaderno de Colab para el Entrenamiento de Llama 3.1

- **Problema**: A medida que los datos estaban listos, ahora necesitábamos el código para realizar realmente el ajuste fino (fine-tuning) del modelo Llama 3.1. Dado que la GPU de nuestra PC local no era suficiente, tuvimos que usar Google Colab.
- **Proceso**:
  > "Por favor, escriba un cuaderno de python para ejecutar llama31_finetuning_experiment_plan_revised.md en Colab."
  > "Divida los datos de entrenamiento solo en train/val en lugar de train/val/test, usando una proporción de 9:1."
- **Resultado**: La IA leyó el plan de entrenamiento y escribió un código perfecto de Jupyter Notebook llamado `llama31_finetuning_colab.ipynb`. Implementó perfectamente la lógica, incluida la configuración de las bibliotecas más recientes como Unsloth, y la división del conjunto de datos en una proporción de 9:1 para entrenamiento y validación.

![Captura de Terminal](./images/02_term.png)

Hoy superamos una barrera realista del proyecto, pagando una tarifa de iniciación aterradora llamada bomba de facturas de API. Sin embargo, a cambio, completamos un excelente conjunto de datos y un cuaderno de Colab para el fine-tuning. ¡Finalmente, el siguiente paso es entrenar el modelo de IA real!
