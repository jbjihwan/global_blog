---
slug: 2026-05-07-maeumjigi-15
title: "[Registro de Desarrollo Maeumjigi #15] Visualización de Resultados de 5 Modelos y Configuración Local"
authors: [jbgih]
tags: [devlog, fine-tuning, results-analysis, visualization, Jupyter, capstone, AI]
date: 2026-05-07
---

![Imagen de Portada](./images/01_cover.png)

El 7 de mayo sintetizamos los resultados de los 5 modelos que habíamos entrenado (Llama3.3-70B, DSR1-70B, HCX-Omni-8B, Qwen35-9B, HCX-Text-1.5B) y procedimos con la visualización a gran escala.

### Configuración Local para la Comparación de Modelos

Para revisar cómodamente los resultados en mi computadora portátil, creé un nuevo cuaderno: `31_comparison_local.ipynb`.

> "¿No puede 30_comparison.ipynb ejecutarse también en mi computadora?"

Al configurar el kernel local de Jupyter en VSCode e instalar las bibliotecas, enfrenté bloqueos del kernel y errores como `ModuleNotFoundError`. Sin embargo, los resolví paso a paso arreglando las rutas.

### Informe Completo y Gráficos

La tarea más importante fue visualizar el rendimiento de estos 5 modelos para compararlos de un vistazo. Junto con la IA, establecimos un plan y comenzamos a organizar los datos sistemáticamente.

> "¿Cuál es la diferencia entre la línea tenue y la línea gruesa? Visualice el training loss y el eval loss."

Eliminé las líneas de tendencia innecesarias de los gráficos generados por la IA, extrayendo finalmente `03_training_loss_all.png` y `04_eval_loss_all.png` que reunieron perfectamente las curvas de pérdida de todos los modelos en un solo lugar.

![Visualización de Gráficos](./images/02_graph.png)

Ahora, basándonos en estos gráficos, podemos decorar maravillosamente nuestros materiales de presentación de la próxima semana.
