Here is the Spanish translation of your technical blog post, maintaining the markdown formatting, frontmatter structure, and image paths as requested:

```markdown
---
slug: 2026-05-03-maeumjigi-12
title: "[Diario de Desarrollo Capstone Maumjigi #12] Fine-tuning de Modelos Masivos 70B y la Batalla con la Memoria GPU (OOM)"
authors: [jbgih]
tags: [개발일지, 파인튜닝, Llama3.3-70B, DeepSeek-R1-70B, OOM, 트러블슈팅, GPU]
date: 2026-05-03
---

Después de haber completado la validación del pipeline de fine-tuning y la evaluación básica de rendimiento utilizando un modelo 8B, intentamos realizar el fine-tuning de modelos de lenguaje masivos a escala de 70B (70 mil millones de parámetros) para mejorar la calidad del servicio. Los modelos objetivo son **Llama 3.3 70B** y **DeepSeek-R1 70B**. Sin embargo, debido al enorme tamaño de los parámetros, nos enfrentamos a cuellos de botella extremos en los recursos de hardware, tal como se esperaba.

En este artículo, documentaremos los problemas de OOM (Out of Memory) que surgieron durante el proceso de fine-tuning de los modelos de inteligencia artificial (IA) 70B, y el proceso de troubleshooting que intentamos para superarlos.

## ⚠️ Troubleshooting: Problema de OOM en el Fine-tuning del Modelo 70B

### 1. Situación del Problema (Problem)
Tan pronto como desplegamos el script de fine-tuning del modelo 70B en el servidor y comenzamos el entrenamiento, ocurrió un error de fallo en la asignación de memoria GPU (CUDA Out of Memory).
Como resultado de analizar los registros a través de `train_log.jsonl`, confirmamos que la capacidad de VRAM requerida por los pesos del modelo (Weights), los estados del optimizador (Optimizer States) y los gradientes (Gradients) superaba la capacidad física del servidor, forzando la terminación del entrenamiento en sus etapas más tempranas.

### 2. Análisis y Primer Enfoque (Analysis)
Con la configuración predeterminada, ni siquiera era posible cargar completamente el modelo 70B en la memoria. Como resultado de monitorear el estado de la VRAM de la GPU a través de `nvitop`, el uso se mantuvo continuamente en 100%, alcanzando su estado MAX. 
En primer lugar, intentamos optimizar la memoria limitando de forma extrema los hiperparámetros relacionados con el entrenamiento y la longitud de la secuencia de entrada para reducir la ocupación de la VRAM.

## 🛠️ Proceso de Resolución (Solution & Parameter Tuning)

Para asegurar memoria disponible, modificamos drásticamente la configuración de `ft_configs.yaml` y el script de entrenamiento de la siguiente manera.

**1. Optimización de Early Stopping y Checkpoints**
Ajustamos los ciclos de evaluación y guardado para reducir los cuellos de botella innecesarios de E/S y asegurar una gestión estable de los recursos.
- `save_steps = 50`: Disminución de la carga de E/S aumentando el ciclo de guardado de los checkpoints.
- `save_total_limit = 10`: Limitación de la cantidad de checkpoints mantenidos para gestionar la capacidad de almacenamiento y prevenir fugas de memoria.
- `eval_steps = 50`: Sincronización de los pasos de evaluación con los pasos de guardado.
- `patience = 10`: Implementación de una condición de Early Stopping para detener prematuramente los cálculos innecesarios de la GPU si no hay mejora en el rendimiento del modelo.

**2. Reducción de la Ventana de Contexto (Context Window)**
Para reducir la complejidad de memoria según la longitud de la secuencia ($O(N^2)$) que ocurre durante el cálculo del mecanismo de Atención (Attention), redujimos drásticamente la longitud del contexto procesado a la vez.
- `max_seq_length = 512`: Limitación de la longitud máxima de secuencia a 512 tokens para ambos modelos, Llama 3.3 70B y DeepSeek-R1 70B.

## 📊 Resultados y Limitaciones (Result & Limitations)

Reanudamos el fine-tuning modificando la configuración como se indicó anteriormente, pero el monitoreo con `nvitop` mostró que la VRAM todavía estaba al límite y sobrecargada. 
Superamos el error de OOM justo después de comenzar, pero a medida que se acumulaba la presión sobre la memoria, se repitió un fenómeno fatal en el que el proceso se congelaba por completo (Hang) o entraba en un punto muerto (Deadlock) en el rango de los pasos de entrenamiento de 100 a 150. 

Como resultado, confirmamos que el enfoque de soft tuning simple de ajustar los hiperparámetros y la longitud de la secuencia era insuficiente para domar a una bestia tan masiva como la de 70B.

## 🚀 Próximos Pasos (Next Steps)

Para superar las limitaciones físicas de la VRAM y tener éxito en el fine-tuning del modelo 70B, en la siguiente etapa planeamos introducir técnicas de optimización de memoria y un Fine-Tuning Eficiente en Parámetros (PEFT) en toda regla.

- **Cuantización (Quantization)**: Planeamos reducir drásticamente el impacto (Footprint) que ocupa el modelo base en la VRAM aplicando cuantización de 4 bits u 8 bits (ej. bitsandbytes, AWQ, GPTQ).
- **LoRA / QLoRA**: Debemos aplicar la técnica de congelar todos los pesos del modelo y entrenar solo una pequeña matriz de adaptador de bajo rango (Low-Rank Adapter) para minimizar el uso de memoria del optimizador.
- **Gradient Checkpointing**: Planeamos activar una opción de optimización que intercambia (trade-off) el uso de VRAM con el volumen de cálculo al no almacenar todos los valores de activación (Activation) intermedios en la memoria durante la propagación hacia adelante (Forward Pass), sino recalculándolos cuando sean necesarios durante la retropropagación (Backpropagation). 

Se espera una batalla interminable con los registros de errores, pero aplicando las técnicas anteriores, completaremos el entrenamiento del modelo 70B incluso con recursos limitados.
```