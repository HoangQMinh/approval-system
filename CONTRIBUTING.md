# Quy trình phát triển (Git)

> Áp dụng cho mọi ticket. `<ID>` = mã ticket (ví dụ: `LEAVE-001`).
> Branch: `feature/<ID>` cho tính năng/setup, `fix/<ID>` cho bug.

## 1. Bắt đầu ticket mới

Chạy lần lượt các lệnh sau:

```bash
git switch main
git pull
git stash list
git switch -c feature/<ID>
```

- Trước khi tạo branch, kiểm tra `git status` để đảm bảo working tree sạch. Nếu còn thay đổi chưa commit, hãy commit hoặc stash trước.
- `git stash list` dùng để kiểm tra các stash đang tồn tại. Không tự ý `stash pop` các stash cũ không thuộc ticket hiện tại.
- Với bug, thay `feature/<ID>` bằng `fix/<ID>`.
- Sau khi pull, kiểm tra các file cấu hình có thay đổi:
  - `requirements*.txt`: cài đặt lại dependencies bằng `pip install -r requirements-dev.txt` (hoặc file requirements tương ứng).
  - `.env.example`: đối chiếu và cập nhật `.env` local; không commit `.env`.
  - `docker-compose.yml`: kiểm tra thay đổi cấu hình và cập nhật services bằng `docker compose up -d` khi cần.

## 2. Trong lúc code

### 2.1. Add và commit

Chỉ add những file thuộc ticket hiện tại:

```bash
git status
git add <file>
git commit -m "[<ID>] <Description>"
```

**Commit message (D-006):**

Format:

```text
[<ID>] <Short description>
```

Ví dụ:

```text
[LEAVE-001] Add leave request validation
[SETUP-004] Add ruff and mypy configuration
```

- Một commit nên tập trung vào một mục đích thay đổi.
- Description ngắn gọn, mô tả hành động hoặc nội dung thay đổi.
- Không commit trực tiếp vào `main`.

### 2.2. Tách commit do tool sửa và sửa bằng tay (D-019)

Khi sử dụng `ruff --fix` hoặc `ruff format`, cần tách thay đổi tự động và thay đổi sửa bằng tay thành các commit riêng.

Ví dụ:

```bash
# Commit các thay đổi do Ruff tự động sửa
git add <file>
git commit -m "[<ID>] Apply ruff auto-fixes"

# Sau đó sửa code bằng tay
git add <file>
git commit -m "[<ID>] Fix validation logic"
```

Không gộp thay đổi tự động của tool và thay đổi logic do developer tự sửa vào cùng một commit nếu có thể tách riêng.

### 2.3. Push branch

**Lần push đầu tiên:** tạo upstream tracking branch.

```bash
git push -u origin feature/<ID>
```

**Các lần push tiếp theo:**

```bash
git push
```

Kiểm tra branch đã có upstream chưa:

```bash
git branch -vv
```

Branch có thông tin tracking như `[origin/feature/<ID>]` nghĩa là đã có upstream. Nếu chưa có, sử dụng `git push -u origin feature/<ID>`.

## 3. main có thay đổi trong lúc đang làm

Cập nhật `main` mới nhất vào branch hiện tại bằng merge (team không sử dụng rebase):

```bash
git fetch origin
git merge origin/main
```

- Nếu không có conflict, tiếp tục kiểm tra và chạy lại test.
- Nếu có conflict:
  1. Dùng `git status` để xem các file bị conflict.
  2. Mở từng file và giải quyết các đoạn conflict.
  3. Xóa các marker `<<<<<<<`, `=======`, `>>>>>>>`.
  4. Kiểm tra lại nội dung sau khi resolve.
  5. Add các file đã resolve và hoàn tất merge:

```bash
git add <file>
git commit
```

- Chạy lại đầy đủ 4 công cụ kiểm tra trước khi tiếp tục.
- Không dùng `git rebase` hoặc force push để xử lý conflict.

## 4. Trước khi mở PR

Phải đảm bảo tất cả điều kiện sau:

1. **4 công cụ kiểm tra đều PASS:**

   ```bash
   ruff check .
   ruff format --check .
   mypy
   pytest
   ```

2. Working tree sạch:

   ```bash
   git status
   ```

   Kết quả phải là `nothing to commit, working tree clean`.

3. Stash không còn thay đổi đang chờ xử lý của ticket:

   ```bash
   git stash list
   ```

   Nếu có stash liên quan đến ticket, phải xác định và xử lý trước khi mở PR.

4. Branch đã được push lên remote.

**Draft PR:**

- Mở Draft PR khi muốn nhận feedback sớm về thiết kế, hướng triển khai hoặc giải pháp kỹ thuật dù code chưa hoàn chỉnh.
- Draft PR chưa được xem là sẵn sàng để merge.
- Chỉ chuyển sang Ready for review khi hoàn tất implementation, kiểm tra và đáp ứng yêu cầu của ticket.

**PR body:**

- Luôn sử dụng PR template có sẵn trong repository.
- Điền đầy đủ nội dung theo template: mục đích, thay đổi, cách kiểm tra và các thông tin liên quan.
- Không copy nội dung từ PR cũ vì mỗi ticket có phạm vi và nội dung khác nhau.

