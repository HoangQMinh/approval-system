# Team Log — 社内申請・承認システム

> Đọc file này đầu mỗi phiên rồi tiếp tục từ "Việc tiếp theo".
> TL (AI) duy trì file này; Intern commit nó cùng PR.

## Trạng thái hiện tại
- **Sprint**: Sprint 0 (Setup) — bắt đầu 2026-10-06
- **Ticket đang làm**: — (chờ 質問票 + SETUP-002)
- **Team**: Dev A = Minh (folder `approval-system`) · Dev B = Minh (folder `approval-system-devb`) · TL/PM/QA/Ops = AI
- **Tiến độ Sprint 0**: ✅ Tất cả ticket Done · ✅ Release v0.1.0 (tag → `9357e6f`) · 🔍 QA: BUG-001 · Retro chờ sau BUG-001
- **Việc tiếp theo**: Dev A sửa BUG-001 (`fix/BUG-001`) → v0.1.1 → Retro Sprint 0 (KPT) → Sprint 1 planning

## Ticket
| ID | Tiêu đề | Người làm | Trạng thái | 見積 (SP / giờ) | 実績 (giờ) | Ghi chú |
|----|---------|-----------|------------|----------------|-----------|---------|
| SETUP-001 | Dựng khung dự án: app factory, health_bp, GET /health, test, .gitignore, README | Minh | ✅ Done (2026-10-10) | 2 SP / 4h (TL ước cho người quen tay) | — | PR #1, squash `be464e7` |
| SETUP-002 | PostgreSQL 16 bằng docker-compose + config đọc từ biến môi trường (`DATABASE_URL`, `.env.example`) | Dev A | ✅ Done (2026-10-21, PR #4 squash `dc2f8c3`) | 3 SP / ~8h | — | Mở sau khi SETUP-001 merge |
| SETUP-005 | Kết nối DB bằng SQLAlchemy (`app/db.py`) + `/health` kiểm tra DB (DB chết → 503) + test | Dev B | ✅ Done (2026-10-24, PR #5 squash `9357e6f`) | 3 SP / ~8h | — | Tách từ SETUP-002; làm song song nhờ hợp đồng D-024 |
| BUG-001 | 405 thiếu header `Allow` (regression từ SETUP-003) | Dev A | 🟢 Code approved | 1 SP | — | QA phát hiện trên v0.1.0; sửa → v0.1.1 |
| SETUP-003 | Error handler trả JSON cho 404/405/500 (hiện Flask trả HTML) | Dev A | ✅ Done (2026-10-17, PR #2 squash `830a54b`) | 2 SP / ~6h | — | Phát hiện khi review Bước 3 SETUP-001 |
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
| D-016 | Ước lượng: TL ước mỗi ticket bằng Story Point (1,2,3,5,8) + quy ra giờ. Minh **không báo 実績** (Minh chọn bỏ qua, 2026-10-17) → cột 実績 để trống | Không có chuẩn chung; Minh chỉ cần hiểu cách TL ước lượng |
| D-017 | Định dạng lỗi API: body `{"error": <tên lỗi HTTP>, "message": <mô tả>}` + status code tương ứng; lỗi 500 không bao giờ trả chi tiết exception ra ngoài, chi tiết chỉ ghi log | Client xử lý lỗi thống nhất; không lộ thông tin nội bộ |
| D-018 | Thứ tự merge Sprint 0: SETUP-004 (công cụ) merge TRƯỚC, SETUP-003 SAU. Dev A được mở PR sớm dưới dạng **Draft** (GitHub khóa nút merge) và chờ 004 merge, rồi `git merge origin/main`, chạy ruff/mypy, sửa, push lại | Công cụ chất lượng là nền: code mới phải qua công cụ trước khi vào main |
| D-019 | Thay đổi máy móc (auto-fix/format của tool) để ở commit riêng, message bắt đầu bằng `[TICKET] Apply ruff ...` | Reviewer lướt nhanh commit máy móc, tập trung commit có logic |
| D-020 | `requirements*.txt` là nguồn sự thật của môi trường: không ai `pip install` lẻ thư viện ngoài file; khi `main` đổi requirements, mọi dev chạy lại `pip install -r requirements-dev.txt` sau khi pull/merge | Môi trường các dev luôn giống nhau, không "máy em chạy được" |
| D-021 | 質問票 với khách do TL (kiêm BrSE) phụ trách; dev chỉ tham gia ở bước **refinement**: đọc ticket/spec và hỏi TL chỗ chưa rõ, không hỏi khách trực tiếp. Q&A lưu ở `docs/qa/`, commit cùng ticket đầu tiên của sprint (chỉ từ clone Dev A) | Minh nêu: dev chủ yếu code theo spec đã thống nhất; đúng với vai intern |
| D-022 | Tài liệu thiết kế nhẹ trong repo: `docs/design/` (状態遷移, テーブル定義, API一覧) do TL viết trước Sprint 1 planning; mỗi ticket **link** tới mục liên quan (design, `docs/qa/`, D-xxx). Dev trước khi code: đọc ticket → mở các link → đọc code hiện có ở chỗ sẽ sửa → hỏi TL nếu chưa rõ | Ticket chỉ nói "làm gì"; thiết kế nói "vì sao / toàn cảnh"; dev cần cả hai |
| D-023 | Truy cập DB: **SQLAlchemy 2.0** (không dùng Flask-SQLAlchemy) + driver **psycopg 3**; PostgreSQL 16 chạy bằng docker-compose (chỉ môi trường dev); migration bằng Alembic ở ticket sau; cấu hình qua biến môi trường, file `.env` (không commit) + `.env.example` (commit) | ORM chuẩn ngành, session tường minh → học transaction; Alembic là chuẩn migration; bí mật không vào Git |
| D-024 | **Hợp đồng giữa SETUP-002 và SETUP-005**: config key `DATABASE_URL` (dạng `postgresql+psycopg://user:pass@host:port/db`) có trong `app.config`; SETUP-005 chỉ đọc key này, test truyền qua `test_config` | Thống nhất giao diện trước → 2 dev làm song song dù có phụ thuộc |
| D-025 | Thứ tự merge: SETUP-002 (config/DB) TRƯỚC, SETUP-005 SAU (merge main về, giải conflict). docker-compose đặt `name: approval` cố định để 2 clone dùng chung 1 container/volume; cổng máy **5433** (tránh Postgres khác đang chiếm 5432) | Nền trước; 2 clone trên 1 máy không tranh cổng |
| D-026 | Test không cần DB thật: dùng `DATABASE_URL=sqlite+pysqlite:///:memory:` trong `test_config` (chỉ cho health `SELECT 1`); case DB chết dùng URL tới cổng đóng `127.0.0.1:1`. Test với PostgreSQL thật quyết định ở Sprint 1 (khi có bảng) | Test nhanh, không phụ thuộc Docker; chiến lược DB test thật để khi có schema |
| D-027 | Vì TL ghi team-log trực tiếp vào clone Dev A, sau khi PR merge Dev A dọn branch theo quy trình: `git stash` → `git switch main` → `git pull` → `git stash pop` → `git branch -D ...`. Thay đổi team-log nằm chờ trên main (chưa commit) và đi theo sang branch ticket kế tiếp | Không commit lên branch đã merge/xóa; không commit thẳng main (D-006) |
| D-028 | Sau khi merge PR có 影響範囲, TL đăng **📢 thông báo** (ngoài đời: Slack) nêu việc mỗi dev phải làm. Dev vẫn tự kiểm sau mỗi `git pull`: `git diff --stat ORIG_HEAD HEAD`, thấy đổi `requirements*.txt` / `.env.example` / `docker-compose.yml` / `pyproject.toml` thì làm bước tương ứng trong README | 3 lớp: thông báo (đẩy) + PR/README (tra cứu) + tự kiểm (thói quen); app fail-fast là lưới cuối |
| D-029 | `DATABASE_URL` dùng **`127.0.0.1`** (không dùng `localhost`) + **`?connect_timeout=3`**; URL trong test cũng phải có `connect_timeout` (`=1`) | Windows thử IPv6 `::1` trước mà container chỉ bind IPv4 → chậm 3s/treo; psycopg mặc định chờ 130s, Windows không báo cổng đóng ngay → test 130s, curl treo |
| D-030 | Nội dung ticket lưu ở `docs/tickets/<ID>.md` (ngoài đời: Jira). TL cập nhật file ticket ngay khi kế hoạch đổi + ghi "Lịch sử thay đổi"; chỉ commit từ clone Dev A (như D-011) | Minh không phải tìm lại ticket trong chat; tránh lỗi "kế hoạch đổi mà ticket không đổi" |
| D-031 | Release = **tag có chú thích** `vMAJOR.MINOR.PATCH` trên `main` + **GitHub Release** (release note liệt kê PR). Sprint 0 = `v0.1.0`. Chưa có server → QA test trên đúng commit của tag | Đánh dấu chính xác "bản nào đã giao cho QA/khách"; quay lại được bản đó bất cứ lúc nào |
| D-032 | Bug: ticket `BUG-xxx`, branch `fix/BUG-xxx`, **viết test tái hiện (đỏ) trước rồi mới sửa**; sửa xong release PATCH (`v0.1.x`). Người tạo ra đoạn code lỗi ưu tiên nhận sửa | Test đỏ trước chứng minh test bắt được bug, chống tái phát; tác giả hiểu code nhất |

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
| 2026-10-24 | TL chạy `git fetch` từ phía mình để lại `.git/objects/maintenance.lock` | Lệnh git có ghi của TL không xóa được file lock | Đổi tên thành `.git/stale-maintenance-lock`, Minh xóa tay | TL chỉ dùng lệnh git chỉ-đọc (`--no-optional-locks`), không fetch/pull từ phía TL |
| 2026-10-24 | Dev B: `curl /health` treo, CMD Flask không in log; test 503 mất 130s | psycopg 3 timeout mặc định 130s + Windows không báo cổng đóng ngay; `localhost` → thử `::1` trước, container chỉ bind 127.0.0.1 (đo: localhost 3s, 127.0.0.1 tức thì) | D-029: URL dùng 127.0.0.1 + connect_timeout | Werkzeug in log SAU khi trả response (không log ≠ không tới); con số lạ (130s) luôn có cơ chế; health check bắt buộc có timeout |
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
- **Lặp lại lần 3 (SETUP-002):** code đổi hành vi (`create_app` giờ raise `RuntimeError`) nhưng docstring không cập nhật — dù ticket đã nhắc. Quy tắc: đổi hành vi hàm → sửa docstring cùng lúc (Args/Returns/**Raises**).
- **Lặp lại lần 2 (SETUP-003):** được yêu cầu *sửa* docstring lỗi thời → *xóa* luôn docstring (giống lần xóa type hint ở SETUP-001). Quy tắc: review nói "sửa X" thì X phải còn và đúng; xóa chỉ khi review nói xóa.
- **Copy-paste mô tả PR mà không đọc lại** (PR #3 ghi SETUP-003, PR #5 chép 概要 của SETUP-002). Quy tắc: copy template thì đọc lại từng dòng trước khi bấm Create.
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
- 2026-10-17: PR #2 squash merge `830a54b`. Cả 2 clone `main` = `origin/main` = `830a54b`, sạch. SETUP-003 Done. Minh bỏ qua 実績 (sửa D-016). Bắt đầu 質問票 Sprint 1.
- 2026-10-17: Minh hỏi dev có phải tìm điểm mơ hồ không → chốt D-021 (TL/BrSE lo 質問票, dev hỏi ở refinement). TL gửi 質問票 16 câu, PM trả lời ngay: đổi 種別 (振替休日 thay 欠勤), mở rộng quá khứ đến hôm trước, backlog: hủy đơn đã duyệt (Sprint 2), quản lý số ngày phép, duyệt thay khi vắng. Lưu `docs/qa/sprint1-qa.md` (untracked, commit cùng ticket Sprint 1 đầu tiên).
- 2026-10-17: Minh hỏi dev có cần đọc tài liệu thiết kế không → chốt D-022 (docs/design/ + ticket link tài liệu).
- 2026-10-17: TL lên kế hoạch phần còn lại Sprint 0: tách SETUP-002 thành SETUP-002 (Dev A: docker-compose + config) và SETUP-005 (Dev B: kết nối DB + health), chốt D-023 (SQLAlchemy 2.0 + psycopg 3, Postgres 16 Docker), D-024 (hợp đồng `DATABASE_URL`).
- 2026-10-18: Docker Desktop OK (lỗi đầu: Engine chưa chạy). TL giao SETUP-002 (Dev A) ‖ SETUP-005 (Dev B). Bản tham chiếu TL: 8 passed, ruff/mypy sạch, SQLAlchemy+psycopg nối thật được PostgreSQL 16, compose file hợp lệ. Dự báo conflict sau khi 002 merge: `app/__init__.py`, `tests/conftest.py` (cả 2 cùng thêm DATABASE_URL) — lần đầu conflict trong CODE.
- 2026-10-19: Review SETUP-002 (Dev A) trước commit: đã chuyển sang branch `feature/SETUP-002` ✅, `python-dotenv==1.2.2` đã sửa và cài ✅, 7 passed, 4 tool sạch, thứ tự env → test_config → kiểm tra đúng ✅, `.env` bị ignore ✅. Điểm cộng: compose bind `127.0.0.1:5433` (DB không lộ ra LAN). Cần sửa: docstring `create_app` thiếu `Raises`; README mục "Khởi động DB" đặt cuối file (sau tham chiếu API) — phải đứng trước "Chạy ứng dụng".
- 2026-10-19: Review PR #4 (SETUP-002, `25a9dc6`, mergeable clean): code ✅ (docstring có Raises, README đúng thứ tự, 3 commit, message đã sửa). Mô tả PR: 概要/変更内容 ghi "kết nối DB" sai (PR không kết nối DB — đó là SETUP-005), 対象外 nên ghi SETUP-005. Dev B CHƯA bắt đầu SETUP-005 → TL quyết: merge #4 trước, Dev B tạo branch từ main mới (không còn conflict dự kiến; bỏ bước tự thêm DATABASE_URL vào conftest).
- 2026-10-21: PR #4 squash merge `dc2f8c3`. Dev A không switch được sang main vì team-log có thay đổi chưa commit (do TL ghi sau commit cuối) → chốt D-027 (dùng git stash).
- 2026-10-21: Minh hỏi sau pull làm sao biết phải cài gì → D-028. TL đăng thông báo cho PR #4.
- 2026-10-24: Dev B sửa test 503 đúng (app riêng). Điều tra: test 130s = timeout mặc định psycopg; giả thuyết localhost/IPv6 được Minh đo xác nhận (3s vs tức thì) → D-029.
- 2026-10-24: Minh yêu cầu lưu ticket vào repo → tạo `docs/tickets/` (README + SETUP-001/002/003/004/005), D-030. Chưa commit — sẽ commit cùng ticket kế tiếp của Dev A.
- 2026-10-24: Review PR #5 (SETUP-005, `7e4bd1d`): code ✅ (đủ 4 điểm sửa). Mô tả: 概要 chép nhầm từ SETUP-002 (lần 2 copy-paste sai ticket, lần 1 ở PR #3) → ghi retro.
- 2026-10-24: PR #5 squash `9357e6f`. Cả 2 clone: main = `9357e6f`, `.env` dùng 127.0.0.1 + connect_timeout, 8 passed. **Sprint 0: hết ticket.** Chốt D-031 (release bằng tag + GitHub Release).
- 2026-10-24: Release v0.1.0 (tag annotated → `9357e6f`, GitHub Release có note PR #1–#5). QA test hộp đen trên v0.1.0 → BUG-001 (405 thiếu Allow, regression từ SETUP-003; bằng chứng: output curl trong PR #1 vs PR #2). Chốt D-032.
- 2026-10-25: Review BUG-001 trước commit: ✅ — sửa đúng (chép header trừ Content-Type), test 405 kiểm Allow, mutation xác nhận test bắt được bug; 8 passed, 4 tool sạch. Test 404 cũng được thêm guard None (đồng nhất 3 test).
