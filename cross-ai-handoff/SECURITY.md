# Security & Legal Guidelines

> Read this before you start. This is written in plain language — no technical background required.

---

## The One Rule

**Would you show this content to a stranger in a coffee shop?**

- Yes → Probably safe to include
- No → Do not include it

When in doubt: don't write it in these files.

---

## What Must Never Appear In Your Files

| Category | Examples |
|----------|---------|
| Credentials | Passwords, API keys, access tokens, SSH keys |
| Personal data | Full names, email addresses, phone numbers, home addresses |
| Financial details | Bank account numbers, card numbers, transaction records |
| Health information | Medical records, diagnoses, prescriptions |
| Legal matters | Ongoing litigation, NDA-covered content, attorney communications |
| Business secrets | Unreleased product plans, proprietary processes, client data |

**If you're unsure whether something belongs in these files: it doesn't.**

---

## Understanding the Multi-AI Risk

This protocol involves sending the same content to multiple AI services.

When you paste your `briefing.md` to Claude, that content goes to **Anthropic's servers**.  
When you paste it to ChatGPT, the same content goes to **OpenAI's servers**.

Each company has its own:
- Privacy policy
- Data retention period
- Training data policy

**You are voluntarily sending your content to each provider you use.**

Check current policies before you start:
- Anthropic (Claude): https://www.anthropic.com/legal/privacy
- OpenAI (ChatGPT): https://openai.com/policies/privacy-policy

---

## Personal Use

If you're using this for personal projects (not work):

- [ ] Have you turned off AI training data settings where possible?
- [ ] Does your content include any other person's personal information?
- [ ] Are you comfortable with the content being stored on external servers?

Free-tier AI tools typically have fewer privacy protections than paid plans. If your content is sensitive, use a paid plan and verify the data policy.

---

## Business / Professional Use

If you're using this for work, answer all of these before proceeding:

- [ ] Does my company have an AI usage policy?
- [ ] Am I permitted to send work-related content to external AI services?
- [ ] Is any of this content covered by a non-disclosure agreement?
- [ ] Does any of this content include client, customer, or patient data?
- [ ] Have I checked with IT or legal if I'm unsure?

**If you cannot answer all five: stop and check with your IT or legal team.**

No productivity gain is worth a data breach or contract violation.

---

## GitHub and Public Repositories

`DATA-CLASS: INTERNAL` files must not go into public repositories.

To prevent accidental commits, add this to your project's `.gitignore`:

```
ai-context/
```

If your project is public and your `ai-context/` files are safe to share, change the `DATA-CLASS` to `PUBLIC` — but only after confirming all content is appropriate.

The template files in this repository are `DATA-CLASS: PUBLIC` because they contain only placeholder text.

---

## Pre-Handoff Checklist

Before pasting content to any AI tool:

- [ ] No passwords, API keys, or tokens present
- [ ] No personal data (names, emails, phone numbers) present
- [ ] No company-confidential content (if using for work)
- [ ] I know which AI service I'm using and have reviewed its data policy
- [ ] `Status` in `source-of-truth.md` is `ACTIVE`

---

## If Something Goes Wrong

If you accidentally paste sensitive information to an AI tool:

1. **Stop the conversation immediately** — do not continue
2. **Check the provider's data deletion process** and submit a request if available
3. **If work-related**: notify your IT security or compliance team right away
4. **If credentials were exposed**: rotate them immediately (change passwords, revoke API keys)

---

## Disclaimer

This protocol is provided as-is, without warranty of any kind. It does not guarantee security, privacy, or legal compliance. You are solely responsible for the content you include in your files, for complying with applicable laws, and for following your organization's policies.

The protocol authors are not liable for any data exposure, legal issue, or other harm resulting from use of this protocol.
