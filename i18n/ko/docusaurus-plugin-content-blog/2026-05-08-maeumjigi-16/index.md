```markdown
---
slug: 2026-05-08-maeumjigi-16
title: "[Diario de Desarrollo Capstone de Maeumjigi #16] Error Crítico y Segundo Fine-tuning, y el Primer Lanzamiento de la App en React Native"
authors: [jbgih]
tags: [diario de desarrollo, fine-tuning, LoRA, hiperparámetros, ReactNative, desarrollo de apps, frontend]
date: 2026-05-08
---

Mientras preparaba los materiales para la presentación intermedia del diseño capstone y analizaba los resultados del primer fine-tuning, descubrí un error en la configuración de los hiperparámetros (Hyperparameter) que afectaba gravemente la calidad de las respuestas del modelo. En este post, registro el análisis de las causas de este problema, el proceso del segundo fine-tuning para solucionarlo y el proceso de configuración inicial del frontend del lado del cliente (React Native).

## Solución de Problemas: Error de Configuración de Hiperparámetros LoRA y Fenómeno de Acortamiento de la Longitud de Respuesta

### Problema
Como resultado de la evaluación cualitativa de los resultados del primer fine-tuning del modelo de inteligencia artificial (IA), se produjo un fenómeno en el que la longitud del texto generado era anormalmente corta en comparación con el modelo base (Base Model) y el contexto se cortaba a la mitad.

### Causa
La causa fue un error de cálculo en la proporción (Scaling Factor) de los valores `rank(r)` y `alpha` configurados durante el entrenamiento LoRA (Low-Rank Adaptation). 
Durante el entrenamiento inicial, se configuró como `r=8` y `alpha=16`, pero en la ecuación de actualización de pesos de LoRA, el scaling factor se determina mediante $\frac{\alpha}{r}$. Como norma general, es común configurar `alpha` igual a `rank` o darle el doble del valor para ajustar el scaling factor alrededor de 1.0~2.0. Sin embargo, debido a una confusión en la proporción de aplicación de la fórmula, la actualización de los pesos se configuró para que se suprimiera extremadamente o se reflejara excesivamente. Como resultado, el espacio de representación de características intermedias (Feature) se distorsionó, causando el problema de que el modelo no pudiera generar texto con una longitud suficiente y terminara anticipadamente (Early Stopping).

---

## Solución: Refinamiento de Datos y Segundo Fine-Tuning en Paralelo (fine_tuning_2)

Para resolver fundamentalmente el problema del acortamiento de la longitud de la respuesta y optimizar el rendimiento de generación del modelo, decidimos llevar a cabo un segundo fine-tuning mediante la construcción inmediata del pipeline `fine_tuning_2`.

### 1. Ingeniería de Datos: Extracción de Conjuntos de Datos Largos
Para inducir al modelo a generar un contexto más largo y rico, reestructuramos los datos de entrenamiento. A partir del `Daily_train_dataset.jsonl` existente, extrajimos por separado solo los 2.000 conjuntos de datos principales con las longitudes de token de texto más largas para generar `Daily_train_dataset_long.jsonl`, y lo utilizamos para el segundo entrenamiento.

### 2. Entrenamiento Distribuido: Entrenamiento en Paralelo MIG y Optimización de Hiperparámetros
Seleccionamos `HCX-Text-1p5B`, `Llama33-70B` y `Qwen35-9B` como modelos para el experimento. Para encontrar la proporción óptima de hiperparámetros LoRA, dividimos los recursos MIG (Multi-Instance GPU) y realizamos el entrenamiento en paralelo con diferentes configuraciones de la siguiente manera:

*   **Entorno MIG-0**: `rank=16`, `alpha=16` (Scaling factor: 1.0)
*   **Entorno MIG-1**: `rank=16`, `alpha=8` (Scaling factor: 0.5)

A continuación, se muestra la estructura de la red neuronal del adaptador LoRA para cada modelo aplicada en este segundo fine-tuning.

![HCX-Text-1p5B LoRA Structure](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week10/HCX-Text-1p5B/hcx_text_with_lora_structure.png)
*Estructura de la aplicación LoRA del modelo HCX-Text-1p5B*

![Llama33-70B LoRA Structure](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week10/Llama33-70B/llama33_with_lora_structure.png)
*Estructura de la aplicación LoRA del modelo Llama33-70B*

![Qwen35-9B LoRA Structure](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week10/Qwen35-9B/qwen35_with_lora_structure.png)
*Estructura de la aplicación LoRA del modelo Qwen35-9B*

---

## Características: Construcción Inicial de la Aplicación Frontend (React Native)

Mientras se llevaba a cabo el segundo entrenamiento distribuido del modelo de IA backend, comenzamos a desarrollar la aplicación cliente con la que los usuarios reales interactuarán en el servicio 'Maeumjigi'.

### Stack Tecnológico
*   **Framework**: React Native
*   **Toolchain**: Expo CLI

### Implementación y Solución de Problemas
Inicializamos un proyecto React Native (Expo) con el nombre `maeum-app`. Para vincular el teléfono inteligente con el servidor en tiempo de ejecución en el entorno de desarrollo local, fue necesario ejecutar el servidor de desarrollo de Expo.

Durante el inicio inicial, se ingresó un comando incorrecto (`npx go start`), lo que provocó un error de vinculación del servidor local y un error en la terminal. Posteriormente, a través del comando correcto de Expo CLI, construimos el servidor normalmente y logramos conectarnos al entorno de depuración escaneando el código QR de Expo renderizado en la terminal con la cámara del dispositivo físico (Smartphone). Adicionalmente, también completamos la tarea de configurar el entorno del icono (`assets/logo.png`), que es el activo estático inicial de la aplicación, construyendo con éxito el esqueleto del frontend para todo el proyecto.
```