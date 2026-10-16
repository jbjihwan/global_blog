---
slug: 2026-06-25-vision-anpr-1
title: "[Vision AI] Detección de Invasión de Carril en Caja Negra y ANPR con Superresolución: Pipeline de 6 Etapas y Desafíos en Tiempo Real (#1)"
authors: [jbgih]
tags: [computer-vision, anpr, object-detection, super-resolution, opencv, deep-learning, python]
date: 2026-06-25
project: anpr_vision
description: "Diseño de un pipeline de visión de 6 etapas que combina detección dinámica de carril, métricas de invasión IoU, detección de matrículas YOLOv5, superresolución EDSR y votación OCR."
---

![Diagrama del Pipeline ANPR de 6 Etapas](./images/01_pipeline_diagram.png)

> 📌 **Key Takeaways (Puntos Clave)**
> - **Problema**: Las grabaciones de baja resolución de cámaras de tablero sufren vibraciones, contraluces y desenfoque de movimiento, lo que hace que el reconocimiento de matrículas y el monitoreo de invasión de carril fallen con frecuencia.
> - **Solución**: Diseñamos una arquitectura desacoplada de 6 etapas: extracción de carril Canny/Hough -> detección de vehículos YOLOv3 -> IoU de invasión -> localización de matrícula YOLOv5 -> superresolución EDSR_x4 -> votación temporal EasyOCR.
> - **Resultado**: Construimos un pipeline en Python de alto rendimiento que mantiene más de 30 FPS identificando con precisión matrículas infractoras bajo condiciones ópticas severas.

{/* truncate */}

---

## 1. Contexto del Proyecto: Por qué la Visión en Dashcams es Difícil

En sistemas de transporte inteligente (ITS), la **detección en tiempo real de invasión de carril y el reconocimiento automático de matrículas (ANPR)** son desafíos esenciales. Las grabaciones reales presentan barreras ópticas críticas:

1. **Baja Resolución Extrema**: La matrícula del vehículo objetivo a menudo ocupa apenas 30x15 a 50x25 píxeles dentro de un fotograma de 640x480.
2. **Vibración de Calzada y Distorsión de Perspectiva**: Las irregularidades del asfalto deforman las líneas viales rectas.
3. **Cuellos de Botella de Cómputo**: Aplicar modelos masivos en cada fotograma completo colapsa la tasa de FPS.

---

## 2. Arquitectura Jerárquica de 6 Etapas

```mermaid
flowchart TD
    Raw["Fotograma Dashcam 640x480"] --> L1["Etapa 1: Extracción Dinámica de Carril Canny + Hough"]
    Raw --> L2["Etapa 2: Detección Rápida de Vehículos YOLOv3-tiny"]
    L1 & L2 --> L3["Etapa 3: Métrica IoU entre Base del Vehículo y Polígono de Carril"]
    L3 -- Si Ocurre Invasión --> L4["Etapa 4: Detección Localizada de Matrícula YOLOv5"]
    L4 --> L5["Etapa 5: Superresolución Profunda 4x con EDSR_x4"]
    L5 --> L6["Etapa 6: EasyOCR + Regex + Votación Temporal por Mayoría"]
    L6 --> Result["Matrícula Final Confirmada: 64가1511"]
```

![Salida de Detección y Reconocimiento ANPR](./images/02_final_result.png)

---

## 3. Parámetros Principales del Sistema (`CONFIG`)

```python
CONFIG = {
    "output_width": 640,
    "output_height": 480,
    "conf_threshold_vehicle": 0.5,
    "nms_threshold_vehicle": 0.4,
    "min_vehicle_w": 70,
    "min_vehicle_h": 70,
    "lane_iou_threshold": 0.05,
    "detection_interval": 15,
    "min_plate_area_for_ocr": 1200,
    "plate_history_size": 7,
    "plate_confirm_threshold": 3,
    "sr_model": "EDSR_x4.pb",
    "yolo_plate_model": "lp_det.pt"
}
```

---

## 4. Próxima Entrega

En la Entrega #2, exploraremos a fondo las matemáticas de la **transformada probabilística de Hough, el filtrado de pendientes** y el **criterio geométrico de invasión basado en IoU**.
