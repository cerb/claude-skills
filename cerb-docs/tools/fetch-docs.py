#!/usr/bin/env python3
"""
Fetch Cerb docs from https://cerb.ai/search.jsonl and write each page as a
Markdown file under cerb-docs/references/ using the URL path as the filename.

Usage:
  python3 fetch-docs.py [--input FILE] [--output DIR] [--clean]

  --input FILE   Read from a local JSONL file instead of fetching live
  --output DIR   Write files to DIR (default: ../references/ relative to script)
  --clean        Remove all files in output dir before writing
"""

import json
import os
import ssl
import sys
import urllib.request
from pathlib import Path

LIVE_URL = "https://cerb.ai/search.jsonl"

SCRIPT_DIR = Path(__file__).parent
DEFAULT_OUTPUT = SCRIPT_DIR.parent / "references"


def url_to_path(url: str) -> Path:
    """Convert a cerb.ai URL to a relative file path."""
    # Strip scheme + host
    path = url.replace("https://cerb.ai/", "").rstrip("/")
    if not path:
        path = "index"
    return Path(path + ".md")


def make_frontmatter(record: dict) -> str:
    tags = record.get("tags") or []
    tags_str = ", ".join(f'"{t}"' for t in tags)
    lines = [
        "---",
        f'id: "{record["id"]}"',
        f'title: "{record["title"].replace(chr(34), chr(39))}"',
        f'url: "{record["url"]}"',
        f'summary: "{record.get("summary", "").replace(chr(34), chr(39))}"',
        f"tags: [{tags_str}]",
        "---",
        "",
    ]
    return "\n".join(lines)


def write_file(out_dir: Path, record: dict) -> Path:
    rel = url_to_path(record["url"])
    dest = out_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    content = record.get("content", "")
    dest.write_text(make_frontmatter(record) + content, encoding="utf-8")
    return rel


def make_ssl_context() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    # macOS python.org builds don't use the system keychain; try common cert paths
    for cafile in ("/etc/ssl/cert.pem", "/usr/local/etc/openssl/cert.pem"):
        if os.path.exists(cafile):
            ctx.load_verify_locations(cafile)
            return ctx
    return ctx


def load_records(input_file: str | None) -> list[dict]:
    if input_file:
        with open(input_file, encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]
    print(f"Fetching {LIVE_URL} ...", flush=True)
    with urllib.request.urlopen(LIVE_URL, context=make_ssl_context()) as resp:
        data = resp.read().decode("utf-8")
    return [json.loads(line) for line in data.splitlines() if line.strip()]


def clean_dir(out_dir: Path):
    if not out_dir.exists():
        return
    for p in out_dir.rglob("*"):
        if p.is_file():
            p.unlink()
    # Remove empty dirs bottom-up
    for p in sorted(out_dir.rglob("*"), reverse=True):
        if p.is_dir():
            try:
                p.rmdir()
            except OSError:
                pass


def build_tree(out_dir: Path) -> str:
    """Return a compact directory-only tree string."""
    dirs = set()
    for p in out_dir.rglob("*.md"):
        rel = p.relative_to(out_dir)
        for parent in rel.parents:
            if str(parent) != ".":
                dirs.add(parent)

    lines = ["references/"]
    for d in sorted(dirs):
        depth = len(d.parts)
        indent = "  " * depth
        lines.append(f"{indent}{d.name}/")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    input_file = None
    out_dir = DEFAULT_OUTPUT
    clean = False

    i = 0
    while i < len(args):
        if args[i] == "--input" and i + 1 < len(args):
            input_file = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            out_dir = Path(args[i + 1])
            i += 2
        elif args[i] == "--clean":
            clean = True
            i += 1
        else:
            print(f"Unknown argument: {args[i]}", file=sys.stderr)
            sys.exit(1)

    if clean:
        print(f"Cleaning {out_dir} ...", flush=True)
        clean_dir(out_dir)

    out_dir.mkdir(parents=True, exist_ok=True)
    records = load_records(input_file)
    print(f"Writing {len(records)} docs to {out_dir} ...", flush=True)

    written = []
    for record in records:
        rel = write_file(out_dir, record)
        written.append(rel)

    print(f"Done. {len(written)} files written.")
    print()
    print(build_tree(out_dir))


if __name__ == "__main__":
    main()
