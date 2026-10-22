# -*- coding: utf-8 -*-
import re

target_file = r"D:\ai\antigravity\global_blog\src\theme\BlogListPage\index.tsx"
with open(target_file, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update LocaleContent interface
old_interface = """  tabSecurity: string;
  tabAll: string;
  bannerMaeumjigiTitle: string;
  bannerMaeumjigiDesc: string;
  bannerRlTitle: string;
  bannerRlDesc: string;
  bannerAnprTitle: string;
  bannerAnprDesc: string;
  bannerSecurityTitle: string;
  bannerSecurityDesc: string;
  bannerAllTitle: string;"""

new_interface = """  tabSecurity: string;
  tabStanford: string;
  tabAll: string;
  bannerMaeumjigiTitle: string;
  bannerMaeumjigiDesc: string;
  bannerRlTitle: string;
  bannerRlDesc: string;
  bannerAnprTitle: string;
  bannerAnprDesc: string;
  bannerSecurityTitle: string;
  bannerSecurityDesc: string;
  bannerStanfordTitle: string;
  bannerStanfordDesc: string;
  bannerAllTitle: string;"""

assert old_interface in code, "old_interface not found"
code = code.replace(old_interface, new_interface, 1)

# 2. Update KO I18N
old_ko_tabs = """    tabSecurity: '보안 & 엔지니어링 (1편)',
    tabAll: '전체 글 피드',
    bannerMaeumjigiTitle: '프로젝트: 마음지기 (Maeumjigi Capstone Dev Log)',"""

new_ko_tabs = """    tabSecurity: '보안 & 엔지니어링 (1편)',
    tabStanford: '스탠포드 CS146S (1편)',
    tabAll: '전체 글 피드',
    bannerMaeumjigiTitle: '프로젝트: 마음지기 (Maeumjigi Capstone Dev Log)',"""

assert old_ko_tabs in code, "old_ko_tabs not found"
code = code.replace(old_ko_tabs, new_ko_tabs, 1)

old_ko_banners = """    bannerSecurityTitle: '프로젝트: 보안 & 웹 엔지니어링',
    bannerSecurityDesc: '정적 사이트 심층 보안 강화, 위협 모델링 및 npm 공급망 취약점 방어',
    bannerAllTitle: '전체 개발 일지 피드',"""

new_ko_banners = """    bannerSecurityTitle: '프로젝트: 보안 & 웹 엔지니어링',
    bannerSecurityDesc: '정적 사이트 심층 보안 강화, 위협 모델링 및 npm 공급망 취약점 방어',
    bannerStanfordTitle: '프로젝트: 스탠포드 CS146S (The Modern Software Developer)',
    bannerStanfordDesc: 'AI 에이전트 시대의 현대 소프트웨어 개발론: 스펙 주도 개발(SDD), 루프 엔지니어링, MCP 표준 아키텍처',
    bannerAllTitle: '전체 개발 일지 피드',"""

assert old_ko_banners in code, "old_ko_banners not found"
code = code.replace(old_ko_banners, new_ko_banners, 1)

old_ko_proj = """    projects: [
      {
        id: 'maeumjigi',"""

new_ko_proj = """    projects: [
      {
        id: 'stanford_cs146s',
        name: '스탠포드 CS146S',
        badge: 'Active · 1편',
        badgeType: 'active',
        category: '소프트웨어 공학 / AI 에이전트',
        icon: 'stanford_cs146s',
        subtitle: '스탠포드 대학교 현대 소프트웨어 개발자 강의 시리즈',
        description:
          '수동 코딩에서 AI 에이전트 지휘자로의 대전환. 스펙 주도 개발(SDD), 루프 엔지니어링, 모델 컨텍스트 프로토콜(MCP)과 현대 풀스택 개발 방법론 완벽 해설.',
        techTags: ['Stanford CS146S', 'Agentic Workflows', 'Spec-Driven', 'MCP', 'CI/CD'],
        postCountText: '개발일지 보러가기 (1편) →',
        hasPosts: true,
      },
      {
        id: 'maeumjigi',"""

assert old_ko_proj in code, "old_ko_proj not found"
code = code.replace(old_ko_proj, new_ko_proj, 1)

# 3. Update EN I18N
old_en_tabs = """    tabSecurity: 'Security & Infra (1 Post)',
    tabAll: 'All Posts Feed',
    bannerMaeumjigiTitle: 'Project: Maeumjigi (Capstone Dev Log)',"""

new_en_tabs = """    tabSecurity: 'Security & Infra (1 Post)',
    tabStanford: 'Stanford CS146S (1 Post)',
    tabAll: 'All Posts Feed',
    bannerMaeumjigiTitle: 'Project: Maeumjigi (Capstone Dev Log)',"""

assert old_en_tabs in code, "old_en_tabs not found"
code = code.replace(old_en_tabs, new_en_tabs, 1)

old_en_banners = """    bannerSecurityTitle: 'Project: Security & Web Engineering',
    bannerSecurityDesc: 'Static site security hardening, threat modeling, and npm supply chain defense',
    bannerAllTitle: 'All Dev Logs Feed',"""

new_en_banners = """    bannerSecurityTitle: 'Project: Security & Web Engineering',
    bannerSecurityDesc: 'Static site security hardening, threat modeling, and npm supply chain defense',
    bannerStanfordTitle: 'Project: Stanford CS146S (The Modern Software Developer)',
    bannerStanfordDesc: 'Modern software engineering in the age of AI agents: Spec-Driven Development, Loop Engineering, and Model Context Protocol (MCP)',
    bannerAllTitle: 'All Dev Logs Feed',"""

assert old_en_banners in code, "old_en_banners not found"
code = code.replace(old_en_banners, new_en_banners, 1)

old_en_proj = """    projects: [
      {
        id: 'maeumjigi',
        name: 'Maeumjigi',
        badge: 'Active · 23 Posts',"""

new_en_proj = """    projects: [
      {
        id: 'stanford_cs146s',
        name: 'Stanford CS146S',
        badge: 'Active · 1 Post',
        badgeType: 'active',
        category: 'Software Engineering / AI Agents',
        icon: 'stanford_cs146s',
        subtitle: 'Stanford University Modern Software Developer Series',
        description:
          'The paradigm shift from syntax typing to AI agent orchestration. Comprehensive breakdowns of Spec-Driven Development (SDD), Loop Engineering, and Model Context Protocol (MCP).',
        techTags: ['Stanford CS146S', 'Agentic Workflows', 'Spec-Driven', 'MCP', 'CI/CD'],
        postCountText: 'Explore Dev Logs (1 Post) →',
        hasPosts: true,
      },
      {
        id: 'maeumjigi',
        name: 'Maeumjigi',
        badge: 'Active · 23 Posts',"""

assert old_en_proj in code, "old_en_proj not found"
code = code.replace(old_en_proj, new_en_proj, 1)

# 4. Update JA I18N
old_ja_tabs = """    tabSecurity: 'セキュリティ＆インフラ (1編)',
    tabAll: '全記事フィード',
    bannerMaeumjigiTitle: 'プロジェクト: マウムジギ (卒業研究 開発日誌)',"""

new_ja_tabs = """    tabSecurity: 'セキュリティ＆インフラ (1編)',
    tabStanford: 'スタンフォード CS146S (1編)',
    tabAll: '全記事フィード',
    bannerMaeumjigiTitle: 'プロジェクト: マウムジギ (卒業研究 開発日誌)',"""

assert old_ja_tabs in code, "old_ja_tabs not found"
code = code.replace(old_ja_tabs, new_ja_tabs, 1)

old_ja_banners = """    bannerSecurityTitle: 'プロジェクト: セキュリティ＆ウェブ工学',
    bannerSecurityDesc: '静적サイト深層セキュリティ強化、脅威モデリングおよびnpmサプライチェーン防御',
    bannerAllTitle: '全開発日誌フィード',"""

new_ja_banners = """    bannerSecurityTitle: 'プロジェクト: セキュリティ＆ウェブ工学',
    bannerSecurityDesc: '静적サイト深層セキュリティ強化、脅威モデリングおよびnpmサプライチェーン防御',
    bannerStanfordTitle: 'プロジェクト: スタンフォード CS146S (現代ソフトウェア開発者)',
    bannerStanfordDesc: 'AIエージェント時代の現代ソフトウェア開発論：仕様駆動開発(SDD)、ループエンジニアリング、MCP規格',
    bannerAllTitle: '全開発日誌フィード',"""

# In JA source, let's check exact text
if "bannerSecurityTitle: 'プロジェクト: セキュリティ＆ウェブ工学'" in code:
    code = re.sub(
        r"(bannerSecurityTitle:\s*'プロジェクト:\s*セキュリティ＆ウェブ工学',\s*bannerSecurityDesc:\s*'.*?',\s*bannerAllTitle:\s*'全開発日誌フィード',)",
        r"bannerSecurityTitle: 'プロジェクト: セキュリティ＆ウェブ工学',\n    bannerSecurityDesc: '静적サイト深層セキュリティ強化、脅威モデリングおよびnpmサプライチェーン防御',\n    bannerStanfordTitle: 'プロジェクト: スタンフォード CS146S (現代ソフトウェア開発者)',\n    bannerStanfordDesc: 'AIエージェント時代の現代ソフトウェア開発論：仕様駆動開発(SDD)、ループエンジニアリング、MCP規格',\n    bannerAllTitle: '全開発日誌フィード',",
        code
    )

old_ja_proj = """    projects: [
      {
        id: 'maeumjigi',
        name: 'マウムジギ (Maeumjigi)',
        badge: 'Active · 23編',"""

new_ja_proj = """    projects: [
      {
        id: 'stanford_cs146s',
        name: 'スタンフォード CS146S',
        badge: 'Active · 1編',
        badgeType: 'active',
        category: 'ソフトウェア工学 / AIエージェント',
        icon: 'stanford_cs146s',
        subtitle: 'スタンフォード大学 現代ソフトウェア開発者講義シリーズ',
        description:
          '手動コーディングからAIエージェント指揮者への大転換。仕様駆動開発（SDD）、ループエンジニアリング、モデルコンテキストプロトコル（MCP）の完全解説。',
        techTags: ['Stanford CS146S', 'Agentic Workflows', 'Spec-Driven', 'MCP', 'CI/CD'],
        postCountText: '開発日誌を見る (1編) →',
        hasPosts: true,
      },
      {
        id: 'maeumjigi',
        name: 'マウムジギ (Maeumjigi)',
        badge: 'Active · 23編',"""

assert old_ja_proj in code, "old_ja_proj not found"
code = code.replace(old_ja_proj, new_ja_proj, 1)

# 5. Update ES I18N
old_es_tabs = """    tabSecurity: 'Seguridad e Infra (1 Post)',
    tabAll: 'Todos los Posts',
    bannerMaeumjigiTitle: 'Proyecto: Maeumjigi (Diario de Desarrollo Capstone)',"""

new_es_tabs = """    tabSecurity: 'Seguridad e Infra (1 Post)',
    tabStanford: 'Stanford CS146S (1 Post)',
    tabAll: 'Todos los Posts',
    bannerMaeumjigiTitle: 'Proyecto: Maeumjigi (Diario de Desarrollo Capstone)',"""

assert old_es_tabs in code, "old_es_tabs not found"
code = code.replace(old_es_tabs, new_es_tabs, 1)

old_es_banners = """    bannerSecurityTitle: 'Proyecto: Seguridad e Ingeniería Web',
    bannerSecurityDesc: 'Blindaje de seguridad en sitios estáticos, modelado de amenazas y defensa de la cadena npm',
    bannerAllTitle: 'Todos los Diarios de Desarrollo',"""

new_es_banners = """    bannerSecurityTitle: 'Proyecto: Seguridad e Ingeniería Web',
    bannerSecurityDesc: 'Blindaje de seguridad en sitios estáticos, modelado de amenazas y defensa de la cadena npm',
    bannerStanfordTitle: 'Proyecto: Stanford CS146S (El Desarrollador de Software Moderno)',
    bannerStanfordDesc: 'Ingeniería de software en la era de los agentes de IA: Desarrollo Guiado por Especificaciones (SDD), Loop Engineering y MCP',
    bannerAllTitle: 'Todos los Diarios de Desarrollo',"""

assert old_es_banners in code, "old_es_banners not found"
code = code.replace(old_es_banners, new_es_banners, 1)

old_es_proj = """    projects: [
      {
        id: 'maeumjigi',
        name: 'Maeumjigi',
        badge: 'Activo · 23 Posts',"""

new_es_proj = """    projects: [
      {
        id: 'stanford_cs146s',
        name: 'Stanford CS146S',
        badge: 'Activo · 1 Post',
        badgeType: 'active',
        category: 'Ingeniería de Software / Agentes de IA',
        icon: 'stanford_cs146s',
        subtitle: 'Serie El Desarrollador de Software Moderno de Stanford',
        description:
          'El cambio de paradigma de escribir código a orquestar agentes. Desgloses de Desarrollo Guiado por Especificaciones (SDD), Loop Engineering y Model Context Protocol (MCP).',
        techTags: ['Stanford CS146S', 'Agentic Workflows', 'Spec-Driven', 'MCP', 'CI/CD'],
        postCountText: 'Ver Diarios de Desarrollo (1 Post) →',
        hasPosts: true,
      },
      {
        id: 'maeumjigi',
        name: 'Maeumjigi',
        badge: 'Activo · 23 Posts',"""

assert old_es_proj in code, "old_es_proj not found"
code = code.replace(old_es_proj, new_es_proj, 1)

# 6. Update getEpisodeNumber
old_ep = "const m = permalink.match(/(?:maeumjigi|vision-anpr|rl-qlearning)-(\\d+)/);"
new_ep = "const m = permalink.match(/(?:maeumjigi|vision-anpr|rl-qlearning|stanford-cs146s)-(\\d+)/);"
assert old_ep in code, "old_ep not found"
code = code.replace(old_ep, new_ep, 1)

# 7. Update activeTab state type
old_tab_state = "  const [activeTab, setActiveTab] = useState<\n    'hub' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'all'\n  >(isFirstPage ? 'hub' : 'all');"
new_tab_state = "  const [activeTab, setActiveTab] = useState<\n    'hub' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'stanford_cs146s' | 'all'\n  >(isFirstPage ? 'hub' : 'all');"
assert old_tab_state in code, "old_tab_state not found"
code = code.replace(old_tab_state, new_tab_state, 1)

# 8. Update useEffect hash parsing
old_hash = """      } else if (hash === 'security' || hash === 'infra') {
        setActiveTab('security');
      } else if (hash === 'all') {"""

new_hash = """      } else if (hash === 'security' || hash === 'infra') {
        setActiveTab('security');
      } else if (hash === 'stanford_cs146s' || hash === 'stanford' || hash === 'cs146s') {
        setActiveTab('stanford_cs146s');
      } else if (hash === 'all') {"""

assert old_hash in code, "old_hash not found"
code = code.replace(old_hash, new_hash, 1)

# 9. Update handleSelectTab signature
old_handler = "  const handleSelectTab = (\n    tab: 'hub' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'all'\n  ) => {"
new_handler = "  const handleSelectTab = (\n    tab: 'hub' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'stanford_cs146s' | 'all'\n  ) => {"
assert old_handler in code, "old_handler not found"
code = code.replace(old_handler, new_handler, 1)

# 10. Update projectPosts filter
old_filter = """    } else if (activeTab === 'security') {
      list = allSidebarItems.filter((item: any) =>
        item.permalink.includes('security') || item.permalink.includes('static-site-security')
      );
    } else if (activeTab === 'all') {"""

new_filter = """    } else if (activeTab === 'security') {
      list = allSidebarItems.filter((item: any) =>
        item.permalink.includes('security') || item.permalink.includes('static-site-security')
      );
    } else if (activeTab === 'stanford_cs146s') {
      list = allSidebarItems.filter((item: any) => item.permalink.includes('stanford-cs146s'));
    } else if (activeTab === 'all') {"""

assert old_filter in code, "old_filter not found"
code = code.replace(old_filter, new_filter, 1)

# 11. Update anchors
old_anchors = """      <span id="security" aria-hidden="true" />
      <span id="all" aria-hidden="true" />"""

new_anchors = """      <span id="security" aria-hidden="true" />
      <span id="stanford_cs146s" aria-hidden="true" />
      <span id="stanford" aria-hidden="true" />
      <span id="cs146s" aria-hidden="true" />
      <span id="all" aria-hidden="true" />"""

assert old_anchors in code, "old_anchors not found"
code = code.replace(old_anchors, new_anchors, 1)

# 12. Update Tab Buttons
old_tab_buttons = """          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'security' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('security')}
          >
            {content.tabSecurity}
          </button>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'all' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('all')}
          >
            {content.tabAll}
          </button>"""

new_tab_buttons = """          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'stanford_cs146s' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('stanford_cs146s')}
          >
            {content.tabStanford}
          </button>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'security' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('security')}
          >
            {content.tabSecurity}
          </button>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'all' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('all')}
          >
            {content.tabAll}
          </button>"""

assert old_tab_buttons in code, "old_tab_buttons not found"
code = code.replace(old_tab_buttons, new_tab_buttons, 1)

# 13. Update Ternary Title and Desc in banner
old_title_ternary = """                  : activeTab === 'security'
                  ? content.bannerSecurityTitle
                  : content.bannerAllTitle}"""

new_title_ternary = """                  : activeTab === 'security'
                  ? content.bannerSecurityTitle
                  : activeTab === 'stanford_cs146s'
                  ? content.bannerStanfordTitle
                  : content.bannerAllTitle}"""

assert old_title_ternary in code, "old_title_ternary not found"
code = code.replace(old_title_ternary, new_title_ternary, 1)

old_desc_ternary = """                  : activeTab === 'security'
                  ? content.bannerSecurityDesc
                  : content.bannerAllDesc}"""

new_desc_ternary = """                  : activeTab === 'security'
                  ? content.bannerSecurityDesc
                  : activeTab === 'stanford_cs146s'
                  ? content.bannerStanfordDesc
                  : content.bannerAllDesc}"""

assert old_desc_ternary in code, "old_desc_ternary not found"
code = code.replace(old_desc_ternary, new_desc_ternary, 1)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(code)

print("BlogListPage/index.tsx successfully updated with Stanford CS146S!")
