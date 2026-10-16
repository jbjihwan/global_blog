import os
import glob
import re
import shutil

# Target acronyms and their full forms for each language
acronyms = {
    'ko': {'AI': '인공지능(AI)', 'LLM': '거대 언어 모델(LLM)', 'API': '응용 프로그램 인터페이스(API)', 'DB': '데이터베이스(DB)'},
    'en': {'AI': 'Artificial Intelligence (AI)', 'LLM': 'Large Language Model (LLM)', 'API': 'Application Programming Interface (API)', 'DB': 'Database (DB)'},
    'ja': {'AI': '人工知能(AI)', 'LLM': '大規模言語モデル(LLM)', 'API': 'アプリケーションプログラミングインターフェース(API)', 'DB': 'データベース(DB)'},
    'es': {'AI': 'Inteligencia Artificial (AI)', 'LLM': 'Modelo de Lenguaje Grande (LLM)', 'API': 'Interfaz de Programación de Aplicaciones (API)', 'DB': 'Base de Datos (DB)'}
}

graph_img = r"C:\Users\jbgih\.gemini\antigravity-cli\brain\81df2a36-b022-405e-98f3-3e13cf3ddd87\alpha_comparison_graph_1791123607289.jpg"
blog_root = r"D:\ai\antigravity\global_blog"

# Iterate over all posts
posts_en = glob.glob(os.path.join(blog_root, 'blog', '*'))
posts_ko = glob.glob(os.path.join(blog_root, 'i18n', 'ko', 'docusaurus-plugin-content-blog', '*'))
posts_ja = glob.glob(os.path.join(blog_root, 'i18n', 'ja', 'docusaurus-plugin-content-blog', '*'))
posts_es = glob.glob(os.path.join(blog_root, 'i18n', 'es', 'docusaurus-plugin-content-blog', '*'))

all_posts = []
for p, lang in [(posts_en, 'en'), (posts_ko, 'ko'), (posts_ja, 'ja'), (posts_es, 'es')]:
    for folder in p:
        if os.path.isdir(folder):
            all_posts.append((folder, lang))

# Compile regex to find bare acronyms safely (ignoring if they are inside words or already formatted)
# Negative lookbehinds and lookaheads to avoid matching inside brackets e.g. (AI) or words like TRAIN
def process_content(content, lang):
    new_content = content
    for acr, full in acronyms[lang].items():
        # Clean existing explicit full forms so we can re-apply cleanly
        new_content = new_content.replace(full, acr)
        # Also clean patterns like Artificial Intelligence(AI) or (AI) if they exist
        if lang == 'ko':
            new_content = re.sub(r'인공지능\s*\(AI\)', 'AI', new_content)
            new_content = re.sub(r'거대 언어 모델\s*\(LLM\)', 'LLM', new_content)
            new_content = re.sub(r'대규모 언어 모델\s*\(LLM\)', 'LLM', new_content)
            new_content = re.sub(r'응용 프로그램 인터페이스\s*\(API\)', 'API', new_content)
            new_content = re.sub(r'데이터베이스\s*\(DB\)', 'DB', new_content)
        elif lang == 'en':
            new_content = re.sub(r'Artificial Intelligence\s*\(AI\)', 'AI', new_content, flags=re.I)
            new_content = re.sub(r'Large Language Model\s*\(LLM\)', 'LLM', new_content, flags=re.I)
            new_content = re.sub(r'Application Programming Interface\s*\(API\)', 'API', new_content, flags=re.I)
            new_content = re.sub(r'Database\s*\(DB\)', 'DB', new_content, flags=re.I)
        elif lang == 'ja':
            new_content = re.sub(r'人工知能\s*\(AI\)', 'AI', new_content)
            new_content = re.sub(r'大規模言語モデル\s*\(LLM\)', 'LLM', new_content)
            new_content = re.sub(r'アプリケーションプログラミングインターフェース\s*\(API\)', 'API', new_content)
            new_content = re.sub(r'データベース\s*\(DB\)', 'DB', new_content)
        elif lang == 'es':
            new_content = re.sub(r'Inteligencia Artificial\s*\(AI\)', 'AI', new_content, flags=re.I)
            new_content = re.sub(r'Modelo de Lenguaje Grande\s*\(LLM\)', 'LLM', new_content, flags=re.I)
            new_content = re.sub(r'Interfaz de Programación de Aplicaciones\s*\(API\)', 'API', new_content, flags=re.I)
            new_content = re.sub(r'Base de Datos\s*\(DB\)', 'DB', new_content, flags=re.I)

        # Now all mentions are just bare acronyms. We want to find the FIRST occurrence and replace it.
        # But we must not replace it inside HTML image tags or URLs.
        # A simple hack: split by the acronym with word boundaries.
        pattern = r'(?<![a-zA-Z\(\[])\b' + acr + r'\b(?![a-zA-Z\)\]])'
        
        parts = re.split(pattern, new_content)
        if len(parts) > 1:
            # Rejoin the first part with the FULL name, and the rest with the bare acronym
            new_content = parts[0] + full + acr.join(parts[1:])
            
    return new_content

for folder, lang in all_posts:
    md_file = os.path.join(folder, 'index.md')
    if not os.path.exists(md_file):
        continue
        
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # If this is a comparison post, replace its first image (01_cover.png or 02) with the bar graph
    is_compare = '비교' in content or 'compar' in content.lower() or '比較' in content or 'comparación' in content.lower()
    
    if is_compare:
        img_dir = os.path.join(folder, 'images')
        os.makedirs(img_dir, exist_ok=True)
        img_dest = os.path.join(img_dir, '01_cover.png')
        if os.path.exists(img_dest):
            shutil.copy(graph_img, img_dest)

    # Process acronyms
    updated_content = process_content(content, lang)
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

print("Done processing acronyms and images!")
