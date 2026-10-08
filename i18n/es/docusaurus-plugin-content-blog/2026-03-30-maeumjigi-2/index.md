---
slug: maeumjigi-2
title: "[Registro de Desarrollo Maeumjigi #2] Planificación Inicial de la App y Pruebas"
authors: [jbgih]
tags: [devlog, IA-coding, ClaudeCode, capstone, testing]
date: 2026-03-30
---

![Imagen de Portada](./images/01_cover.png)

Este es el registro del 30 de marzo, cuando comenzamos oficialmente a desarrollar la aplicación 'Alarma de Reservas MND Convention', que fue la idea inicial para el proyecto Maeumjigi.
Basándonos en las reglas de codificación que establecimos la última vez, elaboramos un plan detallado del proyecto y sentamos las bases para el Desarrollo Guiado por Pruebas (TDD).

### Diseño de los Hitos del Proyecto

- **Problema**: Teníamos la idea de la aplicación, pero necesitábamos un plan paso a paso claro sobre cómo proceder con el desarrollo.
- **Proceso**: 
  > A Claude Code: "Por favor, proceda con el proyecto de acuerdo con Claude plan.md"
- **Resultado**: Completamos un documento de plan de proyecto detallado llamado `Claude plan.md`. Este documento detalla los objetivos de implementación para cada etapa, incluyendo el cliente Android, la estructura del servidor y el rastreo (crawling), y servirá como un hito inquebrantable al trabajar con IA.

### Creación de Páginas Web de Prueba (Fixtures)

- **Problema**: Para construir un rastreador que detecte cambios en un sitio de reservas en tiempo real, normalmente tendríamos que conectarnos continuamente al sitio web real para probarlo. Sin embargo, esto puede sobrecargar el servidor y crear un entorno de prueba inestable. Por lo tanto, era esencial contar con un entorno de simulación (mockup) donde pudiéramos probar de forma segura y libre sin conexión.
- **Proceso**:
  > A Claude Code: "continue"
- **Resultado**: La IA determinó de forma independiente y creó a la perfección los datos HTML de páginas web falsas (Fixture) necesarios para las pruebas de frontend y backend. Al generar de forma precisa `sample_page.html` (estado de reservas llenas) y `sample_page_changed.html` (estado disponible debido a cancelaciones), se sentaron unas bases sólidas para probar de forma rápida y segura si el código del rastreador del servidor detecta con normalidad los cambios en los elementos DOM HTML.

![Captura de Terminal](./images/02_term.png)

Hoy fue un día para vislumbrar verdaderamente la belleza del 'desarrollo automatizado impulsado por IA', donde en lugar de instrucciones paso a paso humanas, simplemente le dijimos a la IA que "procediera de acuerdo con el plan", y ella desglosó los hitos de forma independiente y creó los datos de prueba y la documentación necesarios.
¡Por favor, sigue observando nuestro duro (?) viaje para ver cómo este sencillo proyecto de app de alarma se transforma en un enorme proyecto final basado en Aprendizaje Profundo y Modelos de Lenguaje Grandes (LLM)!
