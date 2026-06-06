# ChatGPT Briefing — AI統合参謀システム

> ChatGPTに途中相談するときに貼る用のブリーフィングファイル。
> 全体版（このファイル）と、末尾の「ChatGPTに貼る短縮版」の2段階構成。
> 最終更新: 2026-06-06

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

## 3. ClaudeとChatGPTの役割分担

| 役割 | Claude（API/Code） | ChatGPT |
|-----|-------------------|---------|
| コード実装 | ◎ 主担当 | △ 相談のみ |
| GitHub操作 | ◎ Claude Code | ✗ |
| 設計壁打ち | ○ | ◎ セカンドオピニオン |
| IR分析・レポート | ◎ 本番運用中 | △ 必要に応じて |
| Notion操作 | △ 未確認 | ✗ |
| コンテキスト管理 | context-headroom-rulesで対応 | 途中参加時は短縮ブリーフで補完 |

**文脈分断の課題**: ClaudeのセッションはリセットされるためChatGPTに相談する際に前提が失われる。このファイルがその橋渡し役。

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
## 前提（以下に短縮ブリーフィングを貼る）
[chatgpt-briefing.md の「ChatGPTに貼る短縮版」を貼る]

## 最新の変更（以下にsync-logの最新差分を貼る）
[sync-log.md の最新エントリを貼る]

## 今回の相談
[具体的な質問・課題を記載]

## 制約条件
- APIキー・秘密情報は含みません
- 実装の最終決定はClaude側で行います
- GitHub・Netlify・Notionへの実際の操作はClaude Codeが担当します
```

---

---

# ChatGPTに貼る短縮版

> このセクションだけを切り取ってChatGPTに貼ってください（約1200文字）

---

## 【AI統合参謀システム 共通前提】2026-06-06版

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

### 役割分担
| 担当 | 役割 |
|-----|------|
| Claude Code | コード実装・GitHub操作・ファイル管理 |
| Claude API | IR分析・市場レポート生成 |
| ChatGPT（あなた） | 設計壁打ち・セカンドオピニオン |
| GitHub | ソース管理・CI/CD |
| Netlify | ホスティング・Functions実行 |

### ルール
- APIキー・トークン・Webhook URLは共有しない
- GitHubへはコードのみpush（secretsは絶対に含めない）
- `docs/shared-context/`が共通台帳（Claude↔ChatGPT間の文脈橋渡し）
- 推測と確定情報は分けて扱う（不明点は「未確認」と明記）

### ChatGPTへのお願い
実装・GitHub操作の最終判断はClaude Codeが行います。設計・方針・選択肢の整理を中心に相談します。不明点は「未確認」と返してください。断定しないでください。
