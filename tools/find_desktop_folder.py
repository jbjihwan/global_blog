import os

user_home = os.path.expanduser("~")
print("User home:", user_home)
for item in os.listdir(user_home):
    full = os.path.join(user_home, item)
    if "바탕" in item or "desktop" in item.lower() or "onedrive" in item.lower():
        print(f" -> {item}")

# Check inside OneDrive if present
onedrive = os.path.join(user_home, "OneDrive")
if os.path.exists(onedrive):
    print("Inside OneDrive:")
    for item in os.listdir(onedrive):
        print(f"   -> {item}")
