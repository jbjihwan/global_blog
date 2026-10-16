```markdown
---
slug: 2026-06-18-maeumjigi-23
title: "[Diario de desarrollo Capstone Maeumjigi #23] Introducción de Safety Wrapper y presentación final del primer semestre"
authors: [jbgih]
tags: [Diario de desarrollo, Fine-Tuning, Safety Wrapper, Nube, Presentación final, Diseño Capstone]
date: 2026-06-18
---

## 1. Selección del 4º modelo de fine-tuning e introducción de la arquitectura Safety Wrapper

### 1.1. Derivación de la proporción de datos óptima: Adopción del modelo mixto 2:1
Como resultado del 4º experimento de Fine-Tuning, un modelo de lenguaje grande (LLM) configurado con una proporción de 2:1 de conjuntos de datos de 'diálogo emocional' y 'diálogo cotidiano' registró los índices de rendimiento más altos en términos de comprensión de la intención del enunciado del usuario y capacidad de empatía. En consecuencia, este modelo fue adoptado finalmente como el modelo de inferencia principal para el servicio Maeumjigi.

### 1.2. Solución de problemas (Troubleshooting): Alucinación (Hallucination) y límites en la respuesta a enunciados de alto riesgo
Debido a la naturaleza del dominio del chatbot de prevención del suicidio y asesoramiento psicológico, las alucinaciones o las respuestas inapropiadas del modelo de inteligencia artificial (IA) pueden llevar a resultados fatales. Con la estructura exclusiva del LLM principal, era difícil garantizar siempre una respuesta segura y estandarizada a los enunciados que contenían intenciones suicidas (Active Suicidality) de usuarios en grupos de alto riesgo de depresión.

### 1.3. Solución (Solution): Construcción de la canalización Safety Wrapper
Para bloquear fundamentalmente estos riesgos, diseñamos y aplicamos una capa **Safety Wrapper (módulo de filtro de seguridad)** que envuelve las etapas de entrada/salida (I/O) del modelo principal.

- **Verificación de Input:** Analiza el texto de entrada del usuario para evaluar si se detectan palabras clave relacionadas con la autolesión o síntomas graves de depresión.
- **Control de Output y cambio de protocolo:** Si se determina que es una situación de alto riesgo, se omite (Bypass) el proceso normal de generación de texto del LLM, y la canalización se reconfigura para devolver inmediatamente una respuesta de seguridad codificada y orientación vinculada a expertos, basadas en el **protocolo de respuesta a crisis (Resource Inquiry Cues)** predefinido en el sistema.

## 2. Construcción de la infraestructura y revisión del rendimiento final del primer semestre

![최종 발표 슬라이드 1](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week12/_preview_slide3.png)

### 2.1. Pila tecnológica (Tech Stack): Configuración del entorno de instancia de GPU AWS EC2
Durante las vacaciones de verano, procedimos con el diseño de la infraestructura en la nube para vincular los servicios frontend/backend con el modelo y realizar pruebas de demostración.
- **Especificaciones de la instancia objetivo:** Para el servicio fluido y la aceleración del modelo, seleccionamos la instancia `g5.2xlarge` (equipada con NVIDIA A10G GPU).
- **Cálculo de costos:** Con el objetivo de un funcionamiento estable del servidor durante los próximos 5 meses, calculamos y planificamos el presupuesto de mantenimiento en la nube de AWS.

### 2.2. Integración de funciones clave de implementación (Features) y presentación final del primer semestre

![최종 발표 슬라이드 2](D:/서울과기대 컴퓨터공학과/26-1/CapDe/팀플/Week12/_preview_slide3.png)

En la presentación final del primer semestre, celebrada el 18 de junio, compartimos los resultados de las pruebas de integración de los módulos desarrollados por cada parte hasta el momento.

- **Backend:** Finalización del diseño del esquema de la base de datos (DB) basada en RDBMS e implementación de la API de paginación (Pagination) para el procesamiento de datos a gran escala.
- **Frontend:** Vista de redacción del diario emocional y optimización de la renderización del componente de la comunidad para la comunicación entre usuarios.
- **AI Model:** Aplicación del 4º modelo de fine-tuning y construcción de un sistema de diálogo seguro ininterrumpido a través de Safety Wrapper.

El diseño de la arquitectura y la validación del modelo durante el primer semestre concluyeron con éxito. Completaremos la implementación (Deployment) y vinculación del servidor en la nube durante las vacaciones, y en el segundo semestre, mejoraremos la estabilidad del sistema para iniciar la demostración del servicio a gran escala.
```