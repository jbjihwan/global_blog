import os
import re

dirs_to_check = [
    r"D:\ai\antigravity\global_blog\blog",
    r"D:\ai\antigravity\global_blog\i18n",
    r"D:\ai\antigravity\global_blog\배포대기"
]

modified_files = []

for d in dirs_to_check:
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith(".md"):
                full = os.path.join(root, f)
                with open(full, "r", encoding="utf-8") as file:
                    content = file.read()
                
                orig = content
                
                # Replace any `<` followed immediately by a digit, e.g. `<180`, `<50`, `<10`
                # If it's `(<180`, change to `(&lt;180` or `(< 180`
                content = re.sub(r'<(\d+)', r'&lt;\1', content)
                
                # Also check $O(1)$ or similar latex notation that might confuse mdx
                content = content.replace("$O(1)$", "`O(1)`")
                content = content.replace("$O(N)$", "`O(N)`")

                if content != orig:
                    with open(full, "w", encoding="utf-8") as file:
                        file.write(content)
                    modified_files.append(full)

print(f"Total files updated with &lt; fix: {len(modified_files)}")
for mf in modified_files:
    print(f" - {mf}")
