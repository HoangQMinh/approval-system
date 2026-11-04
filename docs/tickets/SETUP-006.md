# [SETUP-006] プルリクエストテンプレート導入

| | |
|---|---|
| 担当 | Dev B (🔴) |
| Branch | `feature/SETUP-006` |
| 見積 | 1pt |
| 由来 | Retro Sprint 0 — Try T1, T3 |
| Trạng thái | ✅ Done — PR #7 merge `bd2c066` (2026-10-30) |

## Ticket
**背景**: PR 本文を過去の PR からコピーしていたため、チケット番号の誤記・ドキュメント更新漏れが発生した（PR #3, #5）。

**受け入れ条件 (AC)**
- [ ] `.github/pull_request_template.md` を作成し、PR 作成時に本文へ自動挿入されること
- [ ] 既存の見出し（概要 / 変更内容 / テスト結果 / 影響範囲 / レビュー観点 / 対象外）を含むこと
- [ ] 提出前チェックリストを含むこと（下記）
- [ ] README に PR 作成ルールへの導線があること
- [ ] `CONTRIBUTING.md` を作成し、チケット着手〜マージ後までの Git 手順を記載すること（2026-10-28 追加）

## 📚 Phần học
| Khái niệm | Bên OutSystems |
|---|---|
| PR template (`.github/pull_request_template.md`) | Giống **mẫu Release notes / checklist deploy** chuẩn của team trong LifeTime — ai tạo deployment cũng dùng cùng một mẫu |
| Thư mục `.github/` | Thư mục đặc biệt GitHub đọc để lấy cấu hình (template, CI) |
| `CONTRIBUTING.md` | Tài liệu **"Development guideline / quy tắc publish"** của team OutSystems (ai được publish, phải Compare & Merge trước khi publish…). GitHub tự hiện link tới file này khi có người mở PR/issue |
| `git switch main` + `git pull` trước khi tạo branch | Trong Service Studio: mở module bản **mới nhất trên server** trước khi sửa — nếu sửa trên bản cũ, lúc 1-Click Publish sẽ phải Merge |
| Branch `feature/<ID>` | OutSystems không có branch cho từng dev (mọi người sửa chung 1 module, merge lúc publish). Gần nhất: tự clone module ra làm thử rồi mới đưa về |

### Bước 1 — Tạo template
`.github/pull_request_template.md`:

```markdown
<!-- Title: [TICKET-ID] タイトル（チケットと同じ） -->

## 概要
<!-- TODO: PR này làm gì (1–2 câu). KHÔNG copy từ PR khác -->

## 変更内容
<!-- TODO: liệt kê theo thành phần; thay đổi ngoài phạm vi ticket ghi rõ -->

## テスト結果
<!-- TODO: dán output thật -->

## 影響範囲
<!-- requirements / .env / docker-compose thay đổi? Không có → 特になし -->

## レビュー観点
<!-- Điểm muốn reviewer soi kỹ, hoặc 特になし -->

## 対象外（別チケット）
<!-- Mã ticket, hoặc 特になし -->

## 提出前チェック
- [ ] TODO: (≥ 7 mục — gợi ý ở dưới)
```

Checklist phải bao gồm ít nhất (anh tự viết bằng tiếng Nhật hoặc Việt):
- Title có đúng mã ticket của PR này
- `pytest` / `ruff check` / `ruff format --check` / `mypy` đều đạt
- Docstring đã cập nhật nếu hàm đổi hành vi
- README đã cập nhật nếu cách cài / chạy / API thay đổi
- `.env.example` đã cập nhật nếu thêm/đổi biến môi trường
- `git stash list` trống, không còn thay đổi chưa commit
- Mỗi commit có tiền tố `[TICKET-ID]`

📝 README: KHÔNG.

### Bước 2 — `CONTRIBUTING.md`: thao tác Git cho mỗi ticket
Mục đích: dev mới (hoặc chính em sau 2 tuần) mở 1 file là biết phải gõ gì, theo thứ tự nào — không phải lục chat hay team-log.
Nội dung = **những gì team đã làm thật ở Sprint 0** (D-006, D-019, D-027, D-028, D-032). Anh không viết sẵn lệnh — em điền TODO.

Skeleton `CONTRIBUTING.md` (ở root repo, cạnh README):

