#!/usr/bin/env python3
"""Normalize simple Markdown formatting without changing prose semantics."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)


def format_file(path: Path, check: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = [line.rstrip() for line in original.splitlines()]
    formatted = "\n".join(lines).rstrip() + "\n"
    if formatted == original:
        return False
    if not check:
        path.write_text(formatted, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when formatting changes are needed")
    args = parser.parse_args()
    changed = [path for path in markdown_files() if format_file(path, args.check)]
    if changed and args.check:
        print("Formatting needed:")
        print("\n".join(str(path.relative_to(ROOT)) for path in changed))
        return 1
    print(f"Formatted {len(changed)} Markdown file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
