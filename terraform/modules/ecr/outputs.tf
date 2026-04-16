output "repository_names" {
  description = "Nomes dos repositórios criados"
  value       = { for k, v in aws_ecr_repository.this : k => v.name }
}

output "repository_urls" {
  description = "URLs dos repositórios criados"
  value       = { for k, v in aws_ecr_repository.this : k => v.repository_url }
}