---
name: code-reviewer
description: >
  Reviews code after new features are written — scanning for bugs, security vulnerabilities,
  performance bottlenecks, and convention violations. Generates a structured review report
  with severity ratings, exact file locations, clear problem explanations, and concrete
  fix suggestions including corrected code samples.
  Trigger this skill when the user asks: "review this code", "code review", "check for bugs",
  "any issues?", "security audit", "review new feature", "check performance",
  "is this code safe?", "code-reviewer", or after finishing a feature and wanting validation
  before push/PR.
  ALWAYS invoke this skill for any review, audit, or code quality validation request.
---

# Code Reviewer

Systematically analyzes code across four dimensions — Bug, Security, Performance, and Convention —
then produces an actionable, structured review report with concrete fix suggestions.

---

## Workflow

Follow these phases sequentially. Each dimension is inspected independently to ensure nothing is missed.

---

### Phase 1 — Code Orientation

**Objective:** Understand context before searching for problems.

1. Read the entire codebase or file(s) under review from top to bottom once.
2. Identify:
   - **Language & framework** in use.
   - **Purpose** — what does this feature do?
   - **Entry point** — where does execution begin?
   - **External dependencies** — DB, external APIs, file system, cache, message queues?
   - **Sensitive data** — is there user input, auth tokens, passwords, or PII?
3. Record findings as a `[CONTEXT]` block before beginning the review.

---

### Phase 2 — Dimensional Review

Inspect the code thoroughly across each of the following dimensions.
For every issue found, record:
- **Location**: file name + line number (when available).
- **Severity**: `critical` / `high` / `medium` / `low` / `info`.
- **Description**: why this is a problem and what its impact is.
- **Suggestion**: concrete corrected code.

---

#### Dimension 1 — 🐛 Bug

Search for conditions that will cause the code to fail or behave incorrectly.

**Checklist:**

*Logic errors*
- [ ] Inverted boolean conditions (`>` should be `>=`, `&&` should be `||`)
- [ ] Off-by-one errors in loops or array/slice indexing
- [ ] Unchecked return values
- [ ] Missing or misplaced early returns

*Null / undefined / zero value*
- [ ] Property access without null check (`user.name` without verifying `user`)
- [ ] Array access without bounds check
- [ ] Division by zero
- [ ] Empty string treated as valid input
- [ ] Pointer dereference without nil check (Go, C, Rust unsafe)

*Concurrency*
- [ ] Race condition on shared state
- [ ] Goroutine/thread leak (no timeout or cancellation)
- [ ] Deadlock potential (nested locks, lock without unlock)
- [ ] Context not propagated to downstream calls

*Error handling*
- [ ] Errors silently ignored (`_, err` without check in Go; empty `.catch()` in JS)
- [ ] Overly generic error messages (no context)
- [ ] Panic/throw without recovery on critical path
- [ ] Errors from goroutines not collected

*Data flow*
- [ ] Unintended mutation (pass by reference side effects)
- [ ] Stale state (cache not invalidated)
- [ ] Missing async/await (JS/TS)
- [ ] Unawaited Promise whose result is used downstream

---

#### Dimension 2 — 🔒 Security

Search for exploitable vulnerabilities.

**Checklist:**

*Input validation*
- [ ] User input directly interpolated into SQL query → **SQL Injection**
- [ ] User input passed directly to shell command → **Command Injection**
- [ ] User input rendered as HTML without sanitization → **XSS**
- [ ] User-supplied path used for file access → **Path Traversal**
- [ ] No validation of type, length, or format on inputs

*Authentication & Authorization*
- [ ] Endpoint missing authentication that should be protected
- [ ] Authorization check absent or bypassable
- [ ] IDOR: resource accessed by ID without ownership verification
- [ ] JWT signature not verified
- [ ] Session not invalidated on logout

*Sensitive data*
- [ ] Password logged or exposed in error messages
- [ ] Secret/API key hardcoded in source
- [ ] Token or credential leaked in response body
- [ ] PII (email, name, etc.) written to logs without masking
- [ ] Password stored without hashing (or with weak hash like MD5)

