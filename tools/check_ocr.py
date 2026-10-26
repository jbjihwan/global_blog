import sys
for mod in ["pytesseract", "easyocr"]:
    try:
        __import__(mod)
        print(f"{mod} available")
    except ImportError:
        print(f"{mod} not available")
