# Platform setup

The canonical format is the directory-based Agent Skills format. Host adapters are intentionally
kept separate from skill instructions so the same skill remains portable.

## Claude Code

Use the repository as a plugin marketplace:

```text
/plugin marketplace add WTRois/skillz
/plugin install example-skills@skillz
```

Or copy one skill directory into the host's configured skills directory.

## Zed and other Agent Skills hosts

Copy the complete directory, including `SKILL.md` and any `references/` directory:

```bash
cp -R skills/security-auditor ~/.agents/skills/security-auditor
```

Do not copy the Markdown file to a different filename. Hosts discover the required `SKILL.md` path.

## Cursor, GitHub Copilot, and project instruction files

These hosts use different instruction mechanisms and may not discover Agent Skills automatically. Keep
the skill directory as the source of truth and link or paste only the relevant skill into the host's
project instruction file. Do not concatenate every skill by default: that defeats progressive disclosure
and increases instruction conflicts.

When adapting a skill, preserve its scope, trigger boundary, and confirmation rules.
