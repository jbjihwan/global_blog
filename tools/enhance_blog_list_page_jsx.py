import re
from pathlib import Path

FILE_PATH = Path(r"D:\ai\antigravity\global_blog\src\theme\BlogListPage\index.tsx")
content = FILE_PATH.read_text(encoding="utf-8")

# 1. Update KNOWN_SLUG_DATES
if "'sdc-02-stack-spike-doctrine-hypotheses'" not in content:
    content = content.replace(
        "'sdc-01-architecture-klm-model': '2026-12-03',",
        "'sdc-02-stack-spike-doctrine-hypotheses': '2026-12-04',\n  'sdc-01-architecture-klm-model': '2026-12-03',"
    )

# 2. Update getEpisodeNumber
if "sdc-01-architecture-klm-model" not in content[content.find("function getEpisodeNumber"):]:
    content = content.replace(
        "function getEpisodeNumber(permalink: string): number {",
        """function getEpisodeNumber(permalink: string): number {
  if (permalink.includes('sdc-01-architecture-klm-model')) return 1;
  if (permalink.includes('sdc-02-stack-spike-doctrine-hypotheses')) return 2;
  const sdcM = permalink.match(/sdc-(\d+)/);
  if (sdcM) return parseInt(sdcM[1], 10);"""
    )

# 3. Enhance ProjectHubView signature & implementation if needed
# ProjectHubView currently maps projects. Let's make sure it handles empty state nicely.
old_hub_view = """function ProjectHubView({
  projects,
  postCounts,
  locale,
  btnExploreProject,
  btnUpcoming,
  onSelectProject,
}: {
  projects: ProjectInfo[];
  postCounts: Record<string, number>;
  locale: SupportedLocale;
  btnExploreProject: string;
  btnUpcoming: string;
  onSelectProject: (id: string) => void;
}) {
  return (
    <div className={styles.projectHubContainer}>
      <div className={styles.projectGrid}>"""

new_hub_view = """function ProjectHubView({
  projects,
  postCounts,
  locale,
  btnExploreProject,
  btnUpcoming,
  onSelectProject,
  emptyNotice,
}: {
  projects: ProjectInfo[];
  postCounts: Record<string, number>;
  locale: SupportedLocale;
  btnExploreProject: string;
  btnUpcoming: string;
  onSelectProject: (id: string) => void;
  emptyNotice?: string;
}) {
  return (
    <div className={styles.projectHubContainer}>
      {projects.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--ifm-color-emphasis-600)' }}>
          <p style={{ fontSize: '1.1rem', fontWeight: 600 }}>{emptyNotice || '포스트가 준비 중입니다.'}</p>
        </div>
      ) : (
      <div className={styles.projectGrid}>"""

if old_hub_view in content:
    content = content.replace(old_hub_view, new_hub_view)
    # also add closing parenthesis for ternary
    content = content.replace(
        "        })}\n      </div>\n    </div>\n  );\n}",
        "        })}\n      </div>\n      )}\n    </div>\n  );\n}"
    )

# 4. Update BlogListPageContent implementation
# Search for activeTab state
old_active_tab_state = """  // Active tab state
  const [activeTab, setActiveTab] = useState<
    'hub' | 'crisis_detection' | 'national_budget' | 'stanford_cs329a' | 'stanford_cs146s' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'all'
  >(isFirstPage ? 'hub' : 'all');"""

new_active_tab_state = """  // Taxonomy Filter states
  const [categoryFilter, setCategoryFilter] = useState<'all' | 'theory' | 'practice' | 'error'>('all');
  const [domainFilter, setDomainFilter] = useState<'all' | 'ai' | 'security'>('all');
  const [subTypeFilter, setSubTypeFilter] = useState<'all' | 'lecture' | 'definition' | 'history'>('all');

  // Active tab state
  const [activeTab, setActiveTab] = useState<
    'hub' | 'crisis_detection' | 'national_budget' | 'stanford_cs329a' | 'stanford_cs146s' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'sdc_replanning' | 'all'
  >(isFirstPage ? 'hub' : 'all');"""

if old_active_tab_state in content:
    content = content.replace(old_active_tab_state, new_active_tab_state)

