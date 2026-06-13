# Contributing

Thank you for your interest in improving this protocol.

---

## Most Wanted Contributions

### Examples
Real-world examples of these 3 files in use are the most valuable contribution. Good example domains:
- Academic research
- Business analysis
- Writing and editorial projects
- Product design
- Personal knowledge management

Submit examples in `examples/[domain-name]/`.

### Security edge cases
If you find a way the current security guidance fails or could be misunderstood, please open an issue. This is especially valuable.

### Translations
The templates in `templates/` are in English, but the protocol works in any language. Translated template sets (e.g., `templates-ja/`, `templates-es/`) are welcome.

### Reports from practice
What actually breaks? What guidance is unclear? What did low-literacy users get wrong? These reports are how the spec improves.

---

## What We're Not Looking For (Right Now)

- API integrations or automated tooling (out of scope for v0.x — the protocol is intentionally zero-dependency)
- MCP server implementations (consider this after v1.0 if the protocol gains adoption)
- CLI tools for sync-log generation (same reason)

---

## How to Submit

1. Fork this repository
2. Create a branch: `feature/your-contribution` or `fix/issue-description`
3. Make your changes
4. Open a pull request with a clear description of what changed and why

For security issues, please open an issue marked `[SECURITY]` rather than a PR.

---

## Spec Changes

Changes to `SPEC.md` require discussion before a PR:
1. Open an issue describing the proposed change
2. Explain the use case that motivates it
3. If there's consensus, submit a PR

Breaking changes (major version bumps) require significant justification and a migration path.
