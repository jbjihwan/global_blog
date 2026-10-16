---
slug: 2026-06-27-vision-anpr-3
title: "[Vision AI] Detección Jerárquica de Objetos: ROI de Vehículo YOLOv3, Detector de Matrículas YOLOv5 y Seguimiento CSRT (#3)"
authors: [jbgih]
tags: [computer-vision, anpr, yolo, csrt-tracker, object-detection, opencv, python]
date: 2026-06-27
project: anpr_vision
description: "Estrategia jerárquica en dos etapas: detección general de vehículos con YOLOv3, localización precisa con YOLOv5 y seguimiento por filtro de correlación CSRT."
keywords: ["Detección de Matrículas YOLOv5", "Rastreador CSRT OpenCV", "Detección Jerárquica de Objetos", "Seguimiento Tiempo Real 50FPS", "Localización ROI Vehículo"]
---

![Localización de Matrícula con YOLOv5](./images/01_plate_localization.png)

> 📌 **Key Takeaways (Puntos Clave)**
> - **Problema**: Detectar matrículas diminutas (30x15 píxeles) en todo el fotograma de 640x480 provoca falsos positivos con carteles viales y reduce el rendimiento a menos de 10 FPS.
> - **Solución**: Diseñamos una arquitectura en dos etapas (YOLOv3 para vehículos -> YOLOv5 solo en el ROI del vehículo) combinada con el rastreador CSRT cada 15 fotogramas.
> - **Resultado**: Eliminación del 98% de falsos positivos y reducción del 80% en carga de GPU, manteniendo más de 50 FPS.

{/* truncate */}

---

## 1. Detección Jerárquica en Dos Etapas

```python
vehicle_boxes = detect_vehicles_yolov3(frame, net=vehicle_net, conf_thresh=0.5)

for box in vehicle_boxes:
    x1, y1, x2, y2 = box
    vehicle_roi = frame[y1:y2, x1:x2]
    plate_boxes = plate_model(vehicle_roi)
    for pbox in plate_boxes:
        px1, py1, px2, py2 = pbox
        global_plate_box = [x1 + px1, y1 + py1, x1 + px2, y1 + py2]
```

---

## 2. Seguimiento en Tiempo Real con CSRT

![Seguimiento Continuo con OpenCV CSRT](./images/02_csrt_tracking.png)

---

## 3. Próxima Entrega

En la Entrega #4, abordaremos la **superresolución profunda EDSR_x4** y el **apilamiento multifotograma** para recuperar contornos alfanuméricos nítidos.
