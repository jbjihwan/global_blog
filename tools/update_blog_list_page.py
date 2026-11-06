import re
from pathlib import Path

FILE_PATH = Path(r"D:\ai\antigravity\global_blog\src\theme\BlogListPage\index.tsx")
content = FILE_PATH.read_text(encoding="utf-8")

# 1. Update ProjectInfo interface
old_proj_info = """interface ProjectInfo {
  id: string;
  name: string;
  badgeType: 'active' | 'upcoming';
  category: string;
  icon: string;
  subtitle: string;
  description: string;
  techTags: string[];
  hasPosts: boolean;
  upcomingBadgeText?: string;
}"""

new_proj_info = """interface ProjectInfo {
  id: string;
  name: string;
  badgeType: 'active' | 'upcoming';
  category: string;
  icon: string;
  subtitle: string;
  description: string;
  techTags: string[];
  hasPosts: boolean;
  upcomingBadgeText?: string;
  taxonomyL1?: 'theory' | 'practice' | 'error';
  taxonomyL2?: 'ai' | 'security';
  taxonomyL3?: string;
}"""

if old_proj_info in content:
    content = content.replace(old_proj_info, new_proj_info)

# 2. Update LocaleContent interface
old_loc_content = """interface LocaleContent {
  hubTitle: string;
  hubSubtitle: string;
  tabHub: string;
  tabCrisis: string;
  tabBudget: string;
  tabCs329a: string;
  tabStanford: string;
  tabMaeumjigi: string;
  tabAnpr: string;
  tabRl: string;
  tabSecurity: string;
  tabAll: string;
  bannerCrisisTitle: string;
  bannerCrisisDesc: string;
  bannerBudgetTitle: string;
  bannerBudgetDesc: string;
  bannerCs329aTitle: string;
  bannerCs329aDesc: string;
  bannerStanfordTitle: string;
  bannerStanfordDesc: string;
  bannerMaeumjigiTitle: string;
  bannerMaeumjigiDesc: string;
  bannerAnprTitle: string;
  bannerAnprDesc: string;
  bannerRlTitle: string;
  bannerRlDesc: string;
  bannerSecurityTitle: string;
  bannerSecurityDesc: string;
  bannerAllTitle: string;
  bannerAllDesc: string;"""

new_loc_content = """interface LocaleContent {
  hubTitle: string;
  hubSubtitle: string;
  tabHub: string;
  tabCrisis: string;
  tabBudget: string;
  tabCs329a: string;
  tabStanford: string;
  tabMaeumjigi: string;
  tabAnpr: string;
  tabRl: string;
  tabSecurity: string;
  tabSdc: string;
  tabAll: string;
  // Taxonomy L1
  taxAll: string;
  taxTheory: string;
  taxPractice: string;
  taxError: string;
  // Taxonomy L2
  taxDomainLabel: string;
  taxDomainAll: string;
  taxDomainAi: string;
  taxDomainSecurity: string;
  // Taxonomy L3
  taxTypeLabel: string;
  taxTypeAll: string;
  taxTypeLecture: string;
  taxTypeDef: string;
  taxTypeHistory: string;
  taxProjectLabel: string;
  taxErrorTitle: string;
  taxErrorDesc: string;
  // Banners
  bannerCrisisTitle: string;
  bannerCrisisDesc: string;
  bannerBudgetTitle: string;
  bannerBudgetDesc: string;
  bannerCs329aTitle: string;
  bannerCs329aDesc: string;
  bannerStanfordTitle: string;
  bannerStanfordDesc: string;
  bannerMaeumjigiTitle: string;
  bannerMaeumjigiDesc: string;
  bannerAnprTitle: string;
  bannerAnprDesc: string;
  bannerRlTitle: string;
  bannerRlDesc: string;
  bannerSecurityTitle: string;
  bannerSecurityDesc: string;
  bannerSdcTitle: string;
  bannerSdcDesc: string;
  bannerAllTitle: string;
  bannerAllDesc: string;"""

if old_loc_content in content:
    content = content.replace(old_loc_content, new_loc_content)

