# 🚀 Desafio Técnico - DevOps Pleno

Bem-vindo(a) ao desafio técnico para a posição de **DevOps Pleno**!

Este teste foi desenvolvido para avaliar suas habilidades em infraestrutura como código, containerização, CI/CD, automação e boas práticas de segurança.

## 📋 Índice

- [Contexto](#-contexto)
- [O Desafio](#-o-desafio)
- [Requisitos Técnicos](#-requisitos-técnicos)
- [Critérios de Avaliação](#-critérios-de-avaliação)
- [Entrega](#-entrega)
- [Aplicações Base](#-aplicações-base)
- [Dúvidas](#-dúvidas)

---

## 🎯 Contexto

Você foi contratado para implementar a infraestrutura e o pipeline de CI/CD de uma aplicação composta por:

- **API Backend**: Uma API REST simples (fornecida neste repositório)
- **Frontend**: Uma aplicação web básica que consome a API (fornecida neste repositório)

Sua missão é containerizar essas aplicações e criar toda a infraestrutura necessária para executá-las em um ambiente cloud (AWS), utilizando Infrastructure as Code e práticas modernas de DevOps.

---

## 🏆 O Desafio

### Parte 1: Containerização

- [ ] Criar `Dockerfile` otimizado para a API (multi-stage build)
- [ ] Criar `Dockerfile` otimizado para o Frontend (multi-stage build)
- [ ] Criar `docker-compose.yml` para desenvolvimento local
- [ ] Garantir que as imagens sigam boas práticas de segurança (non-root user, minimal base image, etc.)

### Parte 2: Infrastructure as Code (Terraform/OpenTofu)

Criar módulos Terraform/OpenTofu reutilizáveis para provisionar a infraestrutura na AWS:

- [ ] **Módulo de Rede**: VPC, Subnets (públicas e privadas), Internet Gateway, NAT Gateway, Route Tables
- [ ] **Módulo de Compute**: Escolha uma das opções abaixo:
  - **Opção A**: EKS (Kubernetes gerenciado)
  - **Opção B**: ECS (Fargate ou EC2)
  - **Opção C**: EC2 com Docker
- [ ] **Módulo de Container Registry**: ECR para armazenar as imagens Docker
- [ ] **Módulo de Load Balancer**: ALB para distribuição de tráfego
- [ ] **Módulo de Banco de Dados** (opcional/bonus): RDS ou DynamoDB

**Requisitos dos módulos:**
- Devem ser parametrizáveis via variáveis
- Devem ter outputs bem definidos
- Devem incluir tags padrão para recursos
- Devem seguir convenções de nomenclatura

### Parte 3: Automação com Scripts

Criar scripts de automação para tarefas operacionais:

- [ ] **Script de Health Check** (Python ou Shell): Verificar saúde da API e enviar alertas
- [ ] **Script de Backup** (Shell ou PowerShell): Automatizar backup de configurações/dados
- [ ] **Script de Deploy** (Python ou Shell): Automatizar processo de deploy
- [ ] **Script de Limpeza** (qualquer linguagem): Remover recursos órfãos (imagens antigas, logs, etc.)

### Parte 4: Pipeline CI/CD

Implementar um pipeline completo usando GitHub Actions (ou outra ferramenta de sua escolha):

#### CI (Continuous Integration)
- [ ] Lint e validação de código
- [ ] Testes unitários
- [ ] Build das imagens Docker
- [ ] Scan de vulnerabilidades nas imagens (Trivy, Snyk, etc.)
- [ ] Análise estática de segurança (SAST)
- [ ] Validação do Terraform (fmt, validate, plan)

#### CD (Continuous Deployment)
- [ ] Push das imagens para o registry
- [ ] Deploy automatizado para ambiente de staging (on merge to develop)
- [ ] Deploy para produção com aprovação manual (on merge to main)
- [ ] Rollback automatizado em caso de falha

#### Segurança no Pipeline
- [ ] Secrets gerenciados de forma segura
- [ ] Scan de dependências (Dependabot, Snyk)
- [ ] Verificação de IaC (tfsec, checkov)
- [ ] DAST (opcional/bonus)

---

## 📌 Requisitos Técnicos

### Obrigatórios
- Terraform >= 1.5.0 ou OpenTofu >= 1.6.0
- Docker >= 24.0
- Python >= 3.10 (para scripts)
- GitHub Actions (ou justificar alternativa)
- AWS como cloud provider

### Desejáveis
- Kubernetes (se escolher EKS)
- Helm Charts
- Ansible para configuração
- Observabilidade (Prometheus, Grafana, CloudWatch)

---

## ✅ Critérios de Avaliação

### Terraform/OpenTofu (25%)
| Critério | Peso |
|----------|------|
| Modularização e reusabilidade | Alto |
| Uso correto de variáveis e outputs | Alto |
| State management (remote state, locking) | Médio |
| Segurança (IAM, Security Groups) | Alto |
| Documentação dos módulos | Médio |

### Containerização (20%)
| Critério | Peso |
|----------|------|
| Otimização das imagens (tamanho, layers) | Alto |
| Multi-stage builds | Alto |
| Segurança (non-root, vulnerabilidades) | Alto |
| Docker Compose funcional | Médio |

### CI/CD (25%)
| Critério | Peso |
|----------|------|
| Pipeline completo e funcional | Alto |
| Testes e validações | Alto |
| Segurança no pipeline | Alto |
| Estratégia de deploy (blue-green, canary) | Médio |
| Tratamento de falhas e rollback | Médio |

### Automação/Scripts (15%)
| Critério | Peso |
|----------|------|
| Funcionalidade | Alto |
| Tratamento de erros | Alto |
| Logging e outputs | Médio |
| Código limpo e documentado | Médio |

### Documentação e Organização (15%)
| Critério | Peso |
|----------|------|
| README claro e completo | Alto |
| Decisões técnicas documentadas | Alto |
| Runbook operacional | Médio |
| Diagrama de arquitetura | Médio |
| Organização do repositório | Alto |

---

## 📦 Entrega

1. Faça um **fork** deste repositório
2. Crie uma **branch** com seu nome: `feature/seu-nome`
3. Implemente o desafio
4. Atualize a documentação conforme necessário
5. Abra um **Pull Request** para a branch `main` deste repositório
6. No PR, inclua:
   - Resumo das implementações
   - Decisões técnicas importantes
   - Instruções para executar localmente
   - Screenshots/evidências dos pipelines funcionando
   - Estimativa de custos da infraestrutura (AWS Calculator)

### ⏰ Prazo

- **7 dias corridos** a partir do recebimento do teste
- Se precisar de mais tempo, comunique com antecedência

### ⚠️ Importante

- **NÃO** provisione recursos reais na AWS (a menos que solicitado)
- O Terraform deve estar pronto para ser executado, mas vamos avaliar o código
- Para demonstrar o CI/CD, pode usar recursos gratuitos (GitHub Actions, etc.)
- Commits frequentes e bem descritos são valorizados

---

## 🔧 Aplicações Base

### API (Python/FastAPI)

Localização: `apps/api/`

Uma API REST simples com os seguintes endpoints:
- `GET /health` - Health check
- `GET /api/items` - Lista itens
- `POST /api/items` - Cria um item
- `GET /api/items/{id}` - Busca item por ID

### Frontend (React/HTML)

Localização: `apps/frontend/`

Uma aplicação web simples que:
- Lista os itens da API
- Permite criar novos itens
- Exibe status de conexão com a API

---

## 💡 Dicas

1. **Comece pelo básico**: Containerização e docker-compose funcionando
2. **Modularize desde o início**: Evite refatorações grandes depois
3. **Documente decisões**: Por que escolheu EKS ao invés de ECS? Por que essa imagem base?
4. **Automatize tudo**: Se você fez manualmente mais de uma vez, deveria ser um script
5. **Pense em segurança**: Princípio do menor privilégio sempre
6. **Commits atômicos**: Pequenos commits com mensagens claras

---

## ❓ Dúvidas

Se tiver dúvidas sobre o desafio, abra uma **Issue** neste repositório com a label `question`.

Responderemos em até 24 horas úteis.

---

## 📄 Licença

Este desafio é para fins de avaliação técnica apenas.

---

**Boa sorte! 🍀**

*Estamos ansiosos para ver sua solução!*
# entrevista.devops.desafio
# entrevista.devops.desafio
# entrevista.devops.desafio
