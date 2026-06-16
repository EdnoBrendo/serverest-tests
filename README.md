# 🚀 Automação de Testes API ServeRest

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)]()
[![Pytest](https://img.shields.io/badge/Pytest-8.x-green)]()
[![Requests](https://img.shields.io/badge/Requests-2.x-orange)]()
[![API](https://img.shields.io/badge/API-ServeRest-success)]()

Projeto de automação de testes para o endpoint **/usuarios** da API ServeRest utilizando **Python, Pytest e Requests**.

## 🎯 Objetivo

Validar os principais fluxos da API de usuários, cobrindo cenários positivos, negativos e comportamentos específicos da aplicação.

---

## 📂 Estrutura do Projeto

```text
serverest-tests/
│
├── tests/
│   └── test_usuarios.py
│
├── utils/
│   └── helpers.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

### Responsabilidades

| Arquivo            | Responsabilidade                |
| ------------------ | ------------------------------- |
| `test_usuarios.py` | Casos de teste                  |
| `helpers.py`       | Payloads e geração de dados     |
| `conftest.py`      | Fixtures compartilhadas         |
| `pytest.ini`       | Configuração global da execução |

---

## ✅ Cobertura de Testes

### GET /usuarios

* Listar usuários
* Validar retorno da lista
* Buscar usuário existente
* Buscar usuário inexistente

### POST /usuarios

* Cadastro válido
* E-mail duplicado
* Ausência de e-mail
* Ausência de nome
* Ausência de senha

### PUT /usuarios

* Atualização de usuário existente
* Criação via ID inexistente (upsert)

### DELETE /usuarios

* Exclusão de usuário existente
* Exclusão de usuário inexistente

**Total: 13 cenários automatizados**

---

## ⚙️ Arquitetura Utilizada

### Fixtures

A fixture `created_user` cria um usuário antes da execução do teste e realiza a limpeza automaticamente após sua conclusão.

Benefícios:

* Isolamento entre testes
* Independência de execução
* Limpeza automática do ambiente

### Dados Dinâmicos

Os e-mails são gerados dinamicamente através de UUID para evitar conflitos entre execuções.

Exemplo:

```python
qa_4f4f1d5e@test.com
```

### Configuração Centralizada

A URL da API é mantida em um único local:

```ini
[pytest]
base_url = https://compassuol.serverest.dev
```

---

## 🚀 Execução

### Instalação

```bash
pip install -r requirements.txt
```

### Executar todos os testes

```bash
pytest
```

### Executar com relatório HTML

```bash
pytest --html=reports/report.html --self-contained-html
```

### Executar um cenário específico

```bash
pytest -k "nome_do_teste"
```

### Parar na primeira falha

```bash
pytest -x
```

---

## 🔧 Tecnologias

| Tecnologia  | Finalidade              |
| ----------- | ----------------------- |
| Python      | Linguagem principal     |
| Pytest      | Framework de testes     |
| Requests    | Consumo da API          |
| Pytest HTML | Relatórios              |
| UUID        | Geração de dados únicos |

---

## 📈 Resultado Esperado

```text
===================== test session starts =====================

collected 13 items

13 passed

===================== 100% SUCCESS =====================
```

---

