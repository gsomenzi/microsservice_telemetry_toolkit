from ..domain.port.generic_logger import GenericLogger


class OtelLogger(GenericLogger):
    def log(self, message: str) -> None: ...
