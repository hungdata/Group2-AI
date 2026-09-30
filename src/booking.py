"""
Booking module — Nhóm 2
Chức năng: Tạo và quản lý lịch hẹn
"""


def create_booking(name: str, date: str, time: str) -> dict:
    """
    Tạo một lịch hẹn mới.

    Args:
        name: Tên khách hàng
        date: Ngày đặt lịch (định dạng YYYY-MM-DD)
        time: Giờ đặt lịch (định dạng HH:MM)

    Returns:
        dict: Thông tin lịch hẹn nếu hợp lệ

    Raises:
        ValueError: Nếu thiếu thông tin bắt buộc
    """
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


def cancel_booking(booking: dict) -> dict:
    """
    Huỷ một lịch hẹn.

    Args:
        booking: Thông tin lịch hẹn hiện tại

    Returns:
        dict: Lịch hẹn với trạng thái đã huỷ
    """
    booking["status"] = "cancelled"
    return booking
