---
name: api-designer
description: >
  Use this skill BEFORE any endpoint is coded — whenever the user wants to design, plan, document,
  or review a REST API. Triggers include: "design API", "create API contract", "what endpoints do I need",
  "API spec", "request/response schema", "build API for feature X", "API contract",
  "plan endpoints", "OpenAPI", "swagger spec", "before I build the API", or any phrase implying
  API planning before implementation starts.
  Always use this skill when: user is planning a new feature that will expose HTTP endpoints,
  asking how to structure an API resource, or needs to align frontend/backend before development starts.
  Output: Markdown API contract — method + path, request/response schema (JSON), HTTP status codes,
  error envelope, and auth requirement per endpoint.
  Do NOT use for: GraphQL schema design, gRPC/Protobuf, SDK code generation, or existing API debugging.
---

# API Designer

Generates a complete **API contract** before a single line of implementation code is written.
The output is a Markdown document that serves as a single source of truth between frontend, backend, and QA teams.

---

## Philosophy: Contract-First

An API contract is not documentation — it is an **agreement** that precedes implementation.
The correct order is: **Design → Review → Code**, not Code → Document.

Direct benefits:
- Frontend and backend can develop in parallel.
- No surprises during integration.
- Error handling is defined before edge cases surface in production.

---

## Workflow

### Phase 1 — Extract Context

Before writing a single endpoint, identify:

- **Primary resources**: What objects are exposed? (`users`, `orders`, `products`)
- **Actor / consumer**: Who calls the API? (mobile app, web client, third-party service, internal microservice)
- **Auth model**: public, API key, Bearer JWT, OAuth2, session cookie?
- **Versioning style**: URL path (`/v1/`), header (`API-Version`), or none?
- **Casing convention**: `camelCase` (JSON default) or `snake_case`?

If not specified, apply these defaults: Bearer JWT, `/v1/` URL prefix, `camelCase` JSON bodies.
Ask **at most 3 clarifying questions** if context is genuinely missing.

---

### Phase 2 — Map Resources to Endpoints

For each resource, apply the standard CRUD pattern first, then add non-standard actions:

| Action | Method | Path | Notes |
|--------|--------|------|-------|
| List | GET | `/v1/{resources}` | Paginated, filterable |
| Create | POST | `/v1/{resources}` | Body = payload |
| Get one | GET | `/v1/{resources}/{id}` | Single resource by ID |
| Full update | PUT | `/v1/{resources}/{id}` | Replace entire resource |
| Partial update | PATCH | `/v1/{resources}/{id}` | Update specific fields |
| Delete | DELETE | `/v1/{resources}/{id}` | Soft delete preferred |
| Custom action | POST | `/v1/{resources}/{id}/{action}` | e.g., `/orders/{id}/cancel` |

**Path design principles:**
- Plural nouns, lowercase, hyphens for multi-word segments (`/product-categories`).
- Non-CRUD actions use POST to a sub-resource verb — never `GET /cancelOrder`.
- Nested resources limited to one level: `/orders/{id}/items` — avoid `/a/{id}/b/{id}/c/{id}`.

---

### Phase 3 — Define Request/Response Schemas

For every endpoint, specify:
- **Request**: path params, query params, required headers, body (with data types and validation rules).
- **Success response**: HTTP status code and full body schema with realistic example JSON.
- **Error responses**: all realistic error codes with conditions and error envelope usage.

---

### Phase 4 — Write the Contract

Use the template structure below. Fill each section according to the user's domain.
- **Language Alignment**: Write all descriptions, table labels, error condition explanations, and design notes in the user's interaction language (English if prompted in English, Indonesian if prompted in Indonesian). JSON field names, HTTP methods, and URL paths always remain in English.

---

## Output Template

````markdown
# API Contract: [Feature / Domain Name]

> Base URL: `https://api.example.com`
> API Version: v1
> Auth: Bearer JWT (unless marked `[PUBLIC]`)
> Content-Type: `application/json`
> Date: [YYYY-MM-DD]

---

## Error Envelope (Global)

All error responses use this structure consistently:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource does not exist.",
    "details": {}
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `error.code` | string | Machine-readable error identifier (SCREAMING_SNAKE_CASE) |
| `error.message` | string | Human-readable description |
| `error.details` | object | Optional — field-level validation errors, trace info, etc. |

---

## Standard HTTP Status Codes

