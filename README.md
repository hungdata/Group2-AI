# GROUP 2 — Online Booking System

> 🔗 **Repo:** https://github.com/hungdata/Group2-AI  
> 📌 **Default branch:** `develop` — tất cả làm việc từ đây

---

## 📦 Cấu trúc dự án

```
Group2-AI/
├── README.md               ← file này
├── TASKS.md                ← hướng dẫn code chi tiết từng ticket
├── .gitignore
├── src/
│   └── booking.py          ← viết code vào đây
└── tests/
    └── test_booking.py     ← chạy để kiểm tra
```

---

## 👥 Phân công thành viên

| Vai trò | Ticket | Nhánh | Nhiệm vụ |
|---|---|---|---|
| **Leader** | — | `develop` | Quản lý PR, request review, merge |
| **Member 1** | US-103 | `feature/US-103-create-booking` | Viết hàm `create_booking()` |
| **Member 2** | US-104 | `feature/US-104-cancel-booking` | Viết hàm `cancel_booking()` + Review PR Member 1 & 4 |
| **Member 3** | US-105 | `feature/US-105-update-readme-A` | Sửa tiêu đề README (Conflict A) |
| **Member 4** | US-106 | `feature/US-106-update-readme-B` | Sửa tiêu đề README (Conflict B) + Resolve conflict |

---

## 🚀 Bước đầu — Tất cả member làm trước

```bash
# 1. Clone repo về máy
git clone https://github.com/hungdata/Group2-AI.git
cd Group2-AI

# 2. Chuyển sang develop
git checkout develop
git pull origin develop
```

---

## ⏱️ Thứ tự làm việc cả nhóm

```
[Tất cả]   Clone repo, checkout develop
     ↓
[M1 & M2]  Song song — mỗi người code feature riêng
[M3 & M4]  Song song — mỗi người sửa cùng 1 dòng README (khác nội dung)
     ↓
[M1]  Tạo PR → M2 review → M1 sửa (nếu có) → M2 approve → Leader merge
[M2]  Tạo PR → M1 review → M1 approve → Leader merge
[M3]  Tạo PR → Leader merge NGAY (tạo conflict cho M4)
     ↓
[M4]  git merge origin/develop → CONFLICT xảy ra
      → Thảo luận nhóm → Resolve → push → M2 review → Leader merge
```

---

## 👤 MEMBER 1 — US-103: Tạo chức năng đặt lịch

**Nhánh:** `feature/US-103-create-booking`

### Thứ tự làm việc

| # | Việc cần làm |
|---|---|
| 1 | Tạo nhánh `feature/US-103-create-booking` từ `develop` |
| 2 | Mở `src/booking.py`, hoàn thiện hàm `create_booking()` theo TODO |
| 3 | Chạy test — phần US-103 phải hiện `✅ PASSED` |
| 4 | Commit + push lên GitHub |
| 5 | Tạo Pull Request: nhánh này → `develop` |
| 6 | Chờ **Member 2** review — nếu có comment thì sửa, push lại |
| 7 | Khi Member 2 approve → báo **Leader** merge |
| 8 | Trong lúc chờ → **review PR của Member 2** |

### Lệnh Git

```bash
git checkout develop
git pull origin develop
git checkout -b feature/US-103-create-booking

# --- Viết code vào src/booking.py ---

python tests/test_booking.py   # kiểm tra

git add src/booking.py
git commit -m "feat(booking): implement create_booking with validation"
git push -u origin feature/US-103-create-booking
```

### Yêu cầu code
Mở `src/booking.py` → tìm hàm `create_booking()` → điền vào chỗ `TODO`:
- Nếu `name` rỗng → `raise ValueError`
- Nếu `date` rỗng → `raise ValueError`
- Nếu `time` rỗng → `raise ValueError`
- Trả về `dict` gồm `name`, `date`, `time`, `status = "confirmed"`

---

## 👤 MEMBER 2 — US-104: Tạo chức năng huỷ lịch + Reviewer

**Nhánh:** `feature/US-104-cancel-booking`

### Thứ tự làm việc

| # | Việc cần làm |
|---|---|
| 1 | Tạo nhánh `feature/US-104-cancel-booking` từ `develop` |
| 2 | Mở `src/booking.py`, hoàn thiện hàm `cancel_booking()` theo TODO |
| 3 | Chạy test — phần US-104 phải hiện `✅ PASSED` |
| 4 | Commit + push lên GitHub |
| 5 | Tạo Pull Request: nhánh này → `develop` |
| 6 | **Review PR của Member 1** — để lại ít nhất 1 nhận xét |
| 7 | Khi Member 1 sửa xong → **Approve** PR của Member 1 |
| 8 | Chờ **Member 1** review PR của mình → khi approve → báo **Leader** merge |
| 9 | Cuối buổi → **Review PR của Member 4** sau khi resolve conflict |

### Lệnh Git

```bash
git checkout develop
git pull origin develop
git checkout -b feature/US-104-cancel-booking

# --- Viết code vào src/booking.py ---

python tests/test_booking.py   # kiểm tra

git add src/booking.py
git commit -m "feat(booking): implement cancel_booking with validation"
git push -u origin feature/US-104-cancel-booking
```

