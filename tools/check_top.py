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

def analyze(pattern):
    files = glob.glob(pattern, recursive=True)
    results = []
    for f in sorted(files):
        with open(f, 'r', encoding='utf-8') as fp:
            raw = fp.read()
        body = strip_frontmatter(raw)
        title = get_title(raw, os.path.basename(os.path.dirname(f)))
        char_count = len(body.strip())
        results.append({
            'title': title,
            'chars': char_count,
            'path': f
        })
    avg = sum(r['chars'] for r in results) / len(results)
    results.sort(key=lambda x: x['chars'], reverse=True)
    return avg, results

def main():
    avg_gb, gb = analyze(r"D:\ai\antigravity\global_blog\blog\**\index.md")
    print(f"Global Blog EN Avg: {avg_gb:.1f}")
    print("Top 10 longest:")
    for r in gb[:10]:
        print(f"  {r['chars']} chars | {r['title']}")
        
    avg_nb, nb = analyze(r"D:\ai\antigravity\naver_blog\posts\**\post.md")
    print(f"\nNaver Blog Posts Avg: {avg_nb:.1f}")
    print("Top 5 longest:")
    for r in nb[:5]:
        print(f"  {r['chars']} chars | {r['title']}")

if __name__ == '__main__':
    main()
