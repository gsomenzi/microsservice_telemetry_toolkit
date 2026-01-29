# Guia Rápido de Uso

Este guia mostra os exemplos mais comuns de uso da biblioteca.

## Instalação Rápida

```bash
pip install python-service-telemetry-toolkit
```

## Uso Básico - 3 Passos

### 1. Importar e Inicializar

```python
from microsservice_telemetry_toolkit import OtelAppTracer

# Desenvolvimento (saída no console)
tracer = OtelAppTracer(service_name="meu-servico")

# Produção (exportar para OTLP)
tracer = OtelAppTracer(
    service_name="meu-servico",
    otlp_endpoint="http://otel-collector:4318/v1/traces"
)
```

### 2. Criar Span Raiz

```python
with tracer.start_root_span("servico.recurso.acao") as span:
    # Seu código aqui
    span.set_attribute("chave", "valor")
    span.set_status_ok()
```

**Importante:** O nome do span raiz deve ter exatamente 3 partes separadas por `.`

### 3. Criar Spans Aninhados

```python
with tracer.start_root_span("pedido.processamento.criar") as root:
    # Primeira sub-tarefa
    with tracer.start_span_action("validar") as span:
        span.set_attribute("valido", True)
        span.set_status_ok()
    
    # Segunda sub-tarefa
    with tracer.start_span_action("salvar") as span:
        span.set_status_ok()
```

**Importante:** Spans de ação devem ter apenas 1 parte no nome (sem `.`)

## Exemplo Completo

```python
from microsservice_telemetry_toolkit import OtelAppTracer

tracer = OtelAppTracer(service_name="api-usuarios")

def criar_usuario(nome: str, email: str):
    with tracer.start_root_span("usuario.criacao.criar") as span:
        span.set_attribute("usuario.nome", nome)
        span.set_attribute("usuario.email", email)
        
        try:
            # Validar
            with tracer.start_span_action("validar") as val_span:
                if not nome or not email:
                    val_span.set_status_error("Dados inválidos")
                    raise ValueError("Nome e email obrigatórios")
                val_span.set_status_ok()
            
            # Salvar
            with tracer.start_span_action("salvar") as save_span:
                # Salvar no banco de dados
                save_span.set_status_ok()
            
            span.set_status_ok()
            return {"status": "criado"}
            
        except Exception as e:
            span.record_and_raise_exception(e)

# Usar a função
criar_usuario("João", "joao@example.com")
```

## Métodos Úteis do Span

```python
with tracer.start_root_span("servico.recurso.acao") as span:
    # Adicionar atributos
    span.set_attribute("usuario.id", "123")
    span.set_attribute("quantidade", 42)
    
    # Definir status
    span.set_status_ok()
    span.set_status_error("Descrição do erro")
    
    # Obter contexto (trace_id, span_id)
    contexto = span.get_context()
    print(contexto["trace_id"])
    
    # Registrar exceção
    try:
        # código que pode falhar
        pass
    except Exception as e:
        span.record_exception(e)  # Registra e continua
        # ou
        span.record_and_raise_exception(e)  # Registra e re-lança
```

## Componentes Adicionais

### Base64TextEncoder

```python
from microsservice_telemetry_toolkit import Base64TextEncoder

encoder = Base64TextEncoder()
encoded = encoder.encode("texto")  # dGV4dG8=
```

### HTTPAuthHeaderMapper

```python
from microsservice_telemetry_toolkit import (
    HTTPAuthHeaderMapper,
    Base64TextEncoder
)

encoder = Base64TextEncoder()
mapper = HTTPAuthHeaderMapper(encoder)

headers = mapper.map_from_credentials("usuario", "senha")
# {'Authorization': 'Basic dXN1YXJpbzpzZW5oYQ=='}
```

## Dicas

1. **Sempre use span raiz para operações principais** - Use `start_root_span()`
2. **Use spans de ação para sub-tarefas** - Use `start_span_action()`
3. **Adicione atributos relevantes** - Ajuda na busca e análise
4. **Defina status** - OK para sucesso, ERROR para falha
5. **Registre exceções** - Use `record_exception()` ou `record_and_raise_exception()`

## Ver Mais

Para documentação completa, veja o [README.md](README.md) principal.
