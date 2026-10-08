---
slug: 2026-04-14-maeumjigi-10
title: "[Registro de Desarrollo Maeumjigi #10] Levantamiento de Límites de API y Reanudación de la Síntesis de Datos"
authors: [jbgih]
tags: [devlog, API-limits, datos-sintéticos, generación-datos, troubleshooting]
date: 2026-04-14
---

![Imagen de Portada](./images/01_cover.png)

El 14 de abril es el día en que reanudamos el trabajo de generación de datos sintéticos (v5), que se había detenido temporalmente desde el incidente de la bomba de facturación. Aumentamos el límite de facturación de la API (levantamos la restricción) y ejecutamos el sistema, pero una vez más, no fue fácil.

### "¡Límite de API levantado, reanude la operación!"

- **Problema**: Durante nuestro último intento de generación masiva de datos, el script se detuvo porque excedimos el límite mensual de la API.
- **Proceso**: 
  > "Proceda con el trabajo de acuerdo con v5_emotion_data_generation_commands.md"
  > "Límite de API levantado, por favor reanude la operación" (23:32)
  > "Límite de API levantado, por favor reanude la operación" (00:11)
- **Resultado**: Iniciamos sesión en la consola de la API de Claude, aumentamos el límite de facturación de manera audaz y levantamos la restricción. Instruimos repetidamente a la IA para que reanudara la generación de datos desde donde se detuvo y reiniciamos la canalización.

### Reparación de la Canalización y Automatización

- **Problema**: Se levantó el límite de la API, pero por alguna razón, no se estaban generando nuevos datos correctamente.
- **Proceso**:
  > "No se está generando nada. Por favor verifique"
  > "Cuando se complete la tarea, desconecte automáticamente la API después de verificar los resultados (se otorgan todos los permisos, por lo que no es necesario solicitarlos)"
- **Resultado**: Hicimos que la IA verificara y solucionara de forma independiente los enredos que ocurrieron en la lógica de generación. Como no podíamos estar cerca para solucionar errores cada vez, dimos una instrucción de automatización no tripulada: "Te daré todos los permisos, así que cuando la tarea esté terminada, desconecta automáticamente la API y apágate de forma segura".

![Captura de Terminal](./images/02_term.png)

Hoy fue un duro viaje de equilibrar dinero, tiempo y automatización para el preprocesamiento de datos. ¡Nos vemos en el próximo registro de desarrollo!
