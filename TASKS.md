# 📋 HƯỚNG DẪN CHI TIẾT TỪNG MEMBER — Nhóm 2

> **Link repo:** https://github.com/hungdata/Group2-AI  
> Mỗi member làm đúng phần của mình, **không sửa code của người khác**.

---

## 🔧 Bước chung — Tất cả member làm trước

```bash
# 1. Clone repo về máy
git clone https://github.com/hungdata/Group2-AI.git
cd Group2-AI

# 2. Chuyển sang develop
git checkout develop
git pull origin develop
```

---

---

## 👤 MEMBER 1 — US-103: Tạo chức năng đặt lịch hẹn

### Bước 1 — Tạo nhánh
```bash
git checkout develop
git pull origin develop
git checkout -b feature/US-103-create-booking
```

### Bước 2 — Mở file và viết code
Mở file `src/booking.py`, tìm hàm `create_booking` và hoàn thiện:

```python
def create_booking(name: str, date: str, time: str) -> dict:
    if not name:
        raise ValueError("Tên khách hàng không được để trống")
    if not date:
        raise ValueError("Ngày đặt lịch không được để trống")
    if not time:
        raise ValueError("Giờ đặt lịch không được để trống")

    return {
        "name": name,
        "date": date,
        "time": time,
        "status": "confirmed"
    }
```

### Bước 3 — Kiểm tra test
```bash
python tests/test_booking.py
```
Phần `TEST US-103` phải có 4 dòng `✅ PASSED`.

### Bước 4 — Commit và push
```bash
git add src/booking.py
git commit -m "feat(booking): implement create_booking with validation"
git push -u origin feature/US-103-create-booking
```

### Bước 5 — Tạo Pull Request trên GitHub
- Vào https://github.com/hungdata/Group2-AI
- Nhấn **Compare & pull request**
- **From:** `feature/US-103-create-booking` → **To:** `develop`
- **Title:** `US-103: Implement create booking appointment`
- **Description:**
```
Ticket: US-103

Mục tiêu:
Tạo hàm create_booking với đầy đủ validation.

Thay đổi:
- Thêm hàm create_booking() trong src/booking.py
- Kiểm tra name, date, time không được rỗng
- Trả về dict với status = "confirmed"

Cách kiểm tra:
python tests/test_booking.py
→ Phần US-103 phải 4 PASSED
```
- **Reviewer:** Chọn **Member 2**

### Bước 6 — Đợi Member 2 review
Nếu Member 2 có comment → sửa rồi:
```bash
git add src/booking.py
git commit -m "fix(booking): address review comments"
git push
```

---

---

## 👤 MEMBER 2 — US-104: Tạo chức năng huỷ lịch hẹn + Review PR Member 1

### Phần 1: Code US-104

#### Bước 1 — Tạo nhánh
```bash
git checkout develop
git pull origin develop
git checkout -b feature/US-104-cancel-booking
```

#### Bước 2 — Mở file và viết code
Mở file `src/booking.py`, tìm hàm `cancel_booking` và hoàn thiện:

```python
def cancel_booking(booking: dict) -> dict:
    if booking is None:
        raise ValueError("Lịch hẹn không được là None")
    if "status" not in booking:
        raise ValueError("Lịch hẹn không có trường status")

    booking["status"] = "cancelled"
    return booking
```

#### Bước 3 — Kiểm tra test
```bash
python tests/test_booking.py
```
Phần `TEST US-104` phải có 3 dòng `✅ PASSED`.

#### Bước 4 — Commit và push
```bash
git add src/booking.py
git commit -m "feat(booking): implement cancel_booking with validation"
git push -u origin feature/US-104-cancel-booking
```

#### Bước 5 — Tạo Pull Request
- **From:** `feature/US-104-cancel-booking` → **To:** `develop`
- **Title:** `US-104: Implement cancel booking`
- **Description:**
```
Ticket: US-104

Mục tiêu:
Tạo hàm cancel_booking với validation đầu vào.

Thay đổi:
- Thêm hàm cancel_booking() trong src/booking.py
- Kiểm tra booking không phải None
- Kiểm tra booking có key "status"
- Đổi status thành "cancelled"

Cách kiểm tra:
python tests/test_booking.py
→ Phần US-104 phải 3 PASSED
```
- **Reviewer:** Chọn **Member 1**

---

### Phần 2: Review PR của Member 1

Khi Member 1 tạo PR, bạn vào GitHub kiểm tra:

**Những điều cần review:**
1. Hàm có kiểm tra `name` rỗng chưa?
2. Hàm có kiểm tra `date` rỗng chưa?
3. Hàm có kiểm tra `time` rỗng chưa?
4. Kết quả trả về có đủ `name`, `date`, `time`, `status` chưa?
5. `status` có đúng là `"confirmed"` chưa?

