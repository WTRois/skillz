---
name: optimize-laravel-inertia-vue
description: >
  Guides feature work, refactoring, debugging, testing, and architecture review for Laravel + Inertia.js
  + Vue 3 + TypeScript applications. Use when the task specifically involves Laravel controllers,
  FormRequests, Policies, Inertia props/forms, Vue pages, or shared full-stack patterns. For a general
  code review or dedicated security audit, use the corresponding specialist skill instead.
---

# Laravel + Inertia + Vue 3

Use the simplest project-consistent solution. Read the repository conventions and relevant files before
recommending or writing code.

## Workflow

1. Detect Laravel, Inertia, Vue, TypeScript, testing, and styling conventions.
2. Map the request across route, authorization, validation, action/service, model/query, Inertia props,
   page/component, types, and tests.
3. Explain the smallest implementation plan before making changes. Ask before writing files.
4. Keep controllers thin: authorize, validate, delegate, and respond.
5. Keep business rules and database access out of Vue components; use Policies/FormRequests and the existing
   service/action/domain convention.
6. Keep Inertia payloads minimal and use lazy/deferred props only when the project and data shape justify it.
7. Use Vue 3 `<script setup lang="ts">`, typed props, accessible forms, SSR-safe browser access, and the
   repository's existing styling/component primitives.
8. Add the smallest meaningful test for non-trivial behavior and run the project's existing checks.
9. Before finishing, check authorization, validation, N+1 queries, payload size, type safety, accessibility,
   and duplication.

## References

Load [references/laravel-inertia-vue-guidance.md](references/laravel-inertia-vue-guidance.md) only for
framework-specific patterns, checklists, and examples needed by the current task.

## Output

State the detected stack, scope, implementation plan, changed files, verification commands/results, and
remaining risks. Do not modify files or generate follow-up artifacts without explicit user confirmation.
