import zipfile
import re
import os

ppts = [
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week2\[6팀]캡스톤 디자인 2주차 보고서.pptx",
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week12\1학기_최종발표_마음이.pptx",
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week16\1학기_최종발표_마음이.pptx",
    r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week10\6팀 10주차 발표자료.pptx",
]

def check_slide_text():
    for p in ppts:
        if not os.path.exists(p):
            continue
        print(f"\n=== Inspecting Slide Texts: {os.path.basename(p)} ===")
        with zipfile.ZipFile(p, 'r') as z:
            slides = [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
            for s in sorted(slides):
                xml_data = z.read(s).decode("utf-8", errors="ignore")
                # Extract text inside <a:t>...</a:t>
                texts = re.findall(r'<a:t>(.*?)</a:t>', xml_data)
                full_slide_text = " ".join(texts)
                # Check for sensitive patterns: student IDs (학번: e.g. 202xxxxx, 2511xxxx), phone numbers, team member real names
                if any(w in full_slide_text for w in ["학번", "지도교수", "010-", "@"]):
                    print(f"[{s}] Sensitive candidate: {full_slide_text[:120]}...")
                # Also check title slide
                if "slide1.xml" in s:
                    print(f"[Slide 1 Title]: {full_slide_text[:150]}")

if __name__ == "__main__":
    p = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week12\1학기_최종발표_마음이.pptx"
    with zipfile.ZipFile(p, 'r') as z:
        slides = [n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
        # sort by slide number
        slides = sorted(slides, key=lambda x: int(re.search(r'slide(\d+)\.xml', x).group(1)))
        for s in slides:
            xml_data = z.read(s).decode("utf-8", errors="ignore")
            texts = re.findall(r'<a:t>(.*?)</a:t>', xml_data)
            print(f"[{s}] {' '.join(texts)[:100]}")
