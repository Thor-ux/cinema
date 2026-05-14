import qrcode
import base64
from io import BytesIO

def generate_qr(
    booking_code: str,
    movie_title: str,
    session_id: int,
    row: int,
    seat_number: int,
    seat_type: str,
    price: float
):

    qr_content = f"""
BOOKING_CODE:{booking_code}
MOVIE:{movie_title}
SESSION_ID:{session_id}
ROW:{row}
SEAT:{seat_number}
TYPE:{seat_type}
PRICE:{price}
""".strip()