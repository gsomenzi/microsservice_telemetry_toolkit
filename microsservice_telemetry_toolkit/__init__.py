"""
Microsservice Telemetry Toolkit

A library for telemetry (tracing) in Python microservices using OpenTelemetry.

Main exports:
    - OtelAppTracer: Main tracer implementation for creating spans
    - OtelSpan: Span wrapper with utility methods
    - GenericTracer: Abstract tracer interface (port)
    - TextEncoder: Abstract text encoder interface (port)
    - Base64TextEncoder: Base64 text encoder implementation
    - HTTPAuthHeaderMapper: Helper for creating HTTP auth headers
"""

# Core tracing components
from .infrastructure import Base64TextEncoder, OtelAppTracer, OtelSpan

# Domain ports (interfaces)
from .domain import GenericTracer, TextEncoder

# Application services
from .application import HTTPAuthHeaderMapper

__version__ = "0.1.0"

__all__ = [
    # Main tracing components
    "OtelAppTracer",
    "OtelSpan",
    # Interfaces/Ports
    "GenericTracer",
    "TextEncoder",
    # Implementations
    "Base64TextEncoder",
    # Services
    "HTTPAuthHeaderMapper",
]
