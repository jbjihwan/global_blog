import pytesseract
from PIL import Image

for p in [r"C:\Users\jbgih\OneDrive\사진\1.png", r"C:\Users\jbgih\OneDrive\바탕 화면\img_67048_2.jpg"]:
    try:
        text = pytesseract.image_to_string(Image.open(p), lang="kor+eng")
        print(f"--- OCR for {p} ---")
        print(text[:300])
    except Exception as e:
        print(f"OCR error on {p}: {e}")
