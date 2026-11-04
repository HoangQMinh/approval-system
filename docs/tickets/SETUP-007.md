# [SETUP-007] CI（GitHub Actions）導入

| | |
|---|---|
| 担当 | **TL** (đổi từ Dev B, 2026-11-01) · thao tác Git: Minh **[Thay TL]** từ clone Dev B · review: Dev B |
| Branch | `feature/SETUP-007` |
| 見積 | 2pt |
| 由来 | Retro Sprint 0 — Try T2 |
| Trạng thái | ✅ Done — PR #8 merge `db6d78e` (2026-11-01) |

## Ticket
**背景**: requirements の記述ミスや、テストが失敗する状態のコミットがレビューまで検知されなかった。

**受け入れ条件 (AC)**
- [ ] PR 作成・更新時、および main への push 時に自動でチェックが実行されること
- [ ] クリーンな環境で `requirements-dev.txt` からインストールすること
- [ ] ruff check / ruff format --check / mypy / pytest を実行し、いずれか失敗で CI が失敗すること
- [ ] README にバッジ、または CI の説明があること
- [ ] README「Quy trình phát triển」のチェックツール数の誤記（3 → 4 コマンド）を修正すること（SETUP-006 持ち越し）

## 📚 Phần học
> **Phân công lại (2026-11-01, D-041):** CI là hạ tầng chung — chọn công cụ, phiên bản action, quyền, required check — nên TL làm. Bước 1 bên dưới giữ lại làm **tài liệu đọc** (mapping + giải thích); file thật là `.github/workflows/ci.yml` do TL viết, đã chạy thử 4 lệnh trên môi trường Linux sạch (8 passed) và `actionlint` sạch.
> Phiên bản action cập nhật so với skeleton: `actions/checkout@v7`, `actions/setup-python@v7` (runtime node24; v4/v5 dùng node20 đang bị GitHub ngừng hỗ trợ).
> Dev B: đọc `ci.yml`, hỏi ❓ dòng nào chưa hiểu (review với vai người học — không cần tìm lỗi).

| Khái niệm | Bên OutSystems |
|---|---|
| CI (Continuous Integration) | Giống **TrueChange + chạy BDD test tự động mỗi lần publish**, nhưng chạy trên một máy sạch của GitHub, không phải máy dev |
| Workflow file `.github/workflows/*.yml` | Định nghĩa "khi nào chạy, chạy gì" |
| `runs-on: ubuntu-latest` | Máy ảo Linux do GitHub cấp, **mới tinh mỗi lần** → phát hiện thiếu khai báo trong requirements |
| Status check | Dấu ✅/❌ hiện trên PR |

### Bước 1 — Workflow
`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  # TODO(1): chạy khi có pull_request
  # TODO(2): chạy khi push lên branch main

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: # TODO(3): đúng D-001
          cache: pip
          cache-dependency-path: requirements*.txt
      # TODO(4): cài từ requirements-dev.txt
      # TODO(5): 4 bước kiểm tra, mỗi bước 1 dòng `- run: ...`
```

- YAML: thụt lề bằng **khoảng trắng** (không dùng Tab), 2 khoảng trắng mỗi cấp.
- Test không cần DB thật (D-026) → CI không cần PostgreSQL.

📝 README: KHÔNG.

### Bước 2 — Chứng minh CI bắt lỗi
1. Push branch, mở PR → tab **Checks** phải xanh ✅.
2. **Mutation:** thêm tạm 1 commit làm hỏng (ví dụ thêm import thừa) → push → CI phải **đỏ ❌**. Chụp/ghi lại link run đỏ cho PR body. Rồi revert commit đó (`git revert <hash>`) và push → xanh lại.

📝 README: CÓ — thêm badge CI ở đầu README:
`![CI](https://github.com/HoangQMinh/approval-system/actions/workflows/ci.yml/badge.svg)`
và 1 câu ở mục Kiểm tra code: "4 lệnh này cũng chạy tự động trên CI cho mọi PR".

### Bước 3 — PR + [Thay TL] bật status check bắt buộc
- PR dùng template (SETUP-006).
- Sau merge, **[Thay TL]**: Settings → Rules → `protect-main` → bật **Require status checks to pass** → chọn check `check` (tên job). Từ đó PR đỏ CI không merge được.

📝 README: KHÔNG thêm.

## Definition of Done
- [ ] PR có CI xanh; có bằng chứng CI từng đỏ khi cố tình làm hỏng
- [ ] Badge CI trong README
- [ ] README mục Quy trình phát triển không còn ghi "3 công cụ" (hint: bỏ con số, trỏ tới mục 4 CONTRIBUTING)
- [ ] Ruleset yêu cầu status check `check`

## Lịch sử thay đổi
- 2026-10-26: TL giao (chờ SETUP-006).
- 2026-10-30: SETUP-006 merge → giao. Thêm AC sửa lỗi README sót từ PR #7. Làm theo `CONTRIBUTING.md` từ bước 1 → 6 (tự kiểm tra tài liệu SETUP-006).
- 2026-11-01: Minh góp ý CI nên do TL làm → đổi 担当 sang TL (D-041). TL viết `ci.yml` (checkout@v7, setup-python@v7, job `check`) + README (badge, câu CI ở Kiểm tra code, sửa dòng "3 công cụ"). Đã kiểm: actionlint sạch; 4 lệnh chạy trên clone sạch `bd2c066` → pass.
- 2026-11-01: PR #8 merge → `db6d78e`. CI: xanh `40dc2b4`, mutation đỏ đúng bước ruff check `b3e41a9`, revert xanh `0347185`; run push trên main ✅. [Thay TL] đã bật required status check `check` trong `protect-main` (đã kiểm qua API).
