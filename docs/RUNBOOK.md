# Runbook Operacional

A aplicação é composta por uma API e um frontend, ambos containerizados com Docker e executados localmente via docker-compose. Em ambiente cloud, a arquitetura foi desenhada para execução em ECS Fargate, com exposição via Application Load Balancer (ALB) e uso de serviços gerenciados da AWS.

## Informações Gerais

O ambiente local pode ser acessado através do docker-compose, com o frontend disponível em http://localhost:3000 e a API em http://localhost:8000. A infraestrutura cloud foi definida de forma conceitual utilizando Terraform, com foco em ECS, ALB, VPC e ECR.

O repositório contendo a aplicação e a infraestrutura está disponível em:
https://github.com/Marcosvinni/entrevista.devops.desafio

## Acesso

O acesso à AWS é feito via console (https://console.aws.amazon.com), utilizando a região us-east-1. Os principais serviços utilizados são ECS, ECR, ALB, VPC e CloudWatch.

## Deploy

O fluxo principal de deploy é realizado via GitHub Actions. A cada push no repositório, o pipeline executa o build das aplicações, validações de segurança com Trivy e validação da infraestrutura Terraform.

Para execução local, o deploy pode ser realizado com:

```bash
docker-compose up -d