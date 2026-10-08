---
slug: 2026-04-09-maeumjigi-9
title: "[Registro de Desarrollo Maeumjigi #9] Lucha contra Errores en el Fine-Tuning de Llama 3.1 y Presentación de la Semana 6"
authors: [jbgih]
tags: [devlog, Llama3.1, fine-tuning, troubleshooting, PPT-generation, ERD]
date: 2026-04-09
---

![Imagen de Portada](./images/01_cover.png)

El 9 de abril, usando el cuaderno de Colab que completamos ayer de manera ambiciosa, finalmente intentamos el primer entrenamiento (fine-tuning) de nuestro modelo de IA (Llama 3.1). Sin embargo, la realidad no fue tan fácil y tuvimos que enfrentar numerosos errores. También fue un día difícil ya que tuvimos que crear simultáneamente los materiales de presentación para la sexta semana.

### La Lucha Interminable con los Errores de Fine-Tuning en Colab

- **Problema**: Tan pronto como ejecutamos el cuaderno creado ayer, surgieron varios errores.
- **Proceso**: 
  > "¿Por qué ocurre un error durante el fine-tuning M1 en llama31_finetuning_colab (3).ipynb?"
  > "El resultado ejecutado contiene el eos_token. ¿Por qué ocurre este problema?"
- **Resultado**: Ocurrieron una serie de problemas, como que el token especial (`eos_token`) no se procesaba correctamente y problemas de desbordamiento de memoria. Repetimos el proceso de copiar y pegar todo el registro de errores a Claude para obtener soluciones y modificar el código varias veces. Finalmente, el entrenamiento se completó y pudimos extraer un gráfico de resultados significativo.

### Creación de Presentaciones (PPT) del Asistente de IA

- **Problema**: Mientras nos quedábamos despiertos toda la noche entrenando el modelo, tuvimos que crear un PPT sobre el progreso del frontend y la base de datos para la presentación de la próxima semana.
- **Proceso**:
  > "Capstone_Week6_Frontend.pptx es una colección de imágenes que introducen el resumen hasta ahora. Por favor, utilícelo para crear una presentación para el progreso de esta semana."
  > "Exprese las tablas del diseño de la base de datos para que se puedan ver las relaciones, refiriéndose a las tablas implementadas en el backend... La tabla es demasiado grande y desordenada. Coloque la tabla User en el centro."
- **Resultado**: Sorprendentemente, la IA unió las capturas de pantalla del frontend para crear un guión de presentación y un esqueleto de diapositiva. Incluso cuando le pedí persistentemente que dibujara un complejo diagrama ERD de base de datos basado en el código backend, organizó y explicó perfectamente las relaciones de la base de datos.

![Captura de Terminal](./images/02_term.png)

Hoy fue un día para sentir la emoción de ajustar directamente el último modelo de lenguaje Llama 3.1 con mis propias manos (y el cerebro de la IA). ¡Revelaremos los resultados de las pruebas la próxima vez!
