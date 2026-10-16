```markdown
---
slug: 2026-05-07-maeumjigi-15
title: "[Diario de Desarrollo Capstone Maeumjigi #15] Visualización de Resultados del Fine-Tuning de 5 Modelos y Configuración del Entorno Local"
authors: [jbgih]
tags: [개발일지, 파인튜닝, 결과분석, 시각화, Jupyter, 캡스톤디자인, 인공지능(AI)]
date: 2026-05-07
---

## 1. Descripción general (Overview)
En esta publicación, abordamos el proceso de integración de los resultados y visualización de las métricas de evaluación de rendimiento de 5 modelos de lenguaje grande (Llama3.3-70B, DSR1-70B, HCX-Omni-8B, Qwen35-9B, HCX-Text-1.5B), cuyo fine-tuning basado en inteligencia artificial (IA) se ha completado para la construcción del servicio de chatbot 'Maeumjigi'. También registramos los problemas que surgieron al migrar el pipeline de análisis, que dependía de un servidor remoto, al entorno local, junto con su proceso de resolución (Troubleshooting).

## 2. Tecnologías utilizadas (Tech Stack)
- **Environment**: VSCode Jupyter Kernel, Local Python Environment
- **Data Analysis & Visualization**: `pandas`, `matplotlib`, `seaborn`
- **Evaluation Metrics**: `bert_score`
- **Models (PEFT/LoRA)**: Llama3.3-70B, DSR1-70B, HCX-Omni-8B, Qwen35-9B, HCX-Text-1.5B

## 3. Configuración del entorno de análisis local y resolución de problemas (Troubleshooting)
Para resolver las limitaciones (renderizado lento e inconveniencia en el manejo de la UI) de `30_comparison.ipynb` que se ejecutaba en el servidor remoto, hemos configurado un nuevo notebook dedicado al entorno local, `31_comparison_local.ipynb`. Durante este proceso, resolvimos los siguientes problemas.

### 3.1. Caída del Kernel (Kernel Crash) y conflictos de dependencias de paquetes
- **Problema**: Ocurrencia frecuente del fenómeno "Kernel Crashed" durante el proceso de configuración del kernel de Jupyter en VSCode local y la instalación y carga de `pandas`, `matplotlib`, `seaborn`, y `bert_score`.
- **Solución**: En lugar del entorno Python global, restablecimos explícitamente un entorno virtual aislado (venv) y reinstalamos las bibliotecas necesarias ajustando las dependencias entre sus versiones, asegurando así un entorno de ejecución del kernel estable.

### 3.2. Error de referencia de módulo personalizado (ModuleNotFoundError)
- **Problema**: Debido a la diferencia en la estructura de directorios entre el servidor remoto y el local, ocurría `ModuleNotFoundError: No module named 'ft_utils'` al ejecutar la visualización.
- **Solución**: Resolvimos el problema de referencia de módulos añadiendo dinámicamente la ruta absoluta del directorio raíz del proyecto y de la carpeta de utilidades mediante `sys.path.append()`.

### 3.3. Recuperación de datos de métricas omitidos en ciertos modelos
- **Problema**: Se identificó que faltaba el archivo de indicadores de evaluación `ft_metrics.json` en el directorio de resultados de algunos modelos, como DSR1-70B.
- **Solución**: Escribimos un script de Python independiente que parsea los checkpoints y los datos de registro (logging) que quedaban en el servidor para recalcular y recuperar las métricas faltantes, regenerando así `ft_metrics.json` correctamente.

## 4. Características principales (Features): Visualización integral de datos de 5 modelos
Para comparar el rendimiento de los modelos de manera objetiva e intuitiva, establecimos un plan de análisis llamado `5MODELS_ORGANIZATION_PLAN_present.md` y mejoramos el pipeline de visualización.

### 4.1. Eliminación de ruido en la curva de pérdida (Loss Curve) y mejora de la legibilidad
Eliminamos las líneas de tendencia innecesarias (líneas gruesas) que aparecían en el gráfico inicial y ajustamos la transparencia (Alpha) y el grosor de la curva de aprendizaje real (línea tenue) de cada modelo para aumentar la nitidez. A través de esto, mejoramos el gráfico para poder comparar de un vistazo la velocidad de convergencia (Convergence) y la presencia de sobreajuste (Overfitting) de los 5 modelos.

![Training Loss ALL](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week9/fine_tuning/results/figures/training/03_training_loss_all.png)
*▲ Visualización de las curvas de pérdida de entrenamiento (Training Loss) de los 5 modelos. Se puede observar una tendencia de reducción de pérdida estable a medida que avanzan los pasos de entrenamiento.*

![Eval Loss ALL](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week9/fine_tuning/results/figures/training/04_eval_loss_all.png)
*▲ Visualización de las curvas de pérdida de evaluación (Eval Loss) de los 5 modelos. Comparamos de forma intuitiva el rendimiento de generalización sobre el conjunto de datos de evaluación.*

### 4.2. Análisis de ocupación de recursos y optimización de parámetros (LoRA)
Además de las métricas de rendimiento, analizamos adicionalmente el consumo de recursos de cada modelo y la estabilidad de las capas LoRA, considerando la implementación en el servicio real.

![GPU Memory](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week9/fine_tuning/results/figures/training/02_gpu_memory.png)
*▲ Resultados del benchmark de la ocupación de memoria GPU (VRAM) por modelo durante el proceso de entrenamiento*

Además, para verificar la eficiencia del fine-tuning por modelo, analizamos la distribución de valores singulares (Singular Value) mediante la visualización de la descomposición del rango de LoRA (fenómeno de colapso de rango). A continuación, se muestran los resultados del análisis de dos modelos representativos.

![Llama3.3-70B LoRA Rank](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week10/Llama33-70B/llama33_lora_rank_decomposition.png)
*▲ Análisis del fenómeno de LoRA Rank Decomposition de Llama3.3-70B*

![Qwen35-9B LoRA Rank](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week10/Qwen35-9B/qwen35_lora_rank_decomposition.png)
*▲ Análisis del fenómeno de LoRA Rank Decomposition de Qwen35-9B*

> *※ Los indicadores de Rank Decomposition del resto de los modelos como DSR1-70B, HCX-Omni-8B y HCX-Text-1.5B también han sido documentados y guardados utilizando el mismo pipeline.*

## 5. Conclusión y planes futuros
Al construir un pipeline estable de comparación y análisis en el entorno local, la eficiencia del trabajo de validación de datos ha mejorado significativamente. Los diversos gráficos e indicadores cuantitativos extraídos se utilizarán como material base principal para la presentación intermedia del proyecto Capstone que se llevará a cabo la próxima semana, y en base a esto, planeamos seleccionar el modelo final que se integrará en el servicio de chatbot 'Maeumjigi'.
```