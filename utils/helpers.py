"""
Utilitários reutilizáveis para os testes da API ServeRest.
"""
import uuid


def generate_unique_email() -> str:
    """
    Gera um endereço de e-mail único utilizando UUID4.
    Garante que cada teste trabalhe com um e-mail diferente,
    eliminando conflitos de dados entre execuções.

    Returns:
        str: E-mail único no formato 'qa_<uuid>@test.com'.
    """
    return f"qa_{uuid.uuid4().hex[:12]}@test.com"


def build_user_payload(
    name: str = "Usuário Teste",
    email: str = None,
    password: str = "senha123",
    admin: str = "false",
) -> dict:
    """
    Monta o payload padrão para criação/atualização de usuário.
    Recebe parâmetros opcionais para personalizar o payload em
    cenários de teste específicos (ex.: omitir campo obrigatório).

    Args:
        name:     Nome do usuário.
        email:    E-mail do usuário. Se None, gera um único automaticamente.
        password: Senha do usuário.
        admin:    Flag de administrador ('true' ou 'false').

    Returns:
        dict: Payload pronto para ser enviado via requests.
    """
    payload = {
        "password": password,
        "administrador": admin,
    }

    if name is not None:
        payload["nome"] = name

    if email is not None:
        payload["email"] = email
    else:
        payload["email"] = generate_unique_email()

    return payload
