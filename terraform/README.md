# Terraform / OpenTofu

Este diretório deve conter toda a infraestrutura como código do projeto.

## Requisitos

- Terraform >= 1.5.0 ou OpenTofu >= 1.6.0
- AWS CLI configurado
- Credenciais AWS com permissões adequadas

## Objetivo

Criar módulos Terraform reutilizáveis para provisionar a infraestrutura necessária para executar a API e o Frontend na AWS.

Os módulos devem ser:
- Independentes e parametrizáveis
- Bem documentados
- Seguros por padrão
- Testáveis

## Convenções

### Nomenclatura de Recursos

```
{project}-{environment}-{resource-type}-{identifier}
```

Exemplo: `devops-challenge-staging-vpc`

### Tags Obrigatórias

Todos os recursos devem incluir as seguintes tags:
- `Project`
- `Environment`
- `ManagedBy`
- `Owner`

## Comandos Úteis

```bash
# Inicializar
terraform init

# Formatar código
terraform fmt -recursive

# Validar sintaxe
terraform validate

# Planejar mudanças
terraform plan -out=tfplan

# Aplicar mudanças
terraform apply tfplan
```

## Validação de Segurança

```bash
# tfsec para análise de segurança
tfsec .

# checkov para compliance
checkov -d .
```

## Notas

- Configure remote state para trabalho em equipe
- Nunca commite arquivos `.tfstate` ou `terraform.tfvars` com valores sensíveis
- Use variáveis de ambiente ou AWS Secrets Manager para credenciais
