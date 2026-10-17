# Team Log — 社内申請・承認システム

> Đọc file này đầu mỗi phiên rồi tiếp tục từ "Việc tiếp theo".
> TL (AI) duy trì file này; Intern commit nó cùng PR.

## Trạng thái hiện tại
- **Sprint**: Sprint 0 (Setup) — bắt đầu 2026-10-06
- **Ticket đang làm**: — (SETUP-001 ✅ Done, PR #1 squash merge → `be464e7`)
- **Team**: Dev A = Minh (folder `approval-system`) · Dev B = Minh (folder `approval-system-devb`) · TL/PM/QA/Ops = AI
- **Tiến độ Sprint 0**: SETUP-001 ✅ · SETUP-004 ✅ · SETUP-003 🟢 approved, chờ merge · SETUP-002 ⚪ (kế tiếp)
- **Việc tiếp theo**: Dev A commit+push team-log → sửa 2 nit PR body → squash merge #2 → dọn branch; cả 2 clone pull main · TL giao SETUP-002 · Minh còn nợ: 実績 SETUP-001/003/004, 質問票

## Ticket
| ID | Tiêu đề | Người làm | Trạng thái | 見積 (SP / giờ) | 実績 (giờ) | Ghi chú |
|----|---------|-----------|------------|----------------|-----------|---------|
| SETUP-001 | Dựng khung dự án: app factory, health_bp, GET /health, test, .gitignore, README | Minh | ✅ Done (2026-10-10) | 2 SP / 4h (TL ước cho người quen tay) | chờ Minh báo | PR #1, squash `be464e7` |
| SETUP-002 | Kết nối PostgreSQL (config theo env, docker-compose) | — | ⚪ Backlog | — | — | Mở sau khi SETUP-001 merge |
| SETUP-003 | Error handler trả JSON cho 404/405/500 (hiện Flask trả HTML) | Dev A | 🟢 PR #2 final approve (2026-10-17) — chờ merge | 2 SP / ~6h | — | Phát hiện khi review Bước 3 SETUP-001 |
| SETUP-004 | Đưa ruff + mypy vào requirements-dev, cấu hình trong pyproject, hướng dẫn chạy trong README (PR #3, squash `dbea3b8`) | Dev B | ✅ Done (2026-10-17) | 2 SP / ~5h | — | Minh hỏi vì sao TL thấy lỗi mà máy Minh không thấy |

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
| D-010 | Team 2 dev: mỗi dev 1 folder clone riêng + `git config --local user.name` riêng ("Minh (Dev A)" / "Minh (Dev B)"); 1 tài khoản GitHub | Mô phỏng làm việc song song, conflict thật trên cùng 1 máy |
| D-011 | `docs/team-log.md` chỉ được sửa/commit từ clone **Dev A**; Dev B không đụng file này | Tránh conflict vô nghĩa trên file log (ngoài đời log nằm ở Jira/wiki) |
| D-012 | Khi `main` có commit mới mà branch đang làm chưa có: cập nhật bằng `git merge origin/main` vào feature branch (chưa dùng rebase); TL quyết thứ tự merge PR | Merge an toàn, không viết lại lịch sử đã push; rebase học sau |
| D-013 | GitHub: bật ruleset cho `main` (bắt buộc PR, cấm push thẳng/force push), chỉ cho Squash merge, tự xóa branch sau merge | Chặn lỗi người từ 2 clone; giữ D-006 bằng công cụ thay vì trí nhớ |
| D-014 | Minh học vai TL bằng **quan sát**: mỗi tin của TL có mục **🎓 Góc TL** (TL vừa làm gì, vì sao, có lựa chọn nào khác). TL-AI làm toàn bộ việc TL; không giao bài tập/việc TL cho Minh | Minh muốn biết TL cần làm gì, chưa muốn đảm nhận |
| D-015 | Cỡ ticket: 1 ticket = 1 mục đích = 1 PR; làm ≤ 1–2 ngày; PR review được trong ~15–30 phút (thường < 200–300 dòng thay đổi); quá cỡ thì TL tách. Ticket cho Minh chia 2–3 bước | Minh thấy SETUP-001 nặng; ticket nhỏ → review nhanh, ít conflict |
| D-016 | Ước lượng: TL ước mỗi ticket bằng Story Point (1,2,3,5,8 — độ lớn tương đối) + quy ra giờ cho người làm; dev báo 実績 giờ khi xong; sau vài ticket dùng tỉ lệ 実績/見積 để ước chính xác hơn | Không có chuẩn chung toàn ngành; ước lượng tốt dựa trên dữ liệu thực tế của chính team |
| D-017 | Định dạng lỗi API: body `{"error": <tên lỗi HTTP>, "message": <mô tả>}` + status code tương ứng; lỗi 500 không bao giờ trả chi tiết exception ra ngoài, chi tiết chỉ ghi log | Client xử lý lỗi thống nhất; không lộ thông tin nội bộ |
| D-018 | Thứ tự merge Sprint 0: SETUP-004 (công cụ) merge TRƯỚC, SETUP-003 SAU. Dev A được mở PR sớm dưới dạng **Draft** (GitHub khóa nút merge) và chờ 004 merge, rồi `git merge origin/main`, chạy ruff/mypy, sửa, push lại | Công cụ chất lượng là nền: code mới phải qua công cụ trước khi vào main |
| D-019 | Thay đổi máy móc (auto-fix/format của tool) để ở commit riêng, message bắt đầu bằng `[TICKET] Apply ruff ...` | Reviewer lướt nhanh commit máy móc, tập trung commit có logic |
| D-020 | `requirements*.txt` là nguồn sự thật của môi trường: không ai `pip install` lẻ thư viện ngoài file; khi `main` đổi requirements, mọi dev chạy lại `pip install -r requirements-dev.txt` sau khi pull/merge | Môi trường các dev luôn giống nhau, không "máy em chạy được" |

## Mức hỗ trợ theo kỹ năng (D-008)
Đầy đủ → Vừa: xong 1 ticket cùng loại, approve ≤ 2 vòng review, không xin đáp án. Vừa → Nhẹ: thêm 2 ticket cùng loại đạt mức Vừa.

| Kỹ năng | Mức hiện tại | Ticket đã làm |
|---------|-------------|---------------|
| Setup / cấu trúc dự án | Đầy đủ (SETUP-001: >2 vòng review → chưa lên mức Vừa) | SETUP-001 |
| Git flow (branch/commit/PR) | Đầy đủ (đã làm trọn 1 vòng: branch → amend → PR → squash → dọn branch) | SETUP-001 |
| CRUD | Đầy đủ | — |
| Validation | Đầy đủ | — |

## Bug / Sự cố
| Ngày | Mô tả | Nguyên nhân | Xử lý | Bài học |
|------|-------|-------------|-------|---------|
| 2026-10-17 | (Ghi nhận, không phải lỗi) Merge `origin/main` vào SETUP-003: conflict ở README | 2 ticket song song cùng thêm mục cuối README — TL đã dự đoán (D-018) | Giữ cả 2 mục, sắp theo thứ tự quy trình dev → tham chiếu API; commit merge chỉ chứa merge | Conflict tài liệu dễ; luôn đọc lại file Git tự merge; commit merge không lẫn sửa khác |
| 2026-10-12 | Clone Dev A có thêm `app/pytest.ini` (untracked, giống hệt bản ở root, tạo 10-10) | `pytest.ini` bị kéo nhầm từ root vào `app/` (ngày 10-10), rồi root được `git restore` | `del app\pytest.ini` | File untracked lạ = dấu hiệu thao tác nhầm; `git add .` sẽ gom luôn |
| 2026-10-12 | Clone Dev A: `pytest` lỗi `No module named 'app'` | `pytest.ini` bị xóa ngoài ý muốn (`git status` báo `D pytest.ini`) | `git restore pytest.ini` | Đầu mỗi ticket chạy `git status`: working tree chỉ được chứa thay đổi mình chủ ý |
| 2026-10-06 | `git clone ... .` lỗi "not an empty directory" | App tự đồng bộ folder `Claude outputs` vào thư mục dự án | TL xóa folder, clone lại OK | Clone vào `.` cần folder trống; kiểm tra bằng `dir /a` |
| 2026-10-07 | TL chạy `git status` từ máy khác để lại `.git/index.lock` | `git status` ghi lock để refresh index; tiến trình không xóa được lock | Đổi tên thành `index.lock.bak`, Minh xóa tay | Tool đọc repo nên dùng `git --no-optional-locks status`; gặp lỗi `index.lock: File exists` → kiểm tra không có git nào đang chạy rồi xóa file lock |

## Retro
_(retro chính thức khi đóng Sprint 0)_

Ghi chú cho retro — rút ra từ SETUP-001:
- Sửa theo review bằng trí nhớ → sót điểm. Cách làm: dò lại từng gạch đầu dòng trước khi báo "xong".
- Gặp lỗi type hint thì xóa type hint → né lỗi chứ không sửa. Cách làm: đọc dòng `got ...` của công cụ.
- Chép nguyên ví dụ gợi ý → sai kiểu. Ví dụ là để hiểu cấu trúc.
- **Lặp lại lần 2 (SETUP-003):** được yêu cầu *sửa* docstring lỗi thời → *xóa* luôn docstring (giống lần xóa type hint ở SETUP-001). Quy tắc: review nói "sửa X" thì X phải còn và đúng; xóa chỉ khi review nói xóa.
- Tốt: tự phát hiện README có lệnh vô lý (`git switch`) nhờ chạy thử trên máy sạch; PR body có output thật + 異常系.

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
- 2026-10-10: PR #1 squash merge (`be464e7`), branch local + remote đã xóa, `main` pytest 2 passed. PR body sửa đạt (変更内容 đủ, curl -i, 対象外 đủ 3 ticket). SETUP-001 Done. PM gửi 要件 Sprint 1 (休暇申請) — chờ Minh viết 質問票.
- 2026-10-10: Minh đổi mô hình: team 2 dev (Minh code cả Dev A và Dev B), 1 tài khoản GitHub, 2 tên commit. TL chốt D-010…D-013, giao SETUP-003 (Dev A) ‖ SETUP-004 (Dev B) chạy song song.
- 2026-10-12: Clone Dev B OK (Minh (Dev B), venv 3.12.6, pytest 2 passed, VS Code đỏ). Clone Dev A: danh tính OK nhưng `pytest.ini` bị xóa. Ruleset `protect-main` chưa được tạo (API: main không có rule) — mới cấu hình, chưa bấm Create; merge methods trong ruleset còn để cả 3. Chốt D-014 (lộ trình TL).
- 2026-10-12: Minh chỉ muốn quan sát vai TL (không làm bài tập TL) → sửa D-014. Minh hỏi cỡ ticket → chốt D-015.
- 2026-10-12: Ruleset `protect-main` active (chặn xóa, chặn force push, bắt buộc PR, chỉ squash) — kiểm qua API. `pytest.ini` đã restore (pytest 2 passed) nhưng còn `app/pytest.ini` thừa. Chốt D-016 (ước lượng SP + giờ, ghi 見積/実績).
- 2026-10-13: TL giao SETUP-003 (Dev A) ‖ SETUP-004 (Dev B), có bản tham chiếu TL đã chạy thử (5 passed, ruff/mypy sạch). Chốt D-017 (format lỗi), D-018 (004 merge trước), D-019 (commit máy móc tách riêng).
- 2026-10-13: Minh hỏi SETUP-004 có phải cài cho cả Dev A không → D-020; Dev A chỉ cài ruff/mypy sau khi merge main (sau khi 004 merge). Bổ sung việc cho Dev B: README ghi "đổi requirements → cài lại".
- 2026-10-15: Review SETUP-003 (Dev A) lần 1, trước commit: 5 passed, mypy sạch, mutation "lộ str(error)" → test đỏ ✅, log có traceback ✅. Cần sửa: tên lỗi 500 `INTERNAL_SERVER_ERROR` lệch D-017 (404 dùng "Not Found") — test 500 không kiểm field `error` nên lọt; dòng 106 ký tự (E501 sau SETUP-004); docstring `create_app` chưa nhắc error handler; README mục lỗi chưa có ví dụ/code block.
- 2026-10-15: Review SETUP-003 lần 2 (`80fe767`, chưa push): README mục lỗi rất tốt. Còn: field `error` của 500 thành "Unhandled exception" (lẫn log message với tên lỗi HTTP; README ghi "Internal Server Error" → code và README mâu thuẫn); docstring `create_app` bị xóa thay vì sửa. Định dạng còn lại để `ruff format` xử lý sau khi merge 004.
- 2026-10-15: Review SETUP-003 lần 3 (`84f50c4`): ✅ code approve — 500 trả "Internal Server Error" khớp D-017 + README, docstring khôi phục và cập nhật đúng. Dự báo sau khi merge 004: format + mypy `test_errors.py:29` (json có thể None). Dev B chưa bắt đầu → PR 003 phải chờ (bị chặn bởi phụ thuộc).
- 2026-10-15: PR #2 (Draft) mô tả đạt: title có mã ticket, dòng chờ merge, 500 ghi nhận bằng test, 対象外 theo mã ticket. Nit: 2 dòng 対象外 thiếu `- ` nên hiển thị dính 1 dòng.
- 2026-10-16: Dev B: pin ruff==0.17.1, mypy==2.4.0; commit cấu hình `7b0adf5`; đã chạy `ruff check --fix` + `ruff format` → diff thuần máy móc (3 file), cả 3 tool sạch. Quy tắc trả lời Minh: lỗi có `[*]` → để tool sửa; ruff không `[*]` và mypy → sửa tay.
- 2026-10-16: Dev B commit auto-fix `763b9f1` (thuần máy móc, pytest 2 passed). README review lần 1: thiếu dòng D-020 ở mục Cài đặt; mục "Kiểm tra code" ghi sai thời điểm chạy ("sau khi đổi cấu hình" thay vì "trước khi mở PR"); thêm ghi chú mypy phải sửa tay. Điểm cộng: tự thêm phần quy trình sửa (fix → diff → pytest).
- 2026-10-17: README SETUP-004 review lần 2: ✅ approve — có mục con "Cập nhật dependencies" (D-020), thời điểm chạy "trước khi mở PR", giải thích từng lệnh, ghi chú mypy sửa tay. Nit: câu mypy nên đặt trong phần sửa lỗi thay vì cuối file.
- 2026-10-17: Review PR #3 (SETUP-004, `6f49cff`, mergeable clean): code ✅. Mô tả PR cần sửa: 概要 ghi nhầm SETUP-003 (copy-paste), thiếu mục 影響範囲 (bắt buộc — PR đổi môi trường cả team), 変更内容 không nhắc 3 file code bị auto-fix, 対象外 "ない" → 「なし」.
- 2026-10-17: PR #3 squash merge (`dbea3b8`), mô tả đã sửa đủ (影響範囲, レビュー観点 D-009). Dev B dọn branch + cài lại requirements OK. TL chạy thử merge main vào SETUP-003 trên bản clone riêng: conflict DUY NHẤT ở README (2 mục mới cùng thêm cuối file); `app/__init__.py` Git tự merge (đúng logic, thiếu 1 dòng trống); sau merge: 5 passed, ruff check sạch, format 2 file, mypy `test_errors.py:29`.
- 2026-10-17: Review lại PR #2 sau merge main (`bc76dbf`): commit tách đúng (merge `eb6cc7c` / format `1fc2af0` / mypy `bc76dbf`), sửa mypy bằng `assert data is not None` ✅, 5 passed, ruff+format+mypy sạch, PR mergeable clean, diff PR chỉ còn 5 file của Dev A. ✅ Final approve. Nit PR body: 2 checkbox chưa tick, 対象外 còn ghi SETUP-004 "đang làm" (đã xong).
