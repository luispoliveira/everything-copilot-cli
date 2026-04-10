---
applyTo: '**/*.{js,ts,py,go,java,rb,php}'
description: Backend development global standards
name: Backend Standards
---

# Global Backend Development Standards

## Core Principles

Apply these in order of priority:

| #   | Principle              | Rule                                                                    |
| --- | ---------------------- | ----------------------------------------------------------------------- |
| 1   | **Security first**     | Validate inputs, sanitise outputs, enforce auth, never expose internals |
| 2   | **SOLID**              | Single responsibility, open/closed, Liskov, interface segregation, DI   |
| 3   | **Clean Architecture** | Separate domain, application, infrastructure, and presentation layers   |
| 4   | **DRY**                | Never duplicate logic — extract to shared services or utilities         |
| 5   | **KISS**               | Choose the simplest solution that works; no over-engineering            |
| 6   | **YAGNI**              | Do not add code for hypothetical future requirements                    |

## Architecture Patterns

- **Clean Architecture** — domain logic must not depend on frameworks or infrastructure
- **Repository Pattern** — abstract all data access behind interfaces; never query DB directly in controllers
- **Dependency Injection** — always inject dependencies; never instantiate services manually with `new`
- **Service Layer** — controllers are thin; all business logic lives in services
- **SOLID Principles** — every class has one reason to change; depend on abstractions, not concretions

## API Design

- Follow **RESTful conventions**: nouns for resources, HTTP verbs for actions
- **Versioning**: prefix all routes with `/api/v1/` — never break existing clients
- **Authentication**: JWT (Bearer token) or OAuth2 — no session-based auth for APIs
- **Request validation**: validate and reject invalid payloads before any business logic
- **Response envelope**: consistent structure — `{ data, meta, errors }`
- **HTTP status codes**: use them correctly — `200`, `201`, `204`, `400`, `401`, `403`, `404`, `409`, `422`, `500`
- **Rate limiting**: mandatory on all public endpoints — return `429 Too Many Requests`
- **Pagination**: cursor-based preferred for large datasets; always include `meta.total`, `meta.page`, `meta.perPage`
- **OpenAPI/Swagger**: document every endpoint — request body, parameters, responses, auth scheme

## Code Structure

```
src/
  common/           # Shared utilities, base classes, guards, filters
  config/           # Environment config and validation
  modules/
    <feature>/
      <feature>.controller.{ts,php,py}   # HTTP layer only
      <feature>.service.{ts,php,py}      # Business logic
      <feature>.repository.{ts,php,py}   # Data access
      dto/                               # Request/response shapes
      interfaces/                        # Contracts / abstractions
      <feature>.spec.{ts,php,py}         # Tests alongside source
```

## Database

- **Migrations**: all schema changes via migration files — never modify the DB schema manually
- **Proper indexing**: index foreign keys, columns used in `WHERE`, `ORDER BY`, and `JOIN`
- **Soft deletes**: preferred over hard deletes — use `deleted_at` timestamp pattern
- **Transaction management**: wrap multi-step writes in transactions; rollback on failure
- **Connection pooling**: configure pool size appropriate to the runtime and DB server limits
- **Parameterised queries**: never concatenate user input into SQL strings
- **No `SELECT *`**: always specify required columns to avoid over-fetching

## Error Handling

- Always handle errors explicitly — never swallow them silently
- Log errors with structured context (operation name, entity ID, user ID, stack trace)
- Never expose internal error details (stack traces, query errors) to clients in production
- Map domain exceptions to appropriate HTTP status codes in a centralised error handler
- Use meaningful, user-friendly error messages in responses

```typescript
// Example pattern (adapt to your language/framework)
try {
  const result = await someOperation(id);
  return result;
} catch (error) {
  logger.error('Operation failed', { error, operation: 'someOperation', id });
  throw new AppError(
    'Could not complete the request. Please try again.',
    error,
  );
}
```

## Logging

- Use **structured JSON logging** — never plain `console.log` or `print` in production code
- Include a **correlation ID** on every request — propagate it to all log entries and downstream calls
- Log levels: `debug` (dev only), `info` (significant events), `warn` (recoverable issues), `error` (failures requiring attention)
- Never log secrets, passwords, tokens, or PII

## Security Checklist

Run through this before every PR/feature completion:

- [ ] All user inputs validated and sanitised before use
- [ ] Output sanitised — no raw user data rendered or returned without encoding
- [ ] Parameterised queries used everywhere — no SQL/NoSQL injection risk
- [ ] Authentication enforced on all non-public endpoints
- [ ] Authorisation checks — users can only access their own or permitted resources
- [ ] Rate limiting configured on all public and auth endpoints
- [ ] CORS configured with an explicit allow-list — no wildcard `*` in production
- [ ] Security headers set (`Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`)
- [ ] All secrets and credentials sourced from environment variables — nothing hardcoded
- [ ] Dependencies up to date — no known CVEs in production packages
- [ ] Error responses do not leak stack traces, query details, or internal paths

## Testing Requirements

- Minimum **80% code coverage** across the module
- **Unit tests**: test services and domain logic in isolation with mocked dependencies
- **Integration tests**: test repository layer against a real (or in-memory) database
- **E2E / API tests**: test full HTTP request/response cycle for every endpoint
- Test: happy path, validation errors, auth failures, not-found, and edge cases
- Tests must be independent — no shared mutable state between test cases

## Performance

- Avoid N+1 queries — use eager loading or batch queries
- Cache expensive or frequently read data — document cache TTL and invalidation strategy
- Set timeouts on all external service calls
- Use async/non-blocking I/O wherever the runtime supports it
- Document any performance-critical sections with a comment explaining the approach
