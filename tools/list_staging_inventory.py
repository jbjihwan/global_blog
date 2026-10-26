import os, json

staging_dir = r"D:\ai\antigravity\global_blog\배포대기"
items = sorted([d for d in os.listdir(staging_dir) if os.path.isdir(os.path.join(staging_dir, d))])
print("Current Staging Directory Inventory:")
for idx, d in enumerate(items, 1):
    info_path = os.path.join(staging_dir, d, "stage_info.json")
    status = "N/A"
    if os.path.exists(info_path):
        try:
            with open(info_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                status = data.get("status", "unknown")
        except:
            pass
    print(f" {idx}. {d:<32} [Status: {status}]")
