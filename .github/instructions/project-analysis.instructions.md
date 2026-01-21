---
applyTo: '**/project-*.md'
description: Standards for project analysis and handover documentation
name: Project Analysis Standards
---

# Project Analysis Standards

## Purpose

These standards guide the analysis of projects during handover, ensuring comprehensive evaluation and actionable documentation.

## Analysis Principles

### Objectivity

- Base findings on evidence (code, configs, logs)
- Avoid assumptions without verification
- Distinguish between facts and opinions
- Reference specific files and line numbers

### Completeness

- Cover all analysis categories
- Check both obvious and hidden areas
- Look for what's missing, not just what's present
- Consider edge cases and error paths

### Actionability

- Every finding should have a recommendation
- Prioritize based on impact and effort
- Provide specific next steps
- Include estimated effort where possible

## Risk Assessment Matrix

### Priority Levels

| Level       | Criteria                                                      | Examples                                                 |
| ----------- | ------------------------------------------------------------- | -------------------------------------------------------- |
| 🔴 CRITICAL | Security vulnerabilities, data loss risk, production failures | Exposed secrets, SQL injection, no backups               |
| 🟠 HIGH     | Major blockers, significant tech debt, compliance issues      | Outdated framework with EOL, no tests for critical paths |
| 🟡 MEDIUM   | Quality issues, missing documentation, performance concerns   | Code duplication, missing API docs, N+1 queries          |
| 🟢 LOW      | Improvements, minor refactoring, nice-to-haves                | Naming conventions, minor optimizations                  |

### Impact Assessment

Consider these factors:

1. **Security Impact** - Can this be exploited?
2. **Data Impact** - Can this cause data loss/corruption?
3. **Availability Impact** - Can this cause downtime?
4. **Business Impact** - What's the cost to the business?
5. **Developer Impact** - How does this affect productivity?

## Scoring Guidelines

### Health Score (1-10)

| Score | Description                                   |
| ----- | --------------------------------------------- |
| 9-10  | Excellent - Production ready, well maintained |
| 7-8   | Good - Minor issues, maintainable             |
| 5-6   | Fair - Notable issues, needs attention        |
| 3-4   | Poor - Significant problems, risky            |
| 1-2   | Critical - Major overhaul needed              |

### Score Components

- **Architecture (20%)** - Design quality, patterns, scalability
- **Code Quality (20%)** - Readability, maintainability, standards
- **Security (20%)** - Vulnerabilities, best practices
- **Testing (15%)** - Coverage, quality, automation
- **Documentation (10%)** - Completeness, accuracy
- **DevOps (15%)** - CI/CD, deployment, monitoring

## Red Flags Checklist

### Immediate Concerns

- [ ] Hardcoded secrets/credentials
- [ ] No version control history (squashed/rebased away)
- [ ] No tests at all
- [ ] No README or setup documentation
- [ ] Deprecated/EOL dependencies with known CVEs
- [ ] No error handling in critical paths
- [ ] Database without migrations
- [ ] No environment separation (dev/staging/prod)

### Warning Signs

- [ ] Single contributor with no recent activity
- [ ] No CI/CD pipeline
- [ ] Outdated dependencies (2+ major versions behind)
- [ ] TODO comments older than 1 year
- [ ] No logging or monitoring
- [ ] Hardcoded configuration values
- [ ] No API documentation
- [ ] Inconsistent coding style

## Documentation Requirements

### Report Structure

1. **Executive Summary** - 2-3 paragraphs for stakeholders
2. **Technical Details** - For developers
3. **Risk Register** - Prioritized issues
4. **Onboarding Guide** - For new team members
5. **Recommendations** - Actionable roadmap

### File Naming

```
project-YYYY-MM-DD.md
```

Example: `project-2026-01-21.md`

### Location

Save in project root directory for visibility.

## Analysis Techniques

### Static Analysis

- Review file structure and organization
- Analyze dependency trees
- Check configuration files
- Examine code patterns and anti-patterns
- Count metrics (LOC, complexity, duplication)

### Dynamic Analysis

- Run existing tests
- Check build process
- Verify startup/shutdown
- Test error scenarios
- Profile performance if tools available

### Historical Analysis

- Review git history patterns
- Check commit frequency and contributors
- Look for force pushes or history rewrites
- Analyze issue/PR history if available
- Review changelog entries

## Common Blind Spots

### Often Missed

1. **Environment variables** - Missing documentation for required env vars
2. **Database state** - Migrations, seeds, required data
3. **External dependencies** - Third-party APIs, services
4. **Scheduled jobs** - Cron jobs, background workers
5. **File storage** - Local vs cloud, permissions
6. **Email/notifications** - Templates, providers, configs
7. **Feature flags** - Existing toggles, their states
8. **Rate limits** - External API limits, internal throttling

### Hidden Complexity

1. **Implicit dependencies** - Services that must be running
2. **Order dependencies** - Things that must happen in sequence
3. **Race conditions** - Timing-sensitive code
4. **Memory leaks** - Long-running process issues
5. **Connection pooling** - Database/cache connections

## Quality Checklist for Reports

Before finalizing a report:

- [ ] All sections completed
- [ ] Specific file/line references included
- [ ] Priorities assigned to all issues
- [ ] Recommendations are actionable
- [ ] Onboarding steps are testable
- [ ] Health score justified
- [ ] No assumptions without evidence
- [ ] Report is readable by non-technical stakeholders (executive summary)
