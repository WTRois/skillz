---
name: optimize-laravel-inertia-vue
description: >
  Enforces best practices for Laravel + Inertia.js + Vue 3 + TypeScript full-stack applications.
  Use this skill when building new features, refactoring, code reviewing, debugging, testing,
  or optimizing any Laravel Inertia Vue project.
  Trigger this skill when the user asks: "create a new feature", "build CRUD for [resource]",
  "refactor this controller", "optimize this page", "review this Inertia code",
  "best practices for Laravel Vue", "optimize-laravel-inertia-vue", or any task involving
  Laravel controllers, Inertia responses, Vue pages, or full-stack TypeScript patterns.
  ALWAYS invoke this skill for any Laravel + Inertia + Vue development task.
---

# Laravel + Inertia + Vue 3 Best Practices

Comprehensive ruleset and workflow for building maintainable, type-safe, and performant
full-stack applications with Laravel, Inertia.js, and Vue 3 Composition API.

---

## Core Principles

Every piece of generated code must be:
- **Maintainable** — clear separation of concerns, no god classes.
- **Consistent** — follows modern Laravel and Vue 3 conventions.
- **Type-safe** — TypeScript everywhere on frontend, strict PHPStan on backend.
- **Testable** — every feature can be covered by automated tests.
- **Simple** — no over-engineering; choose the simplest solution that satisfies the requirement.
- **Inertia-correct** — respects the Inertia protocol (server-driven navigation, shared data, proper form handling).

---

## Architecture Rules

### Backend Responsibilities (Laravel)

Laravel owns all of the following — never push these into Vue components:
- Business logic and domain rules.
- Authorization (Policies / Gates).
- Validation (FormRequest classes).
- Database access and query building.
- Data transformation (API Resources / Data Transfer Objects).

**Rule**: If logic touches the database or enforces a business rule, it belongs in a Service class, Action class, or Domain layer — never directly in a Controller.

### Controller Rules

Controllers must remain thin. A well-structured controller method should only:

```php
public function store(StoreProjectRequest $request): RedirectResponse
{
    // 1. Authorization (handled by FormRequest or Policy)
    // 2. Validation (handled by FormRequest — already resolved)
    // 3. Delegate to service/action
    $project = app(CreateProjectAction::class)->execute($request->validated());

    // 4. Return Inertia response
    return redirect()
        ->route('projects.show', $project)
        ->with('success', 'Project created successfully.');
}
```

**Anti-patterns to avoid:**
- Business logic directly in controller methods.
- Raw `$request->validate()` for complex validation — use FormRequest instead.
- Inline authorization checks — use `$this->authorize()` or Policy.
- Returning excessive data in Inertia responses.

### Validation Rules

Always use **FormRequest** classes for any feature with more than two validation rules:

```php
class StoreProjectRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Project::class);
    }

    /** @return array<string, mixed> */
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string', 'max:1000'],
            'status' => ['required', Rule::in(['draft', 'active', 'archived'])],
            'team_id' => ['required', 'exists:teams,id'],
        ];
    }
}
```

### Authorization Rules

Always use **Policy** or **Gate** — never hardcode role checks in controllers or Vue components:

```php
// In Policy
public function update(User $user, Project $project): bool
{
    return $user->id === $project->user_id
        || $user->hasRole('admin');
}

// In Controller
$this->authorize('update', $project);
```

### Database Rules

- **Prevent N+1 Queries**: Always use **eager loading** (`with()`) for related models accessed in views or resources.
- **Limit Columns**: Use `select()` to limit columns retrieved from database tables, especially for tables with large payload fields.
- **Optimized Pagination**: For large datasets (millions of records) or infinite-scroll grids, prefer `cursorPaginate()` over offset-based `paginate()` to avoid deep offset performance overhead.
- **Database Transactions**: Always wrap multi-row or multi-table database write operations in a `DB::transaction()` block to ensure data integrity and ACID compliance.
- **Bulk Operations**: Never execute queries inside loops. Use `chunk()`, `chunkById()`, or `lazy()` for processing large batches. Use `upsert()` or `insert()` for bulk inserts/updates.
- **Database Indexes**: Ensure proper indexing in migration classes:
  - Foreign keys (`foreignId()->index()`).
  - Frequently filtered columns (e.g., `status`, `type`).
  - Frequently sorted columns (e.g., `created_at`, `published_at`).
  - Compound (composite) indexes for combinations of fields frequently filtered/sorted together.

