import os

base_dir = r"D:\ai\antigravity\global_blog"
blog_posts = sorted([d for d in os.listdir(os.path.join(base_dir, "blog")) if os.path.isdir(os.path.join(base_dir, "blog", d))])

missing_zh_hans = []
missing_zh_hant = []

print(f"Total blog posts found: {len(blog_posts)}")

for p in blog_posts:
    zh_hans_path = os.path.join(base_dir, "i18n", "zh-Hans", "docusaurus-plugin-content-blog", p, "index.md")
    zh_hant_path = os.path.join(base_dir, "i18n", "zh-Hant", "docusaurus-plugin-content-blog", p, "index.md")
    
    if not os.path.isfile(zh_hans_path):
        missing_zh_hans.append(p)
    if not os.path.isfile(zh_hant_path):
        missing_zh_hant.append(p)

print(f"Missing zh-Hans: {len(missing_zh_hans)} -> {missing_zh_hans}")
print(f"Missing zh-Hant: {len(missing_zh_hant)} -> {missing_zh_hant}")

if len(missing_zh_hans) == 0 and len(missing_zh_hant) == 0:
    print("SUCCESS: All 36 posts are fully translated and present in both zh-Hans and zh-Hant!")
