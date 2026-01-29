from ...domain.port.text_encoder import TextEncoder


class HTTPAuthHeaderMapper:
    def __init__(self, text_encoder: TextEncoder) -> None:
        self._text_encoder = text_encoder

    def map_from_credentials(self, username: str, password: str) -> dict[str, str]:
        credentials = f"{username}:{password}"
        encoded_credentials = self._text_encoder.encode(credentials)
        return {"Authorization": f"Basic {encoded_credentials}"}