### Yêu cầu code
Mở `src/booking.py` → tìm hàm `cancel_booking()` → điền vào chỗ `TODO`:
- Nếu `booking` là `None` → `raise ValueError`
- Nếu `booking` không có key `"status"` → `raise ValueError`
- Đổi `booking["status"] = "cancelled"`
- Trả về `booking`

---

## 👤 MEMBER 3 — US-105: Cập nhật README (Conflict A)

**Nhánh:** `feature/US-105-update-readme-A`

### Thứ tự làm việc

| # | Việc cần làm |
|---|---|
| 1 | Tạo nhánh `feature/US-105-update-readme-A` từ `develop` |
| 2 | Mở `README.md`, sửa dòng tiêu đề đầu tiên |
| 3 | Commit + push |
| 4 | Tạo Pull Request → báo **Leader** merge ngay |

### Lệnh Git

```bash
git checkout develop
git pull origin develop
git checkout -b feature/US-105-update-readme-A

# --- Sửa dòng đầu README.md ---
# Đổi từ:  # GROUP 2 — Booking System
# Thành:   # GROUP 2 — Online Booking System

git add README.md
git commit -m "docs: update project title to Online Booking System"
git push -u origin feature/US-105-update-readme-A
```

> ✅ Xong sớm. Vai trò quan trọng là **tạo conflict cho Member 4**.

---

## 👤 MEMBER 4 — US-106: Cập nhật README (Conflict B) + Resolve

**Nhánh:** `feature/US-106-update-readme-B`

### Thứ tự làm việc

| # | Việc cần làm |
|---|---|
| 1 | Tạo nhánh `feature/US-106-update-readme-B` từ `develop` |
| 2 | Mở `README.md`, sửa **cùng dòng tiêu đề** như Member 3 nhưng **nội dung khác** |
| 3 | Commit + push |
| 4 | Tạo Pull Request vào `develop` |
| 5 | **Chờ Leader merge PR của Member 3 trước** |
| 6 | Sau đó chạy `git fetch origin` + `git merge origin/develop` |
| 7 | Git báo **CONFLICT** → mở `README.md` xem |
| 8 | Thảo luận nhóm → chọn tên chung hợp lý |
| 9 | Xoá ký hiệu conflict, giữ lại tên đã thống nhất |
| 10 | Commit resolve + push |
| 11 | Báo **Member 2** review → approve → báo **Leader** merge |

### Lệnh Git

```bash
git checkout develop
git pull origin develop
git checkout -b feature/US-106-update-readme-B

# --- Sửa dòng đầu README.md ---
# Đổi từ:  # GROUP 2 — Booking System
# Thành:   # GROUP 2 — Appointment Booking System
# (khác với Member 3!)

git add README.md
git commit -m "docs: update project title to Appointment Booking System"
git push -u origin feature/US-106-update-readme-B

# === SAU KHI PR Member 3 được merge ===

git fetch origin
git merge origin/develop
# → Git báo CONFLICT trong README.md

# Mở README.md, bạn sẽ thấy:
# <<<<<<< HEAD
# # GROUP 2 — Appointment Booking System
# =======
# # GROUP 2 — Online Booking System
# >>>>>>> origin/develop

# Thảo luận nhóm → sửa thành tên chung, ví dụ:
# # GROUP 2 — Online Appointment Booking System
# Xoá hết <<<<<<, =======, >>>>>>>

git add README.md
git commit -m "resolve: merge conflict in README project title"
git push
```

> ⚠️ **Không được chọn đại một bên!** Phải hiểu ý nghĩa cả hai thay đổi rồi mới quyết định.

---

## 👑 LEADER — Tổng quan việc cần làm

| # | Việc cần làm | Thời điểm |
|---|---|---|
| 1 | Request **Member 2** review PR của Member 1 | Khi M1 tạo PR |
| 2 | Request **Member 1** review PR của Member 2 | Khi M2 tạo PR |
| 3 | **Merge ngay** PR của Member 3 | Khi M3 tạo PR |
| 4 | Merge PR Member 1 khi M2 approve | Sau bước 2 |
| 5 | Merge PR Member 2 khi M1 approve | Sau bước 2 |
| 6 | Request **Member 2** review PR Member 4 | Sau khi M4 resolve |
| 7 | Merge PR Member 4 khi M2 approve | Cuối cùng |

> ⚠️ **Quy tắc:** Không ai được tự merge PR của mình. Không được push thẳng vào `develop`.

---

## 🔍 Cách chạy kiểm tra

```bash
python tests/test_booking.py
```

Kết quả mong đợi:
```
==================================================
  TEST US-103 — create_booking (Member 1)
==================================================
✅ test_create_booking_success PASSED
✅ test_create_booking_empty_name PASSED
✅ test_create_booking_empty_date PASSED
✅ test_create_booking_empty_time PASSED

==================================================
  TEST US-104 — cancel_booking (Member 2)
==================================================
✅ test_cancel_booking_success PASSED
✅ test_cancel_booking_none PASSED
✅ test_cancel_booking_no_status PASSED

✅ Hoàn tất kiểm thử!
```

---

## 📌 Quy tắc Pull Request

- **Title:** `US-xxx: Mô tả ngắn`
- Phải có ít nhất **1 reviewer approve**
- **Không được tự merge PR của mình**
- Chỉ **Leader** mới được merge vào `develop`
- Test phải **PASSED** trước khi tạo PR
