import zipfile
import os

pptx_files = [
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week16\1학기_최종발표_마음이.pptx",
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week6\캡디_6주차_발표자료.pptx",
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week8\마음이_8주차_발표.pptx",
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week10\6팀 10주차 발표자료.pptx",
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week11\Qwen35-9B_r32_alpha_ablation_발표자료.pptx",
]

for p in pptx_files:
    if not os.path.exists(p):
        print(f"Not found: {p}")
        continue
    print(f"\n=== PPTX: {os.path.basename(p)} ===")
    try:
        with zipfile.ZipFile(p, 'r') as z:
            media_list = [name for name in z.namelist() if name.startswith("ppt/media/")]
            print(f"Total embedded media: {len(media_list)}")
            for m in media_list[:15]:
                info = z.getinfo(m)
                print(f"  {m} ({info.file_size // 1024} KB)")
            if len(media_list) > 15:
                print(f"  ... and {len(media_list) - 15} more media files")
    except Exception as e:
        print(f"Error reading {p}: {e}")
