# -*- coding: utf-8 -*-
import os
import shutil

GB_ROOT = r"D:\ai\antigravity\global_blog"
STAGING_ROOT = os.path.join(GB_ROOT, "배포대기")

def save_de_post(slug, de_content):
    # 1. Save to Staging
    stage_dir = os.path.join(STAGING_ROOT, slug)
    stage_de_dir = os.path.join(stage_dir, "i18n", "de")
    os.makedirs(stage_de_dir, exist_ok=True)
    with open(os.path.join(stage_de_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(de_content.strip() + "\n")
    print(f"[STAGING OK] {slug} -> {stage_de_dir}\\index.md")

    # 2. Save to i18n/de production blog dir (ready for build)
    prod_de_dir = os.path.join(GB_ROOT, "i18n", "de", "docusaurus-plugin-content-blog", slug)
    os.makedirs(prod_de_dir, exist_ok=True)
    with open(os.path.join(prod_de_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(de_content.strip() + "\n")
    
    # 3. Copy images from blog/<slug>/images
    src_images = os.path.join(GB_ROOT, "blog", slug, "images")
    if os.path.exists(src_images):
        dst_images = os.path.join(prod_de_dir, "images")
        os.makedirs(dst_images, exist_ok=True)
        for item in os.listdir(src_images):
            s = os.path.join(src_images, item)
            d = os.path.join(dst_images, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
        print(f"[IMAGES OK] Copied images to {dst_images}")

# ==============================================================================
# ANPR 1 GERMAN
# ==============================================================================
a1_slug = "2026-06-25-vision-anpr-1"
a1_content = """---
slug: 2026-06-25-vision-anpr-1
title: "[Vision AI] Dashcam-Spurüberwachung & Super-Resolution ANPR: 6-Stufen-Pipeline & Echtzeit-Bedingungen (#1)"
authors: [jbgih]
tags: [computer-vision, anpr, object-detection, super-resolution, opencv, deep-learning, python]
date: 2026-06-25
project: anpr_vision
description: "Architektur einer 6-stufigen Computer-Vision-Pipeline: Dynamische Spurerkennung, geometrische IoU-Kriterien, YOLOv5-Kennzeichenlokalisierung, EDSR-Super-Resolution und OCR-Voting."
keywords: [ANPR Pipeline Computer Vision, Dashcam Videoanalyse Echtzeit, Fahrzeugerkennung YOLOv5, Super Resolution Kennzeichen, Intelligente Verkehrssysteme ITS]
---

![6-Stufen ANPR-Pipeline-Diagramm](./images/01_pipeline_diagram.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Herausforderung**: Dashcam-Aufnahmen bei hoher Geschwindigkeit leiden unter Vibrationen, Gegenlicht und Bewegungsunschärfe. Eine direkte OCR scheitert an niedriger Bildauflösung.
> - **Lösung**: Eine modulare 6-Stufen-Pipeline mit strikter 30-FPS-Grenze, die Spurerkennung, hierarchische YOLO-Detektion, EDSR-Super-Resolution und temporales OCR-Voting kombiniert.

{/* truncate */}

---

### 1. Die 6 Stufen der Pipeline im Überblick

```mermaid
flowchart LR
    A[1. Frame-Eingabe 30 FPS] --> B[2. Dynamische Spurerkennung]
    B --> C[3. Hierarchische Fahrzeug- & Kennzeichenerkennung]
    C --> D[4. Geometrische IoU-Spurübertrittsprüfung]
    D --> E[5. EDSR Deep Super-Resolution]
    E --> F[6. EasyOCR & Temporales Majority Voting]
```

1. **Video-Ingestion**: Dekodierung von 1080p Dashcam-Videostreams mit OpenCV und Multithreading.
2. **Spurerkennung**: Canny-Kantenerkennung, ROI-Maskierung und Hough-Linientransformation (`HoughLinesP`).
3. **Hierarchische Lokalisierung**: Grobe Fahrzeugsuche via YOLOv3, gefolgt von präziser Kennzeichenerkennung via YOLOv5.
4. **Intrusionsmetrik**: Berechnung des Schnittstellenverhältnisses (Intersection over Union, IoU) zwischen Fahrzeug-Bounding-Box und Fahrspur-Polygon.
5. **Super-Resolution**: Hochskalierung kleiner Kennzeichen-Ausschnitte (unter 40x20 Pixel) auf das 4-fache via EDSR.
6. **OCR & Konsens**: Zeichenerkennung mit EasyOCR und temporales Glätten über 11 Frames hinweg.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Modulare Architektur**: Komplexe Vision-Aufgaben werden in 6 klar getrennte Stufen unterteilt, um Engpässe isoliert zu optimieren.
2. **Echtzeitfähigkeit**: Das System hält strikt die 30-FPS-Latenzgrenze für zuverlässige Dashcam-Auswertungen ein.
3. **Robustheit bei Unschärfe**: Deep Super-Resolution (EDSR) stellt unleserliche Kennzeichenfragmente wieder her.
4. **Fehlalarm-Reduktion**: Geometrische IoU-Kriterien verhindern Fehlalarme bei Fahrbahnunebenheiten.
"""

# ==============================================================================
# ANPR 2 GERMAN
# ==============================================================================
a2_slug = "2026-06-26-vision-anpr-2"
a2_content = """---
slug: 2026-06-26-vision-anpr-2
title: "[Vision AI] Dynamische Fahrspurbegrenzung & Geometrisches IoU-Übertrittskriterium (#2)"
authors: [jbgih]
tags: [computer-vision, anpr, lane-detection, hough-transform, iou, opencv, python]
date: 2026-06-26
project: anpr_vision
description: "Canny-Kantenfilterung, probabilistische Hough-Transformation (HoughLinesP), Steigungsschwellenwerte und geometrische Polygon-IoU-Berechnung zur Spurerkennung."
keywords: [OpenCV Spurerkennung, HoughLinesP Fahrspurverfolgung, Fahrspurübertritt Erkennung, Polygon IoU Berechnung, Canny Kantenerkennung Straßen]
---

![Dynamische Spurerkennung Overlay](./images/01_lane_detection.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Herausforderung**: Blendung durch nasse Fahrbahnen, Teer-Risse und Schatten erzeugen fehlerhafte Linien; einfache X-Koordinaten-Vergleiche erkennen Spurübertritte nicht zuverlässig.
> - **Lösung**: Kombination aus adaptiver ROI-Trapezmaske, Steigungsfilterung positiver/negativer Geraden und Polygon-Flächenüberlappung (IoU > 0,15).

{/* truncate */}

---

### 1. Mathematische Formulierung der Spurextraktion

Die Fahrbahnbegrenzung wird durch Geradengleichungen in der Bildebene modelliert:

$$y = m \cdot x + b, \quad \text{wobei } m = \frac{y_2 - y_1}{x_2 - x_1}$$

Um irrelevante horizontale Markierungen und Schatten auszuschließen, definieren wir strikte Steigungsgrenzen:
- **Linke Spur**: $-0.85 < m < -0.45$
- **Rechte Spur**: $+0.45 < m < +0.85$

---

### 2. Geometrisches IoU-Kriterium für Spurübertritte

Ein Spurübertritt gilt als verifiziert, wenn das Polygon der Fahrzeug-Unterkante $P_{\text{vehicle}}$ die Grenzlinie der Fahrspur $P_{\text{lane}}$ schneidet:

$$\text{IoU}_{\text{intrusion}} = \frac{\text{Area}(P_{\text{vehicle}} \cap P_{\text{lane}})}{\text{Area}(P_{\text{vehicle}})} > \theta_{\text{threshold}}$$

Mit einem Schwellenwert $\theta = 0.15$ werden kurzzeitige Messausreißer zuverlässig abgefangen, während ein echter Spurwechsel deterministisch registriert wird.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Robuste Filterung**: Steigungsschwellenwerte eliminieren 95 % aller Störlinien durch Schatten und Teerfugen.
2. **Polygon-IoU statt Punkt-Vergleich**: Die Flächenüberlappung verhindert Fehlauslösungen bei Kurvenfahrten.
3. **Echtzeit-Performance**: Die Hough-Transformation auf der Trapez-ROI beansprucht weniger als 3 Millisekunden pro Frame.
4. **Deterministische Übergabe**: Verifizierte Spurübertritte triggern automatisch die hochauflösende Kennzeichenerfassung.
"""

# ==============================================================================
# ANPR 3 GERMAN
# ==============================================================================
a3_slug = "2026-06-27-vision-anpr-3"
a3_content = """---
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
"""

# ==============================================================================
# ANPR 4 GERMAN
# ==============================================================================
a4_slug = "2026-06-28-vision-anpr-4"
a4_content = """---
slug: 2026-06-28-vision-anpr-4
title: "[Vision AI] Artefakte in Dashcam-Videos überwinden: Deep Super-Resolution (EDSR vs FSRCNN) & Multi-Frame Image Stacking (#4)"
authors: [jbgih]
tags: [computer-vision, super-resolution, edsr, image-stacking, anpr, deep-learning, python]
date: 2026-06-28
project: anpr_vision
description: "Rekonstruktion niedrig aufgelöster Kennzeichen-Ausschnitte mittels 4x EDSR Deep Super-Resolution und temporalem Multi-Frame Image Stacking."
keywords: [EDSR Super Resolution, Kennzeichen Bildentfaltung, OpenCV dnn_superres, Multi-Frame Image Stacking, Deep Residual Upscaling]
---

![EDSR Deep Super-Resolution Vergleich](./images/01_edsr_sr_comparison.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Herausforderung**: Ausgeschnittene Kennzeichen messen oft unter 40x20 Pixel mit starker H.264-Kompressionsblockbildung. Standard-Bikubik-Interpolation verwäscht Zeichenkonturen.
> - **Lösung**: Einsatz von EDSR (Enhanced Deep Residual Networks) zur 4-fachen Kantenrekonstruktion und Multi-Frame-Mittelung zur Rauschunterdrückung.

{/* truncate */}

---

### 1. EDSR vs. FSRCNN: Der Qualitätsvergleich

| Modell | Rechenzeit (ms) | Rekonstruktionsqualität | Geeignet für |
| :--- | :--- | :--- | :--- |
| **Bikubische Interpolation** | < 1 ms | Sehr unscharf; Zeichen verschwimmen | Nicht nutzbar für OCR |
| **FSRCNN (Fast SR)** | ~ 8 ms | Mäßige Kantenschärfung | Mobile Edge-Geräte |
| **EDSR (Enhanced Deep Residual)** | ~ 35 ms | **Hervorragende Zeichenschärfe & Kontrast** | **Produktions-Pipeline** |

EDSR entfernt unnötige Batch-Normalisierungs-Schichten und nutzt erweiterte Residualblöcke, wodurch hochfrequente Ziffernstrukturen selbst aus stark verpixelten Dashcam-Ausschnitten wiederhergestellt werden.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Grenzen klassischer Interpolation**: Bikubische Verfahren verstärken Blockartefakte und verhindern korrekte OCR-Ergebnisse.
2. **EDSR 4x Rekonstruktion**: Neuronale Residualnetzwerke schärfen Buchstabenkonturen und Kontraste signifikant.
3. **Multi-Frame-Stacking**: Temporale Mittelung eliminiert Sensorrauschen vor der Weitergabe an das OCR-Modul.
4. **Verifizierte OCR-Voraussetzung**: Die Super-Resolution erhöht die anschließende Erkennungsrate von 42 % auf über 89 %.
"""

# ==============================================================================
# ANPR 5 GERMAN
# ==============================================================================
a5_slug = "2026-06-29-vision-anpr-5"
a5_content = """---
slug: 2026-06-29-vision-anpr-5
title: "[Vision AI] ANPR-OCR-Engine, Regex-Normalisierung & Temporales Majority Voting (Evolution von v01 bis v11) (#5)"
authors: [jbgih]
tags: [computer-vision, anpr, easyocr, regex, voting-ensemble, python]
date: 2026-06-29
project: anpr_vision
description: "Syntaxvalidierung von Kennzeichen, EasyOCR-Optimierung, temporales Sliding-Window Majority Voting und die Entwicklungsreise über 11 Iterationen von v01 bis v11."
keywords: [EasyOCR Kennzeichenerkennung, ANPR Majority Voting Ensemble, Kennzeichen Regex Normalisierung, OCR Erkennungsgenauigkeit, Intelligente Verkehrssysteme ITS]
---

![Temporales Majority Voting und finale Verifikation](./images/01_voting_evolution.png)

> 📌 **Kernaussagen (TL;DR)**
> - **Herausforderung**: Einzelne Frames führen durch Fahrzeugneigung und Spiegelungen unweigerlich zu Lesefehlern (z. B. Verwechslung von `6` und `8` oder `B` und `8`).
> - **Lösung**: Kombination aus EasyOCR, syntaktischer Regex-Korrektur und temporalem Mehrheitsentscheid (*Sliding-Window Majority Voting*) über 11 Frames.

{/* truncate */}

---

### 1. Das temporale Majority-Voting-Verfahren

Statt dem Ergebnis eines einzelnen Frames blind zu vertrauen, aggregiert das System Erkennungen über ein gleitendes Zeitfenster von 11 aufeinanderfolgenden Bildern:

```mermaid
flowchart TD
    F1["Frame 1: 24가1511"] --> Buffer[Ringpuffer: 11 Frames]
    F2["Frame 2: 24가1511"] --> Buffer
    F3["Frame 3: 24가1571 (Fehllesung)"] --> Buffer
    F4["Frame 4: 24가1511"] --> Buffer
    Buffer --> Voting{"Majority Voting: Welcher String hat die höchste Frequenz?"}
    Voting -->|8 von 11 Stimmen| Confirmed["Bestätigtes Kennzeichen: 24가1511 (Konfidenz: 94.2%)"]
```

---

### 2. Die evolutionäre Reise: Von v01 bis v11

Über 11 Entwicklungszyklen steigerte das Team die End-to-End-Erkennungsrate von initial 31 % auf über 96 % unter realen Straßenbedingungen.

---

### 📌 Management Summary (3–5 Zeilen)
1. **Konsens schlägt Einzelframe**: Temporales Voting filtert kurzzeitige Erkennungsfehler durch Vibrationen zuverlässig heraus.
2. **Regex-Syntaxschutz**: Ungültige Zeichenmuster werden noch vor dem Voting syntaktisch korrigiert.
3. **Hohe Zuverlässigkeit**: Über 11 Iterationen wurde eine Erkennungsgenauigkeit von über 96 % in Realaufnahmen erreicht.
4. **Vollständige Pipeline**: Die Kombination aller 6 Stufen liefert ein produktionsreifes System für intelligente Verkehrsanwendungen.
"""

# Execute Section 3
if __name__ == "__main__":
    print("=" * 60)
    print("Translating Section 3 (Vision ANPR, 5 posts) into German...")
    print("=" * 60)
    save_de_post(a1_slug, a1_content)
    save_de_post(a2_slug, a2_content)
    save_de_post(a3_slug, a3_content)
    save_de_post(a4_slug, a4_content)
    save_de_post(a5_slug, a5_content)
    print("\n[SECTION 3 COMPLETE] All 5 Vision ANPR posts staged and saved in German!")
