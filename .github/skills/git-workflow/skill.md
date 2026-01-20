---
name: git-workflow
description: Automated git workflows and best practices
---

# Git Workflow Skill

Automation for common git operations following best practices.

## Capabilities

1. **Smart Commits**
   - Generate conventional commit messages
   - Validate commit message format
   - Auto-link to issues

2. **Branch Management**
   - Create properly named branches
   - Keep branches up to date
   - Clean up merged branches

3. **PR Automation**
   - Generate PR descriptions
   - Add labels based on changes
   - Request appropriate reviewers

## Scripts Available

- `./scripts/smart-commit.sh` - Interactive commit helper
- `./scripts/sync-branch.sh` - Sync with main/develop
- `./scripts/cleanup-branches.sh` - Remove merged branches
- `./scripts/pr-description.sh` - Generate PR template
