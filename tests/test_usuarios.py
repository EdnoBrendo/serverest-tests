"""
Semana 3 (preservado) + pequenos ajustes.
Cobre GET, POST, PUT, DELETE em /usuarios.
"""
import requests
from utils.helpers import BASE_URL, payload_usuario, email_unico


def test_listar_usuarios():
    r = requests.get(f"{BASE_URL}/usuarios")
    assert r.status_code == 200
    assert "usuarios" in r.json()


def test_cadastrar_usuario_valido():
    r = requests.post(f"{BASE_URL}/usuarios", json=payload_usuario())
    assert r.status_code == 201
    body = r.json()
    assert "_id" in body
    requests.delete(f"{BASE_URL}/usuarios/{body['_id']}")


def test_cadastrar_email_duplicado(usuario_criado):
    r = requests.post(
        f"{BASE_URL}/usuarios",
        json=payload_usuario(email=usuario_criado["email"]),
    )
    assert r.status_code == 400


def test_cadastrar_sem_nome():
    payload = {"email": email_unico(), "password": "senha123", "administrador": "false"}
    r = requests.post(f"{BASE_URL}/usuarios", json=payload)
    assert r.status_code == 400


def test_cadastrar_sem_email():
    payload = {"nome": "Sem Email", "password": "senha123", "administrador": "false"}
    r = requests.post(f"{BASE_URL}/usuarios", json=payload)
    assert r.status_code == 400


def test_buscar_usuario_existente(usuario_criado):
    r = requests.get(f"{BASE_URL}/usuarios/{usuario_criado['_id']}")
    assert r.status_code == 200
    assert r.json()["email"] == usuario_criado["email"]


def test_buscar_usuario_inexistente():
    r = requests.get(f"{BASE_URL}/usuarios/id_que_nao_existe")
    assert r.status_code == 400


def test_atualizar_usuario_existente(usuario_criado):
    r = requests.put(
        f"{BASE_URL}/usuarios/{usuario_criado['_id']}",
        json=payload_usuario(nome="Nome Atualizado"),
    )
    assert r.status_code == 200


def test_atualizar_usuario_inexistente():
    r = requests.put(
        f"{BASE_URL}/usuarios/id_inexistente_999",
        json=payload_usuario(),
    )
    assert r.status_code == 201  # ServeRest faz upsert
    requests.delete(f"{BASE_URL}/usuarios/{r.json()['_id']}")


def test_deletar_usuario_existente():
    r = requests.post(f"{BASE_URL}/usuarios", json=payload_usuario())
    user_id = r.json()["_id"]
    r = requests.delete(f"{BASE_URL}/usuarios/{user_id}")
    assert r.status_code == 200


def test_deletar_usuario_inexistente():
    r = requests.delete(f"{BASE_URL}/usuarios/id_inexistente_000")
    assert r.status_code == 200  # idempotente na ServeRest
