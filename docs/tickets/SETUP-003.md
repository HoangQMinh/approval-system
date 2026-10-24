# [SETUP-003] APIエラーレスポンスのJSON統一

| | |
|---|---|
| 担当 | Dev A |
| 見積 | 2pt |
| Trạng thái | ✅ Done — PR #2, squash `830a54b` (2026-10-17) |

## Ticket
**背景**: 404/405/500 などのエラー時に HTML が返却されている。API 利用側が統一的に処理できるよう JSON に統一する。

**受け入れ条件 (AC)**
- [x] 未定義パス → 404 / JSON `{"error": "Not Found", "message": ...}`
- [x] 許可されていないメソッド → 405 / JSON
- [x] 想定外の例外 → 500 / JSON。例外の詳細はレスポンスに含めない
- [x] 想定外の例外はログに出力する
- [x] テスト追加・全件パス

## Kết quả
- `app/errors.py`: `register_error_handlers(app)` — handler `HTTPException` + handler `Exception` (log `"Unhandled exception"`, trả message chung).
- Định dạng lỗi: D-017. README mục "Định dạng lỗi API".
- PR mở dạng **Draft** để chờ SETUP-004 merge trước (D-018), sau đó merge `origin/main`, giải conflict README, chạy ruff/mypy.

## Bài học chính
- Field `error` (cho client) ≠ log message (cho người điều tra).
- Đổi hành vi hàm → sửa docstring (Args/Returns/Raises), không xóa docstring.
- Commit merge chỉ chứa merge; sửa do tool tách commit riêng (D-019).
- Lỗi mypy `Any | None`: lấy ra biến, `assert ... is not None`, rồi mới dùng.
