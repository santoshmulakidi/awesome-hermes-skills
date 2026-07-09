#!/usr/bin/env python3
"""OpenClaw Skill to Hermes Skill Converter"""
import sys, os, re
from pathlib import Path

def parse_skill(content):
    if not content.startswith("---"):
        return None, content
    end = content.find("---", 3)
    if end == -1:
        return None, content
    return content[3:end], content[end+3:].strip()

def convert(input_path, output_dir):
    p = Path(input_path)
    if not p.exists():
        print(f"Not found: {p}")
        return False
    content = p.read_text(encoding="utf-8")
    fm_text, body = parse_skill(content)
    if fm_text is None:
        print(f"No frontmatter: {p}")
        return False
    # Simple YAML parse
    lines = fm_text.strip().split("\n")
    name = "unknown"
    desc = ""
    for line in lines:
        if line.startswith("name:"):
            name = line.split(":",1)[1].strip()
        elif line.startswith("description:"):
            desc = line.split(":",1)[1].strip()
    
    # Body replacements
    body = body.replace("~/.openclaw", "~/AppData/Local/hermes")
    body = body.replace("openclaw skills", "hermes skills")
    body = body.replace("ClawHub", "Hermes Registry")
    body = body.replace("npx skills add", "hermes skills install")
    
    skill_dir = Path(output_dir) / name.lower().replace(" ","-")
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    out = f"---\nname: {name}\ndescription: {desc[:1024]}\ntrigger: Use when {desc.lower().rstrip('.')}\n---\n\n{body}"
    (skill_dir / "SKILL.md").write_text(out, encoding="utf-8")
    print(f"Converted: {name}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert.py <input.md> <output-dir>")
        print("       python convert.py --batch <input-dir> <output-dir>")
        sys.exit(1)
    if sys.argv[1] == "--batch":
        count = 0
        for f in Path(sys.argv[2]).rglob("SKILL.md"):
            if convert(f, sys.argv[3]):
                count += 1
        print(f"Batch done: {count} skills")
    else:
        convert(sys.argv[1], sys.argv[2])
