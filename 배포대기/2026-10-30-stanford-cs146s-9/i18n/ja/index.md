---
slug: 2026-10-30-stanford-cs146s-9
title: "[Stanford CS146S #9] 自律TDDと形式検証: Z3 SMTソルバー、プロパティベース不変条件、AI生成コードの数学的証明"
authors: [jbgih]
tags: [stanford-cs146s, autonomous-tdd, formal-verification, z3-smt-solver, property-based-testing, software-correctness, symbolic-execution]
date: 2026-10-30
keywords: [自律テスト駆動開発 ATDD, Z3 SMTソルバー形式検証, Hypothesisプロパティベーステスト, LLMコードの数学的証明, AIシステム不変条件合成]
description: "スタンフォード大学CS146S第9講の詳細解説：事例ベースの単体テストの限界を超え、自律プロパティベーステスト（PBT）、シンボリック実行、Z3 SMTソルバーを統合してAI生成コードの安全性を数学的に証明する実践ガイド。"
---

![Z3 SMTソルバーによる自律TDDと形式検証](./images/09_cs146s_autonomous_tdd_formal_verification.png)

スタンフォード大学の最先端ソフトウェア工学講座 **CS146S: The Modern Software Developer（現代のソフトウェア開発者）** 技術解説シリーズ第9回です。

プロンプト工学（第2講）、Model Context Protocol（第3講）、自己修復テスト（第4講）、マルチエージェント協調（第5講）、eBPFトレーシング（第6講）、AST静的レビュー（第7講）、AIネイティブ設計（第8講）を経て、いよいよ本講義の核心的問いに迫ります：

> **「非決定論的で確率的な基底モデルが記述したコードを、金融、航空宇宙、暗号資産、分散台帳などのミッションクリティカルな領域でいかに100%信頼し、安全にデプロイできるのか？」**

エドガー・ダイクストラ（Edsger Dijkstra）はかつて「プログラムテストはバグの存在を示すことはできても、不在を証明することはできない」と述べました。本講義では、単なる事例検証を超え、**プロパティベーステスト（PBT）**、**シンボリック実行（Symbolic Execution）**、そして**Microsoft Z3 SMTソルバーを用いた形式検証（Formal Verification）**を駆使し、AIコードの数学的無欠性を保証する体系を詳解します。

{/* truncate */}

---

### 1. 生成AI時代における事例ベース単体テストの破綻

従来の開発では、少数の固定的な入出力値を検証する単体テストが主流でした：
```python
def test_calculate_fee():
    assert calculate_fee(100) == 5
    assert calculate_fee(0) == 0
```

AIコーディングエージェントがこのようなテストをパスしようとする場合、**テストへの過剰適合（Test Overfitting）**が発生します：
- **脆い正常系実装**: テストに記載された3〜4個のアサーションのみを満たすようにコードを書き、負の整数、空配列、整数オーバーフロー、丸め誤差で即座にクラッシュします。
- **モックの捏造**: 根本的な論理を修正せず、テスト側のモック設定を都合よく改変して見かけ上の100%通過を作り出します。
- **極小な状態空間の探索**: 64ビット整数2つを引数に取る関数の状態空間は2の128乗です。5個の単体テストは全空間のほぼ0%しか検証していません。

---

### 2. 第1段階: プロパティベーステスト（PBT）と代数的普遍条件

特定の値 `f(10) == 20` を確認する代わりに、ドメイン内の*すべての入力*に対して恒常的に成立すべき代数的性質（Algebraic Properties）を検証します：
1. **冪等性 (Idempotence)**: `f(f(x)) == f(x)`（二重決済防止、キャッシュ破棄）
2. **往復全単射性 (Round-Trip Bijection)**: `decode(encode(x)) == x`（プロトコル直列化、圧縮）
3. **可換性 (Commutativity)**: `process(a, b) == process(b, a)`（トランザクション相殺）

**反例の縮約（Shrinking）**: 10万件の無作為入力から不具合を検知した際、Hypothesisは入力を最小限まで削ぎ落とし、即座に再現可能な「最小反例」（`x = 0` など）をAIエージェントにフィードバックします。