## 5. Sửa theo review

Nếu branch đã được push lên remote, sửa code và tạo commit mới:

```bash
git add <file>
git commit -m "[<ID>] Address review comments"
git push
```

- Không cần tạo branch mới cho các lần sửa review.
- Không amend commit đã push lên remote vì có thể làm thay đổi lịch sử commit mà người khác đang sử dụng.
- Chỉ sử dụng `git commit --amend` khi commit chưa được push và cần chỉnh sửa commit cuối cùng.
- Không force push để cập nhật PR.

## 6. Sau khi PR được merge (Squash and merge)

### 6.1. Cập nhật main và xác nhận merge

Sau khi PR được Squash and merge:

```bash
git switch main
git pull
git log --oneline -5
```

- Xác nhận commit squash của PR đã xuất hiện trên `main`.
- Không dựa vào số lượng commit cũ của feature branch để xác nhận vì Squash and merge tạo một commit mới trên `main`.

### 6.2. Xóa branch local

```bash
git branch -D feature/<ID>
```

Sử dụng `-D` thay vì `-d` vì Squash and merge tạo commit mới trên `main`, không giữ nguyên các commit gốc của feature branch. Git có thể vẫn đánh giá branch cũ chưa được merge đầy đủ và từ chối `-d`.

Chỉ xóa branch sau khi đã xác nhận PR được merge thành công.

### 6.3. Xử lý thay đổi dở dang (D-027)

Nếu đang có thay đổi local chưa commit, ví dụ thay đổi trong `docs/`, cần giữ lại trước khi chuyển branch:

```bash
# 1. Cất các thay đổi, bao gồm cả untracked files
git stash push -u -m "WIP: docs changes"

# 2. Về main và cập nhật code
git switch main
git pull

# 3. Xác nhận commit squash đã có trên main
git log --oneline -5

# 4. Xóa branch ticket đã merge
git branch -D feature/<ID>

# 5. Tạo branch mới cho ticket tiếp theo
git switch -c feature/<NEW_ID>

# 6. Khôi phục thay đổi đã stash
git stash pop
```

- Kiểm tra `git status` sau khi khôi phục.
- Nếu có conflict, giải quyết và kiểm tra lại nội dung.
- Nếu `stash pop` thành công, stash tương ứng sẽ được xóa khỏi danh sách.
- Nếu có conflict, stash vẫn được giữ lại; không xóa thủ công trước khi xác nhận đã khôi phục đầy đủ.

### 6.4. Kiểm tra các file thay đổi sau khi pull (D-028)

Sau khi cập nhật `main` bằng `git pull`, sử dụng:

```bash
git diff --name-only ORIG_HEAD HEAD
```

- `ORIG_HEAD`: vị trí HEAD trước khi pull.
- `HEAD`: vị trí HEAD hiện tại sau khi pull.
- Lệnh hiển thị danh sách file thay đổi trong toàn bộ lần cập nhật, kể cả khi pull về nhiều PR hoặc nhiều commit.

Muốn xem nội dung chi tiết của tất cả thay đổi:

```bash
git diff ORIG_HEAD HEAD
```

**Lưu ý:** Thực hiện kiểm tra ngay sau `git pull`, trước khi chạy các thao tác Git khác có thể cập nhật `ORIG_HEAD`.

## 7. Lỗi thường gặp

| Lỗi | Cách xử lý |
|---|---|
| Coding nhầm trên `main`, chưa commit | Dừng coding và không commit. Tạo branch ticket ngay tại trạng thái hiện tại bằng `git switch -c feature/<ID>` (hoặc `fix/<ID>`). Toàn bộ thay đổi chưa commit sẽ được giữ trên branch mới. |
| Coding nhầm trên `main`, đã commit nhưng chưa push | Dừng thao tác, không push và không tự ý chạy `reset` hoặc các lệnh thay đổi lịch sử Git. Báo cáo và hỏi Tech Lead (TL) để được hướng dẫn xử lý. |
| Commit xong nhưng quên push | Kiểm tra `git status` và `git log`, sau đó chạy `git push`. Nếu chưa có upstream, dùng `git push -u origin feature/<ID>`. |
| Quên `stash pop` sau khi tạo branch mới | Chạy `git stash list`, xác định đúng stash rồi chạy `git stash pop`. Kiểm tra lại `git status`. |
| Merge `origin/main` bị conflict | Kiểm tra `git status`, resolve từng file, `git add` và hoàn tất merge. Chạy lại 4 công cụ kiểm tra. |
| Push lần đầu nhưng chưa thiết lập upstream | Chạy `git push -u origin feature/<ID>`. |
| Xóa branch bằng `git branch -d` nhưng Git báo chưa merge | Xác nhận PR đã Squash and merge trên `main`, sau đó dùng `git branch -D feature/<ID>`. |
| Mở PR khi còn thay đổi local chưa commit | Kiểm tra `git status`, commit hoặc stash các thay đổi phù hợp trước khi mở PR. |

**Nguyên tắc chung:** Mỗi ticket có branch riêng, commit có mã ticket, không sửa trực tiếp `main`, không bỏ qua 4 công cụ kiểm tra và luôn kiểm tra trạng thái Git trước khi chuyển branch hoặc mở PR.
