Aquí tienes la traducción al español del post del blog técnico, manteniendo el formato Markdown, la estructura del *frontmatter* y los bloques de código:

```markdown
---
slug: 2026-05-04-maeumjigi-13
title: "[Diario de desarrollo de Capstone Maeumjigi #13] Límites del entrenamiento de 70B y estrategia alternativa con modelos medianos y pequeños (HCX, Qwen)"
authors: [jbgih]
tags: [diario de desarrollo, fine-tuning, HCX-Omni-8B, Qwen35-9B, checkpoint, hiperparámetros, inteligencia artificial (IA)]
date: 2026-05-04
---

## 1. Problemas de OOM y límites en el fine-tuning de modelos de 70B
Durante el proceso de fine-tuning (ajuste fino) de inteligencia artificial (IA) de los modelos Llama3.3 70B y DeepSeek-R1 70B, que eran nuestro plan inicial, nos enfrentamos a un grave problema de OOM (Out of Memory). Para contener el uso de memoria, aplicamos un método de reducción extrema del tamaño de lote (Batch Size) y forzamos el progreso del entrenamiento hasta `checkpoint-1200` y `1300`. Sin embargo, debido a esto, la velocidad de entrenamiento se redujo de manera exponencial, y nos encontramos en una situación en la que era difícil esperar una convergencia (Convergence) significativa de la pérdida (Loss) dentro de los limitados recursos físicos del servidor y el plazo del proyecto capstone.

## 2. Estrategia de pivoteo (Pivot) hacia modelos medianos y pequeños (sLLM)
Para superar las limitaciones de recursos físicos y cumplir con el cronograma del proyecto, cambiamos nuestro objetivo hacia modelos medianos y pequeños (1.5B ~ 9B) con un número relativamente menor de parámetros. 
La nueva línea de modelos adoptados es la siguiente:
- **HCX-Omni-8B**
- **Qwen35-9B**
- **HCX-Text-1.5B**

### 2.1 Ajuste de hiperparámetros y evaluación de rendimiento
A pesar de la reducción en la escala del modelo, el proceso de optimización de hiperparámetros (Hyperparameter) para extraer el mejor rendimiento era esencial. Especialmente considerando el equilibrio (Trade-off) entre la velocidad de entrenamiento y el rendimiento de generalización (Generalization), probamos principalmente el aumento del tamaño del lote dentro de los límites permitidos por la memoria. 
Para una validación eficiente del pipeline, completamos primero el entrenamiento del modelo más pequeño, HCX-Text-1.5B, y realizamos una evaluación de inferencia de extremo a extremo (End-to-End). Utilizamos esto como línea base (Baseline) para establecer la dirección de ajuste de los modelos de 8B y 9B.

## 3. Solución de problemas (Troubleshooting): Error al guardar checkpoints y problemas de compatibilidad del kernel del sistema

Mientras realizábamos un entrenamiento exitoso con el modelo HCX-Omni-8B, ocurrió un error crítico de interrupción del proceso durante el guardado de checkpoints (I/O) alrededor del Step 50.

### 3.1 Registros de error (Error Logs)
```python
[RANK 0] Detected kernel version 5.4.0, which is below the recommended minimum of 5.5.0; this can cause the process to hang.
...
JSONDecodeError Traceback (most recent call last)
---> 60 trainer.train(resume_from_checkpoint=...)
```

### 3.2 Análisis de la causa raíz (Root Cause Analysis)
1. **Advertencia de versión de Kernel del SO inferior:** Se confirmó que la versión del Kernel de Linux del sistema operativo host era 5.4.0, lo cual no alcanzaba la versión mínima recomendada (5.5.0) para procesos de entrenamiento distribuido (como DDP), existiendo la posibilidad de causar un bloqueo (Hang) en el proceso.
2. **Corrupción de archivos de metadatos de checkpoints:** Debido a la inestabilidad a nivel del sistema mencionada o a problemas de sincronización de I/O, los archivos de metadatos como `trainer_state.json` que el `Trainer` de Hugging Face escribe en el disco no se registraron completamente y se dañaron. Por lo tanto, durante el proceso de reanudación del entrenamiento, el analizador (Parser) no pudo leer el archivo correspondiente y devolvió un `JSONDecodeError`.

### 3.3 Solución y próximos pasos (Solution & Next Steps)
- **Confirmación del límite de recuperación de checkpoints:** Aunque está diseñado para permitir la reanudación del entrenamiento a través del argumento `resume_from_checkpoint` del `Trainer` de Hugging Face, confirmamos que es imposible cargarlo cuando el archivo JSON en sí está físicamente dañado.
- **Plan de acción:** Para la creación estable de checkpoints, ajustamos la frecuencia de guardado y adoptamos el método de revertir (Rollback) y reanudar el entrenamiento desde el estado normal más reciente anterior al checkpoint dañado. Además, en preparación para el caso de que ocurran errores frecuentes de I/O, planeamos revisar de manera adicional la actualización de la versión del kernel a nivel de infraestructura o implementar parches de compatibilidad.
```