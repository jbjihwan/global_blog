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

def format_summary(name, results):
    if not results:
        return f"### {name}\n게시글이 없습니다.\n"
    avg_chars = sum(p['chars'] for p in results) / len(results)
    avg_words = sum(p['words'] for p in results) / len(results)
    avg_lines = sum(p['lines'] for p in results) / len(results)
    
    below_avg = [p for p in results if p['chars'] < avg_chars]
    below_avg.sort(key=lambda x: x['chars'])
    
    out = []
    out.append(f"### {name}")
    out.append(f"- **총 게시글 수**: {len(results)}편")
    out.append(f"- **평균 길이**: {avg_chars:.0f}자 (공백 포함 본문) / {avg_words:.0f}단어 / {avg_lines:.0f}줄")
    out.append(f"- **평균 미만 게시글**: **{len(below_avg)}편** (전체의 {len(below_avg)/len(results)*100:.1f}%)\n")
    out.append("| 순위 | 제목 | 글자 수 | 줄 수 | 평균 대비 비율 | 파일 경로 |")
    out.append("| :--- | :--- | :---: | :---: | :---: | :--- |")
    for idx, p in enumerate(below_avg, 1):
        ratio = (p['chars'] / avg_chars) * 100
        # clean markdown table chars
        clean_title = p['title'].replace('|', '-').replace('[', '(').replace(']', ')')
        norm_path = p['path'].replace('\\', '/')
        basename = os.path.basename(p['path'])
        parent = os.path.basename(os.path.dirname(p['path']))
        out.append(f"| {idx} | {clean_title} | {p['chars']:,}자 | {p['lines']}줄 | **{ratio:.1f}%** | [{parent}/{basename}](file:///{norm_path}) |")
    out.append("\n")
    return "\n".join(out)

def main():
    gb_en = analyze_files(glob.glob(r"D:\ai\antigravity\global_blog\blog\**\index.md", recursive=True))
    gb_ko = analyze_files(glob.glob(r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog\**\index.md", recursive=True))
    nb_posts = analyze_files(glob.glob(r"D:\ai\antigravity\naver_blog\posts\**\post.md", recursive=True))
    
    report = "# 게시글 길이 비교 및 평균 미만 게시글 전수 조사 보고서\n\n"
    report += format_summary("1. 글로벌 블로그 (GlobalDevLog 영문 원본 기준)", gb_en)
    report += format_summary("2. 글로벌 블로그 (GlobalDevLog 한국어 번역본 기준)", gb_ko)
    report += format_summary("3. 네이버 블로그 공식 포스팅 (post.md 기준)", nb_posts)
    
    out_file = r"D:\ai\antigravity\global_blog\tools\length_analysis_report.md"
    with open(out_file, 'w', encoding='utf-8') as fp:
        fp.write(report)
    print("Report generated successfully at:", out_file)

if __name__ == '__main__':
    main()
