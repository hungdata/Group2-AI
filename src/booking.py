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
    # TODO (Member 1): Kiểm tra name có rỗng không → raise ValueError
    # TODO (Member 1): Kiểm tra date có rỗng không → raise ValueError
    # TODO (Member 1): Kiểm tra time có rỗng không → raise ValueError
    # TODO (Member 1): Trả về dict gồm name, date, time, status="confirmed"
    pass


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
