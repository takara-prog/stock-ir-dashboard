# Source of Truth — AI統合参謀システム 共通台帳

> このファイルは ClaudeとChatGPTが同じ前提で判断するための「共通台帳」です。
> 推測と確定情報は明示的に区別されています。不明点は「未確認」と記載。
> 最終更新: 2026-06-06

---

## 1. この環境全体の目的

### 確定
- **リポジトリ名**: `takara-prog/stock-ir-dashboard`
- **目的**: 日本株・IR情報を分析・配信するダッシュボード + AI統合運用基盤の構築
- **主なユーザー**: 個人投資家・IR担当者向け（日本語UI）
- **デプロイ先**: Netlify（フロントエンド + Serverless Functions）
- **自動化基盤**: GitHub Actions（朝・夕レポート配信）

### 未確認
- work-agents / library フォルダの具体的な設計仕様（フォルダは現時点で未作成）
- context-headroom-rules の正式な運用開始タイミング
- Notion連携の実装状況（言及あり、実装確認できていない）
- 「AI統合参謀システム」全体の最終形

---

## 2. 現在のシステム構成（確定）

### フロントエンド
- `index.html`（352行）: 単一HTMLファイル
  - タブ1「IR分析」: IRテキスト・決算書の分析
  - タブ2「マーケット」: 主要指数・個別銘柄検索・グローバルニュース
  - タブ3「レポート」: 朝・夕レポート生成
- Claude APIを直接呼び出す構造（ユーザーがAPIキーを入力する形式）

### バックエンド（Netlify Functions）
- `netlify/functions/analyze.js`: Claude API プロキシ（CORS対応）
  - 使用モデル: `claude-haiku-4-5-20251001`
  - ユーザーが渡すAPIキーを使用（サーバー側にキーを保持しない設計）
- `netlify/functions/morning-cron.js`: 朝レポート自動生成
- `netlify/functions/report-cron.js`: 夕レポート自動生成

### 自動化（GitHub Actions）
- `morning-report.yml`: 毎朝5時JST（UTC 20:00）月〜金
  - Claude Sonnet (`claude-sonnet-4-6`) + web_search ツール使用
  - Discord Webhookへ配信
- `evening-report.yml`: 毎夕21時JST（UTC 12:00）月〜金
  - 同上

### 外部サービス連携（確定）
| サービス | 用途 | 認証方法 |
|---------|------|---------|
| Anthropic Claude API | AI分析・レポート生成 | APIキー（GitHub Secrets） |
| Discord Webhook | レポート配信 | Webhook URL（GitHub Secrets） |
| Resend API | メール配信 | APIキー（GitHub Secrets）|
| Netlify | ホスティング・Functions | Netlifyアカウント連携 |

---

## 3. フォルダ構成と役割（現在）

```
stock-ir-dashboard/
├── index.html              # フロントエンド本体
├── netlify.toml            # Netlify設定
├── README.md               # 最小限のREADME
├── netlify/
│   └── functions/          # Serverless Functions
│       ├── analyze.js
│       ├── morning-cron.js
│       └── report-cron.js
├── .github/
│   └── workflows/
│       ├── morning-report.yml
│       └── evening-report.yml
└── docs/
    └── shared-context/     # ← このフォルダ（新規作成）
        ├── source-of-truth.md  （このファイル）
        ├── chatgpt-briefing.md
        └── sync-log.md
```

### 未作成フォルダ（将来予定・未確認）
- `work-agents/`: AIエージェント定義・プロンプトテンプレート等を想定
- `library/`: 共通ナレッジ・参照資料等を想定
- `context-headroom-rules/` または関連ファイル: コンテキスト管理ルール

---

## 4. 役割分担

### 各ツールの役割（確定・運用中）

| ツール | 役割 |
|-------|------|
| **Claude (API)** | IRテキスト分析・市場レポート生成・web検索 |
| **Claude Code (CLI)** | コード実装・ファイル操作・GitHub操作・構成管理 |
| **ChatGPT** | 設計相談・壁打ち・Claude側で詰まった時のセカンドオピニオン |
| **GitHub** | ソースコード管理・GitHub Actions自動化・CI/CD |
| **Netlify** | フロントエンドホスティング・Serverless Functions実行 |

