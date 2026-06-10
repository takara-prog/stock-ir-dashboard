# X AI Monitor

X（旧 Twitter）のキーワード検索結果を毎日自動収集し、週 1 回 Claude AI が分析レポートを作成して Telegram に送信する Web アプリです。

---

## ⚠️ このアプリについて（必ずお読みください）

**これは self-host MVP です。**

| 項目 | 内容 |
|------|------|
| 動作形態 | **各自の環境で `docker compose up` して使う**（self-host） |
| 対象ユーザー | 自分でリポジトリを clone し、自分の API キーを設定して使う人 |
| 前提 | API キーは**各利用者が自分で用意する** |
| ではないもの | 複数ユーザーが共有する hosted SaaS ではない |

### ⚠️ セキュリティ注意

- **`.env` を GitHub に絶対にコミットしない**。`.gitignore` に `.env` が含まれていることを確認すること。
- `/config` 画面は API キー・設定値を直接変更できるため、**公開サーバー上で動かす場合は認証を必ず追加すること**。self-host（localhost）で使う分には問題ない。
- `DB_PATH` のデータは Docker volume に永続化される。コンテナを削除する際はデータの扱いに注意。

### hosted版について

公開 URL で複数ユーザーが使える hosted 版は**次フェーズで検討**します。  
hosted 版には認証・ユーザー分離・API キー管理の設計が別途必要なため、今バージョンには含まれません。

---

## 機能

| 機能 | 内容 |
|------|------|
| ツイート収集 | 毎日指定時刻にキーワードでツイートを 10 件収集し SQLite に保存 |
| 週次分析 | 7 日分のツイートを Claude AI（Haiku）で分析 |
| Telegram 通知 | 分析結果を Telegram Bot で自動送信 |
| Web ダッシュボード | ツイート一覧・分析結果・ステータスをブラウザで確認 |
| 設定画面 | キーワード・API キーをブラウザから変更可能 |

---

## セットアップ（約 10 分）

### 必要なもの