# Update useEffect for hashes
old_use_effect = """  useEffect(() => {
    if (typeof window !== 'undefined') {
      const hash = window.location.hash.replace('#', '').toLowerCase();
      if (hash === 'crisis_detection' || hash === 'crisis' || hash === 'mental-crisis') {
        setActiveTab('crisis_detection');
      } else if (hash === 'national_budget' || hash === 'budget' || hash === 'national-budget') {
        setActiveTab('national_budget');
      } else if (hash === 'stanford_cs329a' || hash === 'cs329a' || hash === 'stanford-cs329a') {
        setActiveTab('stanford_cs329a');
      } else if (hash === 'stanford_cs146s' || hash === 'stanford' || hash === 'cs146s' || hash === 'stanford-cs146s') {
        setActiveTab('stanford_cs146s');
      } else if (hash === 'maeumjigi') {
        setActiveTab('maeumjigi');
      } else if (hash === 'rl_q_learning' || hash === 'rl') {
        setActiveTab('rl_q_learning');
      } else if (hash === 'anpr_vision' || hash === 'anpr' || hash === 'cv') {
        setActiveTab('anpr_vision');
      } else if (hash === 'security' || hash === 'infra') {
        setActiveTab('security');
      } else if (hash === 'all') {
        setActiveTab('all');
      } else if (hash === 'hub' || hash === 'projects') {
        setActiveTab('hub');
      }
    }
  }, []);"""

new_use_effect = """  useEffect(() => {
    if (typeof window !== 'undefined') {
      const hash = window.location.hash.replace('#', '').toLowerCase();
      if (hash === 'theory') {
        setCategoryFilter('theory');
        setActiveTab('hub');
      } else if (hash === 'practice') {
        setCategoryFilter('practice');
        setActiveTab('hub');
      } else if (hash === 'error' || hash === 'errors') {
        setCategoryFilter('error');
        setActiveTab('hub');
      } else if (hash === 'sdc' || hash === 'sdc_replanning' || hash === 'sdc-replanning') {
        setActiveTab('sdc_replanning');
      } else if (hash === 'crisis_detection' || hash === 'crisis' || hash === 'mental-crisis') {
        setActiveTab('crisis_detection');
      } else if (hash === 'national_budget' || hash === 'budget' || hash === 'national-budget') {
        setActiveTab('national_budget');
      } else if (hash === 'stanford_cs329a' || hash === 'cs329a' || hash === 'stanford-cs329a') {
        setActiveTab('stanford_cs329a');
      } else if (hash === 'stanford_cs146s' || hash === 'stanford' || hash === 'cs146s' || hash === 'stanford-cs146s') {
        setActiveTab('stanford_cs146s');
      } else if (hash === 'maeumjigi') {
        setActiveTab('maeumjigi');
      } else if (hash === 'rl_q_learning' || hash === 'rl') {
        setActiveTab('rl_q_learning');
      } else if (hash === 'anpr_vision' || hash === 'anpr' || hash === 'cv') {
        setActiveTab('anpr_vision');
      } else if (hash === 'security' || hash === 'infra') {
        setActiveTab('security');
      } else if (hash === 'all') {
        setActiveTab('all');
      } else if (hash === 'hub' || hash === 'projects') {
        setActiveTab('hub');
      }
    }
  }, []);"""

if old_use_effect in content:
    content = content.replace(old_use_effect, new_use_effect)

# Update handleSelectTab signature
old_handle_select_tab = """  const handleSelectTab = (
    tab: 'hub' | 'crisis_detection' | 'national_budget' | 'stanford_cs329a' | 'stanford_cs146s' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'all'
  ) => {
    setActiveTab(tab);
    if (typeof window !== 'undefined') {
      window.location.hash = tab === 'hub' ? 'projects' : tab;
    }
  };"""

new_handle_select_tab = """  const handleSelectTab = (
    tab: 'hub' | 'crisis_detection' | 'national_budget' | 'stanford_cs329a' | 'stanford_cs146s' | 'maeumjigi' | 'rl_q_learning' | 'anpr_vision' | 'security' | 'sdc_replanning' | 'all'
  ) => {
    setActiveTab(tab);
    if (typeof window !== 'undefined') {
      window.location.hash = tab === 'hub' ? 'projects' : tab;
    }
  };

  const handleSelectCategory = (cat: 'all' | 'theory' | 'practice' | 'error') => {
    setCategoryFilter(cat);
    setActiveTab('hub');
    setDomainFilter('all');
    setSubTypeFilter('all');
    if (typeof window !== 'undefined') {
      window.location.hash = cat === 'all' ? 'projects' : cat;
    }
  };"""

