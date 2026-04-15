# API - DevOps Challenge

API REST de gerenciamento de itens desenvolvida com FastAPI.

## Endpoints

### Core API (v1)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/items` | Lista todos os itens (com paginação e filtros) |
| POST | `/api/v1/items` | Cria um novo item |
| GET | `/api/v1/items/{id}` | Busca item por ID |
| PUT | `/api/v1/items/{id}` | Atualiza um item |
| DELETE | `/api/v1/items/{id}` | Remove item por ID |
| GET | `/api/v1/users/me` | Informações do usuário atual |

### Operacional

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Health check da aplicação |
| GET | `/ready` | Readiness probe (Kubernetes) |
| GET | `/metrics` | Métricas da aplicação |

### Legacy (compatibilidade)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/items` | Lista itens (legado) |
| POST | `/api/items` | Cria item (legado) |
| GET | `/api/items/{id}` | Busca item (legado) |
| DELETE | `/api/items/{id}` | Remove item (legado) |

## Executar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Ou diretamente
python main.py
```

## Executar Testes

```bash
pytest -v
```

## Documentação da API

Com a aplicação rodando em modo debug, acesse:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `PORT` | Porta da aplicação | 8000 |
| `HOST` | Host para bind | 0.0.0.0 |
| `LOG_LEVEL` | Nível de log | DEBUG |
| `DEBUG` | Modo debug | true |
| `API_KEY` | Chave de API | - |
| `DATABASE_URL` | URL do banco de dados | - |
| `ENVIRONMENT` | Nome do ambiente | development |

## Notas para o Candidato

Esta aplicação simula um sistema real. Seu trabalho inclui:

1. **Criar o Dockerfile** otimizado (multi-stage, non-root, etc.)
2. **Configurar health checks** adequados no container
3. **Gerenciar variáveis de ambiente** de forma segura
4. **Garantir segurança** da imagem e da aplicação
5. **Analisar o código** e identificar possíveis melhorias

Documente quaisquer problemas ou melhorias identificadas no código.
