# Sync Log — Claude→ChatGPT 差分共有ログ

> Claude側で作業が進んだときに、ChatGPTへ差分共有するためのログ。
> 新しいエントリは**先頭に追記**してください（最新が上）。

---

## 2026-06-10 役割分担設計の確定

### 変更された前提
- ClaudeとChatGPTの役割を「2者」から「4者モデル」に明確化
- 管理主体はClaudeに確定（ChatGPTは管理主体でない）
- Claude Code をPC実行担当として明示的に分離

### 決定したこと
- Claude = 管理主体・共通台帳更新・実行方針決定
- Claude Code = PC実行担当（ファイル作成・GitHub操作・PR）
- ChatGPT = 外部参謀（外部レビュー・リスク判定・Claudeへの指示文作成）。実行権限なし
- GitHub / docs = 共通台帳の保管場所
- ChatGPTを管理主体として扱わない

### 作成・更新したファイル
- 更新: `docs/shared-context/source-of-truth.md`（セクション4 役割分担を4者モデルに改訂）
- 更新: `docs/shared-context/chatgpt-briefing.md`（役割表・テンプレート・短縮版を4者モデルに改訂）
- 更新: `docs/shared-context/sync-log.md`（このエントリ追記）

### GitHub / Netlify / Claude Code 状態
- PR #2: Draft、マージ可能
- Netlify Deploy Preview: 既存問題のため失敗継続中（PR変更とは無関係）
- GitHub Actions: 変更なし

### ChatGPTに共有すべき差分
- 役割分担が4者モデルに確定した（Claude管理・Claude Code実行・ChatGPT外部参謀）
- ChatGPTに相談するテンプレートが更新された（末尾の短縮版参照）

### 未解決・確認待ち
- Netlify Deploy Preview失敗の根本原因（別途対応）
- work-agents / library / context-headroom-rules の設計仕様

### 次に相談するなら貼るべき情報
1. `chatgpt-briefing.md` の「ChatGPTに貼る短縮版」（末尾セクション）
2. このsync-logの最新エントリ（↑このブロック）
3. 具体的な質問

---

## 2026-06-06 Netlify切り分け結果

### 変更された前提
- Netlify Deploy Preview失敗（PR #2）は今回のPR変更とは無関係と判断

### 決定したこと
- PR #2（docs/shared-context/*.md追加のみ）でNetlify設定変更は行わない
- Netlify Deploy Preview失敗は既存Netlify側問題の可能性。今回PR変更とは無関係と判断
- Netlify問題を調査・修正する場合は別Issue/別PRで扱う

### 作成・更新したファイル
- 更新: `docs/shared-context/sync-log.md`（このエントリ追記）

### GitHub / Netlify / Claude Code 状態
- PR #2: Draft、レビュー待ち
- Netlify Deploy Preview: failure（PR変更とは無関係、既存問題の可能性）
- GitHub Actions: 変更なし
- 本番（main）のNetlify: 影響なし

### ChatGPTに共有すべき差分
- Netlify Deploy Preview失敗はPR #2の変更（markdownのみ）とは無関係と確認済み
- Netlify調査は別対応予定

### 未解決・確認待ち
- Netlify Deploy Preview失敗の根本原因（Netlifyダッシュボードで要確認）

### 次に相談するなら貼るべき情報
1. `chatgpt-briefing.md` の「ChatGPTに貼る短縮版」
2. このsync-logの最新エントリ
3. 具体的な質問

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
