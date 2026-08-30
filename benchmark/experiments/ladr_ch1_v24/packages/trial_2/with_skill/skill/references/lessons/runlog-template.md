# Extraction Run Log

This file is append-only and belongs to the private run directory. It is not
part of the reader-facing submission. Add one record for each deterministic
failure or repair before starting the next acceptance round.

## Round 1 — YYYY-MM-DD HH:MM +0800

- **触发（程序原话 / exit code）：** `SELF-CHECK FAIL` — `<paste the exact message>` (exit `<n>`)
- **根因：** `<what the evidence shows; do not infer beyond it>`
- **教训（绝对规则）：** `<a reusable rule stated as must/must not>`
- **证据：** `<selfcheck item, path, line, hash, or command output>`
- **验证：** `<exact rerun command>` → `<PASS/FAIL and relevant output>`

### 回合对账

- **上轮缺陷认领：** `<block_id or defect>` — repaired / refuted / not applicable; evidence: `<...>`
- **selfcheck 重跑：** `<command>` → `<exit code>`
- **完整验收：** `<validator/score command>` → `<result>`
- **状态解释：** 结构检查通过不代表内容覆盖已确认；记录 `structural_status`、`coverage_status` 和 `human_review_status`。
- **本轮新失败：** `<none or append a new record below>`
