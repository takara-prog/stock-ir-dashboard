# Sync Log — Claude→ChatGPT 差分共有ログ

> Claude側で作業が進んだときに、ChatGPTへ差分共有するためのログ。
> 新しいエントリは**先頭に追記**してください（最新が上）。

---

## 2026-06-06 作業日

### 変更された前提
- `docs/shared-context/` フォルダを新規作成（従来は存在しなかった）
- ClaudeとChatGPTの共通台帳運用を開始

### 決定したこと
- `source-of-truth.md` を共通台帳のマスターファイルとして運用する
- `chatgpt-briefing.md` の「ChatGPTに貼る短縮版」（末尾セクション）を毎回の相談に使う
- `sync-log.md` に差分を積み上げていくことで文脈分断を軽減する
- 推測と確定情報を必ず区別して記録する
- ChatGPTへはAPIキー・トークン・Secrets類を一切共有しない

### 作成・更新したファイル
- 新規作成: `docs/shared-context/source-of-truth.md`
- 新規作成: `docs/shared-context/chatgpt-briefing.md`
- 新規作成: `docs/shared-context/sync-log.md`（このファイル）

### GitHub / Netlify / Claude Code 状態
- ブランチ: `claude/shared-context-setup-YGWSc`
- push済み: 未（このログ記入後にpush予定）
- PR: 未作成（push後に作成予定）
- Netlify: 変更なし（docs追加のみ、動作に影響なし）
- GitHub Actions: 変更なし

### ChatGPTに共有すべき差分
- `docs/shared-context/` フォルダが新設され、共通台帳運用が始まったこと
- 次回からは「短縮版 + 最新sync-log + 質問」の3点セットで相談する運用になった

### 未解決・確認待ち
- リポジトリのpublic/private設定（要確認）
- Notion連携の実装状況（要確認）
- `work-agents/` / `library/` / `context-headroom-rules` の設計仕様（要確認）
- Resend APIの`report-cron.js`内での実装状況（ファイル未読）

### 次に相談するなら貼るべき情報
1. `chatgpt-briefing.md` の「ChatGPTに貼る短縮版」（末尾セクション）
2. このsync-logの最新エントリ（↑このブロック）
3. 具体的な質問

---

<!-- テンプレート（次の作業時にコピーして使用）

## YYYY-MM-DD HH:mm

### 変更された前提
-

### 決定したこと
-

### 作成・更新したファイル
-

### GitHub / Netlify / Claude Code 状態
-

### ChatGPTに共有すべき差分
-

### 未解決・確認待ち
-

### 次に相談するなら貼るべき情報
-

-->
