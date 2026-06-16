"""
Configurações e fixtures globais do Pytest.

As fixtures definidas aqui ficam disponíveis para todos os
arquivos de teste sem necessidade de importação explícita.
"""
import pytest
import requests

from utils.helpers import build_user_payload


# ---------------------------------------------------------------------------
# Fixture: base_url
# ---------------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addini(
        "base_url",
        "URL base da API"
    )
@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    """
    Retorna a URL base da API lida do pytest.ini.
    Escopo 'session' → criada uma única vez por execução.
    """
    return pytestconfig.getini("base_url")


# ---------------------------------------------------------------------------
# Fixture: created_user
# ---------------------------------------------------------------------------

@pytest.fixture
def created_user(base_url: str) -> dict: # pyright: ignore[reportInvalidTypeForm]
    """
    Cria um usuário real na API antes do teste e o remove após.

    Escopo padrão ('function') → cada teste recebe um usuário
    diferente, garantindo isolamento completo entre os testes.

    Yields:
        dict: Dados do usuário criado, incluindo '_id' retornado pela API.

    Teardown:
        Deleta o usuário ao final do teste, independente de sucesso/falha.
    """
    payload = build_user_payload()
    response = requests.post(f"{base_url}/usuarios", json=payload)

    assert response.status_code == 201, (
        f"Falha ao criar usuário na fixture. "
        f"Status: {response.status_code} | Body: {response.text}"
    )

    user_id = response.json().get("_id")
    user_data = {**payload, "_id": user_id}

    yield user_data

    # --- Teardown: remove o usuário criado ---
    requests.delete(f"{base_url}/usuarios/{user_id}")
