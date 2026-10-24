#!/usr/bin/env python3
"""Dependency-free validation for this Agent Skills repository."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED = {"name", "description"}


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    values: dict[str, str] = {}
    lines = text[4:end].splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            # Nested optional metadata is not needed for validation.
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"invalid frontmatter line: {line}")
        key = key.strip()
        value = value.strip().strip(" \\\"'")
        if value in {">", "|"}:
            continuation: list[str] = []
            while index < len(lines) and (lines[index].startswith((" ", "\t")) or not lines[index].strip()):
                continuation.append(lines[index].strip())
                index += 1
            value = " ".join(item for item in continuation if item)
        values[key] = value
    return values, text[end + 6 :]


def markdown_links(body: str) -> list[str]:
    """Return links from prose, excluding fenced code examples."""
    prose = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    return re.findall(r"\]\(([^)]+)\)", prose)


def validate() -> list[str]:
    errors: list[str] = []
    if not SKILLS.is_dir():
        return ["missing skills directory"]
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("no skill directories found")
    catalog = ROOT / ".claude-plugin" / "marketplace.json"
    if catalog.exists():
        try:
            data = json.loads(catalog.read_text(encoding="utf-8"))
            listed = {
                item.removeprefix("./skills/")
                for plugin in data.get("plugins", [])
                for item in plugin.get("skills", [])
            }
            actual = {path.name for path in skill_dirs}
            errors.extend(f"marketplace missing skill: {name}" for name in sorted(actual - listed))
            errors.extend(f"marketplace references unknown skill: {name}" for name in sorted(listed - actual))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid marketplace.json: {exc}")
    for skill_dir in skill_dirs:
        path = skill_dir / "SKILL.md"
        if not path.is_file():
            errors.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
            continue
        try:
            metadata, body = frontmatter(path)
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        missing = REQUIRED - metadata.keys()
        errors.extend(f"{path.relative_to(ROOT)}: missing frontmatter field {key}" for key in sorted(missing))
        name = metadata.get("name", "")
        if name != skill_dir.name:
            errors.append(f"{path.relative_to(ROOT)}: name {name!r} does not match directory {skill_dir.name!r}")
        if not NAME_RE.fullmatch(name):
            errors.append(f"{path.relative_to(ROOT)}: invalid skill name {name!r}")
        description = metadata.get("description", "")
        if not 1 <= len(description) <= 1024:
            errors.append(f"{path.relative_to(ROOT)}: description must be 1-1024 characters")
        if len(body.splitlines()) > 500:
            errors.append(f"{path.relative_to(ROOT)}: body is over 500 lines; move detail to references/")
        for reference in markdown_links(body):
            if reference.startswith(("http://", "https://", "#")):
                continue
            target = (path.parent / reference).resolve()
            if not target.is_file() or ROOT not in target.parents:
                errors.append(f"{path.relative_to(ROOT)}: broken local reference {reference}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="print only failures")
    args = parser.parse_args()
    errors = validate()
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    if not args.quiet:
        print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
