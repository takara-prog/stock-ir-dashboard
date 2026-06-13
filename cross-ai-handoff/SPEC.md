# Cross-AI Handoff Protocol — Specification

**Version**: 0.1.0  
**Status**: Draft  
**Last updated**: 2026-06

---

## 1. Overview

The Cross-AI Handoff Protocol (CAHP) defines a 3-file markdown structure that enables a human operator to maintain shared context across multiple AI assistant sessions without API integrations or technical setup.

**Core design principles:**

1. **Human-relayed** — The human decides when to hand off, what to share, and which AI to use. No autonomous agent-to-agent communication.
2. **Zero dependencies** — Plain markdown files. No APIs, no databases, no code required.
3. **Incrementally updatable** — The sync-log enables partial context sharing without full re-explanation.
4. **AI-agnostic** — Works with any AI assistant that accepts text input.
5. **Stoppable** — A `Status` field provides an explicit stop mechanism.

---

## 2. File Structure

```
[project-root]/
└── ai-context/
    ├── source-of-truth.md
    ├── briefing.md
    └── sync-log.md
```

The folder SHOULD be named `ai-context/`. Alternative names are permitted but must remain consistent across a project.

---

## 3. File Definitions

### 3.1 `source-of-truth.md`

**Purpose**: Authoritative record of the current project state.  
**Maintained by**: Human operator.  
**Shared with AI**: No — reference only. Do not paste to AI tools directly.

**Required structure:**

```markdown
# [Project Name] — Source of Truth
<!-- DATA-CLASS: PERSONAL | INTERNAL | PUBLIC -->
<!-- Last updated: YYYY-MM-DD -->

## Purpose
[What this project is for. 2–3 sentences.]

## Current State
[What is confirmed true right now. Mark assumptions as [UNCONFIRMED].]

## Roles
| Who/What        | Role                                      |
|-----------------|-------------------------------------------|
| Human operator  | [Decision-making, file maintenance]       |
| Manager AI      | [e.g., Claude — context mgmt, execution] |
| Reviewer AI     | [e.g., ChatGPT — review, risk checks]    |

## Scope
### In scope for AI assistance
- [Task 1]

### Out of scope (human decision required)
- [Task 1]

## Status
ACTIVE

## Unconfirmed
- [Assumption 1]

## Do Not Share With AI
- [Sensitive information categories specific to this project]
```

**Rules:**
- Separate confirmed facts from assumptions (`[UNCONFIRMED]` tag)
- `Status` MUST be one of: `ACTIVE`, `PAUSED`, `COMPLETED`, `ABANDONED`
- Never include credentials, tokens, personal data, or NDA-covered content
- Update `Last updated` date whenever the file changes

---

### 3.2 `briefing.md`

**Purpose**: Paste-ready context summary for starting a new AI session.  
**Maintained by**: Human operator (refreshed from `source-of-truth.md`).  
**Shared with AI**: Yes — paste at the start of any AI session.

**Target length**: 500–1500 characters. If it exceeds 1500 characters, it's too long.

**Required structure:**

```markdown
# [Project Name] — AI Briefing
<!-- Refresh date: YYYY-MM-DD -->
<!-- Source: source-of-truth.md, YYYY-MM-DD -->

**What this is**: [1–2 sentence summary]

**Current state**: [2–3 key facts]

**Your role in this session**: [Reviewer | Advisor | Executor — one only]

**Task for this session**: [What you're asking the AI to do]

**Constraints**:
- Do not include passwords, API keys, or personal data in your response
- Do not make decisions outside the task above
- [Project-specific constraint]
```

**Rules:**
- Always specify exactly one role for the AI in this session
- Include constraints explicitly — do not assume the AI will infer them
- Refresh `briefing.md` at the start of each major project phase
- The `Refresh date` must not be more than 30 days older than `source-of-truth.md`'s last update

---

### 3.3 `sync-log.md`

**Purpose**: Incremental log of significant changes for efficient handoffs.  
**Maintained by**: Human operator (after each significant session or decision).  
**Shared with AI**: Yes — paste the most recent entry when switching AI tools or resuming after a break.

**Entry format:**

```markdown
## YYYY-MM-DD — [Session title]

### What changed
- [Change 1]

### Decisions made
- [Decision 1]

### Files created or updated
- [File path or description]

### Unresolved
- [Open question 1]

### Next steps
- [Action 1]
```

**Rules:**
- Entries are ordered newest-first (latest entry at top)
- Each entry MUST be self-contained — readable without other entries
- Do not log credentials, personal data, or sensitive content
- Review entries older than 90 days; remove anything that has become sensitive

---

## 4. Data Classification

Every file MUST include a `DATA-CLASS` comment immediately after the title:

```
<!-- DATA-CLASS: PERSONAL -->   Personal use only; lowest risk
<!-- DATA-CLASS: INTERNAL -->   Business-related; do not commit to public repos
<!-- DATA-CLASS: PUBLIC -->     Safe for public repositories
```

**If `DATA-CLASS` is `INTERNAL` or unset:**
- Do not commit to a public repository
- Add `ai-context/` to `.gitignore`
- Verify your organization's AI data sharing policy before use
- Ensure AI tools used are configured to not use inputs for training

---

## 5. Role System

Each AI assistant in a project MUST be assigned exactly one of the following roles at any given time:

| Role | Responsibilities | May NOT |
|------|-----------------|---------|
| **Manager AI** | Maintain context, coordinate work, make implementation decisions | Approve irreversible actions without human confirmation |
| **Reviewer AI** | Review decisions, identify risks, suggest alternatives | Execute changes, access systems, make final decisions |
| **Executor AI** | Perform specific bounded tasks per explicit instructions | Expand scope, make architectural decisions |

The active role for each session MUST be stated in `briefing.md`.

---

## 6. Handoff Procedure

### Standard handoff (switching AI tools mid-session)

1. Open a new AI session with the target tool
2. Paste: contents of `briefing.md`
3. Paste: most recent entry from `sync-log.md`
4. Add your question or task
5. After the session: if significant decisions were made, add a `sync-log.md` entry

### Full re-context (after long break or major change)

1. Update `source-of-truth.md`
2. Refresh `briefing.md` from `source-of-truth.md`
3. Add a `sync-log.md` entry summarizing what changed
4. Proceed with standard handoff

### Emergency stop

1. Set `Status` in `source-of-truth.md` to `PAUSED`
2. Add a `sync-log.md` entry explaining why
3. No AI sessions should continue until Status is explicitly set back to `ACTIVE` by the human operator

---

## 7. What This Protocol Does Not Cover

- Agent-to-agent communication (see A2A Protocol, MCP)
- Automated context injection (see CLAUDE.md, Cursor Rules)
- Persistent memory systems (see Mem0, OpenMemory)
- Multi-agent orchestration (see LangGraph, CrewAI)

This protocol is intentionally scoped to human-relayed, clipboard-based workflows.

---

## 8. Versioning

This specification follows [Semantic Versioning](https://semver.org/):
- Major version: breaking changes to file structure or required fields
- Minor version: new optional fields or guidance
- Patch version: clarifications, typo fixes

Current version: **0.1.0 (Draft)**

Implementations should record the spec version they follow:

```markdown
<!-- CAHP-VERSION: 0.1.0 -->
```
