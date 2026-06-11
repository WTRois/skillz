---
name: pr-writer
description: >
  Reads git diff (staged/unstaged changes or branch comparisons) and generates:
  (1) a concise conventional commit message and (2) a structured, comprehensive Pull Request (PR) description.
  Ready to copy-paste directly to GitHub, GitLab, Bitbucket, or ADO.
  Trigger this skill when the user asks: "write a PR description", "generate a commit message",
  "write commit description", "create a PR from diff", "pr-writer", "explain my changes",
  or before pushing/merging changes.
  ALWAYS invoke this skill when a git diff is present or when a change-description documentation is requested.
---

# PR Writer

Analyzes git diff structures to generate standard Conventional Commit messages and structured PR descriptions.

---

## Workflow Guide

Follow these three phases sequentially to ensure high-quality documentation.

---

### Phase 1 — Read & Analyze Diff

Execute read-only git queries to obtain the diff content and the current branch name.
* **CRITICAL ZED RULE**: Always append `--no-pager` immediately after Git CLI command calls (e.g., `git --no-pager diff`) to prevent terminal sessions from hanging / blocking awaiting user interactive page navigation.

```bash
# Get the current branch name
git --no-pager branch --show-current

# Get staged changes (ready to commit)
git --no-pager diff --staged

# Get unstaged changes (current working copy modifications)
git --no-pager diff

# Base comparison relative to target branch (e.g., main)
git --no-pager diff main...HEAD

# Summarize file changes and status
git --no-pager diff --staged --stat
git --no-pager log --oneline -n 10
```

Extract the following information from the output diff:

**A. Modified File Inventory**
- Locate all modified, added, or deleted system files.
- Group mutated files by system module/domain (e.g., auth, database, UI components, configs, core business models, tests, pipeline).

**B. Classification of Changes per File**
- `feat` — new feature or runtime logic (e.g., fresh function, api endpoint, ui component).
- `fix` — bug correction or fixing unwanted logic behavior.
- `refactor` — code restructuring without altering external functionality.
- `perf` — performance/speed optimization.
- `style` — code format style tweaks, linting, variable renaming, no code operations changed.
- `test` — adding or modifying unit tests or integration tests.
- `docs` — comments, README, documentation files changes.
- `chore` — dependency upgrades, tools, tooling configurations, build systems, CI/CD scripts.
- `db` — schema modifications, raw migrations (use this specifically if database changes are detected).
- `revert` — rolling back previous commits.

**C. System Impacts**
- Are there breaking changes? (API contract alterations, DB schema removals, table changes, new mandatory env parameters)
- Are there new dependencies or third-party package additions?
- Are there manual steps needed before/after deployment (e.g., database seed, config sync)?

**D. Scope Definition**
Derive the target scope representing the area altered:
*Examples: auth, api, db, ci, model, checkout, docker, gateway.*

---

## Phase 2 — Conventional Commit Matching

Based on your structural diff summary compile:

1. **Primary Type**: Select exactly ONE dominant change type from Phase 1.
2. **Scope**: Keep lowercase, 1–2 words representing the modified domain.
3. **Breaking Change Marker**: Append `!` after the scope if system-wide contracts break.
4. **Summary**: A single imperative sentence (under 72 chars, no trailing period).

**Conventional Commit Format:**
```
<type>(<scope>): <description>

[!] If breaking change: <type>(<scope>)!: <description>
```

**Quality Commit Examples (Check list):**
- `feat(auth): add JWT refresh token endpoint` (Correct)
- `fix(payment): handle timeout on QRIS callback` (Correct)
- `refactor(user): extract validation logic to service class` (Correct)
- `chore(docker): update base image to alpine 3.20` (Correct)
- `db(schema): add index on orders.created_at` (Correct)

**Drafts to AVOID:**
- `update files` (Too vague)
- `fix bug` (Uninformative)
- `feat: added new feature` (Past tense usage, generic scope)
- `WIP` (Fails standard audit conventions)

---

## Phase 3 — Output Generation

Provide two core formats in a single chat layout response:

### Output 1: Commit Message

For localized commits altering a single module domain:
```
feat(auth): add email verification on registration
```

