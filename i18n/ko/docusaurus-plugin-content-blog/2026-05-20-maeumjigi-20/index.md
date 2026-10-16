Aquí está la traducción al español solicitada, conservando el formato markdown, la estructura del frontmatter original (con el título traducido) y respetando las etiquetas en coreano:

```markdown
---
slug: 2026-05-20-maeumjigi-20
title: "[Diario de desarrollo de Capstone de Maeumjigi #20] Finalización del 3er fine-tuning y mejora de funciones de backend (Base de datos (DB), Tablón de anuncios)"
authors: [jbgih]
tags: [개발일지, 파인튜닝, 백엔드, 프론트엔드, 데이터베이스, 캡스톤디자인]
date: 2026-05-20
---

Durante dos días, del 19 al 20 de mayo, trabajamos en paralelo en la construcción de la automatización de evaluación del pipeline del 3er fine-tuning (`fine_tuning_3`) y en la mejora de las funciones de backend/frontend para la integración con el servicio de la aplicación real (App).

## 1. Finalización del 3er fine-tuning (fine_tuning_3) y construcción del pipeline de automatización

Basándonos en los conocimientos de experimentos anteriores, se ha completado el entrenamiento del modelo del 3er fine-tuning, configurado aplicando los conceptos de Grafo de Conocimiento (Knowledge Graph) y Ontología (Ontology). En esta etapa, construimos un proceso de automatización de evaluación basado en scripts de shell para mejorar la eficiencia de la verificación del rendimiento del modelo.

### 1.1. Extracción y configuración automática del Best Checkpoint
Automatizamos el proceso de selección exclusiva de los pesos (Weights) que registraron la métrica de evaluación más alta (Best Eval) entre los múltiples checkpoints del modelo entrenado. Anteriormente, copiábamos los parámetros buscando en el directorio de forma manual, pero con la ayuda de un asistente de inteligencia artificial (IA), escribimos un script para extraer automáticamente y sobrescribir el checkpoint óptimo en la carpeta `adapter`.

### 1.2. Pipeline de inferencia paralela (Parallel Inference Pipeline)
Para procesar simultáneamente la inferencia y evaluación de 4 modelos Alias, escribimos el script de ejecución `run_test_20_30.sh`. A través de esto, asignamos (Dispatch) las tareas de evaluación del modelo en paralelo a un servidor en segundo plano, reduciendo drásticamente el tiempo total necesario para la evaluación.

## 2. Mejora de funciones de backend y frontend

Mientras la inferencia del modelo de lenguaje grande (LLM) se ejecutaba en segundo plano en el servidor, en el entorno local nos centramos en la integración entre el frontend y la API de backend, y en el manejo de la persistencia (Persistence) de la base de datos (DB) `mental-health`.

### 2.1. Solución de problemas: Error de autenticación (Authentication) y conexión a DB
- **Problema (Issue)**: Se produjo un bloqueo en el proceso de autenticación debido a que ocurría continuamente un error `401 Unauthorized` al realizar solicitudes de inicio de sesión del cliente.
- **Solución (Solution)**: Rastreamos el esquema y los datos de usuario ficticios de `seed_data.sql`, utilizado para la configuración inicial de datos. Verificamos el algoritmo de hash (Hashing) de la contraseña de usuario cargada en la DB, y resolvimos el problema de autenticación depurando la lógica de encriptación y emisión de tokens para que la contraseña en texto plano (ej. `Test1234!`) en los datos semilla pasara con éxito la lógica de verificación del servidor.

### 2.2. Características (Features): Implementación de la lógica de negocio central y UI/UX
Después de resolver el problema de inicio de sesión, implementamos las funciones principales que mejoran el flujo de datos y la experiencia del usuario, integrándolas en el código base (`feat: guardar chat de DB de chatbot, paginación de tablón de anuncios, agregar filtro de diario de emociones`).

- **Registro de conversaciones del chatbot LLM (DB Storage)**: Hicimos persistentes formalmente en la DB los datos de las sesiones de conversación del usuario con el modelo ajustado (fine-tuned). Gracias a esto, pudimos mantener el contexto (Context) de la conversación y gestionar el historial incluso sobre una comunicación HTTP sin estado (Stateless).
- **Paginación del tablón de anuncios de la comunidad (Pagination)**: Para evitar el retraso en la renderización y la carga de consultas al servidor que se producen al renderizar una gran cantidad de publicaciones, aplicamos paginación a la API del tablón de anuncios, optimizándola para enviar datos al cliente en fragmentos (chunks).
- **Filtrado del diario de emociones (Emotion Diary Filtering)**: Agregamos una función de filtro de consultas múltiples en el frontend para que los usuarios puedan consultar los diarios de emociones diarios que registraron, categorizados por emoción y por fecha.
```