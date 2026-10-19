import os
import filecmp
import glob


ko_images = glob.glob('i18n/ko/docusaurus-plugin-content-blog/**/images/*.png', recursive=True)
mismatches = 0
for ko_img in ko_images:
    rel = os.path.relpath(ko_img, 'i18n/ko/docusaurus-plugin-content-blog')
    for other_dir in ['blog', 'i18n/ja/docusaurus-plugin-content-blog', 'i18n/es/docusaurus-plugin-content-blog']:
        target = os.path.join(other_dir, rel)
        if not os.path.exists(target) or not filecmp.cmp(ko_img, target):
            print(f"Mismatch: {rel} vs {target}")
            mismatches += 1

print(f"Total images: {len(ko_images)}, Total mismatches: {mismatches}")



















