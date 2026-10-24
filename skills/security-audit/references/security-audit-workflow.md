
# Security Audit

## Objective

Perform a **global, language-agnostic, framework-agnostic, read-only security audit** of the current repository.

The goal is to identify security weaknesses across:

- application code
- APIs
- authentication
- authorization
- business logic
- cryptography
- secrets
- data handling
- dependencies
- software supply chain
- frontend/browser security
- databases
- microservices
- containers
- Kubernetes
- Infrastructure as Code
- CI/CD
- cloud configuration when represented in the repository
- logging and monitoring
- error handling
- resilience and abuse resistance
- security architecture and trust boundaries
- mobile applications when applicable

Produce a practical, evidence-based report at:

```text
/docs/SECURITY-AUDIT.md
```

If `/docs` does not exist, create it.

The audit itself is **read-only**.

The only intended write operation is creating or updating the security report under `/docs/`.

---

# 1. Core Principles

Always follow:

```text
Discover
→ Re-index
→ Understand Architecture
→ Threat Model
→ Static Analysis
→ Tool-assisted Analysis
→ Optional Dynamic Analysis
→ Validate Evidence
→ Classify Risk
→ Recommend Remediation
→ Generate Report
```

Rules:

1. Never modify application source code during the audit.
2. Never patch vulnerabilities during the audit.
3. Never upgrade dependencies during the audit.
4. Never delete files during the audit.
5. Never rotate credentials automatically.
6. Never deploy anything.
7. Never run destructive commands.
8. Never expose secrets.
9. Never treat absence of evidence as proof that a control is missing.
10. Never claim full compliance or certification.
11. Never fabricate severity, CVSS scores, CVEs, references, or evidence.
12. When uncertain, mark the finding appropriately and ask the user when needed.
13. Distinguish static evidence from runtime evidence.
14. Prefer concrete evidence over generic security advice.
15. Do not inflate findings merely because a security control is absent.
16. Consider compensating controls.
17. Preserve confidentiality of the user's repository.

---

# 2. Standards Baseline

Use standards according to applicability.

## Primary Application Security Standard

### OWASP ASVS 5.0.0

Use OWASP ASVS 5.0.0 as the primary verification baseline for web applications and application security controls.

Reference concrete requirements when confidently applicable.

Use the actual ASVS requirement identifier when known.

Do not invent ASVS identifiers.

ASVS is a verification standard. Do not replace it with the OWASP Top 10 checklist.

---

## OWASP Top 10:2025

Use for broad web application risk classification and communication.

Current categories:

- A01:2025 Broken Access Control
- A02:2025 Security Misconfiguration
- A03:2025 Software Supply Chain Failures
- A04:2025 Cryptographic Failures
- A05:2025 Injection
- A06:2025 Insecure Design
- A07:2025 Authentication Failures
- A08:2025 Software or Data Integrity Failures
- A09:2025 Security Logging and Alerting Failures
- A10:2025 Mishandling of Exceptional Conditions

Do not claim comprehensive OWASP Top 10 coverage merely because each category was mentioned.

---

## OWASP API Security Top 10:2023

When APIs exist, assess:

- API1 Broken Object Level Authorization
- API2 Broken Authentication
- API3 Broken Object Property Level Authorization
- API4 Unrestricted Resource Consumption
- API5 Broken Function Level Authorization
- API6 Unrestricted Access to Sensitive Business Flows
- API7 Server Side Request Forgery
- API8 Security Misconfiguration
- API9 Improper Inventory Management
- API10 Unsafe Consumption of APIs

Pay particular attention to:

- BOLA/IDOR
- privilege escalation
- tenant isolation
- object/property authorization
- sensitive business flows
- SSRF
- undocumented endpoints
- deprecated endpoints
- shadow APIs
- excessive resource consumption

---

## OWASP MASVS / MASTG

If the project is:

- Android
- iOS
- Flutter mobile
- React Native
- another mobile application

adapt the audit to OWASP MASVS and relevant MASTG testing guidance.

Do not apply mobile-only controls to non-mobile projects.

---

## MITRE CWE

Use CWE for root-cause classification where appropriate.

Examples include:

