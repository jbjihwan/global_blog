#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check domain availability and registration status via DNS and RDAP.
"""

import socket
import urllib.request
import json
import time

DOMAINS = [
    "engjourney.com",
    "globaldevlog.com",
    "globaldev.blog",
    "autonodev.com",
    "deepdevlog.com",
    "jihwandev.com",
    "jihwanlog.com",
    "parkdev.tech",
    "parklog.dev",
    "mindvision.dev",
    "coredevops.com"
]

def check_dns(domain):
    try:
        ip = socket.gethostbyname(domain)
        return True, ip
    except socket.gaierror:
        return False, None

def check_rdap(domain):
    url = f"https://rdap.org/domain/{domain}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                # If RDAP returns 200, domain is registered
                handle = data.get("handle", "")
                events = data.get("events", [])
                reg_date = ""
                for ev in events:
                    if ev.get("eventAction") == "registration":
                        reg_date = ev.get("eventDate", "")[:10]
                return "REGISTERED (Taken)", reg_date
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "AVAILABLE (등록 가능)", ""
        else:
            return f"HTTP {e.code}", ""
    except Exception as e:
        return f"ERROR ({e})", ""

def main():
    print(f"{'Domain':<20} | {'Status':<22} | {'DNS IP':<16} | {'Registered Date'}")
    print("-" * 75)
    for d in DOMAINS:
        has_dns, ip = check_dns(d)
        rdap_status, reg_date = check_rdap(d)
        ip_str = ip if ip else "-"
        print(f"{d:<20} | {rdap_status:<22} | {ip_str:<16} | {reg_date}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
