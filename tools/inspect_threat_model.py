from PIL import Image

p = r"D:\ai\antigravity\global_blog\blog\2026-10-18-static-site-security-hardening\images\01_threat_model.png"
with Image.open(p) as im:
    print("threat_model format:", im.format, "size:", im.size, "mode:", im.mode)

p2 = r"D:\ai\antigravity\global_blog\blog\2026-10-18-static-site-security-hardening\images\02_security_pipeline.png"
with Image.open(p2) as im2:
    print("security_pipeline format:", im2.format, "size:", im2.size, "mode:", im2.mode)
