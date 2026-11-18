# -*- coding: utf-8 -*-
"""BlogListPage/index.tsx 에서:
1) 0편인 프로젝트 카드·탭·이론 버튼을 동적으로 숨김(postCounts > 0 필터)
2) KNOWN_SLUG_DATES의 미래 날짜를 실제 과거 날짜로 갱신하고 신규 python-urlopen 포스트 매핑 추가
3) 번들 내 'Suicide' / '자살' 문자열 완전 제거
"""
import pathlib

ROOT = pathlib.Path(r"D:\ai\antigravity\global_blog")
TARGET = ROOT / "src" / "theme" / "BlogListPage" / "index.tsx"


def main():
    txt = TARGET.read_text(encoding="utf-8")

    # 1. Sanitize any sensitive words in I18N_DATA
    for old_w, new_w in [
        ("자살/위기", "임상 위기"),
        ("자살", "위기"),
        ("Suicide Risk", "Clinical Risk"),
        ("suicide", "clinical"),
        ("Suicida", "Clínica"),
        ("自殺・", ""),
    ]:
        txt = txt.replace(old_w, new_w)

    # 2. Update KNOWN_SLUG_DATES
    old_dates_block = """const KNOWN_SLUG_DATES: Record<string, string> = {

  'sdc-02-stack-spike-doctrine-hypotheses': '2026-12-04',

  'sdc-01-architecture-klm-model': '2026-12-03',

  'national-budget-surveillance-automated-audit-ledger': '2026-12-02',

  'google-adsense-low-value-content-cloudflare-fix': '2026-12-01',

  'national-budget-education-grant-audit': '2026-11-30',

  'national-budget-local-subsidy-ehojo-audit': '2026-11-29',

  'npm-overrides-transitive-vulnerability-fix': '2026-11-28',"""

    new_dates_block = """const KNOWN_SLUG_DATES: Record<string, string> = {

  'python-urlopen-timeout-dns-hang-windows-fix': '2026-11-16',

  'sdc-03-deterministic-jcs-ed25519-fragmentation': '2026-11-14',

  'sdc-02-stack-spike-doctrine-hypotheses': '2026-11-12',

  'sdc-01-architecture-klm-model': '2026-11-10',

  'npm-overrides-transitive-vulnerability-fix': '2026-11-05',"""

    assert old_dates_block in txt, "old_dates_block not found"
    txt = txt.replace(old_dates_block, new_dates_block, 1)

    # 3. Include python-urlopen in isSecurity and isErrorPost
    old_sec = "    item.permalink.includes('npm-overrides') ||\n\n    item.permalink.includes('vulnerability');"
    new_sec = "    item.permalink.includes('npm-overrides') ||\n\n    item.permalink.includes('python-urlopen') ||\n\n    item.permalink.includes('vulnerability');"
    assert old_sec in txt, "old_sec not found"
    txt = txt.replace(old_sec, new_sec, 1)

    old_err = "    item.permalink.includes('vulnerability') ||"
    new_err = "    item.permalink.includes('python-urlopen') ||\n\n    item.permalink.includes('vulnerability') ||"
    assert old_err in txt, "old_err not found"
    txt = txt.replace(old_err, new_err, 1)

    # 4. Filter ProjectHubView projects by postCounts[proj.id] > 0
    old_hub_map = "{projects.map((proj) => {"
    new_hub_map = "{projects.filter((proj) => (postCounts[proj.id] || 0) > 0).map((proj) => {"
    assert old_hub_map in txt, "old_hub_map not found"
    txt = txt.replace(old_hub_map, new_hub_map, 1)

    # 5. Only show Theory button when postCounts.theory > 0
    old_theory_btn = """            <button

              type="button"

              className={clsx(styles.taxonomyMainButton, categoryFilter === 'theory' && styles.taxonomyMainButtonActive)}

              onClick={() => handleSelectCategory('theory')}

            >

              <span>📘</span> {content.taxTheory} ({formatCount(postCounts.theory, locale)})

            </button>"""
    new_theory_btn = """            {postCounts.theory > 0 && (
            <button

              type="button"

              className={clsx(styles.taxonomyMainButton, categoryFilter === 'theory' && styles.taxonomyMainButtonActive)}

              onClick={() => handleSelectCategory('theory')}

            >

              <span>📘</span> {content.taxTheory} ({formatCount(postCounts.theory, locale)})

            </button>
            )}"""
    assert old_theory_btn in txt, "old_theory_btn not found"
    txt = txt.replace(old_theory_btn, new_theory_btn, 1)

    # 6. Only show tabs with > 0 posts in .tabBar
    for tab_id, label_expr in [
        ("crisis_detection", "content.tabCrisis"),
        ("national_budget", "content.tabBudget"),
        ("stanford_cs329a", "content.tabCs329a"),
        ("stanford_cs146s", "content.tabStanford"),
    ]:
        old_tab = f"""          <button

            type="button"

            className={{clsx(

              styles.tabButton,

              activeTab === '{tab_id}' && styles.tabButtonActive

            )}}

            onClick={{() => handleSelectTab('{tab_id}')}}

          >

            {{`${{{label_expr}}} (${{formatCount(postCounts.{tab_id}, locale)}})`}}

          </button>"""
        new_tab = f"""          {{postCounts.{tab_id} > 0 && (
          <button

            type="button"

            className={{clsx(

              styles.tabButton,

              activeTab === '{tab_id}' && styles.tabButtonActive

            )}}

            onClick={{() => handleSelectTab('{tab_id}')}}

          >

            {{`${{{label_expr}}} (${{formatCount(postCounts.{tab_id}, locale)}})`}}

          </button>
          )}}"""
        assert old_tab in txt, f"old_tab not found for {tab_id}"
        txt = txt.replace(old_tab, new_tab, 1)

    TARGET.write_text(txt, encoding="utf-8")
    print("Updated BlogListPage/index.tsx successfully.")


if __name__ == "__main__":
    main()
