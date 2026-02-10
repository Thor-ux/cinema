import qrcode

def generate_qr(code: str):
    img = qrcode.make(code)
    img.save(f"tickets/{code}.png")