```markdown
# Quy trình phát triển (Git)

> Áp dụng cho mọi ticket. `<ID>` = mã ticket (vd `LEAVE-001`).
> Branch: `feature/<ID>` cho tính năng/setup, `fix/<ID>` cho bug.

## 1. Bắt đầu ticket mới
<!-- TODO(1): 4 lệnh theo thứ tự: về main → lấy code mới nhất → kiểm tra stash trống → tạo branch -->
<!-- TODO(2): sau khi pull, nếu requirements*.txt / .env.example / docker-compose.yml đổi thì phải làm gì -->

## 2. Trong lúc code
<!-- TODO(3): add + commit; format commit message (D-006) + 1 ví dụ -->
<!-- TODO(4): tách commit do tool sửa (ruff --fix / ruff format) và commit sửa tay (D-019) -->
<!-- TODO(5): push lần đầu (tạo upstream) và các lần sau; cách kiểm tra branch đã có upstream chưa -->

## 3. main có thay đổi trong lúc đang làm
<!-- TODO(6): lấy main mới về branch của mình (team dùng merge, chưa dùng rebase); có conflict thì làm gì; chạy lại test -->

## 4. Trước khi mở PR
<!-- TODO(7): 4 công cụ phải đạt; working tree sạch; stash trống -->
<!-- TODO(8): khi nào mở Draft PR; PR body dùng template, KHÔNG copy PR cũ -->

## 5. Sửa theo review
<!-- TODO(9): đã push rồi thì sửa bằng cách nào; khi nào được amend -->

## 6. Sau khi PR được merge (Squash and merge)
<!-- TODO(10): về main, pull, xác nhận commit squash đã có trên main -->
<!-- TODO(11): xoá branch local — vì sao phải dùng -D chứ không phải -d -->
<!-- TODO(12): đang có thay đổi dở (vd docs/) thì thứ tự stash → … (D-027) -->
<!-- TODO(13): xem PR vừa merge đổi file nào (D-028) -->

## 7. Lỗi thường gặp
<!-- TODO(14): ≥ 3 lỗi team đã gặp ở Sprint 0 + cách sửa (gợi ý: code trên main, commit mà quên push, quên stash pop) -->
```

**Cú pháp cần dùng** (em đều đã gõ ở Sprint 0 — xem lại team-log nếu quên):

| Lệnh | Dùng ở mục |
|---|---|
| `git switch main` / `git switch -c <branch>` | 1, 6 |
| `git pull` / `git fetch` / `git merge origin/main` | 1, 3, 6 |
| `git stash` / `git stash list` / `git stash pop` | 1, 4, 6 |
| `git status` / `git add <file>` / `git commit -m "..."` | 2, 4, 5 |
| `git push -u origin <branch>` / `git push` / `git branch -vv` | 2 |
| `git log --oneline -3` | 6 |
| `git branch -D <branch>` | 6 |
| `git diff --stat ORIG_HEAD HEAD` | 6 |
| `pip install -r requirements-dev.txt` | 1 |

**Quy ước viết (Markdown):** mỗi bước là code block ` ```bash ` để copy được; mỗi lệnh 1 dòng; giải thích ngắn bằng comment `#` cuối dòng hoặc 1 câu trên block. Không dùng `&&` nối nhiều lệnh — người mới cần thấy từng lệnh chạy ra gì.

**Tự kiểm tra:** dùng chính file này để làm SETUP-007 (bước 1 → 6). Chỗ nào làm theo mà kẹt → sửa file luôn trong PR SETUP-007.

📝 README: CÓ — thêm mục `## Quy trình phát triển` **ngắn** (≤ 5 dòng): link tới `CONTRIBUTING.md`, nhắc PR dùng template, nhắc 4 công cụ trước khi mở PR. Không chép lại lệnh git vào README (1 nguồn duy nhất — giống D-020).

### Bước 2b — Kiểm tra template
GitHub chỉ đọc PR template từ **default branch (`main`)**. Vì vậy PR SETUP-006 sẽ **không** tự điền (template chưa có trên main) → PR này copy nội dung template vào body bằng tay. Kiểm tra thật ở **PR SETUP-007**: bấm **Compare & pull request** → body phải tự điền.

### Bước 3 — PR
Không đụng `docs/` (D-011). Merge **đầu tiên** trong đợt 1.

## Definition of Done
- [x] Sau khi merge: PR kế tiếp (SETUP-007, #8) thấy template tự điền
- [ ] Checklist ≥ 7 mục, bao gồm các mục bắt buộc ở trên
- [ ] README có mục Quy trình phát triển (ngắn, link tới CONTRIBUTING.md)
- [ ] `CONTRIBUTING.md` đủ 7 mục, không còn TODO; có thể làm theo từ đầu đến cuối mà không cần hỏi

## Lịch sử thay đổi
- 2026-10-26: TL giao.
- 2026-10-28: Thêm AC + Bước 2 `CONTRIBUTING.md` (thao tác Git từ lúc nhận ticket đến sau merge) theo đề xuất của Minh. Ước lượng giữ 1pt (chỉ là tài liệu, lệnh đã biết). → D-039
- 2026-10-30: Sửa Bước 2b + DoD: template chỉ tự điền khi đã có trên `main`, nên kiểm tra ở PR SETUP-007 (lỗi ticket của TL).
- 2026-10-30: PR #7 squash merge → `bd2c066`. Còn sót 1 lỗi tài liệu (README ghi "3 công cụ", đúng là 4 lệnh): bản sửa chưa push trước khi merge → chuyển sang SETUP-007.
- 2026-11-01: Xác nhận PR #8 tự điền template → DoD đủ.
