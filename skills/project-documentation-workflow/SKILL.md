---
name: project-documentation-workflow
description: >
  Create and maintain a consistent, implementation-ready documentation set for software projects,
  including AGENTS.md, PRD.md, ARCHITECTURE.md, plan.md, TASK.md, TESTING.md, and DEPLOYMENT.md.
  Use when starting a project, documenting an existing repository, planning major features,
  refactoring, or preparing deployment. Ask focused clarification questions when important
  requirements are unknown.
---

# Project Documentation Workflow

## Purpose

Use this skill to create a practical, consistent set of project documents that helps a developer and
an agentic coding assistant understand what to build, how to build it, how to verify it, and how to deploy it.

The documents must be actionable and grounded in the user's requirements and the actual repository. Avoid
generic filler, invented requirements, duplicated content, and documentation that is more complicated than
the project needs.

## Core principles

1. **Inspect before assuming.** If a repository is available, inspect its structure, package manifests,
   configuration, source code, tests, CI/CD workflows, and existing documentation before describing the
   current system.
2. **Treat user requirements as the product source of truth.** Treat the repository as the source of truth
   for what is currently implemented. Clearly distinguish existing behavior from planned behavior.
3. **Do not invent details.** Mark unknowns as `TBD`, `Belum diputuskan`, or `Perlu konfirmasi`. Never
   fabricate endpoints, schema fields, infrastructure, credentials, performance targets, or business rules.
4. **Keep documents consistent.** Names, roles, features, architecture, commands, environment variables,
   and acceptance criteria must agree across all files.
5. **Prefer the smallest useful document set.** Create the core documents when relevant. Create optional
   documents only when their added value justifies the maintenance cost.
6. **Write for execution.** Convert broad goals into explicit requirements, milestones, checklists,
   acceptance criteria, commands, and verification steps.
7. **Respect the existing technology stack.** Do not replace frameworks, languages, libraries, or deployment
   platforms unless the user requests it or an evidenced constraint makes a change necessary. Explain
   trade-offs before proposing a major change.
8. **Make uncertainty visible.** Separate confirmed facts, assumptions, decisions, and open questions.
9. **Protect sensitive information.** Never put real secrets, API keys, passwords, tokens, private keys, or
   personal data into documentation. Use variable names and safe placeholders instead.
10. **Ask focused questions when needed.** Before finalizing documents, ask the user about missing decisions
    that materially affect requirements, architecture, scope, security, or deployment. Do not ask questions
    already answered in the conversation or repository.

## When to use this skill

Use this workflow when the user asks to:

- Create a new project or prepare a project for coding-agent implementation.
- Generate or revise `PRD.md`, `plan.md`, `TASK.md`, or other project documents.
- Analyze an existing repository and document its current architecture.
- Plan a refactor, migration, major feature, or dependency upgrade.
- Standardize instructions and quality gates for one or more coding agents.
- Prepare a repeatable deployment or testing process.

Do not automatically create every document for a small, isolated change. Match the deliverables to the
user's request and the project's complexity.

## Standard document set

### Core documents

#### 1. `AGENTS.md` — instructions for coding agents

Purpose: define the rules an agent should follow when working in the repository.

Include, as applicable:

- Project purpose and a short description of the system.
- Confirmed technology stack and important version constraints.
- Repository structure and where major responsibilities live.
- Installation, development, build, lint, test, and type-check commands verified against the repository.
- Coding conventions, naming, formatting, error handling, logging, and validation standards.
- Architecture boundaries and rules that must not be violated.
- Security rules, secret handling, and data/privacy requirements.
- Testing expectations and acceptance criteria before marking work complete.
- How to update documentation and report completed work.
- Explicit prohibitions, such as not introducing a new dependency without justification or not changing
  public APIs without approval, if appropriate.

Keep this file concise and operational. Put detailed product requirements in `PRD.md`, architecture
rationale in `ARCHITECTURE.md`, and task-level details in `TASK.md` instead of duplicating them in `AGENTS.md`.

Only document commands and conventions that are confirmed. If a command cannot be verified, label it as a
suggested command that needs validation.

#### 2. `PRD.md` — product requirements

