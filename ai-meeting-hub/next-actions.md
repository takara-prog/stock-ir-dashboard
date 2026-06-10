# 次アクション (Next Actions)

> 優先度ルール: `priority-rule.md` を参照

---

## アクティブ

| 優先度 | 作業名 | 担当 | 最初の一手 | 完了条件 | 期限 | 状態 |
|---|---|---|---|---|---|---|
| P1 | x-ai-monitor README self-host MVP補完 | Claude（実行者） | x-ai-monitor ブランチのREADMEに self-host明記・セキュリティ注意を追記 | README読んでdocker compose upできる・self-hostである旨明記 | 2026-06-10 | 進行中 |
| P3 | Windows側 work-agents へのZIP配置 | ユーザー | GitHubからZIPDL→ai-meeting-hubのみコピー | `C:\Users\bellc\work-agents\ai-meeting-hub` に23ファイル存在 | 次回PC操作時 | 未着手 |

---

## 詳細

### [P1] x-ai-monitor README self-host MVP補完

**担当:** Claude（実行者）  
**期限:** 2026-06-10  
**状態:** 進行中

**背景・目的:**  
転職用ポートフォリオとして x-ai-monitor を self-host MVP として説明できる状態にする。READMEに「self-host前提」「.env はGitHubに公開しない」「/configの認証注意」を明記する。

**最初の一手:**  
`claude/x-ai-monitor-public-refactor-j8h028` ブランチに切り替えて README.md を編集する

**完了条件:**  
- [ ] README に「self-host MVPである」旨が明記されている
- [ ] `.env` をGitHubに公開しない警告が入っている
- [ ] `/config` を公開サーバーで使う場合の認証注意が入っている
- [ ] hosted版は次フェーズと明記されている
- [ ] `auditor-check.md` のチェックを通過した

**依存関係:**  
- 前提: DEC-2026-0610-001（self-host MVPで完結の決定）
- ブロッカー: なし

**完了後の処理:**  
- [ ] `work-report-template.md` で報告
- [ ] `decision-log.md` の DEC-2026-0610-001 を「完了」に更新

---

### [P3] Windows側 work-agents へのZIP配置

**担当:** ユーザー  
**期限:** 次回PC操作時  
**状態:** 未着手

**最初の一手:**  
ブラウザで PR #4 のブランチZIPをダウンロードし、`ai-meeting-hub/` だけを `C:\Users\bellc\work-agents\` にコピー

**完了条件:**  
- [ ] `C:\Users\bellc\work-agents\ai-meeting-hub` に23ファイルが存在する

---

---

## 完了済み

| 完了日 | 作業名 | 担当 | レポート |
|---|---|---|---|
| | | | |

---

## 保留中

| 保留日 | 作業名 | 保留理由 | 再開条件 |
|---|---|---|---|
| | | | |
