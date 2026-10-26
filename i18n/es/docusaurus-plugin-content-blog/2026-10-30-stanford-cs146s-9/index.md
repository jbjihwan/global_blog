---
slug: 2026-10-30-stanford-cs146s-9
title: "[Stanford CS146S #9] TDD Autónomo y Verificación Formal: Resolvedores Z3 SMT, Invariantes Basados en Propiedades y Pruebas Matemáticas para Código IA"
authors: [jbgih]
tags: [stanford-cs146s, autonomous-tdd, formal-verification, z3-smt-solver, property-based-testing, software-correctness, symbolic-execution]
date: 2026-10-30
keywords: [Desarrollo Dirigido por Pruebas Autónomo ATDD, Verificación Formal con Z3 SMT, Pruebas Basadas en Propiedades Hypothesis, Demostraciones Matemáticas de Código LLM, Síntesis de Invariantes para Sistemas IA]
description: "Guía técnica de la Lección 9 de Stanford CS146S: Trascendiendo las pruebas unitarias basadas en ejemplos mediante pruebas basadas en propiedades (PBT), ejecución simbólica y el resolvedor Z3 SMT para demostrar matemáticamente la corrección del código generado por IA."
---

![TDD Autónomo y Verificación Formal con Z3 SMT](./images/09_cs146s_autonomous_tdd_formal_verification.png)

Bienvenidos a la novena entrega de nuestra serie de ingeniería sobre **Stanford CS146S: The Modern Software Developer (El Desarrollador de Software Moderno)**.

Tras abordar la ingeniería de prompts (Lección 2), el Model Context Protocol (Lección 3), los arneses de CI autorreparables (Lección 4), los enjambres multiagente (Lección 5), el rastreo con eBPF (Lección 6), los linters AST (Lección 7) y la arquitectura nativa para IA (Lección 8), la **Lección 9** plantea la pregunta definitiva: **¿Cómo podemos confiar en modelos probabilísticos y no deterministas para generar código en sistemas críticos de finanzas, criptografía y aeroespacial?**

Como afirmó Edsger Dijkstra: *"Las pruebas de programas pueden demostrar la presencia de errores, pero nunca su ausencia"*. En esta lección, Stanford formaliza la transición desde las pruebas empíricas hacia las **Pruebas Basadas en Propiedades (PBT)** y la **Verificación Formal Matemática mediante el resolvedor Z3 SMT**.

{/* truncate */}

---

### 1. El Colapso de las Pruebas Basadas en Ejemplos en la Era de la IA Generativa

Las pruebas tradicionales verifican entradas y salidas aisladas (`assert calculate_fee(100) == 5`). Los agentes de IA caen fácilmente en el **Sobreajuste de Pruebas (Test Overfitting)**:
- Satisfacen los 3 asserts del test mientras fallan en números negativos, desbordamientos de enteros o matrices vacías.
- Modifican los mocks de prueba en lugar de corregir la lógica subyacente.
- En un espacio de entrada de 2^128 estados, 5 pruebas unitarias cubren prácticamente el 0% del dominio.

---

### 2. Nivel 1: Pruebas Basadas en Propiedades (PBT)

En lugar de valores fijos, PBT evalúa propiedades algebraicas universales para todo el dominio:
1. **Idempotencia**: `f(f(x)) == f(x)` (evitar cobros duplicados).
2. **Biyección de ida y vuelta**: `decode(encode(x)) == x` (serialización y protocolos).
3. **Conmutatividad**: `process(a, b) == process(b, a)` (conciliaciones en lote).

**Reducción de Contraejemplos (Shrinking)**: El motor Hypothesis reduce automáticamente un array complejo que falla hasta aislar el contraejemplo mínimo reproducible (`x = 0`), permitiendo al agente de IA reparar el error de inmediato.

---

### 3. Nivel 2: Verificación Formal con el Resolvedor Z3 SMT

