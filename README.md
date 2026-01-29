# Microsservice Telemetry Toolkit

Uma biblioteca Python para adicionar telemetria (tracing) aos seus microsserviços usando OpenTelemetry.

## Características

- ✅ Interface simples e intuitiva para criação de spans e traces
- ✅ Integração com OpenTelemetry
- ✅ Exportação para OTLP (OpenTelemetry Protocol)
- ✅ Validação automática de nomes de spans
- ✅ Suporte a spans aninhados
- ✅ Arquitetura limpa (Clean Architecture)
- ✅ Tipagem completa (type hints)

## Instalação

### Usando uv (recomendado)

Instalar do PyPI:
```bash
uv add python-service-telemetry-toolkit
```

Instalar diretamente do repositório Git:
```bash
uv add git+https://github.com/gsomenzi/microsservice_telemetry_toolkit.git
```

### Usando pip

Instalar do PyPI:
```bash
pip install python-service-telemetry-toolkit
```

Instalar diretamente do repositório Git:
```bash
pip install git+https://github.com/gsomenzi/microsservice_telemetry_toolkit.git
```

## Uso Básico

### Exemplo Simples

```python
from microsservice_telemetry_toolkit import OtelAppTracer

# Inicializar o tracer
app_tracer = OtelAppTracer(service_name="meu-servico")

# Criar um span raiz
def processar_pedido():
    with app_tracer.start_root_span("servico.pedido.processar") as root_span:
        try:
            # Seu código aqui
            print("Processando pedido...")
            
            # Criar spans aninhados para sub-tarefas
            with app_tracer.start_span_action("validar") as validar_span:
                print("Validando pedido...")
                validar_span.set_attribute("pedido.id", "12345")
            
            with app_tracer.start_span_action("salvar") as salvar_span:
                print("Salvando pedido...")
                salvar_span.set_status_ok()
                
        except Exception as e:
            root_span.record_and_raise_exception(e)

if __name__ == "__main__":
    processar_pedido()
```

### Exportando para OTLP

```python
from microsservice_telemetry_toolkit import (
    OtelAppTracer, 
    HTTPAuthHeaderMapper, 
    Base64TextEncoder
)

# Configurar autenticação usando HTTPAuthHeaderMapper
encoder = Base64TextEncoder()
auth_mapper = HTTPAuthHeaderMapper(encoder)
headers = auth_mapper.map_from_credentials("seu-usuario", "sua-senha")

# Configurar exportação para um coletor OTLP com autenticação
app_tracer = OtelAppTracer(
    service_name="meu-servico",
    otlp_endpoint="http://localhost:4318/v1/traces",
    headers=headers
)

def processar_dados():
    with app_tracer.start_root_span("servico.dados.processar") as span:
        # Seu código aqui
        span.set_attribute("usuario.id", "user-123")
        span.set_status_ok()
```

## Funcionalidades Avançadas

### OtelSpan - Métodos Disponíveis

```python
from microsservice_telemetry_toolkit import OtelAppTracer

app_tracer = OtelAppTracer(service_name="meu-servico")

with app_tracer.start_root_span("servico.operacao.executar") as span:
    # Definir atributos
    span.set_attribute("chave", "valor")
    span.set_attribute("quantidade", 42)
    
    # Definir status
    span.set_status_ok()
    # ou
    span.set_status_error("Descrição do erro")
    
    # Obter contexto do span
    contexto = span.get_context()
    print(f"Trace ID: {contexto['trace_id']}")
    print(f"Span ID: {contexto['span_id']}")
    
    # Registrar exceção
    try:
        # código que pode falhar
        pass
    except Exception as e:
        span.record_exception(e)
        # ou registrar e re-lançar
        span.record_and_raise_exception(e)
```

### Validação de Nomes de Spans

A biblioteca valida automaticamente os nomes dos spans:

- **Span raiz**: Deve ter exatamente 3 partes separadas por `.` (ex: `servico.recurso.acao`)
- **Span de ação**: Deve ter exatamente 1 parte (ex: `validar`, `salvar`)
- Não pode conter caracteres especiais como ``!@#$%^&*()+=[]{}|\;:'",<>/?~``

```python
# ✅ Correto
with app_tracer.start_root_span("usuario.registro.criar"):
    with app_tracer.start_span_action("validar"):
        pass

# ❌ Incorreto - span raiz com apenas 2 partes
with app_tracer.start_root_span("usuario.criar"):
    pass

# ❌ Incorreto - span de ação com múltiplas partes
with app_tracer.start_root_span("usuario.registro.criar"):
    with app_tracer.start_span_action("validar.dados"):
        pass
```

