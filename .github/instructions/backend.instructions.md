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

## Design Patterns

### When to Use Design Patterns

Apply patterns **only when they solve a specific problem** — never apply patterns "just because". Premature abstraction is as harmful as premature optimisation. Prefer simple, direct code until complexity demands a pattern.

### Creational Patterns

| Pattern       | Use When                                                            | Avoid When                              |
| ------------- | ------------------------------------------------------------------- | --------------------------------------- |
| **Factory**   | Object creation logic is complex or needs to be centralised         | A simple constructor is sufficient      |
| **Builder**   | Objects require many optional parameters or multi-step construction | Objects have 3 or fewer required fields |
| **Singleton** | Managing shared resources (logging, config, connection pools)       | Can be replaced with DI container       |

**Example: Factory Pattern**

```typescript
// Use when you need to create different implementations based on context
interface NotificationService {
  send(message: string): Promise<void>;
}

class NotificationFactory {
  static create(type: 'email' | 'sms' | 'push'): NotificationService {
    switch (type) {
      case 'email':
        return new EmailNotificationService();
      case 'sms':
        return new SmsNotificationService();
      case 'push':
        return new PushNotificationService();
    }
  }
}
```

**Example: Builder Pattern**

```typescript
// Use when constructing complex objects with optional parameters
class QueryBuilder {
  private filters: Record<string, any> = {};
  private sorts: Array<[string, 'ASC' | 'DESC']> = [];
  private limit?: number;

  where(field: string, value: any): this {
    this.filters[field] = value;
    return this;
  }

  orderBy(field: string, direction: 'ASC' | 'DESC' = 'ASC'): this {
    this.sorts.push([field, direction]);
    return this;
  }

  take(limit: number): this {
    this.limit = limit;
    return this;
  }

  build(): Query {
    return new Query(this.filters, this.sorts, this.limit);
  }
}

// Usage
const query = new QueryBuilder()
  .where('status', 'active')
  .where('age', { $gte: 18 })
  .orderBy('createdAt', 'DESC')
  .take(10)
  .build();
```

### Structural Patterns

| Pattern       | Use When                                                                         | Avoid When                                  |
| ------------- | -------------------------------------------------------------------------------- | ------------------------------------------- |
| **Adapter**   | Integrating third-party libraries or legacy systems with incompatible interfaces | You control both sides of the interface     |
| **Decorator** | Adding responsibilities to objects dynamically without affecting other instances | Simple inheritance or composition is enough |
| **Facade**    | Simplifying complex subsystems behind a unified interface                        | The subsystem is already simple             |
| **Proxy**     | Controlling access, lazy loading, caching, or logging calls to objects           | Direct access is sufficient                 |

**Example: Adapter Pattern**

```typescript
// Use when wrapping third-party services with incompatible interfaces
interface PaymentProvider {
  processPayment(amount: number, currency: string): Promise<PaymentResult>;
}

class StripeAdapter implements PaymentProvider {
  constructor(private stripeClient: StripeSDK) {}

  async processPayment(
    amount: number,
    currency: string,
  ): Promise<PaymentResult> {
    // Adapt Stripe's API to our interface
    const charge = await this.stripeClient.charges.create({
      amount: amount * 100, // Stripe uses cents
      currency: currency.toLowerCase(),
    });
    return { success: charge.status === 'succeeded', transactionId: charge.id };
  }
}
```

**Example: Decorator Pattern**

```typescript
// Use when adding cross-cutting concerns (logging, caching, validation)
interface UserService {
  getUser(id: string): Promise<User>;
}

class CachedUserService implements UserService {
  constructor(
    private wrapped: UserService,
    private cache: Cache,
  ) {}

  async getUser(id: string): Promise<User> {
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return cached;

    const user = await this.wrapped.getUser(id);
    await this.cache.set(`user:${id}`, user, { ttl: 300 });
    return user;
  }
}

class LoggedUserService implements UserService {
  constructor(
    private wrapped: UserService,
    private logger: Logger,
  ) {}

  async getUser(id: string): Promise<User> {
    this.logger.info('Fetching user', { id });
    const user = await this.wrapped.getUser(id);
    this.logger.info('User fetched', { id, email: user.email });
    return user;
  }
}

// Usage: stack decorators
const service = new LoggedUserService(
  new CachedUserService(new UserService(), cache),
  logger,
);
```

