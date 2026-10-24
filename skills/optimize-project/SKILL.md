---
name: optimize-project
description: >
  Audits and optimizes a software project by finding dead code, unused dependencies, unnecessary files,
  complexity, and other inefficiencies, then estimating impact and validating approved changes. Use for
  project-wide optimization, cleanup, dependency reduction, or performance-oriented maintainability work.
  Never use it as permission to delete files automatically.
---

# Project Optimizer

Run a read-only optimization audit first. Preserve behavior, account for framework conventions and dynamic
loading, and ask for explicit approval before any destructive or modifying action.

## Workflow

1. Detect language, framework, build system, runtime entry points, generated files, and repository conventions.
2. Re-index or refresh project analysis when available; do not infer unused status from one search result.
3. Analyze dead code, unused dependencies/imports, duplicate configuration, oversized assets, complexity,
   and measurable performance opportunities.
4. Classify each candidate as confirmed, likely, possible, or not safe to remove. Record evidence and impact.
5. Recommend the smallest safe change set and wait for approval before modifying anything.
6. After approved changes, run the repository's formatter, linter, build, and tests. Re-measure when practical.
7. Report changed files, validation results, remaining risks, and candidates intentionally left untouched.

## Detailed guidance

Load [references/optimization-workflow.md](references/optimization-workflow.md) only when the current task
needs the full audit checklist, measurement guidance, or report template.

Do not delete code, dependencies, configuration, assets, or files automatically. Treat reflection, dynamic
imports, public APIs, generated code, migrations, and framework discovery as potentially active.
