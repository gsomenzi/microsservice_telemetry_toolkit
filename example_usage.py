"""
Exemplo: Usando o toolkit de telemetria em um serviço web simples.

Este exemplo demonstra como usar a biblioteca para adicionar rastreamento
a uma operação típica de microsserviço.
"""

from microsservice_telemetry_toolkit import OtelAppTracer

# Inicializar o tracer com o nome do seu serviço
# Para saída no console (desenvolvimento):
tracer = OtelAppTracer(service_name="user-service")

# Para exportação OTLP (produção):
# tracer = OtelAppTracer(
#     service_name="user-service",
#     otlp_endpoint="http://otel-collector:4318/v1/traces",
#     headers={"Authorization": "Bearer seu-token"}
# )


def create_user(username: str, email: str) -> dict:
    """
    Função de exemplo que cria um usuário com rastreamento.
    """
    # Iniciar um span raiz para a operação principal
    # Nomes de span raiz devem ter exatamente 3 partes: servico.recurso.acao
    with tracer.start_root_span("user.creation.create") as span:
        # Adicionar atributos ao span para melhor observabilidade
        span.set_attribute("user.username", username)
        span.set_attribute("user.email", email)
        
        try:
            # Validar dados do usuário
            with tracer.start_span_action("validate") as validate_span:
                if not username or not email:
                    validate_span.set_status_error("Campos obrigatórios ausentes")
                    raise ValueError("Nome de usuário e email são obrigatórios")
                
                if "@" not in email:
                    validate_span.set_status_error("Formato de email inválido")
                    raise ValueError("Formato de email inválido")
                
                validate_span.set_attribute("validation.result", "success")
                validate_span.set_status_ok()
            
            # Verificar se o usuário existe
            with tracer.start_span_action("check_exists") as check_span:
                # Simular verificação no banco de dados
                user_exists = False  # No código real, consultar o banco de dados
                check_span.set_attribute("user.exists", user_exists)
                
                if user_exists:
                    check_span.set_status_error("Usuário já existe")
                    raise ValueError("Usuário já existe")
                
                check_span.set_status_ok()
            
            # Criar usuário no banco de dados
            with tracer.start_span_action("save") as save_span:
                # Simular salvamento no banco de dados
                user_id = "user-12345"  # No código real, inserir no banco de dados
                save_span.set_attribute("user.id", user_id)
                save_span.set_status_ok()
            
            # Enviar email de boas-vindas
            with tracer.start_span_action("notify") as notify_span:
                # Simular envio de email
                notify_span.set_attribute("notification.type", "email")
                notify_span.set_attribute("notification.recipient", email)
                notify_span.set_status_ok()
            
            # Todas as operações bem-sucedidas
            span.set_status_ok()
            
            return {
                "id": user_id,
                "username": username,
                "email": email,
                "status": "created"
            }
            
        except Exception as e:
            # Registrar a exceção e re-lançá-la
            span.record_and_raise_exception(e)


def get_user(user_id: str) -> dict:
    """
    Função de exemplo que recupera um usuário com rastreamento.
    """
    with tracer.start_root_span("user.retrieval.get") as span:
        span.set_attribute("user.id", user_id)
        
        try:
            # Buscar do banco de dados
            with tracer.start_span_action("fetch") as fetch_span:
                # Simular busca no banco de dados
                user = {
                    "id": user_id,
                    "username": "john_doe",
                    "email": "john@example.com"
                }
                fetch_span.set_attribute("fetch.result", "found")
                fetch_span.set_status_ok()
            
            # Transformar dados
            with tracer.start_span_action("transform") as transform_span:
                # Simular transformação de dados
                transform_span.set_status_ok()
            
            span.set_status_ok()
            return user
            
        except Exception as e:
            span.record_and_raise_exception(e)


def main():
    """Executar operações de exemplo."""
    print("=" * 60)
    print("Exemplo: Serviço de Usuários com Telemetria")
    print("=" * 60)
    print()
    
    # Exemplo 1: Criação bem-sucedida de usuário
    print("1. Criando um novo usuário...")
    try:
        result = create_user("john_doe", "john@example.com")
        print(f"   ✅ Usuário criado com sucesso: {result['id']}")
    except Exception as e:
        print(f"   ❌ Falha ao criar usuário: {e}")
    print()
    
    # Exemplo 2: Criação inválida de usuário (email inválido)
    print("2. Criando usuário com dados inválidos...")
    try:
        result = create_user("jane_doe", "invalid-email")
        print(f"   ✅ Usuário criado: {result['id']}")
    except ValueError as e:
        print(f"   ❌ Validação falhou (esperado): {e}")
    print()
    
    # Exemplo 3: Buscar usuário
    print("3. Recuperando usuário...")
    try:
        user = get_user("user-12345")
        print(f"   ✅ Usuário recuperado: {user['username']}")
    except Exception as e:
        print(f"   ❌ Falha ao recuperar usuário: {e}")
    print()
    
    print("=" * 60)
    print("Exemplo concluído! Verifique a saída do console para os spans.")
    print("=" * 60)


if __name__ == "__main__":
    main()
