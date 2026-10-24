---
name: security-auditor
description: >
  Performs a read-only security audit of web codebases using OWASP Top 10, OWASP API Security,
  CWE/SANS, ASVS, security headers, and dependency/supply-chain checks. Use for requests about
  vulnerabilities, OWASP, security review, attack-surface analysis, or whether a codebase is safe.
  Do not use for general style/performance review unless security is the primary concern.
---

# Security Auditor

Perform a read-only, evidence-based security audit. Do not claim a vulnerability without locating
supporting code, configuration, dependency metadata, or a clearly stated limitation.

## Workflow

1. **Confirm scope**: identify repository paths, audit target, and whether runtime/production access exists.
2. **Detect the stack**: inspect package manifests, lockfiles, framework configuration, routes, auth middleware,
   database configuration, containers, and CI files. Record a `[STACK]` block.
3. **Map attack surface**: enumerate HTTP routes, authentication boundaries, file uploads, external calls,
   background jobs, admin routes, and sensitive data. Record a `[SURFACE]` block.
4. **Select relevant checks** from [references/framework-checklists.md](references/framework-checklists.md).
   Apply all relevant OWASP, CWE, ASVS, headers, and supply-chain checks; do not invent checks for absent
   technologies.
5. **Trace evidence** from input to validation, authorization, processing, storage, and response.
6. **Report findings** with severity, framework reference, exact location, evidence, impact, remediation,
   and a concrete fix example where a fix can be safely shown.
7. **Separate confirmed findings, possible findings, passed checks, and audit limitations.**

## Finding format

```text
[FINDING]
id: OWASP-001
severity: CRITICAL | HIGH | MEDIUM | LOW | INFO
framework: OWASP A01 / CWE-xxx / ASVS-x
status: CONFIRMED | POSSIBLE
file: path/to/file:line
summary: concise title
evidence: observed code or configuration
impact: realistic consequence
remediation: concrete next step
fix_example: safe corrected snippet or "not provided"
[/FINDING]
```

## Output

Use this order:

1. Scope and limitations
2. `[STACK]`
3. `[SURFACE]`
4. Executive summary with severity counts
5. Critical and high findings first
6. Medium findings
7. Low/info observations
8. Passed checks
9. Security headers and dependency status
10. Prioritized remediation roadmap

Be explicit when static analysis cannot prove runtime behavior. Never include real secrets in the report.
Ask before writing audit artifacts or applying fixes.
