# -*- coding: utf-8 -*-
import urllib.request
import urllib.error

sample_urls = [
    "https://globaldevlog.com/de/blog/stanford-cs146s-1-modern-software-developer",
    "https://globaldevlog.com/fr/blog/stanford-cs146s-1-modern-software-developer",
    "https://globaldevlog.com/pt-BR/blog/stanford-cs146s-1-modern-software-developer",
    "https://globaldevlog.com/pt-BR/blog/static-site-security-npm-audit-truth",
    "https://globaldevlog.com/pt-BR/blog/2026-06-25-vision-anpr-1",
    "https://globaldevlog.com/pt-BR/blog/2026-05-17-rl-qlearning-1",
    "https://globaldevlog.com/pt-BR/blog/maeumjigi-1"
]

for u in sample_urls:
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[{resp.status}] {u}")
    except Exception as e:
        print(f"[ERR: {e}] {u}")
