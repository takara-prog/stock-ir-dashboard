# Cross-AI Handoff Protocol

> A zero-dependency, markdown-native protocol for working across multiple AI assistants without losing context.

No APIs. No code. No integrations. Just markdown and your clipboard.

---

## The Problem

You use Claude for one thing. ChatGPT for another. Maybe Gemini too.

Every time you switch, you spend 10 minutes re-explaining:
- What this project is
- What you already decided
- What changed since last time
- What the AI should and shouldn't do

This protocol solves that.

---

## Who This Is For

**You work with multiple AI tools through their web interfaces and you're not a developer.**

You're a researcher, writer, analyst, or business professional who uses AI seriously — not just occasionally. You've started switching between Claude and ChatGPT depending on the task, and you keep losing context.

You don't use APIs. You don't have a development environment. But you can edit a markdown file.

---

## How It Works

Three files. One folder.

```
your-project/
└── ai-context/
    ├── source-of-truth.md   ← Full picture. You maintain this.
    ├── briefing.md          ← Paste-ready summary for any AI.
    └── sync-log.md          ← What changed since last time.
```

**The workflow in 3 steps:**

1. **Before a new AI session** — paste `briefing.md` + the latest `sync-log.md` entry + your question
2. **After a significant decision** — add an entry to `sync-log.md`
3. **When the project fundamentally changes** — update `source-of-truth.md` and refresh `briefing.md`

That's it.

---

## The 3 Files

### `source-of-truth.md` — Your master reference
The full, accurate record of your project state. You don't paste this to AI tools. You update it when fundamentals change, and you use it to refresh `briefing.md`.

### `briefing.md` — What you paste to the AI
A short summary (500–1500 characters) designed to fit in any AI prompt without wasting context. Refreshed from `source-of-truth.md` every few sessions.

### `sync-log.md` — What changed since last time
A running log of significant decisions and changes. When you switch AI tools or come back after a break, paste only the latest entry. This is what makes "catching up" fast.

---

## Quick Start

```bash
# 1. Copy the templates into your project
cp -r templates/ your-project/ai-context/

# 2. Fill in source-of-truth.md with your project's current state
# 3. Ask an AI to help you write a short briefing.md from it
# 4. You're ready to use the protocol
```

Or just copy the template files manually — no command line required.

See `examples/research-project/` for a worked example.

---

## Why Not Just Use CLAUDE.md or AGENTS.md?

| | CLAUDE.md | AGENTS.md | This Protocol |
|---|---|---|---|
| Works with multiple AI tools | ✗ Claude only | ✗ Automation bots | ✓ Any AI web UI |
| Requires developer setup | ✗ | ✓ | ✓ No setup |
| Human decides when to hand off | Auto-inject | Automated | ✓ Human in the loop |
| Tracks what changed | ✗ | ✗ | ✓ sync-log |
| Works via copy-paste | ✗ | ✗ | ✓ |

A2A (Google) and MCP (Anthropic) are powerful protocols — but they require technical setup and tool integration. This protocol works today, in any browser, with no configuration.

When your tools eventually integrate natively, this protocol becomes unnecessary. Until then, this is the practical option.

---

## Role Design

One of the most important parts of this protocol is **explicitly defining what each AI should and shouldn't do** in each session.

Recommended roles:

| Role | Description |
|------|-------------|
| **Manager AI** | Maintains context, makes decisions, updates files |
| **Reviewer AI** | Reviews decisions, checks for risks, suggests alternatives — does not execute |
| **Executor AI** | Performs specific bounded tasks based on instructions from Manager AI |

Define these roles in your `source-of-truth.md` and include the relevant role in each `briefing.md`. This prevents scope creep and role confusion.

---

## Security

Read `SECURITY.md` before you start. Short version:

- Never include passwords, API keys, or tokens
- Never include personal data (names, emails, addresses)
- If you're using this for work, check your company's AI data policy first
- When in doubt, don't write it in these files

---

## Status & Stop Mechanism

`source-of-truth.md` always includes a `Status` field:

```
Status: ACTIVE | PAUSED | COMPLETED | ABANDONED
```

When Status is not `ACTIVE`, no AI should suggest or take further action on the project without a human decision. This is your built-in stop mechanism.

---

## Contributing

Issues and PRs welcome. Most useful:
- Examples from different domains (business analysis, academic research, writing projects)
- Translations of templates
- Reports of what actually goes wrong in practice
- Security edge cases we haven't considered

See `CONTRIBUTING.md`.

---

## License

MIT — use freely, adapt as needed.

---

## Specification

For the formal protocol definition, see [`SPEC.md`](SPEC.md).
