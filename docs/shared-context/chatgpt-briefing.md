# ChatGPT Briefing — AI統合参謀システム

> ChatGPTに途中相談するときに貼る用のブリーフィングファイル。
> 全体版（このファイル）と、末尾の「ChatGPTに貼る短縮版」の2段階構成。
> 最終更新: 2026-06-10

---

## 1. 現在の全体像

**プロジェクト名**: stock-ir-dashboard  
**目的**: 日本株・IR情報を分析・自動配信するダッシュボード＋AI統合運用基盤  
**リポジトリ**: `takara-prog/stock-ir-dashboard`（GitHub）  
**デプロイ**: Netlify（フロントエンド）+ GitHub Actions（自動化）

### 動いているもの（確定）
- `index.html`: IR分析・市場データ・レポート生成の3タブUI（日本語）
- `netlify/functions/analyze.js`: Claude API プロキシ（claude-haiku-4-5-20251001）
- GitHub Actions: 朝5時JST・夕21時JST に Claude Sonnet + web_search でレポート生成 → Discord配信
- 外部API: Anthropic / Resend / Discord Webhook（すべてGitHub Secretsで管理）

### 設計中・未実装（未確認）
- `work-agents/`: AIエージェント定義フォルダ（未作成）
- `library/`: 共通ナレッジフォルダ（未作成）
- `context-headroom-rules`: コンテキスト管理ルール（未確認）
- Notion連携（言及あり、実装未確認）

---

## 2. work-agents / library / context-headroom-rules の関係

### 現在の位置づけ（想定・未確認）

```
work-agents/          → AIが担当するタスク・エージェント定義を格納
library/              → 分析に使う参照資料・共通ナレッジを格納
context-headroom-rules → Claudeが1セッションで扱えるコンテキスト量の管理ルール
docs/shared-context/  → ClaudeとChatGPTの共通台帳（このフォルダ）
```

これらは「AI統合参謀システム」の構成要素として設計中。具体的な仕様はまだ固まっていない。

---

## 3. 役割分担（4者モデル）

| 担当 | 役割 | 実行権限 |
|-----|------|---------|
| **Claude** | プロジェクト管理・共通台帳更新・実行方針決定 | ◎ 管理主体 |
| **Claude Code** | ファイル作成・GitHub操作・PR・ローカル作業 | ◎ PC実行担当 |
| **ChatGPT（あなた）** | 外部レビュー・リスク判定・選択肢整理・Claudeへの指示文作成 | ✗ 実行しない |
| **GitHub / docs** | 共通台帳の保存場所・CI/CD | — 保管場所 |

**ChatGPTの役割の定義**:
- 判断・監査・リスクチェックを行う外部参謀
- Claude Codeに実行させるための指示文を作成する
- 実装・GitHub操作・Netlify設定は行わない（Claudeへ判断を返すのみ）

**文脈分断の対策**: Claudeのセッションがリセットされても、このファイル＋sync-logの最新差分を渡すことで同じ前提に戻れる。

---

## 4. 触ってよい範囲 / 触ってはいけない範囲

### ChatGPTが参照・議論してよいもの
- このブリーフィングファイルの内容
- コードの設計・構造
- エラーメッセージ（認証情報なし）
- アーキテクチャの選択肢
- `sync-log.md` の差分

### ChatGPTに渡してはいけないもの
- APIキー・トークン（Anthropic / Resend / Discord）
- Webhook URLの実際の値
- `.env` の中身
- GitHub Secretsの内容
- Notionの認証情報

---

## 5. GitHub・Notion・ローカルファイルの扱い

### GitHub
- ブランチ運用: feature/fix → PR → main（直接pushなし）
- Secrets管理: `ANTHROPIC_API_KEY`, `DISCORD_WEBHOOK_URL`, `RESEND_API_KEY`
- ChatGPTへ: コードは貼ってOK、Secretsは貼らない

### Notion（未確認）
- 連携方法・スコープともに未確認
- 確認後にこのファイルを更新予定

### ローカルファイル
- `.env`があっても中身は共有しない
- `docs/shared-context/` はGitHubにpushしてChatGPTにも共有OK

---

## 6. ChatGPTに相談するときのテンプレート

```
【ChatGPT共有用ブリーフィング】
[chatgpt-briefing.md の「ChatGPTに貼る短縮版」を貼る]

【最新sync-log】
[sync-log.md の最新エントリを貼る]

【今回相談したいこと】
[具体的な質問・課題を記載]

【Claude側で完了していること】
[すでに実施済みの作業]

【これからClaude Codeに実行させる予定】
[次の実行予定]

【不安点・判断してほしいこと】
[ChatGPTに判断・レビューしてほしい内容]

【触ってはいけないもの】
- secret/API key/token
- .envの中身
- MCP設定の秘密情報
- GitHub/Notion認証情報
```

**ChatGPTへの期待する返答形式**:
- 判断（やってよい / やめるべき / 要確認）
- リスク（何が危ないか）
- Claudeに返す文（次のClaude Codeへの指示文）
- やってはいけないこと

---

---

# ChatGPTに貼る短縮版

> このセクションだけを切り取ってChatGPTに貼ってください（約1200文字）

---

## 【AI統合参謀システム 共通前提】2026-06-10版

**プロジェクト**: stock-ir-dashboard（`takara-prog/stock-ir-dashboard`）  
**目的**: 日本株・IRダッシュボード＋AI統合運用基盤

### 動いている構成
- フロントエンド: `index.html`（IR分析・市場データ・レポート3タブ、日本語UI）
- バックエンド: Netlify Functions（analyze.js = Claude APIプロキシ）
- 自動化: GitHub Actions（朝5時JST・夕21時JST、Claude Sonnet + web_search → Discord）
- 外部API: Anthropic / Resend / Discord Webhook（GitHub Secretsで管理）

### 設計中・未確認
- `work-agents/`（エージェント定義）・`library/`（ナレッジ）・`context-headroom-rules`（コンテキスト管理）はまだ未作成・設計中
- Notion連携は言及あり、実装未確認

### 役割分担（4者モデル）
| 担当 | 役割 | 実行権限 |
|-----|------|---------|
| Claude | プロジェクト管理・共通台帳更新・実行方針決定 | ◎ 管理主体 |
| Claude Code | ファイル作成・GitHub操作・PR・ローカル作業 | ◎ PC実行担当 |
| ChatGPT（あなた） | 外部レビュー・リスク判定・選択肢整理・Claudeへの指示文作成 | ✗ 実行しない |
| GitHub / docs | 共通台帳の保存・ソース管理・CI/CD | — 保管場所 |

### ルール
- APIキー・トークン・Webhook URL・.env・MCP秘密情報・認証情報は共有しない
- GitHubへはコードのみpush（secretsは絶対に含めない）
- `docs/shared-context/`が共通台帳（Claude↔ChatGPT間の文脈橋渡し）
- 推測と確定情報は分けて扱う（不明点は「未確認」と明記）
- ChatGPTを管理主体として扱わない

### ChatGPTへのお願い
あなたは外部参謀・監査役です。判断・リスクチェック・Claude Codeへの指示文作成を担当してください。実装・GitHub操作はClaudeが決定しClaude Codeが実行します。不明点は「未確認」と返してください。断定しないでください。
