import React from 'react';
import BlogPostItem from '@theme-original/BlogPostItem';
import Giscus from '@giscus/react';
import { useColorMode } from '@docusaurus/theme-common';
import { useBlogPost } from '@docusaurus/plugin-content-blog/client';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import AdCard from '@site/src/components/AdCard';

export default function BlogPostItemWrapper(props: any) {
  const { colorMode } = useColorMode();
  const { isBlogPostPage } = useBlogPost();
  const {
    i18n: { currentLocale },
  } = useDocusaurusContext();

  const giscusLang = ['ko', 'en', 'ja', 'es'].includes(currentLocale)
    ? currentLocale
    : 'en';

  return (
    <>
      <BlogPostItem {...props} />
      {isBlogPostPage && (
        <>
          <AdCard />
          <div style={{ marginTop: '2.5rem' }}>
            <Giscus
              id="comments"
              repo="jbjihwan/global_blog"
              repoId="R_kgDOVBP18w"
              category="General"
              categoryId="DIC_kwDOVBP1884DHWZr"
              mapping="pathname"
              reactionsEnabled="1"
              emitMetadata="0"
              inputPosition="top"
              theme={colorMode === 'dark' ? 'dark' : 'light'}
              lang={giscusLang}
              loading="lazy"
            />
          </div>
        </>
      )}
    </>
  );
}