**Cách comment trên GitHub:**
- Vào tab **Files changed** trong PR
- Click dấu `+` cạnh dòng code muốn comment
- Viết nhận xét cụ thể, ví dụ:
  > "Nên thêm kiểm tra time không được để trống trước khi tạo booking"

**Sau khi ổn:** Nhấn **Approve** → Báo Leader merge.

---

---

## 👤 MEMBER 3 — US-105: Cập nhật README (Conflict A)

> ⚠️ Phần này cố tình tạo conflict với Member 4. Hai người làm **đồng thời**, không đợi nhau.

### Bước 1 — Tạo nhánh
```bash
git checkout develop
git pull origin develop
git checkout -b feature/US-105-update-readme-A
```

### Bước 2 — Sửa dòng tiêu đề trong README.md
Mở `README.md`, tìm dòng đầu tiên:
```
# GROUP 2 — Booking System
```
Sửa thành:
```
# GROUP 2 — Online Booking System
```
Chỉ sửa đúng dòng này, không sửa gì khác.

### Bước 3 — Commit và push
```bash
git add README.md
git commit -m "docs: update project title to Online Booking System"
git push -u origin feature/US-105-update-readme-A
```

### Bước 4 — Tạo Pull Request
- **From:** `feature/US-105-update-readme-A` → **To:** `develop`
- **Title:** `US-105: Update project title`
- **Reviewer:** Chọn **Leader**

### Bước 5 — Báo Leader merge trước
Leader merge PR của Member 3 trước PR của Member 4 → conflict xảy ra cho Member 4.

---

---

## 👤 MEMBER 4 — US-106: Cập nhật README (Conflict B) + Resolve conflict

> ⚠️ Làm **đồng thời** với Member 3. Sau khi PR của Member 3 được merge, bạn phải resolve conflict.

### Phần 1: Tạo nhánh và sửa cùng dòng với Member 3

#### Bước 1 — Tạo nhánh (lúc develop chưa có thay đổi của Member 3)
```bash
git checkout develop
git pull origin develop
git checkout -b feature/US-106-update-readme-B
```

#### Bước 2 — Sửa cùng dòng tiêu đề trong README.md
Mở `README.md`, tìm dòng đầu tiên:
```
# GROUP 2 — Booking System
```
Sửa thành: *(khác với Member 3)*
```
# GROUP 2 — Appointment Booking System
```

#### Bước 3 — Commit và push
```bash
git add README.md
git commit -m "docs: update project title to Appointment Booking System"
git push -u origin feature/US-106-update-readme-B
```

#### Bước 4 — Tạo Pull Request
- **From:** `feature/US-106-update-readme-B` → **To:** `develop`
- **Title:** `US-106: Update project title`

---

### Phần 2: Resolve conflict (sau khi PR Member 3 được merge)

Sau khi Leader merge PR của Member 3, nhánh `develop` đã có:
```
# GROUP 2 — Online Booking System
```

Nhưng nhánh của bạn vẫn có:
```
# GROUP 2 — Appointment Booking System
```

#### Bước 5 — Kéo develop mới về và merge
```bash
git checkout feature/US-106-update-readme-B
git fetch origin
git merge origin/develop
```

Git sẽ báo conflict:
```
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

#### Bước 6 — Mở README.md và xem conflict
```
<<<<<<< HEAD
# GROUP 2 — Appointment Booking System
=======
# GROUP 2 — Online Booking System
>>>>>>> origin/develop
```

#### Bước 7 — Resolve (không chọn đại một bên!)
Thảo luận với nhóm rồi thống nhất một tên, ví dụ:
```
# GROUP 2 — Online Appointment Booking System
```
Xoá hết các ký hiệu `<<<<<<<`, `=======`, `>>>>>>>` và chỉ giữ lại dòng đã thống nhất.

#### Bước 8 — Kiểm tra rồi commit
```bash
# Kiểm tra không còn ký hiệu conflict
grep -n "<<<<<<" README.md  # phải không có kết quả

git add README.md
git commit -m "resolve: merge conflict in README project title"
git push
```

#### Bước 9 — PR tự cập nhật
- Vào GitHub kiểm tra PR của bạn đã hết conflict chưa
- Báo **Member 2** review
- Sau khi approve → báo **Leader** merge

---

---

## 👑 LEADER — Tổng quan việc cần làm

```
1. Merge PR Member 3 (US-105) TRƯỚC khi Member 4 resolve conflict
2. Request Member 2 review PR Member 1
3. Request Member 1 review PR Member 2
4. Request Member 2 review PR Member 4 (sau khi resolve)
5. Kiểm tra CI / test pass trước khi merge
6. Merge theo thứ tự hợp lý vào develop
```

**Thứ tự merge khuyên dùng:**
```
PR Member 1 (US-103)
    ↓
PR Member 2 (US-104)
    ↓
PR Member 3 (US-105)  ← merge trước để tạo conflict cho Member 4
    ↓
PR Member 4 (US-106)  ← sau khi Member 4 resolve conflict
```
