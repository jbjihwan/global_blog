---
slug: national-budget-ai-6-sector-full-suite
title: "Auditoría IA #5: Suite de 6 Sectores y Gasto de Fin de Año"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, procurement-fraud, year-end-dumping, spec-driven-development, devops]
date: 2026-11-22
keywords: ["Suite 6 Sectores", "Fraccionamiento de Contratos", "Gasto Fin de Año", "Detección Fraude IA", "Auditoría Compras Públicas"]
description: "Finalización de la suite de auditoría en 6 sectores: Detección de contratos fraccionados bajo excepciones de 40.000 $ y gasto apresurado de fin de año."
---

![6-Sector Targeted Audit: Divide & Conquer Suite](./images/01_national_budget_6_sector_suite.png)

> 📌 **Puntos Clave (Key Takeaways)**
> - **Suite Integral de 6 Sectores**: Filtrado de 85% de compras rutinarias sobre 4 millones de contratos, expandiendo la auditoría a **6 sectores críticos de fraude**.
> - **2 Grandes Puntos Ciegos Descubiertos**:
>   1. **Sector 5 (Fraccionamiento Preferencial de 40.000 $)**: Evasión mediante contratos concentrados en el 98% del umbral legal ($180.000 detectados).
>   2. **Sector 6 (Vaciado Presupuestario de Fin de Año)**: Rápida adjudicación de 3 contratos en 4 días a finales de diciembre para evitar la devolución de fondos.
> - **Prevención Arquitectural**: Algoritmo de proximidad (96-99.8%) y comprobación de viabilidad física de plazos de entrega.
> - **Corrección de Bugs**: Desduplicación entre sectores por peso de gravedad y normalización de precios netos sin IVA.

{/* truncate */}

---

### ⚠️ Aviso Legal y Anonimización (Legal Notice)

> **[Aviso] Todos los casos han sido rigurosamente anonimizados.**  
> Los nombres de agencias (`Agencia A`), contratistas (`Empresa D`), personas y contratos han sido totalmente enmascarados.

---

### 1. Arquitectura de Auditoría en 6 Sectores

```mermaid
flowchart TD
    Raw[4 Millones de Contratos Públicos] --> Filter{Gestor de Partición 3D}
    Filter -->|85% Consumibles| Drop[Archivo Bajo Riesgo]
    Filter --> S1["Sector 1: TIC <20k $"]
    Filter --> S2["Sector 2: Eventos Municipales"]
    Filter --> S3["Sector 3: Fuga de Subsidios DEI"]
    Filter --> S4["Sector 4: Grandes Licitaciones Monopolio"]
    Filter --> S5["🔴 Sector 5: Abuso de Excepción 40k $"]
    Filter --> S6["🔴 Sector 6: Vaciado Fin de Año"]
    S1 & S2 & S3 & S4 & S5 & S6 --> Master[All Sectors Master Runner]
```

---

### 2. Retos Previstos y Corrección de Fallos

1. **Excepción Política vs. Fraccionamiento**: Análisis de proximidad al umbral legal para evitar falsos positivos en empresas sociales legítimas.
2. **Cierre Rutinario vs. Vaciado Rápido**: Detección de proyectos donde el plazo hasta el 31 de diciembre hace físicamente imposible la entrega de los servicios.
3. **Colisiones Entre Sectores**: Asignación de sector prioritario según la gravedad penal del delito administrativo.
4. **Impuesto IVA**: Deducción inversa de importes con IVA para verificar el umbral legal real sin impuestos.

---

### 3. Validación y Resultados en Campo

Detección de 3 contratos fraccionados de 39.000 $ en la `Agencia A` y adjudicaciones exprés de 100.000 $ en la `Agencia C` en diciembre; 17/17 pruebas superadas.
