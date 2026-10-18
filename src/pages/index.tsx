import React from 'react';
import Head from '@docusaurus/Head';
import { Redirect } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  const blogUrl = `${siteConfig.baseUrl}blog`;

  return (
    <Layout
      title="Global Dev Blog"
      description="Production-grade AI engineering, Autonomous Systems, and Full-Stack Development Journey">
      <Head>
        <meta httpEquiv="refresh" content={`0; url=${blogUrl}`} />
      </Head>
      <main style={{ padding: '4rem 2rem', textAlign: 'center', minHeight: '60vh' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>Global Dev Blog</h1>
        <p style={{ fontSize: '1.2rem', color: 'var(--ifm-color-emphasis-700)', maxWidth: '640px', margin: '0 auto 2rem' }}>
          Production-grade AI engineering, autonomous systems, and computer vision development logs.
        </p>
        <div style={{ marginTop: '2rem' }}>
          <a
            href={blogUrl}
            style={{
              display: 'inline-block',
              padding: '0.8rem 2rem',
              backgroundColor: 'var(--ifm-color-primary)',
              color: '#fff',
              borderRadius: '8px',
              fontWeight: 600,
              textDecoration: 'none',
            }}>
            Explore Developer Blog &amp; Projects &rarr;
          </a>
        </div>
        <Redirect to={blogUrl} />
      </main>
    </Layout>
  );
}
