---
slug: 2026-06-28-vision-anpr-4
title: "[Vision AI] Superación de Artefactos Borrosos de Caja Negra: Superresolución Profunda (EDSR vs FSRCNN) y Apilamiento Multifotograma (#4)"
authors: [jbgih]
tags: [computer-vision, super-resolution, edsr, image-stacking, anpr, deep-learning, python]
date: 2026-06-28
project: anpr_vision
description: "Reconstrucción de parches de matrículas de baja resolución mediante superresolución 4x con EDSR y apilamiento multifotograma."
keywords: ["Superresolución EDSR", "Restauración de Matrículas Borrosas", "OpenCV dnn_superres", "Apilamiento Multifotograma", "Escalado Profundo 4x"]
---

![Resultados de Superresolución EDSR](./images/01_edsr_sr_comparison.png)

> 📌 **Key Takeaways (Puntos Clave)**
> - **Problema**: Las matrículas recortadas suelen medir menos de 40x20 píxeles; la interpolación bicúbica estándar desenfoca los trazos impidiendo el OCR.
> - **Solución**: Red residual profunda EDSR_x4 (EDSR_x4.pb) combinada con apilamiento de 3 a 5 fotogramas consecutivos.
> - **Resultado**: Densidad de píxeles cuadruplicada y precisión de EasyOCR mejorada del 32% a más del 91%.

{/* truncate */}

---

## 1. Motor de Superresolución EDSR_x4

```python
import cv2
from cv2 import dnn_superres

sr = dnn_superres.DnnSuperResImpl_create()
sr.readModel("EDSR_x4.pb")
sr.setModel("edsr", 4)
enhanced_plate = sr.upsample(plate_roi)
```

---

## 2. Apilamiento de Imágenes Multifotograma

![Comparación de Apilamiento Multifotograma](./images/02_frame_stacking.png)

Promediar parches alineados a lo largo del tiempo cancela el ruido del sensor y mejora la nitidez de los caracteres.

---

## 3. Próxima Entrega

En la Entrega #5, concluiremos con la **optimización de EasyOCR, el filtrado regex** y el **motor de votación temporal mayoritaria (evolución v01 a v11)**.

---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **La Barrera Óptica de Baja Resolución**: Las placas recortadas de cámaras de tablero miden menos de $40 \times 20$ píxeles, donde la interpolación bicúbica tradicional solo incrementa el desenfoque sin aportar nitidez.
2. **Superresolución Profunda con EDSR_x4**: Al omitir la normalización por lotes, la red residual EDSR preserva el rango dinámico de píxeles y reconstruye bordes de alta frecuencia con OpenCV `dnn_superres`.
3. **Apilamiento Temporal Multifotograma**: El alineamiento y promediado de $3 \sim 5$ fotogramas consecutivos cancela el ruido estocástico del sensor y el desenfoque por movimiento.
4. **Recuperación Masiva de Precisión OCR**: Esta combinación de superresolución y cancelación de ruido cuadruplica la densidad de píxeles, elevando el éxito de EasyOCR del 32% a más del 91%.
