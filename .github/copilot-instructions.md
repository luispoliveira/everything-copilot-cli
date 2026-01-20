# GitHub Copilot Instructions

## Overview

These are generic instructions for GitHub Copilot to follow when assisting with code generation and development tasks. Use these guidelines when no project-specific instructions are available.

## Development Principles

### Code Quality

- Prioritize security and performance
- Write clean, well-documented code
- Follow language/framework conventions and best practices
- Include robust error handling
- Prefer readability over cleverness
- Use meaningful variable and function names

### Testing

- Aim for minimum 80% code coverage
- Write unit tests and integration tests
- Test edge cases and error scenarios
- Keep tests maintainable and readable

### Git Workflow

- Use semantic commits (conventional commits format)
- Branch naming: `feature/*`, `bugfix/*`, `hotfix/*`
- Include detailed descriptions in pull requests
- Keep commits atomic and focused

### Security

- Never commit secrets or credentials
- Validate all user inputs
- Use HTTPS for external API calls
- Sanitize outputs to prevent injection attacks
- Follow the principle of least privilege

### Documentation

- Include README for each module
- Add comments for complex logic (explain WHY, not WHAT)
- Provide usage examples when applicable
- Keep documentation up to date with code changes

## Code Style Guidelines

### General

- Use consistent indentation (2 or 4 spaces)
- Avoid magic numbers - use named constants
- Keep functions small and focused (single responsibility)
- Limit nesting depth to 3 levels maximum
- Use early returns to reduce complexity

### Error Handling

- Always handle errors explicitly
- Provide meaningful error messages
- Never swallow errors silently
- Log errors with appropriate context

### Performance

- Avoid premature optimization
- Use appropriate data structures
- Cache expensive operations when beneficial
- Document performance-critical sections

## When Generating Code

1. Understand the context and requirements first
2. Follow existing project patterns if present
3. Write code that junior developers can understand
4. Include necessary error handling
5. Consider edge cases
6. Make the code testable
