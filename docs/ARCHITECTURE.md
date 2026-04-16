# Arquitetura da Solução

## Visão Geral

A solução foi desenhada para executar uma aplicação simples (API + frontend) em ambiente AWS, utilizando containers e serviços gerenciados.

A aplicação foi containerizada com Docker e validada localmente com docker-compose. Para execução em cloud, foi escolhida a arquitetura baseada em ECS Fargate, com imagens armazenadas no ECR e exposição via Application Load Balancer (ALB).

A infraestrutura foi definida utilizando Terraform, com separação em módulos (VPC, ECS, ALB e ECR), permitindo reutilização e facilidade de manutenção.

---

## Diagrama de Arquitetura

O diagrama da arquitetura está disponível em:

- `docs/architecture.drawio`
- `docs/architecture.png`

---

## Componentes

### Rede (VPC)

| Componente | Descrição | CIDR |
|------------|-----------|------|
| VPC | Rede principal da aplicação | 10.0.0.0/16 |
| Public Subnet 1 | Subnet pública para ALB | 10.0.1.0/24 |
| Public Subnet 2 | Subnet pública para alta disponibilidade | 10.0.2.0/24 |
| Private Subnet 1 | Subnet privada para execução dos containers | 10.0.11.0/24 |
| Private Subnet 2 | Subnet privada para execução dos containers | 10.0.12.0/24 |

---

### Compute

| Aspecto | Decisão | Justificativa |
|---------|---------|---------------|
| Plataforma | ECS Fargate | evita gerenciamento de instâncias e reduz complexidade |
| Tipo de execução | Serverless containers | ideal para workloads simples e escaláveis |
| Auto Scaling | Não implementado | pode ser adicionado futuramente baseado em CPU/memória |

---

### Segurança

- **Security Groups**: ALB exposto na internet, ECS restrito às subnets privadas  
- **IAM Roles**: role de execução para tasks ECS com permissões mínimas necessárias  
- **Secrets Management**: uso de variáveis de ambiente (sem hardcode de credenciais)  
- **Network ACLs**: configuração padrão da VPC mantida  

---

## Fluxo de Deploy

---

## Estimativa de Custos

Cenário considerado: ~30 mil requisições/mês

| Serviço | Especificação | Custo Mensal Estimado |
|---------|---------------|----------------------|
| ECS Fargate | 2 containers (API + frontend) | ~US$ 18 |
| ALB | 1 load balancer | ~US$ 16–20 |
| NAT Gateway | 1 gateway | ~US$ 30–35 |
| ECR | armazenamento de imagens | ~US$ 1–5 |
| **Total** | | **~US$ 65–75** |

Obs: o NAT Gateway representa a maior parte do custo e pode ser otimizado em ambientes de desenvolvimento.

---

## Escalabilidade

### Horizontal

A aplicação pode escalar aumentando o número de tasks no ECS.

O scaling pode ser configurado com base em:
- CPU
- memória
- número de requisições

### Vertical

A aplicação suporta ajuste de CPU e memória das tasks no ECS.

---

## Alta Disponibilidade

- Multi-AZ: Sim  
- Réplicas: arquitetura preparada para múltiplas tasks  
- Health Checks: endpoint `/health` da API preparado para uso com ALB  

---

## Disaster Recovery

| Métrica | Objetivo | Implementação |
|---------|----------|---------------|
| RPO (Recovery Point Objective) | próximo de 0 | aplicação stateless, sem banco persistente |
| RTO (Recovery Time Objective) | até 15 minutos | recriação rápida via Terraform |

A estratégia de DR considera recriação da infraestrutura em outra região AWS utilizando o código Terraform.

---

## Observabilidade

### Logs
- Centralizados via CloudWatch Logs  
- Acesso por grupos de logs dos serviços ECS  

### Métricas
- CPU e memória das tasks  
- status dos containers  
- health checks da aplicação  

### Alertas
- Não implementados nesta etapa  
- Como melhoria futura: CloudWatch Alarms para falhas e indisponibilidade  

---

## Limitações Conhecidas

1. Auto Scaling não implementado → pode ser adicionado com métricas do CloudWatch  
2. Pipeline ainda sem deploy automatizado completo → evolução futura  
3. Observabilidade básica → pode evoluir com Grafana/Prometheus ou Datadog  
4. Sem banco persistente → possível evolução com RDS ou DynamoDB  

---

## Referências

- AWS Well-Architected Framework  
- Terraform Registry  
- AWS Pricing Calculator  
- Draw.io  