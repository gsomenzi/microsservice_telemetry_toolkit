from domain.port.text_encoder import TextEncoder
import base64


class Base64TextEncoder(TextEncoder):
    def encode(self, text: str) -> str:
        encoded_bytes = base64.b64encode(text.encode("utf-8"))
        return encoded_bytes.decode("utf-8")
