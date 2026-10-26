import os, json

dirs = [
    "2026-10-25-stanford-cs146s-4",
    "2026-10-26-stanford-cs146s-5",
    "2026-10-27-stanford-cs146s-6",
    "2026-10-28-stanford-cs146s-7",
]

base = r"D:\ai\antigravity\global_blog\배포대기"
for d in dirs:
    info_path = os.path.join(base, d, "stage_info.json")
    if os.path.exists(info_path):
        with open(info_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(d, "->", data.get("status"))
    else:
        print(d, "-> no stage_info.json")
