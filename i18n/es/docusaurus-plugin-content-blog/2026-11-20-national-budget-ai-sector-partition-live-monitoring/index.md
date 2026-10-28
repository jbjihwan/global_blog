---
slug: national-budget-ai-sector-partition-live-monitoring
title: "Auditoría IA #3: Partición 3D y Portal en Tiempo Real"
authors: [jbgih]
tags: [ai-agents, sector-partitioning, live-streaming, koneps-api, web-dashboard, devops]
date: 2026-11-20
keywords: ["Partición 3D por Sectores", "API Compras Públicas", "Portal Web Auditoría", "Detección Fraude IA", "Filtro de Ruido"]
description: "Filtrado del 85% del ruido mediante partición 3D por sectores y conexión en vivo con APIs públicas para el portal de auditoría v2.0 con Vis.js."
---

![3D Sector Partitioning & Live Audit Web Portal](./images/01_national_budget_sector_live_monitor.png)

> 📌 **Puntos Clave (Key Takeaways)**
> - **Superación de la Fatiga de Alertas**: Filtrado de más del 85% del ruido de consumibles habituales mediante el **Gestor de Partición 3D por Sectores (SectorPartitionManager)**, concentrando los recursos en áreas de alto riesgo.
> - **Prevención de Fallos**: Implementación de una **cola de búfer aislada en SQLite con reintentos exponenciales** ante caídas y latencias de APIs públicas.
> - **Resolución de 3 Errores Críticos de Producción**:
>   1. Campos con delimitadores compuestos intercalados (`^`) ➔ Normalizador regex y tipado estricto.
>   2. Bloqueo de UI en el navegador al renderizar miles de nodos ➔ **Virtualización de subgrafos Ego-Network (Depth-1)**, reduciendo la latencia un 98%.
>   3. Alertas redundantes por sondeo en tiempo real ➔ **Hashes SHA-256** para asegurar idempotencia.
> - **Entregable**: Portal web interactivo v2.0 operativo y 13/13 pruebas superadas.

{/* truncate */}

---

### ⚠️ Aviso Legal y Anonimización (Legal Notice)

> **[Aviso] Todos los casos han sido rigurosamente anonimizados.**  
> Los nombres de agencias (`Agencia A`), contratistas (`Empresa A`), números de contrato y direcciones físicas han sido completamente enmascarados.

---

### 1. Arquitectura de Partición 3D y Transmisión en Vivo

```mermaid
flowchart TD
    subgraph DataStream ["Etapa 1: Flujo en Tiempo Real y Capa de Resiliencia"]
        A[API Compras Públicas] --> B[Parser ^ Caret]
        B --> C[SHA-256 Deduplicador]
        C --> D[(SQLite Búfer no Auditado)]
    end

    subgraph PartitionEngine ["Etapa 2: Motor de Partición 3D"]
        D --> E{Filtro Matricial 3D<br/>Agencia × Partida × Método}
        E -->|85% Consumibles| F[Archivo de Bajo Riesgo]
        E -->|Alto Riesgo| G[Sector 1: TIC Contratos Divididos]
        E -->|Alto Riesgo| H[Sector 2: Cárteles Eventos Locales]
        E -->|Alto Riesgo| I[Sector 3: Fuga de Subsidios]
    end

    subgraph InspectorPortal ["Etapa 3: Portal del Auditor v2.0"]
        G --> J[Orquestador E2E]
        H --> J
        I --> J
        J --> K[Vis.js Ego-Network]
        J --> L[Base de Precedentes (10 años)]
        J --> M[Parser de Costes HWPX]
        J --> N[Exportación de Informes]
    end
```

---

### 2. Desafíos Previstos y Solución de Errores

1. **Partición 3D**: Eliminó el 85% del ruido rutinario cruzando "Tipo de Entidad × Partida Presupuestaria × Tipo de Contrato".
2. **Error de Delimitador (`^`)**: Resuelto aplanando registros compuestos legados.
3. **Bloqueo del Navegador**: El motor de física de Vis.js colapsaba la UI con miles de nodos; resuelto renderizando bajo demanda vecindarios de orden 1 (Depth-1).
4. **Hashes SHA-256**: Garantizaron la idempotencia frente a reenvíos de la API.

---

### 3. Portal Web v2.0 y Verificación Total

El portal en `http://localhost:8088` integra navegación visual de cárteles, base jurídica y evaluación en tiempo real, validado con 13 pruebas unitarias e integradas (13/13 PASS).
