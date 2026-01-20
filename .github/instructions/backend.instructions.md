---
applyTo: '**/*.{js,ts,py,go,java,rb,php}'
description: Backend development global standards
name: Backend Standards
---

# Global Backend Development Standards

## Architecture Patterns

- Clean Architecture
- Repository Pattern
- Dependency Injection
- SOLID Principles

## API Design

- RESTful conventions
- Versioning: `/api/v1/`
- Authentication: JWT or OAuth2
- Rate limiting mandatory
- OpenAPI/Swagger documentation

## Database

- Use migrations for schema changes
- Proper indexing
- Soft deletes preferred
- Transaction management
- Connection pooling

## Error Handling

```javascript
// Always use try-catch for async operations
try {
  const result = await operation();
  return result;
} catch (error) {
  logger.error('Operation failed', { error, context });
  throw new AppError('User-friendly message', error);
}
```

## Security Checklist

- [ ] Input validation
- [ ] Output sanitization
- [ ] Parameterized queries (no SQL injection)
- [ ] Authentication/Authorization
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Security headers
- [ ] Secrets in environment variables
