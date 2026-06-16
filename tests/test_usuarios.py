"""
Testes automatizados para o endpoint /usuarios da API ServeRest.

Cobertura:
    GET    /usuarios            → listar usuários
    POST   /usuarios            → cadastrar usuário (sucesso, erros)
    GET    /usuarios/{id}       → buscar por ID (existente e inexistente)
    PUT    /usuarios/{id}       → atualizar (existente e inexistente)
    DELETE /usuarios/{id}       → excluir (existente e inexistente)
"""
import requests
import pytest

from utils.helpers import build_user_payload, generate_unique_email


# ===========================================================================
# GET /usuarios
# ===========================================================================

class TestGetUsuarios:

    def test_listar_usuarios_retorna_status_200(self, base_url):
        """
        Verifica que a listagem de usuários responde com HTTP 200
        e que o corpo contém a chave 'quantidade' com valor inteiro.
        """
        response = requests.get(f"{base_url}/usuarios")

        assert response.status_code == 200
        body = response.json()
        assert "quantidade" in body, "Chave 'quantidade' ausente na resposta"
        assert isinstance(body["quantidade"], int), "'quantidade' deve ser inteiro"
        assert "usuarios" in body, "Chave 'usuarios' ausente na resposta"
        assert isinstance(body["usuarios"], list), "'usuarios' deve ser uma lista"

    def test_listar_usuarios_retorna_lista_nao_vazia(self, base_url, created_user):
        """
        Garante que, após criar um usuário via fixture,
        a listagem retorna ao menos um registro.
        """
        response = requests.get(f"{base_url}/usuarios")

        assert response.status_code == 200
        body = response.json()
        assert body["quantidade"] >= 1, "A lista de usuários não pode estar vazia"


# ===========================================================================
# POST /usuarios
# ===========================================================================

