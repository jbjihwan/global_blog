# -*- coding: utf-8 -*-
import os

gb_root = r"D:\ai\antigravity\global_blog"
nb_root = r"D:\ai\antigravity\naver_blog\posts\2026-10-22\stanford_cs146s_1"
folder_name = "2026-10-22-stanford-cs146s-1"

targets = [
    {
        "path": f"{gb_root}/blog/{folder_name}/index.md",
        "ref": """
---

### References & Course Materials
- **Official Course Video Playlist**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Academic Institution**: Stanford University, Department of Computer Science
"""
    },
    {
        "path": f"{gb_root}/i18n/ko/docusaurus-plugin-content-blog/{folder_name}/index.md",
        "ref": """
---

### 참고 자료 및 공식 출처 (References)
- **스탠포드 공식 강의 영상 재생목록**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **개설 기관**: Stanford University, Department of Computer Science
"""
    },
    {
        "path": f"{gb_root}/i18n/es/docusaurus-plugin-content-blog/{folder_name}/index.md",
        "ref": """
---

### Referencias y Materiales del Curso
- **Lista de Reproducción Oficial de Videos**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **Institución Académica**: Stanford University, Department of Computer Science
"""
    },
    {
        "path": f"{gb_root}/i18n/ja/docusaurus-plugin-content-blog/{folder_name}/index.md",
        "ref": """
---

### 参考資料および公式講義映像 (References)
- **スタンフォード公式講義動画プレイリスト**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **開講機関**: Stanford University, Department of Computer Science
"""
    },
    {
        "path": f"{gb_root}/i18n/zh-Hans/docusaurus-plugin-content-blog/{folder_name}/index.md",
        "ref": """
---

### 参考资料与官方课程视频 (References)
- **斯坦福官方课程视频播放列表**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **开设机构**: Stanford University, Department of Computer Science
"""
    },
    {
        "path": f"{gb_root}/i18n/zh-Hant/docusaurus-plugin-content-blog/{folder_name}/index.md",
        "ref": """
---

### 參考資料與官方課程影片 (References)
- **史丹佛官方課程影片播放清單**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
- **開設機構**: Stanford University, Department of Computer Science
"""
    },
    {
        "path": f"{nb_root}/post.md",
        "ref": """
---

## 5. 공식 출처 및 스탠포드 강의 영상 안내

본 포스팅은 미국 스탠포드 대학교 컴퓨터공학과(Stanford University, Department of Computer Science)의 최신 소프트웨어 공학 강좌 내용을 바탕으로 작성되었습니다:

🎥 **스탠포드 공식 강의 유튜브 재생목록 바로가기**: [Stanford CS146S: The Modern Software Development (YouTube Playlist)](https://www.youtube.com/playlist?list=PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9)
"""
    }
]

for t in targets:
    p = t["path"]
    if not os.path.exists(p):
        print(f"File not found: {p}")
        continue
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if playlist link is already present
    if "PLxpwjSdVZQ95OWe3QvkVEcU1f1X-6NDj9" in content:
        print(f"Already contains link: {p}")
        continue
        
    updated = content.rstrip() + "\n" + t["ref"].strip() + "\n"
    with open(p, 'w', encoding='utf-8') as f:
        f.write(updated)
    print(f"Appended source reference to: {p}")

print("All references updated successfully!")