if old_handle_select_tab in content:
    content = content.replace(old_handle_select_tab, new_handle_select_tab)

# Update postCounts calculation
old_post_counts = """  const postCounts = useMemo(() => {
    return {
      crisis_detection: allSidebarItems.filter(isCrisis).length,
      national_budget: allSidebarItems.filter(isNationalBudget).length,
      stanford_cs329a: allSidebarItems.filter((item: any) => item.permalink.includes('stanford-cs329a')).length,
      stanford_cs146s: allSidebarItems.filter((item: any) => item.permalink.includes('stanford-cs146s')).length,
      maeumjigi: allSidebarItems.filter((item: any) => item.permalink.includes('maeumjigi')).length,
      anpr_vision: allSidebarItems.filter((item: any) => item.permalink.includes('vision-anpr')).length,
      rl_q_learning: allSidebarItems.filter((item: any) => item.permalink.includes('rl-qlearning')).length,
      security: allSidebarItems.filter(isSecurity).length,
    };
  }, [allSidebarItems]);"""

new_post_counts = """  const isSdc = (item: any) => item.permalink.includes('sdc-');
  const isTheory = (item: any) =>
    item.permalink.includes('stanford-cs329a') || item.permalink.includes('stanford-cs146s');
  const isPractice = (item: any) => !isTheory(item);
  const isErrorPost = (item: any) =>
    item.permalink.includes('vulnerability') ||
    item.permalink.includes('npm-overrides') ||
    item.permalink.includes('cloudflare-fix') ||
    item.permalink.includes('adsense') ||
    item.permalink.includes('sdc-01') ||
    item.permalink.includes('sdc-02') ||
    item.permalink.includes('nested-cv') ||
    item.permalink.includes('zero-probability-collapse') ||
    item.permalink.includes('extreme-value-bias') ||
    item.permalink.includes('inspector-portal') ||
    item.permalink.includes('security-hardening');

  const postCounts = useMemo(() => {
    return {
      sdc_replanning: allSidebarItems.filter(isSdc).length,
      crisis_detection: allSidebarItems.filter(isCrisis).length,
      national_budget: allSidebarItems.filter(isNationalBudget).length,
      stanford_cs329a: allSidebarItems.filter((item: any) => item.permalink.includes('stanford-cs329a')).length,
      stanford_cs146s: allSidebarItems.filter((item: any) => item.permalink.includes('stanford-cs146s')).length,
      maeumjigi: allSidebarItems.filter((item: any) => item.permalink.includes('maeumjigi')).length,
      anpr_vision: allSidebarItems.filter((item: any) => item.permalink.includes('vision-anpr')).length,
      rl_q_learning: allSidebarItems.filter((item: any) => item.permalink.includes('rl-qlearning')).length,
      security: allSidebarItems.filter(isSecurity).length,
      theory: allSidebarItems.filter(isTheory).length,
      practice: allSidebarItems.filter(isPractice).length,
      error: allSidebarItems.filter(isErrorPost).length,
      theory_ai: allSidebarItems.filter(isTheory).length,
      practice_ai: allSidebarItems.filter((i: any) => isPractice(i) && !isSecurity(i)).length,
      practice_security: allSidebarItems.filter(isSecurity).length,
    };
  }, [allSidebarItems]);"""

if old_post_counts in content:
    content = content.replace(old_post_counts, new_post_counts)

# Update projectPosts logic to support sdc_replanning
old_project_posts = """    if (activeTab === 'crisis_detection') {
      list = allSidebarItems.filter(isCrisis);"""

new_project_posts = """    if (activeTab === 'sdc_replanning') {
      list = allSidebarItems.filter(isSdc);
    } else if (activeTab === 'crisis_detection') {
      list = allSidebarItems.filter(isCrisis);"""

if old_project_posts in content:
    content = content.replace(old_project_posts, new_project_posts)

# Add filteredProjects for ProjectHubView
hub_filter_logic = """  // Filter projects in Hub according to Taxonomy Filter
  const filteredProjects = useMemo(() => {
    return content.projects.filter((proj) => {
      if (categoryFilter === 'theory') {
        if (proj.taxonomyL1 !== 'theory') return false;
        if (domainFilter === 'security') return false;
        if (subTypeFilter !== 'all' && subTypeFilter !== 'lecture') return false;
      } else if (categoryFilter === 'practice') {
        if (proj.taxonomyL1 !== 'practice') return false;
        if (domainFilter === 'ai' && proj.taxonomyL2 !== 'ai') return false;
        if (domainFilter === 'security' && proj.taxonomyL2 !== 'security') return false;
      }
      return true;
    });
  }, [content.projects, categoryFilter, domainFilter, subTypeFilter]);
"""

