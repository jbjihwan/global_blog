import os
p = r"D:\서울과기대 컴퓨터공학과\26-1\CapDe\팀플\Week15"
for f in os.listdir(p):
    fp = os.path.join(p, f)
    try:
        with open(fp, "rb") as test_f:
            data = test_f.read(100)
            print(f"Read {f}: {len(data)} bytes")
    except Exception as e:
        print(f"Cannot read {f}: {e}")
