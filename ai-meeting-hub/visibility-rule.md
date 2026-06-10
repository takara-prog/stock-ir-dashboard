# 公開可否分類 (Visibility Rule)

> ファイル・情報・コードの公開可否を判断するための基準。  
> GitHubへのpush、ポートフォリオへの掲載、外部共有をする前に確認する。

---

## 分類定義

| 分類 | ラベル | 意味 |
|---|---|---|
| 公開可 | `public` | 誰でも見てよい。GitHubにpushできる |
| ポートフォリオ可 | `portfolio` | 採用向けに見せてよいが、一般公開は慎重に |
| 非公開 | `private` | 社内・チーム内のみ。GitHubのprivateリポジトリまで |
| 機密 | `sensitive` | リポジトリにも入れない。ローカルのみ |

---

## 各ファイルの分類

### ai-meeting-hub/ フォルダ全体

**分類:** `public`  
**理由:** APIキーや機密情報を含まないMarkdownテンプレート群

---

### 分類別の対応

#### `public`
- GitHubにpush: OK
- PRに含める: OK
- 外部に共有: OK
- スクリーンショットをSNSに投稿: OK

#### `portfolio`
- GitHubにpush: OK（privateリポジトリ推奨）
- 採用担当者に見せる: OK
- 一般公開: 要判断
- スクリーンショットをSNSに投稿: 注意

#### `private`
- GitHubのprivateリポジトリ: OK
- publicリポジトリへのpush: NG
- 外部共有: NG

#### `sensitive`
- リポジトリへのpush: NG（`.gitignore` に追加）
- ローカルのみ保持
- 例: `.env`, APIキー, パスワード, 個人情報

---

## 絶対に `sensitive` のもの

- `.env` ファイル
- APIキー（OpenAI, Anthropic, Google等）
- パスワード・シークレット
- 個人情報（氏名・メールアドレス等）
- 会社の機密情報

---

## pushする前のチェック

- [ ] `sensitive` なファイルが含まれていないか
- [ ] `.gitignore` に機密ファイルが登録されているか
- [ ] APIキーをコード内にハードコードしていないか
- [ ] コメントにパスワードや機密情報が含まれていないか

---

## ファイル別分類台帳

| ファイル | 分類 | 備考 |
|---|---|---|
| `ai-meeting-hub/*.md` | `public` | テンプレートのみ |
| `.env` | `sensitive` | 作成禁止 |
| APIキー | `sensitive` | 作成禁止 |
