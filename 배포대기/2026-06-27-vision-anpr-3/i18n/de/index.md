---
slug: 2026-06-27-vision-anpr-3
title: "[Vision AI] Hierarchische Objekterkennung: YOLOv3 Fahrzeug-ROI, YOLOv5 Kennzeichendetektor & CSRT-Tracking (#3)"
authors: [jbgih]
tags: [computer-vision, anpr, yolo, csrt-tracker, object-detection, opencv, python]
date: 2026-06-27
project: anpr_vision
description: "Zweistufige hierarchische Lokalisierung: Globale Fahrzeugerkennung via YOLOv3, gezielte Kennzeichen-Inferenz via YOLOv5 und CSRT-Korrelationsfilter-Tracking bei 50 FPS."
keywords: [YOLOv5 Kennzeichenerkennung, CSRT Tracker OpenCV, Hierarchische Objekterkennung, Echtzeit-Fahrzeugverfolgung, Fahrzeug ROI Lokalisierung]
---

![YOLOv5 Kennzeichen-Lokalisierung](./images/01_plate_localization.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Herausforderung**: Die Suche nach winzigen Kennzeichen (30x15 Pixel) im vollen 1080p-Frame führt zu massiven False Positives an Schildern und senkt die Inferenzrate unter 10 FPS.
> - **Lösung**: Zweistufige Hierarchie — Erst Fahrzeug finden (YOLOv3), dann Kennzeichen nur im Ausschnitt suchen (YOLOv5) und Zwischenframes mit schnellem CSRT-Tracking überbrücken.

{/* truncate */}

---

### 1. Das hierarchische Detektionsprinzip

Statt das gesamte Bild mit einem schweren neuronalen Netz nach kleinsten Mustern zu durchsuchen, nutzt das System eine stufenweise Verengung:

```mermaid
flowchart TD
    Frame[Vollbild 1920x1080] --> Step1["Schritt 1: YOLOv3 detektiert Fahrzeug-ROI (Großes Bounding Box)"]
    Step1 --> Crop[Fahrzeug-Ausschnitt isolieren]
    Crop --> Step2["Schritt 2: YOLOv5 detektiert Kennzeichen im Stoßstangenbereich"]
    Step2 --> Plate[Kennzeichen-Patch (z.B. 40x20 px)]
    Plate --> Step3["Schritt 3: CSRT Tracker übernimmt Folgebilder mit 50+ FPS"]
```

Durch das CSRT-Tracking muss das teure YOLOv5-Netzwerk nur alle 5 Frames ausgeführt werden. Die Zwischenbilder werden durch Korrelationsfilter stabil und ressourcenschonend verfolgt.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Hierarchische Verengung**: Eliminiert False Positives an Straßenschildern und Werbetafeln vollständig.
2. **5-fache Geschwindigkeitssteigerung**: CSRT-Tracking reduziert die GPU-Inferenzlast drastisch.
3. **Stabile Verfolgung**: Kennzeichen bleiben auch bei leichten Verdeckungen und Nickbewegungen im Fokus.
4. **Optimale ROI-Übergabe**: Der präzise Kennzeichenausschnitt wird direkt an die Super-Resolution-Stufe weitergeleitet.