- CWE-79 Cross-Site Scripting
- CWE-89 SQL Injection
- CWE-862 Missing Authorization
- CWE-863 Incorrect Authorization
- CWE-22 Path Traversal
- CWE-78 OS Command Injection
- CWE-918 SSRF
- CWE-502 Deserialization of Untrusted Data

Use the most specific supported CWE.

Do not invent a CWE mapping.

---

## CVSS v4.0

When a vulnerability has enough evidence to score it meaningfully, provide a CVSS v4.0 score and vector.

Do not fabricate a vector.

If the evidence is insufficient for reliable CVSS scoring:

```text
CVSS: Not reliably scoreable from available evidence
```

Severity and priority remain separate.

---

## NIST SSDF 1.1

Assess secure software development practices when repository evidence exists:

- protect source code
- protect build systems
- protect CI/CD credentials
- secure dependencies
- secure builds
- security testing
- release integrity
- artifact integrity
- vulnerability remediation
- secure development processes

Do not treat SSDF as a code-vulnerability checklist.

---

## NIST SP 800-115

Use as supporting guidance for technical security testing methodology when dynamic/security testing is authorized and possible.

Do not perform intrusive or destructive testing without explicit authorization.

---

# 3. Project Detection

Before judging security controls, determine:

- programming languages
- frameworks
- runtimes
- package managers
- dependency manifests
- lockfiles
- build systems
- compilers
- linters
- formatters
- type checkers
- test frameworks
- API specifications
- database technology
- cache/queue technology
- deployment model
- containerization
- orchestration
- reverse proxy
- API gateway
- cloud provider configuration
- Infrastructure as Code
- CI/CD provider
- external integrations

Do not assume the project is JavaScript.

Detect the actual ecosystem.

Examples of files to inspect when present:

```text
package.json
package-lock.json
pnpm-lock.yaml
yarn.lock
bun.lockb
bun.lock

pyproject.toml
requirements.txt
uv.lock
poetry.lock
Pipfile

go.mod
go.sum

Cargo.toml
Cargo.lock

composer.json
composer.lock

pom.xml
build.gradle
build.gradle.kts

*.csproj
*.sln

pubspec.yaml

Gemfile
mix.exs
Package.swift

Dockerfile
compose.yml
docker-compose.yml
*.yaml
*.yml

.github/**
.gitlab/**
.azure/**
```

This list is illustrative, not exhaustive.

---

# 4. Re-index the Repository

Perform a fresh repository-wide inspection before reaching conclusions.

Identify:

- source roots
- entry points
- executable binaries
- routes
- API endpoints
- controllers/handlers
- services
- repositories
- models
- authentication boundaries
- authorization boundaries
- privileged operations
- background workers
- jobs
- event handlers
- message consumers
- file processors
- upload handlers
- webhooks
- scheduled tasks
- admin interfaces
- internal interfaces
- external integrations
- configuration
- secrets
- generated code
- tests
- infrastructure

Construct a conceptual attack-surface map.

At minimum:

```text
Internet / User
      ↓
Entry Points
      ↓
Authentication
      ↓
Authorization
      ↓
Business Logic
      ↓
Data / External Systems
```

For microservices:

```text
Internet
   ↓
Gateway / Proxy
   ↓
Service A
   ├── Service B
   ├── Service C
   └── Database
```

Treat internal networks as security boundaries, not inherently trusted zones.

---

# 5. Threat Modeling

Perform a lightweight threat model before detailed findings.

Identify:

## Assets

Examples:

- credentials
- tokens
- PII
- financial data
- business records
- source code
- internal APIs
- administrative capabilities
- cryptographic keys
- infrastructure control

## Threat Actors

Consider applicable actors:

- anonymous internet attacker
- authenticated low-privilege user
- malicious tenant
- compromised account
- compromised service
- insider
- supply-chain attacker

Do not assume every actor is relevant.

## Trust Boundaries

Identify transitions such as:

```text
Browser → API
API Gateway → Service
Service → Service
Application → Database
Application → Queue
Application → Object Storage
CI/CD → Registry
Developer → Production
```

## High-Risk Attack Paths

Look for:

- authentication bypass
- privilege escalation
- tenant breakout
- object ownership bypass
- secret theft
- service-to-service lateral movement
- SSRF into internal systems
- remote code execution
- sensitive business-flow abuse
- supply-chain compromise

---

# 6. Authentication

Inspect, when applicable:

