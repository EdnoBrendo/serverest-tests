"""
Testes para POST /login.
Cobre: credenciais corretas, senha errada, email inexistente, campos vazios.
"""
import requests
from utils.helpers import BASE_URL, payload_usuario


def test_login_credenciais_corretas(usuario_criado):
    """Login com e-mail e senha válidos deve retornar 200 e um token Bearer."""
    r = requests.post(
        f"{BASE_URL}/login",
        json={"email": usuario_criado["email"], "password": usuario_criado["password"]},
    )
    assert r.status_code == 200
    body = r.json()
    assert "authorization" in body
    assert body["authorization"].startswith("Bearer ")


def test_login_senha_errada(usuario_criado):
    """Senha incorreta deve retornar 401."""
    r = requests.post(
        f"{BASE_URL}/login",
        json={"email": usuario_criado["email"], "password": "senha_errada"},
    )
    assert r.status_code == 401


def test_login_email_inexistente():
    """E-mail não cadastrado deve retornar 401."""
    r = requests.post(
        f"{BASE_URL}/login",
        json={"email": "naoexiste@email.com", "password": "qualquer"},
    )
    assert r.status_code == 401


def test_login_sem_email():
    """Payload sem o campo 'email' deve retornar 400."""
    r = requests.post(f"{BASE_URL}/login", json={"password": "senha123"})
    assert r.status_code == 400


def test_login_sem_password():
    """Payload sem o campo 'password' deve retornar 400."""
    r = requests.post(f"{BASE_URL}/login", json={"email": "x@x.com"})
    assert r.status_code == 400


def test_login_campos_vazios():
    """Ambos os campos vazios devem retornar 400."""
    r = requests.post(f"{BASE_URL}/login", json={"email": "", "password": ""})
    assert r.status_code == 400
