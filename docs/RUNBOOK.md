# Runbook Operacional

> **NOTA**: Este é um template. O candidato deve preencher com os procedimentos específicos da implementação.

## Índice

1. [Informações Gerais](#informações-gerais)
2. [Acessos e Credenciais](#acessos-e-credenciais)
3. [Procedimentos de Deploy](#procedimentos-de-deploy)
4. [Troubleshooting](#troubleshooting)
5. [Procedimentos de Rollback](#procedimentos-de-rollback)
6. [Escalação](#escalação)

---

## Informações Gerais

### Ambientes

| Ambiente | URL | Descrição |
|----------|-----|-----------|
| Staging | `https://staging.example.com` | Ambiente de testes |
| Production | `https://app.example.com` | Ambiente produtivo |

### Contatos

| Papel | Nome | Contato |
|-------|------|---------|
| Tech Lead | _Nome_ | _email/slack_ |
| DevOps | _Nome_ | _email/slack_ |
| On-call | _Rotação_ | _PagerDuty/etc_ |

### Repositórios

| Repositório | URL | Descrição |
|-------------|-----|-----------|
| Aplicação | _URL_ | Código fonte |
| Infra | _URL_ | Terraform/IaC |

---

## Acessos e Credenciais

### AWS Console

```
URL: https://console.aws.amazon.com
Account ID: XXXXXXXXXXXX
Região principal: us-east-1
```

### Kubectl (se EKS)

```bash
# Configurar acesso ao cluster
aws eks update-kubeconfig --name <cluster-name> --region <region>

# Verificar conexão
kubectl get nodes
```

### Secrets

| Secret | Localização | Descrição |
|--------|-------------|-----------|
| DB Password | AWS Secrets Manager | `arn:aws:secretsmanager:...` |
| API Keys | GitHub Secrets | `NOME_DO_SECRET` |

---

## Procedimentos de Deploy

### Deploy Automático (CI/CD)

O deploy é disparado automaticamente quando:

1. **Staging**: Push/merge para branch `develop`
2. **Production**: Push/merge para branch `main` + aprovação manual

### Deploy Manual (Emergência)

> ⚠️ Use apenas em caso de emergência quando o CI/CD não estiver disponível.

#### API

```bash
# 1. Build da imagem
docker build -t api:emergency -f apps/api/Dockerfile apps/api/

# 2. Tag para ECR
docker tag api:emergency <account>.dkr.ecr.<region>.amazonaws.com/api:emergency

# 3. Login no ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com

# 4. Push
docker push <account>.dkr.ecr.<region>.amazonaws.com/api:emergency

# 5. Atualizar serviço (ECS)
aws ecs update-service --cluster <cluster> --service api --force-new-deployment

# 5. Atualizar deployment (EKS)
kubectl set image deployment/api api=<account>.dkr.ecr.<region>.amazonaws.com/api:emergency
```

#### Frontend

```bash
# Seguir mesmo processo substituindo 'api' por 'frontend'
```

### Verificação Pós-Deploy

```bash
# 1. Verificar health check
curl https://<url>/health

# 2. Verificar logs
# ECS
aws logs tail /ecs/<service> --follow

# EKS
kubectl logs -f deployment/<deployment-name>

# 3. Verificar métricas no CloudWatch/Grafana
```

---

## Troubleshooting

### API não responde

#### Sintomas
- Health check retornando erro
- Timeouts nas requisições

#### Diagnóstico

```bash
# 1. Verificar status dos containers
# ECS
aws ecs describe-services --cluster <cluster> --services api

# EKS
kubectl get pods -l app=api
kubectl describe pod <pod-name>

# 2. Verificar logs
kubectl logs <pod-name> --tail=100

# 3. Verificar conectividade
kubectl exec -it <pod-name> -- curl localhost:8000/health

# 4. Verificar recursos
kubectl top pods
```

#### Soluções Comuns

| Problema | Solução |
|----------|---------|
| OOMKilled | Aumentar limits de memória |
| CrashLoopBackOff | Verificar logs, corrigir código |
| ImagePullBackOff | Verificar credenciais ECR |
| Connection refused | Verificar Security Groups |

### Frontend não carrega

#### Diagnóstico

```bash
# 1. Verificar se o container está rodando
kubectl get pods -l app=frontend

# 2. Verificar configuração do Nginx
kubectl exec -it <pod> -- nginx -t

# 3. Verificar se API_URL está configurada
kubectl exec -it <pod> -- cat /usr/share/nginx/html/index.html | grep API_URL
```

### Banco de Dados

#### Conexão recusada

```bash
# 1. Verificar Security Groups
aws ec2 describe-security-groups --group-ids <sg-id>

# 2. Verificar se RDS está acessível
nc -zv <rds-endpoint> 5432

# 3. Testar credenciais
psql -h <endpoint> -U <user> -d <database>
```

---

## Procedimentos de Rollback

### Rollback Automático

O pipeline está configurado para rollback automático se:
- Health check falhar após deploy
- Testes de smoke falharem

### Rollback Manual

#### Via GitHub Actions

1. Acesse o repositório no GitHub
2. Vá para Actions → Workflows → CD Production
3. Encontre o último deploy bem-sucedido
4. Clique em "Re-run all jobs"

#### Via CLI

```bash
# EKS - Rollback para revisão anterior
kubectl rollout undo deployment/api
kubectl rollout undo deployment/frontend

# Verificar histórico de revisões
kubectl rollout history deployment/api

# Rollback para revisão específica
kubectl rollout undo deployment/api --to-revision=<number>

# ECS - Deploy de task definition anterior
aws ecs update-service \
  --cluster <cluster> \
  --service api \
  --task-definition api:<previous-revision>
```

#### Via Terraform

```bash
# 1. Identificar estado anterior
cd terraform/environments/production
terraform state list

# 2. Se necessário, reverter via Git
git log --oneline terraform/
git checkout <commit-hash> -- terraform/

# 3. Aplicar
terraform plan
terraform apply
```

---

## Escalação

### Níveis de Severidade

| Nível | Descrição | Tempo de Resposta | Quem Acionar |
|-------|-----------|-------------------|--------------|
| SEV1 | Sistema totalmente indisponível | 15 min | Tech Lead + CTO |
| SEV2 | Funcionalidade crítica afetada | 30 min | Tech Lead |
| SEV3 | Funcionalidade menor afetada | 2 horas | DevOps |
| SEV4 | Problemas cosméticos | 24 horas | Time de desenvolvimento |

### Fluxo de Escalação

```
1. Identificar severidade
2. Criar incidente no [PagerDuty/Slack/etc]
3. Notificar stakeholders conforme severidade
4. Iniciar troubleshooting
5. Documentar ações tomadas
6. Realizar post-mortem (SEV1/SEV2)
```

### Canais de Comunicação

| Canal | Uso |
|-------|-----|
| #incidents | Comunicação durante incidentes |
| #devops | Dúvidas gerais de infraestrutura |
| PagerDuty | Alertas críticos |

---

## Manutenção Programada

### Checklist Pré-Manutenção

- [ ] Comunicar stakeholders com 48h de antecedência
- [ ] Preparar rollback plan
- [ ] Verificar backups recentes
- [ ] Agendar janela de manutenção

### Checklist Pós-Manutenção

- [ ] Verificar todos os health checks
- [ ] Validar funcionalidades principais
- [ ] Monitorar métricas por 30 minutos
- [ ] Comunicar conclusão aos stakeholders

---

## Appendix

### Comandos Úteis

```bash
# Ver todos os recursos no namespace
kubectl get all -n <namespace>

# Descrever um recurso
kubectl describe <resource-type> <resource-name>

# Port-forward para debug local
kubectl port-forward pod/<pod-name> 8080:8000

# Acessar shell do container
kubectl exec -it <pod-name> -- /bin/sh

# Ver eventos recentes
kubectl get events --sort-by='.lastTimestamp'

# Verificar quotas
kubectl describe resourcequota

# AWS - Listar tarefas ECS
aws ecs list-tasks --cluster <cluster> --service-name <service>

# AWS - Descrever tarefa
aws ecs describe-tasks --cluster <cluster> --tasks <task-arn>
```

### Links Úteis

- [AWS Console](https://console.aws.amazon.com)
- [Grafana Dashboard](https://grafana.example.com)
- [Logs (CloudWatch/ELK)](https://logs.example.com)
- [CI/CD (GitHub Actions)](https://github.com/org/repo/actions)
