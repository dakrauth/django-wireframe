import io
import base64


def image_to_base64(im, format="PNG"):
    buffer = io.BytesIO()
    im.save(buffer, format=format)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("ascii")


def image_as_data_url(im, format="PNG"):
    b64 = image_to_base64(im, format=format)
    return f"data:image/{format.lower()};base64,{b64}"
