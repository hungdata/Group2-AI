# GROUP 2 — Booking System

## Giới thiệu
Dự án thực hành Git Flow của Nhóm 2.  
Mục tiêu: Mô phỏng quy trình làm việc nhóm với feature branch, Pull Request, code review và giải quyết conflict.

---

## Thành viên nhóm & Phân công
| Vai trò | Nhiệm vụ trong bài |
|---|---|
| **Leader** | Quản lý `develop`, request review, kiểm tra PR/CI, merge PR |
| **Member 1** | Developer — US-103: Tạo chức năng đặt lịch hẹn |
| **Member 2** | Developer — US-104: Tạo chức năng huỷ lịch hẹn + Reviewer cho Member 1 |
| **Member 3** | Developer — US-105: Cập nhật mô tả dự án (conflict A) |
| **Member 4** | Developer — US-106: Cập nhật mô tả dự án (conflict B) + xử lý conflict |

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

## Bảng Ticket thực hành

| Ticket | Người làm | Nhánh | Mô tả công việc |
|---|---|---|---|
| US-103 | Member 1 | `feature/US-103-create-booking` | Thêm hàm `create_booking()` vào `src/booking.py`, viết test |
| US-104 | Member 2 | `feature/US-104-cancel-booking` | Thêm hàm `cancel_booking()` vào `src/booking.py`, viết test |
| US-105 | Member 3 | `feature/US-105-update-readme-A` | Sửa dòng tiêu đề trong `README.md` (tạo conflict A) |
| US-106 | Member 4 | `feature/US-106-update-readme-B` | Sửa cùng dòng tiêu đề trong `README.md` (tạo conflict B, rồi resolve) |

---

## Luồng Review

```
Member 1 tạo PR  →  Member 2 review  →  Leader merge
Member 2 tạo PR  →  Member 1 review  →  Leader merge
Member 3 tạo PR  →  Leader merge trước
Member 4 tạo PR  →  resolve conflict  →  Member 2 review  →  Leader merge
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
git clone https://github.com/hungdata/Group2-AI.git
cd Group2-AI

# Chuyển sang develop
git checkout develop
git pull origin develop

# Tạo nhánh feature riêng (ví dụ Member 1)
git checkout -b feature/US-103-create-booking
```

---

## Quy tắc Pull Request
- Title: `US-xxx: Mô tả ngắn`
- Phải có ít nhất **1 reviewer approve**
- **Không được tự merge PR của mình**
- Chỉ **Leader** mới merge vào `develop`
