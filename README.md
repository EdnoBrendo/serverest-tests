[![Testes API ServeRest](https://github.com/<seu-usuario>/serverest-tests/actions/workflows/testes.yml/badge.svg)](https://github.com/<seu-usuario>/serverest-tests/actions/workflows/testes.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pytest](https://img.shields.io/badge/Pytest-7.x-blue)

# Automação de Testes — API ServeRest

Suíte de testes para os endpoints `/usuarios`, `/login` e `/produtos` da API **ServeRest**, usando **Python + Pytest + Requests**.

---

## Como rodar

```bash
# 1. Clone
git clone https://github.com/EdnoBrendo/serverest-tests.git
cd serverest-tests

# 2. Ambiente virtual
python3 -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Dependências
pip install -r requirements.txt

# 4. Executar tudo
pytest

# Rodar apenas um módulo
pytest tests/test_login.py
pytest tests/test_produtos.py

# Rodar um teste específico
pytest -k "test_login_credenciais_corretas"
```

---

## Estrutura

```
serverest-tests/
├── .github/workflows/testes.yml   # CI — GitHub Actions
├── tests/
│   ├── test_usuarios.py           # 11 testes (Semana 3, preservado)
│   ├── test_login.py              #  6 testes
│   ├── test_produtos.py           # 11 testes
│   └── test_schemas.py            #  3 testes (Extra 1 — JSON Schema)
├── utils/helpers.py               # BASE_URL, email_unico(), payloads
├── conftest.py                    # Fixtures: usuario_criado, admin_token, produto_criado
├── pytest.ini
├── requirements.txt
├── PLANO-DE-TESTES.md
└── README.md
```

---

## Cobertura de testes

Método baseado no artigo [Como verificar a cobertura de testes da API REST](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b) (Nayara Crema).

### Path Coverage — endpoints únicos cobertos

| Endpoint (URI única) | Coberto? |
|---|---|
| `/usuarios` | ✅ |
| `/usuarios/{id}` | ✅ |
| `/login` | ✅ |
| `/produtos` | ✅ |
| `/produtos/{id}` | ✅ |
| `/carrinhos` | ❌ |
| `/carrinhos/{id}` | ❌ |

**Path Coverage = 5 / 7 = 71%**

### Operator Coverage — métodos HTTP cobertos

| Operação | Coberta? |
|---|---|
| GET /usuarios | ✅ |
| POST /usuarios | ✅ |
| PUT /usuarios/{id} | ✅ |
| DELETE /usuarios/{id} | ✅ |
| POST /login | ✅ |
| GET /produtos | ✅ |
| POST /produtos | ✅ |
| PUT /produtos/{id} | ✅ |
| DELETE /produtos/{id} | ✅ |
| GET /carrinhos | ❌ |
| POST /carrinhos | ❌ |
| DELETE /carrinhos/{id} | ❌ |

**Operator Coverage = 9 / 12 = 75%**

### Parameter Coverage — campos obrigatórios testados

Campos cobertos: `nome`, `email`, `password`, `administrador` (usuários), `email`+`password` (login), `nome`, `preco`, `descricao`, `quantidade` (produtos), `Authorization` header.

**Parameter Coverage = ~90%** (parâmetros de query como `?nome=` e `?preco_min=` não foram cobertos)

### Cobertura total estimada

| Critério | Cobertura |
|---|---|
| Path Coverage | 71% |
| Operator Coverage | 75% |
| Parameter Coverage | ~90% |
| **Média** | **~79%** |

### O que ficou fora e por quê

| Item | Motivo |
|---|---|
| `/carrinhos` | Fora do escopo do desafio desta semana |
| Filtros por query string (`?nome=`, `?preco=`) | Prioridade baixa; aumentaria muito o volume |
| Testes de performance | Requer ferramenta dedicada (k6, Locust) |

---

## Subir no GitHub

```bash
git init
git add .
git commit -m "feat: evolução da suíte — login, produtos, schemas e CI"
git remote add origin https://github.com/<seu-usuario>/serverest-tests.git
git push -u origin main
```

Depois do push, o GitHub Actions roda os testes automaticamente. Veja a aba **Actions** do repositório.

---

## Bug encontrado

Veja o bug reportado na aba **[Issues](https://github.com/<seu-usuario>/serverest-tests/issues)** do repositório.

> **Resumo:** `DELETE /usuarios/{id}` e `DELETE /produtos/{id}` com ID inexistente retornam **HTTP 200** em vez do esperado **404**. Embora seja um comportamento intencional da ServeRest (idempotência), pode mascarar erros em clientes que dependem do 404 para detectar recursos ausentes.
