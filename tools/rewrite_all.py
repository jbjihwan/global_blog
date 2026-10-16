import os
import glob
import subprocess
import json
import re
import shutil
import concurrent.futures

# We will read all the digest.md to find the actual original images.
naver_posts_dir = r"D:\ai\antigravity\naver_blog\posts"
blog_root = r"D:\ai\antigravity\global_blog"

# Helper to run agy
def run_agy(prompt):
    # Use a temporary file for the prompt to avoid shell escaping issues
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write(prompt)
        tmp_name = f.name
    try:
        res = subprocess.run(['agy', '-p', f'$(Get-Content "{tmp_name}" -Raw)'], 
                           capture_output=True, text=True, encoding='utf-8', shell=True)
        return res.stdout.strip()
    finally:
        os.remove(tmp_name)

def process_episode(ko_md_path):
    print(f"Processing {ko_md_path}...")
    with open(ko_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract original frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---", content, flags=re.DOTALL)
    fm = fm_match.group(0) if fm_match else ""

    # Find matching digest.md
    # The ko_md_path is like .../2026-06-18-maeumjigi-23/index.md
    folder_name = os.path.basename(os.path.dirname(ko_md_path))
    date_str = folder_name[:10] # e.g. 2026-06-18
    digest_path = os.path.join(naver_posts_dir, date_str, "maeumjigi", "digest.md")
    
    images_text = ""
    if os.path.exists(digest_path):
        with open(digest_path, 'r', encoding='utf-8') as f:
            digest = f.read()
            # Extract image paths
            imgs = re.findall(r"- `(D:/.*?\.(png|jpg|jpeg))`", digest, re.IGNORECASE)
            images_text = "\n".join([f"- Original image: {img[0]}" for img in imgs])

    # Construct prompt
    prompt = f"""
다음은 기존에 작성된 캡스톤 디자인 프로젝트 블로그 글입니다.
사용자의 요구사항에 맞게 이 글을 완전히 다시 작성해주세요.

[요구사항]
1. 감성적인 수필 형식이 아닌, '개발 기록(Dev Log)' 목적에 맞게 철저히 기술 블로그 스타일로 작성하세요.
2. 사용한 기술(Tech Stack), 발생한 문제(Troubleshooting), 해결 방법(Solution), 구현한 핵심 기능(Features) 위주로 상세하고 전문적으로 서술하세요.
3. 기존 글의 문맥은 유지하되, 기술적인 깊이를 대폭 추가하세요.
4. 마크다운(Markdown) 포맷을 유지하고, Frontmatter는 건드리지 마세요.
5. 첫 번째 AI 관련 단어는 풀네임(약어) 형식으로 표기하세요 (예: 인공지능(AI)).
6. 인위적으로 넣었던 이미지(01_cover.png 등)는 모두 제거하고, 아래에 제시된 [실제 원본 이미지] 리스트가 있다면 그 경로를 그대로 마크다운 이미지 링크로 삽입하여 맥락에 맞게 배치하세요. 만약 이미지가 없다면 억지로 넣지 마세요.

[실제 원본 이미지]
{images_text}

[기존 글]
{content}

출력은 반드시 마크다운 본문만 해주세요 (Frontmatter 포함).
"""

    rewritten = run_agy(prompt)
    if not rewritten.startswith('---'):
        rewritten = fm + "\n\n" + rewritten

    # Save Korean
    with open(ko_md_path, 'w', encoding='utf-8') as f:
        f.write(rewritten)
    print(f"Saved KO: {ko_md_path}")
    
    # Trigger translations
    for lang in ['en', 'ja', 'es']:
        lang_path = ko_md_path.replace(r'\ko\\', f'\\{lang}\\')
        print(f"Translating {ko_md_path} to {lang}...")
        t_prompt = f"Translate the following technical blog post to {lang}. Keep markdown formatting, frontmatter structure (but translate title), and image paths intact.\n\n{rewritten}"
        translated = run_agy(t_prompt)
        if translated:
            with open(lang_path, 'w', encoding='utf-8') as f:
                f.write(translated)

ko_posts = glob.glob(os.path.join(blog_root, 'i18n', 'ko', 'docusaurus-plugin-content-blog', '*', 'index.md'))

# Process concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(process_episode, ko_posts)

print("ALL EPISODES REWRITTEN AND TRANSLATED.")
