import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/blog">
            개발 일지 보러가기 📚
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <div className="container" style={{padding: '4rem 0', textAlign: 'center'}}>
          <h2>환영합니다! 👋</h2>
          <p>
            이곳은 서울과학기술대학교 캡스톤 디자인 프로젝트 <b>'마음지기'</b>의 글로벌 개발 블로그입니다.<br />
            AI 기반 자살 예방 상담 챗봇을 개발하며 겪은 치열한 고민과 기술적 성취를 4개 국어로 공유합니다.
          </p>
          <p>위의 <b>[개발 일지 보러가기]</b> 버튼이나 상단의 <b>Blog</b> 메뉴를 클릭하여 여정을 확인해보세요!</p>
        </div>
      </main>
    </Layout>
  );
}
