# AI会議ハブ v0.1

## 目的

複数のAI（ChatGPT / Claude / Gemini / Claude Code など）を**直接接続するものではない**。  
議題・役割・決定ログ・次アクション・作業レポートを**失わないため**のMarkdown運用ハブ。

## このハブでやること

- 複数AIへの指示を一貫させる「共通文脈」を保持する
- 決定・却下・保留を記録し、判断の再現性を確保する
- AIを切り替えても文脈が失われない引き継ぎ運用を実現する

## このハブでやらないこと（今回）

- Web UI実装
- API連携（OpenAI / Anthropic / Google APIなど）
- Notion連携
- Obsidian連携
- 自動化スクリプト
- .envやAPIキーの作成
- 既存プロジェクトへの変更

## ファイル一覧と役割

| ファイル | 役割 |
|---|---|
| `agenda.md` | 現在の議題と制約 |
| `roles.md` | 各AIの役割定義 |
| `meeting-log.md` | 会議ログ・対立点・統合判断 |
| `decision-log.md` | 決定済み事項の台帳 |
| `next-actions.md` | 次にやること一覧 |
| `handoff-template.md` | AI引き継ぎテンプレート |
| `anti-drift-check.md` | 脱線防止チェック |
| `creation-gate.md` | 新規作成前の確認ゲート |
| `meeting-template.md` | 毎回使う会議テンプレート |
| `decision-id-rule.md` | 決定IDの命名規則 |
| `reproducibility.md` | 再現性を保つ運用ルール |
| `rerun-template.md` | 過去判断の再評価テンプレート |
| `priority-rule.md` | P0〜P4優先度分類 |
| `idea-parking-lot.md` | 保留アイデア箱 |
| `resume-template.md` | 作業再開テンプレート |
| `definition-of-done.md` | 完了条件の定義 |
| `visibility-rule.md` | 公開可否分類 |
| `rejected-ideas.md` | 作らないと決めた案の記録 |
| `auditor-check.md` | 作業終了前の監査チェック |
| `work-report-template.md` | 作業完了レポート |
| `change-summary-template.md` | 変更差分レポート |
| `weekly-review-template.md` | 週次振り返り |

## 基本的な使い方

1. **会議を始めるとき** → `meeting-template.md` を複製して日付付きファイルを作る
2. **AIに指示を出すとき** → `agenda.md` と `roles.md` を前文として貼り付ける
3. **決定したとき** → `decision-log.md` に記録（IDは `decision-id-rule.md` に従う）
4. **AIを切り替えるとき** → `handoff-template.md` を埋めて渡す
5. **新しいファイルを作りたいとき** → `creation-gate.md` を先に確認する
6. **作業が終わったとき** → `work-report-template.md` で報告・`auditor-check.md` で監査

## 将来拡張案（今回は実装しない）

- 台帳の自動統合スクリプト
- GitHub Issues への自動変換
- 自動レポート生成（週次・月次）
- Web UI（議題・決定の可視化）
- マルチAI接続（MCP経由など）
- Notion / Obsidian 連携

## 注意事項

- このフォルダは既存プロジェクトと**独立している**
- 既存の `README.md`、`index.html`、`netlify.toml` には**一切触れない**
- APIキーや `.env` は**作成しない**
