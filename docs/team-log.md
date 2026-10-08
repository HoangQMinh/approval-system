# Team Log — 社内申請・承認システム

> Đọc file này đầu mỗi phiên rồi tiếp tục từ "Việc tiếp theo".
> TL (AI) duy trì file này; Intern commit nó cùng PR.

## Trạng thái hiện tại
- **Sprint**: Sprint 0 (Setup) — bắt đầu 2026-10-06
- **Ticket đang làm**: SETUP-001 (Intern: Minh) — branch `feature/SETUP-001`
- **Tiến độ SETUP-001**: Bước 1–4 ✅ (`91ea1fe`, `91810a4`, `71f95c9`, `7572674`) · Bước 5 🟡 (commit team-log, push, mở PR)
- **Việc tiếp theo**: Minh mở PR `feature/SETUP-001` → `main` → TL review trên PR → Squash and merge

## Ticket
| ID | Tiêu đề | Người làm | Trạng thái | Ghi chú |
|----|---------|-----------|------------|---------|
| SETUP-001 | Dựng khung dự án: app factory, health_bp, GET /health, test, .gitignore, README | Minh | 🟡 In Progress | Repo: github.com/HoangQMinh/approval-system |
| SETUP-002 | Kết nối PostgreSQL (config theo env, docker-compose) | — | ⚪ Backlog | Mở sau khi SETUP-001 merge |
| SETUP-003 | Error handler trả JSON cho 404/405/500 (hiện Flask trả HTML) | — | ⚪ Backlog | Phát hiện khi review Bước 3 SETUP-001 |
| SETUP-004 | Đưa ruff + mypy vào requirements-dev, cấu hình trong pyproject, hướng dẫn chạy trong README | — | ⚪ Backlog (ưu tiên ngay sau SETUP-001) | Minh hỏi vì sao TL thấy lỗi mà máy Minh không thấy |

## Quyết định kỹ thuật của TL (ADR-lite)
| # | Quyết định | Lý do |
|---|-----------|-------|
| D-001 | Python 3.12+, venv tên `.venv` ở root repo | Thống nhất môi trường; `.venv` bị ignore |
| D-002 | Code trong package `app/`; Blueprint ở `app/routes/<domain>.py`; test ở `tests/test_<domain>.py` | Tách theo domain, dễ mở rộng |
| D-003 | Blueprint import **bên trong** `create_app()` | Tránh circular import |
| D-004 | `pytest.ini` có `pythonpath = .` và `testpaths = tests` | Gõ `pytest` ở root không lỗi `No module named 'app'` |
| D-005 | Tách `requirements.txt` (runtime) / `requirements-dev.txt` (`-r requirements.txt` + pytest), pin `==` | Production không cài đồ test; build tái lập được |
| D-006 | `main` chỉ nhận code qua PR; branch `feature/<TICKET-ID>`; commit `[TICKET-ID] Verb ...`; Squash and merge | Lịch sử main sạch |
| D-007 | SETUP-001 chưa đụng DB; PostgreSQL ở SETUP-002 | Mỗi ticket 1 mục đích |
| D-008 | Ticket có 2 phần: **ticket thật** (format Jira, AC tiếng Nhật) + **📚 Phần học**. Phần học giảm theo NĂNG LỰC từng loại kỹ năng (bảng dưới), không theo số sprint | Intern cần giàn giáo, nhưng phải quen ticket thật |
| D-009 | Type hint bắt buộc cho code trong `app/` và **fixture** trong `conftest.py`; **hàm test** (`test_*`) được miễn (sẽ cấu hình ruff bỏ ANN cho `tests/test_*.py` ở SETUP-004) | Fixture là "API dùng chung" được nhiều test gọi → cần rõ kiểu; hàm test do pytest gọi, không ai gọi trực tiếp |

## Mức hỗ trợ theo kỹ năng (D-008)
Đầy đủ → Vừa: xong 1 ticket cùng loại, approve ≤ 2 vòng review, không xin đáp án. Vừa → Nhẹ: thêm 2 ticket cùng loại đạt mức Vừa.

| Kỹ năng | Mức hiện tại | Ticket đã làm |
|---------|-------------|---------------|
| Setup / cấu trúc dự án | Đầy đủ | SETUP-001 (đang làm) |
| Git flow (branch/commit/PR) | Đầy đủ | SETUP-001 (đang làm) |
| CRUD | Đầy đủ | — |
| Validation | Đầy đủ | — |

