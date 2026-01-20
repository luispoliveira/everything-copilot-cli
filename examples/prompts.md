# Example Prompts for Copilot CLI

## Using Custom Agents

### Code Review

```bash
copilot
> Use the code-reviewer agent to review src/api/users.js
```

### Security Audit

```bash
copilot --agent=security-auditor --prompt "Audit this codebase for vulnerabilities"
```

### Generate Tests

```bash
copilot
> @test-generator create comprehensive tests for @src/utils/validation.js
```

## Using Skills

### Git Workflow

```bash
copilot
> Use the git-workflow skill to create a feature branch for user authentication
```

## Using Custom Instructions

Custom instructions are automatically loaded based on:

- Current directory
- File paths mentioned with `@`

```bash
copilot
> Explain @backend/server.js
# Uses .github/instructions/backend.instructions.md

copilot
> Create a React component for user profile
# Uses .github/instructions/frontend.instructions.md
```

## Delegation

```bash
copilot
> /delegate complete the API integration tests and fix any failing edge cases
```

## Context Management

```bash
copilot
> /usage      # View session stats
> /context    # View token usage
> /compact    # Compress history
```

## Adding Files

```bash
copilot
> Fix the bug in @src/app.js considering @tests/app.test.js
```

## Directory Management

```bash
copilot
> /add-dir /path/to/project
> /cwd /path/to/different/project
```
