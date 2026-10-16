```markdown
---
slug: 2026-05-17-maeumjigi-19
title: "[Diario de desarrollo Capstone de Maeumjigi #19] Automatización del informe de fine-tuning y troubleshooting de la integración de la base de datos (DB) del backend"
authors: [jbgih]
tags: [diario de desarrollo, fine-tuning, informe, backend, DB, troubleshooting, diseño capstone]
date: 2026-05-17
---

## 1. Construcción del pipeline de automatización para el análisis de resultados del segundo fine-tuning y generación de informes

### 1.1. Antecedentes de la introducción de la automatización
Durante el segundo fine-tuning (`fine_tuning_2`), se generaron los resultados de inferencia para los conjuntos de datos `common` y `daily`, junto con una gran cantidad de métricas de evaluación. Dado que consideramos ineficiente que una persona analizara y comparara manualmente las métricas de rendimiento entre múltiples modelos, las variaciones según el valor Alpha y las características de cada conjunto de datos, construimos un pipeline automatizado para la interpretación de datos y la redacción de informes utilizando inteligencia artificial (IA).

### 1.2. Informe de métricas de rendimiento del modelo y visualización (Features)
Analizamos cuantitativamente el rendimiento de cada modelo y derivamos las siguientes métricas visualizadas.

**[Métricas de evaluación del conjunto de datos Common]**
![Metric Comparison (Common)](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/common/01_metric_comparison.png)
![Improvement Pct (Common)](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/common/02_improvement_pct.png)
![Radar per Model (Common)](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/common/03_radar_per_model.png)
![Pareto Efficiency (Common)](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/common/04_pareto_efficiency.png)

**[Métricas de evaluación del conjunto de datos Daily]**
![Metric Comparison (Daily)](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/daily/01_metric_comparison.png)
![Radar per Model (Daily)](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/daily/03_radar_per_model.png)
![Pareto Efficiency (Daily)](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/daily/04_pareto_efficiency.png)

**[Análisis comparativo del valor Alpha y conjuntos de datos (Common vs Daily)]**
![Alpha Comparison (Common)](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/05_alpha_comparison_common.png)
![Alpha Comparison (Daily)](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/05_alpha_comparison_daily.png)
![Common vs Daily](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week11/fine_tuning_2/results/figures/eval/06_common_vs_daily.png)

### 1.3. Ingeniería de prompts y salida en formato Word (.docx)
- **Automatización del análisis**: Diseñamos el prompt `report_prompt.md` para inyectar los datos de las métricas de resultados anteriores y deducir automáticamente los insights basados en las ventajas y desventajas de cada modelo y los cambios en el valor Alpha.
- **Optimización del formato**: En lugar de simplemente generar texto en Markdown, modificamos las especificaciones de salida del pipeline para que el borrador final del informe se genere en formato `.docx`, cumpliendo con los requisitos de los entregables prácticos.

---

## 2. Troubleshooting de la migración de la base de datos del backend en PostgreSQL

### 2.1. Situación del problema (Troubleshooting)
Para verificar la estabilidad del sistema integrado entre los componentes del frontend y backend, restauramos el archivo de volcado `backup.sql` que contenía datos de prueba en la base de datos PostgreSQL local. Aunque el servidor se inició y la conexión de red se estableció normalmente, experimentamos un problema en el que se producía un error de acceso denegado continuamente al solicitar el inicio de sesión.
- **Error Log**: `INFO: 127.0.0.1:54446 - POST /auth/login 401 Unauthorized`

### 2.2. Análisis de causas y solución (Solution)
- **Construcción de un entorno de depuración independiente**: Para probar de forma aislada el módulo de autenticación sin pasar por todo el stack del backend (Uvicorn/FastAPI), escribimos el script `debug_login.py` para aislar el problema.
- **Verificación del algoritmo de cifrado de contraseñas**: Investigamos si había discrepancias entre los valores hash de los datos de las cuentas existentes volcadas y la configuración del algoritmo de cifrado (por ejemplo, Bcrypt) utilizado actualmente en el servidor backend local.
- **Aplicación de la solución**: Reiniciamos el servidor Uvicorn y depuramos el historial de conflictos de migración entre el middleware de autenticación y el esquema de la base de datos comparándolos y corrigiéndolos decenas de veces a través de los registros de depuración, logrando finalmente resolver el problema de autenticación `401 Unauthorized` y confirmando la emisión exitosa de la sesión.

---

## 3. Diseño de la integración del Grafo de Conocimiento (Knowledge Graph) para fortalecer la estabilidad y la fiabilidad

### 3.1. Antecedentes de la introducción (Reflexión sobre Tech Stack)
El núcleo del chatbot de prevención del suicidio es proporcionar respuestas fiables sin información inexacta ni alucinaciones (Hallucination) durante las situaciones de crisis de los usuarios. Determinamos que depender únicamente del fine-tuning de un solo modelo de lenguaje grande (LLM) dificultaba garantizar plenamente la estabilidad de la respuesta en situaciones que requieren experiencia médica y psicológica.

### 3.2. Dirección del perfeccionamiento de la arquitectura del sistema (Features)
- **Construcción de Ontología (Ontology) y Grafo de Conocimiento**: Introdujimos un diseño que estructura los manuales de asesoramiento psicológico y los protocolos de prevención del suicidio en forma de un Grafo de Conocimiento (Knowledge Graph).
- **Harness y fusión de modelos complejos**: Actualizamos el diseño del prompt `chatbot_design_prompt.md` en la dirección de controlar la precisión de las respuestas combinando los resultados de búsqueda basados en el grafo de conocimiento con los resultados generados por el modelo.

Más allá de la simple etapa de ajuste de un solo modelo, la escala del proyecto se está expandiendo con éxito a un sistema avanzado combinado con la última arquitectura RAG (Retrieval-Augmented Generation).
```