Purpose: explain the problem, target users, desired outcomes, product scope, and observable behavior.

Recommended sections:

1. Overview and problem statement.
2. Goals and measurable success criteria.
3. Target users, stakeholders, and user roles.
4. User journeys or key workflows.
5. Functional requirements, each with a stable ID such as `FR-001`.
6. Non-functional requirements, each with an ID such as `NFR-001`.
7. Business rules and important edge cases.
8. Data ownership, privacy, and authorization requirements where relevant.
9. In-scope and explicitly out-of-scope items.
10. Acceptance criteria that can be tested.
11. Assumptions, dependencies, risks, and open questions.

Requirements must be specific enough for an agent to implement and a reviewer to verify. Avoid vague phrases
such as “make it fast,” “user-friendly,” or “secure” unless accompanied by an observable criterion or clearly
identified decision still needed.

Do not prescribe implementation details in the PRD unless they are a product constraint or a confirmed
requirement. Put implementation design in `ARCHITECTURE.md`.

#### 3. `ARCHITECTURE.md` — system design

Purpose: describe the system's components and the reasoning behind key technical choices.

Include, as applicable:

- Current state versus proposed or target state.
- System context, components, and responsibility boundaries.
- Technology stack and version constraints.
- Data flow and major request/event flows.
- Database entities and relationships at the level justified by available information.
- API boundaries and integrations.
- Authentication, authorization, tenancy, and trust boundaries.
- Caching, background jobs, file storage, and external services where relevant.
- Offline behavior and synchronization rules if the product is offline-first.
- Deployment topology and network boundaries.
- Important architecture decisions, alternatives considered, and trade-offs.
- Reliability, observability, scaling, backup, and recovery considerations when relevant.
- Known limitations and unresolved architecture decisions.

Use Mermaid diagrams when they clarify system context, sequence, data flow, or deployment. Keep diagrams
consistent with prose. Never portray an unimplemented future component as existing functionality.

#### 4. `plan.md` — implementation plan

Purpose: establish the order of work and the dependencies between milestones.

Include:

- Scope and expected end state.
- Phases or milestones in dependency order.
- Key tasks per phase and the documents or components affected.
- Prerequisites, migration considerations, and decisions required.
- Verification gates for each phase.
- Rollout, compatibility, or rollback considerations where relevant.
- Completion criteria for the overall plan.

The plan should explain the recommended sequence and why it reduces risk. Do not duplicate the complete task
checklist; link to or refer to `TASK.md` for execution tracking.

#### 5. `TASK.md` — actionable work checklist

Purpose: break the plan into small, verifiable units of work.

Use Markdown checkboxes, for example `- [ ] T-001: ...`.

For each substantial task, specify:

- Stable task ID.
- Clear action and expected result.
- Relevant requirement IDs, design sections, or dependencies.
- Expected files/components when known; do not invent paths.
- Acceptance criteria or verification method.
- Dependencies or blocking decisions.

Group tasks by milestone or subsystem. Separate implementation, testing, documentation, migration, and
deployment work where it improves clarity.

Tasks should be small enough to implement and review independently. Avoid vague checklist items such as
“finish backend” or “make everything secure.” Do not mark tasks complete unless evidence supports completion.
For an existing repository, first identify which work is already implemented and which remains outstanding.

#### 6. `TESTING.md` — verification strategy

Purpose: define how correctness, regressions, and critical behavior will be tested.

Include, as appropriate:

- Testing layers: unit, integration, API/contract, end-to-end, security, performance, and manual checks.
- Test commands verified from project scripts or configuration.
- Critical user flows and business rules to cover.
- Positive, negative, boundary, and authorization cases.
- Test data and environment requirements, without real sensitive data.
- Database migration and rollback checks where relevant.
- Offline, retry, synchronization, or concurrency tests when applicable.
- Acceptance gates and how failures should be reported.

Do not claim test coverage or successful execution unless it has been measured or run. Distinguish recommended
tests from tests that already exist.

#### 7. `DEPLOYMENT.md` — release and operations procedure

Purpose: provide a safe, repeatable way to deploy and recover the application.

Include only sections relevant to the actual target environment:

