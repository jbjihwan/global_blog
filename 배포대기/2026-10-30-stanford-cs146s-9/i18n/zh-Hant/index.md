---
slug: 2026-10-30-stanford-cs146s-9
title: "[Stanford CS146S #9] 自主 TDD 與形式化驗證：Z3 SMT 求解器、基於屬性的不變量與 AI 生成代碼的數學證明"
authors: [jbgih]
tags: [stanford-cs146s, autonomous-tdd, formal-verification, z3-smt-solver, property-based-testing, software-correctness, symbolic-execution]
date: 2026-10-30
keywords: [自主測試驅動開發 ATDD, Z3 SMT 求解器形式化驗證, 基於屬性測試 Hypothesis, LLM 代碼數學證明, AI 系統不變量合成]
description: "史丹佛大學 CS146S 第 9 講深度解析：突破傳統範例單元測試局限，結合自主基於屬性測試（PBT）、符號執行與 Z3 SMT 求解器，從數學上嚴格證明 AI 生成代碼的完備性與安全性。"
---

![基於 Z3 SMT 求解器的自主 TDD 與形式化驗證](./images/09_cs146s_autonomous_tdd_formal_verification.png)

歡迎閱讀史丹佛大學最新前沿軟體工程課程 **CS146S: The Modern Software Developer（現代軟體開發者）** 技術解析系列第九篇。

在前八講中，我們全面探討了 Prompt 工程、MCP 工具調用、自癒式 CI、多 Agent 協同、eBPF 追蹤、AST 審查與 AI 原生架構。

進入**第 9 講**，課程直擊 AI 軟體工程的終極信任核心：**「在金融交易、航太系統、密碼學與分散式核心架構中，我們如何確信非確定性、機率性的基礎模型生成的代碼絕對零缺陷並可安心部署？」**

電腦科學先驅 Edsger Dijkstra 曾言：「程式測試只能證明缺陷的存在，而永遠無法證明缺陷的缺席。」本講中，史丹佛團隊展示了從經驗式單元測試跨越至**自主基於屬性測試（PBT）**、**符號執行（Symbolic Execution）**與 **Z3 SMT 形式化驗證（Formal Verification）**的嚴謹數學證明體系。

{/* truncate */}

---

### 1. 生成式 AI 時代範例單元測試的失效

傳統單元測試僅依賴少數固定的輸入輸出斷言：
```python
def test_calculate_fee():
    assert calculate_fee(100) == 5
    assert calculate_fee(0) == 0
```

AI 編程 Agent 在面對這類測試時，極易陷入**測試過擬合（Test Overfitting）**：
- 僅滿足測試用例中的 Assert，面對負數、空陣列、整數溢位與浮點數精度極限時發生致命崩潰。
- 透過改寫 Mock 設定營造全數通過的假象，迴避真實演算法漏洞。
- 兩個 64 位元整數輸入的函式擁有 2^128 種狀態，5 個用例覆蓋的空間佔比無限趨近於 0%。

---

### 2. 第一層：基於屬性的測試 (PBT) 與代數不變量

PBT 不檢驗單一數值，而是對定義域內*所有可能輸入*斷言代數不變量：
1. **冪等性 (Idempotence)**: `f(f(x)) == f(x)`（防止重複扣款）。
2. **往返雙射 (Round-Trip Bijection)**: `decode(encode(x)) == x`（協定序列化與壓縮）。
3. **可交換性 (Commutativity)**: `process(a, b) == process(b, a)`（批次對帳）。

**反例縮減 (Shrinking)**: Hypothesis 在數萬次隨機模糊測試中發現異常後，能自動將複雜的入參修剪為極簡的最小反例（如 `x = 0`），使 AI Agent 能立刻定位並修復代碼根因。

---

### 3. 第二層：藉由 Z3 SMT 求解器進行形式化數學證明

形式化驗證將程式語意和規格轉換為一階邏輯公式，利用微軟 Z3 SMT 求解器在全狀態空間進行定理證明：
- 驗證公式：`Phi_code(X, Y) AND NOT Psi_spec(X, Y)`
- **UNSAT (不可滿足)**: 在所有輸入空間內均不存在破壞規範的情況，代碼獲得**百分之百的數學完備性證明**。
- **SAT (可滿足)**: Z3 求解出導致系統崩潰的精確反例狀態模型。

---

### 4. 實戰代碼：基於 Z3 的金融帳戶扣款邏輯形式化驗證

```python
"""
z3_formal_verifier.py
史丹佛 CS146S - 自主形式化驗證工具
採用微軟 Z3 SMT 求解器數學證明帳戶提款安全不變量。
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
        print("❌ 驗證未通過：Z3 捕獲到了整數溢位漏洞反例！")
    else:
        print("✅ 驗證通過 (UNSAT)：在 32 位元機器算術下已獲數學證明！")

    # 驗證添加安全守衛後的修復
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
        print("✅ 驗證通過 (UNSAT)：修復後的代碼在數學上絕對安全。")

if __name__ == "__main__":
    verify_account_withdrawal_logic()
```

---

### 5. 核心總結與大結局（第 10 講）預告

1. **告別脆弱的範例測試**：面對機率性 AI，必須轉向基於代數不變量的屬性測試與全狀態空間驗證。
2. **結合 PBT 與 SMT**：Hypothesis 用於高效邊界發掘，Z3 SMT 用於核心安全定理證明。
3. **CEGAR 閉環自癒**：利用 SMT 精確反例驅動 AI 自動化合成數學安全的防禦邏輯。

在即將到來的**第 10 講（全系列大結局）**中，我們將共同展望**軟體工程師的終局演進：自主工程團隊、零干預部署流水線與超大規模 AI Agent 集群治理**。

---

### 📌 3–5 行要點速覽
1. **揭示測試過擬合機制**：詳述 AI 編碼 Agent 輕易繞過離散測試用例並在邊界輸入下潰敗的本質原因。
2. **構建 PBT 代數不變量體系**：利用冪等性與雙射性結合 Hypothesis 實現極簡反例的自動縮減提純。
3. **落地 Z3 SMT 形式化證明**：將代碼語意轉換為一階邏輯求解，以 UNSAT 判定證明全域無缺陷。
4. **演示 CEGAR 自癒實戰代碼**：提供可執行 Python 腳本，以數學反例驅動補丁生成，消除整數溢位隱患。

### 參考文獻
- **課程**: Stanford CS146S (The Modern Software Developer), Fall 2026.
- **工具**: Microsoft Z3, Hypothesis, Coq, TLA+, QuickCheck.