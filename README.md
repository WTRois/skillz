# Skillz

Portable Agent Skills for software development workflows. Each skill follows the Agent Skills
convention: one directory, one `SKILL.md`, optional references, scripts, and assets.

## Repository layout

```text
skillz/
├── skills/<skill-name>/SKILL.md
├── skills/<skill-name>/references/   # optional, loaded only when needed
├── evals/                             # prompt-based regression cases
├── scripts/                           # dependency-free repository checks
├── docs/                              # host-specific installation notes
└── .claude-plugin/marketplace.json    # Claude Code plugin catalog
```

## Included skills

| Skill | Use for |
|---|---|
| `api-designer` | REST API contracts before implementation |
| `code-reviewer` | General bug, performance, maintainability, and convention review |
| `component-generator` | Typed, accessible UI component design |
| `db-schema-designer` | Relational schema, ERD, migration, and index design |
| `full-project-analyzer` | Codebase architecture and documentation analysis |
| `optimize-laravel-inertia-vue` | Laravel + Inertia.js + Vue 3 + TypeScript work |
| `optimize-project` | Project-wide cleanup and optimization audit |
| `planmate` | Structured planning, execution, and verification for complex work |
| `pr-writer` | Commit messages and pull request descriptions from diffs |
| `security-audit` | Comprehensive read-only security audits across the stack |
| `security-auditor` | Focused OWASP and supply-chain security audits |

## Installation

### Agent Skills-compatible hosts

Copy a skill directory as-is. Do not flatten it or rename `SKILL.md`:

```bash
cp -R skills/<skill-name> ~/.agents/skills/<skill-name>
```

For all skills:

```bash
for skill in skills/*; do
  [ -d "$skill" ] || continue
  cp -R "$skill" "$HOME/.agents/skills/"
done
```

See [docs/platform-setup.md](docs/platform-setup.md) for host-specific notes.

### Claude Code plugin

Register the repository as a marketplace, then install `example-skills` or individual skills:

```text
/plugin marketplace add WTRois/skillz
/plugin install example-skills@skillz
```

The catalog is defined in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json).

## Development and validation

This repository intentionally has no runtime dependency. Run the complete check suite with:

```bash
make format
make lint
make build
make test
```

The checks use Python's standard library only. `format` normalizes Markdown whitespace; `lint` checks
frontmatter, naming, references, and repository metadata; `build` performs the same validation as a
consumer loading the skills; `test` runs regression checks for structure and trigger boundaries.

Run the validator directly when debugging:

```bash
python3 scripts/validate_repo.py --help
```

## Design rules

- Keep each `SKILL.md` focused and under 500 lines where practical.
- Put detailed, domain-specific material in `references/` and link it from the skill.
- Keep `description` specific about both capability and trigger context.
- Avoid overlapping trigger claims; specialist skills should defer to one another explicitly.
- Never write files, commit, push, or apply fixes without explicit user confirmation.
- Keep reports evidence-based and state static-analysis limitations.
- Add or update an eval in `evals/` when changing behavior or trigger boundaries.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Anthropic skills repository](https://github.com/anthropics/skills)