# 3. Add SDC project and taxonomy fields to ko
ko_tax_fields = """  ko: {
    hubTitle: '프로젝트 & 개발 일지',
    hubSubtitle: '관심 있는 프로젝트를 선택하여 개발 여정과 기술 기록을 확인해보세요.',
    tabHub: '프로젝트 허브',
    tabCrisis: '[고위험 AI] 위기 감지',
    tabBudget: '국가 예산 AI 감사',
    tabCs329a: '스탠포드 CS329A',
    tabStanford: '스탠포드 CS146S',
    tabMaeumjigi: '마음지기',
    tabAnpr: 'ANPR & 차선침범',
    tabRl: 'RL Q-Learning',
    tabSecurity: '보안 & 엔지니어링',
    tabSdc: 'SDC 공중전 임무계획',
    tabAll: '전체 글 피드',
    taxAll: '전체 분류',
    taxTheory: '1. 이론 (Theory)',
    taxPractice: '2. 실습 (Practice)',
    taxError: '3. 오류 (Errors)',
    taxDomainLabel: '도메인',
    taxDomainAll: '전체 도메인',
    taxDomainAi: 'AI',
    taxDomainSecurity: '보안 (Security)',
    taxTypeLabel: '소분류 유형',
    taxTypeAll: '전체 유형',
    taxTypeLecture: '강의 (Lecture)',
    taxTypeDef: '정의 (Definition)',
    taxTypeHistory: '역사 (History)',
    taxProjectLabel: '프로젝트별',
    taxErrorTitle: '오류 및 트러블슈팅 아카이브 (Errors & Troubleshooting)',
    taxErrorDesc: '오류의 하위 분류는 추후 분류 예정입니다 (Pending Sub-classification). 각 프로젝트에서 발생한 날것의 런타임/설계 결함(A-xx, B-xx, D-xx)과 근본 원인 분석(Deep Root Cause), 해결 코드 Diff를 다룬 실전 포스트들을 집대성하여 제공합니다.',"""

content = re.sub(
    r"  ko:\s*\{\s*hubTitle:\s*'프로젝트 & 개발 일지',.*?tabAll:\s*'전체 글 피드',",
    ko_tax_fields,
    content,
    flags=re.DOTALL
)

if "bannerSdcTitle" not in content:
    content = content.replace(
        "bannerSecurityDesc: '정적 사이트 심층 보안 강화, 위협 모델링 및 npm 공급망 취약점 방어',",
        """bannerSecurityDesc: '정적 사이트 심층 보안 강화, 위협 모델링 및 npm 공급망 취약점 방어',
    bannerSdcTitle: '프로젝트: SDC 공중전 동적 임무계획 (Dynamic Mission Replanning)',
    bannerSdcDesc: '비행 중 조종석-지상 간 델타 분산 아키텍처: RFC 8785 JCS, Ed25519 전자서명, MapLibre WebGL UI, CPython 14.5s->0.25s A* 탐색 가속 및 2022 국방백서 기반 T1~T12 위협 대응 실전 개발일지.',"""
    )

# 4. Add SDC project and taxonomy fields to en
en_tax_fields = """  en: {
    hubTitle: 'Projects & Dev Logs',
    hubSubtitle: 'Select a project to explore dev logs and technical milestones.',
    tabHub: 'Projects Hub',
    tabCrisis: 'Mental Crisis NLP',
    tabBudget: 'Public Budget AI',
    tabCs329a: 'Stanford CS329A',
    tabStanford: 'Stanford CS146S',
    tabMaeumjigi: 'Maeumjigi',
    tabAnpr: 'ANPR & Lane Intrusion',
    tabRl: 'RL Q-Learning',
    tabSecurity: 'Security & Infra',
    tabSdc: 'SDC Air Combat',
    tabAll: 'All Posts Feed',
    taxAll: 'All Categories',
    taxTheory: '1. Theory',
    taxPractice: '2. Practice',
    taxError: '3. Errors & Pitfalls',
    taxDomainLabel: 'Domain',
    taxDomainAll: 'All Domains',
    taxDomainAi: 'AI',
    taxDomainSecurity: 'Security',
    taxTypeLabel: 'Sub-type',
    taxTypeAll: 'All Types',
    taxTypeLecture: 'Lecture',
    taxTypeDef: 'Definition',
    taxTypeHistory: 'History',
    taxProjectLabel: 'By Project',
    taxErrorTitle: 'Errors & Troubleshooting Archive',
    taxErrorDesc: 'Sub-classification of errors is pending future definition. This archive aggregates all real-world runtime/design defect postmortems (A-xx, B-xx, D-xx), deep root causes, and clean fix code diffs across projects.',"""

content = re.sub(
    r"  en:\s*\{\s*hubTitle:\s*'Projects & Dev Logs',.*?tabAll:\s*'All Posts Feed',",
    en_tax_fields,
    content,
    flags=re.DOTALL
)

