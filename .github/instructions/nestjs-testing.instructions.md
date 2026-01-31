# NestJS Testing Standards

## Overview

This document defines the testing standards for NestJS applications. Follow these guidelines to ensure consistent, maintainable, and comprehensive test coverage.

## Testing Framework

- **Primary Framework**: Jest (NestJS default)
- **Testing Utilities**: `@nestjs/testing`
- **Mocking**: Jest native mocks + `@golevelup/ts-jest` for advanced scenarios
- **Coverage Target**: Minimum 80%

## Test File Structure

### Unit Tests

- **Location**: Same directory as source file
- **Naming**: `*.spec.ts` (e.g., `user.service.spec.ts`)
- **Scope**: Single class/function in isolation

### Integration Tests

- **Location**: Same directory as source file OR `test/integration/`
- **Naming**: `*.integration.spec.ts`
- **Scope**: Module with real dependencies (mocked external services)

### E2E Tests

- **Location**: `test/` directory at project root
- **Naming**: `*.e2e-spec.ts`
- **Scope**: Full API endpoint testing

## Directory Structure

```
src/
├── users/
│   ├── users.controller.ts
│   ├── users.controller.spec.ts      # Unit test
│   ├── users.service.ts
│   ├── users.service.spec.ts         # Unit test
│   ├── users.service.integration.spec.ts  # Integration test
│   └── dto/
│       ├── create-user.dto.ts
│       └── create-user.dto.spec.ts   # DTO validation test
test/
├── users.e2e-spec.ts                 # E2E test
├── auth.e2e-spec.ts
├── jest-e2e.json
└── setup/
    ├── test-database.ts
    └── test-app.ts
```

## Test Documentation Standards

Every test file MUST include:

1. **File Header**: Describe what is being tested
2. **Test Groups**: Use `describe()` blocks logically
3. **Descriptive Test Names**: Use BDD-style naming
4. **Inline Comments**: Explain complex setup or assertions

### Example Structure

```typescript
/**
 * Unit tests for UsersService
 *
 * Tests cover:
 * - User creation and validation
 * - User retrieval (single and list)
 * - User update operations
 * - User deletion (soft delete)
 *
 * @see UsersService
 */
describe('UsersService', () => {
  // Arrange: Common setup
  let service: UsersService;
  let prisma: DeepMockProxy<PrismaClient>;

  beforeEach(async () => {
    // Setup test module with mocked dependencies
  });

  describe('create()', () => {
    it('should create a user with valid data', async () => {
      // Arrange
      // Act
      // Assert
    });

    it('should throw ConflictException when email already exists', async () => {
      // Test error scenarios
    });
  });
});
```

## Mocking Standards

### Prisma/ZenStack Mocking

Use `jest-mock-extended` for type-safe mocks:

```typescript
import { DeepMockProxy, mockDeep } from 'jest-mock-extended';
import { PrismaClient } from '@prisma/client';

describe('Service with Prisma', () => {
  let prisma: DeepMockProxy<PrismaClient>;

  beforeEach(() => {
    prisma = mockDeep<PrismaClient>();
  });
});
```

### NestJS Service Mocking

```typescript
const mockUsersService = {
  findOne: jest.fn(),
  create: jest.fn(),
  update: jest.fn(),
  remove: jest.fn(),
};

const module = await Test.createTestingModule({
  controllers: [UsersController],
  providers: [
    {
      provide: UsersService,
      useValue: mockUsersService,
    },
  ],
}).compile();
```

### Using @golevelup/ts-jest

```typescript
import { createMock } from '@golevelup/ts-jest';

const mockService = createMock<UsersService>();
```

## Authentication Testing

### JWT/Passport Setup

```typescript
// test/setup/auth.helper.ts
export const createTestToken = (userId: string, roles: string[] = ['user']) => {
  return jwt.sign(
    { sub: userId, roles },
    process.env.JWT_SECRET || 'test-secret',
    { expiresIn: '1h' },
  );
};

// In E2E tests
it('should access protected route with valid token', () => {
  const token = createTestToken('user-1', ['admin']);

  return request(app.getHttpServer())
    .get('/users/me')
    .set('Authorization', `Bearer ${token}`)
    .expect(200);
});
```

### Better-Auth Setup

