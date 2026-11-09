import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import { ProjectIcon } from '@site/src/components/Icons';
import allPostsData from '@site/src/data/all_posts.json';
import styles from './index.module.css';

interface ProjectCardData {
  id: string;
  name: string;
  badge: string;
  category: string;
  subtitle: string;
  description: string;
  tags: string[];
  link: string;
}

const FEATURED_PROJECTS: ProjectCardData[] = [
  {
    id: 'stanford_cs329a',
    name: 'Stanford CS329A',
    badge: 'Frontier AI · 17 Posts',
    category: 'AI Agents / Machine Learning',
    subtitle: 'Stanford University Self-Improving AI Agents Series',
    description:
      'In-depth engineering analyses of test-time compute scaling, Process Reward Models (PRM), Monte Carlo Tree Search (MCTS), DeepSeek GRPO reinforcement learning, automated scientific discovery (Sakana AI Scientist), and Lean 4 formal mathematical verification.',
    tags: ['Stanford CS329A', 'Self-Improving AI', 'MCTS Tree Search', 'GRPO RL', 'PRM', 'VLA Robotics'],
    link: '/blog#stanford_cs329a',
  },
  {
    id: 'stanford_cs146s',
    name: 'Stanford CS146S',
    badge: 'Software Engineering · 10 Posts',
    category: 'Software Engineering / AI Orchestration',
    subtitle: 'Stanford University Modern Software Developer Series',
    description:
      'The paradigm shift from manual syntax typing to AI agent orchestration. Complete architectural breakdowns of Spec-Driven Development (SDD), Agent Loop Engineering, Model Context Protocol (MCP), and production verification circuit breakers.',
    tags: ['Stanford CS146S', 'Agentic Workflows', 'Spec-Driven (SDD)', 'Model Context Protocol', 'CI/CD'],
    link: '/blog#stanford_cs146s',
  },
  {
    id: 'national_budget',
    name: 'Public Budget AI',
    badge: 'Public Finance · 6 Posts',
    category: 'Public Finance / Anomaly Detection',
    subtitle: 'Autonomous Procurement Fraud & Budget Surveillance System',
    description:
      'An end-to-end automated surveillance architecture auditing public procurement datasets: Text-to-SQL financial precision, 3D target sector partitioning, GraphRAG corporate registry cartel tracing, and automated discrepancy dossier compilation.',
    tags: ['Budget AI', 'GraphRAG', 'Text-to-SQL', 'Procurement Audit', 'FastAPI', 'NetworkX'],
    link: '/blog#national_budget',
  },
  {
    id: 'sdc_replanning',
    name: 'SDC Mission Replanning',
    badge: 'Avionics AI · 3 Posts',
    category: 'Mission Critical / Aerospace / AI',
    subtitle: 'In-Flight Air Combat Dynamic Mission Replanning System',
    description:
      'Mission-critical software architecture for tactical data links (Link 16): zero-dependency RFC 8785 deterministic JCS canonicalization, Ed25519 multi-signature cryptographic envelopes, CPython 14.5s to 0.25s A* graph search optimization, and ROK 2022 Threat Matrix T1~T12 modeling.',
    tags: ['Mission Replanning', 'Ed25519', 'RFC 8785 JCS', 'Link 16 MTU', 'RK4 Fuel', 'Simplex AI'],
    link: '/blog#sdc_replanning',
  },
  {
    id: 'anpr_vision',
    name: 'Blackbox ANPR & Vision ITS',
    badge: 'Computer Vision · 5 Posts',
    category: 'Computer Vision / Intelligent Transportation',
    subtitle: 'Real-Time Lane Intrusion Detection & Super-Resolution ANPR',
    description:
      'Real-time highway dashcam computer vision under strict 30 FPS latency constraints: geometric lane intrusion detection with IoU, blurry license plate reconstruction via EDSR_x4 deep super-resolution, and temporal majority voting EasyOCR pipeline across 11 iterations.',
    tags: ['OpenCV', 'YOLOv5', 'EDSR Super-Resolution', 'CSRT Tracker', 'EasyOCR', 'PyTorch'],
    link: '/blog#anpr_vision',
  },
  {
    id: 'security',
    name: 'Security & Web Infrastructure',
    badge: 'DevSecOps · 5 Posts',
    category: 'Web Security / DevSecOps',
    subtitle: 'Static Site Security Hardening & Supply Chain Defense',
    description:
      'Practical defensive engineering for modern static web architectures: threat modeling 45 npm audit vulnerabilities, git secret scanning, PII protection, Content Security Policies, zero-downtime custom domain migration, and automated CI/CD verification.',
    tags: ['npm audit', 'SSG Hardening', 'DevSecOps', 'Threat Modeling', 'CI/CD Pipelines'],
    link: '/blog#security',
  },
  {
    id: 'rl_q_learning',
    name: 'RL Q-Learning Mobile Robot',
    badge: 'Robotics · 5 Posts',
    category: 'Reinforcement Learning / Robotics',
    subtitle: 'Webots Q-Learning Autonomous Obstacle Avoidance Project',
    description:
      'From zero-knowledge exploration to deterministic navigation: continuous distance sensor discretization (648 state bins), velocity/distance reward shaping to counteract sparse reward starvation, and physical Sim-to-Real hardware transfer to dual-motor Arduino microcontrollers.',
    tags: ['Python', 'Webots Simulator', 'Q-Learning', 'NumPy', 'Socket IPC', 'Arduino Hardware'],
    link: '/blog#rl_q_learning',
  },
  {
    id: 'crisis_detection',
    name: '[Crisis AI] Clinical Triage NLP',
    badge: 'Clinical NLP · 4 Posts',
    category: 'High-Stakes AI / Clinical NLP',
    subtitle: 'Clinical Mental Health & Crisis Triage NLP Pipeline Dev Log',
    description:
      'A production-grade NLP pipeline engineered to eliminate False Negatives (FNR Zero) in life-critical psychological text triage. Overcoming 524x Bayesian prior probability skew with dual-stage hybrid triage (cumulative gating + argmax), ordinal tree stabilization, and 14-day temporal decay defenses.',
    tags: ['Clinical NLP', 'FNR Zero', 'Bayesian Barrier', 'LightGBM Ordinal', 'RoBERTa', 'Safety AI'],
    link: '/blog#crisis_detection',
  },
  {
    id: 'maeumjigi',
    name: 'Maeumjigi AI Support',
    badge: 'AI Chatbot · 23 Posts',
    category: 'Capstone Design / Conversational AI',
    subtitle: 'AI Mental Health & Emotional Distress Counseling Dev Log',
    description:
      'Comprehensive dev chronicle of developing a crisis support AI chatbot: synthetic clinical dialogue generation, Llama 3.1 fine-tuning (2:1 emotional-to-daily dialogue ratio), deterministic sub-millisecond Safety Wrapper guardrail architecture, and AWS EC2 GPU server deployment.',
    tags: ['PyTorch', 'Llama 3.1 LoRA', 'Safety Wrapper', 'FastAPI', 'AWS EC2', 'Mental Health Support'],
    link: '/blog#maeumjigi',
  },
];

