#!/usr/bin/env python3
"""
Deploy a deck to GitHub Pages by updating the index and pushing.

Usage:
    python3 deploy.py --repo-path /path/to/repo --title "Title" --slug "slug" --sections 5 --tags "tag1,tag2"
"""

import argparse
import json
import os
import re
import subprocess
from datetime import date


def update_index(repo_path, title, slug, sections, tags):
    """Add the new deck to the index.html DECKS array."""
    index_path = os.path.join(repo_path, "index.html")

    with open(index_path, "r") as f:
        content = f.read()

    deck_entry = {
        "title": title,
        "path": f"decks/{slug}.html",
        "sections": sections,
        "date": date.today().isoformat(),
        "tags": [t.strip() for t in tags.split(",") if t.strip()]
    }

    # Find the DECKS array and add the entry
    pattern = r"const DECKS = \[(.*?)\];"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        existing = match.group(1).strip()
        entry_json = json.dumps(deck_entry)
        if existing:
            new_array = f"{existing},\n            {entry_json}"
        else:
            new_array = f"\n            {entry_json}\n        "
        content = content[:match.start()] + f"const DECKS = [{new_array}];" + content[match.end():]

    with open(index_path, "w") as f:
        f.write(content)

    return index_path


def git_push(repo_path, title):
    """Commit and push changes."""
    cmds = [
        ["git", "add", "-A"],
        ["git", "commit", "-m", f"Add deck: {title}"],
        ["git", "push"]
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Command failed: {' '.join(cmd)}")
            print(result.stderr)
            return False
        print(result.stdout.strip())
    return True


def main():
    parser = argparse.ArgumentParser(description="Deploy deck to GitHub Pages")
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--sections", type=int, required=True)
    parser.add_argument("--tags", default="")
    args = parser.parse_args()

    print(f"Updating index with '{args.title}'...")
    update_index(args.repo_path, args.title, args.slug, args.sections, args.tags)

    print("Pushing to GitHub...")
    success = git_push(args.repo_path, args.title)

    if success:
        print(f"\nDeck live at: https://nataliazarina.github.io/learning-decks/decks/{args.slug}.html")
        print(f"Index at: https://nataliazarina.github.io/learning-decks/")
    else:
        print("\nPush failed — you may need to push manually.")


if __name__ == "__main__":
    main()