- password hashing
- password policy
- login flow
- session creation
- session invalidation
- session fixation
- session expiration
- JWT validation
- token expiration
- refresh token rotation
- refresh token reuse detection
- issuer validation
- audience validation
- signature validation
- OAuth/OIDC
- PKCE
- MFA
- account recovery
- email verification
- login throttling
- brute-force protection
- credential stuffing protection
- account enumeration
- logout
- password reset

Flag strong evidence of:

- plaintext passwords
- weak password hashing
- insecure token storage
- unsigned JWT acceptance
- algorithm confusion
- predictable session identifiers
- missing token expiration
- missing revocation where required
- weak account recovery
- authentication bypass

Do not assume JWT is secure merely because a library is used.

Trace:

```text
Token creation
→ Token storage
→ Token transmission
→ Token validation
→ Authorization decision
→ Expiration/revocation
```

---

# 7. Authorization

Treat authorization as a first-class security domain.

Inspect:

- RBAC
- ABAC
- ownership checks
- object-level authorization
- property-level authorization
- function-level authorization
- tenant isolation
- admin boundaries
- internal service permissions
- role transitions
- permission caching
- default-deny behavior

Always distinguish:

```text
Authentication ≠ Authorization
```

Look for patterns such as:

```text
GET /users/{id}
GET /orders/{id}
PUT /documents/{id}
DELETE /payments/{id}
```

Ask:

```text
Can User A access User B's resource?
Can a lower-privileged user invoke admin functionality?
Can a tenant access another tenant's data?
Can writable properties modify fields the user should not control?
```

---

# 8. API Security

For each significant API group inspect:

- authentication
- authorization
- input validation
- output filtering
- schema validation
- object ownership
- mass assignment
- pagination
- filtering
- sorting
- search
- rate limits
- request-size limits
- body-size limits
- timeout
- concurrency limits
- idempotency
- replay protection
- CORS
- security headers
- versioning
- deprecated endpoints
- undocumented endpoints
- debug endpoints
- health endpoints
- metrics endpoints
- admin endpoints

Map relevant findings to OWASP API Security Top 10.

Do not assume OpenAPI documentation represents the complete API inventory.

---

# 9. Injection and Dangerous Operations

Inspect data flow from attacker-controlled input to dangerous operations.

Relevant classes include:

- SQL injection
- NoSQL injection
- command injection
- template injection
- LDAP injection
- path traversal
- XSS
- SSRF
- unsafe deserialization
- expression-language injection
- dynamic evaluation
- code execution
- HTTP request smuggling where evidence exists
- ReDoS

Dangerous APIs may include equivalents of:

```text
eval
exec
system
shell execution
subprocess
child_process
dynamic SQL
raw queries
innerHTML
dangerouslySetInnerHTML
dynamic template evaluation
user-controlled URLs
```

Do not report a vulnerability merely because a dangerous API exists.

Trace:

```text
Untrusted Input
→ Validation
→ Transformation
→ Authorization
→ Dangerous Sink
```

Only report when evidence supports exploitability or a meaningful security weakness.

---

# 10. Business Logic and Abuse Cases

Explicitly assess business logic.

Look for:

- price manipulation
- quantity manipulation
- coupon abuse
- duplicate transactions
- replay attacks
- race conditions
- workflow bypass
- approval bypass
- privilege escalation
- transaction state tampering
- double spending
- fake account creation
- resource abuse
- sensitive business-flow automation
- missing ownership checks
- client-controlled business decisions

For critical workflows identify:

```text
Start
→ Identity
→ Authorization
→ Validation
→ State transition
→ Approval
→ Side effect
→ Completion
```

Look for ways to skip or reorder states.

---

# 11. Frontend / Browser Security

When browser-facing applications exist, inspect:

- XSS
- DOM XSS
- output encoding
- HTML sanitization
- CSP
- HSTS
- secure cookies
- HttpOnly
- SameSite
- CSRF
- CORS
- token storage
- localStorage
- sessionStorage
- URL handling
- postMessage
- iframe embedding
- clickjacking
- third-party scripts
- dependency risks
- source maps
- browser-exposed configuration
- public environment variables

Verify that server-only secrets cannot reach browser bundles.

Adapt to framework-specific public/private environment variable conventions.

---

# 12. Cryptography and Secrets

