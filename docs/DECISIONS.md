# Registro de Decisões Técnicas (ADR)

> **NOTA**: Este é um template. O candidato deve documentar suas decisões técnicas seguindo este formato.

Este documento registra as decisões arquiteturais importantes tomadas durante o desenvolvimento deste projeto, seguindo o padrão [Architecture Decision Records (ADR)](https://adr.github.io/).

---

## ADR-001: Escolha da Plataforma de Compute

### Status
_Proposta | Aceita | Deprecada | Substituída_

### Contexto
_Precisamos escolher onde executar os containers da API e Frontend. As opções disponíveis são:_
- _Amazon EKS (Kubernetes gerenciado)_
- _Amazon ECS (Fargate ou EC2)_
- _Amazon EC2 com Docker_

### Decisão
_Escolhemos **[OPÇÃO]** porque..._

### Consequências

**Positivas:**
- _Benefício 1_
- _Benefício 2_

**Negativas:**
- _Trade-off 1_
- _Trade-off 2_

### Alternativas Consideradas

| Opção | Prós | Contras |
|-------|------|---------|
| EKS | _Kubernetes nativo, escalabilidade_ | _Complexidade, custo_ |
| ECS Fargate | _Serverless, simplicidade_ | _Vendor lock-in_ |
| EC2 + Docker | _Controle total, custo_ | _Gerenciamento manual_ |

---

## ADR-002: Estratégia de CI/CD

### Status
_Proposta | Aceita | Deprecada | Substituída_

### Contexto
_Precisamos definir a ferramenta e estratégia de CI/CD para o projeto._

### Decisão
_Escolhemos **GitHub Actions** porque..._

### Consequências

**Positivas:**
- _Integração nativa com GitHub_
- _Runners gratuitos_
- _Marketplace de actions_

**Negativas:**
- _Limitações de tempo em runners gratuitos_

---

## ADR-003: Estratégia de Deploy

### Status
_Proposta | Aceita | Deprecada | Substituída_

### Contexto
_Precisamos definir como os deploys serão realizados para minimizar downtime e riscos._

### Decisão
_Implementamos **[Blue-Green / Canary / Rolling Update]** porque..._

### Consequências

**Positivas:**
- _Rollback rápido_
- _Zero downtime_

**Negativas:**
- _Custo adicional (para blue-green)_

---

## ADR-004: Gerenciamento de Estado do Terraform

### Status
_Proposta | Aceita | Deprecada | Substituída_

### Contexto
_O estado do Terraform precisa ser armazenado de forma segura e acessível pela equipe._

### Decisão
_Utilizamos **S3 + DynamoDB** para remote state porque..._

### Consequências

**Positivas:**
- _State compartilhado entre a equipe_
- _Locking para evitar conflitos_
- _Versionamento do state_

**Negativas:**
- _Necessidade de bootstrap inicial_

---

## ADR-005: Imagem Base dos Containers

### Status
_Proposta | Aceita | Deprecada | Substituída_

### Contexto
_Precisamos escolher imagens base para os Dockerfiles que balanceiem segurança, tamanho e compatibilidade._

### Decisão

| Aplicação | Imagem Base | Justificativa |
|-----------|-------------|---------------|
| API | _python:3.11-slim / alpine_ | _..._ |
| Frontend | _nginx:alpine_ | _..._ |

### Consequências

**Positivas:**
- _Imagens pequenas_
- _Menos vulnerabilidades_

**Negativas:**
- _Alpine pode ter incompatibilidades_

---

## ADR-006: Estrutura de Módulos Terraform

### Status
_Proposta | Aceita | Deprecada | Substituída_

### Contexto
_Precisamos organizar o código Terraform de forma modular e reutilizável._

### Decisão
_Estrutura de módulos:_

```
terraform/
├── modules/           # Módulos reutilizáveis
│   ├── networking/
│   ├── compute/
│   └── ...
└── environments/      # Configurações por ambiente
    ├── staging/
    └── production/
```

### Consequências

**Positivas:**
- _DRY (Don't Repeat Yourself)_
- _Facilita manutenção_
- _Ambientes consistentes_

**Negativas:**
- _Overhead inicial de estruturação_

---

## ADR-007: Segurança no Pipeline

### Status
_Proposta | Aceita | Deprecada | Substituída_

### Contexto
_Precisamos implementar verificações de segurança automatizadas no pipeline._

### Decisão
_Implementamos as seguintes ferramentas:_

| Tipo | Ferramenta | Fase |
|------|------------|------|
| Container Scan | _Trivy / Snyk_ | _Build_ |
| SAST | _Semgrep / CodeQL_ | _PR_ |
| IaC Security | _tfsec / Checkov_ | _PR_ |
| Dependency Scan | _Dependabot_ | _Contínuo_ |

### Consequências

**Positivas:**
- _Detecção precoce de vulnerabilidades_
- _Compliance automatizado_

**Negativas:**
- _Possíveis falsos positivos_
- _Aumento no tempo de build_

---

## Template para Novas Decisões

```markdown
## ADR-XXX: [Título]

### Status
Proposta | Aceita | Deprecada | Substituída

### Contexto
[Descreva o contexto e o problema]

### Decisão
[Descreva a decisão tomada]

### Consequências
**Positivas:**
- ...

**Negativas:**
- ...

### Alternativas Consideradas
[Liste outras opções avaliadas]
```

---

## Referências

- [ADR GitHub Organization](https://adr.github.io/)
- [Documenting Architecture Decisions - Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
