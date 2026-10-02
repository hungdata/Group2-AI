# GROUP 2 — Online Appointment Booking System

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

---

## 🎬 Kịch bản thuyết trình thực tế — Từng bước chi tiết

> **Thứ tự lên bảng:** Leader → Member 1 → Member 2 → Member 3 → Member 4  
> Mỗi người **mở sẵn GitHub + Terminal trước khi lên**. Chiếu màn hình lên máy chiếu.

---

### 🖥️ Chuẩn bị trước khi lên bảng — Tất cả làm

```
1. Mở trình duyệt → https://github.com/hungdata/Group2-AI
2. Đăng nhập GitHub của mình
3. Mở sẵn 3 tab: Trang repo chính | Tab Pull Requests | Tab Insights
4. Mở Terminal hoặc VS Code, đã cd vào thư mục project
```

---

### 👑 LEADER — Kịch bản thực tế từng bước (~2 phút)

**[Bước 1]** Đứng lên, giới thiệu:
> *"Dạ em là Leader của nhóm 2. Em xin trình bày tổng quan về cách nhóm em tổ chức Git Flow."*

**[Bước 2]** Chiếu trang chính repo — **click vào dropdown nhánh** (góc trái):
> *"Đây là repo của nhóm em. Nhóm có 2 nhánh chính — main là bản production, develop là nhánh team làm việc hàng ngày. Không ai được push thẳng vào hai nhánh này."*

**[Bước 3]** Click tab **Pull requests**:
> *"Đây là tất cả Pull Request nhóm tạo trong buổi. Mỗi PR ứng với một ticket của từng thành viên. Mọi thay đổi đều phải qua PR và được review trước khi merge."*

**[Bước 4]** Click **Insights → Network**:
> *"Đây là sơ đồ nhánh — thầy thấy develop là gốc, mỗi người tạo nhánh feature riêng từ đó, làm xong merge trở lại qua PR."*

**[Bước 5]** Kết:
> *"Em kiểm soát thứ tự merge — merge PR Member 3 trước rồi mới để Member 4 cập nhật develop — đây là bước cố ý tạo conflict cho phần B. Dạ em xin hết, mời Member 1."*

---

### 👤 MEMBER 1 — Kịch bản thực tế từng bước (~3 phút)

**[Bước 1]** Giới thiệu:
> *"Dạ em làm ticket US-103 — chức năng tạo lịch hẹn."*

**[Bước 2]** Mở Terminal, chiếu lịch sử commit:
```bash
git log --oneline
```
> *"Đây là lịch sử commit của em. Em tạo nhánh từ develop, viết code rồi commit theo chuẩn: feat(booking): implement create_booking."*

**[Bước 3]** Vào GitHub → click PR của mình → tab **Files changed**:
> *"Đây là code em viết. Hàm create_booking nhận 3 tham số: name, date, time. Em kiểm tra từng trường — nếu rỗng thì raise ValueError. Nếu hợp lệ trả về dict có status là confirmed."*
→ Chỉ tay vào từng phần code

**[Bước 4]** Click tab **Conversation** trong PR:
> *"Member 2 để lại comment tại đây."*
→ Đọc to nội dung comment cho thầy nghe
> *"Em đọc hiểu comment, sửa lại và push thêm một commit. Thầy thấy PR có 2 commit — commit đầu là lúc mới push, commit sau là lần sửa theo review."*

**[Bước 5]** Kết:
> *"Sau khi Member 2 approve, em báo Leader và Leader merge PR vào develop. Dạ em xin hết, mời Member 2."*

---

### 👤 MEMBER 2 — Kịch bản thực tế từng bước (~3 phút)

**[Bước 1]** Giới thiệu:
> *"Dạ em có 2 việc: code ticket US-104 và làm reviewer cho Member 1 và Member 4."*

**[Bước 2]** Vào GitHub → PR của mình → tab **Files changed**:
> *"Đây là code US-104 của em — hàm cancel_booking. Em kiểm tra nếu booking là None hoặc không có key status thì raise ValueError. Nếu hợp lệ thì đổi status thành cancelled và trả về."*

**[Bước 3]** Mở Terminal, chạy test trực tiếp:
```bash
python tests/test_booking.py
```
> *"Đây là kết quả — tất cả 7 test PASSED. Em chạy test trước khi tạo PR để chắc chắn code đúng."*

**[Bước 4]** Vào PR của **Member 1** → tab **Conversation**:
> *"Đây là PR của Member 1 — em để lại comment tại đây."*
→ Click vào comment, đọc to cho thầy nghe
> *"Em không chỉ bấm Approve cho có — em đọc từng dòng code, hiểu logic rồi mới nhận xét. Sau khi Member 1 sửa và push lại, em kiểm tra lại rồi mới Approve."*
→ Chỉ vào dấu ✅ Approved trong PR