- Supported environments and deployment prerequisites.
- Build and release steps.
- Configuration and environment-variable names, with descriptions and safe example values.
- Database migration procedure and backup requirements.
- Service restart, health check, and smoke-test steps.
- File permission, ownership, and persistent-storage requirements where relevant.
- Reverse proxy, TLS, domain, tunnel, or network configuration where applicable.
- Logging, monitoring, and troubleshooting steps.
- Rollback and recovery procedure.
- Post-deployment verification checklist.

Commands must be consistent with the actual hosting environment and deployment mechanism. Clearly flag
destructive operations, downtime risk, irreversible migrations, and commands that require elevated privileges.
Never include secrets or ask a user to paste secrets into documentation.

### Optional documents

Create these only when the project needs them:

- `API_SPEC.md`: API endpoints, method, authentication, request/response schemas, validation, status codes,
  error format, pagination, rate limits, and versioning. Prefer the actual OpenAPI specification if the
  project uses one; avoid maintaining duplicate contracts without a reason.
- `UPGRADE.md`: current and target versions, rationale, compatibility analysis, incremental migration steps,
  breaking changes, test strategy, rollback constraints, and completion criteria.
- `CHANGELOG.md`: user- or operator-relevant changes by release, following an established format if the
  repository already uses one.
- `SKILL.md` or a skill directory: reusable instructions for a specialized coding workflow. Keep it separate
  from project requirements and repository-specific agent instructions.
- `SECURITY.md`, `CONTRIBUTING.md`, runbooks, ADRs, or data dictionaries: create when the project, team, or
  operational risk warrants them.

## Workflow

### Step 1 — Understand the request

Identify whether the user is documenting a new project, an existing repository, a planned feature, a refactor,
a migration, or a deployment process.

Extract what is known about:

- Product goal and intended users.
- Scope and priority.
- Technology constraints and versions.
- Existing implementation and repository state.
- Data, integrations, security, and compliance constraints.
- Target environment, operational limits, and deployment method.
- Required files, output language, and expected level of detail.

Use conversation context and available project files first. Do not ask the user to repeat information already provided.

### Step 2 — Inspect the repository, if available

Before documenting an existing system, inspect the relevant files. Start with repository structure, manifests,
scripts, configuration, migrations, routes/controllers/handlers, tests, CI workflows, and existing docs.

Record findings in three categories:

- **Confirmed:** directly supported by source files, configuration, tests, or user statements.
- **Inferred:** strongly suggested by available evidence but not explicitly confirmed.
- **Unknown:** not established by the available evidence.

Do not silently turn inferred or unknown details into facts. If repository access is unavailable, state that
documents are based on the user's description and identify what must be verified against the codebase.

### Step 3 — Identify gaps and ask questions

Before writing definitive architecture, task, testing, or deployment instructions, identify missing information that
would materially change the result.

Ask a concise set of prioritized questions in one message when practical. Focus on decisions such as:

1. The target users, primary workflows, and must-have features.
2. The required stack, version constraints, and technologies that must not change.
3. The source of truth for existing behavior and whether the request is greenfield or a modification.
4. Authentication, permissions, tenancy, sensitive data, and important business rules.
5. Deployment target, domain/network assumptions, database, storage, backups, and operational ownership.
6. Required deliverables, language, and preferred level of detail.

Ask only questions relevant to the current scope. Explain briefly why a question matters when the answer changes
architecture, cost, risk, or scope. Offer sensible options where that makes answering easier, but do not force a
multiple-choice form when a simple question is sufficient.

If the task can proceed safely with a reasonable default, record the default as an assumption and continue rather
than blocking progress. If the missing decision is high-impact or could cause destructive implementation, ask before
making that decision.

### Step 4 — Establish scope and decisions

Create a compact scope summary before generating the full documents:

- Confirmed goals.
- In scope and out of scope.
- Fixed constraints.
- Assumptions and unresolved questions.
- Deliverables to generate.

Resolve conflicting requirements where possible. If a conflict cannot be resolved without user input, highlight it
explicitly instead of choosing silently.

### Step 5 — Draft documents in dependency order

Use this order so later documents can refer to earlier decisions:

