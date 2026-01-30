# Microsservice Telemetry Toolkit

Uma biblioteca Python para adicionar telemetria (tracing) aos seus microsserviços usando OpenTelemetry.

## Características

- ✅ Interface simples e intuitiva para criação de spans e traces
- ✅ Integração com OpenTelemetry
- ✅ Exportação para OTLP (OpenTelemetry Protocol)
- ✅ Validação automática de nomes de spans
- ✅ Suporte a spans aninhados
- ✅ Métricas (Counter, Gauge, Histogram, UpDownCounter)
- ✅ Logging estruturado com OpenTelemetry
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

### Métricas

A biblioteca oferece suporte a diferentes tipos de métricas OpenTelemetry:

#### Counter - Contador Monotônico

Use para valores que apenas aumentam (ex: total de requisições, erros, etc.):

```python
from microsservice_telemetry_toolkit import OtelAppTracer

app_tracer = OtelAppTracer(
    service_name="meu-servico",
    otlp_endpoint="http://localhost:4318/v1/metrics"
)

# Criar um contador
requests_counter = app_tracer.create_counter(
    name="http.requests.total",
    unit="requests",
    description="Total de requisições HTTP recebidas"
)

# Incrementar o contador
requests_counter.add(1, attributes={"method": "GET", "status": 200})
requests_counter.add(1, attributes={"method": "POST", "status": 201})
```

#### Gauge - Medidor de Valor Atual

Use para valores que podem subir ou descer (ex: uso de memória, conexões ativas):

```python
# Criar um gauge
memory_gauge = app_tracer.create_gauge(
    name="system.memory.usage",
    unit="bytes",
    description="Uso atual de memória"
)

# Definir o valor atual
memory_gauge.set(1024 * 1024 * 512, attributes={"type": "heap"})
```

#### Histogram - Distribuição de Valores

Use para medir a distribuição de valores (ex: latência de requisições, tamanho de payloads):

```python
# Criar um histograma com breakpoints customizados
latency_histogram = app_tracer.create_histogram(
    name="http.request.duration",
    unit="ms",
    description="Duração das requisições HTTP",
    breakpoints=[10, 50, 100, 200, 500, 1000, 2000, 5000]
)

# Registrar valores
latency_histogram.record(45.3, attributes={"endpoint": "/api/users"})
latency_histogram.record(123.7, attributes={"endpoint": "/api/orders"})
```

#### UpDownCounter - Contador Bidirecional

Use para valores que podem aumentar ou diminuir (ex: itens em fila, conexões ativas):

```python
# Criar um contador bidirecional
queue_counter = app_tracer.create_up_down_counter(
    name="queue.items",
    unit="items",
    description="Número de itens na fila"
)

# Adicionar ou remover itens
queue_counter.add(5)   # Adiciona 5 itens
queue_counter.add(-2)  # Remove 2 itens
```

#### Exemplo Completo com Métricas

```python
from microsservice_telemetry_toolkit import OtelAppTracer
import time

app_tracer = OtelAppTracer(
    service_name="api-ecommerce",
    otlp_endpoint="http://localhost:4318/v1/metrics"
)

# Criar métricas
requests_counter = app_tracer.create_counter("http.requests.total", "requests")
latency_histogram = app_tracer.create_histogram("http.request.duration", "ms")
active_connections = app_tracer.create_up_down_counter("http.connections.active", "connections")
memory_gauge = app_tracer.create_gauge("system.memory.usage", "bytes")

def processar_pedido(pedido_id: str):
    # Incrementar conexões ativas
    active_connections.add(1)
    
    start_time = time.time()
    
    try:
        with app_tracer.start_root_span("api.pedidos.processar") as span:
            span.set_attribute("pedido.id", pedido_id)
            
            # Simular processamento
            time.sleep(0.1)
            
            # Registrar métricas
            requests_counter.add(1, attributes={"endpoint": "/pedidos", "status": "success"})
            
        # Calcular e registrar latência
        duration_ms = (time.time() - start_time) * 1000
        latency_histogram.record(duration_ms, attributes={"endpoint": "/pedidos"})
        
    finally:
        # Decrementar conexões ativas
        active_connections.add(-1)
        
        # Atualizar uso de memória (exemplo simplificado)
        import os
        import psutil
        process = psutil.Process(os.getpid())
        memory_gauge.set(process.memory_info().rss, attributes={"type": "rss"})
```

### Logging

A biblioteca oferece configuração de logging estruturado com OpenTelemetry:

