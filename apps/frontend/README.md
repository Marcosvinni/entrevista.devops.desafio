# Frontend - DevOps Challenge

Aplicação web de gerenciamento de itens para interagir com a API.

## Tecnologias

- HTML5
- CSS3 (Vanilla)
- JavaScript (Vanilla)
- Nginx (para servir em produção)

## Funcionalidades

- Verificação de status da API (health check)
- Listagem de itens com filtros
- Criação de novos itens
- Edição de itens
- Remoção de itens
- Visualização de métricas
- Configuração dinâmica da URL da API
- Interface responsiva

## Executar Localmente

### Opção 1: Servidor HTTP simples

```bash
# Python 3
python -m http.server 3000

# Node.js
npx http-server -p 3000
```

### Opção 2: Com Nginx

Use a configuração `nginx.conf` fornecida.

## Configuração

A URL da API pode ser configurada de várias formas:

1. **Variável global no HTML**: `window.API_BASE_URL` ou `window.ENV_API_URL`
2. **LocalStorage**: Através da aba de configurações na interface
3. **Substituição em runtime**: Via entrypoint do container

## Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `API_URL` | URL da API backend | http://localhost:8000 |

## Notas para o Candidato

Esta aplicação frontend simula um sistema real. Seu trabalho inclui:

1. **Criar o Dockerfile** otimizado usando Nginx
2. **Configurar a URL da API** via variável de ambiente em runtime
3. **Garantir segurança** da imagem e configuração do Nginx
4. **Implementar health check** no container
5. **Analisar a configuração** do Nginx e identificar possíveis melhorias

Documente quaisquer problemas ou melhorias identificadas.