1. `PRD.md` — what and why.
2. `ARCHITECTURE.md` — how the system should work technically.
3. `plan.md` — the implementation sequence.
4. `TASK.md` — trackable execution items.
5. `TESTING.md` — proof of correctness.
6. `DEPLOYMENT.md` — release and recovery procedure.
7. `AGENTS.md` — concise, repo-wide instructions referencing the other documents.
8. Optional documents only when needed.

The order is a drafting aid, not a requirement to overwrite existing documents in that order. Preserve established
repository conventions and cross-link related material.

### Step 6 — Cross-check consistency

Validate that:

- Every important PRD requirement is reflected in the design and/or implementation tasks.
- Task acceptance criteria are testable and trace back to requirements where practical.
- Architecture choices comply with user constraints.
- APIs, roles, data entities, and terminology use the same names everywhere.
- Testing covers critical functional and non-functional requirements.
- Deployment instructions match the actual stack and target environment.
- Commands and file paths are verified or explicitly marked as unverified.
- No future-state feature is described as already implemented.
- No credentials, production data, or secret values are included.
- Open questions and assumptions are visible and not contradicted elsewhere.

### Step 7 — Review for usability

Before delivering, check that each file is:

- Written in the requested language and at an appropriate technical level.
- Easy to scan with headings, tables, checklists, and diagrams only where useful.
- Specific enough for a coding agent to act without making avoidable assumptions.
- Free of duplicate sections that belong in another document.
- Consistent with existing naming and file conventions.
- Clear about what is confirmed, proposed, pending, or completed.

### Step 8 — Deliver and explain

Provide a short summary of files created or updated and what each one is for. Include any major assumptions,
unresolved decisions, and verification limitations. If files are created, provide their actual paths or links where
supported.

Do not claim that code was implemented, tests were run, or deployment was verified merely because the documentation
describes those actions.

## Quality standards for agentic implementation

- Give every meaningful requirement and task a stable ID when traceability helps.
- Express acceptance criteria as observable outcomes, not subjective impressions.
- Prefer explicit examples and actual commands over abstract advice.
- Include negative cases, authorization checks, and failure handling when relevant.
- Preserve backward compatibility unless a breaking change is approved.
- Keep changes incremental and reviewable.
- Define migrations, backups, and rollback limitations before production-impacting work.
- Ask for confirmation before destructive actions, production data changes, or major scope/stack changes.
- Do not use documentation to hide unresolved product or engineering decisions.

## Recommended cross-reference convention

Use relative Markdown links when the target document exists, for example:

- `PRD.md` for requirements.
- `ARCHITECTURE.md` for implementation design.
- `plan.md` for sequencing.
- `TASK.md` for execution tracking.
- `TESTING.md` for verification.
- `DEPLOYMENT.md` for release and recovery.

Do not create broken links to files that are not being delivered. If a referenced document is intentionally omitted,
explain where its relevant information lives.

## Final checklist

Before considering the documentation set ready, verify:

- [ ] User goals and constraints are captured accurately.
- [ ] Repository facts have been inspected or clearly marked as unverified.
- [ ] Assumptions, unknowns, and decisions needing input are visible.
- [ ] Core documents fit the project's complexity and requested scope.
- [ ] Requirements connect to tasks and verification steps.
- [ ] The architecture respects the chosen stack and deployment constraints.
- [ ] Commands, paths, versions, and environment names are evidence-based or labeled for validation.
- [ ] Security, permissions, secrets, data handling, failure cases, and rollback are covered where relevant.
- [ ] Documents are consistent and cross-links work.
- [ ] The user receives a brief summary of deliverables and outstanding decisions.

## Ask the user questions to improve accuracy

At the end of the documentation-planning process, ask the user focused clarification questions whenever the answers
could improve correctness or prevent a wrong assumption. Use prior conversation and repository evidence first, and do
not repeat questions that have already been answered.

Prioritize questions about the goal and scope, users and primary workflows, technology constraints, business rules,
security and data, deployment target, and acceptance criteria. Ask only relevant questions, combine related questions
in one message, and briefly explain why the answers are needed. If unknown information is not critical, use a
reasonable assumption, mark it in the document, and continue. Never invent answers.
