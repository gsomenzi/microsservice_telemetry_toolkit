"""
Microsservice Telemetry Toolkit

Uma biblioteca para telemetria (rastreamento e logging) em microsserviços Python usando OpenTelemetry.

Principais exportações:
    - OtelTracer: Implementação principal do tracer para criação de spans
    - OtelSpan: Wrapper de span com métodos utilitários
    - OtelLogger: Configurador global de logging com OpenTelemetry
    - GenericTracer: Interface abstrata do tracer (porta)
    - GenericSpan: Interface abstrata do span (porta)
    - TextEncoder: Interface abstrata de codificador de texto (porta)
    - Base64TextEncoder: Implementação de codificador de texto em Base64
    - HTTPAuthHeaderMapper: Auxiliar para criação de cabeçalhos de autenticação HTTP
"""

# Componentes principais de rastreamento e logging
from .infrastructure import Base64TextEncoder, OtelTracer, OtelSpan, OtelLogger

# Portas do domínio (interfaces)
from .domain import (
    GenericSpan,
    GenericTracer,
    GenericHistogram,
    GenericGauge,
    GenericCounter,
    GenericUpDownCounter,
    TextEncoder,
)

# Serviços da aplicação
from .application import HTTPAuthHeaderMapper

__version__ = "0.1.0"

__all__ = [
    # Componentes principais de rastreamento
    "OtelTracer",
    "OtelSpan",
    "OtelLogger",
    # Interfaces/Portas
    "GenericTracer",
    "GenericSpan",
    "GenericHistogram",
    "GenericGauge",
    "GenericCounter",
    "GenericUpDownCounter",
    "TextEncoder",
    # Implementações
    "Base64TextEncoder",
    # Serviços
    "HTTPAuthHeaderMapper",
]
