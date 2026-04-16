output "cluster_name" {
  description = "Nome do cluster ECS"
  value       = aws_ecs_cluster.this.name
}

output "cluster_id" {
  description = "ID do cluster ECS"
  value       = aws_ecs_cluster.this.id
}

output "api_service_name" {
  description = "Nome do service da API"
  value       = aws_ecs_service.api.name
}

output "frontend_service_name" {
  description = "Nome do service do frontend"
  value       = aws_ecs_service.frontend.name
}

output "api_task_definition_arn" {
  description = "ARN da task definition da API"
  value       = aws_ecs_task_definition.api.arn
}

output "frontend_task_definition_arn" {
  description = "ARN da task definition do frontend"
  value       = aws_ecs_task_definition.frontend.arn
}