For broader changes altering multiple linked modules, provide a descriptive body listing sub-bullets:
```
feat(auth): add email verification on registration

- Add POST /auth/verify-email endpoint
- Send verification email via SendGrid on register
- Expire token after 24 hours
- Add resend verification route
```

For commits breaking code compatibility, format with a explicit `BREAKING CHANGE:` footer text block:
```
feat(api)!: change user ID from integer to UUID

BREAKING CHANGE: all endpoints using user ID now expect UUID format.
Run migration `20240611_migrate_user_id_to_uuid.sql` before deploying.
```

---

### Output 2: Pull Request (PR) Description

Generate the PR markdown documentation using the matching structure below. Remove empty fields or unused blocks.
- **Language Alignment**: Draft this documentation matching the user's interaction language (e.g. write in Indonesian if prompted in Indonesian, write in English if prompted in English).

```markdown
## 📝 Summary

[Provide a brief 1-3 sentences summary. Focus on why the modifications are implemented and what business/technical problem it resolves.]

## 🔄 Changes

[Deliver descriptive lists of the principal system updates, aggregated by feature context or module scope]

### [Service Scope 1 - e.g., Authentication]
- [implemented change 1]
- [implemented change 2]

### [Service Scope 2 - e.g., Database Migrations]
- [implemented change 1]

## 🗄️ Database Changes

> Omit this section if no database/migration files were altered.

- [ ] Migration script file: `[migration_filename.ext]`
- [ ] Rollback validation plan prepared: `[Yes/No]`
- [ ] Historical data backfill required: `[Yes/No / Description details]`

## ⚠️ Breaking Changes

> Omit this section if no compatibility breaks exist.

- [State explicit change points that break backwards compatibility]
- [Indicate deployment or manual intervention steps required by developers/reviewers]
- [Updated API contracts or system properties]

## 🧪 Testing Summary

- [ ] Unit tests added / updated
- [ ] Manual verification conducted
- [ ] [Reviewer testing guidelines steps if custom actions are needed]

## 📋 Quality Checklist

- [ ] Self-review completed locally
- [ ] Print statements / debug assertions removed
- [ ] Environmental options updated in configuration blueprints
- [ ] Local migrations executed against developer DB instances
- [ ] Secrets and authentication credentials excluded from diffs

## 🔗 References & Relations

> Omit this section if there are no tracking issues.

- Closes #[issue_number]
- Related to #[issue_number]
- [Design blueprints links, Jira tickets links, Notion references]
```

---

## Phase 4 — Next Action Prompt (Interactive Git Flow)

After presenting Output 1 (Commit Message) and Output 2 (PR Description), the agent MUST explicitly ask the user in their preferred language if they want to automate the next steps:
1. Ask if they want to commit the staged changes automatically using the generated commit message (`GIT_EDITOR=true git commit -m "<Commit Message>"`).
2. Ask if they want to push those committed changes to the remote branch (`git push origin <current_branch_name>`).

*Interactive question example at the end of the response:*
> "Would you like me to commit these changes and push them to the remote on branch `{branch_name}`?"

**CRITICAL RULE**: Do not execute the commit or push commands automatically. Always wait for the user to confirm "yes" or explicitly request it first.

---

## Production Rules

- **Naming Conventions**: Keep commit scopes to lowercase, use imperative present-tense labels.
- **Empty Section Cleanup**: Ensure you delete unused code block sections in the PR template instead of prefixing "N/A" or "None".
- **Database Safety Check**: If modifications are in database modules, verify that matching migration files exists under directories.
- **Diff Capacity**: If the diff size is extremely massive (> 50 changed files), suggest splitting the PR scope into smaller, logical sub-branches to ease review difficulty.
- **No Translation Mix**: Do not mix languages (e.g., half English, half Indonesian). Keep the document cohesive.

---

## Quality Checklist

Verify these constraints before dispatching the final message:
- [ ] Commit subject string length conforms to strict 72-character limits.
- [ ] Types are correctly assigned aligning with Conventional Commit standards.
- [ ] Critical breaking tags ($type! or footer labels) are present if breaking edits are identified.
- [ ] Empty template blocks are omitted.
- [ ] Explicitly asked the user for permission to commit/push to the current remote branch.
