"""
Testes para /produtos.
Fluxo de autenticação: cadastro exige token de usuário administrador.
"""
import requests
from utils.helpers import BASE_URL, payload_produto


# ── GET /produtos ──────────────────────────────────────────────────────────

def test_listar_produtos():
    """Listagem pública de produtos deve retornar 200 com lista."""
    r = requests.get(f"{BASE_URL}/produtos")
    assert r.status_code == 200
    body = r.json()
    assert "produtos" in body
    assert isinstance(body["produtos"], list)


# ── POST /produtos ─────────────────────────────────────────────────────────

def test_cadastrar_produto_com_token_admin(admin_token):
    """Admin autenticado deve conseguir cadastrar produto (201)."""
    headers = {"Authorization": admin_token}
    r = requests.post(f"{BASE_URL}/produtos", json=payload_produto(), headers=headers)
    assert r.status_code == 201
    body = r.json()
    assert "_id" in body
    # Teardown manual
    requests.delete(f"{BASE_URL}/produtos/{body['_id']}", headers=headers)


def test_cadastrar_produto_sem_token():
    """Requisição sem token deve ser rejeitada com 401."""
    r = requests.post(f"{BASE_URL}/produtos", json=payload_produto())
    assert r.status_code == 401


def test_cadastrar_produto_nome_duplicado(admin_token, produto_criado):
    """Nome de produto já existente deve retornar 400."""
    headers = {"Authorization": admin_token}
    payload = payload_produto(nome=produto_criado["nome"])
    r = requests.post(f"{BASE_URL}/produtos", json=payload, headers=headers)
    assert r.status_code == 400


# ── GET /produtos/{id} ─────────────────────────────────────────────────────

def test_buscar_produto_existente(produto_criado):
    """Busca por ID existente deve retornar 200 com dados do produto."""
    r = requests.get(f"{BASE_URL}/produtos/{produto_criado['_id']}")
    assert r.status_code == 200
    body = r.json()
    assert body["_id"] == produto_criado["_id"]
    assert body["nome"] == produto_criado["nome"]


def test_buscar_produto_inexistente():
    """Busca por ID que não existe deve retornar 400."""
    r = requests.get(f"{BASE_URL}/produtos/id_nao_existe_xyz")
    assert r.status_code == 400


# ── PUT /produtos/{id} ─────────────────────────────────────────────────────

def test_atualizar_produto_existente(admin_token, produto_criado):
    """Admin deve conseguir atualizar produto existente (200)."""
    headers = {"Authorization": admin_token}
    payload = payload_produto(nome=f"Produto Atualizado {produto_criado['_id'][:4]}")
    r = requests.put(
        f"{BASE_URL}/produtos/{produto_criado['_id']}",
        json=payload,
        headers=headers,
    )
    assert r.status_code == 200


def test_atualizar_produto_sem_token(produto_criado):
    """PUT sem token deve retornar 401."""
    r = requests.put(
        f"{BASE_URL}/produtos/{produto_criado['_id']}",
        json=payload_produto(),
    )
    assert r.status_code == 401


# ── DELETE /produtos/{id} ──────────────────────────────────────────────────

def test_deletar_produto_existente(admin_token):
    """Admin deve conseguir deletar produto criado por ele mesmo (200)."""
    headers = {"Authorization": admin_token}
    r = requests.post(f"{BASE_URL}/produtos", json=payload_produto(), headers=headers)
    produto_id = r.json()["_id"]

    r = requests.delete(f"{BASE_URL}/produtos/{produto_id}", headers=headers)
    assert r.status_code == 200


def test_deletar_produto_inexistente(admin_token):
    """DELETE em ID inexistente deve retornar 200 (idempotente)."""
    headers = {"Authorization": admin_token}
    r = requests.delete(f"{BASE_URL}/produtos/id_inexistente_del", headers=headers)
    assert r.status_code == 200


def test_deletar_produto_sem_token(produto_criado):
    """DELETE sem token deve retornar 401."""
    r = requests.delete(f"{BASE_URL}/produtos/{produto_criado['_id']}")
    assert r.status_code == 401
