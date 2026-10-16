Here is the translated blog post in Spanish. I have preserved the markdown formatting, frontmatter structure, and image paths as requested.

```markdown
---
slug: 2026-05-13-maeumjigi-18
title: "[Diario de Desarrollo Capstone Maeumjigi #18] Expansión de Tokens de Inferencia y Comparación de Resultados del Segundo Fine-Tuning"
authors: [jbgih]
tags: [diario de desarrollo, fine-tuning, inferencia, max_new_tokens, empatía, diseño capstone]
date: 2026-05-13
---

## 1. Overview & Tech Stack

Después de corregir todos los errores de *hardcoding* identificados ayer en el código de inferencia (Inference), hemos reanudado formalmente las pruebas de inferencia para el modelo del segundo *Fine-Tuning*. Esta publicación es un registro de desarrollo sobre el proceso de resolución de problemas causados por las restricciones de inferencia del modelo y el análisis de los resultados del ajuste de hiperparámetros de LoRA.

- **Base Model**: Llama33-70B
- **Fine-Tuning Method**: PEFT (LoRA)
- **Framework**: PyTorch, Hugging Face Transformers

## 2. Troubleshooting: Degradación de la calidad de respuesta debido a restricciones de decodificación

### Issue
Al analizar los resultados del pipeline de inferencia, se observó que el modelo `Llama33-70B_a8` devolvía respuestas excesivamente cortas, generando textos rígidos que no demostraban suficiente capacidad de empatía.

### Cause Analysis
La causa radicaba en la configuración de las restricciones de decodificación (Decoding) del pipeline de generación de texto. El cuello de botella (Bottleneck) no era un problema de capacidad de comprensión del lenguaje del modelo de inteligencia artificial (IA) en sí, sino que los valores de `max_seq_length` y `max_new_tokens`, que determinan el número máximo de tokens que se pueden generar, estaban limitados a un nivel demasiado bajo. Antes de que el modelo pudiera desarrollar un contexto complejo y profundo, chocaba con el límite de tokens y la generación terminaba abruptamente (Truncation), lo que provocaba la salida de oraciones fragmentadas y secas.

## 3. Solution: Optimización de `max_new_tokens` basada en el monitoreo de VRAM

### Implementation
Para una inferencia estable, era necesario aumentar la longitud de los tokens y, al mismo tiempo, evitar fugas de memoria de la GPU o errores de OOM (Out of Memory). Como resultado del monitoreo del espacio libre de VRAM en tiempo real, se confirmaron aproximadamente 39.8 GB de memoria disponible, una cifra suficiente para expandir la ventana de contexto, incluso considerando el KV Cache y los pesos del modelo.

Basándonos en esto, incrementamos audazmente el valor de `max_new_tokens` en el pipeline de generación de texto a `384`.

```text
[Antes del cambio] "Debe ser muy difícil que tenga esos pensamientos. Es importante hablar con un profesional."
[Después del cambio] "Debe ser muy difícil que tenga esos pensamientos. Sin embargo, tener esos pensamientos no significa que sea débil, sino que es una señal de que está soportando demasiada carga en este momento. Le recomiendo que se tome el tiempo para desentrañar estas emociones con un profesional."
```

### Result
Al proporcionarle una asignación de tokens de generación más amplia, el modelo comenzó a mantener el contexto hasta el final, generando textos de empatía mucho más profundos y fluidos. Fue el momento en que se demostró que el modelo no carecía de capacidad por sí mismo, sino que había estado reteniendo sus palabras atrapado en un espacio de tokens reducido.

## 4. Features & Analysis: Comparación de hiperparámetros `alpha` de LoRA (a=8 vs a=16)

Visualizamos y analizamos los cambios en el rendimiento del modelo y los patrones de aprendizaje según el valor del hiperparámetro de escalado de LoRA, `alpha`, que era el objetivo principal del segundo *Fine-Tuning*.

Extrajimos los datos de registro de los modelos `alpha=8` y `alpha=16` en un entorno controlado con el parámetro `rank(r)` fijado en `16`. A través de esto, pudimos cuantificar las diferencias en el momento en que cada modelo causa sobreajuste (Overfitting) en el conjunto de datos de validación a medida que avanza el aprendizaje y la calidad de generación final.

![Comparación Alpha Dominio Daily](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/.ipynb_checkpoints/05_alpha_comparison_daily-checkpoint.png)

![Comparación Alpha Dominio Common](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/.ipynb_checkpoints/05_alpha_comparison_common-checkpoint.png)

A través de ambos gráficos, pudimos observar claramente el impacto de los cambios de hiperparámetros en la convergencia del modelo y la estabilidad del aprendizaje, y aseguramos indicadores objetivos para seleccionar el valor óptimo de `alpha`.

## 5. Conclusion

Mediante el ajuste correcto del hiperparámetro (`alpha`) y la obtención de un entorno de inferencia holgado (`max_new_tokens`), el modelo ajustado (*fine-tuned*) demostró con éxito el nivel de capacidad de interacción emocional de un "verdadero guardián del corazón" (*Maeumjigi*), como se planeó inicialmente. Sobre la base de esta optimización de inferencia y los resultados de la comparación de modelos, se espera que podamos proceder sin problemas con la próxima presentación intermedia.
```