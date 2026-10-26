import zipfile, xml.etree.ElementTree as ET

pptx_path = r"C:\Users\jbgih\Downloads\[6팀]2학기_1차발표_마음이_여름방학_진행보고.pptx"

with zipfile.ZipFile(pptx_path, 'r') as z:
    for name in z.namelist():
        if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
            root = ET.fromstring(z.read(name))
            texts = [node.text for node in root.iter() if node.text]
            print(f"\n--- {name} ---")
            print(" ".join(texts[:20]))