class TestPostUsuarios:

    def test_cadastrar_usuario_valido_retorna_status_201(self, base_url):
        """
        Cadastro com payload completo e válido deve retornar HTTP 201
        e a mensagem de sucesso com o '_id' do novo usuário.
        """
        payload = build_user_payload()
        response = requests.post(f"{base_url}/usuarios", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert "message" in body
        assert body["message"] == "Cadastro realizado com sucesso"
        assert "_id" in body, "Resposta deve conter '_id' do usuário criado"

        # Teardown manual: remove o usuário recém-criado
        requests.delete(f"{base_url}/usuarios/{body['_id']}")

    def test_cadastrar_usuario_com_email_duplicado_retorna_status_400(
        self, base_url, created_user
    ):
        """
        Tentar cadastrar um segundo usuário com o mesmo e-mail
        deve retornar HTTP 400 com mensagem de conflito.
        A fixture 'created_user' já criou o usuário com o e-mail usado aqui.
        """
        payload = build_user_payload(email=created_user["email"])
        response = requests.post(f"{base_url}/usuarios", json=payload)

        assert response.status_code == 400
        body = response.json()
        assert "message" in body
        assert "já cadastrado" in body["message"].lower() or \
               "email" in body["message"].lower(), (
            f"Mensagem inesperada: {body['message']}"
        )

    def test_cadastrar_usuario_sem_email_retorna_status_400(self, base_url):
        """
        Payload sem o campo 'email' deve ser rejeitado com HTTP 400,
        indicando que o campo é obrigatório.
        """
        payload = {
            "nome": "Sem Email",
            "password": "senha123",
            "administrador": "false",
        }
        response = requests.post(f"{base_url}/usuarios", json=payload)

        assert response.status_code == 400
        body = response.json()
        assert "email" in body, "Resposta deve indicar o campo 'email' como inválido"

    def test_cadastrar_usuario_sem_nome_retorna_status_400(self, base_url):
        """
        Payload sem o campo 'nome' deve ser rejeitado com HTTP 400,
        indicando que o campo é obrigatório.
        """
        payload = {
            "email": generate_unique_email(),
            "password": "senha123",
            "administrador": "false",
        }
        response = requests.post(f"{base_url}/usuarios", json=payload)

        assert response.status_code == 400
        body = response.json()
        assert "nome" in body, "Resposta deve indicar o campo 'nome' como inválido"

    def test_cadastrar_usuario_sem_password_retorna_status_400(self, base_url):
        """
        Payload sem o campo 'password' deve ser rejeitado com HTTP 400.
        Testa mais um campo obrigatório para aumentar a cobertura.
        """
        payload = {
            "nome": "Sem Senha",
            "email": generate_unique_email(),
            "administrador": "false",
        }
        response = requests.post(f"{base_url}/usuarios", json=payload)

        assert response.status_code == 400
        body = response.json()
        assert "password" in body, "Resposta deve indicar o campo 'password' como inválido"


# ===========================================================================
# GET /usuarios/{id}
# ===========================================================================

class TestGetUsuarioById:

    def test_buscar_usuario_existente_retorna_status_200(
        self, base_url, created_user
    ):
        """
        Busca por ID de um usuário previamente criado pela fixture.
        Deve retornar HTTP 200 e os dados corretos do usuário.
        """
        user_id = created_user["_id"]
        response = requests.get(f"{base_url}/usuarios/{user_id}")

        assert response.status_code == 200
        body = response.json()
        assert body["_id"] == user_id
        assert body["nome"] == created_user["nome"]
        assert body["email"] == created_user["email"]

    def test_buscar_usuario_inexistente_retorna_status_400(self, base_url):
        """
        Busca por ID que não existe na base.
        A ServeRest retorna HTTP 400 com mensagem indicando que
        o usuário não foi encontrado.
        """
        id_inexistente = "id_que_nao_existe_000"
        response = requests.get(f"{base_url}/usuarios/{id_inexistente}")

        assert response.status_code == 400
        body = response.json()
        assert "message" in body
        assert "não encontrado" in body["message"].lower() or \
               "nao encontrado" in body["message"].lower(), (
            f"Mensagem inesperada: {body['message']}"
        )


# ===========================================================================
# PUT /usuarios/{id}
# ===========================================================================

class TestPutUsuario:

    def test_atualizar_usuario_existente_retorna_status_200(
        self, base_url, created_user
    ):
        """
        Atualização de um usuário existente deve retornar HTTP 200
        e confirmar a operação com mensagem de sucesso.
        """
        user_id = created_user["_id"]
        payload = build_user_payload(name="Nome Atualizado")

        response = requests.put(f"{base_url}/usuarios/{user_id}", json=payload)

        assert response.status_code == 200
        body = response.json()
        assert "message" in body
        assert "sucesso" in body["message"].lower(), (
            f"Mensagem inesperada: {body['message']}"
        )

    def test_atualizar_usuario_inexistente_cria_usuario_retorna_status_201(
        self, base_url
    ):
        """
        Comportamento específico da ServeRest:
        PUT em um ID inexistente CRIA um novo usuário (upsert)
        e retorna HTTP 201. Esse comportamento é documentado e intencional.
        """
        id_inexistente = "id_inexistente_put_999"
        payload = build_user_payload(name="Usuário Upsert")

        response = requests.put(
            f"{base_url}/usuarios/{id_inexistente}", json=payload
        )

        assert response.status_code == 201
        body = response.json()
        assert "message" in body
        assert "_id" in body, "PUT upsert deve retornar '_id' do usuário criado"

        # Teardown manual: remove o usuário criado pelo upsert
        requests.delete(f"{base_url}/usuarios/{body['_id']}")


# ===========================================================================
# DELETE /usuarios/{id}
# ===========================================================================

class TestDeleteUsuario:

    def test_excluir_usuario_existente_retorna_status_200(self, base_url):
        """
        Criação e exclusão de um usuário em sequência.
        Não usa a fixture 'created_user' aqui para ter controle
        total sobre o ciclo de vida do recurso neste teste.
        """
        # Arrange: cria o usuário manualmente
        payload = build_user_payload()
        post_response = requests.post(f"{base_url}/usuarios", json=payload)
        assert post_response.status_code == 201
        user_id = post_response.json()["_id"]

        # Act: deleta o usuário criado
        delete_response = requests.delete(f"{base_url}/usuarios/{user_id}")

        # Assert
        assert delete_response.status_code == 200
        body = delete_response.json()
        assert "message" in body
        assert "excluído" in body["message"].lower() or \
               "excluido" in body["message"].lower() or \
               "sucesso" in body["message"].lower(), (
            f"Mensagem inesperada: {body['message']}"
        )

    def test_excluir_usuario_inexistente_retorna_status_200_sem_exclusao(
        self, base_url
    ):
        """
        Comportamento específico da ServeRest:
        DELETE em ID inexistente retorna HTTP 200 com mensagem informativa,
        indicando que nenhum registro foi excluído (idempotência).
        """
        id_inexistente = "id_inexistente_delete_000"
        response = requests.delete(f"{base_url}/usuarios/{id_inexistente}")

        assert response.status_code == 200
        body = response.json()
        assert "message" in body
        assert "nenhum registro excluído" in body["message"].lower() or \
               "nao foi encontrado" in body["message"].lower() or \
               "não foi encontrado" in body["message"].lower() or \
               "0" in body["message"], (
            f"Mensagem inesperada: {body['message']}"
        )
