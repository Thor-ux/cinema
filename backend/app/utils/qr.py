import qrcode
import uuid
import base64
import json
from io import BytesIO


def generate_qr(data: dict):

    qr_content = json.dumps(data)

    img = qrcode.make(qr_content)

    buffer = BytesIO()

    img.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode()