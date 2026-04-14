---
name: second-brain
description: Knowledge base for Building a Second Brain methodology using PARA, CODE, and MOC patterns in Obsidian
---

# Second Brain Methodology

A **Second Brain** is an external, digital system for capturing, organizing, and retrieving knowledge so your biological brain is free to think rather than just remember. Coined by Tiago Forte in _Building a Second Brain_.

---

## 🔄 The CODE Framework

The four stages of working with knowledge:

| Stage        | Description                                                             |
| ------------ | ----------------------------------------------------------------------- |
| **C**apture  | Save anything that resonates — ideas, quotes, links, voice memos        |
| **O**rganize | Sort saved material into PARA (by actionability, not topic)             |
| **D**istill  | Highlight the most valuable bits; progressive summarization             |
| **E**xpress  | Use the material to produce something — a note, post, project, decision |

> Key principle: **Organize by actionability, not by topic.**

---

## 📁 The PARA Method

Four and only four top-level folders. Everything in your digital life fits into one of them.

### 1. Projects (`01 - Projects/`)

Short-term efforts with a **specific goal and deadline**.

- Has a defined end state ("launch website", "plan trip to Japan")
- Active right now
- Each project gets its own subfolder with a Project MOC note

**Examples:** `Redesign Portfolio`, `Buy Car`, `Plan Wedding`

### 2. Areas (`02 - Areas/`)

Long-term responsibilities with **no end date** — maintained over time.

- Never "done", only maintained
- Represents a standard you want to uphold

**Examples:** `Health`, `Finances`, `Career`, `Relationships`, `Learning`

### 3. Resources (`03 - Resources/`)

Topics or interests you want to **reference in the future**.

- Not actionable right now
- Organized by topic/interest
- Notes from books, articles, courses, research

**Examples:** `Web Development`, `Psychology`, `Coffee`, `Photography`

### 4. Archives (`04 - Archives/`)

**Inactive** items from the other three categories.

- Completed or paused projects
- Areas no longer relevant
- Resources no longer of interest
- Nothing is ever permanently deleted — just archived

---

## 🗺️ Maps of Content (MOC)

A **Map of Content** is an index note that links to all related notes on a topic. It provides a bird's-eye view without forcing rigid hierarchy.

### When to create a MOC

- When you have 5+ notes on the same topic
- When you want a navigable entry point to a subject
- When a folder would otherwise become too large

### MOC Template Structure

```markdown
# [Topic] MOC

> One-sentence description of this topic.

## 🔗 Key Notes

- [[Note 1]]
- [[Note 2]]

## 📂 Sub-topics

- [[Sub-MOC 1]]

## 📚 Sources & References

- [[Book Note]]
- [[Article Note]]

## 💡 My Insights

_Summary of key takeaways or open questions._
```

---

## 📝 Note Types

| Type           | Purpose                                     | Lives In           |
| -------------- | ------------------------------------------- | ------------------ |
| **Fleeting**   | Quick captures, raw thoughts                | `00 - Inbox/`      |
| **Literature** | Notes from a specific source (book/article) | `Resources/`       |
| **Permanent**  | Processed, atomic ideas in your own words   | `Areas/Resources/` |
| **Project**    | All material related to one active project  | `Projects/`        |
| **MOC**        | Index/map linking related notes             | Anywhere           |
| **Daily Note** | Daily log, captures, tasks, reflections     | `Daily Notes/`     |

---

## 🏷️ Tagging Strategy

Use tags for **cross-folder attributes**, not for organization (that's what folders are for).

### Recommended Tag Taxonomy

```
#type/fleeting
#type/literature
#type/permanent
#type/project
#type/moc

#status/active
#status/done
#status/someday
#status/archived

#area/health
#area/finance
#area/career
#area/learning

#source/book
#source/article
#source/video
#source/podcast
#source/course
```

---

## 🔗 Linking Strategy

- **Link liberally** — when writing any note, ask "what else do I know that relates to this?"
- Use `[[wikilinks]]` to create bidirectional connections
- A note with no links is an orphan — always connect it to at least one MOC
- The **Graph View** in Obsidian reveals clusters of well-connected knowledge

---

## 📅 Daily & Weekly Review Rituals

### Daily Capture (5–10 min)

1. Open `📥 Inbox.md` or today's Daily Note
2. Dump any fleeting thoughts, links, ideas
3. Process yesterday's inbox: move or discard each item

### Weekly Review (30–60 min)

1. **Clear Inbox** — process all fleeting notes
2. **Review Projects** — update status, next actions
3. **Review Areas** — are you maintaining your standards?
4. **Archive** — move completed projects to `04 - Archives/`
5. **Update Weekly Note** — log wins, blockers, lessons

---

## 🏠 Dashboard / HOME Note

Every well-structured vault has a `HOME.md` as its entry point:

```markdown
# 🏠 Home

> _"A place for everything, and everything in its place."_

## 🚀 Active Projects

- [[Project A]]
- [[Project B]]

## 🌱 Areas

- [[Health]] | [[Finances]] | [[Career]]

## 📚 Resource MOCs

- [[Web Development MOC]] | [[Psychology MOC]]

## 📅 Today

![[Daily Notes/{{date}}]]

## 📥 Inbox

[[Inbox]]
```

---

## 🗂️ Recommended Vault Structure

```
📁 00 - Inbox/
📁 01 - Projects/
    📁 Project Name/
        📄 Project Name MOC.md
📁 02 - Areas/
    📁 Health/
    📁 Finances/
    📁 Career/
📁 03 - Resources/
    📁 Topic Name/
📁 04 - Archives/
    📁 Projects/
    📁 Areas/
📁 Daily Notes/
📁 Templates/
    📄 Project Template.md
    📄 Daily Note Template.md
    📄 Literature Note Template.md
    📄 MOC Template.md
📄 🏠 HOME.md
📄 📥 Inbox.md
```

---

## ⚡ Key Principles

1. **Capture first, organize later** — never let perfect be the enemy of captured
2. **One source of truth** — each piece of info lives in one place
3. **Progressive summarization** — highlight on each re-read pass
4. **Organize by actionability** — PARA priority: Projects > Areas > Resources > Archives
5. **Link generously** — connections between ideas are more valuable than the ideas themselves
6. **Review regularly** — a second brain only works if you revisit it
