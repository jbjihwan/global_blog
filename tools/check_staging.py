import os

staging_dir = r"D:\ai\antigravity\global_blog\배포대기"
if os.path.exists(staging_dir):
    print("Contents of 배포대기:")
    for item in os.listdir(staging_dir):
        print(f" - {item}")
else:
    print("Staging dir does not exist.")
