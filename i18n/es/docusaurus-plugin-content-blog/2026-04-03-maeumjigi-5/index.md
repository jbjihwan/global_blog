---
slug: 2026-04-03-maeumjigi-5
title: "[Registro de Desarrollo Maeumjigi #5] Purificando 100,000 Datos de Emociones y la Presión de los Costos de API"
authors: [jbgih]
tags: [devlog, data-cleaning, ClaudeAPI, clasificación-emociones, Llama3.1, api-cost]
date: 2026-04-03
---

![Imagen de Portada](./images/01_cover.png)

Este es el registro del 3 de abril, el día en que comenzamos en serio la tarea de refinar los datos de conversación de entrenamiento para introducirlos en el modelo de aprendizaje profundo (Llama 3.1).
También fue el día en que ejecutamos una canalización masiva que hace que la IA lea el texto y juzgue la emoción por su cuenta.

### Reclasificación de Emociones de Datos (v3 -> v4)

- **Problema**: El etiquetado de emociones del conjunto de datos existente no se alineaba perfectamente con nuestros objetivos de asesoramiento psicológico. De un total de 1 millón de datos, necesitábamos filtrar solo los significativos y mapear con precisión sus emociones.
- **Proceso**: 
  > "El alcance es el millón entero... Porque Claude leerá la conversación y mapeará directamente la emoción. Estamos filtrando solo lo que cae bajo nuestra clasificación de emociones y excluyendo el resto."
- **Resultado**: Establecimos `v4_plan.md` y comenzamos el trabajo. Apuntando inicialmente a 100,000 líneas de datos, escribimos y ejecutamos un script que integra la API de Claude para comprender el contexto de la conversación y reclasificar las emociones.

### El Horror de la Facturación de la API LLM

- **Problema**: Al lanzar cantidades masivas de datos de texto a un LLM (Claude) para su evaluación, el uso de la API (recuento de tokens) aumentó exponencialmente.
- **Proceso**:
  > "Ya estoy usando Claude con una suscripción Pro, ¿necesito una API separada?"
  > "¿Hay alguna manera de usar Claude Code en lugar de la API de Anthropic? La facturación es pesada."
  > "El costo real fue de $10.27."
- **Resultado**: Nos dimos cuenta dolorosamente de que la API de Anthropic, llamada por el script de Python para el procesamiento por lotes automatizado, se factura según el uso, separado de la suscripción Pro. Procesar 100,000 líneas de prueba nos costó instantáneamente unos $10.27. Al darnos cuenta de que procesar el millón de registros costaría una fortuna, fue un día en el que aprendimos de primera mano la importancia de la optimización del modelo y el muestreo de datos.

![Captura de Terminal](./images/02_term.png)

Hoy fue el día en que nos golpeamos contra el muro realista de los 'costos computacionales'.
Aunque logramos obtener datos refinados de alta calidad, fue una experiencia valiosa que nos dejó contemplando cómo equilibrar el costo y la eficiencia a medida que avanzamos con el fine-tuning.
