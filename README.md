# GROUP 2 — Booking System

## Giới thiệu
Dự án thực hành Git Flow của Nhóm 2.  
Mục tiêu: Mô phỏng quy trình làm việc nhóm với feature branch, Pull Request, code review và giải quyết conflict.

---

## Thành viên nhóm
| Vai trò | Nhiệm vụ |
|---|---|
| **Leader** | Quản lý `develop`, request review, kiểm tra PR/CI, merge PR |
| **Member 1** | Developer — Feature US-103 (Create Booking) |
| **Member 2** | Reviewer — Review PR của Member 1 và 4 |
| **Member 3** | Developer — Branch conflict A |
| **Member 4** | Developer — Branch conflict B, xử lý conflict |

---

## Cấu trúc dự án
```
GROUP_2_AI/
├── README.md
├── .gitignore
├── src/
│   └── booking.py       ← logic chính
└── tests/
    └── test_booking.py  ← kiểm thử
```

---

## Quy ước Git Flow

### Nhánh chính
- `main` — bản production ổn định, **không push trực tiếp**
- `develop` — tích hợp tính năng, **không push trực tiếp**

### Nhánh feature
```
feature/<ticket>-<mô-tả-ngắn>
```
Ví dụ: `feature/US-103-create-booking`

### Quy trình làm việc
```
1. Clone repo
2. git checkout develop
3. git pull origin develop
4. git checkout -b feature/US-xxx-ten-chuc-nang
5. Code + commit
6. git push -u origin feature/US-xxx-...
7. Tạo Pull Request: feature → develop
8. Chờ review + CI pass
9. Leader merge PR
```

---

## Cách clone và chạy

```bash
# Clone repo
git clone https://github.com/hungdata/GROUP_2_AI.git
cd GROUP_2_AI

# Chuyển sang develop
git checkout develop
git pull origin develop

# Tạo nhánh feature riêng
git checkout -b feature/US-xxx-ten-chuc-nang
```

---

## Quy tắc Pull Request
- Title: `US-xxx: Mô tả ngắn`
- Phải có ít nhất **1 reviewer approve**
- **Không được tự merge PR của mình**
- Chỉ **Leader** mới merge vào `develop`

---

## Ticket thực hành

| Ticket | Người làm | Mô tả |
|---|---|---|
| US-103 | Member 1 | Tạo chức năng đặt lịch hẹn |
| US-104 | Member 3 | Cập nhật tên dự án (conflict A) |
| US-105 | Member 4 | Cập nhật tên dự án (conflict B) |
