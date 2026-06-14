# 再現性ルール (Reproducibility)

> 同じ手順を踏めば同じ結果が得られる状態を保つためのルール。

---

## 基本原則

1. **決定はすべて記録する** → `decision-log.md`
2. **却下もすべて記録する** → `rejected-ideas.md`
3. **「なんとなく」で作らない** → `creation-gate.md` を通過すること
4. **AIのセッションが変わっても同じ判断ができる** → `handoff-template.md` を使う
5. **手順は文書に残す** → このファイル群が手順書

---

## AIへの指示を再現するために

### 毎回の指示に含めること

```
# 前提
- プロジェクト: [プロジェクト名]
- 現在の作業: [next-actions.md の作業名]
- 関連決定: [decision-log.md の関連DEC-ID]

# 絶対禁止
- 既存プロジェクト（README.md, index.html, netlify.toml）の変更
- APIキー・.envの作成
- スコープ外の実装

# 今回やること
[具体的な指示]
```

### セッションをまたぐとき

1. `handoff-template.md` を埋める
2. 新しいAIに渡す前文として貼り付ける
3. 渡す前に `anti-drift-check.md` でスコープを確認

---

## ファイル変更の再現性

### 変更前にやること

- [ ] `creation-gate.md` のチェックを通過した
- [ ] `decision-log.md` に決定を記録した
- [ ] `next-actions.md` に作業を追加した

### 変更後にやること

- [ ] `work-report-template.md` で報告した
- [ ] `change-summary-template.md` で差分を記録した
- [ ] `auditor-check.md` で監査を通過した

---

## 判断の再現性

問い: 「なぜこの構成にしたのか？」に答えられるか？

- Yes → `decision-log.md` の DEC-ID を示せる
- No → 再現性がない。今から `decision-log.md` に記録する

---

## 再現性の自己チェック

| チェック項目 | OK | NG |
|---|---|---|
| 全決定に DEC-ID がある | | |
| 却下した案が `rejected-ideas.md` にある | | |
| 直近3件の作業に `work-report-template.md` がある | | |
| `handoff-template.md` なしにAIを切り替えていない | | |
