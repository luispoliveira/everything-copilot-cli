---
applyTo: '**/*.{js,ts,py,go,java,php}'
description: Security best practices
name: Security Standards
---

# Global Security Standards

## OWASP Top 10 Compliance

### 1. Broken Access Control

```javascript
// Always check authorization
const canAccess = await checkUserPermission(userId, resourceId, 'read');
if (!canAccess) {
  throw new UnauthorizedError('Access denied');
}
```

### 2. Cryptographic Failures

```javascript
// Use bcrypt for passwords
const hashedPassword = await bcrypt.hash(password, 12);

// Use TLS for all connections
const options = {
  secure: true,
  rejectUnauthorized: true,
};
```

### 3. Injection Prevention

```javascript
// NEVER do this
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ALWAYS use parameterized queries
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

### 4. Input Validation

```javascript
// Validate and sanitize all inputs
const schema = z.object({
  email: z.string().email(),
  age: z.number().int().positive().max(120),
});

const validated = schema.parse(input);
```

## Secrets Management

- NEVER commit secrets to Git
- Use environment variables
- Rotate secrets regularly
- Use secret management tools (HashiCorp Vault, AWS Secrets Manager)

## Security Headers

```javascript
// Express.js example
app.use(
  helmet({
    contentSecurityPolicy: true,
    hsts: true,
    noSniff: true,
    xssFilter: true,
  }),
);
```
