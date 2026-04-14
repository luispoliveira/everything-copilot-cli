# Obsidian Vault Standards

This document defines the conventions, templates, and rules for structuring an Obsidian vault using the Second Brain / PARA methodology.

---

## 1. Folder Structure (PARA)

The vault MUST follow this top-level structure. No other top-level folders should be created.

```
📁 00 - Inbox/
📁 01 - Projects/
📁 02 - Areas/
📁 03 - Resources/
📁 04 - Archives/
📁 Daily Notes/
📁 Templates/
📄 🏠 HOME.md
📄 📥 Inbox.md
```

### Folder Rules

- `00 - Inbox/` — Temporary landing zone. Files here have not yet been processed.
- `01 - Projects/` — One subfolder per active project. Each must contain a Project MOC note.
- `02 - Areas/` — One subfolder per area of responsibility.
- `03 - Resources/` — One subfolder per topic or interest.
- `04 - Archives/` — Mirrors the PARA structure (`Archives/Projects/`, `Archives/Areas/`, `Archives/Resources/`).
- `Daily Notes/` — Auto-created daily notes. Format: `YYYY-MM-DD.md`.
- `Templates/` — Reusable templates. Never edit inline; always duplicate.

---

## 2. File Naming Conventions

| Type         | Convention                 | Example                   |
| ------------ | -------------------------- | ------------------------- |
| Regular note | Title Case, spaces allowed | `My Note About Topic.md`  |
| Daily note   | ISO date                   | `2026-04-14.md`           |
| MOC note     | Append ` MOC` suffix       | `Web Development MOC.md`  |
| Project note | Project name + ` MOC`      | `Launch Portfolio MOC.md` |
| Template     | Prefix `TPL - `            | `TPL - Daily Note.md`     |

### Rules

- No special characters in filenames except hyphens and spaces.
- No underscores — use spaces.
- Do NOT include dates in non-daily note filenames (e.g. avoid `2026-Note.md`).

---

## 3. Frontmatter (YAML Metadata)

Every non-template note MUST include YAML frontmatter.

### Standard Frontmatter

```yaml
---
created: YYYY-MM-DD
modified: YYYY-MM-DD
tags: []
type: note
status: active
---
```

### Field Definitions

| Field      | Required | Allowed Values                                           |
| ---------- | -------- | -------------------------------------------------------- |
| `created`  | Yes      | ISO date `YYYY-MM-DD`                                    |
| `modified` | Yes      | ISO date `YYYY-MM-DD` — update on every significant edit |
| `tags`     | Yes      | See Tag Taxonomy section                                 |
| `type`     | Yes      | `note`, `moc`, `project`, `area`, `resource`, `daily`    |
| `status`   | Yes      | `active`, `done`, `someday`, `archived`                  |
| `source`   | No       | URL or book title (for literature notes)                 |
| `author`   | No       | Original author (for literature notes)                   |

---

## 4. Tag Taxonomy

Tags describe **cross-cutting attributes**. Folders handle location; tags handle categorization.

```
Type tags:      #type/note  #type/moc  #type/project  #type/area  #type/resource  #type/daily
Status tags:    #status/active  #status/done  #status/someday  #status/archived
Source tags:    #source/book  #source/article  #source/video  #source/podcast  #source/course
Area tags:      Use based on user's actual areas (e.g. #area/health  #area/finance  #area/career)
```

### Rules