```php
// Good - eager loaded, limited columns, cursor paginated (or custom pagination)
$projects = Project::with(['owner:id,name', 'tasks:id,project_id,title,status'])
    ->select(['id', 'name', 'status', 'user_id', 'created_at'])
    ->cursorPaginate(20);

// Good - Database Transaction for multi-write operations
DB::transaction(function () use ($validatedData) {
    $project = Project::create($validatedData);
    $project->history()->create(['action' => 'created']);
    return $project;
});

// Bad — N+1, selecting everything, offset pagination on large table
$projects = Project::paginate(20);
// then in blade/vue: $project->owner->name (triggers N+1 query inside loop)
```

---

## Inertia.js Rules

### Data Transfer

Send **only the data the page needs** — never dump entire models or collections (which risks exposing sensitive fields like `password`, `remember_token`, or internal columns).
Always explicitly map fields inside **API Resource** classes:

```php
// In Controller
return Inertia::render('Projects/Index', [
    'projects' => ProjectResource::collection($projects),
    'filters' => $request->only(['search', 'status']),
]);
```

```php
// ProjectResource.php
class ProjectResource extends JsonResource
{
    /** @return array<string, mixed> */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'status' => $this->status,
            'ownerName' => $this->owner->name,
            'taskCount' => $this->tasks_count,
            'createdAt' => $this->created_at->toISOString(),
        ];
    }
}
```

### Shared Data (HandleInertiaRequests)

Use the `HandleInertiaRequests` middleware for globally available data:
- Authenticated user info.
- Flash messages.
- App-wide settings or permissions.

```php
public function share(Request $request): array
{
    return [
        ...parent::share($request),
        'auth' => [
            'user' => $request->user()
                ? $request->user()->only('id', 'name', 'email')
                : null,
        ],
        'flash' => [
            'success' => $request->session()->get('success'),
            'error' => $request->session()->get('error'),
        ],
    ];
}
```

### Lazy Evaluation & Deferred Props (Inertia v2.0+)

For secondary or slow-loading data (e.g., analytics, charts, unrelated tables), use Deferred / Lazy evaluation to improve the Time to First Byte (TTFB) and initial page load speed.

```php
// In Controller (Deferred / Lazy Loading)
return Inertia::render('Projects/Index', [
    'projects' => ProjectResource::collection($projects), // Immediate payload
    
    // Asynchronously deferred prop (Inertia v2.0+)
    'analytics' => Inertia::defer(fn () => AnalyticsService::getSummary()),
    
    // Lazy loaded (only requested on-demand by client)
    'archivedCount' => Inertia::lazy(fn () => Project::where('status', 'archived')->count()),
]);
```

### Inertia Forms

Use `useForm()` for all standard CRUD operations. Prioritize **server-side validation** — do not duplicate complex validation rules on the frontend. Always render validation errors securely under each input:

```vue
<template>
  <form @submit.prevent="submit" class="space-y-4">
    <div>
      <label for="name">Project Name</label>
      <input 
        id="name" 
        v-model="form.name" 
        type="text" 
        class="border p-2 w-full"
        :class="{ 'border-red-500': form.errors.name }"
      />
      <span v-if="form.errors.name" class="text-sm text-red-500">{{ form.errors.name }}</span>
    </div>

    <div>
      <label for="description">Description</label>
      <textarea 
        id="description" 
        v-model="form.description" 
        class="border p-2 w-full"
        :class="{ 'border-red-500': form.errors.description }"
      ></textarea>
      <span v-if="form.errors.description" class="text-sm text-red-500">{{ form.errors.description }}</span>
    </div>

    <button type="submit" :disabled="form.processing" class="bg-blue-500 text-white p-2 text-sm">
      {{ form.processing ? 'Saving...' : 'Create Project' }}
    </button>
  </form>
</template>

<script setup lang="ts">
import { useForm } from '@inertiajs/vue3'

interface ProjectForm {
  name: string
  description: string
  status: 'draft' | 'active' | 'archived'
  team_id: number | null
}

const form = useForm<ProjectForm>({
  name: '',
  description: '',
  status: 'draft',
  team_id: null,
})

function submit() {
  form.post(route('projects.store'), {
    preserveScroll: true,
    onSuccess: () => form.reset(),
  })
}
</script>
```