*Cryptography*
- [ ] Use of deprecated algorithms: MD5, SHA1, DES, ECB mode
- [ ] Non-CSPRNG random number generator used for security purposes
- [ ] IV/nonce reuse for encryption

*HTTP & API*
- [ ] Overly permissive CORS (`*` on sensitive endpoints)
- [ ] No rate limiting on auth/sensitive endpoints
- [ ] Missing security headers (CSP, HSTS, X-Frame-Options)
- [ ] Incorrect HTTP method (GET for data-mutating operations)

*Dependencies*
- [ ] Unused imports still present
- [ ] Very outdated dependency versions (potential CVE exposure)

---

#### Dimension 3 — ⚡ Performance

Search for bottlenecks and resource waste.

**Checklist:**

*Database*
- [ ] N+1 query: query inside a loop without batch/join
- [ ] `SELECT *` when only a few columns are needed
- [ ] Query without index on frequently filtered/joined columns
- [ ] No pagination on endpoints that can return many rows
- [ ] Excessively long transactions (holding locks too long)
- [ ] Connection not closed or returned to pool

*Memory*
- [ ] Entire dataset loaded into memory when streaming is possible
- [ ] Memory leak: event listeners not removed, subscriptions not unsubscribed
- [ ] Large objects copied when pass-by-reference would suffice
- [ ] Buffer/slice grown repeatedly without pre-allocation

*Network & I/O*
- [ ] Requests that could be parallelized but run sequentially
- [ ] No caching for infrequently changing data
- [ ] Large files loaded entirely without streaming
- [ ] Repeated API calls with identical arguments without memoization

*Rendering (Frontend)*
- [ ] Unnecessary re-renders: incorrect dependency array in `useEffect`
- [ ] Missing `useMemo`/`computed` for expensive calculations
- [ ] List without stable `key` prop
- [ ] Images without lazy loading or size optimization
- [ ] Bundle size: large library imported for a single small utility

*Algorithm*
- [ ] O(n²) loop that could be O(n) with Map/Set
- [ ] Repeated sorting on the same dataset
- [ ] Heavy regex compiled repeatedly inside a loop

---

#### Dimension 4 — 📐 Convention

Search for consistency, readability, and maintainability violations.

**Checklist:**

*Naming*
- [ ] Overly generic names: `data`, `result`, `temp`, `obj`, `val`
- [ ] Inconsistent casing: mixed camelCase and snake_case
- [ ] Boolean without `is`/`has`/`can`/`should` prefix
- [ ] Function without verb in name: `user()` should be `getUser()`

*Structure & Readability*
- [ ] Function too long (>50 lines) — candidate for splitting
- [ ] Nesting too deep (>3 levels) — candidate for early return/guard clause
- [ ] Magic numbers/strings without named constants
- [ ] Comments explaining "what" instead of "why"
- [ ] Dead code: unused functions, variables, or imports

*TypeScript / Type Safety*
- [ ] Unnecessary use of `any`
- [ ] Type assertion (`as SomeType`) without runtime check
- [ ] `// @ts-ignore` or `// @ts-nocheck` without justification
- [ ] Overly wide interface (many optional fields that are always present)
- [ ] Missing explicit return type on public API functions

*Framework-specific*
- Vue: `watch` without cleanup, unnecessary reactivity, direct prop mutation
- React: state update during render, missing dependency in `useEffect`
- Go: exported function without doc comment, error wrapping not using `%w`

*Testing (if present)*
- [ ] Test without assertions (test that always passes)
- [ ] Hardcoded data in tests that should use fixtures/factories
- [ ] Tests overly coupled to internal implementation (brittle tests)

---

### Phase 3 — Compile Review Report

Generate the final report using the structure below.
- **Language Alignment**: Write the report in the user's interaction language (English if prompted in English, Indonesian if prompted in Indonesian).

---

