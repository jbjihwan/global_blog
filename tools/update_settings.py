# -*- coding: utf-8 -*-
import os
import json
import shutil

settings_path = os.path.expanduser(r"~\.gemini\antigravity-cli\settings.json")
print(f"Target settings path: {settings_path}")

if not os.path.exists(settings_path):
    print("settings.json does not exist yet. Creating new one.")
    data = {}
else:
    backup_path = settings_path + ".bak"
    shutil.copy2(settings_path, backup_path)
    print(f"Backed up settings.json to {backup_path}")
    with open(settings_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error parsing json: {e}")
            data = {}

if "permissions" not in data:
    data["permissions"] = {}

if "allow" not in data["permissions"]:
    data["permissions"]["allow"] = []

allow_list = data["permissions"]["allow"]
rules_to_add = [
    "command(*)",
    "command(powershell)",
    "command(python)",
    "command(git)",
]

added = []
for rule in rules_to_add:
    if rule not in allow_list:
        allow_list.append(rule)
        added.append(rule)

with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Successfully updated settings.json! Added rules: {added}")
print("Current allow list:", json.dumps(allow_list, indent=2))
