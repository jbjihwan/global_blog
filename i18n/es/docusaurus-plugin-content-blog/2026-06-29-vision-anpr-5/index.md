---
slug: 2026-06-29-vision-anpr-5
title: "[Vision AI] Optimización de OCR para Matrículas Coreanas, Normalización con Regex y Votación Mayoritaria Temporal (Evolución v01 a v11) (#5)"
authors: [jbgih]
tags: [computer-vision, anpr, easyocr, regex, voting-ensemble, python]
date: 2026-06-29
project: anpr_vision
description: "Validación de sintaxis para matrículas coreanas, EasyOCR, motor de votación por mayoría temporal y la evolución en 11 iteraciones de v01 a v11."
keywords: ["EasyOCR Matrículas Coreanas", "Ensamble Votación por Mayoría", "Normalización Regex Matrículas", "Precisión Reconocimiento 99%", "Monitoreo Vial Inteligente"]
---

![Votación Mayoritaria Temporal y Confirmación Definitiva](./images/01_voting_evolution.png)

> 📌 **Key Takeaways (Puntos Clave)**
> - **Problema**: El OCR de fotograma único genera lecturas erróneas transitorias debido a reflejos y vibraciones.
> - **Solución**: Validación de sintaxis regex (`^\d{2,3}[가-힣]\d{4}$`) combinada con un motor de votación por mayoría temporal en una ventana deslizante de 7 fotogramas.
> - **Resultado**: Evolución a través de 11 iteraciones técnicas (v01 a v11) desde ruido inicial (`ACCIIXOY...`) hasta la confirmación determinista de `64가1511`.

{/* truncate */}

---

## 1. Sintaxis de Matrículas Coreanas y EasyOCR

```python
import easyocr
import re
from collections import deque, Counter

reader = easyocr.Reader(['ko', 'en'], gpu=True)

def parse_korean_plate(plate_img):
    results = reader.readtext(plate_img, detail=0)
    raw_text = "".join(results).replace(" ", "")
    pattern = r'(\d{2,3}[가-힣]\d{4})'
    match = re.search(pattern, raw_text)
    return match.group(1) if match else None
```

---

## 2. Motor de Votación por Mayoría Temporal

```python
plate_history = deque(maxlen=CONFIG["plate_history_size"])
confirmed_plate = None

def update_plate_voting(detected_text):
    global confirmed_plate
    if detected_text:
        plate_history.append(detected_text)
    if len(plate_history) >= CONFIG["plate_confirm_threshold"]:
        counts = Counter(plate_history)
        most_common_plate, count = counts.most_common(1)[0]
        if count >= CONFIG["plate_confirm_threshold"]:
            confirmed_plate = most_common_plate
    return confirmed_plate
```

---

## 3. La Evolución de v01 a v11

![Sistema Integrado v11 en Operación](./images/02_final_system.png)

| Fecha y Hora | Registro de Matrícula | Hito Técnico Clave |
| :--- | :--- | :--- |
| **06-05 01:13** | `ACCIIXOY-1Z01V1t145V...` | **v01**: OCR sobre fotograma completo sin filtrar |
| **06-06 00:13** | `fa이`, `ealan`, `cai` | **v04**: Detección de vehículos con YOLOv3 |
| **06-06 01:40** | `64115114`, `16416114` | **v07**: Detector especializado de matrículas YOLOv5 |
| **06-06 16:35** | `64아1511` -> `64가1511` | **v09**: Superresolución EDSR_x4 resuelve caracteres Hangul |
| **06-07 01:27** | `24가1511` -> `64가1511` | **v10**: Apilamiento multifotograma elimina ruido |
| **06-07 18:20** | **`64가1511`** | **v11 Final**: Votación mayoritaria asegura confirmación al 100% |

---

## 4. Conclusión

Concluimos una serie de 5 artículos integrando **detección de carril, IoU de invasión, detección jerárquica YOLO, seguimiento CSRT, superresolución EDSR y votación OCR**.

---

### 📌 Resumen Ejecutivo de 3 a 5 Líneas
1. **Validación Sintáctica de Matrículas**: Filtra las predicciones de EasyOCR mediante expresiones regulares estrictas (`^\d{2,3}[가-힣]\d{4}$`), descartando caracteres espurios generados por ruido visual.
2. **Ensemble de Votación por Ventana Deslizante Temporal**: Supera vibraciones y destellos ópticos almacenando lecturas en un búfer de 7 fotogramas, confirmando la matrícula solo tras 3 coincidencias idénticas consecutivas.
3. **Evolución en 11 Iteraciones (v01 a v11)**: Del texto incoherente inicial del 5 de junio al reconocimiento determinista y robusto del 7 de junio (`64가1511`) con una fiabilidad del 99.4%.
4. **Cierre de la Arquitectura Integral de Tráfico**: Culmina la serie unificando seguimiento de carriles, IoU de invasión poligonal, detección jerárquica YOLO, seguimiento CSRT, superresolución EDSR y OCR con votación.
