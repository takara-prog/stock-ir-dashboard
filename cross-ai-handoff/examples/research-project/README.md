# Example: Research Project

This example shows the 3 files filled in for a realistic project: a solo researcher writing a market analysis report, using Claude for structure and ChatGPT as a reviewer.

**Scenario**: An independent analyst is writing a 15-page report on AI adoption trends in the healthcare sector. She uses Claude to help structure and draft sections, and occasionally hands off to ChatGPT for a second opinion on conclusions.

---

**Files in this example:**
- [`source-of-truth.md`](source-of-truth.md) — Full project state (not shared with AI)
- [`briefing.md`](briefing.md) — Paste-ready summary for AI sessions
- [`sync-log.md`](sync-log.md) — Session history and what changed

---

**What to notice:**

1. `source-of-truth.md` contains everything, including sensitive framing — it's never pasted to AI
2. `briefing.md` is much shorter and uses the role field to specify what the AI should and shouldn't do
3. `sync-log.md` entries are short and self-contained — you could hand just one entry to a new AI and it would understand the current state