- Docker + Docker Compose（[インストール](https://docs.docker.com/get-docker/)）
- 下記 API キー（取得方法は後述）

| API | プラン | 用途 |
|-----|--------|------|
| X Developer Portal | **Basic（$100/月）以上** | ツイート検索 |
| Anthropic Claude | 従量課金 | 週次分析（数円/回） |
| Telegram Bot | 無料 | 分析結果の通知 |

> **X API について**：ツイート全文検索（`search_recent_tweets`）は Free ティアでは利用不可です。
> テストデータ機能を使えば X API なしで分析フローは検証できます。

---

### 手順

#### 1. クローン

```bash
git clone https://github.com/<your-org>/stock-ir-dashboard.git
cd stock-ir-dashboard/x-ai-monitor
```

#### 2. .env を作成

```bash
cp .env.example .env
```

`.env` を開いて必要な値を入力します（最低限 `ANTHROPIC_API_KEY` と `TELEGRAM_*` があれば動作確認可能）。

> **⚠️ `.env` は絶対に Git にコミットしないこと。** `.gitignore` に `.env` が含まれていますが、`git add -f` 等で強制追加しないよう注意してください。

#### 3. 起動

```bash
docker compose up -d
```

http://localhost:8000 にアクセスして画面が表示されれば成功です。

#### 4. 初回設定（オプション）

http://localhost:8000/config でブラウザから API キーとキーワードを設定できます。

---

## API キー取得方法

### X (Twitter) Bearer Token

1. https://developer.x.com/en/portal/dashboard にアクセス
2. プロジェクトを作成 → **Keys and Tokens** → **Bearer Token** をコピー
3. `.env` の `TWITTER_API_KEY` に貼り付け

### Anthropic API Key

1. https://console.anthropic.com/settings/keys にアクセス
2. **Create Key** → コピー
3. `.env` の `ANTHROPIC_API_KEY` に貼り付け

### Telegram Bot Token と Chat ID

```bash
# 1. Telegram で @BotFather に /newbot と送信 → Token を取得
# 2. 自分のボットにメッセージを送る
# 3. 以下の URL で Chat ID を確認
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
# → result[0].message.chat.id が Chat ID
```

---

## 使い方

### ページ一覧

| URL | 内容 |
|-----|------|
| `/` | 直近 7 日のツイート一覧 + 最新 AI 分析 |
| `/config` | キーワード・API キー・スケジュール設定 |
| `/status` | 収集履歴・スケジューラー状態・手動実行 |

### 手動実行

`/status` ページの「手動実行」から収集・分析をいつでも実行できます。

### テストデータで動作確認

X API キーがない場合でも `/status` → **テストデータ生成** を押すと
7 日分 × 10 件のダミーツイートが生成されます。
その後 **今すぐ分析** を押すと Claude API による分析フローが検証できます。

---

## 設定値一覧

| 変数 | デフォルト | 説明 |
|------|-----------|------|
| `TWITTER_API_KEY` | — | Twitter Bearer Token |
| `ANTHROPIC_API_KEY` | — | Claude API キー |
| `TELEGRAM_BOT_TOKEN` | — | Telegram Bot Token |
| `TELEGRAM_CHAT_ID` | — | Telegram 送信先 Chat ID |
| `MONITOR_KEYWORD` | `株` | 検索キーワード |
| `COLLECT_HOUR` | `8` | 収集時刻（JST、0〜23） |
| `ANALYZE_WEEKDAY` | `MON` | 分析曜日（MON〜SUN） |
| `DB_PATH` | `/data/tweets.db` | SQLite ファイルパス |

設定は `/config` 画面から変更した場合、DB に保存されて .env より優先されます。

---

## DB スキーマ

```sql
-- ツイート保存テーブル
CREATE TABLE tweets (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id       TEXT UNIQUE NOT NULL,  -- X上のツイートID
    text           TEXT NOT NULL,
    likes          INTEGER DEFAULT 0,
    retweets       INTEGER DEFAULT 0,
    collected_date TEXT NOT NULL,         -- YYYY-MM-DD（JST基準）
    author_id      TEXT DEFAULT '',
    created_at     TEXT DEFAULT '',
    raw_json       TEXT DEFAULT ''        -- APIレスポンス原文
);

-- 分析結果保存テーブル
CREATE TABLE analyses (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    analyzed_at  TEXT NOT NULL,           -- UTC ISO 8601
    period_start TEXT NOT NULL,           -- YYYY-MM-DD
    period_end   TEXT NOT NULL,           -- YYYY-MM-DD
    keyword      TEXT NOT NULL,
    result       TEXT NOT NULL            -- Claude の分析テキスト
);

-- ランタイム設定（/config からの変更を保存）
CREATE TABLE settings (
    key        TEXT PRIMARY KEY,
    value      TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### Claude 送信フォーマット（圧縮）

7 日分のツイートを以下の形式に圧縮して 1 リクエストで送信します：

```
tw:{本文50文字}|l:{likes}|rt:{retweets}|d:{MMDD}
```

---

## ディレクトリ構成

```
x-ai-monitor/
├── .env.example        # 設定テンプレート
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── app/
    ├── main.py         # FastAPI ルーティング
    ├── config.py       # 設定読み込み（.env + DB）
    ├── database.py     # SQLite CRUD
    ├── collector.py    # X API ツイート収集
    ├── analyzer.py     # Claude API 分析
    ├── notifier.py     # Telegram 通知
    ├── scheduler.py    # APScheduler ジョブ管理
    └── templates/      # Jinja2 HTML テンプレート
```

---

## よくある質問

**Q: X API の Basic プランに入らないといけませんか？**
A: ツイート収集機能を使う場合は必要です。テストデータ機能を使えば Claude 分析と Telegram 通知だけ検証できます。

**Q: キーワードを複数設定できますか？**
A: 現バージョンでは 1 キーワードのみです。スペース区切りや OR 演算子（`株 OR NISA`）で擬似的に複数対応できます。

**Q: データはどこに保存されますか？**
A: `./data/tweets.db`（SQLite）に保存されます。Docker volume でコンテナを再起動しても消えません。

**Q: 複数人で共有して使えますか？**
A: このバージョンは self-host MVP のため、**1人が自分の環境で使う想定**です。複数ユーザーでの共有・公開 URL での提供は対応していません。

**Q: `/config` を公開サーバーで動かすのは安全ですか？**
A: 安全ではありません。`/config` は API キーを直接変更できるため、公開サーバーで動かす場合は Basic 認証等を追加してください。**localhost での self-host 運用であれば問題ありません。**

**Q: `.env` ファイルを GitHub にコミットしてもいいですか？**
A: **絶対にしないでください。** `.gitignore` に `.env` が含まれていますが、`git add -f .env` 等で強制追加しないよう注意してください。API キーが公開されると即座に不正利用されます。
