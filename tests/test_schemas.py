"""
Extra 1 — Validação de JSON Schema em 3 endpoints.
Garante que a estrutura da resposta não mudou, além do status code.
"""
import requests
import pytest
from jsonschema import validate, ValidationError
from utils.helpers import BASE_URL


# ── Schemas ────────────────────────────────────────────────────────────────

SCHEMA_LISTA_USUARIOS = {
    "type": "object",
    "required": ["quantidade", "usuarios"],
    "properties": {
        "quantidade": {"type": "integer"},
        "usuarios": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["_id", "nome", "email", "password", "administrador"],
                "properties": {
                    "_id":           {"type": "string"},
                    "nome":          {"type": "string"},
                    "email":         {"type": "string", "format": "email"},
                    "password":      {"type": "string"},
                    "administrador": {"type": "string", "enum": ["true", "false"]},
                },
            },
        },
    },
}

SCHEMA_LOGIN_SUCESSO = {
    "type": "object",
    "required": ["message", "authorization"],
    "properties": {
        "message":       {"type": "string"},
        "authorization": {"type": "string", "pattern": "^Bearer .+"},
    },
}

SCHEMA_LISTA_PRODUTOS = {
    "type": "object",
    "required": ["quantidade", "produtos"],
    "properties": {
        "quantidade": {"type": "integer"},
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["_id", "nome", "preco", "descricao", "quantidade"],
                "properties": {
                    "_id":       {"type": "string"},
                    "nome":      {"type": "string"},
                    "preco":     {"type": "number"},
                    "descricao": {"type": "string"},
                    "quantidade":{"type": "integer"},
                },
            },
        },
    },
}


# ── Testes ─────────────────────────────────────────────────────────────────

def test_schema_lista_usuarios():
    """GET /usuarios deve retornar estrutura válida conforme schema."""
    r = requests.get(f"{BASE_URL}/usuarios")
    assert r.status_code == 200
    try:
        validate(instance=r.json(), schema=SCHEMA_LISTA_USUARIOS)
    except ValidationError as e:
        pytest.fail(f"Schema inválido em GET /usuarios: {e.message}")


def test_schema_login_sucesso(usuario_criado):
    """POST /login bem-sucedido deve retornar schema com token Bearer."""
    r = requests.post(
        f"{BASE_URL}/login",
        json={"email": usuario_criado["email"], "password": usuario_criado["password"]},
    )
    assert r.status_code == 200
    try:
        validate(instance=r.json(), schema=SCHEMA_LOGIN_SUCESSO)
    except ValidationError as e:
        pytest.fail(f"Schema inválido em POST /login: {e.message}")


def test_schema_lista_produtos():
    """GET /produtos deve retornar estrutura válida conforme schema."""
    r = requests.get(f"{BASE_URL}/produtos")
    assert r.status_code == 200
    try:
        validate(instance=r.json(), schema=SCHEMA_LISTA_PRODUTOS)
    except ValidationError as e:
        pytest.fail(f"Schema inválido em GET /produtos: {e.message}")
