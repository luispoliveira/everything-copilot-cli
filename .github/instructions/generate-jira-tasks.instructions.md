# Rule: Generating Jira Tasks from a PRD

## Goal

To guide in creating a detailed, structured Jira-ready task list in Markdown format based on an existing Product Requirements Document (PRD). The output should be ready for import or manual creation in Jira, containing Epics, Stories, Tasks, and Sub-tasks with estimates, tags, priorities, and descriptions.

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `jira-[prd-file-name].md` (e.g., `jira-0001-prd-user-profile-editing.md`)

## Process

1. **Receive PRD Reference:** The user points the AI to a specific PRD file.
2. **Analyze PRD:** The AI reads and analyzes the functional requirements, user stories, acceptance criteria, and other sections of the specified PRD.
3. **Assess Current State:** Review the existing codebase to understand existing infrastructure, architectural patterns, and conventions. Identify any existing components or features that could be relevant to the PRD requirements.
4. **Phase 1: Generate Epics:** Based on the PRD analysis, create the file and generate the Epic(s) required to encompass the feature. Present these Epics to the user. Inform the user: "I have generated the Epic(s) based on the PRD. Ready to generate Stories and Tasks? Respond with 'Go' to proceed."
5. **Wait for Confirmation:** Pause and wait for the user to respond with "Go".
6. **Phase 2: Generate Stories, Tasks & Sub-tasks:** Once the user confirms, break down each Epic into Stories (user-facing) and/or Tasks (technical). Stories and Tasks are direct children of Epics. Add Sub-tasks to Stories or Tasks as needed (Sub-tasks are the only valid children of Stories/Tasks).
7. **Apply Estimates & Metadata:** Add story points, priorities, tags, and detailed descriptions to each item.
8. **Generate Final Output:** Combine all items into the final Markdown structure following the output format below.
9. **Save Task List:** Save the generated document in the `/tasks/` directory with the filename `jira-[prd-file-name].md`.

> **Hierarchy Reminder:** Jira only supports Epic → Story → Sub-task OR Epic → Task → Sub-task. Never create Tasks as children of Stories.

## Story Points Scale

Use the Fibonacci sequence for estimation:

| Points | Complexity   | Time Estimate | Description                                  |
| ------ | ------------ | ------------- | -------------------------------------------- |
| 1      | Trivial      | < 2 hours     | Simple config change, copy update, minor fix |
| 2      | Simple       | 2-4 hours     | Small feature, single file change            |
| 3      | Medium       | 4-8 hours     | Standard feature, multiple files             |
| 5      | Complex      | 1-2 days      | Multiple components, requires testing        |
| 8      | Very Complex | 2-4 days      | Large feature, multiple integrations         |
| 13     | Epic-level   | 1 week+       | Major feature, should be broken down further |

## Priority Levels

| Priority    | Description                                           |
| ----------- | ----------------------------------------------------- |
| **Highest** | Blocker - Must be done immediately, blocks other work |
| **High**    | Critical path - Required for core functionality       |
| **Medium**  | Standard priority - Important but not blocking        |
| **Low**     | Nice to have - Can be deferred if needed              |
| **Lowest**  | Optional - Enhancement for future consideration       |

## Tags/Labels

Use consistent tags for categorization:

- `backend` - Backend/API work
- `frontend` - Frontend/UI work
- `database` - Database changes/migrations
- `infrastructure` - DevOps/Infrastructure changes
- `security` - Security-related work
- `testing` - Testing-focused tasks
- `documentation` - Documentation updates
- `refactoring` - Code refactoring
- `bugfix` - Bug fixes
- `feature` - New feature development
- `integration` - Third-party integrations
- `performance` - Performance optimization

## Output Format

The generated Jira task list _must_ follow this structure:

```markdown
# Jira Tasks: [Feature Name]

> Generated from PRD: `[prd-filename].md`
> Date: [Generation Date]

---

## Summary

| Type                   | Count |
| ---------------------- | ----- |
| Epics                  | X     |
| Stories                | X     |
| Tasks                  | X     |
| Sub-tasks              | X     |
| **Total Story Points** | X     |

---

## Epic 1: [Epic Title]

**Type:** Epic
**Priority:** [Highest/High/Medium/Low/Lowest]
**Tags:** `tag1`, `tag2`
**Description:**

> [Detailed description of the epic, including the business value and high-level scope]

**Acceptance Criteria:**

- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

### Story 1.1: [Story Title]

**Type:** Story
**Parent:** Epic 1
**Priority:** [Priority]
**Story Points:** [1/2/3/5/8/13]
**Tags:** `tag1`, `tag2`

**Description:**

> As a [user type], I want [functionality] so that [benefit].

**Acceptance Criteria:**

- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Technical Notes:**

- [Any technical considerations or implementation hints]

---

#### Sub-task 1.1.1: [Sub-task Title]

**Type:** Sub-task
**Parent:** Story 1.1
**Priority:** [Priority]
**Story Points:** [1/2/3]
**Tags:** `tag1`, `tag2`
**Assignee:** [Optional - Team/Role]

**Description:**

> [Brief description of the sub-task]

**Implementation Details:**

- [Step 1]
- [Step 2]

**Affected Files:**

- `path/to/file1.ts` - [Brief description]
- `path/to/file2.ts` - [Brief description]

---

### Task 1.2: [Task Title] (Technical Work)

**Type:** Task
**Parent:** Epic 1
**Priority:** [Priority]
**Story Points:** [1/2/3/5/8]
**Tags:** `tag1`, `tag2`
**Assignee:** [Optional - Team/Role]

**Description:**

> [Detailed description of what needs to be done - technical work not user-facing]

**Implementation Details:**

- [Step 1]
- [Step 2]

**Affected Files:**

- `path/to/file1.ts` - [Brief description]
- `path/to/file2.ts` - [Brief description]

---

#### Sub-task 1.2.1: [Sub-task Title]

**Type:** Sub-task
**Parent:** Task 1.2
**Priority:** [Priority]
**Story Points:** [1/2/3]
**Tags:** `tag1`

**Description:**

> [Brief description of the sub-task]

---

## Dependencies

| Item       | Depends On | Type       |
| ---------- | ---------- | ---------- |
| Story 1.2  | Story 1.1  | Blocks     |
| Task 2.1.1 | Task 1.1.1 | Relates to |

---

## Risk Assessment

| Risk               | Impact          | Mitigation            |
| ------------------ | --------------- | --------------------- |
| [Risk description] | High/Medium/Low | [Mitigation strategy] |

---

## Notes for Jira Import

- Create Epics first, then Stories, then Tasks, then Sub-tasks
- Link dependencies after all items are created
- Adjust story points after team refinement session
- Tags should be created in Jira before import if they don't exist
```

## Issue Type Hierarchy

Jira supports two valid parent-child hierarchies:

```
Option A (User-facing work):
Epic
└── Story
    └── Sub-task

Option B (Technical work):
Epic
└── Task
    └── Sub-task
```

> **Important:** Jira does NOT support Epic -> Story -> Task -> Sub-task. Stories and Tasks are both direct children of Epics and cannot be nested within each other.

- **Epic:** Large body of work that can be broken down into smaller pieces. Represents a feature or major initiative.
- **Story:** User-facing functionality described from the user's perspective. Delivers value to the end user. Direct child of Epic.
- **Task:** Technical work that may not be user-facing. Direct child of Epic. Use when work is purely technical.
- **Sub-task:** Smallest unit of work. Can be a child of either Story or Task. Specific, actionable items that can be completed in a few hours.

### When to Use Story vs Task

| Use **Story** when...                      | Use **Task** when...                       |
| ------------------------------------------ | ------------------------------------------ |
| Work delivers user-facing value            | Work is purely technical                   |
| Can be described as "As a user, I want..." | Infrastructure, refactoring, or setup work |
| End user will notice the change            | No direct user impact                      |
| Feature or functionality                   | DevOps, documentation, or maintenance      |

## Interaction Model

The process explicitly requires a pause after generating Epics to get user confirmation ("Go") before proceeding to generate the detailed Stories, Tasks, and Sub-tasks. This ensures the high-level structure aligns with expectations before diving into details.

## Best Practices

1. **Epics** should represent complete features or major initiatives
2. **Stories** should be completable within a single sprint (user-facing work, direct child of Epic)
3. **Tasks** should be completable within 1-2 days (technical work, direct child of Epic)
4. **Sub-tasks** should be completable within a few hours (child of Story OR Task)
5. Use **Stories** for user-facing functionality, **Tasks** for technical/infrastructure work
6. Each item should have clear acceptance criteria
7. Dependencies should be explicitly documented
8. Story points should reflect complexity, not just time
9. Descriptions should be detailed enough for any team member to understand
10. Never create Tasks as children of Stories - use Sub-tasks instead

## Target Audience

Assume the primary reader is a **Product Owner or Scrum Master** who will create and manage these items in Jira, and **developers** who will implement them.