**[Bước 5]** Kết:
> *"Cuối buổi em cũng review PR của Member 4 sau khi bạn resolve conflict xong. Dạ em xin hết, mời Member 3."*

---

### 👤 MEMBER 3 — Kịch bản thực tế từng bước (~2 phút)

**[Bước 1]** Giới thiệu:
> *"Dạ em làm ticket US-105 — vai trò em là tạo conflict để nhóm thực hành giải quyết."*

**[Bước 2]** Vào GitHub → click PR của mình (trạng thái **Merged** màu tím):
> *"Đây là PR của em — trạng thái Merged nghĩa là đã được merge vào develop thành công."*

**[Bước 3]** Click tab **Files changed**:
> *"Dòng màu đỏ là nội dung cũ, dòng màu xanh là nội dung em sửa — tiêu đề thành 'Online Booking System'. Chỉ một dòng thay đổi nhưng đúng dòng đó Member 4 cũng sửa ở nhánh khác — đây là nguyên nhân conflict."*

**[Bước 4]** Kết:
> *"Sau khi Leader merge PR của em trước, develop có 'Online Booking System'. Nhánh Member 4 vẫn là 'Appointment Booking System' — conflict đã được tạo ra. Dạ em xin hết, mời Member 4."*

---

### 👤 MEMBER 4 — Kịch bản thực tế từng bước (~4 phút) — quan trọng nhất

**[Bước 1]** Giới thiệu:
> *"Dạ em làm ticket US-106 — tạo conflict và giải quyết conflict."*

**[Bước 2]** Mở Terminal, chiếu lịch sử commit:
```bash
git log --oneline
```
> *"Thầy thấy 2 commit — commit đầu là lúc em sửa tiêu đề. Commit thứ hai là 'resolve: merge conflict' — đây là lúc em giải quyết xong."*

**[Bước 3]** Giải thích conflict xảy ra — chiếu Terminal:
> *"Sau khi Leader merge PR Member 3, em chạy:"*
```bash
git fetch origin
git merge origin/develop
```
> *"Git báo ngay: CONFLICT in README.md — Automatic merge failed."*

**[Bước 4]** Mở file README.md, chiếu nội dung conflict lên:
```
<<<<<<< HEAD
# GROUP 2 — Appointment Booking System
=======
# GROUP 2 — Online Booking System
>>>>>>> origin/develop
```
> *"Phần trên dấu ======= là code của em. Phần dưới là code Member 3 đã vào develop. Git không tự biết chọn bên nào nên báo conflict để mình tự quyết định."*

**[Bước 5]** Giải thích cách resolve — quan trọng nhất:
> *"Em không chọn đại một bên — 'Online' nói lên tính năng trực tuyến, 'Appointment' nói lên chức năng đặt lịch. Nhóm em thảo luận và thống nhất giữ cả hai ý nghĩa: 'Online Appointment Booking System'. Em xoá hết ký hiệu <<<, ===, >>> và sửa thành tên đã thống nhất."*

**[Bước 6]** Vào GitHub → PR của mình → tab **Commits**:
> *"PR của em có 2 commit — commit đầu khi tạo nhánh, commit sau là resolve conflict."*

**[Bước 7]** Tab **Files changed**:
> *"Kết quả cuối cùng — tiêu đề là 'Online Appointment Booking System', không còn ký hiệu conflict nào."*

**[Bước 8]** Tab **Conversation**:
> *"Member 2 vào review và Approve tại đây. Sau đó Leader merge PR vào develop — bài thực hành phần B hoàn thành."*

**[Bước 9]** Kết toàn nhóm:
> *"Bài học em rút ra: conflict không đáng sợ nếu hiểu ý nghĩa từng thay đổi. Phải đọc cả hai phía, thống nhất với nhóm rồi mới resolve — không chọn đại. Dạ nhóm em xin hết, cảm ơn thầy."*

---

### ❓ Câu hỏi thầy hay hỏi — và cách trả lời

| Câu hỏi | Người trả lời | Trả lời |
|---|---|---|
| *"Tại sao không push thẳng vào develop?"* | Leader | Để mọi thay đổi đều được review, tránh lỗi vào nhánh chính |
| *"PR là gì, tại sao cần?"* | Member 1 | PR là yêu cầu merge code, giúp reviewer kiểm tra trước khi tích hợp |
| *"Conflict xảy ra khi nào?"* | Member 4 | Khi 2 người sửa cùng vị trí trong cùng file trên 2 nhánh khác nhau |
| *"Resolve conflict như thế nào?"* | Member 4 | Mở file, đọc hiểu cả hai thay đổi, thống nhất nội dung, xoá ký hiệu, commit lại |
| *"Reviewer có trách nhiệm gì?"* | Member 2 | Đọc code, nhận xét cụ thể, chỉ approve khi code đúng và đủ |
| *"Leader làm gì trong Git Flow?"* | Leader | Không code trực tiếp vào develop, phân công, kiểm soát PR, merge đúng quy trình |



