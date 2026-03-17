import qrcode
import uuid
import base64
from io import BytesIO


def generate_qr(data: str):

    img = qrcode.make(data)

    buffer = BytesIO()

    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return qr_base64