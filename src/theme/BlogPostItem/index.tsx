import React from 'react';
import BlogPostItem from '@theme-original/BlogPostItem';
import Giscus from '@giscus/react';
import { useColorMode } from '@docusaurus/theme-common';
import { useBlogPost } from '@docusaurus/plugin-content-blog/client';

export default function BlogPostItemWrapper(props: any) {
  const { colorMode } = useColorMode();
  const { isBlogPostPage } = useBlogPost();

  return (
    <>
      <BlogPostItem {...props} />
      {isBlogPostPage && (
        <div style={{ marginTop: '2rem' }}>
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
            lang="ko"
            loading="lazy"
          />
        </div>
      )}
    </>
  );
}
