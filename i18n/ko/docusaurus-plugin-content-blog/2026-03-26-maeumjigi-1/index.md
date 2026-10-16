```markdown
---
slug: maeumjigi-1
title: "[Registro de Desarrollo Capstone de Maeumjigi #1] El primer inicio y planificación del proyecto"
authors: [jbgih]
tags: [개발일지, 인공지능(AI)코딩, ClaudeCode, 캡스톤디자인, 프로젝트기획]
date: 2026-03-26
---

Este post es un registro de desarrollo (Dev Log) sobre la planificación inicial y la fase de diseño de arquitectura del proyecto capstone 'Maeumjigi' realizado el 26 de marzo de 2026. Cubre el diseño de la estructura del sistema de la aplicación inicial basada en Android y el proceso de construcción de un entorno de generación de código basado en inteligencia artificial (IA), antes de que evolucionara al proyecto actual de ajuste fino (fine-tuning) de un modelo de lenguaje grande (LLM).

## 1. Objetivos de implementación y características principales (Features)

El objetivo principal del proyecto inicial era el desarrollo de una aplicación para Android que monitorizara el estado de las reservas en tiempo real de un sitio web específico (Convención de Defensa Nacional) y detectara cambios de estado.

- **Target System**: Sistema de reservas del sitio web de la Convención de Defensa Nacional
- **Core Feature**: Un sistema de detección de estado basado en rastreo (crawling) que envía inmediatamente una notificación push al dispositivo del usuario cuando un horario no disponible cambia al estado 'disponible para reserva'.
- **Architecture Draft**: Planificación de un planificador de rastreo web (crawler scheduler) para verificar el estado periódicamente y la estructura de integración con el cliente móvil (Android).

## 2. Configuración del entorno de desarrollo y stack tecnológico (Tech Stack)

Para maximizar la productividad inicial del proyecto, integramos Claude Code, un asistente de codificación de IA basado en CLI, en nuestro flujo de trabajo de desarrollo.

- **AI Agent**: Claude Code
- **Integration Test**: Para verificar la capacidad de procesamiento de lenguaje natural (NLP) en coreano y la comprensión del contexto del agente, probamos la capacidad de respuesta del sistema con un prompt inicial como `"¿Entiendes coreano?"`. Luego, introdujimos un prompt específico: `"Quiero crear una aplicación que envíe una alarma cuando cambie a 'disponible para reserva'. Por favor, crea un plan paso a paso para construir esto"`, para inducir al agente a diseñar la arquitectura inicial y la hoja de ruta de desarrollo (roadmap).

## 3. Problemas y soluciones (Troubleshooting)

### Problem: Pérdida de contexto e inconsistencia en la generación automática masiva de código
Durante el proceso de desarrollo utilizando el agente, se anticipó que si se generaban automáticamente cantidades masivas de código, el agente podría olvidar los objetivos principales del proyecto o desviarse de las convenciones de codificación, causando problemas de alucinación (Hallucination) y fragmentación del código.

### Solution: Establecimiento de una estructura de control del agente basada en documentación de reglas declarativas (Rule-based Documentation)
Para controlar el radio de acción del agente y mantener forzosamente el contexto del proyecto, definimos documentos de reglas globales a nivel de repositorio para que funcionaran como prompts del sistema (system prompts).

- `Claude.md`: El documento maestro que especifica la lógica de negocio general y los requisitos del sistema del proyecto.
- `CLAUDE_coding_rule.md`: Un documento de reglas a nivel de análisis estático que el agente de IA debe cumplir estrictamente al escribir código, como convenciones de nomenclatura (naming conventions), estructura de directorios y manejo de excepciones.

Como resultado, pudimos establecer con éxito restricciones (Constraints) para que el agente dependiera de las reglas de los documentos de referencia durante el desarrollo, como se vio en respuestas como *"No recibiré alarmas... Construiré la aplicación de Android de acuerdo con Claude.md"*.

## 4. Dirección futura del proyecto

La planificación inicial de la aplicación de alarmas establecida este día sufrió un pivote (Pivot) de acuerdo con los cambios en los requisitos del proyecto, marcando un gran cambio de dirección hacia el proyecto actual de 'Maeumjigi', que involucra el ajuste fino (fine-tuning) de Llama y datos sintéticos de texto a gran escala (Synthetic Data).

Aunque el dominio del producto ha cambiado, las reglas de control del agente basadas en documentos y el pipeline de ingeniería de prompts establecidos inicialmente se convirtieron en una base de arquitectura central para procesar cantidades masivas de datos de texto y automatizar el proceso de entrenamiento de modelos más adelante. Junto con los cambios en la planificación inicial, los próximos posts cubrirán pipelines de entrenamiento de modelos específicos y técnicas de síntesis de datos.
```