| Code | When to Use |
|------|-------------|
| `200 OK` | Request succeeded, response body returned |
| `201 Created` | Resource successfully created |
| `204 No Content` | Success, no body (DELETE, logout) |
| `400 Bad Request` | Validation failed, malformed body |
| `401 Unauthorized` | Token missing or expired |
| `403 Forbidden` | Token valid but insufficient permissions |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Duplicate data or state conflict |
| `422 Unprocessable Entity` | Syntax valid but business logic prevents processing |
| `429 Too Many Requests` | Rate limit reached |
| `500 Internal Server Error` | Unhandled server error |

---

## Endpoints

---

### 1. List Users

**`GET /v1/users`**
Retrieve a paginated list of users with optional filters.
Auth: `Bearer JWT` | Role: `admin`

#### Query Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `page` | integer | No | `1` | Page number |
| `limit` | integer | No | `20` | Max `100` |
| `search` | string | No | — | Filter by name or email (partial match) |
| `status` | string | No | — | `active` \| `inactive` \| `banned` |
| `sortBy` | string | No | `createdAt` | Field to sort by |
| `sortDir` | string | No | `desc` | `asc` \| `desc` |

#### Response `200 OK`

```json
{
  "data": [
    {
      "id": "usr_01J8X2K9M3P",
      "email": "jane@example.com",
      "name": "Jane Doe",
      "status": "active",
      "createdAt": "2024-11-01T08:30:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 142,
    "totalPages": 8
  }
}
```

#### Error Codes

| Status | Code | Condition |
|--------|------|-----------|
| `401` | `UNAUTHORIZED` | Token invalid or expired |
| `403` | `FORBIDDEN` | Not an `admin` role |

---

### 2. Create User

**`POST /v1/users`**
Create a new user.
Auth: `Bearer JWT` | Role: `admin`

#### Request Body

```json
{
  "email": "john@example.com",
  "name": "John Smith",
  "password": "Str0ng!Pass",
  "role": "member"
}
```

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `email` | string | Yes | Valid email format, unique in system |
| `name` | string | Yes | Min 2, max 100 characters |
| `password` | string | Yes | Min 8 characters, must contain uppercase + digit |
| `role` | string | No | `member` \| `admin` — default `member` |

#### Response `201 Created`

```json
{
  "data": {
    "id": "usr_01J8X2K9M3P",
    "email": "john@example.com",
    "name": "John Smith",
    "role": "member",
    "status": "active",
    "createdAt": "2024-11-15T10:00:00Z"
  }
}
```

#### Error Codes

| Status | Code | Condition |
|--------|------|-----------|
| `400` | `VALIDATION_ERROR` | Field does not meet validation — `details` contains per-field errors |
| `409` | `EMAIL_ALREADY_EXISTS` | Email already registered |

---

### 3. Get User

**`GET /v1/users/{id}`**
Retrieve details of a single user by ID.
Auth: `Bearer JWT` | Role: `admin` or the user themselves

#### Path Parameters

| Param | Type | Description |
|-------|------|-------------|
| `id` | string | User ID (format `usr_*`) |

#### Response `200 OK`

```json
{
  "data": {
    "id": "usr_01J8X2K9M3P",
    "email": "john@example.com",
    "name": "John Smith",
    "role": "member",
    "status": "active",
    "createdAt": "2024-11-15T10:00:00Z",
    "updatedAt": "2024-11-15T10:00:00Z"
  }
}
```

#### Error Codes

| Status | Code | Condition |
|--------|------|-----------|
| `403` | `FORBIDDEN` | User attempting to access another user's data |
| `404` | `USER_NOT_FOUND` | ID not found |

---

### 4. Update User (Partial)

**`PATCH /v1/users/{id}`**
Update specific fields of a user. Only fields included in the body are modified.
Auth: `Bearer JWT` | Role: `admin` or the user themselves

#### Request Body

```json
{
  "name": "John Updated",
  "status": "inactive"
}
```

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `name` | string | No | Min 2, max 100 characters |
| `status` | string | No | `active` \| `inactive` — only `admin` can change |

#### Response `200 OK`

```json
{
  "data": {
    "id": "usr_01J8X2K9M3P",
    "name": "John Updated",
    "status": "inactive",
    "updatedAt": "2024-11-20T09:15:00Z"
  }
}
```

#### Error Codes

| Status | Code | Condition |
|--------|------|-----------|
| `400` | `VALIDATION_ERROR` | Invalid field value |
| `403` | `FORBIDDEN` | Non-admin attempting to change `status` |
| `404` | `USER_NOT_FOUND` | ID not found |

---

### 5. Delete User