content = content.replace("  const allSidebarItems = sidebar?.items || [];", hub_filter_logic + "\n  const allSidebarItems = sidebar?.items || [];")

# Add anchors
anchors_target = '<span id="projects" aria-hidden="true" />'
anchors_replacement = """<span id="projects" aria-hidden="true" />
      <span id="theory" aria-hidden="true" />
      <span id="practice" aria-hidden="true" />
      <span id="error" aria-hidden="true" />
      <span id="errors" aria-hidden="true" />
      <span id="sdc" aria-hidden="true" />
      <span id="sdc_replanning" aria-hidden="true" />"""
content = content.replace(anchors_target, anchors_replacement)

# Update hubHeader to include Taxonomy Navigation Container
old_tab_bar = """        {/* Tab Switcher with Dynamic Counts */}
        <div className={styles.tabBar}>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'hub' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('hub')}
          >
            {content.tabHub}
          </button>"""

new_tax_nav = """        {/* 3-Tier Taxonomy Navigation Bar */}
        <div className={styles.taxonomyNavContainer}>
          {/* Level 1: Major Classification (전체, 1. 이론, 2. 실습, 3. 오류) */}
          <div className={styles.taxonomyTier1Row}>
            <button
              type="button"
              className={clsx(styles.taxonomyMainButton, categoryFilter === 'all' && styles.taxonomyMainButtonActive)}
              onClick={() => handleSelectCategory('all')}
            >
              <span>🌐</span> {content.taxAll} ({formatCount(allSidebarItems.length, locale)})
            </button>
            <button
              type="button"
              className={clsx(styles.taxonomyMainButton, categoryFilter === 'theory' && styles.taxonomyMainButtonActive)}
              onClick={() => handleSelectCategory('theory')}
            >
              <span>📘</span> {content.taxTheory} ({formatCount(postCounts.theory, locale)})
            </button>
            <button
              type="button"
              className={clsx(styles.taxonomyMainButton, categoryFilter === 'practice' && styles.taxonomyMainButtonActive)}
              onClick={() => handleSelectCategory('practice')}
            >
              <span>🛠️</span> {content.taxPractice} ({formatCount(postCounts.practice, locale)})
            </button>
            <button
              type="button"
              className={clsx(styles.taxonomyMainButton, categoryFilter === 'error' && styles.taxonomyMainButtonActive)}
              onClick={() => handleSelectCategory('error')}
            >
              <span>⚠️</span> {content.taxError} ({formatCount(postCounts.error, locale)})
            </button>
          </div>

          {/* Sub-Filters: shown when 'theory' is active */}
          {categoryFilter === 'theory' && (
            <div className={styles.taxonomySubFilterPanel}>
              <div className={styles.filterRow}>
                <span className={styles.filterLabel}>{content.taxDomainLabel}:</span>
                <button
                  type="button"
                  className={clsx(styles.filterPill, domainFilter === 'all' && styles.filterPillActive)}
                  onClick={() => setDomainFilter('all')}
                >
                  {content.taxDomainAll}
                </button>
                <button
                  type="button"
                  className={clsx(styles.filterPill, domainFilter === 'ai' && styles.filterPillActive)}
                  onClick={() => setDomainFilter('ai')}
                >
                  {content.taxDomainAi} ({formatCount(postCounts.theory_ai, locale)})
                </button>
                <button
                  type="button"
                  className={clsx(styles.filterPill, domainFilter === 'security' && styles.filterPillActive)}
                  onClick={() => setDomainFilter('security')}
                >
                  {content.taxDomainSecurity} (0)
                </button>
              </div>
              <div className={styles.filterRow}>
                <span className={styles.filterLabel}>{content.taxTypeLabel}:</span>
                <button
                  type="button"
                  className={clsx(styles.filterPill, subTypeFilter === 'all' && styles.filterPillActive)}
                  onClick={() => setSubTypeFilter('all')}
                >
                  {content.taxTypeAll}
                </button>
                <button
                  type="button"
                  className={clsx(styles.filterPill, subTypeFilter === 'lecture' && styles.filterPillActive)}
                  onClick={() => setSubTypeFilter('lecture')}
                >
                  {content.taxTypeLecture} ({formatCount(postCounts.theory, locale)})
                </button>
                <button
                  type="button"
                  className={clsx(styles.filterPill, subTypeFilter === 'definition' && styles.filterPillActive)}
                  onClick={() => setSubTypeFilter('definition')}
                >
                  {content.taxTypeDef} (0)
                </button>
                <button
                  type="button"
                  className={clsx(styles.filterPill, subTypeFilter === 'history' && styles.filterPillActive)}
                  onClick={() => setSubTypeFilter('history')}
                >
                  {content.taxTypeHistory} (0)
                </button>
              </div>
            </div>
          )}

          {/* Sub-Filters: shown when 'practice' is active */}
          {categoryFilter === 'practice' && (
            <div className={styles.taxonomySubFilterPanel}>
              <div className={styles.filterRow}>
                <span className={styles.filterLabel}>{content.taxDomainLabel}:</span>
                <button
                  type="button"
                  className={clsx(styles.filterPill, domainFilter === 'all' && styles.filterPillActive)}
                  onClick={() => setDomainFilter('all')}
                >
                  {content.taxDomainAll}
                </button>
                <button
                  type="button"
                  className={clsx(styles.filterPill, domainFilter === 'ai' && styles.filterPillActive)}
                  onClick={() => setDomainFilter('ai')}
                >
                  {content.taxDomainAi} ({formatCount(postCounts.practice_ai, locale)})
                </button>
                <button
                  type="button"
                  className={clsx(styles.filterPill, domainFilter === 'security' && styles.filterPillActive)}
                  onClick={() => setDomainFilter('security')}
                >
                  {content.taxDomainSecurity} ({formatCount(postCounts.practice_security, locale)})
                </button>
              </div>
            </div>
          )}

          {/* Error Notice: shown when 'error' is active */}
          {categoryFilter === 'error' && (
            <div className={styles.errorArchiveNotice}>
              <h4 className={styles.errorArchiveTitle}>
                <span>⚠️</span> {content.taxErrorTitle}
              </h4>
              <p className={styles.errorArchiveDesc}>
                {content.taxErrorDesc}
              </p>
            </div>
          )}
        </div>

        {/* Tab Switcher with Dynamic Counts */}
        <div className={styles.tabBar}>
          <button
            type="button"
            className={clsx(styles.tabButton, activeTab === 'hub' && styles.tabButtonActive)}
            onClick={() => handleSelectTab('hub')}
          >
            {content.tabHub}
          </button>
          <button
            type="button"
            className={clsx(
              styles.tabButton,
              activeTab === 'sdc_replanning' && styles.tabButtonActive
            )}
            onClick={() => handleSelectTab('sdc_replanning')}
          >
            {`${content.tabSdc} (${formatCount(postCounts.sdc_replanning, locale)})`}
          </button>"""