- Use hierarchical tags with `/` separator (supported natively in Obsidian).
- Do NOT replicate folder structure with tags (e.g. don't tag `#projects/my-project`).
- Maximum 5 tags per note to avoid tag bloat.

---

## 5. Note Templates

### 5.1 Daily Note (`TPL - Daily Note.md`)

```markdown
---
created: { { date:YYYY-MM-DD } }
modified: { { date:YYYY-MM-DD } }
tags: [type/daily]
type: daily
status: active
---

# 📅 {{date:dddd, MMMM D, YYYY}}

## 🌅 Morning Check-in

- [ ] Top priority today:

## 📥 Captures

_Anything to note: ideas, links, quotes, tasks._

-

## ✅ Done Today

## 🔗 Links & References

## 🌙 Evening Reflection

> _One thing I learned today:_
```

### 5.2 Project MOC (`TPL - Project MOC.md`)

```markdown
---
created: { { date:YYYY-MM-DD } }
modified: { { date:YYYY-MM-DD } }
tags: [type/project, status/active]
type: project
status: active
---

# 🚀 [Project Name]

> **Goal:** _One sentence describing the desired outcome._
> **Deadline:** YYYY-MM-DD
> **Status:** 🟢 Active | 🟡 On Hold | ✅ Done

## 📋 Next Actions

- [ ]

## 🗒️ Notes & Decisions

-

## 🔗 Related Notes

-

## 📜 Log

| Date       | Update          |
| ---------- | --------------- |
| YYYY-MM-DD | Project started |
```

### 5.3 Area Note (`TPL - Area.md`)

```markdown
---
created: { { date:YYYY-MM-DD } }
modified: { { date:YYYY-MM-DD } }
tags: [type/area, status/active]
type: area
status: active
---

# 🏛️ [Area Name]

> **Standard to maintain:** _What does "good" look like in this area?_

## 🎯 Current Goals

-

## 📌 Key Notes

- [[]]

## 🔗 Related Projects

- [[]]

## 📚 Resources

- [[]]
```

### 5.4 Literature Note (`TPL - Literature Note.md`)

```markdown
---
created: { { date:YYYY-MM-DD } }
modified: { { date:YYYY-MM-DD } }
tags: [type/resource, source/book]
type: resource
status: active
source:
author:
---

# 📖 [Book/Article Title]

**Author:**
**Source:**

## ⭐ Key Ideas

1.

## 💬 Notable Quotes

>

## 🔗 Connections

_How does this relate to what I already know?_

-

## 💡 My Takeaways
```

### 5.5 MOC Note (`TPL - MOC.md`)

```markdown
---
created: { { date:YYYY-MM-DD } }
modified: { { date:YYYY-MM-DD } }
tags: [type/moc, status/active]
type: moc
status: active
---

# 🗺️ [Topic] MOC

> _One-sentence description._

## 🔗 Key Notes

- [[]]

## 📂 Sub-Topics

- [[]]

## 📚 Sources

- [[]]

## 💡 Synthesis

_My current understanding of this topic._
```

---

## 6. HOME Dashboard (`🏠 HOME.md`)

The `HOME.md` file is the vault's entry point. It must:

- Be in the vault root (not in any subfolder)
- Link to all active projects, area MOCs, and key resources
- Include a direct link to `Inbox.md` and today's daily note
- Never be archived

### Structure

```markdown
# 🏠 Home

> _Last updated: YYYY-MM-DD_

## 🚀 Active Projects

- [[01 - Projects/...]]

## 🌱 Areas

- [[02 - Areas/...]]

## 📚 Resource MOCs

- [[03 - Resources/...]]

## 📥 Inbox

[[Inbox]] — Process regularly!

## 📅 Today

[[Daily Notes/YYYY-MM-DD]]
```

---

## 7. Inbox Processing Rules

The `00 - Inbox/` folder and `Inbox.md` note are **temporary capture zones only**.

- **Process inbox at least once per week** during the weekly review
- For each item in the inbox, decide:
  - 🗑️ **Delete** — not useful
  - ➡️ **Move** — place in the correct PARA folder
  - 📝 **Process** — expand into a permanent note, then move

- The inbox should ideally be **empty** after each weekly review

---

## 8. Archiving Rules

When archiving:

- Move the folder/note to the corresponding `04 - Archives/` subfolder
- Update the `status` frontmatter field to `archived`
- Add a `archived_date` field in frontmatter with the date
- Do NOT delete — archived notes are searchable reference material

---

## 9. Linking Rules

- Always link a new note to at least one existing note (no orphans)
- Link from **specific to general** (note → MOC → HOME)
- Use `[[wikilinks]]` for internal links
- Use descriptive link text: `[[Note Name|Display Text]]` when the filename isn't self-explanatory
- Add backlink context — when linking, write a sentence explaining _why_ you're linking
