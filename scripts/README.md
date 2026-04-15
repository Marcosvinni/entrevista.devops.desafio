# Scripts de Automação

Este diretório deve conter os scripts de automação para tarefas operacionais.

## Scripts Requeridos

### 1. Health Check

Script para verificar a saúde da aplicação e serviços.

**Requisitos**:
- Verificar endpoints de health
- Suportar múltiplos serviços
- Enviar alertas em caso de falha
- Exit codes apropriados

### 2. Backup

Script para automatizar backup de configurações e dados importantes.

**Requisitos**:
- Backup do Terraform state
- Rotação de backups antigos
- Upload para storage (S3)
- Logging

### 3. Deploy

Script para automatizar o processo de deploy.

**Requisitos**:
- Aceitar parâmetros (ambiente, versão)
- Verificar pré-requisitos
- Health check pós-deploy
- Rollback em caso de falha

### 4. Cleanup

Script para remover recursos órfãos e otimizar custos.

**Requisitos**:
- Listar recursos não utilizados (imagens ECR antigas, etc)
- Modo dry-run obrigatório
- Confirmação antes de deletar

## Requisitos Gerais

Todos os scripts devem:

- Ter tratamento de erros
- Suportar --help
- Usar logging adequado
- Ter exit codes significativos
- Ser idempotentes quando possível

## Linguagens Aceitas

- Python 3.10+
- Bash/Shell
- PowerShell (para backup)

## Variáveis de Ambiente

Os scripts devem suportar configuração via variáveis de ambiente:

| Variável | Descrição |
|----------|-----------|
| `AWS_REGION` | Região AWS |
| `API_URL` | URL da API para health check |
| `SLACK_WEBHOOK` | Webhook para notificações |
| `S3_BUCKET` | Bucket para backups |
| `LOG_LEVEL` | Nível de logging (DEBUG, INFO, WARN, ERROR) |