## Bug / Sự cố
| Ngày | Mô tả | Nguyên nhân | Xử lý | Bài học |
|------|-------|-------------|-------|---------|
| 2026-10-06 | `git clone ... .` lỗi "not an empty directory" | App tự đồng bộ folder `Claude outputs` vào thư mục dự án | TL xóa folder, clone lại OK | Clone vào `.` cần folder trống; kiểm tra bằng `dir /a` |
| 2026-10-07 | TL chạy `git status` từ máy khác để lại `.git/index.lock` | `git status` ghi lock để refresh index; tiến trình không xóa được lock | Đổi tên thành `index.lock.bak`, Minh xóa tay | Tool đọc repo nên dùng `git --no-optional-locks status`; gặp lỗi `index.lock: File exists` → kiểm tra không có git nào đang chạy rồi xóa file lock |

## Retro
_(làm sau khi đóng Sprint 0)_

## Lịch sử phiên
- 2026-10-06: Workspace trống → TL giao lại SETUP-001. Minh kết nối folder `Desktop\PJ\approval-system`; TL review trực tiếp từ folder.
- 2026-10-06: Thống nhất D-008 (ticket thật + phần học giảm dần theo năng lực).
- 2026-10-07: Minh xong clone + branch + Bước 1–2. TL review: 3 điểm sửa nhỏ (README, .gitignore whitespace, newline cuối file).
- 2026-10-07: Commit `91ea1fe` đã push. Minh test README ở C:\temp (clone -b). README review lần 3: tách "setup 1 lần" (README) khỏi "quy trình mỗi ticket" (branch); `pip install flask pytest` chạy được hôm nay nhưng bỏ qua version pin → bug ẩn. Bài học: đã push thì không amend, sửa bằng commit mới.
- 2026-10-07: README review lần 4 đạt (cài bằng `-r requirements-dev.txt`, đã test lại ở C:\temp). TL approve Bước 1–2 → sang Bước 3.
- 2026-10-09: Review Bước 3 lần 1. Đạt: `is not None` (nháp trước dùng `if not test_config` — bug đảo điều kiện, Minh tự sửa), import blueprint trong hàm, 200/404/405 đúng. Cần sửa: `-> dict` sai (mypy: got Response), thiếu status 200 tường minh, PEP 8 (dấu cách sau phẩy, 2 dòng trống trước hàm), README `flask run` chiếm CMD nên curl phải ở cửa sổ khác.
- 2026-10-09: Review Bước 3 lần 2 (`4370058`). README đạt (tách CMD 1/CMD 2). health.py: Minh XÓA type hint thay vì sửa → né lỗi chứ không sửa lỗi (ruff ANN201); 2 lỗi PEP 8 còn nguyên. Bài học: commit chưa push thì được `--amend`; đã push thì commit mới.
- 2026-10-09: Review Bước 3 lần 3 (`fdff09c`). PEP 8 đạt, amend đúng cách. Type hint chép nguyên ví dụ `tuple[str, int]` → mypy: got `tuple[Response, int]`. Bài học: đọc thông báo lỗi — `got` = thực tế, `expected` = cái mình khai báo; ví dụ gợi ý là để hiểu cấu trúc, không để chép.
- 2026-10-09: Review Bước 3 lần 4 (`71f95c9`): ✅ Approve. ruff + mypy sạch, 200/404/405 đúng, Content-Type JSON. Nit (không chặn): thứ tự import `Blueprint, Response, jsonify`. Bước 3 mất 4 vòng review → kỹ năng Setup vẫn ở mức Đầy đủ.
- 2026-10-09: Minh hỏi vì sao TL có thông báo lỗi còn máy Minh không. Giải thích: Python không kiểm type hint lúc chạy; ruff/mypy là công cụ phân tích tĩnh TL chạy riêng (không có trong .venv của Minh). Tạo SETUP-004 để team cùng dùng. Tạm thời: bật Pylance `typeCheckingMode: basic` trong VS Code.
- 2026-10-09: Review Bước 4 lần 1 (`b8fccf3`): pytest 2 passed; mutation test của TL: đổi "ok"→"okk" và 200→201 đều làm test đỏ ✅; trả dict thay jsonify vẫn xanh (đúng — test kiểm hành vi, không kiểm cách cài đặt). Cần sửa: conftest dòng 8 thụt 5 space, fixture thiếu type hint (D-009 mới), commit message "tets", tên test `return` → `returns`.
- 2026-10-09: Review Bước 4 lần 2 (`7572674`): ✅ Approve kèm 1 sửa nhỏ không cần review lại (type hint tham số `app` của fixture `client`). pytest 2 passed, mypy sạch. Nit: thứ tự import (isort) — sẽ tự động hóa ở SETUP-004.
