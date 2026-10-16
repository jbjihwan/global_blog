```markdown
---
slug: maeumjigi-2
title: "[Diario de desarrollo Capstone Maeumjigi #2] Concreción y pruebas del diseño inicial de la aplicación de alarmas"
authors: [jbgih]
tags: [Diario de desarrollo, Codificación de Inteligencia Artificial (IA), ClaudeCode, Diseño Capstone, Planificación de proyectos, Código de prueba]
date: 2026-03-30
---

Este es el registro del 30 de marzo, cuando comenzamos el desarrollo de la aplicación 'Alarma de reservas del Centro de Convenciones de Defensa', que fue el plan inicial del proyecto Maeumjigi. Nos centramos en diseñar la arquitectura general del sistema y los hitos de implementación detallados en función de convenciones de codificación predefinidas, y en construir un entorno de Mock para un ciclo de TDD (Test-Driven Development) fluido.

## 📌 Tech Stack
- **AI Coding Agent**: Claude Code
- **Testing**: HTML Fixture-based Mocking

## 🚀 Características e Hitos

### 1. Diseño y documentación de los hitos del proyecto
Los requisitos de la aplicación estaban definidos, pero existía el problema de que la estructura de comunicación entre el cliente Android y el servidor backend, y el orden de implementación del módulo del rastreador (crawler), no estaban claros. Para resolver esto, indicamos al agente de inteligencia artificial (IA) Claude Code que procediera de forma autónoma con el proyecto basándose en `plan.md`.

Como resultado, se generó un documento de hitos detallado llamado `Claude plan.md`. En este documento, se especifican paso a paso los objetivos de implementación para cada dominio, como el flujo UI/UX del cliente Android, las especificaciones de la API del servidor y la estrategia de rastreo del sitio objetivo. Esto se utilizará como un hito clave para mantener el contexto durante el proceso futuro de programación en pareja (pair programming) con la IA.

### 2. Construcción de Fixtures para la validación del rastreador basada en TDD
Antes de implementar el módulo del rastreador que realiza un seguimiento de los cambios en el estado de las reservas en tiempo real, era necesario construir un entorno de pruebas.

#### 🚨 Solución de problemas: Inestabilidad en las pruebas del rastreador
- **Problema**: Enviar solicitudes continuamente al sitio web objetivo que está en servicio activo para probar la lógica de análisis del DOM del rastreador genera una carga innecesaria en el servidor objetivo, y es una causa de pruebas inestables (Flaky Tests) donde los resultados varían según el estado de la red.
- **Solución**: Eliminamos las dependencias externas y construimos un entorno de Mockup (Fixture) que opera de manera determinista en un entorno offline.
  
A través del comando `continue` en Claude Code, le indicamos que generara automáticamente datos HTML simulados para las pruebas de frontend y backend. En consecuencia, se construyeron Fixtures HTML precisos que representan los siguientes dos estados:
- `sample_page.html`: Estructura DOM de un estado donde las reservas están llenas y no hay asientos disponibles.
- `sample_page_changed.html`: Estructura DOM de un estado donde se ha producido una cancelación y el botón de reserva está activado.

Utilizando estos Fixtures, sentamos las bases de pruebas unitarias que permiten verificar de forma rápida y estable si el código del rastreador en el lado del servidor detecta con precisión el cambio de estado (reserva no disponible -> reserva disponible) del HTML DOM Tree y desencadena eventos de notificación, sin necesidad de comunicación de red real.

---

El trabajo de hoy es un ejemplo que demuestra la eficiencia de un flujo de trabajo de desarrollo impulsado por IA, automatizando desde la división de hitos hasta la generación de recursos para el código de prueba, otorgando al agente una planificación general y autonomía en lugar de que el desarrollador escriba directamente cada detalle de la lógica de implementación. En la próxima publicación, cubriremos cómo la arquitectura inicialmente simple de la aplicación de alarmas evolucionará a un proyecto Capstone a gran escala basado en aprendizaje profundo (Deep Learning) y LLM.
```