### Behavioral Patterns

| Pattern                     | Use When                                                            | Avoid When                      |
| --------------------------- | ------------------------------------------------------------------- | ------------------------------- |
| **Strategy**                | Selection between multiple algorithms or behaviours at runtime      | Only one algorithm exists       |
| **Observer**                | Multiple objects need to react to state changes in another object   | Simple callbacks are sufficient |
| **Command**                 | Encapsulating requests as objects (queues, undo/redo, transactions) | Direct method calls are clearer |
| **Chain of Responsibility** | Multiple handlers can process a request, with dynamic ordering      | Only one handler exists         |
| **Template Method**         | Defining the skeleton of an algorithm with subclass-specific steps  | The algorithm has no variation  |

**Example: Strategy Pattern**

```typescript
// Use when you need to switch between algorithms at runtime
interface PricingStrategy {
  calculatePrice(basePrice: number): number;
}

class RegularPricing implements PricingStrategy {
  calculatePrice(basePrice: number): number {
    return basePrice;
  }
}

class SeasonalDiscountPricing implements PricingStrategy {
  constructor(private discountPercent: number) {}

  calculatePrice(basePrice: number): number {
    return basePrice * (1 - this.discountPercent / 100);
  }
}

class VIPPricing implements PricingStrategy {
  calculatePrice(basePrice: number): number {
    return basePrice * 0.8; // 20% discount for VIP
  }
}

class PriceCalculator {
  constructor(private strategy: PricingStrategy) {}

  setStrategy(strategy: PricingStrategy): void {
    this.strategy = strategy;
  }

  calculate(basePrice: number): number {
    return this.strategy.calculatePrice(basePrice);
  }
}
```

**Example: Chain of Responsibility Pattern**

```typescript
// Use when building middleware pipelines or validation chains
abstract class ValidationHandler {
  protected next?: ValidationHandler;

  setNext(handler: ValidationHandler): ValidationHandler {
    this.next = handler;
    return handler;
  }

  async validate(data: any): Promise<void> {
    await this.check(data);
    if (this.next) {
      await this.next.validate(data);
    }
  }

  protected abstract check(data: any): Promise<void>;
}

class RequiredFieldsValidator extends ValidationHandler {
  constructor(private fields: string[]) {
    super();
  }

  protected async check(data: any): Promise<void> {
    for (const field of this.fields) {
      if (!data[field]) {
        throw new ValidationError(`Field ${field} is required`);
      }
    }
  }
}

class EmailFormatValidator extends ValidationHandler {
  protected async check(data: any): Promise<void> {
    if (data.email && !this.isValidEmail(data.email)) {
      throw new ValidationError('Invalid email format');
    }
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}

// Usage
const validator = new RequiredFieldsValidator(['name', 'email']);
validator.setNext(new EmailFormatValidator()).setNext(new AgeValidator());

await validator.validate(userData);
```

### Pattern Selection Guide

1. **Need to create objects?** → Creational patterns (Factory, Builder)
2. **Need to wrap or adapt existing code?** → Structural patterns (Adapter, Decorator, Facade, Proxy)
3. **Need to change behaviour at runtime?** → Behavioral patterns (Strategy, Command, Chain of Responsibility)
4. **Need objects to communicate?** → Observer, Mediator
5. **Still unsure?** → Don't use a pattern — keep it simple

### Anti-Patterns to Avoid

- **God Object** — classes that know or do too much; violates Single Responsibility Principle
- **Anemic Domain Model** — domain objects with no behaviour, only getters/setters
- **Leaky Abstraction** — abstractions that expose implementation details
- **Golden Hammer** — using the same pattern everywhere regardless of fit
- **Over-engineering** — applying patterns when simple code would suffice

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
