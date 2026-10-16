import os
import shutil
import glob

blog_root = r"D:\ai\antigravity\global_blog"
cv_root = r"D:\CV"

# Diagram file
diagram_matches = glob.glob(os.path.join(cv_root, "*Mermaid*.png"))
diagram_path = diagram_matches[0] if diagram_matches else None

# Image sources
img_162313 = os.path.join(cv_root, "Catch-Lane-Intrusion-Blackbox-KOR-ANPR-System", "162313_D_v11.png")
img_163614_v11 = os.path.join(cv_root, "Catch-Lane-Intrusion-Blackbox-KOR-ANPR-System", "163614_D_v11.png")
img_163614_fin = os.path.join(cv_root, "Term_project", "163614_D_fin.png")
img_163614_v11_1 = os.path.join(cv_root, "Term_project", "163614_D_v11_1.png")
img_163614_fin_1 = os.path.join(cv_root, "Term_project", "163614_D_fin_1.png")

posts_mapping = {
    "2026-06-25-vision-anpr-1": [
        (diagram_path, "01_pipeline_diagram.png"),
        (img_163614_v11, "02_final_result.png")
    ],
    "2026-06-26-vision-anpr-2": [
        (img_162313, "01_lane_detection.png"),
        (img_163614_fin, "02_intrusion_iou.png")
    ],
    "2026-06-27-vision-anpr-3": [
        (img_163614_v11_1, "01_plate_localization.png"),
        (img_163614_fin_1, "02_csrt_tracking.png")
    ],
    "2026-06-28-vision-anpr-4": [
        (img_163614_v11, "01_edsr_sr_comparison.png"),
        (img_162313, "02_frame_stacking.png")
    ],
    "2026-06-29-vision-anpr-5": [
        (img_163614_fin, "01_voting_evolution.png"),
        (img_163614_v11, "02_final_system.png")
    ]
}

locales = [
    os.path.join(blog_root, "blog"),
    os.path.join(blog_root, "i18n", "ko", "docusaurus-plugin-content-blog"),
    os.path.join(blog_root, "i18n", "ja", "docusaurus-plugin-content-blog"),
    os.path.join(blog_root, "i18n", "es", "docusaurus-plugin-content-blog"),
]

for post_slug, img_list in posts_mapping.items():
    for loc_dir in locales:
        post_dir = os.path.join(loc_dir, post_slug)
        img_dir = os.path.join(post_dir, "images")
        os.makedirs(img_dir, exist_ok=True)
        for src, dest_name in img_list:
            if src and os.path.exists(src):
                dest = os.path.join(img_dir, dest_name)
                shutil.copy2(src, dest)
                print(f"Copied {src} -> {dest}")

print("Image setup completed successfully!")
