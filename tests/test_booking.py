"""
Test cases cho booking module — Nhóm 2
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from booking import create_booking, cancel_booking


def test_create_booking_success():
    """Tạo lịch hẹn hợp lệ"""
    result = create_booking("Nguyen Van A", "2024-12-01", "09:00")
    assert result["name"] == "Nguyen Van A"
    assert result["date"] == "2024-12-01"
    assert result["time"] == "09:00"
    assert result["status"] == "confirmed"
    print("✅ test_create_booking_success PASSED")


def test_create_booking_empty_name():
    """Tên rỗng phải báo lỗi"""
    try:
        create_booking("", "2024-12-01", "09:00")
        print("❌ test_create_booking_empty_name FAILED")
    except ValueError as e:
        print(f"✅ test_create_booking_empty_name PASSED — {e}")


def test_create_booking_empty_date():
    """Ngày rỗng phải báo lỗi"""
    try:
        create_booking("Nguyen Van A", "", "09:00")
        print("❌ test_create_booking_empty_date FAILED")
    except ValueError as e:
        print(f"✅ test_create_booking_empty_date PASSED — {e}")


def test_create_booking_empty_time():
    """Giờ rỗng phải báo lỗi"""
    try:
        create_booking("Nguyen Van A", "2024-12-01", "")
        print("❌ test_create_booking_empty_time FAILED")
    except ValueError as e:
        print(f"✅ test_create_booking_empty_time PASSED — {e}")


def test_cancel_booking():
    """Huỷ lịch hẹn"""
    booking = create_booking("Nguyen Van A", "2024-12-01", "09:00")
    cancelled = cancel_booking(booking)
    assert cancelled["status"] == "cancelled"
    print("✅ test_cancel_booking PASSED")


if __name__ == "__main__":
    print("=== Chạy test Booking ===\n")
    test_create_booking_success()
    test_create_booking_empty_name()
    test_create_booking_empty_date()
    test_create_booking_empty_time()
    test_cancel_booking()
    print("\n=== Hoàn tất ===")
