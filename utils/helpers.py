import uuid

BASE_URL = "https://compassuol.serverest.dev"


def email_unico():
    """Gera e-mail único com UUID para evitar conflitos entre testes."""
    return f"qa_{uuid.uuid4().hex[:8]}@test.com"


def payload_usuario(nome="QA Teste", email=None, admin="false"):
    return {
        "nome": nome,
        "email": email or email_unico(),
        "password": "senha123",
        "administrador": admin,
    }


def payload_produto(nome=None, preco=100, descricao="Produto de teste", quantidade=10):
    nome = nome or f"Produto {uuid.uuid4().hex[:6]}"
    return {
        "nome": nome,
        "preco": preco,
        "descricao": descricao,
        "quantidade": quantidade,
    }