---

## Vue 3 Rules

### Script Setup & TypeScript

Always use the Composition API with TypeScript:

```vue
<script setup lang="ts">
// All Vue components must use this format
</script>
```

### Component Size Limit

If a `.vue` file exceeds **200 lines**:
- Extract sub-components for reusable UI blocks.
- Extract logic into composables (`use[Name].ts`).
- Extract pure utility functions into `lib/` or `utils/`.

### Props Typing

Always define explicit TypeScript interfaces for props — never use `any`:

```vue
<script setup lang="ts">
interface Props {
  project: {
    id: number
    name: string
    status: 'draft' | 'active' | 'archived'
    ownerName: string
    taskCount: number
    createdAt: string
  }
  canEdit: boolean
}

const props = defineProps<Props>()
</script>
```

### Business Logic Placement

Do not place heavy business logic in Vue components. Move it to:
- **Composables** — for stateful, reusable reactive logic (`useProjectFilters.ts`).
- **Utility functions** — for pure, stateless transformations (`lib/formatCurrency.ts`).

### SSR (Server-Side Rendering) Compatibility

If the application supports Server-Side Rendering (SSR):
- Do not access browser global objects (`window`, `document`, `localStorage`, `sessionStorage`, etc.) directly at the root level of `<script setup>`.
- Move any setup code that relies on these browser globals inside the `onMounted()` lifecycle hook.

```vue
<script setup lang="ts">
import { onMounted, ref } from 'vue'

const currentTheme = ref('light')

// Avoid direct global access at root level (could crash SSR server)
// currentTheme.value = localStorage.getItem('theme') || 'light'

// Safe for SSR
onMounted(() => {
  currentTheme.value = localStorage.getItem('theme') || 'light'
})
</script>
```

---

## TypeScript Rules

- **Forbidden**: `any` type — unless genuinely unavoidable and documented with a `// TODO` comment.
- **Required**: Explicit interfaces for all Inertia page props, form data, and API responses.
- **Recommended**: Shared type definitions in a `types/` directory (`types/models.d.ts`, `types/inertia.d.ts`).
- **Type-safe Routing (Ziggy)**: Always integrate route autocompletion for the `route()` helper. Ensure typing files (such as `ziggy.d.ts` generated via `php artisan ziggy:generate` or `@types/ziggy-js`) are imported and declared in `tsconfig.json`.

```typescript
// Example of type-safe routing on the frontend
route('projects.show', { project: props.project.id })
```

```typescript
// types/models.d.ts
export interface User {
  id: number
  name: string
  email: string
}

export interface Project {
  id: number
  name: string
  status: 'draft' | 'active' | 'archived'
  ownerName: string
  taskCount: number
  createdAt: string
}

// types/inertia.d.ts
export interface PageProps {
  auth: {
    user: User | null
  }
  flash: {
    success: string | null
    error: string | null
  }
}
```

---

## Naming Conventions

### Pages (Inertia Vue Pages)

Follow Laravel resource controller naming:

```
resources/js/Pages/
├── Users/
│   ├── Index.vue
│   ├── Create.vue
│   ├── Edit.vue
│   └── Show.vue
├── Projects/
│   ├── Index.vue
│   ├── Create.vue
│   ├── Edit.vue
│   └── Show.vue
```

### Components

PascalCase, descriptive, domain-prefixed:

```
resources/js/Components/
├── UserTable.vue
├── UserForm.vue
├── UserCard.vue
├── ProjectStatusBadge.vue
```

### Composables

`use` prefix, camelCase:

```
resources/js/Composables/
├── useUserFilters.ts
├── useProjectActions.ts
├── usePagination.ts
```

---

## Testing Rules

### Backend (Laravel)

- Write **Feature Tests** for every controller action (HTTP-level tests).
- Write **Unit Tests** for isolated Service/Action classes with complex logic.
- Use factories and seeders for test data — never hardcode IDs or values.

