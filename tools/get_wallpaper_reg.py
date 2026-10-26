import winreg

try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop")
    val, _ = winreg.QueryValueEx(key, "Wallpaper")
    print("Wallpaper path in registry:", val)
    winreg.CloseKey(key)
except Exception as e:
    print("Error reading registry:", e)