if "Project: SDC In-Flight" not in content:
    content = content.replace(
        "bannerSecurityDesc: 'Static site security hardening, threat modeling, and npm supply chain defense',",
        """bannerSecurityDesc: 'Static site security hardening, threat modeling, and npm supply chain defense',
    bannerSdcTitle: 'Project: SDC In-Flight Dynamic Mission Replanning Engine',
    bannerSdcDesc: 'In-flight cockpit-ground distributed delta architecture: RFC 8785 JCS, Ed25519 signatures, MapLibre WebGL UI, CPython 14.5s->0.25s A* search acceleration, and ROK MND 2022 Threat Matrix T1~T12 replanning series.',"""
    )

# 5. Add ja
ja_tax_fields = """  ja: {
    hubTitle: 'プロジェクト＆開発日誌',
    hubSubtitle: '関心のあるプロジェクトを選択して、開発の歩みと技術的な記録をご覧ください。',
    tabHub: 'プロジェクトハブ',
    tabCrisis: '危機検知NLP AI',
    tabBudget: '国家予算AI監査',
    tabCs329a: 'スタンフォード CS329A',
    tabStanford: 'スタンフォード CS146S',
    tabMaeumjigi: 'マウムジギ',
    tabAnpr: 'ANPR＆車線侵犯',
    tabRl: 'RL Q-Learning',
    tabSecurity: 'セキュリティ＆インフラ',
    tabSdc: 'SDC 空中戦任務計画',
    tabAll: '全記事フィード',
    taxAll: '全分類',
    taxTheory: '1. 理論 (Theory)',
    taxPractice: '2. 実習 (Practice)',
    taxError: '3. エラー (Errors)',
    taxDomainLabel: 'ドメイン',
    taxDomainAll: '全ドメイン',
    taxDomainAi: 'AI',
    taxDomainSecurity: 'セキュリティ',
    taxTypeLabel: 'サブ分類',
    taxTypeAll: '全タイプ',
    taxTypeLecture: '講義 (Lecture)',
    taxTypeDef: '定義 (Definition)',
    taxTypeHistory: '歴史 (History)',
    taxProjectLabel: 'プロジェクト別',
    taxErrorTitle: 'エラー＆トラブルシューティング アーカイブ',
    taxErrorDesc: 'エラーのサブ分類は今後分類予定です。各プロジェクトで発生したランタイム・設計の欠陥（A-xx、B-xx、D-xx）と根本原因分析、修正コードDiffを収録した実戦記事をまとめて提供します。',"""

content = re.sub(
    r"  ja:\s*\{\s*hubTitle:\s*'プロジェクト＆開発日誌',.*?tabAll:\s*'全記事フィード',",
    ja_tax_fields,
    content,
    flags=re.DOTALL
)

if "SDC 空中戦動的任務計画" not in content:
    content = content.replace(
        "bannerSecurityDesc: '静적サイト深層セキュリティ強化、脅威モデリングおよびnpmサプライチェーン防御',",
        """bannerSecurityDesc: '静적サイト深層セキュリティ強化、脅威モデリングおよびnpmサプライチェーン防御',
    bannerSdcTitle: 'プロジェクト: SDC 空中戦動的任務計画 (Dynamic Mission Replanning)',
    bannerSdcDesc: '飛行中の操縦席-地上間分散デルタアーキテクチャ: RFC 8785 JCS、Ed25519電子署名、MapLibre WebGL UI、CPython 14.5秒->0.25秒 A*探索加速および2022韓国国防白書ベースT1~T12脅威対応実録。',"""
    )

# 6. Add es
es_tax_fields = """  es: {
    hubTitle: 'Proyectos y Diarios de Desarrollo',
    hubSubtitle: 'Selecciona un proyecto para explorar los diarios de desarrollo y los hitos técnicos.',
    tabHub: 'Panel de Proyectos',
    tabCrisis: 'IA Crisis NLP',
    tabBudget: 'Auditoría Presupuesto IA',
    tabCs329a: 'Stanford CS329A',
    tabStanford: 'Stanford CS146S',
    tabMaeumjigi: 'Maeumjigi',
    tabAnpr: 'ANPR e Invasión',
    tabRl: 'RL Q-Learning',
    tabSecurity: 'Seguridad e Infra',
    tabSdc: 'SDC Combate Aéreo',
    tabAll: 'Todos los Posts',
    taxAll: 'Todas las Categorías',
    taxTheory: '1. Teoría',
    taxPractice: '2. Práctica',
    taxError: '3. Errores y Fallos',
    taxDomainLabel: 'Dominio',
    taxDomainAll: 'Todos los Dominios',
    taxDomainAi: 'IA',
    taxDomainSecurity: 'Seguridad',
    taxTypeLabel: 'Subtipo',
    taxTypeAll: 'Todos los Tipos',
    taxTypeLecture: 'Clase (Lecture)',
    taxTypeDef: 'Definición',
    taxTypeHistory: 'Historia',
    taxProjectLabel: 'Por Proyecto',
    taxErrorTitle: 'Archivo de Errores y Depuración',
    taxErrorDesc: 'La subclasificación de errores está pendiente de definición futura. Este archivo reúne todos los análisis de fallos en tiempo de ejecución/diseño (A-xx, B-xx, D-xx), causas raíz y diffs de código correctivo.',"""