```php
public function test_user_can_create_project(): void
{
    $user = User::factory()->create();
    $team = Team::factory()->create();

    $this->actingAs($user)
        ->post(route('projects.store'), [
            'name' => 'New Project',
            'description' => 'A test project',
            'status' => 'draft',
            'team_id' => $team->id,
        ])
        ->assertRedirect()
        ->assertSessionHas('success');

    $this->assertDatabaseHas('projects', ['name' => 'New Project']);
}
```

### Frontend (Vue)

- **Vitest** for component unit tests and composable tests.
- **Playwright** for end-to-end tests on critical user flows (login, CRUD operations, payment).

---

## Feature Generation Workflow

When building a new feature, follow this exact sequence:

1. **Analyze requirements** — understand the domain, entities, and user stories.
2. **Identify models** — determine Eloquent models, migrations, and relationships involved.
3. **Define authorization** — create or update Policies.
4. **Define validation** — create FormRequest classes.
5. **Build backend** — Service/Action classes, Controller methods, API Resources.
6. **Build Inertia response** — map data to page props using Resources.
7. **Build Vue page** — create typed page component with `<script setup lang="ts">`.
8. **Add TypeScript types** — define or update shared interfaces.
9. **Review performance** — check for N+1 queries, payload size, unnecessary re-renders.
10. **Review security** — verify authorization, input sanitization, and CSRF protection.

**Rule**: Do not write code without first explaining the solution structure to the user. Present the plan, then implement after alignment.

---

## Performance Checklist

Run through these checks before considering a feature complete:

- [ ] No N+1 queries (verify with Laravel Debugbar or Telescope).
- [ ] No unnecessary Vue component re-renders (check reactive dependencies).
- [ ] Inertia page props payload is minimal — no unused data sent to client.
- [ ] Heavy or secondary page props use Inertia lazy/deferred loading.
- [ ] No duplicated database queries across controller methods.
- [ ] No duplicated API calls from Vue components.
- [ ] Database indexes exist for frequently filtered, sorted, or foreign-key columns.
- [ ] All multi-write/update sequences use Database Transactions.
- [ ] Cursor pagination is used for high-volume infinite scroll datasets instead of offset-based pagination.
- [ ] No unnecessary Vue `watch()` calls — prefer `computed` when possible.
- [ ] Large lists use pagination — never load unbounded collections.

---

## Code Review Checklist

Verify before approving any PR:

1. Is the controller thin (authorize → validate → delegate → respond)?
2. Is authorization enforced via Policy or Gate?
3. Is validation handled by FormRequest?
4. Are there N+1 query risks or missing database indexes (e.g., in migrations)?
5. Are sensitive payload fields excluded in API Resources?
6. Are multi-row write operations wrapped in a Database Transaction?
7. Is the frontend fully TypeScript type-safe (no `any`, type-safe routes)?
8. Are Vue components under 200 lines?
9. Is the Inertia props payload minimal (and lazy loaded when appropriate)?
10. Are browser globals (like `window`) safe for SSR (not accessible at `setup` root level)?
11. Is the feature testable?
12. Is there code duplication that should be extracted?
13. Is this the simplest correct solution?

---

## Interactive Prompt

After generating code or completing a review using this skill, the agent MUST ask the user what they would like to do next. Suggest contextually relevant follow-up actions based on the work performed.

*Examples:*
> "The feature scaffolding is ready. Would you like me to also generate the Feature Test for the `ProjectController`?"

> "I've reviewed the code. Would you like me to apply the suggested fixes to `app/Http/Controllers/ProjectController.php` and `resources/js/Pages/Projects/Index.vue`?"

> "The CRUD pages are generated. Would you like me to create the TypeScript type definitions in `resources/js/types/models.d.ts`?"

**CRITICAL RULE**: Do not write files or apply changes without explicit user confirmation.

---

## Quality Checklist

Verify these constraints before dispatching the final message:
- [ ] Backend follows thin controller pattern.
- [ ] FormRequest and Policy classes are used appropriately.
- [ ] Inertia data transfer uses API Resources.
- [ ] Vue components use `<script setup lang="ts">` exclusively.
- [ ] No `any` types in TypeScript code.
- [ ] Naming conventions are consistent (Pages, Components, Composables).
- [ ] Output descriptions and documentation are in the user's language.
- [ ] User is prompted for a contextually relevant next action.