```markdown
# Code Review — [Feature Name / File Path]

## 📊 Summary

| Dimension | Critical | High | Medium | Low | Info |
|-----------|----------|------|--------|-----|------|
| 🐛 Bug | 0 | 0 | 0 | 0 | 0 |
| 🔒 Security | 0 | 0 | 0 | 0 | 0 |
| ⚡ Performance | 0 | 0 | 0 | 0 | 0 |
| 📐 Convention | 0 | 0 | 0 | 0 | 0 |

**Total issues:** X &nbsp;|&nbsp; Must fix before merge: X

---

## 🐛 Bug

### [BUG-001] [Short Title]
- **Severity:** `critical` / `high` / `medium` / `low`
- **Location:** `path/to/file.ts:42`
- **Problem:** [Concrete explanation of why this is a bug and its impact]

**Problematic code:**
```[lang]
// problematic code
```

**Suggested fix:**
```[lang]
// corrected code
```

---

## 🔒 Security

### [SEC-001] [Short Title]
- **Severity:** `critical`
- **Location:** `path/to/file.ts:88`
- **Problem:** [Explanation of the vulnerability and potential exploitation]
- **Reference:** OWASP A01:2021 / CWE-89 / etc. (if applicable)

**Problematic code:**
```[lang]
// problematic code
```

**Suggested fix:**
```[lang]
// corrected code
```

---

## ⚡ Performance

### [PERF-001] [Short Title]
- **Severity:** `high` / `medium`
- **Location:** `path/to/file.ts:110`
- **Problem:** [Explanation of the bottleneck and estimated impact]

**Problematic code:**
```[lang]
// problematic code
```

**Suggested fix:**
```[lang]
// corrected code
```

---

## 📐 Convention

### [CONV-001] [Short Title]
- **Severity:** `low` / `info`
- **Location:** `path/to/file.ts:15`
- **Problem:** [Explanation of the convention violation]

**Problematic code:**
```[lang]
// problematic code
```

**Suggested fix:**
```[lang]
// corrected code
```

---

## ✅ What's Done Well

> Acknowledge positive patterns worth keeping.

- [List 2–4 things that are well-written]

---

## 🎯 Action Items

Prioritized fix order:

1. **Must fix before merge** (Critical + High):
   - [ ] [BUG-001] ...
   - [ ] [SEC-001] ...

2. **Strongly recommended** (Medium):
   - [ ] [PERF-001] ...

3. **Nice to have** (Low + Info):
   - [ ] [CONV-001] ...
```

---

### Phase 4 — Next Action Prompt (Interactive Fix Application)

After presenting the review report, the agent MUST ask the user whether they would like to proceed with automated fixes:

1. List the specific issues that have concrete code fix suggestions (from Phases 2–3).
2. Ask the user whether they want the agent to automatically apply the suggested fixes to the affected files.

*Interactive question example at the end of the response:*
> "I found **X** issues with concrete fix suggestions. Would you like me to automatically apply the fixes for the Critical and High severity items to the codebase?"

**CRITICAL RULE**: Do not modify any files automatically. Always wait for the user's explicit confirmation before applying changes.

---

## Severity Guide

| Level | When to Use | Must Fix Before Merge? |
|-------|-------------|------------------------|
| `critical` | Data loss, security breach, production crash | ✅ Yes, block merge |
| `high` | Bug that will definitely occur, SQL injection, serious memory leak | ✅ Yes, block merge |
| `medium` | Conditional bug, poor performance at certain scale | ⚠️ Strongly recommended |
| `low` | Code smell, minor convention violation, small optimization | ℹ️ Optional |
| `info` | Suggestion, more idiomatic alternative, future consideration | ℹ️ Optional |

---

## Review Rules

- **Always include fix code** — do not just describe the problem without a solution.
- **Do not review subjective style** without a clear convention basis from the project.
- **Acknowledge what's good** — a review is not only about what's wrong.
- **Be specific about location** — always mention file and line number when possible.
- **Prioritize Security and Bug** — convention issues can follow later.
- **Do not overwhelm** — if issues exceed 20, group recurring patterns together.
- If the code under review is **already excellent**, state that clearly — do not fabricate problems.

---

## Quality Checklist

Verify these constraints before dispatching the final message:
- [ ] Context block (`[CONTEXT]`) is recorded before beginning review.
- [ ] All four dimensions (Bug, Security, Performance, Convention) are covered.
- [ ] Every issue includes file location, severity, description, and concrete fix code.
- [ ] Summary table counts are accurate.
- [ ] Action items are prioritized by severity.
- [ ] Positive observations are acknowledged.
- [ ] User is asked for permission to apply fixes automatically.
