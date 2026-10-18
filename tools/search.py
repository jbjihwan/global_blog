#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zero-Popup File & Text Search Tool for Antigravity CLI.
Runs via pre-approved `python -X utf8` to eliminate PowerShell pipeline permission prompts.
"""

import os
import sys
import argparse
import fnmatch
import re

DEFAULT_IGNORE_DIRS = {'.git', 'node_modules', '.docusaurus', 'build', '.cache', '__pycache__', '.venv', 'venv'}

def search_files(base_dir, name_pattern=None, grep_pattern=None, extensions=None, max_results=50, ignore_dirs=True):
    results = []
    base_dir = os.path.abspath(base_dir)
    
    if not os.path.exists(base_dir):
        print(f"[ERROR] Directory does not exist: {base_dir}", file=sys.stderr)
        return []

    regex = None
    if grep_pattern:
        try:
            regex = re.compile(grep_pattern, re.IGNORECASE)
        except re.error:
            # Fallback to literal search if invalid regex
            regex = None

    ext_set = None
    if extensions:
        ext_set = {e.lower() if e.startswith('.') else f".{e.lower()}" for e in extensions}

    count = 0
    for root, dirs, files in os.walk(base_dir):
        if ignore_dirs:
            dirs[:] = [d for d in dirs if d not in DEFAULT_IGNORE_DIRS]

        # Directory name match if name_pattern is set and no grep_pattern
        if name_pattern and not grep_pattern:
            for dname in dirs:
                if fnmatch.fnmatch(dname.lower(), name_pattern.lower()):
                    rel_dir = os.path.relpath(os.path.join(root, dname), base_dir)
                    results.append(f"[DIR] {rel_dir}")
                    count += 1
                    if count >= max_results:
                        return results

        for fname in files:
            if ext_set:
                _, ext = os.path.splitext(fname)
                if ext.lower() not in ext_set:
                    continue

            # Filename pattern match
            if name_pattern:
                if not fnmatch.fnmatch(fname.lower(), name_pattern.lower()):
                    continue

            file_path = os.path.join(root, fname)

            # Grep inside content if requested
            if grep_pattern:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_idx, line in enumerate(f, 1):
                            matched = False
                            if regex:
                                matched = bool(regex.search(line))
                            else:
                                matched = grep_pattern.lower() in line.lower()
                            
                            if matched:
                                rel_path = os.path.relpath(file_path, base_dir)
                                results.append(f"{rel_path}:{line_idx}: {line.strip()[:140]}")
                                count += 1
                                if count >= max_results:
                                    return results
                except Exception:
                    continue
            else:
                # Name-only match
                rel_path = os.path.relpath(file_path, base_dir)
                results.append(f"{rel_path}")
                count += 1
                if count >= max_results:
                    return results

    return results

def main():
    parser = argparse.ArgumentParser(description="Antigravity Zero-Popup File/Content Search Utility")
    parser.add_argument("--dir", "-d", default=".", help="Root directory to search (default: current directory)")
    parser.add_argument("--name", "-n", default=None, help="Filename pattern to match (e.g. '*security*')")
    parser.add_argument("--grep", "-g", default=None, help="Text/Regex pattern to search within file contents")
    parser.add_argument("--ext", "-e", nargs="*", default=None, help="File extensions to include (e.g. md tsx py)")
    parser.add_argument("--max", "-m", type=int, default=50, help="Maximum number of matches to return (default: 50)")
    parser.add_argument("--all", "-a", action="store_true", help="Include ignored directories (node_modules, build, etc.)")

    args = parser.parse_args()

    matches = search_files(
        base_dir=args.dir,
        name_pattern=args.name,
        grep_pattern=args.grep,
        extensions=args.ext,
        max_results=args.max,
        ignore_dirs=not args.all
    )

    if not matches:
        print("[No matches found]")
        return

    print(f"[Found {len(matches)} matches]:")
    for m in matches:
        print(m)

if __name__ == "__main__":
    main()
