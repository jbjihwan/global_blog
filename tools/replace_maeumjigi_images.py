import os
import shutil
from PIL import Image

EXTRACT_DIR = r"D:\ai\antigravity\global_blog\extracted_ppt_images"
CAPDE_ROOT = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플"
BLOG_ROOT = r"D:\ai\antigravity\global_blog"

# Mapping for 23 episodes: (folder_name, img1_path, img2_path, img2_filename)
MAPPINGS = [
    # #1 (2026-03-26)
    ("2026-03-26-maeumjigi-1", 
     os.path.join(EXTRACT_DIR, "week2", "image1.png"), 
     os.path.join(EXTRACT_DIR, "week2", "image11.png"), 
     "02_term.png"),
    
    # #2 (2026-03-30)
    ("2026-03-30-maeumjigi-2", 
     os.path.join(EXTRACT_DIR, "week2", "image11.png"), 
     os.path.join(EXTRACT_DIR, "week6", "fImage13575859741.png"), 
     "02_term.png"),
     
    # #3 (2026-03-31)
    ("2026-03-31-maeumjigi-3", 
     os.path.join(CAPDE_ROOT, r"Week12\_preview\s02.png"), 
     os.path.join(EXTRACT_DIR, "week6", "fImage142995826491.jpeg"), 
     "02_term.png"),
     
    # #4 (2026-04-01)
    ("2026-04-01-maeumjigi-4", 
     os.path.join(CAPDE_ROOT, r"Week6\학습데이터별학습결과.png"), 
     os.path.join(EXTRACT_DIR, "week6", "fImage1523757929358.jpeg"), 
     "02_term.png"),
     
    # #5 (2026-04-03)
    ("2026-04-03-maeumjigi-5", 
     os.path.join(CAPDE_ROOT, r"Week6\테스트결과지표_1.png"), 
     os.path.join(CAPDE_ROOT, r"Week6\테스트결과지표_2.png"), 
     "02_term.png"),
     
    # #6 (2026-04-05)
    ("2026-04-05-maeumjigi-6", 
     os.path.join(CAPDE_ROOT, r"Week6\프론트엔드버그.png"), 
     os.path.join(CAPDE_ROOT, r"Week6\테스트 결과.png"), 
     "02_term.png"),
     
    # #7 (2026-04-07)
    ("2026-04-07-maeumjigi-7", 
     os.path.join(CAPDE_ROOT, r"Week7\test_result(M0,M5,M6).png"), 
     os.path.join(CAPDE_ROOT, r"Week6\테스트결과지표_1.png"), 
     "02_term.png"),
     
    # #8 (2026-04-08)
    ("2026-04-08-maeumjigi-8", 
     os.path.join(CAPDE_ROOT, r"Week7\training_result(M3~M6).png"), 
     os.path.join(CAPDE_ROOT, r"Week9\fine_tuning\results\figures\training\02_gpu_memory.png"), 
     "02_term.png"),
     
    # #9 (2026-04-09)
    ("2026-04-09-maeumjigi-9", 
     os.path.join(EXTRACT_DIR, "week8", "fImage18499422941.png"), 
     os.path.join(EXTRACT_DIR, "week8", "fImage6549712286334.png"), 
     "02_term.png"),
     
    # #10 (2026-04-14)
    ("2026-04-14-maeumjigi-10", 
     os.path.join(CAPDE_ROOT, r"Week8\lora_rank_decomposition.png"), 
     os.path.join(CAPDE_ROOT, r"Week8\lora_formula_anatomy.png"), 
     "02_term.png"),
     
    # #11 (2026-04-19)
    ("2026-04-19-maeumjigi-11", 
     os.path.join(CAPDE_ROOT, r"Week8\llama31_with_lora_structure.png"), 
     os.path.join(CAPDE_ROOT, r"Week8\all_matrices_in_block.png"), 
     "02_term.png"),
     
    # #12 (2026-05-03)
    ("2026-05-03-maeumjigi-12", 
     os.path.join(CAPDE_ROOT, r"Week9\fine_tuning\results\figures\eval\03_radar_per_model.png"), 
     os.path.join(CAPDE_ROOT, r"Week9\llama_baseline_eval\results\comparison\figures\01_ranking_bertscore.png"), 
     "02_term.png"),
     
    # #13 (2026-05-04)
    ("2026-05-04-maeumjigi-13", 
     os.path.join(CAPDE_ROOT, r"Week9\fine_tuning\results\figures\training\01_loss_curves.png"), 
     os.path.join(CAPDE_ROOT, r"Week9\fine_tuning\results\figures\training\04_eval_loss_all.png"), 
     "02_error.png"),
     
    # #14 (2026-05-06)
    ("2026-05-06-maeumjigi-14", 
     os.path.join(CAPDE_ROOT, r"Week9\fine_tuning\results\figures\eval\01_metric_comparison.png"), 
     os.path.join(CAPDE_ROOT, r"Week9\fine_tuning\results\figures\eval\02_improvement_pct.png"), 
     "02_eval.png"),
     
    # #15 (2026-05-07)
    ("2026-05-07-maeumjigi-15", 
     os.path.join(CAPDE_ROOT, r"Week9\fine_tuning\results\figures\eval\04_pareto_efficiency.png"), 
     os.path.join(CAPDE_ROOT, r"Week9\llama_baseline_eval\results\comparison\figures\06_inference_speed.png"), 
     "02_graph.png"),
     
    # #16 (2026-05-08)
    ("2026-05-08-maeumjigi-16", 
     os.path.join(CAPDE_ROOT, r"Week9\GPU사용량\01_llama33_70b (1) GPU 사용량.png"), 
     os.path.join(CAPDE_ROOT, r"Week9\GPU사용량\Qwen35-9B_root@958391d840d6_ ~ 2026-04-26 오전 2_10_15.png"), 
     "02_app.png"),
     
    # #17 (2026-05-12)
    ("2026-05-12-maeumjigi-17", 
     os.path.join(EXTRACT_DIR, "week10", "fImage3443004488467.png"), 
     os.path.join(EXTRACT_DIR, "week10", "fImage3469618198467.png"), 
     "02_bug.png"),
     
    # #18 (2026-05-13)
    ("2026-05-13-maeumjigi-18", 
     os.path.join(CAPDE_ROOT, r"Week9\fine_tuning\results\figures\training\03_training_loss_all.png"), 
     os.path.join(CAPDE_ROOT, r"Week9\fine_tuning\results\figures\eval\base_model_graph.png"), 
     "02_graph.png"),
     
    # #19 (2026-05-17)
    ("2026-05-17-maeumjigi-19", 
     os.path.join(CAPDE_ROOT, r"Week12\_preview\s07.png"), 
     os.path.join(CAPDE_ROOT, r"Week15\견적_1차시도.png"), 
     "02_db.png"),
     
    # #20 (2026-05-20)
    ("2026-05-20-maeumjigi-20", 
     os.path.join(EXTRACT_DIR, "week16_final", "web_feature_1.jpeg"), 
     os.path.join(EXTRACT_DIR, "week16_final", "web_feature_2.jpeg"), 
     "02_app_feature.png"),
     
    # #21 (2026-05-22)
    ("2026-05-22-maeumjigi-21", 
     os.path.join(EXTRACT_DIR, "week16_final", "web_feature_3.jpeg"), 
     os.path.join(EXTRACT_DIR, "week16_final", "web_feature_4.jpeg"), 
     "02_ratio.png"),
     
    # #22 (2026-05-30)
    ("2026-05-30-maeumjigi-22", 
     os.path.join(EXTRACT_DIR, "week16_final", "web_feature_5.jpeg"), 
     os.path.join(EXTRACT_DIR, "week16_final", "web_feature_6.jpeg"), 
     "02_architecture.png"),
     
    # #23 (2026-06-18)
    ("2026-06-18-maeumjigi-23", 
     os.path.join(CAPDE_ROOT, r"Week12\_preview\s01.png"), 
     os.path.join(CAPDE_ROOT, r"Week12\_preview\s05.png"), 
     "02_presentation.png"),
]

