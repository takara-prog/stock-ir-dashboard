# 次アクション (Next Actions)

> 優先度ルール: `priority-rule.md` を参照

---

## アクティブ

| 優先度 | 作業名 | 担当 | 最初の一手 | 完了条件 | 期限 | 状態 |
|---|---|---|---|---|---|---|
| P0 | x-ai-monitor の展開方針を決める | ユーザー + Claude | MTG-2026-0610-001.md を使って self-host/hosted を比較する | 今日やる範囲とやらない範囲が決まる | 2026-06-10 | **完了** |
| P1 | x-ai-monitor README self-host MVP補完 | Claude（実行者） | x-ai-monitor ブランチのREADMEに self-host明記・セキュリティ注意を追記 | README読んでdocker compose upできる・self-hostである旨明記 | 2026-06-10 | **完了** |
| P1 | x-ai-monitor スクリーンショット / デモ動画作成 | ユーザー | docker compose up → /status → テストデータ → 分析の流れを記録 | ポートフォリオに使える画像・動画が手元にある | 今週中 | 未着手 |
| P3 | Windows側 work-agents へのZIP配置 | ユーザー | GitHubからZIPDL→ai-meeting-hubのみコピー | `C:\Users\bellc\work-agents\ai-meeting-hub` に24ファイル存在 | 次回PC操作時 | **完了** |

---

## 詳細

### [P1] x-ai-monitor スクリーンショット / デモ動画作成

**担当:** ユーザー  
**期限:** 今週中  
**状態:** 未着手

**背景・目的:**  
転職用ポートフォリオとして x-ai-monitor の動作を視覚的に示す素材を用意する。

**最初の一手:**  
`docker compose up` で起動 → `/status` → テストデータ生成 → 今すぐ分析 の流れをスクリーンショットまたは画面録画で記録する

**完了条件:**  
- [ ] `docker compose up` で起動できることを確認した
- [ ] `/status` → テストデータ生成 → 分析 の流れを記録した
- [ ] ポートフォリオに使える画像 or 動画が手元にある

**依存関係:**  
- 前提: Docker Desktop がインストール済みであること
- ブロッカー: なし

**完了後の処理:**  
- [ ] `work-report-template.md` で報告

---

### [完了] x-ai-monitor README self-host MVP補完

**担当:** Claude（実行者）  
**完了日:** 2026-06-10  
**状態:** 完了

**背景・目的:**  
転職用ポートフォリオとして x-ai-monitor を self-host MVP として説明できる状態にする。READMEに「self-host前提」「.env はGitHubに公開しない」「/configの認証注意」を明記した。

**完了条件:**  
- [x] README に「self-host MVPである」旨が明記されている
- [x] `.env` をGitHubに公開しない警告が入っている
- [x] `/config` を公開サーバーで使う場合の認証注意が入っている
- [x] hosted版は次フェーズと明記されている
- [x] 作業完了レポートが残っている

**完了後の処理:**  
- [x] 作業完了レポート確認済み
- [x] `decision-log.md` に DEC-2026-0610-001 記録済み

---

### [完了] Windows側 work-agents へのZIP配置

**担当:** ユーザー  
**完了日:** 2026-06-10  
**状態:** 完了

**最初の一手:**  
ブラウザで PR #4 のブランチZIPをダウンロードし、`ai-meeting-hub/` だけを `C:\Users\bellc\work-agents\` にコピー

**完了条件:**  
- [x] `C:\Users\bellc\work-agents\ai-meeting-hub` に24ファイルが存在する
- [x] `MTG-2026-0610-001.md` が存在する
- [x] 既存 `C:\Users\bellc\x-ai-monitor` は変更なし

---

## 完了済み

| 完了日 | 作業名 | 担当 | レポート |
|---|---|---|---|
| 2026-06-10 | x-ai-monitor の展開方針を決める | ユーザー + Claude | MTG-2026-0610-001.md / DEC-2026-0610-001 |
| 2026-06-10 | x-ai-monitor README self-host MVP補完 | Claude | 作業完了レポート確認済み |
| 2026-06-10 | Windows側 work-agents へのZIP配置 | ユーザー | 配置確認済み（24ファイル）|

---

## 保留中

| 保留日 | 作業名 | 保留理由 | 再開条件 |
|---|---|---|---|
| | | | |