content = re.sub(
    r"  es:\s*\{\s*hubTitle:\s*'Proyectos y Diarios de Desarrollo',.*?tabAll:\s*'Todos los Posts',",
    es_tax_fields,
    content,
    flags=re.DOTALL
)

if "Motor de Replanificación Dinámica" not in content:
    content = content.replace(
        "bannerSecurityDesc: 'Blindaje de seguridad en sitios estáticos, modelado de amenazas y defensa de la cadena npm',",
        """bannerSecurityDesc: 'Blindaje de seguridad en sitios estáticos, modelado de amenazas y defensa de la cadena npm',
    bannerSdcTitle: 'Proyecto: Motor de Replanificación Dinámica de Combate Aéreo (SDC)',
    bannerSdcDesc: 'Arquitectura distribuida de delta cabina-tierra en vuelo: RFC 8785 JCS, firmas Ed25519, MapLibre WebGL UI, aceleración de búsqueda A* de 14.5s a 0.25s y matriz de amenazas T1~T12 del Libro Blanco de Defensa 2022.',"""
    )

# 7. Add taxonomyL1, taxonomyL2, taxonomyL3 to project objects
proj_mappings = {
    "'crisis_detection'": "taxonomyL1: 'practice', taxonomyL2: 'ai', taxonomyL3: 'project-crisis'",
    "'national_budget'": "taxonomyL1: 'practice', taxonomyL2: 'ai', taxonomyL3: 'project-budget'",
    "'maeumjigi'": "taxonomyL1: 'practice', taxonomyL2: 'ai', taxonomyL3: 'project-maeumjigi'",
    "'anpr_vision'": "taxonomyL1: 'practice', taxonomyL2: 'ai', taxonomyL3: 'project-anpr'",
    "'rl_q_learning'": "taxonomyL1: 'practice', taxonomyL2: 'ai', taxonomyL3: 'project-rl'",
    "'security'": "taxonomyL1: 'practice', taxonomyL2: 'security', taxonomyL3: 'project-security-infra'",
    "'stanford_cs329a'": "taxonomyL1: 'theory', taxonomyL2: 'ai', taxonomyL3: 'lecture'",
    "'stanford_cs146s'": "taxonomyL1: 'theory', taxonomyL2: 'ai', taxonomyL3: 'lecture'",
}

for pid, tax_str in proj_mappings.items():
    pattern = rf"(id:\s*{pid},.*?hasPosts:\s*true,)"
    def repl(m):
        if "taxonomyL1:" in m.group(1):
            return m.group(1)
        return m.group(1) + f"\n        {tax_str},"
    content = re.sub(pattern, repl, content, flags=re.DOTALL)

# Add SDC project card to ko.projects
sdc_card_ko = """      {
        id: 'sdc_replanning',
        name: 'SDC 공중전 동적 임무계획',
        badgeType: 'active',
        category: '실습 / AI / 항공전자',
        icon: 'sdc_replanning',
        subtitle: '비행 중 임무 재계획 및 델타 분산 아키텍처 실전 연구',
        description:
          '전술 데이터링크 교란 환경에서의 RFC 8785 결정론적 JCS, Ed25519 전자서명, MapLibre WebGL UI, CPython 14.5s->0.25s A* 탐색 최적화 및 2022 국방백서 기반 T1~T12 위협 대응 실전 개발일지.',
        techTags: ['Mission Replanning', 'Ed25519', 'MapLibre WebGL', 'RK4 Fuel', 'Simplex AI', 'A* Search'],
        hasPosts: true,
        taxonomyL1: 'practice',
        taxonomyL2: 'ai',
        taxonomyL3: 'project-sdc',
      },"""

if "id: 'sdc_replanning'" not in content:
    content = content.replace("projects: [\n      {\n        id: 'crisis_detection'", "projects: [\n" + sdc_card_ko + "\n      {\n        id: 'crisis_detection'")

FILE_PATH.write_text(content, encoding="utf-8")
print("[+] Updated index.tsx data structures successfully.")
