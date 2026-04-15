# Guia de Contribuição

Obrigado por participar do nosso processo seletivo! 🎉

## Como Entregar o Desafio

### 1. Fork do Repositório

Faça um fork deste repositório para sua conta pessoal do GitHub.

### 2. Clone e Crie sua Branch

```bash
git clone https://github.com/SEU-USUARIO/devops-challenge.git
cd devops-challenge
git checkout -b feature/seu-nome
```

### 3. Desenvolva sua Solução

- Siga a estrutura sugerida no README principal
- Faça commits frequentes e descritivos
- Documente suas decisões

### 4. Commits

Use mensagens de commit claras e descritivas:

```
feat: adiciona Dockerfile para API
fix: corrige health check no nginx
docs: documenta decisão de arquitetura EKS
chore: atualiza dependências do Python
```

Prefixos sugeridos:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `chore`: Tarefas de manutenção
- `refactor`: Refatoração de código
- `test`: Adição/modificação de testes

### 5. Abra o Pull Request

1. Faça push da sua branch
2. Abra um Pull Request para a branch `main` do repositório original
3. Preencha o template de PR completamente
4. Aguarde o feedback

## Padrões de Código

### Terraform

```hcl
# Use 2 espaços para indentação
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "my-vpc"
  }
}
```

### Python

```python
# Siga PEP 8
# Use type hints quando possível
def health_check(url: str, timeout: int = 30) -> bool:
    """Check if the service is healthy."""
    pass
```

### Shell Script

```bash
#!/bin/bash
set -euo pipefail  # Sempre use isso

# Use variáveis com ${VAR} ao invés de $VAR
echo "Hello, ${NAME}"
```

## Dúvidas?

Abra uma Issue com a label `question`.