export default function Home(): React.JSX.Element {
  const totalPostsCount = allPostsData.length;

  return (
    <Layout
      title="Global Dev Blog | Production Engineering & AI Systems Deep Dives"
      description="Production-grade engineering research, empirical benchmarks, and technical postmortems in AI Agents, Robotics, Computer Vision, and Aerospace Systems.">
      <main className={styles.homeContainer}>
        {/* 1. Hero Section */}
        <section className={styles.heroSection}>
          <div className={styles.heroBadge}>ENGINEERING LAB NOTEBOOK &amp; EMPIRICAL RESEARCH</div>
          <h1 className={styles.heroTitle}>Global Dev Blog</h1>
          <p className={styles.heroSubtitle}>
            Hands-on technical postmortems, architecture trade-offs, and rigorous benchmarks in{' '}
            <strong>AI Systems, Autonomous Robotics, Deep Computer Vision, Aerospace Replanning, and Cloud Security</strong>.
          </p>

          <div className={styles.statsRow}>
            <div className={styles.statItem}>
              <span className={styles.statNumber}>{totalPostsCount}</span>
              <span className={styles.statLabel}>Published Articles</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statNumber}>100%</span>
              <span className={styles.statLabel}>Empirically Verified</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statNumber}>9</span>
              <span className={styles.statLabel}>R&amp;D Project Tracks</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statNumber}>2</span>
              <span className={styles.statLabel}>Languages (EN / KO)</span>
            </div>
          </div>

          <div className={styles.heroActions}>
            <Link className={styles.btnPrimary} to="/blog">
              Explore All {totalPostsCount} Technical Articles &rarr;
            </Link>
            <Link className={styles.btnSecondary} to="/about">
              About the Lab &amp; Hardware Rig
            </Link>
            <Link className={styles.btnSecondary} to="/terms">
              Terms &amp; Research Disclaimer
            </Link>
          </div>
        </section>

        {/* 2. Core Engineering Project Tracks Showcase */}
        <section style={{ marginBottom: '4rem' }}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>
              <span>🛠️</span> Core Engineering R&amp;D Tracks
            </h2>
            <p className={styles.sectionSubtitle}>
              Selected production systems, academic curriculum breakdowns, and architectural postmortems.
            </p>
          </div>

          <div className={styles.projectsGrid}>
            {FEATURED_PROJECTS.map((proj) => (
              <div key={proj.id} className={styles.projectCard}>
                <div>
                  <div className={styles.cardHeader}>
                    <span className={styles.cardBadge}>{proj.badge}</span>
                    <span className={styles.cardCategory}>{proj.category}</span>
                  </div>

                  <div className={styles.projectTitleGroup}>
                    <div className={styles.projectIconBox}>
                      <ProjectIcon id={proj.id} size={24} />
                    </div>
                    <h3 className={styles.projectName}>{proj.name}</h3>
                  </div>

                  <div className={styles.projectSub}>{proj.subtitle}</div>
                  <p className={styles.projectDesc}>{proj.description}</p>

                  <div className={styles.techTags}>
                    {proj.tags.map((tag) => (
                      <span key={tag} className={styles.techTag}>
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>

                <div className={styles.cardFooter}>
                  <Link className={styles.cardLink} to={proj.link}>
                    View Project Series &amp; Episodes &rarr;
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 3. Static Articles Directory (All 83 Posts in SSG HTML) */}
        <section className={styles.articlesDirectory}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>
              <span>📚</span> Complete Engineering Publication Directory ({totalPostsCount} Posts)
            </h2>
            <p className={styles.sectionSubtitle}>
              All production dev logs, failure analyses, and empirical benchmark reports arranged in chronological order.
            </p>
          </div>

          <div className={styles.articlesGrid}>
            {allPostsData.map((post) => (
              <Link key={post.permalink} className={styles.articleItem} to={post.permalink}>
                <span className={styles.articleTitle} title={post.title}>
                  {post.title}
                </span>
                <span className={styles.articleDate}>{post.date}</span>
              </Link>
            ))}
          </div>
        </section>

        {/* 4. Editorial Integrity & Verification Standards (E-E-A-T) */}
        <section>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>
              <span>🛡️</span> Publication Ethics &amp; Verification Rigor
            </h2>
            <p className={styles.sectionSubtitle}>
              How we guarantee technical credibility, zero AI hallucination, and empirical reproducibility.
            </p>
          </div>

          <div className={styles.infoGrid}>
            <div className={styles.infoCard}>
              <h3 className={styles.infoCardTitle}>
                <span>🔬</span> 100% Empirically Tested
              </h3>
              <p className={styles.infoCardDesc}>
                Every architectural pattern, SQL query, machine learning pipeline, and troubleshooting fix published on this blog is executed and verified on actual hardware rigs (NVIDIA GeForce RTX 4060 GPU, Ubuntu Linux / WSL2, Python 3.12, TypeScript, Webots) before publication.
              </p>
            </div>

            <div className={styles.infoCard}>
              <h3 className={styles.infoCardTitle}>
                <span>🚫</span> Zero Hallucination Guarantee
              </h3>
              <p className={styles.infoCardDesc}>
                We do not publish untested theoretical code or generic AI summaries. All failure modes, benchmark figures, and exception traces are captured directly from live test harnesses and production CI/CD runs.
              </p>
            </div>

            <div className={styles.infoCard}>
              <h3 className={styles.infoCardTitle}>
                <span>⚖️</span> Postmortems &amp; Real Failure Logs
              </h3>
              <p className={styles.infoCardDesc}>
                We believe documenting failure modes—such as buffer deadlocks, cyclic dependency crashes, and Bayes prior collapses—delivers far greater value to engineering peers than idealized success stories.
              </p>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
