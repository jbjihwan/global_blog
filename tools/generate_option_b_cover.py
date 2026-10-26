import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

web_img_path = r"D:\Projects\26_1\CapDe\maeumjigi\test-results\관련사진\웹2_인터프린터클릭시챗봇으로넘어가고메시지시현.png"
app_img_path = r"D:\Projects\26_1\CapDe\maeumjigi\test-results\관련사진\Screenshot_20260728_220115_Expo Go.jpg"

W, H = 1920, 1080
canvas = Image.new("RGBA", (W, H), (15, 23, 42, 255))
draw = ImageDraw.Draw(canvas)

# Decorative background grid lines
for y in range(0, H, 60):
    draw.line([(0, y), (W, y)], fill=(30, 41, 59, 120), width=1)
for x in range(0, W, 80):
    draw.line([(x, 0), (x, H)], fill=(30, 41, 59, 120), width=1)

# Header banner
draw.rectangle([(0, 0), (W, 90)], fill=(30, 41, 59, 230))
draw.line([(0, 90), (W, 90)], fill=(56, 189, 248, 255), width=3)

font_title = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 36)
font_sub = ImageFont.truetype(r"C:\Windows\Fonts\malgun.ttf", 22)

draw.text((60, 26), "마음지기 (Maeumjigi) AI 캡스톤 프로젝트 실기 시현 (Web & Mobile Expo)", fill=(255, 255, 255), font=font_title)
draw.text((1350, 32), "Capstone Design · Live Deployment", fill=(56, 189, 248), font=font_sub)

# Load Web screenshot
web_im = Image.open(web_img_path).convert("RGBA")
# Target height for web: 880
web_h = 880
web_w = int(web_im.width * (web_h / web_im.height))
web_resized = web_im.resize((web_w, web_h), Image.Resampling.LANCZOS)

# Position Web screenshot on left: x=60, y=140
canvas.paste(web_resized, (60, 140))
# Add border around web screenshot
draw.rectangle([(58, 138), (60 + web_w + 1, 140 + web_h + 1)], outline=(71, 85, 105), width=2)

# Load App screenshot
app_im = Image.open(app_img_path).convert("RGBA")
# Target height for app: 880
app_h = 880
app_w = int(app_im.width * (app_h / app_im.height))
app_resized = app_im.resize((app_w, app_h), Image.Resampling.LANCZOS)

# Position App screenshot on right: x=1420, y=140
app_x = W - app_w - 80
canvas.paste(app_resized, (app_x, 140))
# Add border around app screenshot
draw.rectangle([(app_x - 2, 138), (app_x + app_w + 1, 140 + app_h + 1)], outline=(56, 189, 248), width=3)

# Label badges
font_badge = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 20)
draw.rounded_rectangle([(80, 155), (340, 195)], radius=6, fill=(15, 23, 42, 220), outline=(56, 189, 248), width=2)
draw.text((95, 162), "💻 Web 챗봇 인터페이스", fill=(56, 189, 248), font=font_badge)

draw.rounded_rectangle([(app_x + 20, 155), (app_x + 240, 195)], radius=6, fill=(15, 23, 42, 220), outline=(52, 211, 153), width=2)
draw.text((app_x + 35, 162), "📱 Mobile Expo 앱", fill=(52, 211, 153), font=font_badge)

# Target paths: blog/ and all 5 i18n locales
target_dirs = [
    r"D:\ai\antigravity\global_blog\blog\2026-03-26-maeumjigi-1\images",
    r"D:\ai\antigravity\global_blog\i18n\ko\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images",
    r"D:\ai\antigravity\global_blog\i18n\ja\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images",
    r"D:\ai\antigravity\global_blog\i18n\es\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images",
    r"D:\ai\antigravity\global_blog\i18n\zh-Hans\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images",
    r"D:\ai\antigravity\global_blog\i18n\zh-Hant\docusaurus-plugin-content-blog\2026-03-26-maeumjigi-1\images",
]

for td in target_dirs:
    os.makedirs(td, exist_ok=True)
    out_path = os.path.join(td, "01_cover.png")
    canvas.save(out_path, format="PNG")
    print(f"Saved Option B real screenshot cover to {out_path} ({os.path.getsize(out_path)} bytes)")
