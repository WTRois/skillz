---
name: security-audit
description: >
  Performs a read-only, evidence-based security audit of any software project across application code,
  APIs, authentication, dependencies, supply chain, containers, cloud/IaC, and CI/CD when represented in
  the repository. Use for comprehensive security audits, OWASP reviews, vulnerability assessment, or
  penetration-test preparation. Never modify application code or infrastructure during an audit.
---

# Security Audit

Use a source-first, evidence-based workflow. Loading this skill does not authorize exhaustive auditing,
file creation, exploitation, or remediation. Choose the smallest operating mode that answers the request.

## Operating modes

- **Guidance**: answer a security question or explain a control; inspect only relevant material.
- **Focused review**: investigate a named component, endpoint, finding, or trust boundary.
- **Full audit**: use only when the user explicitly requests a comprehensive/end-to-end audit or report.

## Workflow

1. Confirm scope, assets, trust boundaries, available runtime access, and reporting requirements.
2. Detect stack, deployment model, dependencies, secrets exposure, entry points, auth boundaries, and data flows.
3. Load the relevant sections of [references/security-audit-workflow.md](references/security-audit-workflow.md).
4. Trace each candidate to source evidence and distinguish confirmed, possible, and not-applicable findings.
5. Prioritize with realistic impact and exploitability; avoid unsupported severity claims.
6. Report evidence, affected principal/resource, impact, location, remediation, references, passed checks,
   limitations, and recommended follow-up validation.

## Safety rules

- Read-only by default; never modify application code or infrastructure.
- Do not exploit production systems or expose secrets.
- Ask before writing a report artifact, running invasive checks, or accessing external systems.
- A missing control is not automatically a vulnerability without a concrete affected trust boundary or outcome.
