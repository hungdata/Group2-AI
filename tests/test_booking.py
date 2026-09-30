"""
Test cases cho booking module — Nhóm 2
Chạy lệnh: python tests/test_booking.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from booking import create_booking, cancel_booking


# ================================================================
# Test cho US-103 — Member 1 viết hàm create_booking
# ================================================================
def test_create_booking_success():
    result = create_booking("Nguyen Van A", "2024-12-01", "09:00")
    assert result["name"] == "Nguyen Van A"
    assert result["date"] == "2024-12-01"
    assert result["time"] == "09:00"
    assert result["status"] == "confirmed"
    print("✅ test_create_booking_success PASSED")


def test_create_booking_empty_name():
    try:
        create_booking("", "2024-12-01", "09:00")
        print("❌ test_create_booking_empty_name FAILED — phải raise ValueError")
    except ValueError as e:
        print(f"✅ test_create_booking_empty_name PASSED — {e}")


def test_create_booking_empty_date():
    try:
        create_booking("Nguyen Van A", "", "09:00")
        print("❌ test_create_booking_empty_date FAILED — phải raise ValueError")
    except ValueError as e:
        print(f"✅ test_create_booking_empty_date PASSED — {e}")


def test_create_booking_empty_time():
    try:
        create_booking("Nguyen Van A", "2024-12-01", "")
        print("❌ test_create_booking_empty_time FAILED — phải raise ValueError")
    except ValueError as e:
        print(f"✅ test_create_booking_empty_time PASSED — {e}")


# ================================================================
# Test cho US-104 — Member 2 viết hàm cancel_booking
# ================================================================
def test_cancel_booking_success():
    booking = {"name": "Nguyen Van A", "date": "2024-12-01", "time": "09:00", "status": "confirmed"}
    result = cancel_booking(booking)
    assert result["status"] == "cancelled"
    print("✅ test_cancel_booking_success PASSED")


def test_cancel_booking_none():
    try:
        cancel_booking(None)
        print("❌ test_cancel_booking_none FAILED — phải raise ValueError")
    except ValueError as e:
        print(f"✅ test_cancel_booking_none PASSED — {e}")


def test_cancel_booking_no_status():
    try:
        cancel_booking({"name": "Nguyen Van A"})
        print("❌ test_cancel_booking_no_status FAILED — phải raise ValueError")
    except ValueError as e:
        print(f"✅ test_cancel_booking_no_status PASSED — {e}")


# ================================================================
# Chạy tất cả test
# ================================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  TEST US-103 — create_booking (Member 1)")
    print("=" * 50)
    test_create_booking_success()
    test_create_booking_empty_name()
    test_create_booking_empty_date()
    test_create_booking_empty_time()

    print()
    print("=" * 50)
    print("  TEST US-104 — cancel_booking (Member 2)")
    print("=" * 50)
    test_cancel_booking_success()
    test_cancel_booking_none()
    test_cancel_booking_no_status()

    print()
    print("✅ Hoàn tất kiểm thử!")
