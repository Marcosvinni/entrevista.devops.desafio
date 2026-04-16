# Registro de Decisões Técnicas (ADR)

Este documento registra as principais decisões arquiteturais tomadas durante o desenvolvimento da solução.

---

## ADR-001: Escolha da Plataforma de Compute

### Status
Aceita

### Contexto
Era necessário definir a melhor forma de executar os containers da aplicação (API e frontend) em ambiente AWS, considerando simplicidade, custo e esforço operacional.

As opções avaliadas foram:
- Amazon EKS
- Amazon ECS (Fargate ou EC2)
- Amazon EC2 com Docker

### Decisão
Foi escolhido o **Amazon ECS Fargate**, por ser uma solução serverless que elimina a necessidade de gerenciamento de instâncias, reduzindo a complexidade operacional.

### Consequências

**Positivas:**
- Não há necessidade de gerenciar servidores
- Integração simples com outros serviços AWS
- Deploy mais rápido e direto

**Negativas:**
- Menor flexibilidade comparado ao Kubernetes
- Dependência maior da AWS (vendor lock-in)

---

## ADR-002: Estratégia de CI/CD

### Status
Aceita

### Contexto
Era necessário definir uma forma de automatizar build, validação e segurança da aplicação.

### Decisão
Foi escolhido o uso de **GitHub Actions**, pela integração nativa com o repositório e facilidade de configuração.

### Consequências

**Positivas:**
- Integração direta com o código
- Fácil configuração e manutenção
- Permite validação de infraestrutura e segurança no pipeline

**Negativas:**
- Limitações em runners gratuitos
- Pipeline ainda sem etapa completa de deploy

---

## ADR-003: Estratégia de Deploy

### Status
Aceita

### Contexto
Era necessário definir uma estratégia de deploy simples e segura, considerando o escopo do desafio.

### Decisão
Foi adotado um modelo de **recriação do ambiente (rolling simplificado)**, utilizando containers atualizados.

### Consequências

**Positivas:**
- Simplicidade na implementação
- Baixo risco de inconsistência

**Negativas:**
- Pode haver pequeno downtime
- Não implementa estratégias avançadas como blue-green

---

## ADR-004: Gerenciamento de Estado do Terraform

### Status
Parcial

### Contexto
O Terraform precisa manter estado consistente da infraestrutura.

### Decisão
Para o escopo do desafio, o state foi mantido localmente, com estrutura preparada para evolução futura para **remote state em S3 com DynamoDB**.

### Consequências

**Positivas:**
- Simplicidade para desenvolvimento inicial
- Fácil execução local

**Negativas:**
- Não adequado para times ou produção
- Risco de inconsistência em múltiplos usuários

---

## ADR-005: Imagem Base dos Containers

### Status
Aceita

### Contexto
Era necessário escolher imagens base seguras e leves para os containers.

### Decisão

| Aplicação | Imagem Base | Justificativa |
|-----------|-------------|---------------|
| API | python:3.11-slim | imagem leve e compatível |
| Frontend | nginx:alpine | ideal para servir conteúdo estático |

### Consequências

**Positivas:**
- Imagens menores
- Menor superfície de ataque

**Negativas:**
- Possíveis limitações de bibliotecas em imagens mais enxutas

---

## ADR-006: Estrutura de Módulos Terraform

### Status
Aceita

### Contexto
Era necessário organizar o código Terraform de forma reutilizável e escalável.

### Decisão
Foi adotada estrutura modular separando componentes como VPC, ECS, ECR e ALB.

### Consequências

**Positivas:**
- Reutilização de código
- Facilidade de manutenção
- Melhor organização

**Negativas:**
- Maior esforço inicial de estruturação

---

## ADR-007: Segurança no Pipeline

### Status
Aceita

### Contexto
Era necessário garantir validações de segurança no processo de build.

### Decisão
Foi implementado scan de vulnerabilidades com **Trivy** no pipeline de CI.

### Consequências

**Positivas:**
- Identificação de vulnerabilidades nas imagens
- Maior segurança no processo de build

**Negativas:**
- Pode gerar falsos positivos
- Aumenta o tempo do pipeline