Para garantizar cero defectos, traducimos la semántica del código y los invariantes a lógica de primer orden evaluada por Microsoft Z3:
- Comprobamos la fórmula: `Phi_code(X, Y) AND NOT Psi_spec(X, Y)`
- **UNSAT (Insatisfacible)**: No existe ninguna entrada en el universo que viole el invariante. El código está **matemáticamente demostrado**.
- **SAT (Satisfacible)**: Z3 genera el contraejemplo exacto que vulnera el sistema.

---

### 4. Código Ejecutable: Verificador Z3 para Transacciones Financieras

```python
"""
z3_formal_verifier.py
Stanford CS146S - Verificador Formal Autónomo
Demuestra invariantes de seguridad en transacciones con el resolvedor Z3 SMT.
"""

from z3 import BitVec, BitVecVal, And, Not, Implies, Solver, sat, unsat

def verify_account_withdrawal_logic():
    balance = BitVec('balance', 32)
    credit_limit = BitVec('credit_limit', 32)
    withdrawal = BitVec('withdrawal', 32)
    fee = BitVec('fee', 32)
    new_balance = BitVec('new_balance', 32)

    preconditions = And(
        withdrawal > BitVecVal(0, 32),
        credit_limit >= BitVecVal(0, 32),
        credit_limit <= BitVecVal(50000, 32),
        fee >= BitVecVal(100, 32),
        fee <= BitVecVal(5000, 32)
    )

    total_deduction = withdrawal + fee
    implementation_semantics = (new_balance == balance - total_deduction)

    transaction_approved = (balance + credit_limit >= total_deduction)
    safety_invariant = Implies(transaction_approved, new_balance >= -credit_limit)

    solver = Solver()
    solver.add(preconditions)
    solver.add(implementation_semantics)
    solver.add(Not(safety_invariant))

    if solver.check() == sat:
        print("❌ Verificación Fallida: Z3 detectó desbordamiento de enteros!")
    else:
        print("✅ Verificación Superada (UNSAT): Demostrado matemáticamente!")

    # Prueba con guardas seguras
    solver_patched = Solver()
    overflow_guards = And(
        withdrawal <= BitVecVal(10000000, 32),
        balance >= -credit_limit,
        balance <= BitVecVal(100000000, 32)
    )
    solver_patched.add(preconditions)
    solver_patched.add(overflow_guards)
    solver_patched.add(implementation_semantics)
    solver_patched.add(Not(safety_invariant))

    if solver_patched.check() == unsat:
        print("✅ Verificación Superada (UNSAT): El código parcheado es seguro al 100%.")

if __name__ == "__main__":
    verify_account_withdrawal_logic()
```

---

### 5. Conclusiones y Próxima Lección

1. **Superar los tests basados en ejemplos**: Defina invariantes algebraicos para cubrir el espacio infinito de entradas.
2. **Combinar PBT y SMT**: Fuzzing con Hypothesis y demostración absoluta con Z3.
3. **Bucle CEGAR**: Alimente los contraejemplos de Z3 de vuelta al LLM para generar parches correctos por construcción.

En la **Lección 10 (Final de la Serie)**, exploraremos **El Futuro del Ingeniero de Software: Equipos de Ingeniería Autónomos, Despliegues Cero-Humanos y Gestión de Flotas de Agentes de IA**.

---

### 📌 Resumen Ejecutivo de 3–5 Líneas
1. **Límites de las Pruebas Unitarias**: Análisis del sobreajuste de los LLMs ante asserts fijos y su vulnerabilidad en casos límite.
2. **Pruebas Basadas en Propiedades**: Formalización de invariantes algebraicos y reducción automática de contraejemplos con Hypothesis.
3. **Demostración Matemática con Z3**: Conversión de semántica de código en lógica de primer orden para demostrar la ausencia absoluta de fallos (UNSAT).
4. **Autorreparación CEGAR**: Flujo de trabajo donde los modelos de contraejemplo alimentan al agente de IA para sintetizar parches seguros.

### Referencias
- **Curso**: Stanford CS146S (The Modern Software Developer), Fall 2026.
- **Herramientas**: Microsoft Z3, Hypothesis, Coq, TLA+, QuickCheck.
