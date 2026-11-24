import base64
from io import BytesIO

import qrcode


def generate_qr(content: str) -> str:
    """Return `content` encoded as a QR code PNG, base64 encoded."""
    image = qrcode.make(content)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()