```python
from microsservice_telemetry_toolkit import OtelLogger
import logging

# Configurar logging global
OtelLogger.configure_global_logging(
    service_name="meu-servico",
    service_environment="production",
    log_level=logging.INFO,
    otlp_endpoint="http://localhost:4318/v1/logs",
    headers={"Authorization": "Bearer token"}
)

# Usar o logging padrão do Python
logger = logging.getLogger(__name__)

def processar_dados():
    logger.info("Iniciando processamento de dados")
    logger.debug("Detalhes do processamento...")
    
    try:
        # Seu código aqui
        resultado = realizar_operacao()
        logger.info(f"Processamento concluído com sucesso: {resultado}")
    except Exception as e:
        logger.error(f"Erro ao processar dados: {e}")
        logger.exception("Stack trace completo")
```

#### Configurações de Logging

- **service_name**: Nome do serviço (obrigatório)
- **service_environment**: Ambiente de execução (padrão: "development")
- **log_level**: Nível mínimo de log (padrão: `logging.INFO`)
- **otlp_endpoint**: Endpoint OTLP para exportação (opcional, usa console se não fornecido)
- **headers**: Headers HTTP para autenticação (opcional)

#### Níveis de Log Disponíveis

```python
logger.debug("Mensagem de debug")      # Informações detalhadas para diagnóstico
logger.info("Mensagem informativa")    # Confirmação de funcionamento normal
logger.warning("Mensagem de aviso")    # Indicação de situação inesperada
logger.error("Mensagem de erro")       # Erro que não impede o funcionamento
logger.critical("Mensagem crítica")    # Erro grave que pode impedir o funcionamento
logger.exception("Erro com stack")     # Inclui traceback da exceção
```

#### Exemplo Integrado: Tracing, Métricas e Logging

```python
from microsservice_telemetry_toolkit import OtelAppTracer, OtelLogger
import logging

# Configurar logging
OtelLogger.configure_global_logging(
    service_name="api-usuarios",
    log_level=logging.INFO,
    otlp_endpoint="http://localhost:4318/v1/logs"
)

# Configurar tracing e métricas
app_tracer = OtelAppTracer(
    service_name="api-usuarios",
    otlp_endpoint="http://localhost:4318/v1/traces"
)

# Criar métricas
requests_counter = app_tracer.create_counter("api.requests.total", "requests")
errors_counter = app_tracer.create_counter("api.errors.total", "errors")
latency_histogram = app_tracer.create_histogram("api.request.duration", "ms")

logger = logging.getLogger(__name__)

def criar_usuario(nome: str, email: str):
    import time
    start_time = time.time()
    
    logger.info(f"Criando usuário: {email}")
    
    with app_tracer.start_root_span("api.usuarios.criar") as span:
        span.set_attribute("usuario.email", email)
        
        try:
            with app_tracer.start_span_action("validar") as validar_span:
                logger.debug(f"Validando dados do usuário: {email}")
                # Validação...
                validar_span.set_status_ok()
            
            with app_tracer.start_span_action("salvar") as salvar_span:
                logger.debug("Salvando usuário no banco de dados")
                # Salvar...
                salvar_span.set_status_ok()
            
            # Registrar métricas de sucesso
            requests_counter.add(1, attributes={"endpoint": "/usuarios", "status": "success"})
            logger.info(f"Usuário criado com sucesso: {email}")
            
        except Exception as e:
            # Registrar erro em todas as camadas de observabilidade
            logger.error(f"Erro ao criar usuário {email}: {e}")
            span.record_exception(e)
            span.set_status_error(str(e))
            errors_counter.add(1, attributes={"endpoint": "/usuarios", "error_type": type(e).__name__})
            raise
        
        finally:
            # Registrar latência
            duration_ms = (time.time() - start_time) * 1000
            latency_histogram.record(duration_ms, attributes={"endpoint": "/usuarios"})
            logger.debug(f"Requisição concluída em {duration_ms:.2f}ms")
```

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

Você pode usar o Docker Compose para executar um coletor OpenTelemetry local que recebe traces, métricas e logs:

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

Exemplo de configuração (`otel-collector-config.yaml`) para traces, métricas e logs:

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
    metrics:
      receivers: [otlp]
      exporters: [logging]
    logs:
      receivers: [otlp]
      exporters: [logging]
```

### Exemplo Completo de Configuração

Para exportar para um backend de observabilidade (como Jaeger, Prometheus, Grafana Loki):

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318

exporters:
  # Exportar traces para Jaeger
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
  
  # Exportar métricas para Prometheus
  prometheus:
    endpoint: "0.0.0.0:8889"
  
  # Exportar logs para Loki
  loki:
    endpoint: http://loki:3100/loki/api/v1/push
  
  # Console para debug
  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [jaeger, logging]
    metrics:
      receivers: [otlp]
      exporters: [prometheus, logging]
    logs:
      receivers: [otlp]
      exporters: [loki, logging]
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
