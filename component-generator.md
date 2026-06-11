---
name: component-generator
description: >
  Detects the active UI framework (Vue 3, React, Svelte, Angular, SolidJS, Astro, etc.)
  and generates production-ready UI components complete with scoped typing, props, event emitters,
  composable hooks (if required), and implementation examples.
  Trigger this skill when the user asks: "create a component", "generate UI components",
  "build a button/modal/card/form/table", or similar UI component generation queries.
  ALWAYS invoke this skill for any UI component creation requests, even if the framework is not specified.
---

# Component Generator

Detects workspace stack conventions, parses component requirements, and drafts typed, accessibility-compliant components.

---

## Workflow Phases

Complete these steps in order. Phase 1 is key for establishing matching patterns.

---

### Phase 1 — Stack & Project Conventions Detection

**Objective:** Map out the client code environment prior to drafting code.

#### 1a. UI Framework Detection

Inspect signature directory files to determine the frontend stack:

| File Indicator | Detected UI Stack |
|----------------|-------------------|
| `nuxt.config.*` | Nuxt (Vue 3) |
| `vue` in `package.json` | Vue 3 (or Vue 2 if `"vue": "^2"`) |
| `next.config.*` / `react` in `package.json` | React / Next.js |
| `svelte.config.*` / `@sveltejs/kit` | SvelteKit / Svelte 5 |
| `angular.json` / `@angular/core` | Angular |
| `solid-js` | SolidJS |
| `astro.config.*` | Astro |

*If detection fails, explicitly ask the user for their targeted tech stack before continuing.*

#### 1b. Utility Tooling Detection

Check dependency packages to style and structure the component:

| Tooling Checked | Design Pattern & Implication |
|-----------------|-----------------------------|
| `typescript` or `tsconfig.json` | Draft components with strong typing (Interfaces & Types). |
| `tailwindcss` or `tailwind.config.*` | Use Tailwind CSS utility classes for layout markup. |
| `pinia` (for Vue) | Component may bind to Pinia store attributes. |
| `vee-validate`, `react-hook-form`, `zod` | Use standard validator configurations. |
| `shadcn-ui`, `radix-ui`, `headlessui` | Leverage primitive hooks or component elements. |
| `vitest`, `jest`, `testing-library` | Prepare component unit tests alongside code. |

#### 1c. Code Alignment Rules

Inspect 1 or 2 existing components (e.g. under `components/`, `src/components/`, `app/components/`) to identify styling conventions:
- **Naming Conventions**: PascalCase vs. kebab-case file paths.
- **CSS Strategy**: Scoped styles vs. CSS Modules vs. Tailwind.
- **Vue Props Handling**: `defineProps` vs. `withDefaults` with generic TypeScript shapes.

Record these properties in a `[STACK]` overview block prior to Proceeding to Phase 2.

---

### Phase 2 — System Decomposition & Requirements

**Objective:** Map props, states, styles, and events prior to writing code.

#### 2a. Component Blueprint Mapping

Identify the following structures from the user requirements:

**Name & Placement Category (Atomic Design)**
- **Name**: PascalCase (e.g. `UserCard`, `DataTable`, `SearchInput`).
- **Classification**:
  - *Atom*: Button, Input, Icon, Spinner, Badge, Avatar.
  - *Molecule*: FormField, MenuItem, SearchBar, CardHeader.
  - *Organism*: DataTable, UserForm, ProductCard, NavigationHeader.
  - *Template*: PageLayout, DashboardWrapper, AuthShell.

**Props Definitions**
Map and define each prop:
- Property name (camelCase).
- Data Type (string, number, boolean, object, array, enum).
- Required status & default value properties.

**Events & Callback Handlers**
- Determine events to bubble upwards.
- Vue convention: `emit('update:modelValue')` / React: `onChange: (value: string) => void`.

**Slot Configurations / Children**
- Decide slots setups (Default slots, Svelte snippets, or React `ReactNode` items).

**Local Component State**
- Map local states (e.g., active dropdown triggers, focus handlers).

---

### Phase 3 — Component Codebase Templates

Generate complete, typed components according to the detected stack:

### Vue 3 Composition Format

```vue
<script setup lang="ts">
// 1. Types & Interfaces
interface Props {
  label: string
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
}

// 2. Props with defaults
const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
})

// 3. Emits
const emit = defineEmits<{
  click: [event: MouseEvent]
  'update:modelValue': [value: string]
}>()

// 4. Computed Classes & Hooks
const classes = computed(() => {
  return {}
})
</script>

<template>
  <button :disabled="disabled || loading" :class="classes" @click="emit('click', $event)">
    <slot name="prefix" />
    <span>{{ label }}</span>
    <slot />
  </button>
</template>

<style scoped>
/* Scoped styles only if Tailwind is not in use */
</style>
```

