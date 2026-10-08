---
slug: 2026-04-19-maeumjigi-11
title: "[Registro de Desarrollo Maeumjigi #11] Evaluación del Modelo M6 Entrenado con Datos Sintéticos (v5)"
authors: [jbgih]
tags: [devlog, datos-sintéticos, evaluación-modelo, M6, FAISS, reporte-semanal]
date: 2026-04-19
---

![Imagen de Portada](./images/01_cover.png)

El 19 de abril es el día en que evaluamos el rendimiento del modelo (M6) entrenado en el conjunto de datos sintéticos (v5) que creamos con tanto esfuerzo. ¿Valieron la pena los datos que generamos mientras soportábamos una bomba de facturación de $10?

### Un Enfrentamiento Real del Rendimiento del Modelo: M0 vs M5 vs M6

- **Problema**: Para persuadir al profesor asesor, necesitábamos un informe semanal que incluyera resultados de pruebas cuantitativas y ejemplos de comparación.
- **Proceso**: 
  > "Por favor, reescriba el informe. El punto principal es la comparación entre M5 basado en v4 y M6 basado en v5..."
  > "Al describir los resultados, incluya explicaciones con ejemplos de las diferencias entre el modelo base sin ajustar (M0) y M6."
- **Resultado**: La IA analizó los resultados de texto generados por los modelos M0, M5 y M6 y extrajo un archivo de comparación. Los resultados mostraron que el modelo base Llama 3.1 (M0) era algo torpe en el asesoramiento en coreano. Por el contrario, el modelo M6 entrenado con datos sintéticos de alta calidad (v5) dominó perfectamente el tono cálido y profesional típico de un consejero psicológico.

### El Informe Semanal de la Séptima Semana Escrito por IA (DOCX)

- **Proceso**:
  > "Por favor, escriba el informe de la séptima semana... Luego genere archivos docx para cada uno basados en los archivos md."
- **Resultado**: Con una sola instrucción, se completaron dos versiones (concisa y detallada) en un instante y se convirtieron ordenadamente en archivos de Word.

### Introducción a la Arquitectura RAG: Evaluación de FAISS DB

- **Proceso**:
  > "Realicé la construcción de FAISS_DB... Por favor evalúe nuestro plan y los resultados."
- **Resultado**: Además del fine-tuning, introdujimos una base de datos vectorial FAISS para RAG para reducir las alucinaciones al hacer referencia a conocimientos externos. Pedí a la IA que evaluara la estructura que construí y recibí comentarios positivos.

![Captura de Terminal](./images/02_term.png)

Hoy fue un día en el que todo el trabajo duro dio sus frutos. ¡La emoción de confirmar que el modelo de IA entrenado se volvió notablemente más inteligente es increíble! Con el rendimiento del modelo probado y FAISS DB integrado, el chatbot Maeumjigi está un paso más cerca.