```typescript
// test/setup/better-auth.helper.ts
export const mockBetterAuthSession = (userId: string) => {
  return {
    user: { id: userId, email: 'test@example.com' },
    session: { id: 'session-id', expiresAt: new Date() },
  };
};
```

## DTO Validation Testing

```typescript
import { validate } from 'class-validator';
import { plainToInstance } from 'class-transformer';

describe('CreateUserDto', () => {
  it('should fail validation with invalid email', async () => {
    const dto = plainToInstance(CreateUserDto, {
      email: 'invalid-email',
      password: 'ValidPass123!',
    });

    const errors = await validate(dto);

    expect(errors.length).toBeGreaterThan(0);
    expect(errors[0].property).toBe('email');
  });
});
```

## Database Testing Strategies

### Strategy 1: In-Memory (SQLite)

Best for: Fast unit/integration tests

```typescript
// prisma/schema.prisma - use sqlite for tests
datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}
```

### Strategy 2: Test Containers

Best for: Production-like integration tests

```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';

let container: StartedPostgreSqlContainer;

beforeAll(async () => {
  container = await new PostgreSqlContainer().start();
  process.env.DATABASE_URL = container.getConnectionUri();
});

afterAll(async () => {
  await container.stop();
});
```

### Strategy 3: Transaction Rollback

Best for: E2E tests with real database

```typescript
beforeEach(async () => {
  await prisma.$executeRaw`BEGIN`;
});

afterEach(async () => {
  await prisma.$executeRaw`ROLLBACK`;
});
```

## Test Data Factories

Use factories for consistent test data:

```typescript
// test/factories/user.factory.ts
import { faker } from '@faker-js/faker';

export const createUserData = (overrides: Partial<CreateUserDto> = {}) => ({
  email: faker.internet.email(),
  password: 'ValidPass123!',
  name: faker.person.fullName(),
  ...overrides,
});

export const createUserEntity = (overrides: Partial<User> = {}): User => ({
  id: faker.string.uuid(),
  email: faker.internet.email(),
  name: faker.person.fullName(),
  createdAt: new Date(),
  updatedAt: new Date(),
  ...overrides,
});
```

## Coverage Configuration

### jest.config.js

```javascript
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.module.ts',
    '!src/**/*.dto.ts',
    '!src/**/*.entity.ts',
    '!src/main.ts',
    '!src/**/*.spec.ts',
  ],
};
```

## Common Patterns

### Testing Guards

```typescript
describe('JwtAuthGuard', () => {
  it('should allow access with valid token', async () => {
    const context = createMock<ExecutionContext>();
    context.switchToHttp().getRequest.mockReturnValue({
      headers: { authorization: 'Bearer valid-token' },
    });

    const result = await guard.canActivate(context);
    expect(result).toBe(true);
  });
});
```

### Testing Interceptors

```typescript
describe('TransformInterceptor', () => {
  it('should wrap response in data object', async () => {
    const interceptor = new TransformInterceptor();
    const context = createMock<ExecutionContext>();
    const next = { handle: () => of({ id: 1 }) };

    const result = await lastValueFrom(interceptor.intercept(context, next));
    expect(result).toEqual({ data: { id: 1 } });
  });
});
```

### Testing Pipes

```typescript
describe('ParseUUIDPipe', () => {
  it('should throw BadRequestException for invalid UUID', () => {
    const pipe = new ParseUUIDPipe();

    expect(() => pipe.transform('invalid', { type: 'param' })).toThrow(
      BadRequestException,
    );
  });
});
```

## Commands Reference

```bash
# Run all tests
npm run test

# Run with coverage
npm run test:cov

# Run E2E tests
npm run test:e2e

# Run specific test file
npm run test -- users.service.spec.ts

# Run tests in watch mode
npm run test:watch

# Run tests matching pattern
npm run test -- --testNamePattern="should create"

# Debug tests
npm run test:debug
```

## Guardrails

### ✅ DO

- Use AAA pattern (Arrange, Act, Assert)
- Test one behavior per test
- Use descriptive test names
- Mock external dependencies
- Clean up after tests
- Test error scenarios

### ❌ DON'T

- Share state between tests
- Test implementation details
- Use hardcoded timeouts
- Skip error handling tests
- Leave console.logs in tests
- Test private methods directly
