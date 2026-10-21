import os
import glob
import re

def strip_frontmatter(content):
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2]
    return content

def get_title(content, default_name):
    match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    h1_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    return default_name

def analyze_files(files):
    results = []
    for f in sorted(files):
        with open(f, 'r', encoding='utf-8') as fp:
            raw = fp.read()
        body = strip_frontmatter(raw)
        title = get_title(raw, os.path.basename(os.path.dirname(f)))
        char_count = len(body.strip())
        word_count = len(body.split())
        line_count = len(body.strip().splitlines())
        results.append({
            'path': f,
            'title': title,
            'chars': char_count,
            'words': word_count,
            'lines': line_count
        })
    return results

def print_section(name, results):
    print(f"\n==========================================")
    print(f"=== {name} ===")
    print(f"==========================================")
    if not results:
        print("No items found.")
        return
    avg_chars = sum(p['chars'] for p in results) / len(results)
    avg_words = sum(p['words'] for p in results) / len(results)
    avg_lines = sum(p['lines'] for p in results) / len(results)
    print(f"Total count: {len(results)}")
    print(f"Average: {avg_chars:.1f} chars | {avg_words:.1f} words | {avg_lines:.1f} lines\n")
    
    below_avg = [p for p in results if p['chars'] < avg_chars]
    below_avg.sort(key=lambda x: x['chars'])
    print(f"Items below average length: {len(below_avg)} / {len(results)} ({len(below_avg)/len(results)*100:.1f}%)")
    for idx, p in enumerate(below_avg, 1):
        ratio = (p['chars'] / avg_chars) * 100
        print(f"{idx:2d}. [{p['chars']} chars | {p['lines']} lines | {ratio:.1f}% of avg]")
        print(f"    제목: {p['title']}")
        print(f"    경로: {p['path']}")

def main():
    # 1. Global Blog English Posts
    gb_en_files = glob.glob(r"D:\ai\antigravity\global_blog\blog\**\index.md", recursive=True)
    gb_en = analyze_files(gb_en_files)
    print_section("1. 글로벌 블로그 (GlobalDevLog 영문 원본 기준)", gb_en)

    # 2. Global Blog Korean Posts
    gb_ko_files = glob.glob(r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog\**\index.md", recursive=True)
    gb_ko = analyze_files(gb_ko_files)
    print_section("2. 글로벌 블로그 (GlobalDevLog 한국어 번역본 기준)", gb_ko)

    # 3. Naver Blog Posts (post.md)
    nb_post_files = glob.glob(r"D:\ai\antigravity\naver_blog\posts\**\post.md", recursive=True)
    nb_posts = analyze_files(nb_post_files)
    print_section("3. 네이버 블로그 게시글 (post.md 기준)", nb_posts)

    # 4. Naver Blog Daily Digests (digest.md)
    nb_digest_files = glob.glob(r"D:\ai\antigravity\naver_blog\posts\**\digest.md", recursive=True)
    nb_digests = analyze_files(nb_digest_files)
    print_section("4. 네이버 블로그 작업 일지/다이제스트 (digest.md 기준)", nb_digests)

if __name__ == '__main__':
    main()
