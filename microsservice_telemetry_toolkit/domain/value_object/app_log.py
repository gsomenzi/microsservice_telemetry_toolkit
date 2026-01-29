import time


class AppLog:
    message: str
    timestamp: float

    def __init__(self, message: str, timestamp: float):
        self.message = message
        self.timestamp = timestamp

    @classmethod
    def create(cls, message: str) -> "AppLog":
        timestamp = time.time()
        return cls(message, timestamp)