content = content.replace(old_tab_bar, new_tax_nav)

# Update ProjectHubView call to pass filteredProjects and emptyNotice
content = content.replace(
    "projects={content.projects}",
    "projects={filteredProjects}"
)
content = content.replace(
    "btnUpcoming={content.btnUpcoming}",
    "btnUpcoming={content.btnUpcoming}\n            emptyNotice={content.emptyNotice}"
)

# Update banner title and description in project view
old_banner_title = """                {activeTab === 'crisis_detection'
                  ? `${content.bannerCrisisTitle} (${formatCount(postCounts.crisis_detection, locale)})`"""

new_banner_title = """                {activeTab === 'sdc_replanning'
                  ? `${content.bannerSdcTitle} (${formatCount(postCounts.sdc_replanning, locale)})`
                  : activeTab === 'crisis_detection'
                  ? `${content.bannerCrisisTitle} (${formatCount(postCounts.crisis_detection, locale)})`"""

if old_banner_title in content:
    content = content.replace(old_banner_title, new_banner_title)

old_banner_desc = """                {activeTab === 'crisis_detection'
                  ? content.bannerCrisisDesc"""

new_banner_desc = """                {activeTab === 'sdc_replanning'
                  ? content.bannerSdcDesc
                  : activeTab === 'crisis_detection'
                  ? content.bannerCrisisDesc"""

if old_banner_desc in content:
    content = content.replace(old_banner_desc, new_banner_desc)

FILE_PATH.write_text(content, encoding="utf-8")
print("[+] Enhanced BlogListPage JSX logic successfully.")
