# [SETUP-004] 静的解析ツール（ruff / mypy）導入

| | |
|---|---|
| 担当 | Dev B |
| 見積 | 2pt |
| Trạng thái | ✅ Done — PR #3, squash `dbea3b8` (2026-10-17) |

## Ticket
**背景**: コーディング規約・型ヒントの確認がレビュー時の目視に依存している。ツールで自動チェックできるようにする。

**受け入れ条件 (AC)**
- [x] ruff / mypy が requirements-dev.txt にバージョン固定で追加されていること
- [x] 設定が pyproject.toml に集約されていること（テスト関数は型ヒント対象外：D-009）
- [x] 既存コードが ruff check / ruff format --check / mypy を全てパスすること
- [x] README に実行方法が記載されていること

## Kết quả
- `pyproject.toml`: ruff (E, W, F, I, ANN; miễn ANN cho `tests/test_*.py`), mypy (`files = ["app", "tests"]`, `check_untyped_defs = true`).
- README mục "Kiểm tra code" + "Cập nhật dependencies" (D-020).

## Bài học chính
- Lỗi có `[*]` → để `ruff check --fix` sửa; `ruff format` không bao giờ sửa tay; mypy luôn sửa tay.
- Thay đổi máy móc để commit riêng (D-019).
- PR đổi môi trường cả team phải có mục 影響範囲.
