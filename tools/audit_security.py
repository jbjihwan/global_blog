import os
import re
import subprocess

REPO_DIR = r"D:\ai\antigravity\global_blog"

PATTERNS = [
    (r'(?i)(api[_-]?key|secret|token|password|auth|bearer)\s*[:=]\s*["\']([^"\']{8,})["\']', "Potential Key/Secret Assignment"),
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token"),
    (r'sk-[a-zA-Z0-9]{32,}', "OpenAI/Claude API Key"),
    (r'AIzaSy[a-zA-Z0-9_-]{33}', "Google API Key"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key"),
    (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', "Private Key Certificate"),
]

def check_files():
    print("=== 1. Checking Tracked Files for Secrets ===")
    found = 0
    # Use git ls-files
    result = subprocess.run(["git", "-C", REPO_DIR, "ls-files"], capture_output=True, text=True, encoding="utf-8")
    files = result.stdout.splitlines()
    for rel_path in files:
        if rel_path.endswith((".png", ".jpg", ".jpeg", ".ico", ".svg", ".lock", "package-lock.json")):
            continue
        full_path = os.path.join(REPO_DIR, rel_path)
        if not os.path.exists(full_path):
            continue
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for pat, label in PATTERNS:
                    matches = re.findall(pat, content)
                    for m in matches:
                        # Exclude harmless examples or tracking IDs
                        val = m[1] if isinstance(m, tuple) and len(m) > 1 else m
                        if "G-VM2CVW28SL" in str(val) or "jbjihwan" in str(val):
                            continue
                        print(f"[ALERT] {label} in {rel_path}: {val[:15]}...")
                        found += 1
        except Exception as e:
            print(f"Error reading {rel_path}: {e}")
    if found == 0:
        print("[OK] No hardcoded secrets or API keys found in tracked files.")

def check_git_diff_secrets():
    print("\n=== 2. Checking Recent Git Commits for Secrets ===")
    result = subprocess.run(["git", "-C", REPO_DIR, "log", "-n", "10", "-p"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    log_content = result.stdout
    found = 0
    for pat, label in PATTERNS:
        matches = re.findall(pat, log_content)
        for m in matches:
            val = m[1] if isinstance(m, tuple) and len(m) > 1 else m
            if "G-VM2CVW28SL" in str(val) or "jbjihwan" in str(val):
                continue
            print(f"[ALERT] {label} in git commit diff: {val[:15]}...")
            found += 1
    if found == 0:
        print("[OK] No secrets found in recent git commit history.")

def check_privacy_pii():
    print("\n=== 3. Checking for PII / Real Phone Numbers / Sensitive Info ===")
    # Korean phone number: 010-XXXX-XXXX
    phone_pattern = r'01[016789]-\d{3,4}-\d{4}'
    # Resident registration number pattern
    rrn_pattern = r'\d{6}-[1-4]\d{6}'
    found = 0
    result = subprocess.run(["git", "-C", REPO_DIR, "ls-files", "blog/*.md", "i18n/*/docusaurus-plugin-content-blog/**/*.md"], capture_output=True, text=True, encoding="utf-8")
    for rel_path in result.stdout.splitlines():
        full_path = os.path.join(REPO_DIR, rel_path)
        if not os.path.exists(full_path):
            continue
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                phones = re.findall(phone_pattern, content)
                rrns = re.findall(rrn_pattern, content)
                if phones:
                    print(f"[ALERT] Phone number in {rel_path}: {phones}")
                    found += len(phones)
                if rrns:
                    print(f"[ALERT] Resident Registration Number in {rel_path}: {rrns}")
                    found += len(rrns)
        except Exception as e:
            pass
    if found == 0:
        print("[OK] No PII (phone numbers, resident numbers) detected in blog posts.")

if __name__ == "__main__":
    check_files()
    check_git_diff_secrets()
    check_privacy_pii()