Inspect:

- hardcoded credentials
- API keys
- access tokens
- refresh tokens
- JWT secrets
- private keys
- signing keys
- encryption keys
- database credentials
- webhook secrets
- insecure `.env` handling
- secrets in logs
- weak hashes
- weak encryption
- insecure random generation
- predictable identifiers
- TLS configuration
- certificate validation

Prefer:

- modern password hashing such as Argon2id when appropriate
- cryptographically secure randomness
- authenticated encryption
- properly configured TLS
- secret management systems
- key rotation
- least-privileged credentials

Never invent custom cryptography.

Never print secret values.

If a secret is found, report:

```text
Secret detected: YES
Location: <file>:<line>
Type: <credential type>
Value: REDACTED
```

---

# 13. Database Security

Inspect:

- SQL/NoSQL injection protection
- query parameterization
- ORM/query-builder use
- database credentials
- public exposure
- network segmentation
- least-privilege DB accounts
- sensitive data storage
- encryption requirements
- tenant isolation
- access-control enforcement
- backup security
- migration safety

Do not delete or modify database objects during an audit.

Do not assume a database object is unused based solely on repository references.

---

# 14. File Upload and File Processing

If uploads exist, inspect:

- authentication
- authorization
- file size limits
- content validation
- MIME validation
- magic-byte validation
- filename normalization
- path traversal
- storage isolation
- executable content
- public exposure
- malware scanning
- archive extraction
- decompression bombs
- document/image processing
- content-disposition
- generated thumbnails/previews

Never trust file extensions alone.

---

# 15. SSRF

When server-side URL fetching exists, inspect:

- arbitrary URL fetching
- redirects
- DNS rebinding
- private IP access
- loopback
- localhost
- cloud metadata endpoints
- internal service endpoints
- URL parser discrepancies
- protocol restrictions
- allowlist enforcement

Check webhook, image proxy, import, document fetching, URL preview, and integration features.

---

# 16. Error Handling and Resilience

Inspect:

- stack trace exposure
- debug mode
- database errors
- filesystem paths
- internal service names
- credentials in errors
- framework internals
- fail-open behavior
- inconsistent authorization failures

Also inspect resilience against:

- CPU exhaustion
- memory exhaustion
- connection exhaustion
- request flooding
- queue flooding
- expensive queries
- expensive regex
- huge JSON bodies
- deep nested payloads
- pagination abuse
- repeated expensive operations
- large uploads
- concurrent request abuse

Security controls should consider both correctness and availability.

---

# 17. Logging, Auditability, and Alerting

Inspect:

- authentication events
- authorization failures
- privileged actions
- security events
- audit logs
- structured logging
- request IDs
- correlation IDs
- alerting
- error monitoring
- retention
- access to logs
- sensitive-data redaction

Flag secrets in logs:

- passwords
- access tokens
- refresh tokens
- session identifiers
- API keys
- cookies
- private data

Also check whether important security events can be investigated after an incident.

---

# 18. Security Headers, Cookies, and CORS

For browser-facing systems inspect:

```text
Content-Security-Policy
Strict-Transport-Security
X-Content-Type-Options
Referrer-Policy
Permissions-Policy
frame-ancestors
```

Check cookies:

```text
Secure
HttpOnly
SameSite
Path
Domain
Expiration
```

For CORS inspect:

- allowed origins
- credentials
- methods
- headers
- wildcard behavior
- environment differences

Flag overly broad credentialed CORS.

Do not blindly recommend a copied CSP policy. Tailor recommendations to actual application dependencies.

---

# 19. Microservices and Service-to-Service Security

Inspect:

- service authentication
- service authorization
- service identity
- mTLS when required
- TLS
- secret handling
- network segmentation
- internal endpoints
- SSRF
- timeouts
- retries
- circuit breakers
- trust boundaries
- lateral movement

Ask:

```text
If Service A is compromised,
what can Service A access?
```

Check for excessive service privileges.

---

# 20. Containers and Kubernetes

When applicable inspect:

- root containers
- privileged containers
- excessive capabilities
- host networking
- host PID/IPC
- Docker socket mounts
- writable root filesystem
- exposed ports
- secrets in images
- secrets in Compose/Kubernetes manifests
- image provenance
- mutable image tags
- outdated base images
- unnecessary packages
- resource limits
- health checks
- pod/service exposure
- RBAC
- service accounts
- security contexts
- network policies
- admission controls
- sensitive host mounts

