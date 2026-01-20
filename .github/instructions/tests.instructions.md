---
applyTo: '**/*.{test,spec}.{js,ts,jsx,tsx}'
description: Testing global standards
name: Testing Standards
---

# Global Testing Standards

## Framework

- Jest or Vitest for unit/integration
- Testing Library for React/Vue
- Playwright or Cypress for E2E

## Structure (AAA Pattern)

```javascript
describe('FeatureName', () => {
  // Setup
  beforeEach(() => {
    // Reset state, mocks, etc.
  });

  describe('when [condition]', () => {
    it('should [expected behavior]', () => {
      // Arrange - Setup test data
      const input = createTestData();

      // Act - Execute the code
      const result = functionUnderTest(input);

      // Assert - Verify expectations
      expect(result).toBe(expected);
    });
  });

  describe('edge cases', () => {
    it('should handle null gracefully', () => {
      expect(() => fn(null)).toThrow(ValidationError);
    });

    it('should handle empty array', () => {
      expect(fn([])).toEqual([]);
    });
  });
});
```

## Coverage Requirements

- Overall: 80% minimum
- Critical paths: 100%
- Branches: 80%
- Functions: 80%

## Best Practices

- One assertion per test (when possible)
- Descriptive test names
- Avoid implementation details
- Mock external dependencies only
- Fast execution (unit tests < 100ms)
