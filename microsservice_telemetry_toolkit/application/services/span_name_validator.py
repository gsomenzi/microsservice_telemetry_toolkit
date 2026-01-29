from typing import Any
from ...domain.port.chain_handler import ChainHandler


class IsValidString(ChainHandler):
    def handle(self, request: str) -> Any:
        if not isinstance(request, str) or not request.strip():
            return {"error": "invalid string"}
        return super().handle(request)


class HasValidParts(ChainHandler):
    def __init__(self, parts_count: int = 1):
        self.parts_count = parts_count

    def handle(self, request: str) -> Any:
        parts = request.split(".")
        if len(parts) != self.parts_count:
            return {
                "error": f"String must have exactly {self.parts_count} parts separated by '.'"
            }
        return super().handle(request)


class HasInvalidCharacters(ChainHandler):
    def handle(self, request: str) -> Any:
        invalid_chars = set("!@#$%^&*()+=[]{}|\\;:'\",<>/?`~")
        if any(char in invalid_chars for char in request):
            return {"error": "String contains invalid characters"}
        return super().handle(request)


class SpanNameValidator:
    def __init__(self, parts_count: int = 3):
        self.parts_count = parts_count

    def validate(self, span_name: str) -> Any:
        chain = IsValidString()
        parts_handler = chain.set_next(HasValidParts(parts_count=self.parts_count))
        parts_handler.set_next(HasInvalidCharacters())
        result = chain.handle(span_name)
        if result is not None:
            raise ValueError(result["error"])
        return None