Prefer:

- non-root execution
- minimal images
- multi-stage builds
- dropped capabilities
- `no-new-privileges`
- read-only filesystem where practical
- resource limits
- pinned or digest-pinned artifacts where practical
- image scanning
- least-privilege service accounts

Do not claim an infrastructure vulnerability without considering deployment context and compensating controls.

---

# 21. Infrastructure as Code and Cloud

When IaC or cloud configuration exists, inspect:

- IAM
- public exposure
- network rules
- firewall/security groups
- storage permissions
- service accounts
- secrets
- encryption
- key management
- logging
- monitoring
- backup configuration
- metadata-service exposure
- Kubernetes RBAC
- public endpoints
- overly broad principals
- wildcard permissions

Never make cloud changes during the audit.

---

# 22. Dependency and Software Supply Chain

Inspect:

- dependency vulnerabilities
- dependency freshness
- lockfiles
- version pinning
- transitive dependencies
- abandoned packages
- install scripts
- package registries
- dependency confusion risks
- typosquatting indicators where evidence exists
- build plugins
- GitHub/GitLab actions
- CI/CD credentials
- artifact integrity
- provenance
- SBOM support
- dependency scanning
- secret scanning

If a vulnerability is identified, report when known:

- package
- installed version
- direct/transitive
- advisory/CVE
- severity
- fixed version
- evidence
- exploitability in this application

Never state that a vulnerable dependency is exploitable solely because a CVE exists.

---

# 23. CI/CD Security

Inspect:

- workflow permissions
- token permissions
- branch protection evidence
- pull request security
- untrusted code execution
- secrets exposure
- fork handling
- artifact integrity
- deployment credentials
- environment separation
- production approval gates
- third-party actions
- mutable action references
- dependency installation
- build isolation

Pay special attention to pull-request workflows where untrusted code may access secrets.

---

# 24. Generated Code and Build Artifacts

Detect:

```text
dist/
build/
target/
coverage/
vendor/
generated/
.cache/
.tmp/
```

Do not automatically classify them as vulnerabilities or dead source code.

Determine whether they are:

- generated
- committed intentionally
- deployed
- required for builds
- ignored by version control

---

# 25. Static vs Dynamic vs Hybrid Audit

Default mode:

```text
STATIC
```

Use static repository analysis unless dynamic testing is explicitly authorized.

Supported modes:

```text
STATIC
DYNAMIC
HYBRID
```

## STATIC

Inspect:

- code
- config
- dependencies
- IaC
- container configuration
- CI/CD
- secrets
- architecture

## DYNAMIC

Only when the user explicitly authorizes it and an appropriate local/staging target is available.

Allowed examples:

- endpoint discovery
- safe authentication tests
- authorization checks using test identities
- security-header checks
- CORS checks
- non-destructive input validation checks
- safe rate-limit checks
- OpenAPI verification

Never:

- exploit production systems without explicit authorization
- destroy data
- brute-force real accounts
- use discovered credentials against external systems
- access unrelated infrastructure
- exfiltrate sensitive data

## HYBRID

Correlate source evidence with runtime evidence.

Runtime evidence is stronger than static assumptions when safely obtained.

---

# 26. Security Tooling

Use available security tooling when present and appropriate.

Potential categories:

- SAST
- dependency scanners
- secret scanners
- container scanners
- IaC scanners
- linters
- SBOM tooling
- API security testing tools
- static analyzers

Do not assume a tool exists.

Do not install arbitrary tools without user approval unless the execution environment explicitly provides them and installation is known to be safe/non-destructive.

When using tools, record:

- tool
- version when available
- command
- scope
- result
- limitations

Never treat tool output as automatically correct.

Validate important findings manually where practical.

---

# 27. False Positive Control

Before reporting a vulnerability, trace the relevant data/control path.

For data-flow findings:

```text
Input
→ Validation
→ Transformation
→ Authorization
→ Dangerous Operation
→ Output
```

For authorization findings:

```text
Identity
→ Role
→ Resource
→ Ownership
→ Permission
→ Decision
```

For supply-chain findings:

```text
Dependency
→ Build
→ Artifact
→ Deployment
→ Runtime
```

