---
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
