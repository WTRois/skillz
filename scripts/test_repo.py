#!/usr/bin/env python3
"""Small regression suite for structure and trigger boundaries."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_repo  # noqa: E402


def body_for(name: str) -> str:
    return (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    if validate_repo.validate():
        failures.append("repository validator returned errors")
    expected = {
        "security-auditor": "references/framework-checklists.md",
        "optimize-laravel-inertia-vue": "references/laravel-inertia-vue-guidance.md",
    }
    for name, reference in expected.items():
        if reference not in body_for(name):
            failures.append(f"{name} does not link its detailed reference")
    if "security-auditor" not in body_for("code-reviewer"):
        failures.append("code-reviewer does not defer dedicated security audits")
    if "optimize-laravel-inertia-vue" not in body_for("code-reviewer"):
        failures.append("code-reviewer does not defer framework-specific review")
    if "Ask before writing audit artifacts or applying fixes" not in body_for("security-auditor"):
        failures.append("security-auditor confirmation guardrail is missing")
    if failures:
        print("Tests failed:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("Tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
