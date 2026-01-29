"""
Microsservice Telemetry Toolkit

Uma biblioteca para telemetria (rastreamento) em microsserviços Python usando OpenTelemetry.

Principais exportações:
    - OtelAppTracer: Implementação principal do tracer para criação de spans
    - OtelSpan: Wrapper de span com métodos utilitários
    - GenericTracer: Interface abstrata do tracer (porta)
    - TextEncoder: Interface abstrata de codificador de texto (porta)
    - Base64TextEncoder: Implementação de codificador de texto em Base64
    - HTTPAuthHeaderMapper: Auxiliar para criação de cabeçalhos de autenticação HTTP
"""

# Componentes principais de rastreamento
from .infrastructure import Base64TextEncoder, OtelAppTracer, OtelSpan

# Portas do domínio (interfaces)
from .domain import GenericTracer, TextEncoder

# Serviços da aplicação
from .application import HTTPAuthHeaderMapper

__version__ = "0.1.0"

__all__ = [
    # Componentes principais de rastreamento
    "OtelAppTracer",
    "OtelSpan",
    # Interfaces/Portas
    "GenericTracer",
    "TextEncoder",
    # Implementações
    "Base64TextEncoder",
    # Serviços
    "HTTPAuthHeaderMapper",
]