### 各ツールの役割（未確認・将来想定）

| ツール | 想定役割 |
|-------|---------|
| **Notion** | ナレッジ管理・ログ・タスク管理（連携方法未確認） |
| **work-agents** | エージェント定義の格納場所（設計未完） |
| **library** | 共通参照資料の格納場所（設計未完） |

---

## 5. Claude Codeが読んでよい範囲

### 許可（確定）
- リポジトリ内の全ファイル（コード・設定・ドキュメント）
- `netlify.toml`、`*.yml`（ワークフロー定義）
- `docs/shared-context/` 配下のファイル

### 注意が必要
- `.env` ファイル（現在は存在しない。もし作成された場合は中身を読まない）
- GitHub Secrets（Claude Codeからは参照不可・すべきでない）

---

## 6. ChatGPTに共有してよい範囲

### 共有OK
- このファイル（source-of-truth.md）全体
- `chatgpt-briefing.md` の内容
- `sync-log.md` の差分
- コードの構造・設計の議論
- エラーメッセージ・ログ（認証情報を含まないもの）

### 共有禁止
- APIキー・トークン・シークレット類
- `.env` の中身
- Webhook URL の実際の値
- GitHub Secrets の内容
- Notionの認証情報・内部URL（設定済みの場合）

---

## 7. GitHubにpushしてよい範囲

### pushOK
- コード全般（index.html、Netlify Functions、GitHub Actionsワークフロー）
- `docs/shared-context/` 配下のファイル（このファイル含む）
- `netlify.toml`、`README.md`

### push禁止・要注意
- `.env` ファイル（`.gitignore` に必ず含めること）
- APIキー・トークンを含むファイル
- 個人情報・プライベートなログ

### 現在のリポジトリ可視性
- **未確認**（publicかprivateか要確認。publicの場合は特にsecretの混入に注意）

---

## 8. secret / API key / token の安全運用ルール

### 現在の運用（確定）
- `ANTHROPIC_API_KEY`: GitHub Secretsに格納、GitHub Actionsから参照
- `DISCORD_WEBHOOK_URL`: GitHub Secretsに格納
- `RESEND_API_KEY`: GitHub Secretsに格納（ワークフロー内で使用想定）
- フロントエンドのAPIキー: ユーザーがブラウザで入力（サーバー保存なし）

### ルール
1. APIキー・トークンはコードに直書き禁止
2. `.env` が必要な場合は必ず `.gitignore` に追加
3. ログ・エラーメッセージにAPIキーを含めない
4. ChatGPT・Claudeへの質問時にシークレット情報を貼らない

---

## 9. やってはいけないこと

- [ ] APIキー・トークンをコードやMarkdownに直書きする
- [ ] `.env` を `.gitignore` なしで git add する
- [ ] GitHub Secretsの内容を外部ツールに貼り付ける
- [ ] 確認なしに `main` ブランチへ直接 push する
- [ ] 推測情報を確定情報として記録する
- [ ] このファイルを更新せずにシステム構成を大きく変える

---

## 10. 現在の安全運用ルール（Claude Code）

- 開発ブランチ: `claude/shared-context-setup-YGWSc`
- `main` ブランチへの直接pushは禁止
- 変更はPR経由でマージ
- 重要な構成変更は `sync-log.md` に記録

---

## 11. 未確認事項一覧

| # | 項目 | 確認方法 |
|---|------|---------|
| 1 | リポジトリのpublic/private設定 | GitHub設定で確認 |
| 2 | Notion連携の実装状況 | ユーザーへ確認 |
| 3 | work-agents フォルダの設計仕様 | ユーザーへ確認 |
| 4 | library フォルダの設計仕様 | ユーザーへ確認 |
| 5 | context-headroom-rules の内容 | ユーザーへ確認 |
| 6 | Resend APIの実装状況（Functions内） | report-cron.js を確認 |
| 7 | Netlify環境変数の設定状況 | Netlifyダッシュボードで確認 |
| 8 | 「AI統合参謀システム」の最終設計 | ユーザーへ確認 |