**Vue Rules**:
- Always utilize `<script setup lang="ts">`.
- Avoid old Options API layouts. Define props via `withDefaults(defineProps<Props>(), {...})`.
- Type emit declarations in compiler macros.
- Use `use[Name].ts` composables if logic exceeds 30 lines.

---

### React Component Format

```tsx
import * as React from 'react'

// 1. Component Interfaces
export interface [ComponentName]Props {
  label: string
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void
  onChange?: (value: string) => void
  children?: React.ReactNode
}

// 2. Main Component Definition
export function [ComponentName]({
  label,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  children,
}: [ComponentName]Props) {
  // State & interaction hooks
  
  return (
    <button
      disabled={disabled || loading}
      onClick={onClick}
      className={`btn btn-${variant} btn-${size}`}
    >
      <span>{label}</span>
      {children}
    </button>
  )
}

[ComponentName].displayName = '[ComponentName]'
```

**React Rules**:
- Standardize on named exports over default exports (except pages in Next.js).
- If internal state exceeds 20 lines, split into a custom `use[ComponentName].ts` state hook.
- Implement `React.forwardRef` if exposure of node element DOM reference is required.

---

### Svelte 5 (Runes Concept)

```svelte
<script lang="ts">
  // Types & properties
  interface Props {
    label: string
    variant?: 'primary' | 'secondary'
    onclick?: (e: MouseEvent) => void
    children?: import('svelte').Snippet
  }

  let {
    label,
    variant = 'primary',
    onclick,
    children,
  }: Props = $props()

  // Svelte 5 reactive states
  let count = $state(0)
</script>

<button {onclick} class="btn-{variant}">
  {label}
  {@render children?.()}
</button>
```

---

### Angular standalone Component

```typescript
import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core'
import { CommonModule } from '@angular/common'

export type Variant = 'primary' | 'secondary' | 'danger'

@Component({
  selector: 'app-[component-name]',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <button [disabled]="disabled" (click)="clicked.emit($event)">
      {{ label }}
    </button>
  `,
})
export class [ComponentName]Component {
  @Input({ required: true }) label!: string
  @Input() variant: Variant = 'primary'
  @Input() disabled = false

  @Output() clicked = new EventEmitter<MouseEvent>()
}
```

---

## Required Deliverables per Component

Ensure the final agent message includes:
- **Language Alignment**: Write all descriptions, comments, props table labels, and usage examples in the user's interaction language (English if prompted in English, Indonesian if prompted in Indonesian). Code identifiers (variable names, function names) always remain in English.

1. **Core Component Code**: Thoroughly written code matching typescript standards.
2. **TypeScript Declarations**: Explicit props and event structures.
3. **Usage Demonstrations**: Clear examples for primary options and variations.
4. **Summary Reference Table**: A markdown table documenting the component's API properties.

---

## Phase 4 — Next Action Prompt (Interactive File Creation)

After generating the code blueprints, the agent MUST prompt the user for permission to write the files directly to the codebase:
1. Recommend the path where the component fits based on Phase 1c analysis (e.g. `src/components/UserCard.vue`, `components/UserCard.tsx`, or `app/components/UserCard.tsx`).
2. Ask if the user wants the agent to automatically write the generated component code to that suggested file path.

*Interactive question example at the end of the response:*
> "Would you like me to write this component code automatically to `src/components/UserCard.tsx`?"

**CRITICAL RULE**: Do not write the file or create parent folders without explicit confirmation from the user.

---

## Coding Quality Standards

- **Forbidden Types**: Never fallback to `any` typings. Keep type assertions explicit.
- **Accessibility (A11y)**: Integrate required attributes (e.g., `aria-label`, `role`, keyboard trigger bindings).
- **Tailwind conditional tools**: Use standard classes manipulation tools libraries like `cn()` / `clsx()` / `tailwind-merge` instead of string templates.
- **Large Components**: Split components into specialized sub-modules if files exceed 150 lines.

---

## Quality Checklist

Verify these constraints before dispatching the final message:
- [ ] UI framework is correctly identified and template aligns.
- [ ] TypeScript syntax has been generated (assuming project uses TS).
- [ ] Props declarations define default properties.
- [ ] Example usages showcase code variations.
- [ ] A clean summary table is generated representing the properties API.
- [ ] Output descriptions and documentation are in the user's language.
- [ ] User is prompted for permission to create/write the component automatically at a suggested path.