If a suspected issue is already mitigated elsewhere, do not report it as an active vulnerability.

Document the mitigating control.

---

# 28. Severity

Every finding must have exactly one severity:

| Severity | Meaning |
|---|---|
| Critical | Catastrophic or broadly exploitable impact such as RCE, authentication bypass, major secret compromise, or broad unauthorized access |
| High | Serious security impact with realistic exploitability |
| Medium | Meaningful weakness with limited scope or additional conditions |
| Low | Limited practical impact or defense-in-depth weakness |
| Informational | Observation, hardening opportunity, or non-vulnerability |

Do not inflate severity.

---

# 29. Confidence

Use a separate confidence field:

```text
Confirmed
Likely
Potential
Unverified
```

Confidence is not severity.

Example:

```text
Severity: High
Confidence: Potential
```

---

# 30. CVSS and Business Risk

Where evidence supports it, report:

```text
Severity: High
CVSS: 8.x
CVSS Version: 4.0
Business Impact: High
Priority: P1
```

Evaluate:

- exploitability
- privileges required
- attack complexity
- user interaction
- exposure
- blast radius
- confidentiality
- integrity
- availability
- sensitive data
- business impact
- compensating controls

Do not make CVSS replace business risk.

---

# 31. Priority

Use:

```text
P0 = Critical / immediate containment or remediation
P1 = High / fix before production or as soon as practical
P2 = Medium / schedule near-term
P3 = Low / hardening or normal backlog
```

Priority must not replace severity.

---

# 32. Finding Format

Each finding must use:

```markdown
## SEC-001 — <Finding Title>

- Severity: Critical | High | Medium | Low | Informational
- Confidence: Confirmed | Likely | Potential | Unverified
- CVSS: <score or Not Reliably Scoreable>
- CWE: <CWE if applicable>
- OWASP: <category if applicable>
- ASVS: <requirement if confidently known>
- Component: <frontend/backend/API/infrastructure/etc.>
- Evidence Type: Static | Dynamic | Configuration | Dependency | Runtime | Architectural | Tool
- Evidence Strength: Strong | Moderate | Weak
- Location: `path/to/file.ext:123`
- Status: Open
- Priority: P0 | P1 | P2 | P3

### Summary

<Concise explanation>

### Evidence

<Concrete evidence without exposing secrets>

### Security Impact

Explain impact to:

- Confidentiality
- Integrity
- Availability
- Authentication
- Authorization
- Data exposure
- Lateral movement
- Business operations

Only include relevant dimensions.

### Attack Scenario

Describe a realistic, non-destructive attack path at a high level.

Do not provide dangerous exploit payloads.

### Root Cause

Explain the underlying design or implementation weakness.

### Recommended Fix

Provide actionable remediation.

### Verification

Explain exactly how the fix should be validated.

### References

- <standard/reference>
```

---

# 33. Report Structure

Generate:

```text
/docs/SECURITY-AUDIT.md
```

with:

```markdown
# Security Audit Report

## 1. Executive Summary

## 2. Audit Scope

## 3. Methodology

## 4. Technology & Architecture Observed

## 5. Threat Model Summary

## 6. Attack Surface Summary

## 7. Security Posture

| Severity | Count |
|---|---:|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Informational | 0 |

## 8. Critical & High Findings

## 9. Medium Findings

## 10. Low & Informational Findings

## 11. Detailed Findings

## 12. Security Controls Already Present

## 13. Standards Coverage

| Standard | Area | Status |
|---|---|---|
| OWASP ASVS 5.0.0 | ... | Pass / Partial / Fail / N/A / Not Assessed / Unverified |
| OWASP Top 10:2025 | ... | ... |
| OWASP API Security Top 10:2023 | ... | ... |
| OWASP MASVS/MASTG | ... | ... |
| CWE | ... | ... |
| NIST SSDF 1.1 | ... | ... |

## 14. Supply Chain & CI/CD

## 15. Infrastructure / Container / IaC Findings

## 16. Business Logic & Abuse Cases

## 17. Remediation Roadmap

### P0 — Immediate
### P1 — High Priority
### P2 — Near Term
### P3 — Hardening

## 18. Security Debt

## 19. Unverified / Not Assessed Areas

## 20. Limitations

## 21. Positive Security Controls

## 22. Final Risk Summary
```

