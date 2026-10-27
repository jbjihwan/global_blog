# -*- coding: utf-8 -*-
"""
Sanitize LaTeX formulas in Stanford CS329A Ep1 into clean Unicode / MDX-compliant code blocks.
"""
import os
import glob

def sanitize_content(text: str) -> str:
    # 1. Block formulas
    text = text.replace(
        "$$\\mathcal{L}_{\\text{MLE}}(\\theta) = - \\sum_{i=1}^{T} \\log P_\\theta(x_i \\mid x_{1:i-1})$$",
        "```text\nL_MLE(θ) = - ∑ log P_θ(x_i | x_{1:i-1})\n```"
    )
    text = text.replace(
        "$$\\max_\\theta \\mathbb{E}_{(x, y) \\sim \\mathcal{D}} \\left[ r_\\psi(x, y) \\right] - \\beta \\, \\mathbb{D}_{\\text{KL}}\\left(\\pi_\\theta(y \\mid x) \\,|\\|\\, \\pi_{\\text{ref}}(y \\mid x)\\right)$$",
        "```text\nmax_θ E_{(x, y) ~ D} [ r_ψ(x, y) ] - β · D_KL( π_θ(y | x) || π_ref(y | x) )\n```"
    )
    text = text.replace(
        "$$L(N, D) = E + \\frac{A}{N^\\alpha} + \\frac{B}{D^\\beta}$$",
        "```text\nL(N, D) = E + A / N^α + B / D^β\n```"
    )
    text = text.replace(
        "$$\\text{Pass@}k = \\mathbb{E}\\left[ 1 - \\frac{\\binom{n - c}{k}}{\\binom{n}{k}} \\right]$$",
        "```text\nPass@k = E[ 1 - C(n - c, k) / C(n, k) ]\n```"
    )
    text = text.replace(
        "$$\\text{Complexity}(\\text{Verification}) \\ll \\text{Complexity}(\\text{Generation}) \\quad \\text{in closed formal domains (NP-complete)}$$",
        "```text\nComplexity(Verification) ≪ Complexity(Generation)   [Closed Formal Domains]\n```"
    )
    text = text.replace(
        "$$\\text{Complexity}(\\text{Verification}) \\approx \\text{Complexity}(\\text{Generation}) \\quad \\text{in open-ended natural domains}$$",
        "```text\nComplexity(Verification) ≈ Complexity(Generation)   [Open-Ended Natural Domains]\n```"
    )
    text = text.replace(
        "$$\\text{복잡도}(\\text{검증}) \\ll \\text{복잡도}(\\text{생성}) \\quad \\text{닫힌 정형 도메인 (수학, 코딩)}$$",
        "```text\n복잡도(검증) ≪ 복잡도(생성)   [닫힌 정형 도메인: 수학, 코딩]\n```"
    )
    text = text.replace(
        "$$\\text{복잡도}(\\text{검증}) \\approx \\text{복잡도}(\\text{생성}) \\quad \\text{열린 자연어 도메인 (전략, 글쓰기)}$$",
        "```text\n복잡도(검증) ≈ 복잡도(생성)   [열린 자연어 도메인: 전략, 글쓰기]\n```"
    )
    text = text.replace(
        "$$\\text{計算量}(\\text{検証}) \\ll \\text{計算量}(\\text{生成}) \\quad \\text{閉じた形式的領域（数学、コード、Lean 4）}$$",
        "```text\n計算量(検証) ≪ 計算量(生成)   [閉じた形式的領域: 数学、コード、Lean 4]\n```"
    )
    text = text.replace(
        "$$\\text{計算量}(\\text{検証}) \\approx \\text{計算量}(\\text{生成}) \\quad \\text{開かれた自然言語領域（小論文、戦略、法律）}$$",
        "```text\n計算量(検証) ≈ 計算量(生成)   [開かれた自然言語領域: 小論文、戦略、法律]\n```"
    )
    text = text.replace(
        "$$\\text{Complejidad}(\\text{Verificación}) \\ll \\text{Complejidad}(\\text{Generación}) \\quad \\text{en dominios formales cerrados (código, matemáticas)}$$",
        "```text\nComplejidad(Verificación) ≪ Complejidad(Generación)   [Dominios Formales Cerrados]\n```"
    )
    text = text.replace(
        "$$\\text{Complejidad}(\\text{Verificación}) \\approx \\text{Complejidad}(\\text{Generación}) \\quad \\text{en dominios abiertos en lenguaje natural}$$",
        "```text\nComplejidad(Verificación) ≈ Complejidad(Generación)   [Dominios Abiertos en Lenguaje Natural]\n```"
    )
    text = text.replace(
        "$$\\text{复杂度}(\\text{验证}) \\ll \\text{复杂度}(\\text{生成}) \\quad \\text{封闭形式化领域（数学、代码）}$$",
        "```text\n复杂度(验证) ≪ 复杂度(生成)   [封闭形式化领域: 数学、代码]\n```"
    )
    text = text.replace(
        "$$\\text{复杂度}(\\text{验证}) \\approx \\text{复杂度}(\\text{生成}) \\quad \\text{开放自然语言领域（文章、战略、谈判）}$$",
        "```text\n复杂度(验证) ≈ 复杂度(生成)   [开放自然语言领域: 文章、战略、谈判]\n```"
    )
    text = text.replace(
        "$$\\text{複雜度}(\\text{驗證}) \\ll \\text{複雜度}(\\text{生成}) \\quad \\text{封閉形式化領域（數學、程式碼）}$$",
        "```text\n複雜度(驗證) ≪ 複雜度(生成)   [封閉形式化領域: 數學、程式碼]\n```"
    )
    text = text.replace(
        "$$\\text{複雜度}(\\text{驗證}) \\approx \\text{複雜度}(\\text{生成}) \\quad \\text{開放自然語言領域（文章、戰略、談判）}$$",
        "```text\n複雜度(驗證) ≈ 複雜度(生成)   [開放自然語言領域: 文章、戰略、談判]\n```"
    )
    text = text.replace(
        "$$\\text{Komplexität}(\\text{Verifikation}) \\ll \\text{Komplexität}(\\text{Generierung}) \\quad \\text{in geschlossenen formalen Domänen (Code, Mathe)}$$",
        "```text\nKomplexität(Verifikation) ≪ Komplexität(Generierung)   [Geschlossene Formale Domänen]\n```"
    )
    text = text.replace(
        "$$\\text{Komplexität}(\\text{Verifikation}) \\approx \\text{Komplexität}(\\text{Generierung}) \\quad \\text{in offenen natürlichsprachlichen Domänen}$$",
        "```text\nKomplexität(Verifikation) ≈ Komplexität(Generierung)   [Offene Natürlichsprachliche Domänen]\n```"
    )
    text = text.replace(
        "$$\\text{Complexité}(\\text{Vérification}) \\ll \\text{Complexité}(\\text{Génération}) \\quad \\text{en domaines formels clos (maths, code, Lean 4)}$$",
        "```text\nComplexité(Vérification) ≪ Complexité(Génération)   [Domaines Formels Clos]\n```"
    )
    text = text.replace(
        "$$\\text{Complexité}(\\text{Vérification}) \\approx \\text{Complexité}(\\text{Génération}) \\quad \\text{en domaines ouverts en langage naturel}$$",
        "```text\nComplexité(Vérification) ≈ Complexité(Génération)   [Domaines Ouverts en Langage Naturel]\n```"
    )
    text = text.replace(
        "$$\\text{Complexidade}(\\text{Verificação}) \\ll \\text{Complexidade}(\\text{Geração}) \\quad \\text{em domínios formais fechados (matemática, código)}$$",
        "```text\nComplexidade(Verificação) ≪ Complexidade(Geração)   [Domínios Formais Fechados]\n```"
    )
    text = text.replace(
        "$$\\text{Complexidade}(\\text{Verificação}) \\approx \\text{Complexidade}(\\text{Geração}) \\quad \\text{em domínios abertos de linguagem natural}$$",
        "```text\nComplexidade(Verificação) ≈ Complexidade(Geração)   [Domínios Abertos de Linguagem Natural]\n```"
    )

    # 2. Inline formulas
    replacements = [
        (r"$(x_{\text{prompt}}, y_{\text{response}})$", "`(x_prompt, y_response)`"),
        (r"$r_\psi(x, y)$", "`r_ψ(x, y)`"),
        (r"$r_t = R(x, y_{1:t})$", "`r_t = R(x, y_{1:t})`"),
        (r"$r(x, y)$", "`r(x, y)`"),
        (r"$\pi_\theta$", "π_θ"),
        (r"$\text{Pass@}k$", "`Pass@k`"),
        (r"$\alpha \approx 0.34, \beta \approx 0.28$", "α ≈ 0.34, β ≈ 0.28"),
        (r"$10^{21}$", "10²¹"),
        (r"$10^{23}$", "10²³"),
        (r"$10^{25}$", "10²⁵"),
        (r"$10^{26}$", "10²⁶"),
        (r"$100\times$", "100×"),
        (r"$1,000\times$", "1,000×"),
        (r"$1\,000\times$", "1 000×"),
        (r"$1.000\times$", "1.000×"),
        (r"$C$", "C"),
        (r"$N$", "N"),
        (r"$D$", "D"),
        (r"$E$", "E"),
        (r"$A$", "A"),
        (r"$B$", "B"),
        (r"$n$", "n"),
        (r"$c$", "c"),
        (r"$k+1$", "`k+1`"),
        (r"$k$", "`k`"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
        
    return text

def main():
    base_dir = r"D:\ai\antigravity\global_blog\배포대기\2026-11-01-stanford-cs329a-1"
    files = glob.glob(os.path.join(base_dir, "**", "index.md"), recursive=True)
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        sanitized = sanitize_content(content)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(sanitized)
        print(f"Sanitized: {fpath} ({len(sanitized)} bytes)")

if __name__ == "__main__":
    main()
