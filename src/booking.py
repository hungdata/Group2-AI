"""
Booking module — Nhóm 2
Các member sẽ hoàn thiện các hàm bên dưới theo ticket của mình.
"""


# ================================================================
# US-103 — Member 1 làm
# ================================================================
def create_booking(name: str, date: str, time: str) -> dict:
    """
    Tạo một lịch hẹn mới.

    Args:
        name: Tên khách hàng
        date: Ngày đặt lịch (định dạng YYYY-MM-DD)
        time: Giờ đặt lịch (định dạng HH:MM)

    Returns:
        dict chứa thông tin lịch hẹn với status = "confirmed"

    Raises:
        ValueError: Nếu name, date hoặc time bị để trống
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


# ================================================================
# US-104 — Member 2 làm
# ================================================================
def cancel_booking(booking: dict) -> dict:
    """
    Huỷ một lịch hẹn.

    Args:
        booking: dict lịch hẹn hiện tại (phải có key "status")

    Returns:
        dict lịch hẹn với status = "cancelled"

    Raises:
        ValueError: Nếu booking là None hoặc không có key "status"
    """
    # TODO (Member 2): Kiểm tra booking có phải None không → raise ValueError
    # TODO (Member 2): Kiểm tra booking có key "status" không → raise ValueError
    # TODO (Member 2): Đổi booking["status"] thành "cancelled"
    # TODO (Member 2): Trả về booking đã cập nhật
    pass
