# Plano de Testes — API ServeRest

**Versão:** 2.0  
**Autor:** QA Trainee  
**Data:** 2025  
**Repositório:** serverest-tests

---

## 1. Objetivo

Validar o comportamento dos endpoints `/usuarios`, `/login` e `/produtos` da API ServeRest, garantindo que as operações CRUD respondam com os status codes corretos, as mensagens esperadas e a estrutura de dados definida na documentação.

---

## 2. Estratégia

| Item | Decisão |
|---|---|
| Tipo de teste | Testes de API (caixa-preta) |
| Camada | Integração — diretamente contra a API publicada |
| Ferramentas | Python + Pytest + Requests + jsonschema |
| Abordagem | Testes independentes, dados dinâmicos via UUID, fixtures com teardown |
| Execução | Local via `pytest` e automática via GitHub Actions a cada push |

---

## 3. Escopo

### ✅ Coberto

| Endpoint | Métodos cobertos |
|---|---|
| `/usuarios` | GET (lista), GET (por ID), POST, PUT, DELETE |
| `/login` | POST |
| `/produtos` | GET (lista), GET (por ID), POST, PUT, DELETE |

### ❌ Fora do escopo

| Endpoint | Motivo |
|---|---|
| `/carrinhos` | Fora do escopo do desafio desta semana |
| Testes de performance | Fora do escopo (requereria k6 ou Locust) |
| Testes de contrato (Pact) | Complexidade além do nível atual |
| Cenários com parâmetros de query (`_limit`, `nome=X`) | Prioridade baixa; API tem paginação simples |

---

## 4. Cenários a implementar

### `/usuarios`
- [x] GET — listar todos os usuários
- [x] POST — cadastrar usuário válido
- [x] POST — e-mail duplicado (400)
- [x] POST — sem campo `nome` (400)
- [x] POST — sem campo `email` (400)
- [x] GET `/{id}` — usuário existente
- [x] GET `/{id}` — usuário inexistente (400)
- [x] PUT `/{id}` — atualizar existente (200)
- [x] PUT `/{id}` — ID inexistente → upsert (201)
- [x] DELETE `/{id}` — excluir existente (200)
- [x] DELETE `/{id}` — ID inexistente, idempotente (200)

### `/login`
- [x] POST — credenciais corretas (200 + token)
- [x] POST — senha errada (401)
- [x] POST — e-mail inexistente (401)
- [x] POST — sem campo `email` (400)
- [x] POST — sem campo `password` (400)
- [x] POST — campos vazios (400)

### `/produtos`
- [x] GET — listar todos os produtos
- [x] POST — cadastrar com token de admin (201)
- [x] POST — sem token (401)
- [x] POST — nome duplicado (400)
- [x] GET `/{id}` — produto existente (200)
- [x] GET `/{id}` — produto inexistente (400)
- [x] PUT `/{id}` — atualizar com token (200)
- [x] PUT `/{id}` — sem token (401)
- [x] DELETE `/{id}` — excluir com token (200)
- [x] DELETE `/{id}` — ID inexistente, idempotente (200)
- [x] DELETE `/{id}` — sem token (401)

### JSON Schema (Extra 1)
- [x] GET `/usuarios` — validar estrutura da resposta
- [x] POST `/login` — validar estrutura com token
- [x] GET `/produtos` — validar estrutura da resposta

---

## 5. Critérios de qualidade

Um teste está **pronto** quando:

1. **Independente** — passa sozinho (`pytest -k nome_do_teste`) sem depender de outros
2. **Dados limpos** — cria e remove seus próprios dados (fixture com teardown)
3. **Assert específico** — verifica status code **e** pelo menos um campo do body
4. **Nome descritivo** — o nome diz o que testa e o que espera
5. **Sem duplicação** — usa helper para montar payload; não repete código

---

## 6. Riscos identificados

| Risco | Mitigação |
|---|---|
| E-mails duplicados entre execuções | UUID4 no helper `email_unico()` |
| Token expirado entre fixtures | Token gerado a cada fixture `admin_token` |
| Ambiente instável (API fora do ar) | Testes marcam falha clara; CI notifica via Actions |
| Comportamento de upsert no PUT | Documentado e testado explicitamente |