**`DELETE /v1/users/{id}`**
Soft-delete a user (sets `deletedAt` timestamp, does not remove from database).
Auth: `Bearer JWT` | Role: `admin`

#### Response `204 No Content`

_(Empty body)_

#### Error Codes

| Status | Code | Condition |
|--------|------|-----------|
| `403` | `FORBIDDEN` | Not an `admin` role |
| `404` | `USER_NOT_FOUND` | ID not found |
| `409` | `CANNOT_DELETE_SELF` | Admin attempting to delete their own account |

---

### 6. Custom Action — Suspend User

**`POST /v1/users/{id}/suspend`**
Explicitly suspend a user with a reason. Differs from a status update because it creates an audit log entry.
Auth: `Bearer JWT` | Role: `admin`

#### Request Body

```json
{
  "reason": "Violation of terms of service",
  "notifyUser": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `reason` | string | Yes | Min 10 characters |
| `notifyUser` | boolean | No | Default `false` — send email notification |

#### Response `200 OK`

```json
{
  "data": {
    "id": "usr_01J8X2K9M3P",
    "status": "suspended",
    "suspendedAt": "2024-11-20T09:15:00Z",
    "suspendedBy": "usr_admin_001",
    "reason": "Violation of terms of service"
  }
}
```

#### Error Codes

| Status | Code | Condition |
|--------|------|-----------|
| `404` | `USER_NOT_FOUND` | ID not found |
| `409` | `USER_ALREADY_SUSPENDED` | User is already in suspended status |

---

## Endpoint Summary

| # | Method | Path | Auth | Description |
|---|--------|------|------|-------------|
| 1 | GET | `/v1/users` | JWT / admin | List users |
| 2 | POST | `/v1/users` | JWT / admin | Create user |
| 3 | GET | `/v1/users/{id}` | JWT / self or admin | Get user |
| 4 | PATCH | `/v1/users/{id}` | JWT / self or admin | Update user |
| 5 | DELETE | `/v1/users/{id}` | JWT / admin | Delete user |
| 6 | POST | `/v1/users/{id}/suspend` | JWT / admin | Suspend user |

````

---

## Design Conventions & Decisions

### ID Format
Use **Prefixed IDs** (`usr_`, `ord_`, `prd_`) for easier debugging and log tracing.
Alternative: plain UUID — more universal but less human-readable.

### Pagination
**Offset-based** (page + limit) for most use cases.
Use **cursor-based** if the dataset is large (>1M rows) or for real-time feeds where sort order may shift.

```json
{
  "meta": {
    "nextCursor": "eyJpZCI6MTIzfQ==",
    "hasMore": true
  }
}
```

### Timestamps
Always **ISO 8601 UTC** (`2024-11-15T10:00:00Z`). Never send Unix timestamps to clients.

### Versioning
- **URL path** (`/v1/`) — most visible, easy to test in browser.
- **Header** (`API-Version: 2024-11`) — more "RESTful" but less discoverable.
- Pick one and stay consistent. Default: URL path.

### Naming: camelCase vs. snake_case
- JSON body → `camelCase` (JavaScript-friendly default).
- Query params → `camelCase` as well (`?sortBy=createdAt`).
- Internal documentation → flexible, as long as it is consistent.

---

## Phase 5 — Next Action Prompt (Interactive Contract File Creation)

After generating the complete API contract, the agent MUST ask the user for permission before writing any files:

1. Recommend a file path for the contract document (e.g. `docs/api-contract-[domain].md`).
2. Ask if the user wants the agent to write the contract automatically to that path.

*Interactive question example at the end of the response:*
> "Would you like me to save this API contract to `docs/api-contract-users.md`?"

**CRITICAL RULE**: Do not create any files automatically. Always wait for explicit user confirmation before writing to disk.

---

## Quality Checklist

Verify these constraints before dispatching the final message:
- [ ] Every endpoint has an explicit auth requirement.
- [ ] All realistic error codes are listed per endpoint.
- [ ] Request body includes per-field validation (type, required, constraints).
- [ ] Success responses include realistic example JSON (not placeholders).
- [ ] Pagination is present on all List endpoints.
- [ ] Custom actions use POST to a sub-resource — no verbs in URL paths.
- [ ] Error envelope structure is consistent across the entire API.
- [ ] Timestamps are in ISO 8601 UTC format.
- [ ] No ambiguity between 401 and 403 usage.
- [ ] Endpoint summary table is present at the end.
- [ ] Output descriptions and documentation are in the user's language.
- [ ] User is asked for permission to write the contract file to disk.