### Componentes Auxiliares

#### Base64TextEncoder

```python
from microsservice_telemetry_toolkit import Base64TextEncoder

encoder = Base64TextEncoder()
encoded = encoder.encode("Hello, World!")
print(encoded)  # SGVsbG8sIFdvcmxkIQ==
```

#### HTTPAuthHeaderMapper

```python
from microsservice_telemetry_toolkit import HTTPAuthHeaderMapper, Base64TextEncoder

encoder = Base64TextEncoder()
auth_mapper = HTTPAuthHeaderMapper(encoder)

headers = auth_mapper.map_from_credentials("usuario", "senha")
print(headers)  # {'Authorization': 'Basic dXN1YXJpbzpzZW5oYQ=='}
```

## Arquitetura

A biblioteca segue os princípios da Clean Architecture:

```
microsservice_telemetry_toolkit/
├── domain/              # Camada de domínio (interfaces e regras de negócio)
│   ├── port/           # Portas (interfaces abstratas)
│   │   ├── generic_tracer.py      # Interface do tracer
│   │   ├── text_encoder.py        # Interface para encoders
│   │   └── chain_handler.py       # Pattern Chain of Responsibility
│   └── value_object/   # Objetos de valor
│       └── app_log.py
├── application/         # Camada de aplicação (casos de uso)
│   └── services/
│       ├── span_name_validator.py  # Validador de nomes
│       └── http_auth_header_mapper.py
└── infrastructure/      # Camada de infraestrutura (implementações)
    ├── otel_app_tracer.py         # Implementação do tracer
    ├── otel_span.py               # Wrapper do span
    └── base64_text_encoder.py     # Implementação do encoder
```

## Exemplos Completos

### Exemplo com Flask

```python
from flask import Flask
from microsservice_telemetry_toolkit import OtelAppTracer

app = Flask(__name__)
app_tracer = OtelAppTracer(
    service_name="api-usuarios",
    otlp_endpoint="http://otel-collector:4318/v1/traces"
)

@app.route("/usuarios/<user_id>")
def obter_usuario(user_id):
    with app_tracer.start_root_span("api.usuarios.obter") as span:
        span.set_attribute("usuario.id", user_id)
        
        with app_tracer.start_span_action("buscar") as buscar_span:
            # Buscar usuário no banco de dados
            usuario = {"id": user_id, "nome": "João"}
            buscar_span.set_attribute("resultado.encontrado", True)
        
        with app_tracer.start_span_action("serializar") as serializar_span:
            # Serializar resposta
            serializar_span.set_status_ok()
        
        return usuario

if __name__ == "__main__":
    app.run()
```

### Exemplo com FastAPI

```python
from fastapi import FastAPI
from microsservice_telemetry_toolkit import OtelAppTracer

app = FastAPI()
app_tracer = OtelAppTracer(
    service_name="api-pedidos",
    otlp_endpoint="http://otel-collector:4318/v1/traces"
)

@app.post("/pedidos")
async def criar_pedido(pedido: dict):
    with app_tracer.start_root_span("api.pedidos.criar") as span:
        span.set_attribute("pedido.valor", pedido.get("valor", 0))
        
        with app_tracer.start_span_action("validar") as validar_span:
            # Validar pedido
            validar_span.set_status_ok()
        
        with app_tracer.start_span_action("processar") as processar_span:
            # Processar pedido
            processar_span.set_attribute("pedido.id", "123")
            processar_span.set_status_ok()
        
        return {"id": "123", "status": "criado"}
```

## Integração com OpenTelemetry Collector

Você pode usar o Docker Compose para executar um coletor OpenTelemetry local:

```yaml
version: '3'
services:
  otel-collector:
    image: otel/opentelemetry-collector:latest
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4318:4318"   # OTLP HTTP receiver
      - "55679:55679" # zpages extension
```

Exemplo de configuração (`otel-collector-config.yaml`):

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318

exporters:
  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [logging]
```

## Requisitos

- Python >= 3.14
- opentelemetry-api >= 1.39.1
- opentelemetry-sdk >= 1.39.1
- opentelemetry-exporter-otlp-proto-http >= 1.39.1

## Desenvolvimento

### Instalação para Desenvolvimento

```bash
# Clonar o repositório
git clone https://github.com/gsomenzi/microsservice_telemetry_toolkit.git
cd microsservice_telemetry_toolkit

# Instalar dependências com uv
uv sync
```

### Executar Exemplo

```bash
uv run python main.py
```

## Contribuindo

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

## Licença

Este projeto está licenciado sob a licença MIT.

## Autor

Guilherme Somenzi (@gsomenzi)