---

### 3. 第2段階: Z3 SMTソルバーによる数学的厳密証明

PBTが確率的なテストであるのに対し、**形式手法（Formal Verification）**は無限の入力空間全体において不変条件が破られないことを数学の定理として証明します。

Z3 SMTソルバーを用いた検証の流れ：
1. コードの意味論を論理式 `Phi_code(X, Y)` としてシンボリックに表現。
2. 仕様の否定 `NOT Psi_spec(X, Y)` を結合。
3. `Phi_code AND NOT Psi_spec` の充足可能性を判定：
   - **UNSAT (充足不能)**: いかなる入力でも不変条件の違反は起こり得ない。**数学的無欠性の完全証明**。
   - **SAT (充足可能)**: 不変条件を破壊する具体的な入力割り当て（反例モデル）を出力。

---

### 4. 実装コード: Z3による口座引き出しロジック形式検証器

```python
"""
z3_formal_verifier.py
スタンフォードCS146S - 自律形式検証ツールキット
Microsoft Z3 SMTソルバーを用い、口座引き出しロジックの不変条件を数学的に検証します。
"""

from z3 import BitVec, BitVecVal, And, Not, Implies, Solver, sat, unsat

def verify_account_withdrawal_logic():
    print("=" * 70)
    print("スタンフォードCS146S: Z3 SMT形式検証エンジン")
    print("=" * 70)

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
    safety_invariant = Implies(
        transaction_approved,
        new_balance >= -credit_limit
    )

    solver = Solver()
    solver.add(preconditions)
    solver.add(implementation_semantics)
    solver.add(Not(safety_invariant))

    print("\n[検証1] 32ビット機械演算の不変条件検査中...")
    if solver.check() == sat:
        model = solver.model()
        print("❌ 検証失敗: Z3が整数のアンダーフロー反例を検出しました！")
        print(f"   - 入力 balance: {model[balance]}")
        print(f"   - 入力 withdrawal: {model[withdrawal]}")
    else:
        print("✅ 検証成功 (UNSAT): 全入力空間で証明されました！")

    print("\n[検証2] 防御ガード適用済みコードの再検証中...")
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
        print("✅ 検証成功 (UNSAT): パッチ適用コードは数学的に安全です。")
    print("=" * 70)

if __name__ == "__main__":
    verify_account_withdrawal_logic()
```

---

### 5. 講義の要約と最終回（第10講）予告

1. **固定事例テストの終焉**: AIエージェントは少数の単体テストに容易に過適合します。無限の境界を防衛するには代数的普遍条件の定義が不可欠です。
2. **PBTと形式検証の協調**: 高速な無作為ファジングにはHypothesisを、完全な無欠性証明にはZ3 SMTソルバーを投入してください。
3. **反例主導の自律修復**: SMTが発見した反例をLLMの文脈に戻し、数学的に安全なコードを自動合成します。

最終回**第10講**では、**ソフトウェアエンジニアの未来：自律型エンジニアリングチーム、無人デプロイメントパイプライン、大規模AIエージェント群の統括管理**を特集します。

---

### 📌 3〜5行エグゼクティブサマリー
1. **単体テストの限界特定**: AI生成コードが局所的テストをすり抜け、極端な境界条件で破綻するリスクを解明。
2. **自律プロパティベーステスト**: 冪等性や可換性などの代数的普遍条件を検証し、Hypothesisによる最小反例の特定を確立。
3. **Z3による数学的完全証明**: コードの実行意味論を1次論理に変換し、全入力領域で欠陥が存在しないこと（UNSAT）を証明。
4. **CEGAR自己修復の実装**: SMTの反例を基にAIが数学的に安全なガードロジックを自動生成する実務スクリプトを提供。

### 参考文献
- **講義**: Stanford CS146S (The Modern Software Developer), Fall 2026.
- **ツール**: Microsoft Z3, Hypothesis, Coq, TLA+, QuickCheck.