LOCALES = [
    r"blog",
    r"i18n\ko\docusaurus-plugin-content-blog",
    r"i18n\ja\docusaurus-plugin-content-blog",
    r"i18n\es\docusaurus-plugin-content-blog",
]

def save_as_png(src_path, dst_path):
    with Image.open(src_path) as im:
        rgb_im = im.convert("RGBA" if im.mode in ("RGBA", "P") else "RGB")
        rgb_im.save(dst_path, format="PNG", optimize=True)

def apply_replacement():
    print("=== Replacing AI images with authentic PPT & coursework images ===")
    success_count = 0
    for post_dir, img1_src, img2_src, img2_name in MAPPINGS:
        if not os.path.exists(img1_src):
            print(f"[ERROR] img1 not found: {img1_src}")
            continue
        if not os.path.exists(img2_src):
            print(f"[ERROR] img2 not found: {img2_src}")
            continue
            
        for loc in LOCALES:
            target_img_dir = os.path.join(BLOG_ROOT, loc, post_dir, "images")
            os.makedirs(target_img_dir, exist_ok=True)
            
            dst1 = os.path.join(target_img_dir, "01_cover.png")
            dst2 = os.path.join(target_img_dir, img2_name)
            
            save_as_png(img1_src, dst1)
            save_as_png(img2_src, dst2)
            
        print(f"[DONE] {post_dir}: 01_cover.png <- {os.path.basename(img1_src)}, {img2_name} <- {os.path.basename(img2_src)}")
        success_count += 1
        
    print(f"\nSuccessfully replaced images for {success_count} / {len(MAPPINGS)} episodes across all 4 locales!")

if __name__ == "__main__":
    apply_replacement()