---

# 34. Standards Coverage Rules

Use only:

```text
PASS
PARTIAL
FAIL
NOT APPLICABLE
NOT ASSESSED
UNVERIFIED
```

Meaning:

- PASS = evidence supports the control
- PARTIAL = some requirements satisfied
- FAIL = evidence supports a security weakness
- NOT APPLICABLE = control does not apply
- NOT ASSESSED = outside the performed audit scope
- UNVERIFIED = relevant evidence was unavailable

Do not treat `NOT ASSESSED` as `FAIL`.

Do not treat `UNVERIFIED` as `PASS`.

---

# 35. Limitations

Always disclose limitations.

Examples:

```text
Production infrastructure was not tested.
External identity provider behavior was not verified.
Cloud IAM configuration was not available.
Runtime testing was not authorized.
Only repository-level evidence was available.
Third-party services were not assessed.
```

Do not imply that untested areas are secure.

---

# 36. Compliance Language

Never claim:

```text
OWASP compliant
ASVS certified
ISO compliant
100% secure
fully secure
no vulnerabilities
penetration test passed
```

unless that exact assertion is legitimately established by a separate authorized certification or assessment process.

Use language such as:

```text
ASVS Coverage: 62 requirements assessed
Critical Findings: 0
High Findings: 2
Unverified Areas: 8
```

---

# 37. Remediation Quality

Do not give generic recommendations such as:

```text
Improve authentication.
Enable security.
Fix authorization.
Use HTTPS.
```

Instead provide:

```text
Observed:
services/auth/jwt.go:84 validates the signature but does not visibly
enforce issuer and audience constraints.

Recommendation:
Validate issuer and audience against configured trusted values,
enforce token expiration, and reject unexpected signing algorithms.

Verification:
Add negative tests for wrong issuer, wrong audience, expired token,
and unsupported signing algorithm.
```

Recommendations must be:

- specific
- actionable
- technically realistic
- tied to evidence
- verifiable

---

# 38. Global / Adaptive Scope

This skill is global.

Adapt automatically to detected project type.

Examples:

## Web

Activate:

- ASVS
- OWASP Top 10
- browser security
- session security

## API

Activate:

- API Security Top 10
- BOLA/BFLA/property authorization
- rate limiting
- inventory management
- business flows

## Mobile

Activate:

- MASVS
- MASTG
- local storage
- mobile authentication
- platform permissions
- certificate/network security

## Backend

Activate:

- authentication
- authorization
- injection
- data protection
- service-to-service security
- resilience

## Library / SDK

Treat exported/public APIs as potentially externally consumed.

## Monorepo

Audit:

- workspace boundaries
- cross-package trust
- dependency boundaries
- CI/CD permissions
- shared infrastructure

## Containers / Kubernetes

Activate:

- container security
- image security
- RBAC
- service accounts
- network policy
- secrets
- runtime privileges

## IaC / Cloud

Activate:

- IAM
- public exposure
- network boundaries
- encryption
- secrets
- storage
- logging

Do not apply irrelevant controls.

---

# 39. Ask User When Necessary

Ask the user when:

- dynamic testing needs authorization
- production/staging target is ambiguous
- external API testing requires authorization
- discovered credentials could access real systems
- an exported API may have external consumers
- a database object may be externally used
- a security control depends on deployment infrastructure unavailable in the repository
- compensating controls cannot be determined
- a high-risk finding is ambiguous
- remediation would require changing architecture

Do not guess in high-risk situations.

---

# 40. Final Audit Behavior

At completion:

1. Create/update `/docs/SECURITY-AUDIT.md`.
2. Do not modify application code.
3. Do not expose secrets.
4. Prioritize Critical and High risks.
5. Include concrete evidence.
6. Include remediation.
7. Include verification steps.
8. Include standards mapping where supported.
9. Separate severity from confidence.
10. Separate severity from business priority.
11. Distinguish measured/runtime evidence from static assumptions.
12. Document positive controls.
13. Document unverified areas.
14. Document limitations.
15. Never claim certification or full compliance.

The goal is not to generate the largest number of findings.

The goal is to produce:

> **accurate, evidence-based, risk-prioritized, actionable security findings with clear impact, clear remediation, and explicit limitations.**
