```markdown
---
slug: 2026-05-12-maeumjigi-17
title: "[Diario de desarrollo Capstone Maeumjigi #17] Finalización del segundo Fine-Tuning y las trampas del pipeline de evaluación automatizada"
authors: [jbgih]
tags: [diario-de-desarrollo, fine-tuning, máximo-rendimiento, checkpoint, hardcoding, diseño-capstone]
date: 2026-05-12
---

Esta publicación es un registro de desarrollo (Dev Log) que aborda los problemas experimentados durante el proceso de informar sobre la finalización del segundo Fine-Tuning y la construcción del pipeline de automatización de evaluación (Evaluation) para la optimización del modelo de lenguaje de inteligencia artificial (IA) del proyecto Maeumjigi. Resume el proceso de diseño del pipeline y resolución de problemas (troubleshooting) para corregir los errores de configuración de hiperparámetros del experimento anterior y verificar eficientemente los resultados de inferencia de múltiples modelos.

## 🛠 Tech Stack
- **Model:** Qwen35-9B, HCX-Text-1p5B
- **Tuning Method:** PEFT (LoRA)
- **Infrastructure:** Linux GPU Server
- **Scripting:** Shell Script (`.sh`), Jupyter Notebook

## ✨ Features: Finalización del segundo Fine-Tuning y construcción del pipeline para extraer el mejor Checkpoint

### 1. Finalización del Fine-Tuning y extracción de los pesos óptimos (Best Checkpoint)
Se completó el aprendizaje en paralelo del segundo Fine-Tuning (`fine_tuning_2`) corrigiendo los errores de configuración de los hiperparámetros `alpha` y `rank` de LoRA descubiertos en el primer entrenamiento. En total, se exploraron 6 combinaciones de hiperparámetros basadas en 3 modelos base.
Se construyó una lógica para transferir automáticamente al directorio `adapter` el mejor (Best) checkpoint que logró el mayor rendimiento evitando el sobreajuste (Overfitting) para cada modelo, analizando comparativamente la métrica de pérdida de validación (`eval_loss`) inmediatamente después de finalizar el entrenamiento.

### 2. Creación de script de shell para automatización de evaluación y comparación
Se implementó el script `run_test_20_30.sh` para procesar la inferencia del modelo (Eval) y la comparación de resultados (Comparison) de una vez en forma de pipeline en el entorno en segundo plano del servidor. A través de esto, se sentaron las bases para cargar secuencialmente múltiples modelos con fine-tuning y ejecutar pruebas por lotes.

## 🚨 Troubleshooting

### Issue 1: Disminución de la velocidad de inferencia debido a un cuello de botella por Batch Size y falta de almacenamiento
**[Problem]**
Ocurrió un fenómeno anormal de disminución de la velocidad de inferencia durante el proceso de ejecución del script de automatización de evaluación. El rendimiento (Throughput) fue tan bajo que solo se generaron 12 muestras en 15 minutos en el modelo `HCX-Text-1p5B`, que tiene la menor cantidad de parámetros. Como resultado del monitoreo de GPU, el uso de VRAM se mantuvo en el nivel de 1.6GB por dispositivo, por lo que los recursos casi no se utilizaban. Para empeorar las cosas, al mismo tiempo ocurrió un problema de falta de capacidad de almacenamiento del servidor.

**[Cause]**
- Dentro del script de inferencia, el `Batch Size` estaba fijo en 1, lo que limitaba el procesamiento en paralelo de la GPU y causaba un grave cuello de botella computacional.
- Al acumularse grandes archivos de checkpoints y registros, se excedió la capacidad de almacenamiento disponible de la ruta del proyecto existente (`~/home/`).

**[Solution]**
- Para resolver las limitaciones de infraestructura, se migró todo el espacio de trabajo del proyecto a la ruta `~/home/data/temporary/`, que tiene espacio libre, y se restablecieron las rutas de referencia de directorio de todos los scripts de shell relacionados.
- Se planea optimizar la velocidad de inferencia en el futuro aumentando el Batch Size del código de evaluación hasta el límite de la VRAM de la GPU (un nivel donde no ocurra OOM).

### Issue 2: Contaminación de las pruebas debido al Hardcoding en el script de evaluación
**[Problem]**
Pensé que el pipeline de evaluación había funcionado normalmente, pero encontré un error lógico fatal (Logical Bug) durante el proceso de verificación del registro de resultados ejecutados. Copié y ejecuté en segundo plano archivos de cuaderno individuales compuestos por el nombre de cada modelo objetivo, como `20_eval_HCX-Text-1p5B_a8.ipynb`, pero en realidad todos los resultados se generaban solo para un modelo específico idéntico.

**[Cause]**
Al copiar el archivo `.ipynb` que sirve como plantilla mientras se configuraba la lógica de automatización, solo se cambió el nombre del archivo y el nombre del modelo objetivo de evaluación en el código interno mantuvo el estado hardcodeado como `MODEL_ALIAS = 'Qwen35-9B_a16'`. Como resultado, el pipeline cargaba continuamente solo los pesos del modelo `Qwen35-9B_a16` en la VRAM, independientemente del nombre del archivo, repitiendo tareas de inferencia duplicadas.

**[Solution]**
- Se eliminaron las variables hardcodeadas y se refactorizó el código de evaluación para que el nombre del modelo objetivo se pueda mapear dinámicamente (Dynamic Mapping) a través de argumentos (Argument) o variables de entorno durante la ejecución del script.
- Todos los registros de resultados de inferencia existentes contaminados y los productos se eliminaron (Drop), y se planea volver a realizar la inferencia del modelo basándose en el código con el error corregido.
```