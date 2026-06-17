import pytest
import requests
from utils.helpers import BASE_URL, payload_usuario, payload_produto


# ── Usuário comum ──────────────────────────────────────────────────────────

@pytest.fixture
def usuario_criado():
    """Cria um usuário comum e remove ao final do teste."""
    payload = payload_usuario()
    r = requests.post(f"{BASE_URL}/usuarios", json=payload)
    assert r.status_code == 201, f"Falha ao criar usuário: {r.text}"
    user_id = r.json()["_id"]
    yield {**payload, "_id": user_id}
    requests.delete(f"{BASE_URL}/usuarios/{user_id}")


# ── Usuário administrador + token ──────────────────────────────────────────

@pytest.fixture
def admin_token():
    """
    Cria um usuário administrador, faz login, retorna o token Bearer
    e remove o usuário ao final.
    """
    payload = payload_usuario(nome="Admin Teste", admin="true")
    r = requests.post(f"{BASE_URL}/usuarios", json=payload)
    assert r.status_code == 201, f"Falha ao criar admin: {r.text}"
    user_id = r.json()["_id"]

    login = requests.post(
        f"{BASE_URL}/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login.status_code == 200, f"Falha no login: {login.text}"
    token = login.json()["authorization"]

    yield token

    requests.delete(f"{BASE_URL}/usuarios/{user_id}")


# ── Produto (depende do token de admin) ────────────────────────────────────

@pytest.fixture
def produto_criado(admin_token):
    """Cria um produto como admin e remove ao final do teste."""
    headers = {"Authorization": admin_token}
    payload = payload_produto()
    r = requests.post(f"{BASE_URL}/produtos", json=payload, headers=headers)
    assert r.status_code == 201, f"Falha ao criar produto: {r.text}"
    produto_id = r.json()["_id"]
    yield {**payload, "_id": produto_id}
    requests.delete(f"{BASE_URL}/produtos/{produto_id}", headers=headers)
